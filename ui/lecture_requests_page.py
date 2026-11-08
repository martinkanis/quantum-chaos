"""Page where the reader queues a recorded lecture for notes and follows the queue.

It has a form, so it stays in the layout (hidden) like the other form pages.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Sequence

from dash import dcc, html

from assistant.lecture_requests import NEW_TOPIC, LectureRequest, RequestStatus
from ui import ids
from ui.lecture_requests_content import (
    DEFAULT_DETAIL,
    DEFAULT_PRESENTATION,
    DETAIL_LABEL,
    DETAIL_LABELS,
    DETAIL_OPTIONS,
    EMPTY_QUEUE,
    HOW_IT_WORKS,
    LEAD,
    NEW_TOPIC_LABEL,
    NEW_TOPIC_OPTION,
    NOTE_LABEL,
    NOTE_PLACEHOLDER,
    OPEN_NOTES,
    PRESENTATION_LABEL,
    PRESENTATION_LABELS,
    PRESENTATION_OPTIONS,
    QUEUE_TITLE,
    REFRESH_LABEL,
    STATUS_LABELS,
    SUBMIT_LABEL,
    TITLE,
    TOPIC_LABEL,
    URL_LABEL,
    URL_PLACEHOLDER,
)
from ui.navigation import HIDDEN, PHOTONICS_TOPIC_ANCHOR
from ui.topic_catalog import RESEARCH_TOPICS

STATUS_CLASSES: Dict[RequestStatus, str] = {
    RequestStatus.WAITING: "request-status waiting",
    RequestStatus.PROCESSING: "request-status processing",
    RequestStatus.DONE: "request-status done",
    RequestStatus.FAILED: "request-status failed",
}


def build_lecture_requests_page() -> html.Div:
    return html.Div(
        id=ids.LECTURE_REQUESTS_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            html.H1(TITLE),
            html.P(LEAD, className="lead"),
            html.Ul([html.Li(point) for point in HOW_IT_WORKS], className="hint"),
            _form(),
            html.Section(className="card", children=[
                html.H2(QUEUE_TITLE),
                html.Button(REFRESH_LABEL, id=ids.LECTURE_REQUEST_REFRESH, className="secondary-button"),
                html.Div(id=ids.LECTURE_REQUEST_LIST, children=html.P(EMPTY_QUEUE, className="hint")),
            ]),
        ],
    )


def topic_names() -> Dict[str, str]:
    return {topic.anchor: topic.title for topic in RESEARCH_TOPICS}


def request_list(requests: Sequence[LectureRequest]) -> List:
    if not requests:
        return [html.P(EMPTY_QUEUE, className="hint")]
    names = topic_names()
    return [html.Ul(className="request-list", children=[_request_item(request, names) for request in requests])]


def _form() -> html.Section:
    return html.Section(className="card", children=[
        _field(URL_LABEL, dcc.Input(id=ids.LECTURE_REQUEST_URL, type="url", placeholder=URL_PLACEHOLDER)),
        _field(TOPIC_LABEL, dcc.Dropdown(
            id=ids.LECTURE_REQUEST_TOPIC,
            options=[{"label": title, "value": anchor} for anchor, title in topic_names().items()]
            + [{"label": NEW_TOPIC_OPTION, "value": NEW_TOPIC}],
            value=PHOTONICS_TOPIC_ANCHOR,
            clearable=False,
        )),
        _field(NEW_TOPIC_LABEL, dcc.Input(id=ids.LECTURE_REQUEST_NEW_TOPIC, type="text")),
        _field(DETAIL_LABEL, dcc.RadioItems(
            id=ids.LECTURE_REQUEST_DETAIL,
            options=[{"label": label, "value": level.value} for level, label in DETAIL_OPTIONS],
            value=DEFAULT_DETAIL.value,
            className="radio-list",
        )),
        _field(PRESENTATION_LABEL, dcc.RadioItems(
            id=ids.LECTURE_REQUEST_PRESENTATION,
            options=[{"label": label, "value": style.value} for style, label in PRESENTATION_OPTIONS],
            value=DEFAULT_PRESENTATION.value,
            className="radio-list",
        )),
        _field(NOTE_LABEL, dcc.Textarea(id=ids.LECTURE_REQUEST_NOTE, placeholder=NOTE_PLACEHOLDER)),
        html.Button(SUBMIT_LABEL, id=ids.LECTURE_REQUEST_SUBMIT, className="primary-button"),
        html.Div(id=ids.LECTURE_REQUEST_MESSAGE, role="status"),
    ])


def _field(label: str, control) -> html.Div:
    return html.Div(className="field", children=[html.Label(label), control])


def _request_item(request: LectureRequest, names: Dict[str, str]) -> html.Li:
    topic = request.new_topic_title or names.get(request.topic_anchor, request.topic_anchor)
    return html.Li(className="request-item", children=[
        html.Span(STATUS_LABELS[request.status], className=STATUS_CLASSES[request.status]),
        " ",
        html.A(request.url, href=request.url, target="_blank", rel="noopener noreferrer"),
        html.Div(
            f"{topic} · {DETAIL_LABELS[request.detail]} · {PRESENTATION_LABELS[request.presentation]} · "
            f"zadáno {_czech_date(request.created_at)}",
            className="hint small",
        ),
        *([html.Div(request.message, className="hint small")] if request.message else []),
        *([dcc.Link(OPEN_NOTES, href=request.page_path, className="primary-link")]
          if request.status is RequestStatus.DONE and request.page_path else []),
    ])


def _czech_date(moment: datetime) -> str:
    return f"{moment.day}. {moment.month}. {moment.year}"
