from __future__ import annotations

from dash import dcc, html

from ui import ids
from ui.navigation import ACADEMY_PATH
from ui.topic_catalog import RESEARCH_TOPICS, TOPICS_TITLE, PageEntry, ResearchTopic, TopicSection

LEAD = (
    "Přehled témat aplikace. Každé téma má vlastní stránky s interaktivními výpočty a podrobným výkladem psaným "
    "pro začínající doktorandy. Další témata budou přibývat sem."
)


def build_topics_page() -> html.Div:
    return html.Div(
        id=ids.TOPICS_PAGE,
        className="gbs-page",
        children=[
            html.H1(TOPICS_TITLE),
            html.P(LEAD, className="lead"),
            *[_topic_card(topic) for topic in RESEARCH_TOPICS],
            html.P(
                className="hint",
                children=[
                    "Odkazy na kurzy, blogy a další materiály ke kvantovému počítání jsou na stránce ",
                    dcc.Link("Quantum Academy", href=ACADEMY_PATH),
                    ".",
                ],
            ),
        ],
    )


def _topic_card(topic: ResearchTopic) -> html.Section:
    return html.Section(
        id=topic.anchor,
        className="card topic-card theory-section",
        children=[html.H2(topic.title), html.P(topic.summary), *[_section(section) for section in topic.sections]],
    )


def _section(section: TopicSection) -> html.Div:
    return html.Div(
        className="topic-section",
        children=[html.H3(section.title), html.Ul([_page_item(page) for page in section.pages])],
    )


def _page_item(page: PageEntry) -> html.Li:
    return html.Li([dcc.Link(page.title, href=page.path, className="topic-page-link"), html.Br(), page.description])
