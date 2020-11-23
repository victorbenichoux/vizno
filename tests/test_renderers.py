import random
import tempfile

import altair
import matplotlib.pyplot as plt
import pandas as pd
import pytest
from bokeh.plotting import figure as bokeh_figure

from vyz.renderers import FallbackContentConfiguration
from vyz.renderers.altair import AltairContentConfiguration
from vyz.renderers.bokeh import BokehContentConfiguration
from vyz.renderers.matplotlib import MatplotlibContentConfiguration
from vyz.report import Report


class OddContent:
    pass


@pytest.fixture(scope="module", params=["matplotlib", "odd", "altair", "bokeh"])
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


def test_renderers(content):
    r = Report()

    r.widget(content[0])

    assert isinstance(r.get_configuration().widgets[0].content, content[1])
    with tempfile.TemporaryDirectory() as tmpdir:
        r.render(tmpdir)
