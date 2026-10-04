"""Explanatory topics rendered as numbered sections with further reading; shared by the theory page and the guide."""

from __future__ import annotations

from typing import Callable, List, Sequence

from dash import dcc, html

from ui.navigation import caveat_href
from ui.theory_content import Reading, Source, TheoryTopic, all_sources


def table_of_contents(topics: Sequence[TheoryTopic], href: Callable[[str], str], sources_anchor: str) -> html.Nav:
    return html.Nav(
        className="card toc",
        children=[
            html.H2("Obsah"),
            html.Ol([html.Li(dcc.Link(topic.title, href=href(topic.anchor))) for topic in topics]),
            dcc.Link("Všechny zdroje – česky i původní články →", href=href(sources_anchor), className="back-link"),
        ],
    )


def topic_section(number: int, topic: TheoryTopic, illustrations: Sequence[html.Div] = ()) -> html.Section:
    return html.Section(
        id=topic.anchor,
        className="card step theory-section",
        children=[
            html.H2([html.Span(str(number), className="step-number"), topic.title]),
            html.Div(className="in-short", children=[
                html.Strong("V kostce: "), dcc.Markdown(topic.in_short, mathjax=True),
            ]),
            dcc.Markdown(topic.explanation, mathjax=True),
            *illustrations,
            *_related_caveats(topic),
            html.H3("Kde číst dál"),
            markdown_list([_reading_item(reading) for reading in topic.further_reading]),
        ],
    )


def sources_section(topics: Sequence[TheoryTopic], anchor: str) -> html.Section:
    sources = all_sources(topics)
    return html.Section(
        id=anchor,
        className="card step theory-section",
        children=[
            html.H2("Všechny zdroje"),
            html.P("Každý zdroj, na který se stránka odkazuje, na jednom místě.", className="hint"),
            html.H3("V češtině"),
            markdown_list(source_items([source for source in sources if source.czech])),
            html.H3("Původní články a další literatura"),
            markdown_list(source_items([source for source in sources if not source.czech])),
        ],
    )


def source_items(sources: Sequence[Source]) -> List[str]:
    return [f"- {source.citation}." for source in sources]


def markdown_list(items: Sequence[str]) -> dcc.Markdown:
    return dcc.Markdown("\n".join(items), mathjax=True, link_target="_blank")


def _reading_item(reading: Reading) -> str:
    note = f" – {reading.note}" if reading.note else ""
    return f"- {reading.source.citation}{note}."


def _related_caveats(topic: TheoryTopic) -> List:
    if not topic.related_caveats:
        return []
    links: List = []
    for caveat in topic.related_caveats:
        if links:
            links.append(", ")
        links.append(dcc.Link(caveat.title, href=caveat_href(caveat.anchor)))
    return [html.P(className="hint", children=["Související háčky: ", *links])]
