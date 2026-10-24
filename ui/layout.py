from __future__ import annotations

from dash import dcc, html

from ui import ids
from ui.advantage_page import build_advantage_page
from ui.breadcrumbs import build_breadcrumb
from ui.gbs_page import build_gbs_page
from ui.lazy_pages import build_rendered_pages_store, page_placeholder
from ui.main_menu import build_main_menu
from ui.portfolio_page import build_portfolio_page
from ui.random_matrix_page import build_random_matrix_page
from ui.study_progress import build_progress_store, build_study_pager
from ui.topics_page import build_topics_page


def build_layout() -> html.Div:
    return html.Div(
        children=[
            dcc.Location(id=ids.URL, refresh="callback-nav"),
            build_progress_store(),
            build_rendered_pages_store(),
            build_main_menu(),
            build_breadcrumb(),
            build_topics_page(),
            page_placeholder(ids.ACADEMY_PAGE),
            build_portfolio_page(),
            build_gbs_page(),
            page_placeholder(ids.CAVEATS_PAGE),
            page_placeholder(ids.THEORY_PAGE),
            page_placeholder(ids.HAFNIAN_PAGE),
            build_advantage_page(),
            page_placeholder(ids.GUIDE_PAGE),
            page_placeholder(ids.QPURPOSE_PAGE),
            page_placeholder(ids.ANDERSEN_SHAN_PAPER_PAGE),
            page_placeholder(ids.VQE_PAPER_PAGE),
            page_placeholder(ids.LITERATURE_REVIEW_PAGE),
            page_placeholder(ids.PHOTONIC_HARDWARE_PAGE),
            page_placeholder(ids.PHOTONICS_LANDSCAPE_PAGE),
            build_random_matrix_page(),
            page_placeholder(ids.FAILURE_DIAGNOSTICS_PAGE),
            page_placeholder(ids.RANDOM_MATRIX_GBS_PAGE),
            page_placeholder(ids.INTEGRALS_CHEAT_SHEET_PAGE),
            build_study_pager(),
        ]
    )
