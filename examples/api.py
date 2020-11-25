from vizno.api import ViznoApp
from vizno.report import Report
from typing import Optional

app = ViznoApp()


@app.report("/")
def f(value: Optional[str] = None):
    r = Report()
    if value is None:
        r.text(f"No value provided, try to add a value for example like [this](http://localhost:8000?value=\"with a value\")", name="Result here")
    else:
        r.text(f"The value was {value}", name="Result here")
    return r.get_configuration()
