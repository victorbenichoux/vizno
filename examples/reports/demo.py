import random

import altair
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import pygal
from bokeh.plotting import figure as bokeh_figure

from vizno.renderers.code import CodeContent
from vizno.renderers.latex import LatexContent
from vizno.renderers.mathjax import MathJaxContent
from vizno.report import Report

xs = [random.random() for _ in range(100)]
ys = [x + random.random() * 0.1 for x in xs]

r = Report(
    title="The demo report",
    description="This demo report showcases the capabilities of vizno.",
)


r.header(
    "Python plotting libraries",
    description="""
`vizno` supports all the common Python plotting libraries.
""",
)

f = plt.figure()
ax = f.add_subplot(111)
ax.plot(xs, ys, ".")
ax.set_xlabel("Label")

r.widget(
    f,
    name="Matplotlib",
    description="A [matplotlib](https://matplotlib.org/) figure",
    layout={"width": 6},
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

r.widget(
    chart,
    name="Atlair",
    description="An [altair](https://altair-viz.github.io/) figure",
    layout={"width": 6},
)

plot = bokeh_figure(plot_width=400, plot_height=300)
plot.circle(xs, ys)

r.widget(
    plot,
    name="Bokeh",
    description="A [bokeh](https://docs.bokeh.org/en/latest/index.html#) figure",
    layout={"width": 6},
)


pygal_figure = pygal.XY(stroke=False)
pygal_figure.add("x/y", list(zip(xs, ys)))

r.widget(
    pygal_figure,
    name="Pygal",
    description="A [pygal](http://www.pygal.org/en/stable/) figure",
    layout={"width": 6},
)


plotly_figure = go.Figure()
plotly_figure.add_trace(
    go.Scatter(
        x=xs,
        y=ys,
        mode="markers",
        marker=go.scatter.Marker(size=5),
    )
)


r.widget(
    plotly_figure,
    name="Plotly",
    description="A [plotly](https://github.com/plotly/plotly.py) figure",
    layout={"width": 6},
)


r.header(
    "Table data",
    description="""
`vizno` supports rendering tabular data from dataframes.
""",
)


r.widget(
    pd.DataFrame(
        {
            "a": xs,
            "b": ys,
        }
    ),
    name="A table",
)

r.header(
    "Typesetting",
    description="""
`vizno` supports rendering Markdown text.
""",
)

r.text(
    """
It is possible to just write some Markdown text.

### Sections

Use `#` for sections.

# H1
## H2
### H3
#### H4
##### H5
###### H6

### Links and images

You can include linked images:

![image](https://via.placeholder.com/300.png)

[via placeholder](https://placeholder.com/)

As well as links [**important** important link](#example)


### Code

    You can indent
    blocks to format
    code

Or wrap in backticks

```
print("Hello")
```

### Quotes

> You can insert block quotes by
> preceeding each line with `>`.
>
> Blockquotes can also contain line  
> breaks.


### Lists

- Unordered
* Lists
+ Of mixed type

1. Ordered
2. Lists
4. Numbers are ignored
    """  # NOQA
)

r.header(
    "Advanced typesetting",
    description="""
`vizno` supports advanced typesetting.
""",
)

r.widget(
    CodeContent(
        code="""def do_something(argument):
    print(f"Hello {argument}!")
do_something("ok")""",
        language="python",
    ),
    name="Code",
    layout={"width": 6},
)

r.widget(
    MathJaxContent(
        text="""
When \(a \\ne 0\), there are two solutions to \(ax^2 + bx + c = 0\) and they are
$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$
"""
    ),
    name="MathJax",
    layout={"width": 6},
)

r.widget(
    LatexContent(
        text="""
\documentclass{article}

\\begin{document}

When $a \\ne 0$, there are two solutions to $ax^2 + bx + c = 0$ and they are
$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$

\end{document}
"""
    ),
    name="LaTeX",
    layout={"width": 6},
)
