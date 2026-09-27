from __future__ import annotations

from typing import Tuple

from dash import Dash, Input, Output, dcc, html

from ui import ids

PORTFOLIO_PATH = "/"
GBS_PATH = "/gbs"

VISIBLE = {"display": "block"}
HIDDEN = {"display": "none"}
ACTIVE_LINK_CLASS = "nav-link active"
LINK_CLASS = "nav-link"


def build_navigation() -> html.Nav:
    return html.Nav(
        className="top-nav",
        children=[
            dcc.Link("1 · Klasické Monte Carlo", href=PORTFOLIO_PATH, id=ids.NAV_PORTFOLIO_LINK, className=LINK_CLASS),
            dcc.Link("2 · Monte Carlo na GBS", href=GBS_PATH, id=ids.NAV_GBS_LINK, className=LINK_CLASS),
        ],
    )


def register_navigation_callbacks(app: Dash) -> None:
    app.callback(
        Output(ids.PORTFOLIO_PAGE, "style"),
        Output(ids.GBS_PAGE, "style"),
        Output(ids.NAV_PORTFOLIO_LINK, "className"),
        Output(ids.NAV_GBS_LINK, "className"),
        Input(ids.URL, "pathname"),
    )(show_page)


def show_page(pathname: str) -> Tuple[dict, dict, str, str]:
    """Both pages stay mounted and are only hidden, so the GBS page can read the portfolio form."""
    if pathname == GBS_PATH:
        return HIDDEN, VISIBLE, LINK_CLASS, ACTIVE_LINK_CLASS
    return VISIBLE, HIDDEN, ACTIVE_LINK_CLASS, LINK_CLASS
