"""Text the reader selected on a page, with the context the browser sends along (assets/highlighter.js)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

MAX_SELECTION_LENGTH = 2000
MAX_PARAGRAPH_LENGTH = 4000
MAX_TITLE_LENGTH = 300
MAX_PAGE_ID_LENGTH = 100


class SelectionError(ValueError):
    """The request from the browser is not usable; the message says why in Czech."""


@dataclass(frozen=True)
class SelectionContext:
    page_id: str
    page_title: str
    section_title: str
    """Heading of the chapter around the selection; empty when the page has none."""
    selection: str
    paragraph: str
    """The paragraph (or list item) the selection starts in, for context."""


def selection_from_request(data: Any) -> SelectionContext:
    if not isinstance(data, Mapping):
        raise SelectionError("Chybí označený text. Označ text na stránce a zkus to znovu.")
    selection = _text(data, "selection")
    if not selection:
        raise SelectionError("Chybí označený text. Označ text na stránce a zkus to znovu.")
    if len(selection) > MAX_SELECTION_LENGTH:
        raise SelectionError(
            f"Označený text je moc dlouhý ({len(selection)} znaků). Označ nejvýš {MAX_SELECTION_LENGTH} znaků."
        )
    return SelectionContext(
        page_id=_text(data, "page_id")[:MAX_PAGE_ID_LENGTH],
        page_title=_text(data, "page_title")[:MAX_TITLE_LENGTH],
        section_title=_text(data, "section_title")[:MAX_TITLE_LENGTH],
        selection=selection,
        paragraph=_text(data, "paragraph")[:MAX_PARAGRAPH_LENGTH],
    )


def selection_to_dict(context: SelectionContext) -> dict:
    return {
        "page_id": context.page_id,
        "page_title": context.page_title,
        "section_title": context.section_title,
        "selection": context.selection,
        "paragraph": context.paragraph,
    }


def _text(data: Mapping[str, Any], key: str) -> str:
    """Text with white space collapsed: the browser sends layout line breaks and indentation along."""
    value = data.get(key)
    return " ".join(value.split()) if isinstance(value, str) else ""
