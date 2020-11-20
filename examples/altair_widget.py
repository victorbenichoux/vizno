import altair
import pandas as pd

from vyz.report import Report

r = Report(
    title="My Altair", datetime="The datetime", description="a very basic report"
)


@r.widget(name="An altair widget")
def _():
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
    chart.save("chart.html")
    return chart


r.render("examples/output/altair")
