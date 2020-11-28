import os

from vizno.renderers.latex import LatexContent
from vizno.report import Report

r = Report()
r.widget(
    LatexContent(
        text=open(os.path.join(os.path.dirname(__file__), "something.tex")).read()
    )
)
