from __future__ import annotations

from typing import Dict, FrozenSet, Tuple

from dash import Dash, Input, Output

from ui import ids
from ui.generated_topics import generated_page_ids, generated_paths
from ui.knowledge_map_content import LAYERS

TOPICS_PATH = "/"
ACADEMY_PATH = "/quantum-academy"
KNOWLEDGE_MAP_PATH = "/mapa"
"""Kept as an alias of the home page, where the knowledge map now lives."""
PORTFOLIO_PATH = "/klasicke-monte-carlo"
GBS_PATH = "/gbs"
CAVEATS_PATH = "/gbs/hacky"
THEORY_PATH = "/gbs/teorie"
HAFNIAN_PATH = "/gbs/hafnian"
ADVANTAGE_PATH = "/vyhoda-gbs"
GUIDE_PATH = "/vyhoda-gbs/pruvodce"
QPURPOSE_PATH = "/vyhoda-gbs/qpurpose"
ANDERSEN_SHAN_PAPER_PATH = "/vyhoda-gbs/clanek-andersen-shan"
VQE_PAPER_PATH = "/kvantova-optimalizace/vqe-ibm-fez"
LITERATURE_REVIEW_PATH = "/reserse-gbs-financni-riziko"
PHOTONIC_HARDWARE_PATH = "/reserse-gbs-financni-riziko/fotonicky-hardware"
PHOTONICS_LANDSCAPE_PATH = "/fotonika-ve-svete"
PIQUASSO_PATH = "/fotonika-ve-svete/piquasso"
PSIQUANTUM_PATH = "/fotonika-ve-svete/psiquantum"
PRIMER_BASICS_PATH = "/fotonika/zaklady"
PRIMER_GAUSSIAN_STATES_PATH = "/fotonika/gaussovske-stavy"
PRIMER_PHASE_SPACE_PATH = "/fotonika/fazovy-prostor"
PRIMER_GBS_PATH = "/fotonika/gaussian-boson-sampling"
PRIMER_APPENDICES_PATH = "/fotonika/dodatky"
WALTHER_LECTURE_PATH = "/fotonika/prednaska-walther-2022"
GHZ_STATES_PATH = "/fotonika/prednaska-walther-2022/ghz-stavy"
RANDOM_MATRIX_PATH = "/nahodne-matice-portfolio"
RANDOM_MATRIX_GBS_PATH = "/vyzkumne-smery/nahodne-matice-a-gbs"
FAILURE_DIAGNOSTICS_PATH = "/vyzkumne-smery/kdy-gbs-selze"
INTEGRALS_CHEAT_SHEET_PATH = "/tahaky/integraly"

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
    ids.HAFNIAN_PAGE,
    ids.ADVANTAGE_PAGE,
    ids.GUIDE_PAGE,
    ids.QPURPOSE_PAGE,
    ids.ANDERSEN_SHAN_PAPER_PAGE,
    ids.VQE_PAPER_PAGE,
    ids.LITERATURE_REVIEW_PAGE,
    ids.PHOTONIC_HARDWARE_PAGE,
    ids.PHOTONICS_LANDSCAPE_PAGE,
    ids.PIQUASSO_PAGE,
    ids.PSIQUANTUM_PAGE,
    ids.PRIMER_BASICS_PAGE,
    ids.PRIMER_GAUSSIAN_STATES_PAGE,
    ids.PRIMER_PHASE_SPACE_PAGE,
    ids.PRIMER_GBS_PAGE,
    ids.PRIMER_APPENDICES_PAGE,
    ids.WALTHER_LECTURE_PAGE,
    ids.GHZ_STATES_PAGE,
    ids.RANDOM_MATRIX_PAGE,
    ids.RANDOM_MATRIX_GBS_PAGE,
    ids.FAILURE_DIAGNOSTICS_PAGE,
    ids.INTEGRALS_CHEAT_SHEET_PAGE,
) + generated_page_ids()
NAV_LINK_IDS = (ids.NAV_TOPICS_LINK,) + tuple(info.menu_id for info in LAYERS)
"""Top-level menu entries: the home page with the knowledge map and one drop-down per group of pages."""
PAGE_BY_PATH = {
    TOPICS_PATH: ids.TOPICS_PAGE,
    KNOWLEDGE_MAP_PATH: ids.TOPICS_PAGE,
    ACADEMY_PATH: ids.ACADEMY_PAGE,
    PORTFOLIO_PATH: ids.PORTFOLIO_PAGE,
    GBS_PATH: ids.GBS_PAGE,
    CAVEATS_PATH: ids.CAVEATS_PAGE,
    THEORY_PATH: ids.THEORY_PAGE,
    HAFNIAN_PATH: ids.HAFNIAN_PAGE,
    ADVANTAGE_PATH: ids.ADVANTAGE_PAGE,
    GUIDE_PATH: ids.GUIDE_PAGE,
    QPURPOSE_PATH: ids.QPURPOSE_PAGE,
    ANDERSEN_SHAN_PAPER_PATH: ids.ANDERSEN_SHAN_PAPER_PAGE,
    VQE_PAPER_PATH: ids.VQE_PAPER_PAGE,
    LITERATURE_REVIEW_PATH: ids.LITERATURE_REVIEW_PAGE,
    PHOTONIC_HARDWARE_PATH: ids.PHOTONIC_HARDWARE_PAGE,
    PHOTONICS_LANDSCAPE_PATH: ids.PHOTONICS_LANDSCAPE_PAGE,
    PIQUASSO_PATH: ids.PIQUASSO_PAGE,
    PSIQUANTUM_PATH: ids.PSIQUANTUM_PAGE,
    PRIMER_BASICS_PATH: ids.PRIMER_BASICS_PAGE,
    PRIMER_GAUSSIAN_STATES_PATH: ids.PRIMER_GAUSSIAN_STATES_PAGE,
    PRIMER_PHASE_SPACE_PATH: ids.PRIMER_PHASE_SPACE_PAGE,
    PRIMER_GBS_PATH: ids.PRIMER_GBS_PAGE,
    PRIMER_APPENDICES_PATH: ids.PRIMER_APPENDICES_PAGE,
    WALTHER_LECTURE_PATH: ids.WALTHER_LECTURE_PAGE,
    GHZ_STATES_PATH: ids.GHZ_STATES_PAGE,
    RANDOM_MATRIX_PATH: ids.RANDOM_MATRIX_PAGE,
    RANDOM_MATRIX_GBS_PATH: ids.RANDOM_MATRIX_GBS_PAGE,
    FAILURE_DIAGNOSTICS_PATH: ids.FAILURE_DIAGNOSTICS_PAGE,
    INTEGRALS_CHEAT_SHEET_PATH: ids.INTEGRALS_CHEAT_SHEET_PAGE,
    **generated_paths(),
}
ACTIVE_LINKS_BY_PAGE: Dict[str, FrozenSet[str]] = {
    ids.TOPICS_PAGE: frozenset({ids.NAV_TOPICS_LINK}),
    **{page_id: frozenset({info.menu_id}) for info in LAYERS for page_id in info.page_ids},
}

# Pages are only hidden, so the browser cannot jump to an anchor on its own. Formulas (MathJax)
# and charts also render after navigation and push the target down, so the target is kept in
# view until the layout settles, unless the user starts scrolling first. A page sent on its first
# visit can block the browser for many seconds while MathJax sets it, so the settling is counted
# in checks after the target appears (a blocked browser runs none), not in time since the click.
SCROLL_TO_ANCHOR_JS = """
function(hash, pathname) {
    const targetId = hash ? decodeURIComponent(hash.slice(1)) : "";
    if (!targetId) {
        window.scrollTo(0, 0);
        return;
    }
    const checkMilliseconds = 100;
    const settleChecks = 30;
    const giveUpMilliseconds = 30000;
    const startedAt = Date.now();
    let checksInView = 0;
    let userTookOver = false;
    ["wheel", "touchstart", "keydown", "mousedown"].forEach((eventType) =>
        window.addEventListener(eventType, () => { userTookOver = true; }, {once: true, passive: true})
    );
    const keepTargetInView = () => {
        if (userTookOver || checksInView >= settleChecks || Date.now() - startedAt > giveUpMilliseconds) {
            return;
        }
        const target = document.getElementById(targetId);
        if (target && target.offsetParent !== null) {
            target.scrollIntoView({block: "start"});
            checksInView += 1;
        }
        setTimeout(keepTargetInView, checkMilliseconds);
    };
    keepTargetInView();
}
"""


def caveat_href(anchor: str) -> str:
    return f"{CAVEATS_PATH}#{anchor}"


def theory_href(anchor: str) -> str:
    return f"{THEORY_PATH}#{anchor}"


def hafnian_href(anchor: str) -> str:
    return f"{HAFNIAN_PATH}#{anchor}"


def guide_href(anchor: str) -> str:
    return f"{GUIDE_PATH}#{anchor}"


def qpurpose_href(anchor: str) -> str:
    return f"{QPURPOSE_PATH}#{anchor}"


def andersen_shan_paper_href(anchor: str) -> str:
    return f"{ANDERSEN_SHAN_PAPER_PATH}#{anchor}"


def integrals_cheat_sheet_href(anchor: str) -> str:
    return f"{INTEGRALS_CHEAT_SHEET_PATH}#{anchor}"


def literature_review_href(anchor: str) -> str:
    return f"{LITERATURE_REVIEW_PATH}#{anchor}"


def photonic_hardware_href(anchor: str) -> str:
    return f"{PHOTONIC_HARDWARE_PATH}#{anchor}"


def photonics_landscape_href(anchor: str) -> str:
    return f"{PHOTONICS_LANDSCAPE_PATH}#{anchor}"


def piquasso_href(anchor: str) -> str:
    return f"{PIQUASSO_PATH}#{anchor}"


def psiquantum_href(anchor: str) -> str:
    return f"{PSIQUANTUM_PATH}#{anchor}"


def walther_lecture_href(anchor: str) -> str:
    return f"{WALTHER_LECTURE_PATH}#{anchor}"


def ghz_states_href(anchor: str) -> str:
    return f"{GHZ_STATES_PATH}#{anchor}"


PHOTONICS_TERMS_HREF = photonics_landscape_href("svet-pojmy")
PHOTONICS_TOPIC_ANCHOR = "tema-fotonika"
PHOTONICS_TOPIC_HREF = f"{TOPICS_PATH}#{PHOTONICS_TOPIC_ANCHOR}"
"""Chapter on modes, nonlinear crystals and squeezed light; pages that mention them link to it."""


def random_matrix_href(anchor: str) -> str:
    return f"{RANDOM_MATRIX_PATH}#{anchor}"


def random_matrix_gbs_href(anchor: str) -> str:
    return f"{RANDOM_MATRIX_GBS_PATH}#{anchor}"


def failure_diagnostics_href(anchor: str) -> str:
    return f"{FAILURE_DIAGNOSTICS_PATH}#{anchor}"


def register_navigation_callbacks(app: Dash) -> None:
    app.callback(
        [Output(page_id, "style") for page_id in PAGE_IDS] + [Output(link_id, "className") for link_id in NAV_LINK_IDS],
        Input(ids.URL, "pathname"),
    )(show_page)
    app.clientside_callback(SCROLL_TO_ANCHOR_JS, Input(ids.URL, "hash"), Input(ids.URL, "pathname"))


def show_page(pathname: str) -> Tuple:
    """All pages stay mounted and are only hidden, so forms and results survive switching pages."""
    page = PAGE_BY_PATH.get(pathname, ids.TOPICS_PAGE)
    styles = tuple(VISIBLE if page_id == page else HIDDEN for page_id in PAGE_IDS)
    active_links = ACTIVE_LINKS_BY_PAGE[page]
    link_classes = tuple(ACTIVE_LINK_CLASS if link_id in active_links else LINK_CLASS for link_id in NAV_LINK_IDS)
    return styles + link_classes
