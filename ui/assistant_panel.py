"""The assistant in the layout: the pop-up with explanations and previews, and the stores and timer of the agents.

Everything is always in the layout, so that the callbacks have their inputs from the start; assets/assistant.js
opens the pop-up right away when the reader asks the highlighter toolbar for an explanation. The agents themselves
are listed on their page (ui/agents_page.py), which the timer keeps current while one of them runs.
"""

from __future__ import annotations

from typing import List

from dash import dcc, html

from assistant.topics import NEW_TOPIC
from ui import ids
from ui.assistant_content import (
    ACCEPT_LABEL,
    CLOSE_LABEL,
    DEFAULT_TOPIC_SUFFIX,
    EXPAND_LABEL,
    NEW_TOPIC_LABEL,
    NEW_TOPIC_OPTION,
    NEW_TOPIC_PLACEHOLDER,
    REJECT_LABEL,
    START_LABEL,
    TOPIC_LABEL,
)
from ui.navigation import HIDDEN
from ui.topic_catalog import EXPANDED_TOPIC, choosable_topics

POLL_MILLISECONDS = 5000
MODAL_CLASS = "assistant-modal"
OPEN_MODAL_CLASS = "assistant-modal open"
SCROLL_CLASS = "assistant-scroll"
"""The part of the dialog that scrolls between the title and the buttons, so that the buttons never cover it."""


def build_assistant() -> html.Div:
    return html.Div(className="assistant", children=[
        dcc.Store(id=ids.ASSISTANT_REQUEST),
        dcc.Store(id=ids.ASSISTANT_CONTEXT),
        dcc.Store(id=ids.AGENTS_REFRESH),
        dcc.Store(id=ids.AGENTS_STATE),
        dcc.Interval(id=ids.AGENTS_INTERVAL, interval=POLL_MILLISECONDS, disabled=False),
        _modal(),
    ])


def topic_options() -> List[dict]:
    """Dropdown of the research topics a new page can join: the default first, a new topic last."""
    options = [
        {"label": topic.title + (DEFAULT_TOPIC_SUFFIX if topic.anchor == EXPANDED_TOPIC.anchor else ""),
         "value": topic.anchor}
        for topic in choosable_topics()
    ]
    return options + [{"label": NEW_TOPIC_OPTION, "value": NEW_TOPIC}]


def _modal() -> html.Div:
    return html.Div(id=ids.ASSISTANT_MODAL, className=MODAL_CLASS, children=html.Div(
        className="assistant-dialog",
        role="dialog",
        **{"aria-modal": "true", "aria-labelledby": ids.ASSISTANT_MODAL_TITLE},
        children=[
            html.H2(id=ids.ASSISTANT_MODAL_TITLE, className="assistant-title"),
            html.Div(className=SCROLL_CLASS, children=[
                dcc.Loading(type="dot", children=html.Div(id=ids.ASSISTANT_MODAL_BODY, className="assistant-body")),
                _placement_chooser(),
                html.P(id=ids.ASSISTANT_MODAL_MESSAGE, className="error-message"),
            ]),
            html.Div(className="assistant-actions", children=[
                html.Button(EXPAND_LABEL, id=ids.ASSISTANT_EXPAND_BUTTON, className="primary-button", style=HIDDEN),
                html.Button(START_LABEL, id=ids.ASSISTANT_START_BUTTON, className="primary-button", style=HIDDEN),
                html.Button(ACCEPT_LABEL, id=ids.ASSISTANT_ACCEPT_BUTTON, className="primary-button", style=HIDDEN),
                html.Button(REJECT_LABEL, id=ids.ASSISTANT_REJECT_BUTTON, className="secondary-button", style=HIDDEN),
                html.Button(CLOSE_LABEL, id=ids.ASSISTANT_CLOSE_BUTTON, className="secondary-button"),
            ]),
        ],
    ))


def _placement_chooser() -> html.Div:
    """Where the new page joins the topics; shown before an agent starts and again when its proposal is approved."""
    return html.Div(id=ids.ASSISTANT_PLACEMENT, className="assistant-placement", style=HIDDEN, children=[
        html.Div(className="field", children=[
            html.Label(TOPIC_LABEL),
            dcc.Dropdown(
                id=ids.ASSISTANT_TOPIC_DROPDOWN, options=topic_options(), value=EXPANDED_TOPIC.anchor, clearable=False,
            ),
        ]),
        html.Div(className="field", children=[
            html.Label(NEW_TOPIC_LABEL),
            dcc.Input(id=ids.ASSISTANT_NEW_TOPIC_INPUT, type="text", value="", placeholder=NEW_TOPIC_PLACEHOLDER),
        ]),
    ])
