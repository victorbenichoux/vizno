from typing import Optional

import pytest
from starlette.testclient import TestClient

from vizno.api import ViznoApp
from vizno.report import Report


@pytest.fixture
def vizno_app():
    app = ViznoApp()

    @app.report("/")
    def f(value: Optional[str] = None):
        r = Report()
        r.text("# Report served with the API")
        if value is None:
            r.text(
                """
    No value provided.


    Try to add a value in the search string.

    For example [like this](http://localhost:8000?value="with a value")
    """,
                name="Result here",
            )
        else:
            r.text(f"The value was {value}", name="Result here")
        return r.get_configuration()

    with TestClient(app) as client:
        yield client


PATHS = [
    ("/", 200),
    ("?value=10", 200),
    ("/?value=10", 200),
    ("", 200),
    ("/static/index.html", 200),
    ("/static/vizno.css", 200),
    ("/static/vizno-core.min.js", 200),
    ("/static/vz-ico.png", 200),
]


@pytest.mark.parametrize("path, status_code", PATHS)
def test_app(path, status_code, vizno_app):
    response = vizno_app.get(path)
    assert response.status_code == status_code
