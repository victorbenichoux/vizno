import matplotlib.pyplot as plt

from vyz.report import Report

r = Report(
    title="My super report", datetime="The datetime", description="a very basic report"
)


@r.widget(name="A matplotlib widget", description="with a *description*")
def _():
    f = plt.figure()
    ax = f.add_subplot(111)
    ax.plot([1, 2, 3], [2, 1, 3])
    ax.set_xlabel("Label")
    return f


r.render("examples/output/matplotlib_widget")
