"""Breadcrumb line under the navigation that shows where the current page sits among the topics."""

from __future__ import annotations

from typing import List, Tuple

from dash import Dash, Input, Output, dcc, html

from ui import ids
from ui.navigation import HIDDEN, PAGE_BY_PATH, VISIBLE
from ui.topic_catalog import Crumb, breadcrumb_trail

SEPARATOR = " › "


def build_breadcrumb() -> html.Nav:
    return html.Nav(id=ids.BREADCRUMB, className="breadcrumb", style=HIDDEN)


def register_breadcrumb_callbacks(app: Dash) -> None:
    app.callback(
        Output(ids.BREADCRUMB, "children"),
        Output(ids.BREADCRUMB, "style"),
        Input(ids.URL, "pathname"),
    )(describe_location)


def describe_location(pathname: str) -> Tuple[List, dict]:
    page_id = PAGE_BY_PATH.get(pathname)
    trail = breadcrumb_trail(page_id) if page_id else []
    if not trail:
        return [], HIDDEN
    return _crumbs(trail), VISIBLE


def _crumbs(trail: List[Crumb]) -> List:
    children: List = []
    for label, href in trail:
        if children:
            children.append(html.Span(SEPARATOR, className="breadcrumb-separator"))
        children.append(dcc.Link(label, href=href) if href else html.Span(label, className="breadcrumb-current"))
    return children
