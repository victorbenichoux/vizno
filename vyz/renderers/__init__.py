from typing import Any

from vyz.renderers.base import ContentConfiguration, FallbackContentRenderer

RENDERERS = []


def render(content: Any) -> ContentConfiguration:
    for renderer in RENDERERS:
        if isinstance(content, FallbackContentRenderer.__orig_bases__[0].__args__[0]):
            return renderer.render(content)
    return FallbackContentRenderer.render(content)
