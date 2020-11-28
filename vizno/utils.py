import importlib.resources
import os
import shutil

import vizno.statics


def copy_resource(resource_name: str, output_dir: str):
    with importlib.resources.open_binary(vizno.statics, resource_name) as fresource:
        with open(os.path.join(output_dir, resource_name), "wb") as fdestination:
            shutil.copyfileobj(fresource, fdestination)
