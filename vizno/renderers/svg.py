import io
import xml.etree.ElementTree as et

from vizno.renderers import ContentConfiguration


class SVGContentConfiguration(ContentConfiguration):
    component: str = "SVGContent"
    data: str


def clean_svg(svg, scale="down", width=None, height=None, inherit_font=True):
    # parse svg
    et.register_namespace("", "http://www.w3.org/2000/svg")
    et.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    root = et.fromstring(svg)
    # override width and height
    if scale == "full":
        root.attrib["width"] = "100%"
        root.attrib["height"] = "100%"
    elif scale == "fixed" and width and height:
        root.attrib["width"] = f"{width}in"
        root.attrib["height"] = f"{height}in"
    elif width:
        root.attrib["height"] = f"{height}in"
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
        return str_io.getvalue()
