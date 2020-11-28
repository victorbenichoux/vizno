# -*- coding: utf-8 -*-

import uuid

import bokeh.embed
import bokeh.models

from vizno.renderers import ContentConfiguration, magic_include, render


class BokehContentConfiguration(ContentConfiguration):
    component: str = "BokehContent"
    spec: dict
    content_uuid: str


@magic_include
@render.register
def _(
    model: bokeh.models.Model,
) -> BokehContentConfiguration:
    model.sizing_mode = "scale_both"
    item = bokeh.embed.json_item(model)
    version = item["doc"]["version"]
    return BokehContentConfiguration(
        spec=item,
        external_js_dependencies=[
            f"https://cdn.bokeh.org/bokeh/release/bokeh-{version}.min.js",
            f"https://cdn.bokeh.org/bokeh/release/bokeh-widgets-{version}.min.js",
            f"https://cdn.bokeh.org/bokeh/release/bokeh-tables-{version}.min.js",
        ],
        content_uuid=f"vega-{uuid.uuid4().hex[:8]}",
    )
