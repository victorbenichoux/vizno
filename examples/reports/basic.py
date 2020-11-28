from vizno.report import Report

r = Report(
    title="My super report", datetime="The datetime", description="a very basic report"
)


r.widget(
    "This one returns text",
    name="A second widget",
    description="with another *description*",
)
