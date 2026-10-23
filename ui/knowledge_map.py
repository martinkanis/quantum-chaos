"""Knowledge map: nodes with positions, typed relations and the Cytoscape elements that draw them.

The user's own subtopics and connections are parsed in ui/knowledge_map_notes.py and passed in here. Nodes can be
dragged in the browser; the positions the user chose come back as `positions` and win over the default layout.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Collection, Dict, List, Mapping, Optional, Sequence, Tuple

from ui.knowledge_map_content import (
    CENTRAL_QUESTION,
    CENTRAL_QUESTION_SHORT,
    LAYERS,
    MAP_LABELS,
    RELATION_KINDS,
    RELATIONS,
    Layer,
    Relation,
    RelationKind,
    RelationKindInfo,
)
from ui.knowledge_map_notes import Subtopic
from ui.topic_catalog import page_entries

CENTER_ID = "stred"
HUB_RADIUS = 1.7
PAGE_RADIUS = 3.4
SUBTOPIC_RADIUS = 4.6
SUBTOPIC_SPREAD_DEGREES = 9.0
MIN_SECTOR_PAGES = 2
"""A group with a single page still gets the room of two, so its hub does not sit right next to a neighbour."""
PIXELS_PER_UNIT = 120
"""Cytoscape works in pixels with y pointing down; the layout above is in units with y pointing up."""
LABEL_WIDTH = 16
LABEL_SIDE_THRESHOLD = 0.35
CENTER_COLOR = "#1c2330"
STRUCTURE_COLOR = "#dde2ea"
OWN_CONNECTION_COLOR = "#1c2330"
FADED_OPACITY = 0.15
HOVER_NOTE_LENGTH = 160

Position = Dict[str, float]

STYLESHEET: List[dict] = [
    {"selector": "node", "style": {
        "label": "data(label)", "text-wrap": "wrap", "font-size": 14, "color": CENTER_COLOR,
        "background-color": "data(color)", "width": 26, "height": 26, "text-valign": "bottom", "text-margin-y": 5,
        "text-background-color": "#ffffff", "text-background-opacity": 0.7, "text-background-padding": 1,
    }},
    {"selector": "node.center", "style": {"width": 70, "height": 70, "font-size": 17, "font-weight": "bold"}},
    {"selector": "node.layer", "style": {"width": 44, "height": 44, "font-size": 16, "font-weight": "bold"}},
    {"selector": "node.subtopic", "style": {"shape": "diamond", "width": 26, "height": 26, "font-style": "italic"}},
    {"selector": "node.label-right", "style": {"text-halign": "right", "text-valign": "center", "text-margin-x": 8}},
    {"selector": "node.label-left", "style": {"text-halign": "left", "text-valign": "center", "text-margin-x": -8}},
    {"selector": "node.label-top", "style": {"text-valign": "top", "text-margin-y": -5}},
    {"selector": "node.page, node.subtopic", "style": {"cursor": "pointer"}},
    {"selector": "edge.structure", "style": {"line-color": STRUCTURE_COLOR, "width": 2, "curve-style": "straight"}},
    {"selector": "edge.relation", "style": {
        "width": 2.5, "line-color": "data(color)", "target-arrow-color": "data(color)",
        "target-arrow-shape": "triangle", "curve-style": "bezier", "arrow-scale": 1.1,
    }},
    {"selector": "edge.own", "style": {"line-style": "dashed", "width": 3}},
    {"selector": ".faded", "style": {"opacity": FADED_OPACITY}},
    {"selector": "node.chosen", "style": {"border-width": 3, "border-color": CENTER_COLOR}},
    {"selector": "node:selected", "style": {"overlay-opacity": 0}},
]
"""Colours come from each element's data, so one stylesheet serves every group and kind of relation."""


@dataclass(frozen=True)
class MapNode:
    node_id: str
    title: str
    description: str
    kind: str
    """"center", "layer", "page" or "subtopic"."""
    x: float
    y: float
    color: str
    layer: Optional[Layer] = None
    path: Optional[str] = None
    label: str = ""
    """Short text drawn next to the node; the title is shown in the details and on hover."""


@dataclass(frozen=True)
class NodeRelation:
    direction: str
    """"out" when the node is the source, "in" when it is the target."""
    kind_label: str
    other: MapNode
    note: str
    is_own: bool


def map_nodes(subtopics: Sequence[Subtopic] = ()) -> Dict[str, MapNode]:
    """The central question in the middle, group hubs around it, every page on a ring and own subtopics outside it.

    Each group owns a slice of the ring proportional to its number of pages; its hub sits in the middle of the
    slice, so the lines from a hub to its pages fan out without crossing other groups. A subtopic sits behind the
    first page it expands.
    """
    entries = page_entries()
    nodes = {
        CENTER_ID: MapNode(
            CENTER_ID, CENTRAL_QUESTION_SHORT, CENTRAL_QUESTION, "center", 0.0, 0.0, CENTER_COLOR,
            label=CENTRAL_QUESTION_SHORT,
        ),
    }
    page_angles: Dict[str, float] = {}
    weights = [max(len(info.page_ids), MIN_SECTOR_PAGES) for info in LAYERS]
    sector_start = 90.0
    for info, weight in zip(LAYERS, weights):
        sector = 360.0 * weight / sum(weights)
        middle = math.radians(sector_start - sector / 2)
        nodes[_layer_node_id(info.layer)] = MapNode(
            _layer_node_id(info.layer), info.title, info.role, "layer",
            HUB_RADIUS * math.cos(middle), HUB_RADIUS * math.sin(middle), info.color, info.layer, label=info.title,
        )
        step = sector / len(info.page_ids)
        for position, page_id in enumerate(info.page_ids):
            angle = math.radians(sector_start - step * (position + 0.5))
            page_angles[page_id] = angle
            entry = entries[page_id]
            nodes[page_id] = MapNode(
                page_id, entry.title, entry.description, "page",
                PAGE_RADIUS * math.cos(angle), PAGE_RADIUS * math.sin(angle), info.color, info.layer, entry.path,
                MAP_LABELS.get(page_id, entry.title),
            )
        sector_start -= sector
    nodes.update(_subtopic_nodes(subtopics, nodes, page_angles))
    return nodes


def page_ids() -> List[str]:
    return [page_id for info in LAYERS for page_id in info.page_ids]


def node_options(subtopics: Sequence[Subtopic] = ()) -> List[Dict[str, str]]:
    """Pages in the order of their groups, then the user's subtopics, for the drop-downs of the forms."""
    nodes = map_nodes(subtopics)
    pages = [
        {"label": f"{nodes[page_id].label} ({info.title})", "value": page_id}
        for info in LAYERS for page_id in info.page_ids
    ]
    own = [{"label": f"{subtopic.title} (vlastní podtéma)", "value": subtopic.subtopic_id} for subtopic in subtopics]
    return pages + own


def kind_info(kind: RelationKind) -> RelationKindInfo:
    return next(info for info in RELATION_KINDS if info.kind == kind)


def subtopic_relations(subtopics: Sequence[Subtopic]) -> List[Relation]:
    return [
        Relation(subtopic.subtopic_id, RelationKind.EXPANDS, page_id, "")
        for subtopic in subtopics for page_id in subtopic.page_ids
    ]


def connection_label(relation: Relation, subtopics: Sequence[Subtopic] = ()) -> str:
    nodes = map_nodes(subtopics)
    note = f" – {relation.note}" if relation.note else ""
    return f"{nodes[relation.source].label} {kind_info(relation.kind).label} {nodes[relation.target].label}{note}"


def relations_of(node_id: str, own: Sequence[Relation], subtopics: Sequence[Subtopic] = ()) -> List[NodeRelation]:
    nodes = map_nodes(subtopics)
    found = []
    for relation, is_own in _all_relations(own, subtopics):
        if node_id not in (relation.source, relation.target):
            continue
        direction = "out" if relation.source == node_id else "in"
        other_id = relation.target if direction == "out" else relation.source
        found.append(NodeRelation(direction, kind_info(relation.kind).label, nodes[other_id], relation.note, is_own))
    return found


def default_positions(subtopics: Sequence[Subtopic] = ()) -> Dict[str, Position]:
    return {node_id: _pixels(node) for node_id, node in map_nodes(subtopics).items()}


def build_elements(
    visible_layers: Collection[str], visible_kinds: Collection[str], own: Sequence[Relation],
    subtopics: Sequence[Subtopic] = (), selected: Optional[str] = None,
    positions: Optional[Mapping[str, Mapping[str, float]]] = None,
) -> List[dict]:
    """Nodes and edges for Cytoscape; a dragged node keeps the position from `positions`."""
    nodes = map_nodes(subtopics)
    shown = {node_id: node for node_id, node in nodes.items() if node.layer is None or node.layer.value in visible_layers}
    relations = [
        (relation, is_own) for relation, is_own in _all_relations(own, subtopics)
        if (is_own or relation.kind.value in visible_kinds) and relation.source in shown and relation.target in shown
    ]
    neighbours = _neighbours(selected, relations)
    elements = [_node_element(node, neighbours, selected, positions or {}) for node in shown.values()]
    elements += _structure_edges(shown)
    elements += [
        _relation_edge(index, relation, is_own, nodes, selected) for index, (relation, is_own) in enumerate(relations)
    ]
    return elements


def positions_of(elements: Optional[Sequence[Mapping[str, object]]]) -> Dict[str, Position]:
    """Node positions as Cytoscape reports them after the user dragged something."""
    found = {}
    for element in elements or []:
        data = element.get("data") or {}
        position = element.get("position")
        if isinstance(data, Mapping) and "source" not in data and isinstance(position, Mapping):
            found[str(data.get("id"))] = {"x": float(position["x"]), "y": float(position["y"])}
    return found


def describe_hover(data: Optional[Mapping[str, object]]) -> str:
    """One line under the map for the node or arrow under the pointer."""
    if not data:
        return ""
    return str(data.get("hover", ""))


def wrap_label(text: str, width: int = LABEL_WIDTH) -> str:
    lines: List[str] = []
    for word in text.split():
        if lines and len(lines[-1]) + 1 + len(word) <= width:
            lines[-1] += f" {word}"
        else:
            lines.append(word)
    return "\n".join(lines)


def _all_relations(own: Sequence[Relation], subtopics: Sequence[Subtopic]) -> List[Tuple[Relation, bool]]:
    return (
        [(relation, False) for relation in RELATIONS]
        + [(relation, True) for relation in subtopic_relations(subtopics)]
        + [(relation, True) for relation in own]
    )


def _subtopic_nodes(
    subtopics: Sequence[Subtopic], nodes: Mapping[str, MapNode], page_angles: Mapping[str, float],
) -> Dict[str, MapNode]:
    """Subtopics of the same page fan out alternately to both sides of it."""
    placed: Dict[str, int] = {}
    subtopic_nodes = {}
    for subtopic in subtopics:
        anchor = nodes[subtopic.page_ids[0]]
        count = placed.get(anchor.node_id, 0)
        placed[anchor.node_id] = count + 1
        offset = SUBTOPIC_SPREAD_DEGREES * ((count + 1) // 2) * (1 if count % 2 else -1)
        angle = page_angles[anchor.node_id] + math.radians(offset)
        note = subtopic.note[:HOVER_NOTE_LENGTH] + ("…" if len(subtopic.note) > HOVER_NOTE_LENGTH else "")
        subtopic_nodes[subtopic.subtopic_id] = MapNode(
            subtopic.subtopic_id, subtopic.title, note or "vlastní podtéma", "subtopic",
            SUBTOPIC_RADIUS * math.cos(angle), SUBTOPIC_RADIUS * math.sin(angle), anchor.color, anchor.layer,
            label=subtopic.title,
        )
    return subtopic_nodes


def _layer_node_id(layer: Layer) -> str:
    return f"vrstva-{layer.value}"


def _pixels(node: MapNode) -> Position:
    return {"x": node.x * PIXELS_PER_UNIT, "y": -node.y * PIXELS_PER_UNIT}


def _label_side(node: MapNode) -> str:
    """Labels of the outer rings point away from the centre, so they do not cover the arrows."""
    if node.kind not in ("page", "subtopic"):
        return "label-bottom"
    radius = math.hypot(node.x, node.y)
    if node.x / radius > LABEL_SIDE_THRESHOLD:
        return "label-right"
    if node.x / radius < -LABEL_SIDE_THRESHOLD:
        return "label-left"
    return "label-top" if node.y > 0 else "label-bottom"


def _neighbours(selected: Optional[str], relations: Sequence[Tuple[Relation, bool]]) -> Optional[set]:
    if selected is None:
        return None
    linked = {selected}
    for relation, _ in relations:
        if selected in (relation.source, relation.target):
            linked |= {relation.source, relation.target}
    return linked


def _node_element(
    node: MapNode, neighbours: Optional[set], selected: Optional[str], positions: Mapping[str, Mapping[str, float]],
) -> dict:
    classes = [node.kind, _label_side(node)]
    if neighbours is not None and node.node_id not in neighbours:
        classes.append("faded")
    if node.node_id == selected:
        classes.append("chosen")
    position = positions.get(node.node_id) or _pixels(node)
    return {
        "data": {
            "id": node.node_id, "label": wrap_label(node.label), "title": node.title, "kind": node.kind,
            "color": node.color, "path": node.path or "", "hover": f"{node.title}: {node.description}",
        },
        "position": {"x": float(position["x"]), "y": float(position["y"])},
        "classes": " ".join(classes),
    }


def _structure_edges(shown: Mapping[str, MapNode]) -> List[dict]:
    edges = []
    for node in shown.values():
        if node.kind not in ("layer", "page"):
            continue
        anchor_id = CENTER_ID if node.kind == "layer" else _layer_node_id(node.layer)
        if anchor_id in shown:
            edges.append({
                "data": {"id": f"struktura-{node.node_id}", "source": anchor_id, "target": node.node_id},
                "classes": "structure",
                "selectable": False,
            })
    return edges


def _relation_edge(
    index: int, relation: Relation, is_own: bool, nodes: Mapping[str, MapNode], selected: Optional[str],
) -> dict:
    is_free_connection = is_own and relation.kind != RelationKind.EXPANDS
    classes = ["relation", relation.kind.value]
    if is_free_connection:
        classes.append("own")
    if selected is not None and selected not in (relation.source, relation.target):
        classes.append("faded")
    prefix = "vlastní: " if is_own else ""
    note = f" – {relation.note}" if relation.note else ""
    source, target = nodes[relation.source], nodes[relation.target]
    return {
        "data": {
            "id": f"vztah-{index}", "source": relation.source, "target": relation.target,
            "color": OWN_CONNECTION_COLOR if is_free_connection else kind_info(relation.kind).color,
            "hover": f"{prefix}{source.label} {kind_info(relation.kind).label} {target.label}{note}",
        },
        "classes": " ".join(classes),
    }
