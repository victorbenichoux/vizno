from vizno.report import Report


def test_basic_report():
    r = Report()

    r.widget(None)

    assert len(r.elements) == 1
