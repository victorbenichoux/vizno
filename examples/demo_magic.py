import random

import altair
import matplotlib.pyplot as plt
import pandas as pd
from bokeh.plotting import figure as bokeh_figure

from vizno.report import Report

xs = [random.random() for _ in range(100)]
ys = [x + random.random() * 0.1 for x in xs]

f = plt.figure()
ax = f.add_subplot(111)
ax.plot(xs, ys, ".")
ax.set_xlabel("Label")

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

plot = bokeh_figure(plot_width=400, plot_height=300)
plot.circle(xs, ys)


r = Report.magic(title="Magic report", description="A magically gathered report")
r.render("examples/output/magic")
