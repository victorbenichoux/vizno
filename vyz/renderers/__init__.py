import functools
from typing import Any

import pydantic


class ContentConfiguration(pydantic.BaseModel):
    component: str
    component_module: str = "vyz-core.js"


class FallbackContentConfiguration(ContentConfiguration):
    component: str = "FallbackContent"
    component_module: str = "vyz-core.js"
    detected_type: str


@functools.singledispatch
def render(content: Any) -> ContentConfiguration:
    return FallbackContentConfiguration(detected_type=type(content).__name__)
