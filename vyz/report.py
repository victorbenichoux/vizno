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


class Element:
    pass


class Widget(Element):
    def __init__(
        self,
        content,
        name: str = "",
        description: str = "",
        width: int = 12,
        newline: bool = False,
        **kwargs,
    ):
        self.content = content
        self.name = name
        self.description = description
        self.width = width
        self.newline = newline
        self.render_kwargs = kwargs

    def get_configuration(self):
        return WidgetConfiguration(
            name=self.name,
            description=self.description,
            content=render(self.content, **self.render_kwargs),
            layout={"width": self.width, "newline": self.newline},
        )


class Header(Element):
    def __init__(self, name: str = "", description: str = ""):
        self.name = name
        self.description = description

    def get_configuration(self):
        return HeaderConfiguration(
            name=self.name,
            description=self.description,
        )


class Text(Element):
    def __init__(self, text: str = ""):
        self.text = text

    def get_configuration(self):
        return TextConfiguration(text=self.text)


class ReportConfiguration(pydantic.BaseModel):
    title: str = ""
    description: str = ""
    datetime: str
    widgets: Sequence[ElementConfiguration]

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
        widgets: List[Element] = None,
    ):
        self.widgets = widgets or []
        self.title = title
        self.datetime = datetime
        self.description = description

    def widget(self, content, **kwargs):
        self.widgets.append(Widget(content, **kwargs))

    def header(self, name, description: str = ""):
        self.widgets.append(Header(name=name, description=description))

    def text(self, text):
        self.widgets.append(Text(text=text))

    def get_configuration(self):
        return ReportConfiguration(
            title=self.title,
            description=self.description,
            datetime=self.datetime,
            widgets=[w.get_configuration() for w in self.widgets],
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
                for widget in configuration.widgets
                if isinstance(widget, WidgetConfiguration)
                for dep in widget.content.external_js_dependencies
            },
            external_css_dependencies={
                dep: None
                for widget in configuration.widgets
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
