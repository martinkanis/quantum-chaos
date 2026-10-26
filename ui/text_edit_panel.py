"""The paragraph editor in the layout: a pop-up with the paragraph's source text, opened from the highlighter toolbar.

It is always in the layout, so that the callbacks have their inputs from the start; assets/text_edit.js opens it
right away and asks for the paragraph through TEXT_EDIT_REQUEST.
"""

from __future__ import annotations

from dash import dcc, html

from ui import ids
from ui.navigation import HIDDEN
from ui.text_edit_content import CANCEL_LABEL, ORIGINAL_LABEL, REVERT_LABEL, SAVE_LABEL, TITLE

MODAL_CLASS = "assistant-modal"
OPEN_MODAL_CLASS = "assistant-modal open"
"""The look of the assistant's pop-up (assets/assistant.css)."""
TEXT_ROWS = 12


def build_text_editor() -> html.Div:
    return html.Div(className="text-editor", children=[
        dcc.Store(id=ids.TEXT_EDIT_REQUEST),
        dcc.Store(id=ids.TEXT_EDIT_CONTEXT),
        html.Div(id=ids.TEXT_EDIT_MODAL, className=MODAL_CLASS, children=html.Div(
            className="assistant-dialog",
            role="dialog",
            **{"aria-modal": "true", "aria-labelledby": ids.TEXT_EDIT_TITLE},
            children=[
                html.H2(TITLE, id=ids.TEXT_EDIT_TITLE, className="assistant-title"),
                html.Div(id=ids.TEXT_EDIT_HINT, className="hint small"),
                dcc.Textarea(id=ids.TEXT_EDIT_TEXT, className="text-edit-area", rows=TEXT_ROWS, value=""),
                html.Details(id=ids.TEXT_EDIT_ORIGINAL_BOX, className="text-edit-original", style=HIDDEN, children=[
                    html.Summary(ORIGINAL_LABEL),
                    html.Pre(id=ids.TEXT_EDIT_ORIGINAL),
                ]),
                html.P(id=ids.TEXT_EDIT_MESSAGE, className="error-message"),
                html.Div(className="assistant-actions", children=[
                    html.Button(REVERT_LABEL, id=ids.TEXT_EDIT_REVERT_BUTTON, className="secondary-button", style=HIDDEN),
                    html.Button(CANCEL_LABEL, id=ids.TEXT_EDIT_CANCEL_BUTTON, className="secondary-button"),
                    html.Button(SAVE_LABEL, id=ids.TEXT_EDIT_SAVE_BUTTON, className="primary-button"),
                ]),
            ],
        )),
    ])
