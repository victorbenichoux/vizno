import tempfile

import altair
import matplotlib.pyplot as plt
import pandas as pd
import pytest

from vyz.renderers import FallbackContentConfiguration
from vyz.renderers.altair import AltairContentConfiguration
from vyz.renderers.matplotlib import MatplotlibContentConfiguration
from vyz.renderers.text import TextContentConfiguration
from vyz.report import Report


class OddContent:
    pass


@pytest.fixture(scope="module", params=["str", "matplotlib", "odd", "altair"])
def content(request):

    if request.param == "str":
        yield ("Bonjour", TextContentConfiguration)
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


def test_renderers(content):
    r = Report()

    @r.widget()
    def something():
        return content[0]

    assert isinstance(r.get_configuration().widgets[0].content, content[1])
    with tempfile.TemporaryDirectory() as tmpdir:
        r.render(tmpdir)
