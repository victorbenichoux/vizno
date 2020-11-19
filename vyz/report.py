# -*- coding: utf-8 -*-
"""
This package contains the parent class for vyz reports.
"""

import json
import os
import shutil
from typing import Callable, List

import pkg_resources
import pydantic

from vyz.renderers import render
from vyz.renderers.base import ContentConfiguration


class WidgetConfiguration(pydantic.BaseModel):
    name: str
    description: str
    content: ContentConfiguration


class Widget:
    def __init__(self, func, name, description):
        self.func = func
        self.name = name
        self.description = description

    def render_content(self):
        return render(self.func())

    def get_configuration(self):
        return WidgetConfiguration(
            name=self.name, description=self.description, content=self.render_content()
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

    def widget(self, name: str = "", description: str = "") -> Callable:
        def decorator(func: Callable) -> Callable:
            self.add_widget(func, name, description)
            return func

        return decorator

    def add_widget(self, func, name, description):
        self.widgets.append(Widget(func, name, description))

    def get_configuration(self):
        return ReportConfiguration(
            title=self.title,
            description=self.description,
            datetime=self.datetime,
            widgets=[w.get_configuration() for w in self.widgets],
        )

    def _write_config(self, output_fn):
        with open(output_fn, "w", encoding="utf-8") as f:
            f.write(
                "configuration=JSON.parse("
                f"{json.dumps(self.get_configuration().json())}"
                ")"
            )

    def render(self, output_dir: str):
        print("Starting report generation")
        output_dir = os.path.realpath(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        shutil.copyfile(
            pkg_resources.resource_filename("vyz", "js/index.html"),
            os.path.join(output_dir, "index.html"),
        )
        shutil.copyfile(
            pkg_resources.resource_filename("vyz", "js/vyz.css"),
            os.path.join(output_dir, "vyz.css"),
        )
        shutil.copyfile(
            pkg_resources.resource_filename("vyz", "js/vyz-core.js"),
            os.path.join(output_dir, "vyz-core.js"),
        )
        self._write_config(os.path.join(output_dir, "vyz-config.js"))
        print(f"Success:\n\tfile://{os.path.join(output_dir, 'index.html')}")
