"""Page on PsiQuantum, a subpage of Photonics in the world: its path from Rudolph's blueprint to October 2026."""

from __future__ import annotations

from typing import List

from dash import dcc, html

from ui import ids
from ui.navigation import HIDDEN, PHOTONICS_LANDSCAPE_PATH, psiquantum_href
from ui.psiquantum_content import (
    FUNDING_ROUNDS,
    INTRO,
    KEY_FINDINGS,
    LECTURE_SLIDES,
    MONEY_TOPIC,
    PLAN_TOPIC,
    SOURCES_ANCHOR,
    TITLE,
    TOPICS,
)
from ui.theory_content import TheoryTopic
from ui.topic_sections import key_findings_card, sources_section, table_of_contents, topic_section
from ui.walther_lecture_content import SLIDES
from ui.walther_lecture_page import slide_figure


def build_psiquantum_page() -> html.Div:
    return html.Div(
        id=ids.PSIQUANTUM_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            _back_link(),
            html.H1(TITLE),
            html.P(INTRO, className="lead"),
            key_findings_card(KEY_FINDINGS, psiquantum_href),
            table_of_contents(TOPICS, psiquantum_href, SOURCES_ANCHOR),
            *[topic_section(number, topic, _illustrations(topic)) for number, topic in enumerate(TOPICS, start=1)],
            sources_section(TOPICS, SOURCES_ANCHOR),
            _back_link(),
        ],
    )


def funding_markdown() -> str:
    rows = ["| Kdy | Kolo | Částka | Investoři | Ocenění |", "|---|---|---|---|---|"]
    rows += [
        f"| {funding.date} | {funding.name} | {_millions(funding.amount_musd)} | {funding.investors} "
        f"| {funding.valuation} |"
        for funding in FUNDING_ROUNDS
    ]
    return "\n".join(rows)


def _millions(amount_musd: int) -> str:
    if amount_musd >= 1000:
        return f"{amount_musd / 1000:g}".replace(".", ",") + " mld. USD"
    return f"{amount_musd} mil. USD"


def _illustrations(topic: TheoryTopic) -> List:
    if topic.anchor == PLAN_TOPIC.anchor:
        slides = [slide for slide in SLIDES if slide.file_name in LECTURE_SLIDES]
        return [
            html.H3("Slajdy z Waltherovy přednášky"),
            html.Div(className="slide-gallery", children=[slide_figure(slide) for slide in slides]),
        ]
    if topic.anchor == MONEY_TOPIC.anchor:
        return [
            html.H4("Potvrzená soukromá kola"),
            html.Div(className="text-table", children=dcc.Markdown(funding_markdown())),
        ]
    return []


def _back_link() -> dcc.Link:
    return dcc.Link("← Zpět na Fotonika ve světě", href=PHOTONICS_LANDSCAPE_PATH, className="back-link")
