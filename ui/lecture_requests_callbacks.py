"""Callbacks of the lecture notes page: queue a request and show the queue."""

from __future__ import annotations

from typing import Any, List, Tuple

from dash import Dash, Input, Output, State, ctx, html, no_update

from assistant.lecture_requests import LectureRequestError, LectureRequestStore, new_request
from ui import ids
from ui.lecture_requests_content import SUBMITTED
from ui.lecture_requests_page import request_list
from ui.navigation import LECTURE_REQUESTS_PATH


def register_lecture_request_callbacks(app: Dash, store: LectureRequestStore) -> None:
    app.callback(
        Output(ids.LECTURE_REQUEST_MESSAGE, "children"),
        Output(ids.LECTURE_REQUEST_LIST, "children"),
        Output(ids.LECTURE_REQUEST_URL, "value"),
        Input(ids.LECTURE_REQUEST_SUBMIT, "n_clicks"),
        Input(ids.LECTURE_REQUEST_REFRESH, "n_clicks"),
        Input(ids.URL, "pathname"),
        State(ids.LECTURE_REQUEST_URL, "value"),
        State(ids.LECTURE_REQUEST_TOPIC, "value"),
        State(ids.LECTURE_REQUEST_NEW_TOPIC, "value"),
        State(ids.LECTURE_REQUEST_DETAIL, "value"),
        State(ids.LECTURE_REQUEST_PRESENTATION, "value"),
        State(ids.LECTURE_REQUEST_NOTE, "value"),
    )(lambda _submit, _refresh, pathname, *form: handle_lecture_request(store, ctx.triggered_id, pathname, form))


def handle_lecture_request(store: LectureRequestStore, trigger: Any, pathname: str, form: Tuple) -> Tuple:
    """Message, the queue and the URL field; the queue is read only on this page, not on every navigation."""
    if trigger == ids.LECTURE_REQUEST_SUBMIT:
        try:
            store.add(new_request(*form))
        except LectureRequestError as error:
            return html.P(str(error), className="error-message"), _queue(store), no_update
        return html.P(SUBMITTED, className="success-message"), _queue(store), ""
    if trigger == ids.LECTURE_REQUEST_REFRESH or pathname == LECTURE_REQUESTS_PATH:
        return no_update, _queue(store), no_update
    return no_update, no_update, no_update


def _queue(store: LectureRequestStore) -> List:
    try:
        return request_list(store.recent())
    except LectureRequestError as error:
        return [html.P(str(error), className="error-message")]
