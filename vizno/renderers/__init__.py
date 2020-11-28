import functools
from typing import Any, Callable, List, Optional

import pydantic


class ContentConfiguration(pydantic.BaseModel):
    component: str
    component_module: Optional[str]
    external_js_dependencies: List[str] = []
    external_css_dependencies: List[str] = []


class FallbackContentConfiguration(ContentConfiguration):
    component: str = "FallbackContent"
    detected_type: str


@functools.singledispatch
def render(content: Any) -> ContentConfiguration:
    return FallbackContentConfiguration(detected_type=type(content).__name__)


def magic_include(func: Callable) -> Callable:
    func._magic_include = True  # type: ignore[attr-defined]
    return func
