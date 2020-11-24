import importlib.resources
import os
import shutil
from typing import Dict

import vizno.js


def copy_resource(resource_name: str, output_dir: str):
    with importlib.resources.open_binary(vizno.js, resource_name) as fresource:
        with open(os.path.join(output_dir, resource_name), "wb") as fdestination:
            shutil.copyfileobj(fresource, fdestination)


def copy_index_template(
    template_name: str,
    output_dir: str,
    external_js_dependencies: Dict[str, None],
    external_css_dependencies: Dict[str, None],
):
    with importlib.resources.open_text(vizno.js, template_name) as fin:
        with open(os.path.join(output_dir, template_name), "w") as fout:
            for l in fin:
                fout.write(l)
                if "<!-- external_js_dependencies -->" in l:
                    for dep in external_js_dependencies:
                        fout.write(f"""    <script defer src="{dep}"></script>\n""")
                if "<!-- external_css_dependencies -->" in l:
                    for dep in external_css_dependencies:
                        fout.write(f"""    <link rel="stylesheet" href="{dep}" />\n""")
