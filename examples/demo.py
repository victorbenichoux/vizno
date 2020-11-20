import random

import altair
import matplotlib.pyplot as plt
import pandas as pd
from bokeh.plotting import figure as bokeh_figure

from vyz.report import Report

r = Report(title="The demo report", description="A demo report")


r.widget(None, name="A first widget", description="with a *description*")

f = plt.figure()
ax = f.add_subplot(111)
ax.plot([1, 2, 3], [2, 1, 3])
ax.set_xlabel("Label")

r.widget(f, name="A matplotlib widget", description="with a *description*")

chart = (
    altair.Chart(
        pd.DataFrame(
            {
                "a": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
                "b": [28, 55, 43, 91, 81, 53, 19, 87, 52],
            }
        )
    )
    .mark_bar()
    .encode(x="a", y="b")
)

r.widget(chart, name="An altair widget")


plot = bokeh_figure(plot_width=400, plot_height=300)
plot.circle(
    [random.random() for _ in range(100)], [random.random() for _ in range(100)]
)

r.widget(plot, name="A bokeh widget")

r.widget(
    "This one returns text",
    name="A widget",
    description="with another *description*",
)


r.render("examples/output/demo")
