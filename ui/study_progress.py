"""Study progress: the pager under every topic page and the "studied" marks kept in the browser."""

from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from dash import Dash, Input, Output, State, dcc, html

from ui import ids
from ui.navigation import HIDDEN, PAGE_BY_PATH, VISIBLE
from ui.topic_catalog import PageEntry, StudyStep, study_step
from ui.topics_page import topic_cards

STUDIED_LABEL = "✓ Prostudováno"
NOT_STUDIED_LABEL = "Označit jako prostudované"
STUDIED_BUTTON_CLASS = "secondary-button study-toggle studied"
NOT_STUDIED_BUTTON_CLASS = "secondary-button study-toggle"

StudiedPageIds = List[str]


def build_progress_store() -> dcc.Store:
    """Local storage keeps the progress per browser, without any account, and it never leaves the device."""
    return dcc.Store(id=ids.STUDY_PROGRESS_STORE, storage_type="local")


def build_study_pager() -> html.Nav:
    return html.Nav(
        id=ids.STUDY_PAGER,
        className="study-pager",
        style=HIDDEN,
        children=[
            html.Div(
                className="study-pager-status",
                children=[
                    html.Button(NOT_STUDIED_LABEL, id=ids.STUDY_TOGGLE_BUTTON, className=NOT_STUDIED_BUTTON_CLASS),
                    html.Span(id=ids.STUDY_STEP_LABEL, className="hint"),
                ],
            ),
            html.Div(id=ids.STUDY_PAGER_LINKS, className="study-pager-links"),
        ],
    )


def register_study_progress_callbacks(app: Dash) -> None:
    app.callback(
        Output(ids.STUDY_PAGER, "style"),
        Output(ids.STUDY_STEP_LABEL, "children"),
        Output(ids.STUDY_PAGER_LINKS, "children"),
        Output(ids.STUDY_TOGGLE_BUTTON, "children"),
        Output(ids.STUDY_TOGGLE_BUTTON, "className"),
        Input(ids.URL, "pathname"),
        Input(ids.STUDY_PROGRESS_STORE, "data"),
    )(describe_pager)
    app.callback(
        Output(ids.STUDY_PROGRESS_STORE, "data"),
        Input(ids.STUDY_TOGGLE_BUTTON, "n_clicks"),
        State(ids.URL, "pathname"),
        State(ids.STUDY_PROGRESS_STORE, "data"),
        prevent_initial_call=True,
    )(toggle_current_page)
    app.callback(
        Output(ids.TOPICS_LIST, "children"),
        Input(ids.STUDY_PROGRESS_STORE, "data"),
    )(describe_topics)


def studied_pages(stored: Optional[Sequence[str]]) -> StudiedPageIds:
    """The store is empty until the first page is marked."""
    return list(stored or [])


def toggle_page(studied: Sequence[str], page_id: str) -> StudiedPageIds:
    if page_id in studied:
        return [studied_id for studied_id in studied if studied_id != page_id]
    return [*studied, page_id]


def toggle_current_page(_clicks: Optional[int], pathname: str, stored: Optional[Sequence[str]]) -> StudiedPageIds:
    page_id = PAGE_BY_PATH.get(pathname)
    if page_id is None or study_step(page_id) is None:
        return studied_pages(stored)
    return toggle_page(studied_pages(stored), page_id)


def describe_topics(stored: Optional[Sequence[str]]) -> List[html.Section]:
    return topic_cards(studied_pages(stored))


def describe_pager(pathname: str, stored: Optional[Sequence[str]]) -> Tuple[dict, str, List, str, str]:
    page_id = PAGE_BY_PATH.get(pathname)
    step = study_step(page_id) if page_id else None
    if step is None:
        return HIDDEN, "", [], NOT_STUDIED_LABEL, NOT_STUDIED_BUTTON_CLASS

    is_studied = page_id in studied_pages(stored)
    return (
        VISIBLE,
        f"{step.topic.title} · krok {step.number} / {step.total}",
        _neighbour_links(step),
        STUDIED_LABEL if is_studied else NOT_STUDIED_LABEL,
        STUDIED_BUTTON_CLASS if is_studied else NOT_STUDIED_BUTTON_CLASS,
    )


def _neighbour_links(step: StudyStep) -> List:
    return [
        _neighbour_link(step.previous, "← Předchozí", "pager-previous"),
        _neighbour_link(step.next, "Další →", "pager-next"),
    ]


def _neighbour_link(page: Optional[PageEntry], direction: str, class_name: str) -> html.Div:
    if page is None:
        return html.Div(className=class_name)
    return html.Div(
        className=class_name,
        children=dcc.Link(
            href=page.path,
            className="pager-link",
            children=[html.Span(direction, className="pager-direction"), html.Span(page.title)],
        ),
    )
