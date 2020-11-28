import os
import tempfile

from tests import ROOT_DIR
from vizno.cli import render


def test_render():
    fn = os.path.join(ROOT_DIR, "tests", "testdata", "report.py")
    with tempfile.TemporaryDirectory() as tmp_dir:
        render(fn, tmp_dir)
