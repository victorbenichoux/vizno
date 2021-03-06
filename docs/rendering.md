## As standalone files

`vizno` reports generated by calling `render` in the python code, or using the `vizno render` CLI are standalone, and can be opened by openting `index.html` in the browser.

If the report depends on JS packages, they will be loaded at runtime. Although they can be retained in cache, they are not packaged alongside the document itself: opening the report requires an internet connection (except for SVG only renderers, i.e. matplotlib/pygal).

## In a FastAPI server

`vizno.api` exposes a `fastapi.FastAPI` subclass that allows you to quickly server `vizno` reports from a [fastapi]() app.

```python
from vizno.api import ViznoApp
from vizno.report import Report

app = ViznoApp()

@app.report("/your/endpoint/path")
def f():
    r = Report()
    # populate the report with elements...
    return r.get_configuration()
```

The app can then be mounted within your main `FastAPI` application.

### Using arguments

The `@app.report` decorator behaves mucbeh like a usual `@app.get` decorator in `fastapi`, and in particular it is possible to pass it arguments, which will be parsed when the report is requested.

See the example in `examples/api`.

### How it works

When initialized:

```python
app = ViznoApp(static_url: str = "/static", **kwargs)
```

creates a FastAPI app, and serves all static `vizno` files (JS, CSS, logo, `index.html`) under the `/static` path (using `fastapi.staticfiles.StaticFiles`).

When the `report` decorator is called:

```
@app.report("/your/endpoint/path")
def f(value: Optional[str] = None):
    r = Report()
    # populate the report with elements...
    return r.get_configuration()
```

It creates creates two endpoints in the `viznoapp`:

- a `GET` endpoint at `/your/endpoint/path_config`, with arguments/options specified as in `fastapi` from the function arguments. This endpoint will be called by the JS code in `index.html` to produce the report.
- a `GET` endpoint at `/your/endpoint/path` with the same with arguments/options. It will redirected towards `/static/index.html` with options set such that `index.html` will know to retrieve the configuration.



