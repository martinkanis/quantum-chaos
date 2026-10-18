from __future__ import annotations

from typing import Dict, List

from dash import dcc, html

from randommatrix.factor_market import DEFAULT_SECTOR_COUNT
from ui import ids
from ui.components import REFERENCE_SEED, details_link, labelled, seed_dropdown
from ui.failure_diagnostics_content import DIAGNOSTIC_TOOLS
from ui.navigation import HIDDEN, failure_diagnostics_href, random_matrix_href
from ui.random_matrix_content import (
    DETERMINISTIC_CHAOS,
    IN_SHORT,
    LAB_ANCHOR,
    LAB_INTRO,
    LEAD,
    SOURCES_ANCHOR,
    TOPICS,
)
from ui.theory_content import TheoryTopic
from ui.topic_sections import sources_section, table_of_contents, topic_section

ASSET_COUNT_OPTIONS = (50, 100, 200, 400)
DEFAULT_ASSET_COUNT = 200
OBSERVATION_COUNT_LABELS: Dict[int, str] = {
    250: "250 (asi 1 rok denních dat)",
    500: "500 (asi 2 roky)",
    1000: "1 000 (asi 4 roky)",
    2500: "2 500 (asi 10 let)",
    4000: "4 000 (asi 16 let)",
}
DEFAULT_OBSERVATION_COUNT = 500


def build_random_matrix_page() -> html.Div:
    return html.Div(
        id=ids.RANDOM_MATRIX_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            html.H1("Náhodné matice a riziko portfolia"),
            html.P(LEAD, className="lead"),
            html.Div(className="in-short", children=[html.Strong("V kostce: "), dcc.Markdown(IN_SHORT, mathjax=True)]),
            table_of_contents(TOPICS, random_matrix_href, SOURCES_ANCHOR),
            _lab_section(),
            html.Div(id=ids.RANDOM_MATRIX_ERROR_MESSAGE, className="error-message"),
            dcc.Loading(html.Div(id=ids.RANDOM_MATRIX_RESULTS), type="circle"),
            *[topic_section(number, topic, _illustrations(topic)) for number, topic in enumerate(TOPICS, start=1)],
            sources_section(TOPICS, SOURCES_ANCHOR),
        ],
    )


def _lab_section() -> html.Section:
    return html.Section(
        id=LAB_ANCHOR,
        className="card",
        children=[
            html.H2("Laboratoř: kolik šumu je v korelační matici"),
            dcc.Markdown(LAB_INTRO.format(sector_count=DEFAULT_SECTOR_COUNT), mathjax=True),
            html.Div(
                className="control-grid",
                children=[
                    labelled("Počet akcií N", dcc.Dropdown(
                        id=ids.RANDOM_MATRIX_ASSET_COUNT_DROPDOWN,
                        options=[{"label": str(count), "value": count} for count in ASSET_COUNT_OPTIONS],
                        value=DEFAULT_ASSET_COUNT, clearable=False, searchable=False,
                    )),
                    labelled("Délka historie T (počet dní)", dcc.Dropdown(
                        id=ids.RANDOM_MATRIX_OBSERVATION_COUNT_DROPDOWN,
                        options=[{"label": label, "value": count} for count, label in OBSERVATION_COUNT_LABELS.items()],
                        value=DEFAULT_OBSERVATION_COUNT, clearable=False, searchable=False,
                    )),
                    seed_dropdown(ids.RANDOM_MATRIX_SEED_DROPDOWN, default_value=REFERENCE_SEED),
                ],
            ),
            html.Button("Nasimulovat trh", id=ids.RANDOM_MATRIX_RUN_BUTTON, className="primary-button"),
        ],
    )


def _illustrations(topic: TheoryTopic) -> List[dcc.Link]:
    if topic != DETERMINISTIC_CHAOS:
        return []
    return [details_link(
        "nástroje teorie chaosu jako diagnostika selhání odhadu rizika", failure_diagnostics_href(DIAGNOSTIC_TOOLS.anchor),
    )]
