"""Layout of a topic page written by the assistant; the same content shows as a preview before it is accepted."""

from __future__ import annotations

from typing import List

from dash import dcc, html

from assistant.topics import TopicPage
from ui.generated_topics import generated_page_id
from ui.lecture_notes_page import czech_date, lecture_notes_content, source_item
from ui.navigation import HIDDEN
from ui.topic_catalog import page_entries

SELECTION_EXCERPT_LENGTH = 160


def build_generated_page(topic: TopicPage) -> html.Div:
    return html.Div(
        id=generated_page_id(topic.slug),
        className="gbs-page",
        style=HIDDEN,
        children=generated_page_content(topic, with_anchors=True),
    )


def generated_page_content(topic: TopicPage, with_anchors: bool) -> List:
    """Without anchors for the preview: the ids would clash once the accepted page is in the app too."""
    entries = page_entries()
    parent = entries.get(topic.placement.parent_page_id or "")
    back_link = [dcc.Link(f"← Zpět na {parent.title}", href=parent.path, className="back-link")] if parent else []
    if topic.lecture:
        return back_link + lecture_notes_content(topic, with_anchors)
    origin = entries.get(topic.origin.page_id)
    return [
        *back_link,
        html.H1(topic.title),
        html.P(topic.description, className="lead"),
        html.P(className="hint generated-note", children=[
            f"Rozvedl asistent Claude {czech_date(topic.origin.created)} z úryvku „{_excerpt(topic.origin.selection)}“"
            f" na stránce „{origin.title if origin else topic.origin.page_id}“. "
            "Text píše jazykový model: tvrzení ověřuj podle zdrojů na konci stránky.",
        ]),
        html.Div(className="in-short", children=[
            html.Strong("V kostce: "), dcc.Markdown(topic.in_short, mathjax=True),
        ]),
        *[
            html.Section(
                className="card step theory-section",
                children=[
                    html.H2([html.Span(str(number), className="step-number"), section.heading]),
                    dcc.Markdown(section.body, mathjax=True, link_target="_blank"),
                ],
                **({"id": f"{topic.slug}-{number}"} if with_anchors else {}),
            )
            for number, section in enumerate(topic.sections, start=1)
        ],
        html.Section(className="card theory-section", children=[
            html.H2("Zdroje"),
            html.Ol([source_item(source) for source in topic.sources]) if topic.sources
            else html.P("Agent neuvedl žádný zdroj s odkazem; text ber jako vlastní vysvětlení modelu.", className="hint"),
        ]),
    ]


def _excerpt(text: str) -> str:
    if len(text) <= SELECTION_EXCERPT_LENGTH:
        return text
    return text[:SELECTION_EXCERPT_LENGTH].rsplit(" ", 1)[0] + "…"
