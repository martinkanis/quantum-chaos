"""Notes from a recorded lecture, stored as a topic file with a lecture (content/topics, content/lectures).

The same look as the hand-written lecture pages (ui/walther_lecture_page.py): TL;DR, contents, chapters with a link
into the video and the frames of their part, sources. Frames and the presentation are served behind the login.
"""

from __future__ import annotations

from datetime import date
from typing import List, Sequence

from dash import dcc, html

from assistant.topics import Lecture, TopicPage, TopicSection, TopicSource, section_end
from ui.generated_topics import topic_path
from ui.reading_time import reading_minutes, reading_time_label
from ui.theory_content import KeyFinding
from ui.topic_sections import key_findings_card, toc_item
from ui.walther_lecture_content import LectureSlide, timestamp
from ui.walther_lecture_page import slide_figure, video_link
from web.lecture_slides import PRESENTATION_NAME, slide_url

DOWNLOAD_LABEL = "Stáhnout prezentaci (.pptx)"
SOURCES_TITLE = "Zdroje"


def lecture_notes_content(topic: TopicPage, with_anchors: bool) -> List:
    """Without anchors for a preview: the ids would clash once the published page is in the app too."""
    lecture = topic.lecture
    return [
        html.H1(topic.title),
        html.P(topic.description, className="lead"),
        html.P(_how_made(topic, lecture), className="hint small", style={"maxWidth": "80ch"}),
        html.P([
            html.A("Video přednášky", href=lecture.video_url, target="_blank", rel="noopener", className="primary-link"),
            *([" ", html.A(DOWNLOAD_LABEL, href=slide_url(lecture.folder, PRESENTATION_NAME), download="",
                           className="primary-button")] if lecture.has_presentation else []),
        ]),
        html.Div(className="in-short", children=[
            html.Strong("V kostce: "), dcc.Markdown(topic.in_short, mathjax=True),
        ]),
        *([key_findings_card(
            [KeyFinding(point.text, section_anchor(topic, point.section)) for point in lecture.key_points],
            lambda anchor: f"{topic_path(topic)}#{anchor}",
        )] if lecture.key_points else []),
        _contents(topic),
        *[
            _chapter(topic, number, section, with_anchors)
            for number, section in enumerate(topic.sections, start=1)
        ],
        _sources(topic.sources),
    ]


def section_anchor(topic: TopicPage, number: int) -> str:
    return f"{topic.slug}-{number}"


def _how_made(topic: TopicPage, lecture: Lecture) -> str:
    return (
        f"Přednáší {lecture.speaker} ({lecture.event}, {czech_date(lecture.recorded)}, "
        f"{_length(lecture.video_seconds)}, {lecture.language}). {lecture.how_made} Zápisky napsal "
        f"{topic.origin.model} {czech_date(topic.origin.created)}; tvrzení ověřuj podle zdrojů na konci stránky. "
        "Snímky i prezentace jsou jen pro přihlášené."
    )


def _contents(topic: TopicPage) -> html.Nav:
    minutes = [reading_minutes([section.body]) for section in topic.sections]
    path = topic_path(topic)
    return html.Nav(className="card toc", children=[
        html.H2("Obsah"),
        html.P(f"Celkem asi {reading_time_label(sum(minutes))}", className="hint small"),
        html.Ol([
            toc_item(section.heading, f"{path}#{section_anchor(topic, number)}", section_minutes)
            for number, (section, section_minutes) in enumerate(zip(topic.sections, minutes), start=1)
        ]),
    ])


def _chapter(topic: TopicPage, number: int, section: TopicSection, with_anchors: bool) -> html.Section:
    return html.Section(
        className="card step theory-section",
        children=[
            html.H2([html.Span(str(number), className="step-number"), section.heading]),
            *_video_part(topic, number, section),
            dcc.Markdown(section.body, mathjax=True, link_target="_blank"),
            *_frames(topic.lecture, section),
        ],
        **({"id": section_anchor(topic, number)} if with_anchors else {}),
    )


def _video_part(topic: TopicPage, number: int, section: TopicSection) -> List:
    if section.start is None:
        return [html.P("Naše kapitola, ve videu nezazní.", className="hint")]
    return [html.P(className="hint", children=[
        "Ve videu od ", video_link(section.start, topic.lecture.video_url),
        f" do {timestamp(section_end(topic, number))}.",
    ])]


def _frames(lecture: Lecture, section: TopicSection) -> List:
    if not section.slides:
        return []
    return [html.Details(open=True, className="lecture-slides", children=[
        html.Summary(f"Snímky z této části ({len(section.slides)}), kliknutím se zvětší"),
        html.Div(className="slide-gallery", children=[
            slide_figure(LectureSlide(slide.file_name, slide.caption), lecture.folder, lecture.video_url)
            for slide in section.slides
        ]),
    ])]


def _sources(sources: Sequence[TopicSource]) -> html.Section:
    return html.Section(className="card theory-section", children=[
        html.H2(SOURCES_TITLE),
        html.Ol([source_item(source) for source in sources]),
    ])


def source_item(source: TopicSource) -> html.Li:
    return html.Li([
        html.A(source.title, href=source.url, target="_blank", rel="noopener noreferrer"),
        *([f" – {source.note}"] if source.note else []),
    ])


def _length(seconds: int) -> str:
    return f"{round(seconds / 60)} min"


def czech_date(iso_date: str) -> str:
    """„8. 11. 2026“; a date that is not ISO stays as it is."""
    try:
        day = date.fromisoformat(iso_date)
    except ValueError:
        return iso_date
    return f"{day.day}. {day.month}. {day.year}"
