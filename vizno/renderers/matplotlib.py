# -*- coding: utf-8 -*-
import io

import matplotlib

from vizno.renderers import magic_include, render
from vizno.renderers.svg import SVGContentConfiguration, clean_svg

matplotlib.use("Agg")

from matplotlib.pyplot import Figure, rcParams  # noqa: E402

rcParams["svg.fonttype"] = "none"


@magic_include
@render.register
def _(
    figure: Figure,
    scale: str = "down",
    inherit_font: bool = True,
    tight_layout: bool = True,
    bbox_inches: str = None,
) -> SVGContentConfiguration:
    if tight_layout:
        figure.tight_layout()

    fig_size = figure.get_size_inches()
    with io.StringIO() as str_io:
        figure.savefig(str_io, format="svg", transparent=True, bbox_inches=bbox_inches)
        svg = str_io.getvalue()
    return SVGContentConfiguration(
        data=clean_svg(
            svg,
            scale=scale,
            width=fig_size[0],
            height=fig_size[1],
            inherit_font=inherit_font,
        )
    )
