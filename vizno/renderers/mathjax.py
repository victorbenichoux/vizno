# -*- coding: utf-8 -*-

import pydantic

from vizno.renderers import ContentConfiguration, render


class MathJaxContent(pydantic.BaseModel):
    text: str


class MathJaxContentConfiguration(ContentConfiguration):
    component: str = "MathJaxContent"
    text: str


@render.register
def _(obj: MathJaxContent) -> MathJaxContentConfiguration:
    return MathJaxContentConfiguration(
        text=obj.text.strip("\n"),
        external_js_dependencies=[
            "https://polyfill.io/v3/polyfill.min.js?features=es6",
            "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js",
        ],
    )
