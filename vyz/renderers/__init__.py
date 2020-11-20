import functools
from typing import Any, List

import pydantic


class ContentConfiguration(pydantic.BaseModel):
    component: str
    component_module: str = "vyz-core.js"
    external_js_dependencies: List[str] = []


class FallbackContentConfiguration(ContentConfiguration):
    component: str = "FallbackContent"
    component_module: str = "vyz-core.js"
    detected_type: str


@functools.singledispatch
def render(content: Any) -> ContentConfiguration:
    return FallbackContentConfiguration(detected_type=type(content).__name__)
