from __future__ import annotations

from typing import Dict, List, Tuple

from dash import dcc, html

from ui import ids
from ui.components import details_link
from ui.failure_diagnostics_content import (
    ESTIMATOR_SOURCE,
    IN_SHORT,
    INPUT_SOURCE,
    LEAD,
    SOURCES_ANCHOR,
    TOPICS,
    failure_sources_table,
)
from ui.navigation import HIDDEN, failure_diagnostics_href, random_matrix_gbs_href, random_matrix_href
from ui.random_matrix_content import LAB_ANCHOR
from ui.random_matrix_gbs_content import FIRST_STUDY
from ui.theory_content import TheoryTopic
from ui.topic_sections import sources_section, table_of_contents, topic_section

DETAIL_LINKS: Dict[str, Tuple[str, str]] = {
    ESTIMATOR_SOURCE.anchor: ("první výpočet na stránce Náhodné matice a GBS", random_matrix_gbs_href(FIRST_STUDY.anchor)),
    INPUT_SOURCE.anchor: ("laboratoř na stránce Náhodné matice a riziko portfolia", random_matrix_href(LAB_ANCHOR)),
}


def build_failure_diagnostics_page() -> html.Div:
    return html.Div(
        id=ids.FAILURE_DIAGNOSTICS_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            html.H1("Kdy odhad rizika přes GBS selže: tři zdroje chyby"),
            html.P(LEAD, className="lead"),
            html.Div(className="in-short", children=[html.Strong("V kostce: "), dcc.Markdown(IN_SHORT)]),
            html.Section(
                className="card",
                children=[html.H2("Tři zdroje chyby na jednom místě"), dcc.Markdown(failure_sources_table())],
            ),
            table_of_contents(TOPICS, failure_diagnostics_href, SOURCES_ANCHOR),
            *[topic_section(number, topic, _illustrations(topic)) for number, topic in enumerate(TOPICS, start=1)],
            sources_section(TOPICS, SOURCES_ANCHOR),
        ],
    )


def _illustrations(topic: TheoryTopic) -> List[dcc.Link]:
    link = DETAIL_LINKS.get(topic.anchor)
    return [details_link(*link)] if link else []
