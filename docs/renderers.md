## Elements

Given a `Report` object, add elements to it by calling the `Report.widget`, `Report.header` or `Report.text`

### Widgets

Widgets are the most importan elements because they can contain visualizations:

```python
r = Report()
r.widget(
    content,
    name="Title",
    description="Description",
    layout={"width": 6, newline: True}
    )
```

- `content` is a figure object, see below for supported options
- `name` appears as a header to the widget element
- `description` is markdown rendered below the widget content
- The layout grid is 12 units wide, 6 is half of the full widths.
- `newline` ensures that the widget is rendered on a new line

### Markdown

All titles and descriptions support Markdown text using [snarkdown](https://github.com/developit/snarkdown).

It is also possible to render a text element instead of a widget:

```python
r = Report()
r.text("Some **Markdown** text")
```

### Header

Finally, one can add `header` sections to the `Report` object:

```python
r = Report()
r.text(
    title="A header",
    description="Markdown that goes directly below the header"
    )
```

## Widget contents

`vizno` lays out and renders your Python visualizations in lightweight web pages. They can either be shared as standalone files, or rendered with fastAPI.

It supports rendering from the major Python visualization libraries:

### Matplotlib

It is possible to render [matplotlib](https://matplotlib.org/) figures within a vizno widget.

The figure has to be a `matplotlib.pyploy.Figure` subclass, and will be exported to SVG and included in the final report.

The `figure` object is exported as an SVG using the `Agg` interface, and is then cleaned before being passed to the backend. This cleaning process is tweakable through keyword arguments passed to the `Report.widget` call (see the SVG section).

Checkout the `examples/renderers/matplotlib.py` for an example, and the [resulting report](./examples/matplotlib.html).

### Altair

[altair](https://altair-viz.github.io/) charts can be rendered by passing them as the first argument of the `Report.widget()` function. They have to be instances of `altair.Chart`.

They are rendered by using the `Chart.to_dict()` function, and in the frontend by the `vega` JS library.

Checkout the `examples/renderers/altair.py` for an example, and the [resulting report](./examples/altair.html).

### Bokeh

[bokeh](https://docs.bokeh.org/en/latest/index.html) models can be rendererd by passing them as the first argument of the `Report.widget()` function. They have to be instances of `bokeh.models.Model` .

They are rendered by using `bokeh.embed.json_item` and then by `BokehJS` in the frontend.

Checkout the `examples/renderers/bokeh.py` for an example, and the [resulting report](./examples/bokeh.html).

### Plotly

[plotly](https://github.com/plotly/plotly.py) components can be rendered by passing them as the first argument of the `Report.widget()` function. They have to be instances of `plotly.basedatatypes.BaseFigure`.

They are rendered by first saving them using `BaseFigure.to_dict()` method, and by `plotly.js` in the frontend.

Checkout the `examples/renderers/plotly.py` for an example, and the [resulting report](./examples/plotly.html).

### Pygal

[pygal](http://www.pygal.org/en/stable/) charts can be rendered by passing them as the first argument of the `Report.widget()` function. They have to be instances of `pygal.graph.graph.Graph`.

They are rendered as SVG using `pygal`'s `Graph.render(disable_xml_declaration=True)` function and pass through the same cleaning process as the other SVG contents (see below).

Checkout the `examples/renderers/pygal.py` for an example, and the [resulting report](./examples/pygal.html).


### SVG

SVG rendering can be tweaked with keyword arguments passed to the `Report.widget` calls.

- `inherit_font` (default `True`) the font inside the figure is replaced by the report's font
- `width`/`height` override the width/height of the SVG in inches
- `scale` (default `down`) control the scaling behavior of the SVG: `full` sets the width/height to 100% of the parent container. `fixed` sets the specified widths and heights, `down` preserves the height of the original SVG, and sets the width to `100%`.

## Data

It also supports displaying large [pandas]() dataframes as tables (using [tabulator](http://tabulator.info/)).

Checkout the `examples/renderers/table.py` for an example, and the [resulting report](./examples/table.html).


## Typesetting

### Code

It is possible to render syntax-highlighted code with [highlightjs](https://highlightjs.org/). To do so, pass a `CodeContent` structure to `Report.widget`, for example:

```python
from vizno.renderers.code import CodeContent
r.widget( CodeContent(
        code="""
def do_something(argument):
    print(f"Hello {argument}!")
do_something("ok)
""",
        language="python",
    )
)
```

Checkout the `examples/renderers/code.py` for an example, and the [resulting report](./examples/code.html).


### LaTeX

It is possible to render full LaTeX documents by passing a `LatexContent(text=...)` object to a widget. It will be rendered with [latex.js](https://latex.js.org/).

Checkout the `examples/renderers/latex.py` for an example, and the [resulting report](./examples/latex.html).

### MathJax

It is possible to render full MathJax documents by passing a `MathJaxContent(text=...)` object to a widget. It will be rendered with [mathjax](https://www.mathjax.org/).

Checkout the `examples/renderers/mathjax.py` for an example, and the [resulting report](./examples/mathjax.html).

## Custom rendering

!!! warning This section requires some knowledge of JS/React

It is possible to provide a completely custom renderer that will render its content inside a widget. To do so you need two files.

In the python file, define the necessary configurations and register your rendering function with the main `vizno.renderers.render` dispact. as so:

```python
import pydantic

from vizno.renderers import ContentConfiguration, render
from vizno.report import Report


class CustomObject(pydantic.BaseModel):
    ...


class CustomRenderConfiguration(ContentConfiguration):
    ...

@render.register
def _(obj: CustomObject):
    ...
    return CustomRenderConfiguration(
        component="MyCustomComponent",
        component_module="my_renderer.js",
        parameter=obj.parameter
    )

```

The second file should expose a custom Preact+htm component. Its props will be the fields of the `ContentConfiguration` defined in the python file. Here is a possible content for `my_renderer.js`:

```js
function MyCustomComponent(props) {
  return html`<p>something</p>`;
}
```

When rendering, the `my_renderer.js` file will be moved to within the render directory (or served as a static file). When `vizno-core.js` encounters a widget content that has `component_module="my_renderer.js"` it will attempt to import it (by adding a `script` node), and then render the content by looking for `window.MyCustomComponent`.

Checkout the `examples/custom_renderer/custom_renderer.py` for an example.

### With external dependencies

If you need external dependencies, you first need to define them in Python. Add the necessary URLs as lists of strings in the `external_js_dependencies` and `external_css_dependencies` fields of the of the `ContentConfiguration` you return.

In JS you can use the custom `useDependencies` hook which will import dependencies for you (no need to import it) and make sure that they are correctly loaded before rendering (as well as controlling that each external library is only loaded once).

A typical pattern looks like this:

In Python:

```python

@render.register
def _(obj: CustomObject):
    ...
    return CustomRenderConfiguration(
        component="MyCustomComponent",
        component_module="my_renderer.js",
        parameter=parameter
        external_js_dependencies=["https://where.my/js/lives", ...]
        external_js_dependencies=["https://where.my/css/lives", ...]
    )

```

In `my_renderer.js`:

```js
function MyCustomComponent({
  external_js_dependencies,
  external_css_dependencies,
  some_parameter,
}) {
  const ready = useDependencies({
    componentName: "MyCustomComponent",
    jsDependencies: external_js_dependencies,
    cssDependencies: external_css_dependencies,
  });

  const divRef = useRef(null);

  useEffect(() => {
    if (divRef.current && ready) {
      window.YourImportedLibrary.doSomething(divRef.current, some_parameter);
    }
  }, [divRef, ready, some_parameter]);

  return html`<div ref="${divRef}" />`;
}
```
