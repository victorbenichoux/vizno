import copy
import importlib
import os
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager

import requests
import typer

from vizno.report import Report  # noqa: E402


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
        sys.modules[fn] = module
        spec.loader.exec_module(module)
        return module


def find_and_render(module, output_dir, with_statics: bool = False):
    report_name = next(
        v
        for v in dir(module)
        if not v.startswith("__") and isinstance(getattr(module, v), Report)
    )
    report = getattr(module, report_name)
    report.render(output_dir, with_statics)


def render_from_file(fn, output_dir, with_statics: bool = False):
    report_module = import_report_module(fn)
    find_and_render(report_module, output_dir, with_statics)


app = typer.Typer()


@app.command()
def render(
    report_fn: str,
    output_dir: str = ".",
    reload: bool = False,
    with_statics: bool = False,
):
    fn = os.path.realpath(report_fn)
    render_from_file(fn, output_dir, with_statics=with_statics)
    if reload:
        current_mtime = os.stat(fn).st_mtime
        try:
            while True:
                time.sleep(0.1)
                if os.stat(fn).st_mtime != current_mtime:
                    current_mtime = os.stat(fn).st_mtime
                    render_from_file(fn, output_dir, with_statics=with_statics)
        except KeyboardInterrupt:
            pass


@app.command()
def serve(report_fn: str):
    env = copy.copy(os.environ)
    with tempfile.TemporaryDirectory() as tmpdir:
        fn = os.path.realpath(report_fn)
        render_from_file(fn, tmpdir)
        current_mtime = os.stat(fn).st_mtime
        env["SERVER_DIR"] = tmpdir
        proc = subprocess.Popen(["uvicorn", "vizno.server:app"], env=env)
        try:
            while True:
                time.sleep(0.1)
                if os.stat(fn).st_mtime != current_mtime:
                    current_mtime = os.stat(fn).st_mtime
                    render_from_file(fn, tmpdir)
                    requests.post("http://127.0.0.1:8000/update")
        except KeyboardInterrupt:
            pass
        proc.terminate()


def main():
    app()


if __name__ == "__main__":
    main()
