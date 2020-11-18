#!/usr/bin/env python3

import typer
import os
import subprocess
import sys
import copy

realpath = os.path.realpath(__file__)
dir_realpath = os.path.dirname(os.path.dirname(realpath))
sys.path.append(dir_realpath)


def report(report_fn: str):
    env = copy.copy(os.environ)
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] += ":" + dir_realpath
    else:
        env["PYTHONPATH"] = dir_realpath

    subprocess.call([sys.executable, os.path.realpath(report_fn)], env=env)


if __name__ == "__main__":
    typer.run(report)
