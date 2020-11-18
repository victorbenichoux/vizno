from vyz.report import Report

r = Report(title="My super report", datetime="The datetime", description="a very basic report")

@r.widget(name="A first widget", description="with a *description*")
def f():
    pass

@r.widget(name="A second widget", description="with another *description*")
def f():
    pass

r.render("examples/output/basic")