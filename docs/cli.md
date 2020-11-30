
`vizno` provides a command line interface to generate reports:

## Render as a server

Render the report and serve it within a webserver. This will automatically reload the page on changes to the report file.

```bash
vizno render path/to/you/report.py serve
```

## Render to directory

```bash
vizno render path/to/you/report.py --output-dir path/to/generate [--reload]
```

Turning the `--reload` flag on will re-generate the report if the report file changes.
