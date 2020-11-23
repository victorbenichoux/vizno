import random

import altair
import matplotlib.pyplot as plt
import pandas as pd
from bokeh.plotting import figure as bokeh_figure

from vyz.report import Report

xs = [random.random() for _ in range(100)]
ys = [x + random.random() * 0.1 for x in xs]

r = Report(
    title="The demo report",
    description="This demo report showcases the capabilities of vyz.",
)


r.header("Some Header", description="In each section we can find multiple widgets.")

f = plt.figure()
ax = f.add_subplot(111)
ax.plot(xs, ys, ".")
ax.set_xlabel("Label")

r.widget(
    f,
    name="This is a matplotlib widget",
    description="It contains the above figure, but also a description, which _may include_ [markdown](https://daringfireball.net/projects/markdown/) ***formatted*** text",
)

chart = (
    altair.Chart(
        pd.DataFrame(
            {
                "a": xs,
                "b": ys,
            }
        )
    )
    .mark_circle(size=20)
    .encode(x="a", y="b")
)

r.widget(chart, name="An altair widget")

plot = bokeh_figure(plot_width=400, plot_height=300)
plot.circle(xs, ys)

r.widget(plot, name="A bokeh widget")

r.widget(
    pd.DataFrame(
        {
            "a": xs,
            "b": ys,
        }
    ),
    name="A table",
)


r.render("examples/output/demo")
