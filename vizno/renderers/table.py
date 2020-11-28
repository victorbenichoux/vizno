# -*- coding: utf-8 -*-
import uuid
from typing import List

import pandas as pd

from vizno.renderers import ContentConfiguration, render


class TableContentConfiguration(ContentConfiguration):
    component: str = "TableContent"
    data: List[dict]
    columns: List[str]
    content_uuid: str


@render.register
def _(df: pd.DataFrame):
    return TableContentConfiguration(
        data=[{c: getattr(row, c) for c in df.columns} for row in df.itertuples()],
        columns=[c for c in df.columns],
        external_js_dependencies=[
            "https://unpkg.com/tabulator-tables@4.9.1/dist/js/tabulator_core.min.js",
            "https://unpkg.com/tabulator-tables@4.9.1/dist/js/modules/sort.min.js",
        ],
        external_css_dependencies=[
            "https://unpkg.com/tabulator-tables@4.9.1/dist/css/tabulator_simple.min.css"
        ],
        content_uuid=f"table-{uuid.uuid4().hex[:8]}",
    )
