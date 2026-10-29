"""Reading pages without forms reach the browser on their first visit instead of with the initial layout.

They made up most of the layout and almost all of its formulas, and the browser typeset every formula of every
hidden page on each load. Pages with forms stay in the initial layout, because Dash needs their callback inputs
from the start.
"""

from __future__ import annotations

from functools import lru_cache, partial
from typing import Callable, Dict, List, Optional

from dash import Dash, Input, Output, State, dcc, html, no_update

from ui import ids
from ui.academy_page import build_academy_page
from ui.andersen_shan_paper_page import build_andersen_shan_paper_page
from ui.caveats_page import build_caveats_page
from ui.failure_diagnostics_page import build_failure_diagnostics_page
from ui.generated_page import build_generated_page
from ui.generated_topics import GENERATED_TOPICS, generated_page_id
from ui.guide_page import build_guide_page
from ui.hafnian_page import build_hafnian_page
from ui.integrals_cheat_sheet_page import build_integrals_cheat_sheet_page
from ui.literature_review_page import build_literature_review_page
from ui.navigation import PAGE_BY_PATH
from ui.photonic_hardware_page import build_photonic_hardware_page
from ui.photonics_landscape_page import build_photonics_landscape_page
from ui.piquasso_page import build_piquasso_page
from ui.primer_page import PRIMER_CHAPTERS, build_primer_page
from ui.qpurpose_page import build_qpurpose_page
from ui.random_matrix_gbs_page import build_random_matrix_gbs_page
from ui.theory_page import build_theory_page
from ui.vqe_paper_page import build_vqe_paper_page
from ui.walther_lecture_page import build_walther_lecture_page

PAGE_BUILDERS: Dict[str, Callable[[], html.Div]] = {
    ids.ACADEMY_PAGE: build_academy_page,
    ids.CAVEATS_PAGE: build_caveats_page,
    ids.THEORY_PAGE: build_theory_page,
    ids.HAFNIAN_PAGE: build_hafnian_page,
    ids.GUIDE_PAGE: build_guide_page,
    ids.QPURPOSE_PAGE: build_qpurpose_page,
    ids.ANDERSEN_SHAN_PAPER_PAGE: build_andersen_shan_paper_page,
    ids.VQE_PAPER_PAGE: build_vqe_paper_page,
    ids.LITERATURE_REVIEW_PAGE: build_literature_review_page,
    ids.PHOTONIC_HARDWARE_PAGE: build_photonic_hardware_page,
    ids.PHOTONICS_LANDSCAPE_PAGE: build_photonics_landscape_page,
    ids.PIQUASSO_PAGE: build_piquasso_page,
    **{page_id: partial(build_primer_page, page_id) for page_id in PRIMER_CHAPTERS},
    ids.WALTHER_LECTURE_PAGE: build_walther_lecture_page,
    ids.FAILURE_DIAGNOSTICS_PAGE: build_failure_diagnostics_page,
    ids.RANDOM_MATRIX_GBS_PAGE: build_random_matrix_gbs_page,
    ids.INTEGRALS_CHEAT_SHEET_PAGE: build_integrals_cheat_sheet_page,
    **{generated_page_id(topic.slug): partial(build_generated_page, topic) for topic in GENERATED_TOPICS},
}
"""Pages loaded on their first visit; none of their components may be a callback input, state or output."""
LAZY_PAGE_IDS = tuple(PAGE_BUILDERS)


@lru_cache(maxsize=None)
def built_page(page_id: str) -> html.Div:
    """The pages are static, so each is built once per process and then only sent."""
    return PAGE_BUILDERS[page_id]()


def page_placeholder(page_id: str) -> html.Div:
    """The page container with its id, class and visibility, filled on the first visit."""
    page = built_page(page_id)
    return html.Div(id=page.id, className=page.className, style=page.style, children=[])


def build_rendered_pages_store() -> dcc.Store:
    """Pages already sent to this browser tab; a reload starts empty together with the layout."""
    return dcc.Store(id=ids.RENDERED_PAGES_STORE, data=[])


def built_page_children(page_id: str) -> List:
    return built_page(page_id).children


def render_visited_page(
    pathname: str,
    rendered_page_ids: Optional[List[str]],
    page_children: Callable[[str], List] = built_page_children,
) -> List:
    """Content of the visited page if it is lazy and not in the browser yet, and the updated list of sent pages.

    The app passes page_children that apply the reader's text edits (ui/editable_text.py).
    """
    page_id = PAGE_BY_PATH.get(pathname)
    rendered = list(rendered_page_ids or [])
    if page_id not in PAGE_BUILDERS or page_id in rendered:
        return [no_update] * (len(LAZY_PAGE_IDS) + 1)
    contents = [page_children(page_id) if lazy_id == page_id else no_update for lazy_id in LAZY_PAGE_IDS]
    return contents + [rendered + [page_id]]


def register_lazy_page_callbacks(app: Dash, page_children: Callable[[str], List] = built_page_children) -> None:
    app.callback(
        [Output(page_id, "children") for page_id in LAZY_PAGE_IDS] + [Output(ids.RENDERED_PAGES_STORE, "data")],
        Input(ids.URL, "pathname"),
        State(ids.RENDERED_PAGES_STORE, "data"),
    )(lambda pathname, rendered_page_ids: render_visited_page(pathname, rendered_page_ids, page_children))
