"""Top menu: the same five groups of pages as the topics dashboard and the knowledge map, each as a drop-down.

Opening and closing is plain browser behaviour of <details>, tidied up by assets/menu.js (one group open at a time,
closing after navigation, the toggle on narrow screens), so it needs no server round trip.
"""

from __future__ import annotations

from dash import dcc, html

from auth.login import LOGOUT_PATH
from ui import ids
from ui.assistant_content import AGENTS_LABEL
from ui.knowledge_map_content import LAYERS, LayerInfo
from ui.lecture_requests_content import TITLE as LECTURE_REQUESTS_TITLE
from ui.navigation import AGENTS_PATH, LECTURE_REQUESTS_PATH, LINK_CLASS, TOPICS_PATH
from ui.topic_catalog import page_entries

MENU_CLASS = "top-nav"
MENU_BUTTON_LABEL = "☰ Menu"


def build_main_menu() -> html.Header:
    return html.Header(
        className="site-header",
        children=[
            html.Div(className="menu-bar", children=[
                html.Button(MENU_BUTTON_LABEL, id=ids.MENU_TOGGLE, className="menu-toggle", n_clicks=0),
            ]),
            html.Nav(
                id=ids.MAIN_MENU,
                className=MENU_CLASS,
                children=[
                    dcc.Link("Témata a mapa", href=TOPICS_PATH, id=ids.NAV_TOPICS_LINK, className=LINK_CLASS),
                    *[_group_menu(info) for info in LAYERS],
                    dcc.Link(LECTURE_REQUESTS_TITLE, href=LECTURE_REQUESTS_PATH, id=ids.NAV_LECTURE_REQUESTS_LINK,
                             className=LINK_CLASS),
                    _account_links(),
                ],
            ),
        ],
    )


def _account_links() -> html.Div:
    """Agents and logout at the right end of the bar; grouped, so that they wrap to a new row together."""
    return html.Div(className="nav-account", children=[
        # The label gets the number of proposals waiting for approval (ui/assistant_callbacks.py).
        dcc.Link(AGENTS_LABEL, href=AGENTS_PATH, id=ids.NAV_AGENTS_LINK, className=LINK_CLASS),
        html.A("Odhlásit", href=LOGOUT_PATH, className=LINK_CLASS),
    ])


def _group_menu(info: LayerInfo) -> html.Details:
    entries = page_entries()
    return html.Details(
        id=info.menu_id,
        className=LINK_CLASS,
        open=False,
        children=[
            html.Summary([html.Span(className="layer-dot", style={"background": info.color}), info.title]),
            html.Div(className="submenu", children=[
                html.P(info.role, className="submenu-role"),
                *[
                    dcc.Link(entries[page_id].title, href=entries[page_id].path, className="submenu-link")
                    for page_id in info.page_ids
                ],
            ]),
        ],
    )
