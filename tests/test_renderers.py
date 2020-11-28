import random
import tempfile

import altair
import matplotlib.pyplot as plt
import pandas as pd
import pytest
from bokeh.plotting import figure as bokeh_figure

from vizno.renderers import FallbackContentConfiguration
from vizno.renderers.altair import AltairContentConfiguration
from vizno.renderers.bokeh import BokehContentConfiguration
from vizno.renderers.code import CodeContent, CodeContentConfiguration
from vizno.renderers.latex import LatexContent, LatexContentConfiguration
from vizno.renderers.mathjax import MathJaxContent, MathJaxContentConfiguration
from vizno.renderers.matplotlib import MatplotlibContentConfiguration
from vizno.report import Report


class OddContent:
    pass


@pytest.fixture(
    scope="module",
    params=["matplotlib", "odd", "altair", "bokeh", "code", "latex", "mathjax"],
)
def content(request):
    if request.param == "matplotlib":
        f = plt.figure()
        yield (f, MatplotlibContentConfiguration)
        f.clf()
        del f
    if request.param == "odd":
        yield (OddContent(), FallbackContentConfiguration)
    if request.param == "altair":
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
        yield (chart, AltairContentConfiguration)
    if request.param == "bokeh":
        plot = bokeh_figure(plot_width=400, plot_height=300)
        plot.circle(
            [random.random() for _ in range(100)], [random.random() for _ in range(100)]
        )
        yield (plot, BokehContentConfiguration)
    if request.param == "code":
        yield (
            CodeContent(code="lambda x: x", language="python"),
            CodeContentConfiguration,
        )
    if request.param == "latex":
        yield (
            LatexContent(text="$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$"),
            LatexContentConfiguration,
        )
    if request.param == "mathjax":
        yield (
            MathJaxContent(text="$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$"),
            MathJaxContentConfiguration,
        )
    if request.param == "custom":
        yield (
            MathJaxContent(text="$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$"),
            MathJaxContentConfiguration,
        )


def test_renderers(content):
    r = Report()

    r.widget(content[0])

    assert isinstance(r.get_configuration().elements[0].content, content[1])
    with tempfile.TemporaryDirectory() as tmpdir:
        r.render(tmpdir)
