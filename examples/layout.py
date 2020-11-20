from vyz.report import Report

r = Report(
    title="The demo report",
    description="This report showcases the grid system based on 12 vertical divisions",
)


r.widget("Size 1", width=1)
r.widget("Size 2", width=2)
r.widget("Size 3", width=3)
r.widget("Size 4", width=4)
r.widget("Size 5", width=5)
r.widget("Size 6", width=6)
r.widget("Size 7", width=7)
r.widget("Size 8", width=8)
r.widget("Size 9", width=9)
r.widget("Size 10", width=10)
r.widget("Size 11", width=11)
r.widget("Size 12", width=12)


r.widget("Size 1 (newline)", width=1, newline=True)
r.widget("Size 2 (newline)", width=2, newline=True)
r.widget("Size 3 (newline)", width=3, newline=True)
r.widget("Size 4 (newline)", width=4, newline=True)
r.widget("Size 5 (newline)", width=5, newline=True)
r.widget("Size 6 (newline)", width=6, newline=True)
r.widget("Size 7 (newline)", width=7, newline=True)
r.widget("Size 8 (newline)", width=8, newline=True)
r.widget("Size 9 (newline)", width=9, newline=True)
r.widget("Size 10 (newline)", width=10, newline=True)
r.widget("Size 11 (newline)", width=11, newline=True)
r.widget("Size 12 (newline)", width=12, newline=True)


r.render("examples/output/layout")
