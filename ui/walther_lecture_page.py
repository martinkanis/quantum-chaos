"""Page with notes from Philip Walther's lecture: chapters of the talk, each with its slides and a link into the video."""

from __future__ import annotations

from typing import List

from dash import dcc, html

from ui import ids
from ui.navigation import HIDDEN, PHOTONICS_TOPIC_HREF, walther_lecture_href
from ui.theory_content import TheoryTopic
from ui.topic_sections import key_findings_card, sources_section, table_of_contents, topic_section
from ui.walther_lecture_content import (
    HOW_MADE,
    INTRO,
    KEY_FINDINGS,
    LECTURE,
    SOURCES_ANCHOR,
    TITLE,
    TOPICS,
    LectureSlide,
    chapter_end,
    chapter_slides,
    chapter_start,
    timestamp,
    video_at,
)
from web.lecture_slides import slide_url


def build_walther_lecture_page() -> html.Div:
    return html.Div(
        id=ids.WALTHER_LECTURE_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            _back_link(),
            html.H1(TITLE),
            html.P(INTRO, className="lead"),
            html.P(HOW_MADE, className="hint small", style={"maxWidth": "80ch"}),
            key_findings_card(KEY_FINDINGS, walther_lecture_href),
            table_of_contents(TOPICS, walther_lecture_href, SOURCES_ANCHOR),
            *[topic_section(number, topic, _chapter_slides(topic)) for number, topic in enumerate(TOPICS, start=1)],
            sources_section(TOPICS, SOURCES_ANCHOR),
            _back_link(),
        ],
    )


def _chapter_slides(topic: TheoryTopic) -> List:
    start, end = chapter_start(topic.anchor), chapter_end(topic.anchor)
    slides = chapter_slides(topic.anchor)
    return [
        html.H3("Slajdy a video"),
        html.P(className="hint", children=[
            "Tahle část je ve videu od ",
            _video_link(start),
            f" do {timestamp(end)}. Kliknutím na slajd se otevře v plné velikosti.",
        ]),
        html.Details(open=True, className="lecture-slides", children=[
            html.Summary(f"Slajdy z této části ({len(slides)})"),
            html.Div(className="slide-gallery", children=[_slide(slide) for slide in slides]),
        ]),
    ]


def _slide(slide: LectureSlide) -> html.Figure:
    url = slide_url(LECTURE, slide.file_name)
    return html.Figure(className="lecture-slide", children=[
        html.A(html.Img(src=url, alt=slide.caption), href=url, target="_blank", rel="noopener"),
        html.Figcaption([slide.caption, " · ", _video_link(slide.seconds)]),
    ])


def _video_link(seconds: int) -> html.A:
    return html.A(timestamp(seconds), href=video_at(seconds), target="_blank", rel="noopener")


def _back_link() -> dcc.Link:
    return dcc.Link("← Zpět na téma Fotonika", href=PHOTONICS_TOPIC_HREF, className="back-link")
