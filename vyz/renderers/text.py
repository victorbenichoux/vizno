# -*- coding: utf-8 -*-
from vyz.renderers.base import ContentConfiguration, GenericContentRenderer


class TextContentConfiguration(ContentConfiguration):
    component: str = "TextContent"
    component_module: str = "vyz-core.js"
    text: str


class TextRenderer(GenericContentRenderer[str, TextContentConfiguration]):
    @staticmethod
    def render(text):
        return TextContentConfiguration(text=text)
