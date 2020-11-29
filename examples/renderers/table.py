import pandas as pd

from vizno.report import Report

products = pd.DataFrame(
    {
        "Product": ["Tablet", "iPhone", "Laptop", "Monitor"] * 1000,
        "Price": [250, 800, 1200, 300] * 1000,
    }
)


r = Report(
    title="My super report", datetime="The datetime", description="a very basic report"
)

r.widget(products, width=12, name="A table", description="with a *description*")
