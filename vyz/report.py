# -*- coding: utf-8 -*-
"""
This package contains the parent class for vyz reports.
"""

import importlib
import json
import os
import time
import uuid
from typing import List, Optional, Sequence

import pydantic

from vyz.renderers import ContentConfiguration, render
from vyz.utils import copy_index_template, copy_template

for renderer in [
    "vyz.renderers.altair",
    "vyz.renderers.bokeh",
    "vyz.renderers.matplotlib",
    "vyz.renderers.table",
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
        return ReportConfiguration(
            title=self.title,
            description=self.description,
            datetime=self.datetime,
            elements=[element for element in self.elements],
        )

    def render(self, output_dir: str):
        configuration = self.get_configuration()

        output_dir = os.path.realpath(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        copy_index_template(
            "index.html",
            output_dir,
            # There are defined as dicts such that insertion key
            # order is maintained, but values are discarded
            # This is particularly useful when the order of import
            # in dependencies is important (e.g. for tabulator)
            external_js_dependencies={
                dep: None
                for widget in configuration.elements
                if isinstance(widget, WidgetConfiguration)
                for dep in widget.content.external_js_dependencies
            },
            external_css_dependencies={
                dep: None
                for widget in configuration.elements
                if isinstance(widget, WidgetConfiguration)
                for dep in widget.content.external_css_dependencies
            },
        )
        copy_template("vyz.css", output_dir)
        copy_template("vyz-core.js", output_dir)

        with open(
            os.path.join(output_dir, "vyz-config.js"), "w", encoding="utf-8"
        ) as f:
            f.write(
                "configuration=JSON.parse(" f"{json.dumps(configuration.json())}" ")"
            )
        print(f"Success:\n\tfile://{os.path.join(output_dir, 'index.html')}")
