from __future__ import annotations

from typing import Collection, List

from dash import dcc, html

from ui import ids
from ui.knowledge_map_page import details_card, layer_overview, map_card, map_stores, notes_cards
from ui.navigation import ACADEMY_PATH
from ui.topic_catalog import (
    RESEARCH_TOPICS,
    TOPICS_TITLE,
    PageEntry,
    ResearchTopic,
    next_unstudied_page,
    section_title,
    study_path,
)

PERCENT = 100
STUDIED_MARK = "✓"

STUDY_PATHS_LEAD = (
    "Studijní cesty procházejí stránky v pořadí, ve kterém se dobře čtou. Dole na každé stránce ji můžeš označit jako "
    "prostudovanou a pokračovat dalším krokem; postup se ukládá jen v tomto prohlížeči."
)


def build_topics_page() -> html.Div:
    """Home page: the knowledge map across the whole width, then the study paths and the user's own notes."""
    return html.Div(
        id=ids.TOPICS_PAGE,
        className="home-page",
        children=[
            html.Div(className="home-intro", children=html.H1(TOPICS_TITLE)),
            map_card(),
            html.Div(className="gbs-page home-content", children=[
                details_card(),
                html.H2("Studijní cesty", className="topics-heading"),
                html.P(STUDY_PATHS_LEAD, className="hint"),
                html.Div(id=ids.TOPICS_LIST, children=topic_cards(studied_page_ids=())),
                _groups_card(),
                *notes_cards(),
                html.P(
                    className="hint",
                    children=[
                        "Odkazy na kurzy, blogy a další materiály ke kvantovému počítání jsou na stránce ",
                        dcc.Link("Quantum Academy", href=ACADEMY_PATH),
                        ".",
                    ],
                ),
            ]),
            *map_stores(),
        ],
    )


def _groups_card() -> html.Section:
    return html.Section(className="card structure-card", children=[
        html.H2("Skupiny stránek"),
        html.P(
            "Stejných pět skupin jako v horním menu a v mapě: finance, fotonika, jejich průnik GBS ve financích, "
            "vlastní výzkum a základy.",
            className="hint",
        ),
        layer_overview(),
    ])


def topic_cards(studied_page_ids: Collection[str]) -> List[html.Section]:
    return [_topic_card(topic, studied_page_ids) for topic in RESEARCH_TOPICS]


def progress_label(studied_count: int, page_count: int) -> str:
    return f"Prostudováno {studied_count} / {page_count}"


def _topic_card(topic: ResearchTopic, studied_page_ids: Collection[str]) -> html.Section:
    path = study_path(topic)
    studied_count = sum(page.page_id in studied_page_ids for page in path)
    return html.Section(
        id=topic.anchor,
        className="card topic-card theory-section",
        children=[
            html.H2(topic.title),
            html.P(topic.summary),
            _progress_bar(studied_count, len(path)),
            _continue_link(topic, studied_page_ids),
            html.H3("Doporučené pořadí studia"),
            html.Ol(
                className="study-path",
                children=[_page_item(topic, page, studied_page_ids) for page in path],
            ),
        ],
    )


def _progress_bar(studied_count: int, page_count: int) -> html.Div:
    return html.Div(
        className="topic-progress",
        children=[
            html.Div(
                className="progress-track",
                children=html.Div(
                    className="progress-fill", style={"width": f"{studied_count / page_count * PERCENT:.0f}%"},
                ),
            ),
            html.Span(progress_label(studied_count, page_count), className="hint small"),
        ],
    )


def _continue_link(topic: ResearchTopic, studied_page_ids: Collection[str]) -> html.P:
    next_page = next_unstudied_page(topic, studied_page_ids)
    if next_page is None:
        return html.P("Celé téma máš prostudované.", className="topic-continue done")
    has_started = any(page.page_id in studied_page_ids for page in study_path(topic))
    label = "Pokračuj" if has_started else "Začni tady"
    return html.P(
        className="topic-continue",
        children=dcc.Link(f"{label}: {next_page.title} →", href=next_page.path, className="primary-link"),
    )


def _page_item(topic: ResearchTopic, page: PageEntry, studied_page_ids: Collection[str]) -> html.Li:
    is_studied = page.page_id in studied_page_ids
    class_names = ["study-path-item"]
    if is_studied:
        class_names.append("studied")
    if page.parent_page_id:
        class_names.append("subpage")
    return html.Li(
        className=" ".join(class_names),
        children=[
            html.Span(STUDIED_MARK if is_studied else "", className="study-mark"),
            html.Div([
                dcc.Link(page.title, href=page.path, className="topic-page-link"),
                html.Span(section_title(topic, page.page_id), className="section-tag"),
                html.Br(),
                page.description,
            ]),
        ],
    )
