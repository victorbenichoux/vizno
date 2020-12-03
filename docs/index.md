<p align="center">
  <a href="https://github.com/victorbenichoux/vizno">
    <img src="vizno.svg" alt="Logo" width="100" height="100">
  </a>
</p>
<p align="center">
  <em>Layout python visualizations in HTML reports.</em>
</p>
    

`vizno` allows you to generate lightweight, portable and servable reports by laying out text and graphics together.

Check out the [demonstration report](examples/demo.html) for a demonstration of what it looks like, it's a single HTML file!

# Installation

Install vizno with PyPi:

```bash
pip install vizno
```

# Quick start

Create a python script `my_report.py`:

```python
from vizno.report import Report

r = Report(
    title="Report title",
    description="Here goes the report _description_.",
)
# Write your figure generating code here ... 
f = ...

r.widget(f, title="Widget title", description="widget description")
```

At this point you have several options to generate the result.

Either:

- use the `vizno` CLI, and run a local HTTP server
    ```bash
    vizno serve my_report.py
    ```
- use the `vizno` CLI to generate a standalone HTML and associated files to `directory`:
    ```bash
    vizno render reports/demo.py --output-dir directory
    ```
- programmatically write to the directory with a `r.render(output_dir)` statement and simply run the python file
    ```bash
    python reports/demo.py
    ```

