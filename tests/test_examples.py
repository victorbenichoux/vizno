import copy
import os
import shutil
import subprocess
import sys
import tempfile

import pytest

from tests import ROOT_DIR

EXAMPLES_DIR = [
    os.path.join(ROOT_DIR, "examples", "renderers"),
    os.path.join(ROOT_DIR, "examples", "reports"),
]

EXAMPLES = [
    os.path.join(d, fn)
    for d in EXAMPLES_DIR
    for fn in os.listdir(d)
    if fn.endswith(".py")
]


@pytest.mark.parametrize("example_fn", EXAMPLES)
def test_examples(example_fn):
    env = copy.copy(os.environ)
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] += ":" + ROOT_DIR
    else:
        env["PYTHONPATH"] = ROOT_DIR
    with tempfile.TemporaryDirectory() as tmpdir:
        _, fn = os.path.split(example_fn)
        output_dir = os.path.join(ROOT_DIR, "docs", "examples")
        report_name = fn.replace(".py", ".html")
        assert (
            subprocess.call(
                [
                    sys.executable,
                    "vizno/cli.py",
                    "render",
                    example_fn,
                    "--output",
                    os.path.join(tmpdir, report_name),
                ],
                env=env,
            )
            == 0
        )
        if os.environ.get("UPDATE_EXAMPLES"):
            shutil.copy2(
                os.path.join(tmpdir, report_name), os.path.join(output_dir, report_name)
            )
        assert os.path.isfile(os.path.join(output_dir, report_name))


def test_examples_with_statics():
    env = copy.copy(os.environ)
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] += ":" + ROOT_DIR
    else:
        env["PYTHONPATH"] = ROOT_DIR
    with tempfile.TemporaryDirectory() as tmpdir:
        assert (
            subprocess.call(
                [
                    sys.executable,
                    "vizno/cli.py",
                    "render",
                    EXAMPLES[0],
                    "--output",
                    os.path.join(tmpdir, "index.html"),
                    "--with-statics",
                ],
                env=env,
            )
            == 0
        )
        assert set(os.listdir(tmpdir)) == {
            "index.html",
            "vizno-core.min.js",
            "vizno.css",
            "vz-ico.png",
        }
