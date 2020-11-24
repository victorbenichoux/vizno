import matplotlib.pyplot as plt

from vizno.report import Report

f = plt.figure()
ax = f.add_subplot(111)
ax.plot([1, 2, 3], [2, 1, 3])
ax.set_xlabel("Label")

r = Report(
    title="My super report", datetime="The datetime", description="a very basic report"
)

r.widget(f, width=12, name="A matplotlib widget", description="with a *description*")

r.render("examples/output/matplotlib_widget")
