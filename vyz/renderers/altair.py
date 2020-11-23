# -*- coding: utf-8 -*-

import uuid

import altair
import altair.vega
import altair.vegalite

from vyz.renderers import ContentConfiguration, magic_include, render


class AltairContentConfiguration(ContentConfiguration):
    component: str = "VegaContent"
    component_module: str = "vyz-core.js"
    spec: dict
    content_uuid: str


@magic_include
@render.register
def _(chart: altair.Chart) -> AltairContentConfiguration:
    return AltairContentConfiguration(
        spec=chart.to_dict(),
        external_js_dependencies=[
            "https://cdn.jsdelivr.net/npm/vega@" f"{altair.vega.SCHEMA_VERSION[1]}",
            "https://cdn.jsdelivr.net/npm/vega-lite@"
            f"{altair.vegalite.SCHEMA_VERSION[1]}",
            "https://cdn.jsdelivr.net/npm/vega-embed@6",
        ],
        content_uuid=f"vega-{uuid.uuid4().hex[:8]}",
    )
