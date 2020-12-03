<p align="center">
  <a href="https://github.com/victorbenichoux/vizno">
    <img src="https://raw.githubusercontent.com/victorbenichoux/vizno/main/.github/resources/vizno.svg" alt="Logo" width="80" height="80">
  </a>
</p>
<h1 align="center"> vizno </h1>
<p align="center">
  <em>Layout python visualizations in HTML reports.</em>
</p>
    
---

`vizno` lays out and renders your Python visualizations in lightweight web pages. They can either be shared as standalone files, or rendered with fastAPI.

Check out the [demonstration report](https://victorbenichoux.github.io/vizno/examples/demo.html) for a demonstration of what it looks like, it's a single HTML file!

## Quickstart

You can use `vizno` with your existing Python code in no time:

```python
from vizno import Report

r = Report()

f = ... # your existing figure generating code

r.widget(f)

r.render(output_dir) # output a standalone HTML report to a directory
```

Refer to the [documentation](https://victorbenichoux.github.io/vizno/) for more information.

## Content supported

`vizno` supports rendering objects from the major Python visualization libraries:

- [matplotlib](https://matplotlib.org/)
- [altair](https://altair-viz.github.io/)
- [bokeh](https://docs.bokeh.org/en/latest/index.html#)
- [plotly](https://github.com/plotly/plotly.py)
- [pygal](http://www.pygal.org/en/stable/)

It also supports displaying [pandas]() dataframes as tables (using [tabulator](http://tabulator.info/)).

Finally, `vizno` supports advanced typesetting within the reports:

- Markdown titles, labels and all text with [snarkdown](https://github.com/developit/snarkdown)
- code display with [highlightjs](https://highlightjs.org/)
- LaTeX documents with [latex.js](https://latex.js.org/)
- MathJax formulas with [mathjax](https://www.mathjax.org/)

## Features

`vizno` is easy to use and involves little boilerplate code. Just create a `Report` and pass it existing figure objects.

`vizno` pages can straightforwardly be served with [fastapi](), or as HTML files renderable in any browser

`vizno` is lightweight, it uses [Preact]() and will only retrieve and load libraries that are used in each page. The size of the complete vizno overhead code is < 10kB.

`vizno` is extendable, adding your own components to render arbitrary code is very simple.

`vizno` includes sensible tooling that allows you to quickly iterate on your reports.

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

## License

Distributed under the MIT License. See `LICENSE` for more information.
