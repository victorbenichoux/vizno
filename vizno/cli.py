#!/usr/bin/env python3

import copy
import importlib
import os
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager

import typer
import watchdog.events
import watchdog.observers

realpath = os.path.realpath(__file__)
dir_realpath = os.path.dirname(os.path.dirname(realpath))
sys.path.append(dir_realpath)

import requests

from vizno.report import Report  # noqa: E402


class ReportFileChangedHandler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self, fn, output_dir, **kwargs):
        self.fn = fn
        self.output_dir = output_dir
        super().__init__(**kwargs)

    def on_modified(self, event):
        super(ReportFileChangedHandler, self).on_modified(event)
        print(f"Detected file change in {event.src_path}...")
        render_from_file(self.fn, self.output_dir)


@contextmanager
def add_to_path(p):
    import sys

    old_path = sys.path
    sys.path = sys.path[:]
    sys.path.insert(0, p)
    try:
        yield
    finally:
        sys.path = old_path


def import_report_module(fn):
    fn_dir = os.path.dirname(fn)
    with add_to_path(fn_dir):
        spec = importlib.util.spec_from_file_location(fn, fn)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


def find_and_render(module, output_dir):
    report_name = next(
        v
        for v in dir(module)
        if not v.startswith("__") and isinstance(getattr(module, v), Report)
    )
    report = getattr(module, report_name)
    report.render(output_dir)


def render_from_file(fn, output_dir):
    report_module = import_report_module(fn)
    find_and_render(report_module, output_dir)


app = typer.Typer()


@app.command()
def render(
    report_fn: str, output_dir: str = ".", reload: bool = False, dev: bool = False
):
    fn = os.path.realpath(report_fn)
    report_module = import_report_module(fn)
    find_and_render(report_module, output_dir)
    if reload:
        observer = watchdog.observers.Observer()
        event_handler = ReportFileChangedHandler(fn, output_dir, patterns=[fn])
        observer.schedule(event_handler, os.path.dirname(fn))
        if dev:
            vizno_src_path = os.path.join(dir_realpath, "vizno")
            dev_event_handler = ReportFileChangedHandler(
                fn, output_dir, patterns=["*/index.html", "*.js", "*.py", "*.css"]
            )
            observer.schedule(dev_event_handler, vizno_src_path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


class ReportFileChangedHandlerWithPush(watchdog.events.PatternMatchingEventHandler):
    def __init__(self, fn, output_dir, **kwargs):
        self.fn = fn
        self.output_dir = output_dir
        super().__init__(**kwargs)

    def on_modified(self, event):
        super(ReportFileChangedHandlerWithPush, self).on_modified(event)
        print(f"Detected file change in {event.src_path}...")
        render_from_file(self.fn, self.output_dir)
        requests.post("http://127.0.0.1:8000/update")


@app.command()
def serve(report_fn: str):
    env = copy.copy(os.environ)
    with tempfile.TemporaryDirectory() as tmpdir:
        fn = os.path.realpath(report_fn)
        report_module = import_report_module(fn)
        find_and_render(report_module, tmpdir)
        observer = watchdog.observers.Observer()
        event_handler = ReportFileChangedHandlerWithPush(fn, tmpdir, patterns=[fn])
        observer.schedule(event_handler, os.path.dirname(fn))
        observer.start()
        env["SERVER_DIR"] = tmpdir
        proc = subprocess.Popen(["uvicorn", "vizno.server:app"], env=env)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            proc.terminate()
            observer.stop()
        observer.join()


def main():
    app()


if __name__ == "__main__":
    main()
