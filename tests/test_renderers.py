import tempfile

import matplotlib.pyplot as plt
import pytest

from vyz.report import Report

from vyz.renderers.matplotlib import MatplotlibContentConfiguration
from vyz.renderers.text import TextContentConfiguration
from vyz.renderers import FallbackContentConfiguration


class OddContent:
    pass


@pytest.mark.parametrize(
    "content, config_type",
    [
        ("Bonjour", TextContentConfiguration),
        (plt.figure(), MatplotlibContentConfiguration),
        (OddContent(), FallbackContentConfiguration),
    ],
)
def test_renderers(content, config_type):
    r = Report()

    @r.widget()
    def something():
        return content

    assert isinstance(r.get_configuration().widgets[0].content, config_type)
    with tempfile.TemporaryDirectory() as tmpdir:
        r.render(tmpdir)
