import os
import tempfile

import pytest
from starlette.testclient import TestClient

from tests import ROOT_DIR
from vizno.cli import render


def test_render():
    fn = os.path.join(ROOT_DIR, "tests", "testdata", "report.py")
    with tempfile.TemporaryDirectory() as tmp_dir:
        render(fn, tmp_dir)


@pytest.fixture(scope="session")
def server_fixture():
    with tempfile.TemporaryDirectory() as tmp_dir:
        fn = os.path.join(ROOT_DIR, "tests", "testdata", "report.py")
        render(fn, tmp_dir)
        os.environ["SERVER_DIR"] = tmp_dir
        from vizno.server import app

        with TestClient(app) as client:
            yield client
        del os.environ["SERVER_DIR"]


PATHS = [
    ("/", 200),
    ("/static/index.html", 200),
    ("/static/vizno.css", 404),
    ("/static/vizno-core.min.js", 404),
    ("/static/vz-ico.png", 404),
]


@pytest.mark.parametrize("path, status_code", PATHS)
def test_cli_app(path, status_code, server_fixture):
    response = server_fixture.get(path)
    assert response.status_code == status_code


def test_cli_post_update(server_fixture):
    response = server_fixture.post("/update")
    assert response.status_code == 200


def test_ws(server_fixture):
    with server_fixture.websocket_connect("/ws") as websocket:
        server_fixture.post("/update")
        data = websocket.receive_text()
        assert data == "update"
