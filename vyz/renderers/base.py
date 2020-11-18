# -*- coding: utf-8 -*-
from typing import Any, Generic, Type, TypeVar

import pydantic


class ContentConfiguration(pydantic.BaseModel):
    component: str
    component_module: str = "vyz-core.js"


ConfigType = TypeVar("ConfigType", bound=ContentConfiguration)
SupportedType = TypeVar("ConfigType", bound=Type)


class GenericContentRenderer(Generic[SupportedType, ConfigType]):
    """
    Base class for renderers
    """

    @staticmethod
    def render(content: SupportedType) -> ConfigType:
        pass


class FallbackContentConfiguration(ContentConfiguration):
    component: str = "FallbackContent"
    component_module: str = "vyz-core.js"
    detected_type: str


class FallbackContentRenderer(
    GenericContentRenderer[Any, FallbackContentConfiguration]
):
    def render(content):
        return FallbackContentConfiguration(detected_type=type(content).__name__)
