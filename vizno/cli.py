import copy
import importlib
import os
import queue
import subprocess
import sys
import tempfile
from contextlib import contextmanager

import requests
import typer
import watchdog.events
import watchdog.observers

from vizno.report import Report  # noqa: E402


class ReportFileChangedHandler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self, queue, **kwargs):
        super().__init__(**kwargs)
        self.queue = queue

    def on_modified(self, event):
        self.queue.put(True)


class ObserverState:
    observer: watchdog.observers.Observer
    queue: queue.Queue
    fn: str

    def __init__(self, fn):
        self.fn = fn
        self.queue = queue.Queue()
        self.observer = None

    def start(self):
        self.observer = watchdog.observers.Observer()
        self.queue = queue.Queue()
        event_handler = ReportFileChangedHandler(queue=self.queue, patterns=[self.fn])
        self.observer.schedule(event_handler, os.path.dirname(self.fn))
        self.observer.start()

    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None


@contextmanager
def safe_observer_bypass(obs):
    obs.stop()
    try:
        yield
    finally:
        obs.start()


@contextmanager
def add_to_path(p):
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
def render(report_fn: str, output_dir: str = ".", reload: bool = False):
    fn = os.path.realpath(report_fn)
    render_from_file(fn, report_fn)
    if reload:
        obs = ObserverState(fn)
        obs.start()
        try:
            while True:
                try:
                    obs.queue.get(timeout=1)
                    with safe_observer_bypass(obs):
                        render_from_file(fn, report_fn)
                except queue.Empty:
                    pass
        except KeyboardInterrupt:
            pass
        obs.stop()


@app.command()
def serve(report_fn: str):
    env = copy.copy(os.environ)
    with tempfile.TemporaryDirectory() as tmpdir:
        fn = os.path.realpath(report_fn)
        render_from_file(fn, tmpdir)
        obs = ObserverState(fn)
        env["SERVER_DIR"] = tmpdir
        proc = subprocess.Popen(["uvicorn", "vizno.server:app"], env=env)
        obs.start()
        try:
            while True:
                try:
                    obs.queue.get(timeout=0.1)
                    with safe_observer_bypass(obs):
                        render_from_file(fn, tmpdir)
                        requests.post("http://127.0.0.1:8000/update")
                except queue.Empty:
                    pass
        except KeyboardInterrupt:
            pass
        proc.terminate()
        obs.stop()


def main():
    app()


if __name__ == "__main__":
    main()
