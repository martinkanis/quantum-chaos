"""Callbacks of the paragraph editor: opening a paragraph, saving the new text and returning to the original.

A saved paragraph changes on the page at once (set_props on its editable id), and every page served afterwards
is built with the edit (ui/editable_text.py). The work is in plain functions that return an EditorView, which the
tests call directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Mapping, Optional, Tuple

from dash import Dash, Input, Output, State, ctx, no_update, set_props

from edits.store import TextEditError
from ui import ids
from ui.editable_text import Block, EditablePages, editable_id
from ui.navigation import HIDDEN, VISIBLE
from ui.text_edit_content import MARKDOWN_HINT, MEMORY_HINT, MISSING_BLOCK, PLAIN_HINT
from ui.text_edit_panel import MODAL_CLASS, OPEN_MODAL_CLASS

MAX_PAGE_ID_LENGTH = 100
MAX_KEY_LENGTH = 40


@dataclass(frozen=True)
class EditorView:
    """What an action changes; fields left at no_update keep the pop-up as it is."""

    open: Any = no_update
    text: Any = no_update
    hint: Any = no_update
    original: Any = no_update
    """The original text when the paragraph is edited, otherwise None (the box is hidden)."""
    message: Any = ""
    can_revert: Any = no_update
    context: Any = no_update
    changed: Optional[Tuple[dict, str]] = None
    """Editable id and new children of the paragraph on the page."""


def handle_editor_action(
    pages: EditablePages, trigger: Any, request: Optional[Mapping], text: Any, context: Optional[Mapping]
) -> EditorView:
    if trigger == ids.TEXT_EDIT_REQUEST:
        return open_block(pages, request or {})
    if trigger == ids.TEXT_EDIT_SAVE_BUTTON:
        return save(pages, context or {}, text)
    if trigger == ids.TEXT_EDIT_REVERT_BUTTON:
        return revert(pages, context or {})
    return EditorView()


def open_block(pages: EditablePages, request: Mapping) -> EditorView:
    block = _block(pages, request)
    if block is None:
        return EditorView(
            open=True, text="", hint="", original=None, message=MISSING_BLOCK, can_revert=False, context=None,
        )
    edit = pages.text_edits.get(block.page_id, block.key)
    return EditorView(
        open=True,
        text=edit.text if edit else block.original.strip(),
        hint=_hint(pages, block),
        original=block.original.strip() if edit else None,
        can_revert=edit is not None,
        context={"page": block.page_id, "key": block.key},
    )


def save(pages: EditablePages, context: Mapping, text: Any) -> EditorView:
    block = _block(pages, context)
    if block is None:
        return EditorView(message=MISSING_BLOCK)
    try:
        edit = pages.text_edits.save(block.page_id, block.key, block.original, text)
    except TextEditError as error:
        return EditorView(message=str(error))
    return _closed(block, edit.text if edit else block.original)


def revert(pages: EditablePages, context: Mapping) -> EditorView:
    block = _block(pages, context)
    if block is None:
        return EditorView(message=MISSING_BLOCK)
    try:
        pages.text_edits.revert(block.page_id, block.key)
    except TextEditError as error:
        return EditorView(message=str(error))
    return _closed(block, block.original)


def editor_outputs(view: EditorView) -> Tuple:
    modal_class = no_update if view.open is no_update else (OPEN_MODAL_CLASS if view.open else MODAL_CLASS)
    original_style = no_update if view.original is no_update else (HIDDEN if view.original is None else VISIBLE)
    original = no_update if view.original is no_update else (view.original or "")
    revert_style = no_update if view.can_revert is no_update else (VISIBLE if view.can_revert else HIDDEN)
    return modal_class, view.text, view.hint, original_style, original, view.message, revert_style, view.context


def _closed(block: Block, children: str) -> EditorView:
    return EditorView(open=False, context=None, changed=(editable_id(block.page_id, block.key), children))


def _hint(pages: EditablePages, block: Block) -> List[str]:
    hints = [MARKDOWN_HINT if block.markdown else PLAIN_HINT]
    if not pages.text_edits.persistent:
        hints.append(" " + MEMORY_HINT)
    return hints


def _block(pages: EditablePages, request: Mapping) -> Optional[Block]:
    page_id, key = request.get("page"), request.get("key")
    if not isinstance(page_id, str) or not isinstance(key, str):
        return None
    if len(page_id) > MAX_PAGE_ID_LENGTH or len(key) > MAX_KEY_LENGTH:
        return None
    return pages.block(page_id, key)


CANCEL_JS = "function(clicks) { return clicks ? '" + MODAL_CLASS + "' : window.dash_clientside.no_update; }"


def register_text_edit_callbacks(app: Dash, pages: EditablePages) -> None:
    def on_action(request, _save, _revert, text, context):
        view = handle_editor_action(pages, ctx.triggered_id, request, text, context)
        if view.changed:
            set_props(view.changed[0], {"children": view.changed[1]})
        return editor_outputs(view)

    app.callback(
        Output(ids.TEXT_EDIT_MODAL, "className", allow_duplicate=True),
        Output(ids.TEXT_EDIT_TEXT, "value"),
        Output(ids.TEXT_EDIT_HINT, "children"),
        Output(ids.TEXT_EDIT_ORIGINAL_BOX, "style"),
        Output(ids.TEXT_EDIT_ORIGINAL, "children"),
        Output(ids.TEXT_EDIT_MESSAGE, "children"),
        Output(ids.TEXT_EDIT_REVERT_BUTTON, "style"),
        Output(ids.TEXT_EDIT_CONTEXT, "data"),
        Input(ids.TEXT_EDIT_REQUEST, "data"),
        Input(ids.TEXT_EDIT_SAVE_BUTTON, "n_clicks"),
        Input(ids.TEXT_EDIT_REVERT_BUTTON, "n_clicks"),
        State(ids.TEXT_EDIT_TEXT, "value"),
        State(ids.TEXT_EDIT_CONTEXT, "data"),
        prevent_initial_call=True,
    )(on_action)

    app.clientside_callback(
        CANCEL_JS,
        Output(ids.TEXT_EDIT_MODAL, "className"),
        Input(ids.TEXT_EDIT_CANCEL_BUTTON, "n_clicks"),
        prevent_initial_call=True,
    )
