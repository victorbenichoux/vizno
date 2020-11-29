import altair
import pandas as pd

from vizno.report import Report

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

r = Report(
    title="My Altair", datetime="The datetime", description="a very basic report"
)

r.widget(chart, name="An altair widget")
