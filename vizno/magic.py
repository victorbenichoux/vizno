import inspect
from typing import Sequence

from vizno.renderers import render


def renderable_objects(objects: Sequence[object]):
    for o in objects:
        if getattr(render.dispatch(type(o)), "_magic_include", False):
            yield o


def iterate_frame_objects(level=0):
    stack = inspect.stack()
    frame, filename, line_num, func, source_code, source_index = stack[level]
    for _, v in {**frame.f_globals, **frame.f_locals}.items():
        yield v
