from __future__ import annotations

from typing import Dict, FrozenSet, Tuple

from dash import Dash, Input, Output, dcc, html

from auth.login import LOGOUT_PATH
from ui import ids

TOPICS_PATH = "/"
ACADEMY_PATH = "/quantum-academy"
PORTFOLIO_PATH = "/klasicke-monte-carlo"
GBS_PATH = "/gbs"
CAVEATS_PATH = "/gbs/hacky"
THEORY_PATH = "/gbs/teorie"
ADVANTAGE_PATH = "/vyhoda-gbs"
GUIDE_PATH = "/vyhoda-gbs/pruvodce"
QPURPOSE_PATH = "/vyhoda-gbs/qpurpose"
VQE_PAPER_PATH = "/kvantova-optimalizace/vqe-ibm-fez"
LITERATURE_REVIEW_PATH = "/reserse-gbs-financni-riziko"
RANDOM_MATRIX_PATH = "/nahodne-matice-portfolio"
RANDOM_MATRIX_GBS_PATH = "/vyzkumne-smery/nahodne-matice-a-gbs"
FAILURE_DIAGNOSTICS_PATH = "/vyzkumne-smery/kdy-gbs-selze"

VISIBLE: dict = {}
"""No inline display, so the stylesheet decides how a shown element is laid out (reading pages use a grid)."""
HIDDEN = {"display": "none"}
ACTIVE_LINK_CLASS = "nav-link active"
LINK_CLASS = "nav-link"

PAGE_IDS = (
    ids.TOPICS_PAGE,
    ids.ACADEMY_PAGE,
    ids.PORTFOLIO_PAGE,
    ids.GBS_PAGE,
    ids.CAVEATS_PAGE,
    ids.THEORY_PAGE,
    ids.ADVANTAGE_PAGE,
    ids.GUIDE_PAGE,
    ids.QPURPOSE_PAGE,
    ids.VQE_PAPER_PAGE,
    ids.LITERATURE_REVIEW_PAGE,
    ids.RANDOM_MATRIX_PAGE,
    ids.RANDOM_MATRIX_GBS_PAGE,
    ids.FAILURE_DIAGNOSTICS_PAGE,
)
MONTE_CARLO_PAGES = frozenset({
    ids.PORTFOLIO_PAGE, ids.GBS_PAGE, ids.CAVEATS_PAGE, ids.THEORY_PAGE, ids.ADVANTAGE_PAGE, ids.GUIDE_PAGE,
    ids.QPURPOSE_PAGE,
})
NAV_LINK_IDS = (
    ids.NAV_TOPICS_LINK,
    ids.NAV_MONTE_CARLO_LINK,
    ids.NAV_LITERATURE_REVIEW_LINK,
    ids.NAV_OPTIMIZATION_LINK,
    ids.NAV_RANDOM_MATRIX_LINK,
    ids.NAV_RESEARCH_DIRECTIONS_LINK,
    ids.NAV_ACADEMY_LINK,
    ids.NAV_PORTFOLIO_LINK,
    ids.NAV_GBS_LINK,
    ids.NAV_ADVANTAGE_LINK,
)
PAGE_BY_PATH = {
    TOPICS_PATH: ids.TOPICS_PAGE,
    ACADEMY_PATH: ids.ACADEMY_PAGE,
    PORTFOLIO_PATH: ids.PORTFOLIO_PAGE,
    GBS_PATH: ids.GBS_PAGE,
    CAVEATS_PATH: ids.CAVEATS_PAGE,
    THEORY_PATH: ids.THEORY_PAGE,
    ADVANTAGE_PATH: ids.ADVANTAGE_PAGE,
    GUIDE_PATH: ids.GUIDE_PAGE,
    QPURPOSE_PATH: ids.QPURPOSE_PAGE,
    VQE_PAPER_PATH: ids.VQE_PAPER_PAGE,
    LITERATURE_REVIEW_PATH: ids.LITERATURE_REVIEW_PAGE,
    RANDOM_MATRIX_PATH: ids.RANDOM_MATRIX_PAGE,
    RANDOM_MATRIX_GBS_PATH: ids.RANDOM_MATRIX_GBS_PAGE,
    FAILURE_DIAGNOSTICS_PATH: ids.FAILURE_DIAGNOSTICS_PAGE,
}
ACTIVE_LINKS_BY_PAGE: Dict[str, FrozenSet[str]] = {
    ids.TOPICS_PAGE: frozenset({ids.NAV_TOPICS_LINK}),
    ids.ACADEMY_PAGE: frozenset({ids.NAV_ACADEMY_LINK}),
    ids.PORTFOLIO_PAGE: frozenset({ids.NAV_MONTE_CARLO_LINK, ids.NAV_PORTFOLIO_LINK}),
    ids.GBS_PAGE: frozenset({ids.NAV_MONTE_CARLO_LINK, ids.NAV_GBS_LINK}),
    ids.CAVEATS_PAGE: frozenset({ids.NAV_MONTE_CARLO_LINK, ids.NAV_GBS_LINK}),
    ids.THEORY_PAGE: frozenset({ids.NAV_MONTE_CARLO_LINK, ids.NAV_GBS_LINK}),
    ids.ADVANTAGE_PAGE: frozenset({ids.NAV_MONTE_CARLO_LINK, ids.NAV_ADVANTAGE_LINK}),
    ids.GUIDE_PAGE: frozenset({ids.NAV_MONTE_CARLO_LINK, ids.NAV_ADVANTAGE_LINK}),
    ids.QPURPOSE_PAGE: frozenset({ids.NAV_MONTE_CARLO_LINK, ids.NAV_ADVANTAGE_LINK}),
    ids.VQE_PAPER_PAGE: frozenset({ids.NAV_OPTIMIZATION_LINK}),
    ids.LITERATURE_REVIEW_PAGE: frozenset({ids.NAV_LITERATURE_REVIEW_LINK}),
    ids.RANDOM_MATRIX_PAGE: frozenset({ids.NAV_RANDOM_MATRIX_LINK}),
    ids.RANDOM_MATRIX_GBS_PAGE: frozenset({ids.NAV_RESEARCH_DIRECTIONS_LINK}),
    ids.FAILURE_DIAGNOSTICS_PAGE: frozenset({ids.NAV_RESEARCH_DIRECTIONS_LINK}),
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


def theory_href(anchor: str) -> str:
    return f"{THEORY_PATH}#{anchor}"


def guide_href(anchor: str) -> str:
    return f"{GUIDE_PATH}#{anchor}"


def qpurpose_href(anchor: str) -> str:
    return f"{QPURPOSE_PATH}#{anchor}"


def literature_review_href(anchor: str) -> str:
    return f"{LITERATURE_REVIEW_PATH}#{anchor}"


def random_matrix_href(anchor: str) -> str:
    return f"{RANDOM_MATRIX_PATH}#{anchor}"


def random_matrix_gbs_href(anchor: str) -> str:
    return f"{RANDOM_MATRIX_GBS_PATH}#{anchor}"


def failure_diagnostics_href(anchor: str) -> str:
    return f"{FAILURE_DIAGNOSTICS_PATH}#{anchor}"


def build_navigation() -> html.Header:
    """Topics in the top row; the pages of the Monte Carlo topic in a second row under it."""
    return html.Header(
        className="site-header",
        children=[
            html.Nav(
                className="top-nav",
                children=[
                    dcc.Link("Témata", href=TOPICS_PATH, id=ids.NAV_TOPICS_LINK, className=LINK_CLASS),
                    dcc.Link("Monte Carlo", href=PORTFOLIO_PATH, id=ids.NAV_MONTE_CARLO_LINK, className=LINK_CLASS),
                    dcc.Link(
                        "Rešerše GBS", href=LITERATURE_REVIEW_PATH, id=ids.NAV_LITERATURE_REVIEW_LINK,
                        className=LINK_CLASS,
                    ),
                    dcc.Link(
                        "Kvantová optimalizace", href=VQE_PAPER_PATH, id=ids.NAV_OPTIMIZATION_LINK,
                        className=LINK_CLASS,
                    ),
                    dcc.Link(
                        "Náhodné matice", href=RANDOM_MATRIX_PATH, id=ids.NAV_RANDOM_MATRIX_LINK,
                        className=LINK_CLASS,
                    ),
                    dcc.Link(
                        "Výzkumné směry", href=FAILURE_DIAGNOSTICS_PATH, id=ids.NAV_RESEARCH_DIRECTIONS_LINK,
                        className=LINK_CLASS,
                    ),
                    dcc.Link("Quantum Academy", href=ACADEMY_PATH, id=ids.NAV_ACADEMY_LINK, className=LINK_CLASS),
                    html.A("Odhlásit", href=LOGOUT_PATH, className="nav-link logout-link"),
                ],
            ),
            html.Nav(
                id=ids.MONTE_CARLO_SUBNAV,
                className="sub-nav",
                style=HIDDEN,
                children=[
                    dcc.Link("Klasické", href=PORTFOLIO_PATH, id=ids.NAV_PORTFOLIO_LINK, className=LINK_CLASS),
                    dcc.Link("Na GBS", href=GBS_PATH, id=ids.NAV_GBS_LINK, className=LINK_CLASS),
                    dcc.Link("Výhoda GBS", href=ADVANTAGE_PATH, id=ids.NAV_ADVANTAGE_LINK, className=LINK_CLASS),
                ],
            ),
        ],
    )


def register_navigation_callbacks(app: Dash) -> None:
    app.callback(
        [Output(page_id, "style") for page_id in PAGE_IDS]
        + [Output(link_id, "className") for link_id in NAV_LINK_IDS]
        + [Output(ids.MONTE_CARLO_SUBNAV, "style")],
        Input(ids.URL, "pathname"),
    )(show_page)
    app.clientside_callback(SCROLL_TO_ANCHOR_JS, Input(ids.URL, "hash"), Input(ids.URL, "pathname"))


def show_page(pathname: str) -> Tuple:
    """All pages stay mounted and are only hidden, so forms and results survive switching pages."""
    page = PAGE_BY_PATH.get(pathname, ids.TOPICS_PAGE)
    styles = tuple(VISIBLE if page_id == page else HIDDEN for page_id in PAGE_IDS)
    active_links = ACTIVE_LINKS_BY_PAGE[page]
    link_classes = tuple(ACTIVE_LINK_CLASS if link_id in active_links else LINK_CLASS for link_id in NAV_LINK_IDS)
    subnav_style = VISIBLE if page in MONTE_CARLO_PAGES else HIDDEN
    return styles + link_classes + (subnav_style,)
