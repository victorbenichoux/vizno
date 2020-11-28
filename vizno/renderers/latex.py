# -*- coding: utf-8 -*-

from typing import Optional

import pydantic

from vizno.renderers import ContentConfiguration, magic_include, render


class LatexContent(pydantic.BaseModel):
    text: str


class LatexContentConfiguration(ContentConfiguration):
    component: str = "LatexContent"
    text: str


@render.register
def _(obj: LatexContent) -> LatexContentConfiguration:
    return LatexContentConfiguration(
        text=obj.text.strip("\n"),
        external_js_dependencies=[
            "https://cdn.jsdelivr.net/npm/latex.js/dist/latex.js"
        ],
    )
