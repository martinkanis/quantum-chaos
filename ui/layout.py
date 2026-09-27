from __future__ import annotations

from dash import dcc, html

from ui import ids
from ui.caveats_page import build_caveats_page
from ui.gbs_page import build_gbs_page
from ui.navigation import build_navigation
from ui.portfolio_page import build_portfolio_page


def build_layout() -> html.Div:
    return html.Div(
        children=[
            dcc.Location(id=ids.URL),
            build_navigation(),
            build_portfolio_page(),
            build_gbs_page(),
            build_caveats_page(),
        ]
    )
