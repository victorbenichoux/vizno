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
    def on_modified(self, event):
        super(ReportFileChangedHandler, self).on_modified(event)
        print(f"Detected file change in {event.src_path}...")
        run_report_file(event.src_path)


def run_report_file(fn):
    env = copy.copy(os.environ)
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] += ":" + dir_realpath
    else:
        env["PYTHONPATH"] = dir_realpath
    subprocess.call([sys.executable, fn], env=env)


def report(report_fn: str, reload: bool = False):
    fn = os.path.realpath(report_fn)
    if not reload:
        run_report_file(fn)
    else:
        event_handler = ReportFileChangedHandler(patterns=[fn])
        observer = watchdog.observers.Observer()
        observer.schedule(event_handler, os.path.dirname(fn))
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


if __name__ == "__main__":
    typer.run(report)
