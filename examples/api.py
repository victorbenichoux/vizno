from vyz.api import VyzApp
from vyz.report import Report

app = VyzApp()


@app.report("/something")
def f(value: str):
    r = Report()
    r.widget(value, name="Result here")
    return r.get_configuration()
