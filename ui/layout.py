from __future__ import annotations

from dash import dcc, html

from ui import ids
from ui.academy_page import build_academy_page
from ui.advantage_page import build_advantage_page
from ui.breadcrumbs import build_breadcrumb
from ui.caveats_page import build_caveats_page
from ui.gbs_page import build_gbs_page
from ui.guide_page import build_guide_page
from ui.literature_review_page import build_literature_review_page
from ui.navigation import build_navigation
from ui.portfolio_page import build_portfolio_page
from ui.random_matrix_page import build_random_matrix_page
from ui.research_directions_page import build_research_directions_page
from ui.study_progress import build_progress_store, build_study_pager
from ui.theory_page import build_theory_page
from ui.topics_page import build_topics_page
from ui.vqe_paper_page import build_vqe_paper_page


def build_layout() -> html.Div:
    return html.Div(
        children=[
            dcc.Location(id=ids.URL),
            build_progress_store(),
            build_navigation(),
            build_breadcrumb(),
            build_topics_page(),
            build_academy_page(),
            build_portfolio_page(),
            build_gbs_page(),
            build_caveats_page(),
            build_theory_page(),
            build_advantage_page(),
            build_guide_page(),
            build_vqe_paper_page(),
            build_literature_review_page(),
            build_random_matrix_page(),
            build_research_directions_page(),
            build_study_pager(),
        ]
    )
