from typing import Any

from vyz.renderers.base import ContentConfiguration, FallbackContentRenderer
from vyz.renderers.matplotlib import MatplotlibRenderer
from vyz.renderers.text import TextRenderer

RENDERERS = [MatplotlibRenderer, TextRenderer]


def render(content: Any, **kwargs) -> ContentConfiguration:
    for renderer in RENDERERS:
        if isinstance(content, renderer.__orig_bases__[0].__args__[0]):
            return renderer.render(content, **kwargs)
    return FallbackContentRenderer.render(content)
