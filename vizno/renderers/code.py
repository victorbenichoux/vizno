# -*- coding: utf-8 -*-

from typing import Optional

import pydantic

from vizno.renderers import ContentConfiguration, render


class CodeContent(pydantic.BaseModel):
    code: str
    language: Optional[str]
    highlightjs_style: str = "default"


class CodeContentConfiguration(ContentConfiguration):
    component: str = "CodeContent"
    code: str
    language: Optional[str]


@render.register
def _(obj: CodeContent) -> CodeContentConfiguration:
    return CodeContentConfiguration(
        code=obj.code.strip("\n"),
        language=obj.language,
        external_js_dependencies=[
            "https://unpkg.com/@highlightjs/cdn-assets@10.4.0/highlight.min.js"
        ],
        external_css_dependencies=[
            "https://unpkg.com/@highlightjs/cdn-assets@"
            f"10.4.0/styles/{obj.highlightjs_style}.min.css"
        ],
    )
