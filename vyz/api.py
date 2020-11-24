import urllib.parse

import fastapi
import pkg_resources
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import RedirectResponse


class VyzApp(fastapi.FastAPI):
    def __init__(self, static_url: str = "/static", **kwargs):
        super().__init__(**kwargs)
        self.static_url = static_url
        self.mount(
            static_url,
            StaticFiles(directory=pkg_resources.resource_filename("vyz", "js")),
            name="static",
        )

    def report(self, path: str, *args, **kwargs):
        def report_redirect(request: Request):
            params = dict(request.query_params)
            params["configurationRequestURL"] = f"{path}_config"
            return RedirectResponse(
                url=f"{self.static_url}/index.html?{urllib.parse.urlencode(params)}"
            )

        self.router.add_api_route(
            path,
            report_redirect,
            methods={"GET"},
        )

        return self.get(f"{path}_config", *args, **kwargs)
