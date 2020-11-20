# -*- coding: utf-8 -*-
import io
import xml.etree.ElementTree as et

import matplotlib

from vyz.renderers import ContentConfiguration, magic_include, render

matplotlib.use("Agg")

from matplotlib.pyplot import Figure, rcParams  # noqa: E402

rcParams["svg.fonttype"] = "none"


class MatplotlibContentConfiguration(ContentConfiguration):
    component: str = "SVGContent"
    component_module: str = "vyz-core.js"
    data: str


@magic_include
@render.register
def _(
    figure: Figure,
    scale: str = "down",
    inherit_font: bool = True,
    tight_layout: bool = True,
    bbox_inches: str = None,
) -> MatplotlibContentConfiguration:
    if tight_layout:
        figure.tight_layout()

    with io.StringIO() as str_io:
        figure.savefig(str_io, format="svg", transparent=True, bbox_inches=bbox_inches)
        svg = str_io.getvalue()

    # parse svg
    et.register_namespace("", "http://www.w3.org/2000/svg")
    et.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    root = et.fromstring(svg)
    # override width and height
    fig_size = figure.get_size_inches()
    if scale == "full":
        root.attrib["width"] = "100%"
        root.attrib["height"] = "100%"
    elif scale == "fixed":
        root.attrib["width"] = f"{fig_size[0]}in"
        root.attrib["height"] = f"{fig_size[1]}in"
    else:
        root.attrib["height"] = f"{fig_size[1]}in"
        root.attrib["width"] = "100%"

    if inherit_font:
        # inherit fonts
        for element in root.iter("{http://www.w3.org/2000/svg}text"):
            s = element.attrib.get("style")
            if s:
                rules = {
                    r[0]: r[1]
                    for r in map(lambda x: x.split(":") if x else None, s.split(";"))
                    if r
                }
                rules["font-family"] = "inherit"
                element.set(
                    "style", ";".join((": ".join(rule) for rule in rules.items()))
                )

    with io.StringIO() as str_io:
        et.ElementTree(root).write(str_io, encoding="unicode")
        return MatplotlibContentConfiguration(data=str_io.getvalue())
