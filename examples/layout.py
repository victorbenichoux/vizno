import random

import altair
import matplotlib.pyplot as plt
import pandas as pd
from bokeh.plotting import figure as bokeh_figure

from vyz.report import Report

r = Report(title="The demo report", description="This report showcases the grid system based on 12 vertical divisions")


r.widget("Content",
    width=1,
    name="1",
)

r.widget("Content",
    width=2,
    name="2",
)

r.widget("Content",
    width=3,
    name="3",
)

r.widget("Content",
    width=4,
    name="4",
)

r.widget("Content",
    width=5,
    name="5",
)


r.widget("Content",
    width=6,
    name="6",
)

r.widget("Content",
    width=7,
    name="7",
)

r.widget("Content",
    width=8,
    name="8",
)

r.widget("Content",
    width=9,
    name="9",
)

r.widget("Content",
    width=10,
    name="10",
)
r.widget("Content",
    width=11,
    name="11",
)
r.widget("Content",
    width=12,
    name="12",
)


r.render("examples/output/layout")
