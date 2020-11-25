from vizno.api import ViznoApp
from vizno.report import Report
from typing import Optional

app = ViznoApp()


@app.report("/")
def f(value: Optional[str] = None):
    r = Report()
    r.text("# Report served with the API")
    if value is None:
        r.text(f"""
No value provided.


Try to add a value in the search string.

For example [like this](http://localhost:8000?value="with a value")
""", name="Result here")
    else:
        r.text(f"The value was {value}", name="Result here")
    return r.get_configuration()
