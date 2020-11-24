from vizno.api import viznoApp
from vizno.report import Report

app = viznoApp()


@app.report("/something")
def f(value: str):
    r = Report()
    r.widget(value, name="Result here")
    return r.get_configuration()
