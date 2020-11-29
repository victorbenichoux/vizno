import random

import plotly
import plotly.graph_objects as go

from vizno.report import Report

xs = [random.random() for _ in range(100)]
ys = [x + random.random() * 0.1 for x in xs]
sizes = [x * 5 + 5 for x in xs]
colors = [random.random() * 0.1 for x in xs]

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=xs,
        y=ys,
        mode="markers",
        marker=go.scatter.Marker(
            size=sizes, color=colors, opacity=0.6, colorscale="Viridis"
        ),
    )
)

r = Report()
r.widget(fig, name="A plotly widget")
# # create a simple plot
# bar = plotly.graph_objs.Bar(x=['giraffes', 'orangutans', 'monkeys'],
#                             y=[20, 14, 23])
# layout = plotly.graph_objs.Layout()
# fig = plotly.graph_objs.Figure([bar], layout)

# # convert it to JSON
# fig_json = fig.to_json()

# # a simple HTML template
# template = """<html>
# <head>
#     <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
# </head>
# <body>
#     <div id='divPlotly'></div>
#     <script>
#         var plotly_data = {}
#         Plotly.react('divPlotly', plotly_data.data, plotly_data.layout);
#     </script>
# </body>

# </html>"""

# # write the JSON to the HTML template
# with open('new_plot.html', 'w') as f:
#     f.write(template.format(fig_json))
