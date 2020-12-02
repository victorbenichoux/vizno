# -*- coding: utf-8 -*-
"""
This package contains the parent class for vizno reports.
"""

import importlib
import json
import os
import shutil
import time
import uuid
from typing import List, Optional, Sequence

import pydantic

from vizno import __version__
from vizno.magic import iterate_frame_objects, renderable_objects
from vizno.renderers import ContentConfiguration, render
from vizno.utils import copy_resource

for renderer in [
    "vizno.renderers.altair",
    "vizno.renderers.bokeh",
    "vizno.renderers.matplotlib",
    "vizno.renderers.table",
    "vizno.renderers.code",
    "vizno.renderers.latex",
    "vizno.renderers.mathjax",
    "vizno.renderers.plotly",
    "vizno.renderers.pygal",
]:
    try:
        importlib.import_module(renderer)
    except ImportError:
        pass


class LayoutParameters(pydantic.BaseModel):
    width: int = 12
    newline: bool = False


class ElementConfiguration(pydantic.BaseModel):
    name: str = ""
    description: str = ""
    layout: Optional[LayoutParameters]
    element_type: str

    @pydantic.validator("layout", always=True, pre=True)
    def default_layout(v):
        return v or LayoutParameters()


class WidgetConfiguration(ElementConfiguration):
    element_type: str = "widget"
    content: ContentConfiguration


class HeaderConfiguration(ElementConfiguration):
    id: Optional[str]
    element_type: str = "header"

    @pydantic.validator("id", always=True, pre=True)
    def generate_header_id(v):
        return v or f"header-{uuid.uuid4().hex[:8]}"


class TextConfiguration(ElementConfiguration):
    element_type: str = "text"
    text: str


class ReportConfiguration(pydantic.BaseModel):
    title: str = ""
    description: str = ""
    datetime: str
    elements: Sequence[ElementConfiguration]

    @pydantic.validator("datetime")
    def validate_datetime(v):
        return v or time.ctime()


class Report:
    """
    Use this object to start creating a report
    """

    def __init__(
        self,
        title: str = "",
        description: str = "",
        datetime: str = "",
        elements: List[ElementConfiguration] = None,
    ):
        self.elements = elements or []
        self.title = title
        self.datetime = datetime
        self.description = description

    def widget(self, content, **kwargs):
        self.elements.append(WidgetConfiguration(content=render(content), **kwargs))

    def header(self, name, **kwargs):
        self.elements.append(HeaderConfiguration(name=name, **kwargs))

    def text(self, text, **kwargs):
        self.elements.append(TextConfiguration(text=text, **kwargs))

    def get_configuration(self):
        elements = [element for element in self.elements]
        return ReportConfiguration(
            title=self.title,
            description=self.description,
            datetime=self.datetime,
            elements=elements,
            js_dependencies=[
                dep
                for dep in {
                    dep: None
                    for widget in elements
                    if isinstance(widget, WidgetConfiguration)
                    for dep in widget.content.external_js_dependencies
                }
            ],
            css_dependencies=[
                dep
                for dep in {
                    dep: None
                    for widget in elements
                    if isinstance(widget, WidgetConfiguration)
                    for dep in widget.content.external_css_dependencies
                }
            ],
        )

    def render(self, output_dir: str, with_statics: bool = False):
        configuration = self.get_configuration()

        output_dir = os.path.realpath(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        if not with_statics:
            copy_resource(
                "index.html",
                output_dir,
                replace={
                    **{
                        "configuration = undefined": f"configuration = JSON.parse("
                        f"{json.dumps(configuration.json())}"
                        ")"
                    },
                    **{
                        static_asset: "https://cdn.jsdelivr.net/gh/victorbenichoux/"
                        f"vizno@{__version__}/vizno/statics/{static_asset}"
                        for static_asset in [
                            "vizno-core.min.js",
                            "vz-ico.png",
                            "vizno.css",
                        ]
                    },
                },
            )
        else:
            copy_resource(
                "index.html",
                output_dir,
                replace={
                    "configuration = undefined": "configuration=JSON.parse("
                    f"{json.dumps(configuration.json())}"
                    ")"
                },
            )
            copy_resource("vizno.css", output_dir)
            copy_resource("vizno-core.min.js", output_dir)
            copy_resource("vz-ico.png", output_dir)

        for element in configuration.elements:
            if isinstance(element, WidgetConfiguration):
                if element.content.component_module:
                    module_path = os.path.realpath(element.content.component_module)
                    shutil.copy(module_path, output_dir)

        print(f"Success:\n\tfile://{os.path.join(output_dir, 'index.html')}")

    @staticmethod
    def magic(title: str = "", description: str = "", datetime: str = ""):
        r = Report(title=title, description=description, datetime=datetime)

        for l in renderable_objects(iterate_frame_objects(-1)):
            dispatched_fun = render.dispatch(type(l))
            if hasattr(dispatched_fun, "_magic_include"):
                r.widget(l)

        return r
