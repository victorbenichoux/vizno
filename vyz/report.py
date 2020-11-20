# -*- coding: utf-8 -*-
"""
This package contains the parent class for vyz reports.
"""

import json
import os
from typing import List

import pydantic

import vyz.renderers.altair  # noqa: F401
import vyz.renderers.bokeh  # noqa: F401
import vyz.renderers.matplotlib  # noqa: F401
import vyz.renderers.text  # noqa: F401
from vyz.renderers import ContentConfiguration, render
from vyz.utils import copy_index_template, copy_template


class WidgetConfiguration(pydantic.BaseModel):
    class LayoutParameters(pydantic.BaseModel):
        width: int = 3

    name: str
    description: str = ""
    content: ContentConfiguration
    layout: LayoutParameters


class Widget:
    def __init__(self, content, name, description, width: int = 3):
        self.content = content
        self.name = name
        self.description = description
        self.width = width

    def get_configuration(self):
        return WidgetConfiguration(
            name=self.name,
            description=self.description,
            content=render(self.content),
            layout={"width": self.width},
        )


class ReportConfiguration(pydantic.BaseModel):
    title: str
    description: str
    datetime: str
    widgets: List[WidgetConfiguration]


class Report:
    """
    Use this object to start creating a report
    """

    def __init__(
        self,
        title: str = "",
        description: str = "",
        datetime: str = "",
        widgets: List[Widget] = None,
    ):
        self.widgets = widgets or []
        self.title = title
        self.datetime = datetime
        self.description = description

    def widget(self, content, name: str = "", description: str = "", width: int = 3):
        self.widgets.append(Widget(content, name, description, width))

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
        external_js_dependencies = {
            dep
            for widget in configuration.widgets
            for dep in widget.content.external_js_dependencies
        }
        copy_index_template(
            "index.html",
            output_dir,
            external_js_dependencies=external_js_dependencies,
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
