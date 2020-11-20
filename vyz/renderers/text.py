# -*- coding: utf-8 -*-
from vyz.renderers import ContentConfiguration, render


class TextContentConfiguration(ContentConfiguration):
    component: str = "TextContent"
    component_module: str = "vyz-core.js"
    text: str


@render.register
def _(text: str):
    return TextContentConfiguration(text=text)
