from vyz.report import Report

def test_basic_report():
    r = Report()

    @r.widget()
    def something():
        return None

    assert len(r.widgets) == 1