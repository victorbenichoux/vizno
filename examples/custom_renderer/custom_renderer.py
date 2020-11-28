import pydantic

from vizno.renderers import ContentConfiguration, render
from vizno.report import Report


class CustomObject(pydantic.BaseModel):
    parameter: int


class CustomRenderConfiguration(ContentConfiguration):
    parameter: int


@render.register
def _(obj: CustomObject):
    return CustomRenderConfiguration(
        component="MyCustomComponent",
        component_module="./my_renderer.js",
        parameter=obj.parameter,
    )


r = Report()
r.widget(CustomObject(parameter=10))
r.render("./output")
r.widget(
    CustomObject(parameter=1000),
    name="It works with a name",
    description="and a description",
)
r.render("./output")
