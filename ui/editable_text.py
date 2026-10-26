"""Paragraphs that the reader can edit by hand, and the pages served with the saved edits (edits/).

On every page each dcc.Markdown and each html.P with plain text gets a pattern-matching id {"type": TEXT_EDIT,
"page": page id, "key": block key}. A Markdown with several blocks is split into one Markdown per block, which
renders the same and lets each paragraph be edited on its own. assets/text_edit.js finds the block under the
selection by this id and the save callback changes its children in place. Components that already have an id are
left alone, because callbacks fill them.
"""

from __future__ import annotations

import copy
import threading
from collections import Counter
from dataclasses import dataclass
from typing import Callable, Collection, Dict, List, Mapping, Optional, Tuple

from dash import dcc, html
from dash.development.base_component import Component

from edits.blocks import block_key, split_blocks
from edits.store import TextEdits
from ui import ids
from ui.navigation import PAGE_IDS

LAYOUT = "layout"
"""Cache name of the served layout, whose pages are the ones with forms; the lazy pages are cached by their id."""


@dataclass(frozen=True)
class Block:
    page_id: str
    key: str
    original: str
    markdown: bool
    """Markdown with formulas; otherwise plain text of an html.P."""


Blocks = Dict[Tuple[str, str], Block]
EditsOf = Callable[[str], Mapping[str, str]]
"""Edited texts of a page's blocks by block key."""


def editable_id(page_id: str, key: str) -> dict:
    return {"type": ids.TEXT_EDIT, "page": page_id, "key": key}


def editable(component: Component, edits_of: EditsOf) -> Tuple[Component, Blocks]:
    """A copy of the tree with editable paragraphs inside the pages and the edits applied, and its blocks.

    Components that do not change are shared with the original tree, which is never modified.
    """
    blocks: Blocks = {}
    walked = _Walk(edits_of, blocks).node(component, None)
    return walked[0], blocks


class _Walk:
    def __init__(self, edits_of: EditsOf, blocks: Blocks) -> None:
        self._edits_of = edits_of
        self._blocks = blocks
        self._edits: Mapping[str, str] = {}
        self._seen: Counter = Counter()

    def node(self, node, page_id: Optional[str]) -> List:
        """The node as one or more nodes: a Markdown with several blocks becomes one Markdown per block."""
        if not isinstance(node, Component):
            return [node]
        node_id = getattr(node, "id", None)
        if isinstance(node_id, str) and node_id in PAGE_IDS:
            page_id = node_id
            self._edits = self._edits_of(page_id)
            self._seen = Counter()
        elif page_id and node_id is None:
            if isinstance(node, dcc.Markdown) and isinstance(getattr(node, "children", None), str):
                return self._markdown(node, page_id) or [node]
            if isinstance(node, html.P) and isinstance(getattr(node, "children", None), str) and node.children.strip():
                return [self._paragraph(node, page_id)]
        children = getattr(node, "children", None)
        if not isinstance(children, (Component, list, tuple)):
            return [node]
        original = list(children) if isinstance(children, (list, tuple)) else [children]
        walked = [walked_child for child in original for walked_child in self.node(child, page_id)]
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
            key = self._register(page_id, block, True)
            markdowns.append(dcc.Markdown(self._edits.get(key, block), id=editable_id(page_id, key), **props))
        return markdowns

    def _paragraph(self, node: html.P, page_id: str) -> html.P:
        key = self._register(page_id, node.children, False)
        changed = copy.copy(node)
        changed.id = editable_id(page_id, key)
        changed.children = self._edits.get(key, node.children)
        return changed

    def _register(self, page_id: str, original: str, markdown: bool) -> str:
        """Key of the block; the same text twice on a page gets a numbered key the second time."""
        key = block_key(original.strip())
        self._seen[key] += 1
        if self._seen[key] > 1:
            key = f"{key}-{self._seen[key]}"
        self._blocks[(page_id, key)] = Block(page_id, key, original, markdown)
        return key


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
