import pygal  # First import pygal

from vizno.report import Report

bar_chart = pygal.Bar()  # Then create a bar graph object
bar_chart.add("Fibonacci", [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values

r = Report()
r.widget(bar_chart)
