from vizno.renderers.code import CodeContent
from vizno.report import Report

r = Report()
r.widget(
    CodeContent(
        code="""
def do_something(argument):
    print(f"Hello {argument}!")
do_something("ok)
""",
        language="python",
    )
)
