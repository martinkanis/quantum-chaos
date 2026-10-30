"""Page on three-photon GHZ states, a subpage of Walther's lecture notes."""

from __future__ import annotations

from typing import List

from dash import dcc, html

from ui import ids
from ui.ghz_states_content import BLUEPRINT_SLIDES, INTRO, KEY_FINDINGS, SOURCES_ANCHOR, TITLE, TOPICS, WHY_THREE_TOPIC
from ui.navigation import HIDDEN, WALTHER_LECTURE_PATH, ghz_states_href
from ui.theory_content import TheoryTopic
from ui.topic_sections import key_findings_card, sources_section, table_of_contents, topic_section
from ui.walther_lecture_content import SLIDES
from ui.walther_lecture_page import slide_figure


def build_ghz_states_page() -> html.Div:
    return html.Div(
        id=ids.GHZ_STATES_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            _back_link(),
            html.H1(TITLE),
            html.P(INTRO, className="lead"),
            key_findings_card(KEY_FINDINGS, ghz_states_href),
            table_of_contents(TOPICS, ghz_states_href, SOURCES_ANCHOR),
            *[topic_section(number, topic, _illustrations(topic)) for number, topic in enumerate(TOPICS, start=1)],
            sources_section(TOPICS, SOURCES_ANCHOR),
            _back_link(),
        ],
    )


def _illustrations(topic: TheoryTopic) -> List:
    if topic.anchor != WHY_THREE_TOPIC.anchor:
        return []
    slides = [slide for slide in SLIDES if slide.file_name in BLUEPRINT_SLIDES]
    return [
        html.H3("Slajdy z Waltherovy přednášky"),
        html.Div(className="slide-gallery", children=[slide_figure(slide) for slide in slides]),
    ]


def _back_link() -> dcc.Link:
    return dcc.Link("← Zpět na přednášku Philipa Walthera", href=WALTHER_LECTURE_PATH, className="back-link")
