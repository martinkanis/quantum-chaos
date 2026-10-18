from __future__ import annotations

from typing import List

from dash import dcc, html

from ui import ids
from ui.navigation import HIDDEN, RANDOM_MATRIX_PATH, random_matrix_gbs_href
from ui.random_matrix_gbs_content import (
    FIRST_STUDY,
    IN_SHORT,
    LEAD,
    SAVINGS_TABLE_HINT,
    SOURCES_ANCHOR,
    TOPICS,
    savings_table,
    study_findings,
)
from ui.theory_content import TheoryTopic
from ui.topic_sections import sources_section, table_of_contents, topic_section


def build_random_matrix_gbs_page() -> html.Div:
    return html.Div(
        id=ids.RANDOM_MATRIX_GBS_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            html.H1("Náhodné matice a GBS: hypotéza a první výpočet"),
            html.P(LEAD, className="lead"),
            dcc.Link("Základy v tématu Náhodné matice →", href=RANDOM_MATRIX_PATH, className="back-link"),
            html.Div(className="in-short", children=[html.Strong("V kostce: "), dcc.Markdown(IN_SHORT)]),
            table_of_contents(TOPICS, random_matrix_gbs_href, SOURCES_ANCHOR),
            *[topic_section(number, topic, _illustrations(topic)) for number, topic in enumerate(TOPICS, start=1)],
            sources_section(TOPICS, SOURCES_ANCHOR),
        ],
    )


def _illustrations(topic: TheoryTopic) -> List[html.Div]:
    if topic != FIRST_STUDY:
        return []
    return [html.Div([
        html.H4("Úspora vzorků GBS proti Monte Carlu, šest aktiv a dvě portfolia"),
        dcc.Markdown(savings_table()),
        html.P(SAVINGS_TABLE_HINT, className="hint small"),
        dcc.Markdown(study_findings(), mathjax=True),
    ])]
