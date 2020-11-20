from vyz.report import Report

r = Report(
    title="My super report", datetime="The datetime", description="a very basic report"
)


r.widget(None, name="A first widget", description="with a *description*")


r.widget(
    "This one returns text",
    name="A second widget",
    description="with another *description*",
)


r.render("examples/output/basic")
