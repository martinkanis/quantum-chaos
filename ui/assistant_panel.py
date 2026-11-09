"""The assistant in the layout: the pop-up with explanations and previews, and the stores and timer of the agents.

Everything is always in the layout, so that the callbacks have their inputs from the start; assets/assistant.js
opens the pop-up right away when the reader asks the highlighter toolbar for an explanation. The agents themselves
are listed on their page (ui/agents_page.py), which the timer keeps current while one of them runs.
"""

from __future__ import annotations

from dash import dcc, html

from ui import ids
from ui.assistant_content import ACCEPT_LABEL, CLOSE_LABEL, EXPAND_LABEL, REJECT_LABEL
from ui.navigation import HIDDEN

POLL_MILLISECONDS = 5000
MODAL_CLASS = "assistant-modal"
OPEN_MODAL_CLASS = "assistant-modal open"


def build_assistant() -> html.Div:
    return html.Div(className="assistant", children=[
        dcc.Store(id=ids.ASSISTANT_REQUEST),
        dcc.Store(id=ids.ASSISTANT_CONTEXT),
        dcc.Store(id=ids.AGENTS_REFRESH),
        dcc.Store(id=ids.AGENTS_STATE),
        dcc.Interval(id=ids.AGENTS_INTERVAL, interval=POLL_MILLISECONDS, disabled=False),
        _modal(),
    ])


def _modal() -> html.Div:
    return html.Div(id=ids.ASSISTANT_MODAL, className=MODAL_CLASS, children=html.Div(
        className="assistant-dialog",
        role="dialog",
        **{"aria-modal": "true", "aria-labelledby": ids.ASSISTANT_MODAL_TITLE},
        children=[
            html.H2(id=ids.ASSISTANT_MODAL_TITLE, className="assistant-title"),
            dcc.Loading(type="dot", children=html.Div(id=ids.ASSISTANT_MODAL_BODY, className="assistant-body")),
            html.P(id=ids.ASSISTANT_MODAL_MESSAGE, className="error-message"),
            html.Div(className="assistant-actions", children=[
                html.Button(EXPAND_LABEL, id=ids.ASSISTANT_EXPAND_BUTTON, className="primary-button", style=HIDDEN),
                html.Button(ACCEPT_LABEL, id=ids.ASSISTANT_ACCEPT_BUTTON, className="primary-button", style=HIDDEN),
                html.Button(REJECT_LABEL, id=ids.ASSISTANT_REJECT_BUTTON, className="secondary-button", style=HIDDEN),
                html.Button(CLOSE_LABEL, id=ids.ASSISTANT_CLOSE_BUTTON, className="secondary-button"),
            ]),
        ],
    ))
