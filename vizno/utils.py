import importlib.resources
import os
import shutil

import vizno.js


def copy_resource(resource_name: str, output_dir: str):
    with importlib.resources.open_binary(vizno.js, resource_name) as fresource:
        with open(os.path.join(output_dir, resource_name), "wb") as fdestination:
            shutil.copyfileobj(fresource, fdestination)
