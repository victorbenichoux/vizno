import pydantic
import pytest

from vizno.report import Report, ReportConfiguration


def test_basic_report():
    r = Report()

    r.widget(None)
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        r.header(None)
    r.header("Some header")
    r.header("Some header", description="Some description")
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        r.text(None)
    r.text("Some text")
    r.text("Some header", description="Some description")

    assert len(r.elements) == 5
    config = r.get_configuration()
    assert isinstance(config, ReportConfiguration)
    assert len(config.elements) == 5
