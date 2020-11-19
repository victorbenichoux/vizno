import tempfile

import matplotlib.pyplot as plt
import pytest

from vyz.renderers import FallbackContentConfiguration
from vyz.renderers.matplotlib import MatplotlibContentConfiguration
from vyz.renderers.text import TextContentConfiguration
from vyz.report import Report


class OddContent:
    pass


@pytest.fixture(scope="module", params=["str", "matplotlib", "odd"])
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


def test_renderers(content):
    r = Report()

    @r.widget()
    def something():
        return content[0]

    assert isinstance(r.get_configuration().widgets[0].content, content[1])
    with tempfile.TemporaryDirectory() as tmpdir:
        r.render(tmpdir)
