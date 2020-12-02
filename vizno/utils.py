import importlib.resources
import shutil
from typing import Dict, Optional

import vizno.statics


def copy_resource(
    resource_name: str, output_fn: str, replace: Optional[Dict[str, str]] = None
):
    if not replace:
        with importlib.resources.open_binary(
            vizno.statics, resource_name
        ) as fresource_bin:
            with open(output_fn, "wb") as fdestination_bin:
                shutil.copyfileobj(fresource_bin, fdestination_bin)
    else:
        with importlib.resources.open_text(vizno.statics, resource_name) as fresource:
            with open(output_fn, "w") as fdestination:
                for l in fresource:
                    newl = l
                    for pattern, replacement in replace.items():
                        newl = newl.replace(pattern, replacement)
                    fdestination.write(newl)
