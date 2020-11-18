#!/usr/bin/env python3

import copy
import os
import subprocess
import sys
import time

import typer
import watchdog.events
import watchdog.observers

realpath = os.path.realpath(__file__)
dir_realpath = os.path.dirname(os.path.dirname(realpath))
sys.path.append(dir_realpath)


class ReportFileChangedHandler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self, target_report_fn, **kwargs):
        self.target_report_fn = target_report_fn
        super().__init__(**kwargs)

    def on_modified(self, event):
        super(ReportFileChangedHandler, self).on_modified(event)
        print(f"Detected file change in {event.src_path}...")
        run_report_file(self.target_report_fn)


def run_report_file(fn):
    env = copy.copy(os.environ)
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] += ":" + dir_realpath
    else:
        env["PYTHONPATH"] = dir_realpath
    subprocess.call([sys.executable, fn], env=env)


def report(report_fn: str, reload: bool = False, dev: bool = False):
    fn = os.path.realpath(report_fn)
    run_report_file(fn)
    if reload:
        observer = watchdog.observers.Observer()
        event_handler = ReportFileChangedHandler(fn, patterns=[fn])
        observer.schedule(event_handler, os.path.dirname(fn))
        if dev:
            vyz_src_path = os.path.join(dir_realpath, "vyz")
            dev_event_handler = ReportFileChangedHandler(fn, patterns=["*.js", "*.py"])
            observer.schedule(dev_event_handler, vyz_src_path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


if __name__ == "__main__":
    typer.run(report)
