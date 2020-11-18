# -*- coding: utf-8 -*-
"""
This package contains the parent class for vyz reports.
"""

from typing import Callable, List


class Widget:
    def __init__(self, func, name, description):
        self.fun = func
        self.name = name
        self.description = description


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
