import os
import shutil
from typing import Dict

import pkg_resources


def copy_template(template_name: str, output_dir: str):
    shutil.copyfile(
        pkg_resources.resource_filename("vyz", os.path.join("js", template_name)),
        os.path.join(output_dir, template_name),
    )


def copy_index_template(
    template_name: str,
    output_dir: str,
    external_js_dependencies: Dict[str, None],
    external_css_dependencies: Dict[str, None],
):
    with open(
        pkg_resources.resource_filename("vyz", os.path.join("js", template_name))
    ) as fin:
        with open(os.path.join(output_dir, template_name), "w") as fout:
            for l in fin:
                fout.write(l)
                if "<!-- external_js_dependencies -->" in l:
                    for dep in external_js_dependencies:
                        fout.write(f"""    <script defer src="{dep}"></script>\n""")
                if "<!-- external_css_dependencies -->" in l:
                    for dep in external_css_dependencies:
                        fout.write(f"""    <link rel="stylesheet" href="{dep}" />\n""")
