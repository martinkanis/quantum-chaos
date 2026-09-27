from __future__ import annotations

from typing import Tuple

from dash import Dash, Input, Output, dcc, html

from ui import ids

PORTFOLIO_PATH = "/"
GBS_PATH = "/gbs"
CAVEATS_PATH = "/gbs/hacky"

VISIBLE = {"display": "block"}
HIDDEN = {"display": "none"}
ACTIVE_LINK_CLASS = "nav-link active"
LINK_CLASS = "nav-link"

PAGE_IDS = (ids.PORTFOLIO_PAGE, ids.GBS_PAGE, ids.CAVEATS_PAGE)
NAV_LINK_IDS = (ids.NAV_PORTFOLIO_LINK, ids.NAV_GBS_LINK)
PAGE_BY_PATH = {PORTFOLIO_PATH: ids.PORTFOLIO_PAGE, GBS_PATH: ids.GBS_PAGE, CAVEATS_PATH: ids.CAVEATS_PAGE}
ACTIVE_LINK_BY_PAGE = {
    ids.PORTFOLIO_PAGE: ids.NAV_PORTFOLIO_LINK,
    ids.GBS_PAGE: ids.NAV_GBS_LINK,
    ids.CAVEATS_PAGE: ids.NAV_GBS_LINK,
}

# Pages are only hidden, so the browser cannot jump to an anchor on its own. Formulas (MathJax)
# and charts also render after navigation and push the target down, so the target is kept in
# view until the layout settles, unless the user starts scrolling first.
SCROLL_TO_ANCHOR_JS = """
function(hash, pathname) {
    const targetId = hash ? decodeURIComponent(hash.slice(1)) : "";
    if (!targetId) {
        window.scrollTo(0, 0);
        return;
    }
    const settleMilliseconds = 3000;
    const startedAt = Date.now();
    let userTookOver = false;
    ["wheel", "touchstart", "keydown", "mousedown"].forEach((eventType) =>
        window.addEventListener(eventType, () => { userTookOver = true; }, {once: true, passive: true})
    );
    const keepTargetInView = () => {
        if (userTookOver || Date.now() - startedAt > settleMilliseconds) {
            return;
        }
        const target = document.getElementById(targetId);
        if (target && target.offsetParent !== null) {
            target.scrollIntoView({block: "start"});
        }
        setTimeout(keepTargetInView, 100);
    };
    keepTargetInView();
}
"""


def caveat_href(anchor: str) -> str:
    return f"{CAVEATS_PATH}#{anchor}"


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
        [Output(page_id, "style") for page_id in PAGE_IDS]
        + [Output(link_id, "className") for link_id in NAV_LINK_IDS],
        Input(ids.URL, "pathname"),
    )(show_page)
    app.clientside_callback(SCROLL_TO_ANCHOR_JS, Input(ids.URL, "hash"), Input(ids.URL, "pathname"))


def show_page(pathname: str) -> Tuple:
    """All pages stay mounted and are only hidden, so the GBS page can read the portfolio form."""
    page = PAGE_BY_PATH.get(pathname, ids.PORTFOLIO_PAGE)
    styles = tuple(VISIBLE if page_id == page else HIDDEN for page_id in PAGE_IDS)
    active_link = ACTIVE_LINK_BY_PAGE[page]
    link_classes = tuple(ACTIVE_LINK_CLASS if link_id == active_link else LINK_CLASS for link_id in NAV_LINK_IDS)
    return styles + link_classes
