# -*- coding: utf-8 -*-

import uuid

import plotly.basedatatypes

from vizno.renderers import ContentConfiguration, magic_include, render


class PlotlyContentConfiguration(ContentConfiguration):
    component: str = "PlotlyComponent"
    spec: dict
    content_uuid: str


@magic_include
@render.register
def _(chart: plotly.basedatatypes.BaseFigure) -> PlotlyContentConfiguration:
    return PlotlyContentConfiguration(
        spec=chart.to_dict(),
        external_js_dependencies=["https://cdn.plot.ly/plotly-latest.min.js"],
        content_uuid=f"plotly-{uuid.uuid4().hex[:8]}",
    )
