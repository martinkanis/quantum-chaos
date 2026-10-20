"""Integrals cheat sheet: short rules with examples, linked to the pages where the app uses them."""

from __future__ import annotations

from typing import Dict, Tuple

from dash import html

from ui import ids
from ui.integrals_cheat_sheet_content import (
    BY_PARTS_TOPIC,
    GAUSSIAN_TOPIC,
    IMPROPER_TOPIC,
    INTRO,
    MONTE_CARLO_TOPIC,
    MULTIPLE_TOPIC,
    SOURCES_ANCHOR,
    TITLE,
    TOPICS,
)
from ui.navigation import (
    HIDDEN,
    PORTFOLIO_PATH,
    andersen_shan_paper_href,
    guide_href,
    integrals_cheat_sheet_href,
    theory_href,
)
from ui.topic_sections import RelatedLink, related_pages, sources_section, table_of_contents, topic_section

RELATED_PAGES: Dict[str, Tuple[RelatedLink, ...]] = {
    BY_PARTS_TOPIC.anchor: (
        ("Steinovo lemma a výpočet momentů (Průvodce)", guide_href("pruvodce-gaussovska-uloha")),
    ),
    IMPROPER_TOPIC.anchor: (("Podmínka (A1) v článku Andersena a Shan", andersen_shan_paper_href("clanek-podminka-a1")),),
    MULTIPLE_TOPIC.anchor: (("Hustota h(x) v článku Andersena a Shan", andersen_shan_paper_href("clanek-hustota")),),
    GAUSSIAN_TOPIC.anchor: (
        ("Wickova–Isserlisova věta a hafnián (Teorie)", theory_href("wickova-veta")),
        ("Rovnice (1) a (2) v článku Andersena a Shan", andersen_shan_paper_href("clanek-rovnice-1")),
    ),
    MONTE_CARLO_TOPIC.anchor: (
        ("Klasické Monte Carlo (Teorie)", theory_href("monte-carlo")),
        ("1 · Klasické Monte Carlo portfolia", PORTFOLIO_PATH),
    ),
}


def build_integrals_cheat_sheet_page() -> html.Div:
    return html.Div(
        id=ids.INTEGRALS_CHEAT_SHEET_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            html.H1(TITLE),
            html.P(INTRO, className="lead"),
            table_of_contents(TOPICS, integrals_cheat_sheet_href, SOURCES_ANCHOR),
            *[
                topic_section(number, topic, related_pages(RELATED_PAGES.get(topic.anchor, ())))
                for number, topic in enumerate(TOPICS, start=1)
            ],
            sources_section(TOPICS, SOURCES_ANCHOR),
        ],
    )
