import copy
import os
import subprocess
import sys

import pytest

from tests import ROOT_DIR

EXAMPLES = [
    os.path.join(ROOT_DIR, "examples", fn)
    for fn in os.listdir(os.path.join(ROOT_DIR, "examples"))
    if fn.endswith(".py")
]


@pytest.mark.parametrize("example_fn", EXAMPLES)
def test_examples(example_fn):
    env = copy.copy(os.environ)
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] += ":" + ROOT_DIR
    else:
        env["PYTHONPATH"] = ROOT_DIR
    assert subprocess.call([sys.executable, example_fn], env=env) == 0
