"""Texts of the pages that the reader can edit by hand, and the pages served with the saved edits (edits/).

Every text on a page gets a pattern-matching id {"type": TEXT_EDIT, "page", "key", "copy"}: each block of a
dcc.Markdown (a Markdown with several blocks is split into one Markdown per block, which renders the same), and
each plain text of an html component or a dcc.Link – the component itself when the text is its only child,
otherwise the text wrapped in an html.Span. The key is the hash of the original text, so the same text twice on a
page is one block with two copies and one edit changes both (a chapter title and its entry in the contents).
assets/text_edit.js finds the block under the selection by this id and the save callback changes every copy in
place. Components with an id of their own are left alone, because callbacks fill them; so are buttons, code and
texts without a letter (chapter numbers, icons).
"""

from __future__ import annotations

import copy
import threading
from dataclasses import dataclass, replace
from typing import Callable, Collection, Dict, List, Mapping, Optional, Tuple

from dash import dcc, html
from dash.development.base_component import Component

from edits.blocks import block_key, split_blocks
from edits.store import TextEdits
from ui import ids
from ui.navigation import PAGE_IDS

LAYOUT = "layout"
"""Cache name of the served layout, whose pages are the ones with forms; the lazy pages are cached by their id."""
NOT_EDITABLE = (html.Button, html.A, html.Code, html.Pre, html.Script, html.Textarea, html.Option, html.Kbd, html.Samp)
"""Plain texts inside these stay as they are: a click on them does something else, or the text is code."""

Edges = Tuple[str, str]
"""White space before and after a plain text; an edit keeps it, so „V kostce: “ still ends with a space."""


@dataclass(frozen=True)
class Block:
    page_id: str
    key: str
    original: str
    markdown: bool
    """Markdown with formulas; otherwise plain text."""
    edges: Tuple[Edges, ...] = (("", ""),)
    """One entry per copy of the block on the page, in page order."""

    @property
    def copies(self) -> int:
        return len(self.edges)


Blocks = Dict[Tuple[str, str], Block]
EditsOf = Callable[[str], Mapping[str, str]]
"""Edited texts of a page's blocks by block key."""


def editable_id(page_id: str, key: str, copy_number: int = 1) -> dict:
    return {"type": ids.TEXT_EDIT, "page": page_id, "key": key, "copy": copy_number}


def copy_ids(block: Block) -> List[dict]:
    return [editable_id(block.page_id, block.key, number) for number in range(1, block.copies + 1)]


def shown_text(block: Block, copy_number: int, text: str) -> str:
    """Children of one copy for the given text: a plain text keeps the white space around the original."""
    before, after = block.edges[copy_number - 1]
    return before + text.strip() + after if not block.markdown else text


def editable(component: Component, edits_of: EditsOf) -> Tuple[Component, Blocks]:
    """A copy of the tree with editable texts inside the pages and the edits applied, and its blocks.

    Components that do not change are shared with the original tree, which is never modified.
    """
    blocks: Blocks = {}
    walked = _Walk(edits_of, blocks).node(component, None)
    return walked[0], blocks


def _has_letter(text: str) -> bool:
    return any(character.isalpha() for character in text)


def _holds_plain_text(node: Component) -> bool:
    """Components whose own text children are editable: html elements other than NOT_EDITABLE, and links."""
    if isinstance(node, NOT_EDITABLE):
        return False
    return isinstance(node, dcc.Link) or type(node).__module__.startswith("dash.html")


class _Walk:
    def __init__(self, edits_of: EditsOf, blocks: Blocks) -> None:
        self._edits_of = edits_of
        self._blocks = blocks
        self._edits: Mapping[str, str] = {}

    def node(self, node, page_id: Optional[str]) -> List:
        """The node as one or more nodes: a Markdown with several blocks becomes one Markdown per block."""
        if not isinstance(node, Component):
            return [node]
        node_id = getattr(node, "id", None)
        children = getattr(node, "children", None)
        if isinstance(node_id, str) and node_id in PAGE_IDS:
            page_id = node_id
            self._edits = self._edits_of(page_id)
        elif page_id and node_id is None:
            if isinstance(node, dcc.Markdown) and isinstance(children, str):
                return self._markdown(node, page_id) or [node]
            if isinstance(children, str) and _has_letter(children) and _holds_plain_text(node):
                return [self._plain(node, page_id)]
        if not isinstance(children, (Component, list, tuple)):
            return [node]
        original = list(children) if isinstance(children, (list, tuple)) else [children]
        wraps_texts = bool(page_id) and node_id is None and _holds_plain_text(node)
        walked = [
            walked_child for child in original
            for walked_child in (
                [self._wrapped_text(child, page_id)] if wraps_texts and isinstance(child, str) and _has_letter(child)
                else self.node(child, page_id)
            )
        ]
        if len(walked) == len(original) and all(new is old for new, old in zip(walked, original)):
            return [node]
        changed = copy.copy(node)
        changed.children = walked if isinstance(children, (list, tuple)) or len(walked) != 1 else walked[0]
        return [changed]

    def _markdown(self, node: dcc.Markdown, page_id: str) -> List[Component]:
        props = {
            name: getattr(node, name) for name in node._prop_names
            if name not in ("children", "id") and hasattr(node, name)
        }
        markdowns = []
        for block in split_blocks(node.children):
            key, copy_number = self._register(page_id, block, True)
            text = self._edits.get(key, block)
            markdowns.append(dcc.Markdown(text, id=editable_id(page_id, key, copy_number), **props))
        return markdowns

    def _plain(self, node: Component, page_id: str) -> Component:
        """The component with its only child, a plain text, as an editable block."""
        changed = copy.copy(node)
        changed.id, changed.children = self._plain_text(node.children, page_id)
        return changed

    def _wrapped_text(self, text: str, page_id: str) -> html.Span:
        """A plain text among other children, wrapped so that it can carry an id."""
        span_id, children = self._plain_text(text, page_id)
        return html.Span(children, id=span_id)

    def _plain_text(self, text: str, page_id: str) -> Tuple[dict, str]:
        key, copy_number = self._register(page_id, text, False)
        block = self._blocks[(page_id, key)]
        edited = self._edits.get(key)
        return editable_id(page_id, key, copy_number), shown_text(block, copy_number, edited) if edited else text

    def _register(self, page_id: str, original: str, markdown: bool) -> Tuple[str, int]:
        """Key of the block and the number of this copy; the first copy decides the original and the kind."""
        stripped = original.strip()
        key = block_key(stripped)
        edges = (original[:len(original) - len(original.lstrip())], original[len(original.rstrip()):])
        known = self._blocks.get((page_id, key))
        if known is None:
            self._blocks[(page_id, key)] = Block(page_id, key, original, markdown, (edges,))
            return key, 1
        self._blocks[(page_id, key)] = replace(known, edges=known.edges + (edges,))
        return key, known.copies + 1


class EditablePages:
    """The served layout and the lazy pages with the saved edits, each built once until the edits change."""

    def __init__(
        self,
        text_edits: TextEdits,
        build_layout: Callable[[], Component],
        built_page: Callable[[str], Component],
        lazy_page_ids: Collection[str],
    ) -> None:
        self.text_edits = text_edits
        self._build_layout = build_layout
        self._built_page = built_page
        self._lazy_page_ids = frozenset(lazy_page_ids)
        self._cache: Dict[str, Tuple[Component, Blocks]] = {}
        self._cache_version: Optional[int] = None
        self._lock = threading.Lock()

    def layout(self) -> Component:
        """The app layout for Dash (app.layout is this method, so each page load gets the current edits)."""
        return self._edited(LAYOUT)[0]

    def page_children(self, page_id: str) -> List:
        return self._edited(page_id)[0].children

    def block(self, page_id: str, key: str) -> Optional[Block]:
        name = page_id if page_id in self._lazy_page_ids else LAYOUT
        return self._edited(name)[1].get((page_id, key))

    def _edited(self, name: str) -> Tuple[Component, Blocks]:
        version = self.text_edits.version()
        with self._lock:
            if self._cache_version != version:
                self._cache, self._cache_version = {}, version
            cached = self._cache.get(name)
        if cached is None:
            source = self._build_layout() if name == LAYOUT else self._built_page(name)
            cached = editable(source, self.text_edits.for_page)
            with self._lock:
                if self._cache_version == version:
                    self._cache[name] = cached
        return cached
