import random

from bokeh.plotting import figure as bokeh_figure

from vizno.report import Report

r = Report(title="My bokeh", datetime="The datetime", description="a very basic report")

plot = bokeh_figure(plot_width=400, plot_height=300)
plot.circle(
    [random.random() for _ in range(100)], [random.random() for _ in range(100)]
)

r.widget(plot, name="A bokeh widget")
