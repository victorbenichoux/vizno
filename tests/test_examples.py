import copy
import os
import subprocess
import sys
import tempfile

import pytest

from tests import ROOT_DIR

EXAMPLES_DIR = os.path.join(ROOT_DIR, "examples", "reports")
EXAMPLES = [
    os.path.join(EXAMPLES_DIR, fn)
    for fn in os.listdir(os.path.join(EXAMPLES_DIR))
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
        assert (
            subprocess.call(
                [
                    sys.executable,
                    "vizno/cli.py",
                    "render",
                    example_fn,
                    "--output-dir",
                    tmpdir,
                ],
                env=env,
            )
            == 0
        )
        assert set(os.listdir(tmpdir)) == {
            "index.html",
            "vizno.css",
            "vizno-core.min.js",
            "vz-ico.png",
            "vizno-config.js",
        }