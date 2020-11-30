# -*- coding: utf-8 -*-

import uuid

import altair
import altair.vega
import altair.vegalite

from vizno.renderers import ContentConfiguration, magic_include, render


class AltairContentConfiguration(ContentConfiguration):
    component: str = "VegaContent"
    spec: dict
    content_uuid: str
    container_height: str = "40vh"


@magic_include
@render.register
def _(
    chart: altair.Chart, container_height: str = "40vh"
) -> AltairContentConfiguration:
    return AltairContentConfiguration(
        spec=chart.to_dict(),
        external_js_dependencies=[
            "https://cdn.jsdelivr.net/npm/vega@" f"{altair.vega.SCHEMA_VERSION[1]}",
            "https://cdn.jsdelivr.net/npm/vega-lite@"
            f"{altair.vegalite.SCHEMA_VERSION[1]}",
            "https://cdn.jsdelivr.net/npm/vega-embed@6",
        ],
        content_uuid=f"vega-{uuid.uuid4().hex[:8]}",
        container_height=container_height,
    )
