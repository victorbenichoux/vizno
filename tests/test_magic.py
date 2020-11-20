from vyz.magic import renderable_objects
from vyz.renderers import magic_include, render


class NonRenderableObject:
    pass


@render.register
def _(arg: NonRenderableObject):
    pass


class RenderableObject:
    pass


@magic_include
@render.register
def __(arg: RenderableObject):
    pass


def test_renderable():
    assert len(list(renderable_objects([NonRenderableObject()]))) == 0
    assert len(list(renderable_objects([RenderableObject()]))) == 1
