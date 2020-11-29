# -*- coding: utf-8 -*-


import pygal

from vizno.renderers import magic_include, render
from vizno.renderers.svg import SVGContentConfiguration, clean_svg


@magic_include
@render.register
def _(
    chart: pygal.graph.graph.Graph,
    inherit_font: bool = True,
    scale: str = "down",
) -> SVGContentConfiguration:
    return SVGContentConfiguration(
        data=clean_svg(chart.render(disable_xml_declaration=True), scale=scale)
    )
