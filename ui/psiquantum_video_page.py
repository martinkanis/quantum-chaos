"""Page with notes from Ben Miles's video about PsiQuantum, a subpage of the PsiQuantum page."""

from __future__ import annotations

from typing import List

from dash import dcc, html

from ui import ids
from ui.navigation import HIDDEN, PSIQUANTUM_PATH, psiquantum_video_href
from ui.psiquantum_video_content import (
    HOW_MADE,
    INTRO,
    KEY_FINDINGS,
    LECTURE,
    SOURCES_ANCHOR,
    TITLE,
    TOPICS,
    VIDEO_URL,
    chapter_end,
    chapter_slides,
    chapter_start,
)
from ui.theory_content import TheoryTopic
from ui.topic_sections import key_findings_card, sources_section, table_of_contents, topic_section
from ui.walther_lecture_content import timestamp
from ui.walther_lecture_page import slide_figure, video_link
from web.lecture_slides import PRESENTATION_NAME, slide_url

DOWNLOAD_LABEL = "Stáhnout prezentaci (.pptx)"


def build_psiquantum_video_page() -> html.Div:
    return html.Div(
        id=ids.PSIQUANTUM_VIDEO_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            _back_link(),
            html.H1(TITLE),
            html.P(INTRO, className="lead"),
            html.P(HOW_MADE, className="hint small", style={"maxWidth": "80ch"}),
            html.P(html.A(
                DOWNLOAD_LABEL, href=slide_url(LECTURE, PRESENTATION_NAME), download="", className="primary-button",
            )),
            key_findings_card(KEY_FINDINGS, psiquantum_video_href),
            table_of_contents(TOPICS, psiquantum_video_href, SOURCES_ANCHOR),
            *[topic_section(number, topic, _frames(topic)) for number, topic in enumerate(TOPICS, start=1)],
            sources_section(TOPICS, SOURCES_ANCHOR),
            _back_link(),
        ],
    )


def _frames(topic: TheoryTopic) -> List:
    slides = chapter_slides(topic.anchor)
    if not slides:
        return []
    start, end = chapter_start(topic.anchor), chapter_end(topic.anchor)
    return [
        html.H3("Snímky a video"),
        html.P(className="hint", children=[
            "Tahle část je ve videu od ",
            video_link(start, VIDEO_URL),
            f" do {timestamp(end)}. Kliknutím na snímek se otevře v plné velikosti.",
        ]),
        html.Div(className="slide-gallery", children=[slide_figure(slide, LECTURE, VIDEO_URL) for slide in slides]),
    ]


def _back_link() -> dcc.Link:
    return dcc.Link("← Zpět na stránku PsiQuantum", href=PSIQUANTUM_PATH, className="back-link")
