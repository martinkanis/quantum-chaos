"""Knowledge map: nodes with positions, typed relations, user connections and the Plotly figure that draws them."""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from typing import Collection, Dict, List, Mapping, Optional, Sequence, Tuple

import plotly.graph_objects as go

from ui import ids
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
from ui.navigation import ACADEMY_PATH
from ui.topic_catalog import RESEARCH_TOPICS, PageEntry

CENTER_ID = "stred"
HUB_RADIUS = 1.7
PAGE_RADIUS = 3.4
MIN_SECTOR_PAGES = 2
"""A layer with a single page still gets the room of two, so its hub does not sit right next to a neighbour."""
LABEL_WIDTH = 16
LABEL_SIDE_THRESHOLD = 0.35
NODE_SIZES = {"center": 46, "layer": 30, "page": 18}
CENTER_COLOR = "#1c2330"
STRUCTURE_COLOR = "#dde2ea"
OWN_CONNECTION_COLOR = "#1c2330"
FADED_OPACITY = 0.2
ARROW_STANDOFF = 12
FIGURE_HEIGHT = 700
X_RANGE = 6.4
Y_RANGE = 4.6
MAX_NOTE_LENGTH = 200

logger = logging.getLogger(__name__)

ACADEMY_ENTRY = PageEntry(
    ids.ACADEMY_PAGE, "Quantum Academy", ACADEMY_PATH,
    "Kurzy, videa, blogy a platformy (Classiq, CUDA-Q, Quandela) pro samostudium kvantového počítání.",
)


class KnowledgeMapError(ValueError):
    """Raised when a user connection between two pages cannot be added."""


@dataclass(frozen=True)
class MapNode:
    node_id: str
    title: str
    description: str
    kind: str
    """"center", "layer" or "page"."""
    x: float
    y: float
    color: str
    layer: Optional[Layer] = None
    path: Optional[str] = None
    label: str = ""
    """Short text drawn next to the node; the title is shown on hover."""


@dataclass(frozen=True)
class NodeRelation:
    direction: str
    """"out" when the node is the source, "in" when it is the target."""
    kind_label: str
    other: MapNode
    note: str
    is_own: bool


def page_entries() -> Dict[str, PageEntry]:
    entries = {page.page_id: page for topic in RESEARCH_TOPICS for page in topic.pages}
    entries[ACADEMY_ENTRY.page_id] = ACADEMY_ENTRY
    return entries


def map_nodes() -> Dict[str, MapNode]:
    """The central question in the middle, layer hubs around it and every page on an outer ring.

    Each layer owns a slice of the ring proportional to its number of pages; its hub sits in the middle of the
    slice, so the lines from a hub to its pages fan out without crossing other layers.
    """
    entries = page_entries()
    nodes = {
        CENTER_ID: MapNode(
            CENTER_ID, CENTRAL_QUESTION_SHORT, CENTRAL_QUESTION, "center", 0.0, 0.0, CENTER_COLOR,
            label=CENTRAL_QUESTION_SHORT,
        ),
    }
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
            entry = entries[page_id]
            nodes[page_id] = MapNode(
                page_id, entry.title, entry.description, "page",
                PAGE_RADIUS * math.cos(angle), PAGE_RADIUS * math.sin(angle), info.color, info.layer, entry.path,
                MAP_LABELS.get(page_id, entry.title),
            )
        sector_start -= sector
    return nodes


def page_options() -> List[Dict[str, str]]:
    nodes = map_nodes()
    return [
        {"label": f"{nodes[page_id].label} ({info.title})", "value": page_id}
        for info in LAYERS for page_id in info.page_ids
    ]


def kind_info(kind: RelationKind) -> RelationKindInfo:
    return next(info for info in RELATION_KINDS if info.kind == kind)


def parse_connections(stored: Optional[Sequence[Mapping[str, str]]]) -> List[Relation]:
    """Connections saved in the browser; malformed entries or ones pointing to removed pages are skipped and logged."""
    nodes = map_nodes()
    relations = []
    for item in stored or []:
        try:
            relation = Relation(item["source"], RelationKind(item["kind"]), item["target"], item.get("note", ""))
        except (KeyError, ValueError, TypeError) as error:
            logger.warning("Skipping malformed knowledge map connection %r: %s", item, error)
            continue
        if relation.source in nodes and relation.target in nodes:
            relations.append(relation)
        else:
            logger.warning("Skipping knowledge map connection to an unknown page: %r", item)
    return relations


def add_connection(
    stored: Optional[Sequence[Mapping[str, str]]], source: Optional[str], kind: Optional[str],
    target: Optional[str], note: Optional[str],
) -> List[Dict[str, str]]:
    nodes = map_nodes()
    if not source or not target or not kind:
        raise KnowledgeMapError("Vyber obě stránky i typ vztahu.")
    if source == target:
        raise KnowledgeMapError("Stránku nejde propojit samu se sebou – vyber dvě různé.")
    if source not in nodes or target not in nodes:
        raise KnowledgeMapError("Jedna z vybraných stránek už v mapě není, načti stránku znovu.")
    clean_note = (note or "").strip()[:MAX_NOTE_LENGTH]
    existing = [_as_dict(relation) for relation in parse_connections(stored)]
    if any(item["source"] == source and item["target"] == target and item["kind"] == kind for item in existing):
        raise KnowledgeMapError("Takové propojení už máš.")
    return existing + [{"source": source, "kind": RelationKind(kind).value, "target": target, "note": clean_note}]


def remove_connections(stored: Optional[Sequence[Mapping[str, str]]], indices: Collection[int]) -> List[Dict[str, str]]:
    return [_as_dict(relation) for index, relation in enumerate(parse_connections(stored)) if index not in indices]


def connection_label(relation: Relation) -> str:
    nodes = map_nodes()
    note = f" – {relation.note}" if relation.note else ""
    return f"{nodes[relation.source].label} {kind_info(relation.kind).label} {nodes[relation.target].label}{note}"


def relations_of(node_id: str, own: Sequence[Relation]) -> List[NodeRelation]:
    nodes = map_nodes()
    found = []
    for relation, is_own in [(relation, False) for relation in RELATIONS] + [(relation, True) for relation in own]:
        if node_id not in (relation.source, relation.target):
            continue
        direction = "out" if relation.source == node_id else "in"
        other_id = relation.target if direction == "out" else relation.source
        found.append(NodeRelation(direction, kind_info(relation.kind).label, nodes[other_id], relation.note, is_own))
    return found


def build_figure(
    visible_layers: Collection[str], visible_kinds: Collection[str], own: Sequence[Relation],
    selected: Optional[str] = None,
) -> go.Figure:
    nodes = map_nodes()
    shown = {node_id: node for node_id, node in nodes.items() if node.layer is None or node.layer.value in visible_layers}
    relations = [
        (relation, False) for relation in RELATIONS
        if relation.kind.value in visible_kinds and relation.source in shown and relation.target in shown
    ] + [(relation, True) for relation in own if relation.source in shown and relation.target in shown]
    neighbours = _neighbours(selected, relations)

    figure = go.Figure()
    figure.add_trace(_structure_trace(shown))
    for info in RELATION_KINDS:
        if info.kind.value in visible_kinds:
            figure.add_trace(_legend_line(info.label, info.color))
    if own:
        figure.add_trace(_legend_line("vlastní propojení", OWN_CONNECTION_COLOR, dash="dash"))
    for relation, is_own in relations:
        figure.add_annotation(_arrow(nodes[relation.source], nodes[relation.target], relation, is_own, selected))
    figure.add_trace(_relation_hover_trace(relations, nodes))
    figure.add_trace(_node_trace([node for node in shown.values() if node.kind != "page"], neighbours, selected))
    for info in LAYERS:
        layer_pages = [node for node in shown.values() if node.kind == "page" and node.layer == info.layer]
        if layer_pages:
            figure.add_trace(_node_trace(layer_pages, neighbours, selected, name=info.title))
    figure.update_layout(
        height=FIGURE_HEIGHT, margin=dict(l=10, r=10, t=10, b=10), dragmode="pan", hovermode="closest",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="top", y=-0.02, xanchor="center", x=0.5),
        xaxis=dict(visible=False, range=[-X_RANGE, X_RANGE]),
        yaxis=dict(visible=False, range=[-Y_RANGE, Y_RANGE], scaleanchor="x"),
    )
    return figure


def wrap_label(text: str, width: int = LABEL_WIDTH) -> str:
    lines: List[str] = []
    for word in text.split():
        if lines and len(lines[-1]) + 1 + len(word) <= width:
            lines[-1] += f" {word}"
        else:
            lines.append(word)
    return "<br>".join(lines)


def _layer_node_id(layer: Layer) -> str:
    return f"vrstva-{layer.value}"


def _text_position(node: MapNode) -> str:
    """Labels of the outer ring point away from the centre, so they do not cover the arrows."""
    if node.kind != "page":
        return "bottom center"
    radius = math.hypot(node.x, node.y)
    if node.x / radius > LABEL_SIDE_THRESHOLD:
        return "middle right"
    if node.x / radius < -LABEL_SIDE_THRESHOLD:
        return "middle left"
    return "top center" if node.y > 0 else "bottom center"


def _neighbours(selected: Optional[str], relations: Sequence[Tuple[Relation, bool]]) -> Optional[set]:
    if selected is None:
        return None
    linked = {selected}
    for relation, _ in relations:
        if selected in (relation.source, relation.target):
            linked |= {relation.source, relation.target}
    return linked


def _structure_trace(shown: Mapping[str, MapNode]) -> go.Scatter:
    xs: List[Optional[float]] = []
    ys: List[Optional[float]] = []
    for node in shown.values():
        if node.kind == "center":
            continue
        anchor = shown[CENTER_ID] if node.kind == "layer" else shown.get(_layer_node_id(node.layer))
        if anchor is None:
            continue
        xs += [anchor.x, node.x, None]
        ys += [anchor.y, node.y, None]
    return go.Scatter(
        x=xs, y=ys, mode="lines", line=dict(color=STRUCTURE_COLOR, width=2), hoverinfo="skip", showlegend=False,
    )


def _legend_line(name: str, color: str, dash: str = "solid") -> go.Scatter:
    return go.Scatter(x=[None], y=[None], mode="lines", line=dict(color=color, width=3, dash=dash), name=name)


def _arrow(source: MapNode, target: MapNode, relation: Relation, is_own: bool, selected: Optional[str]) -> dict:
    involved = selected is None or selected in (relation.source, relation.target)
    return dict(
        x=target.x, y=target.y, ax=source.x, ay=source.y, xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=3, arrowsize=1.2, arrowwidth=2.6 if is_own else 1.8,
        arrowcolor=OWN_CONNECTION_COLOR if is_own else kind_info(relation.kind).color,
        standoff=ARROW_STANDOFF, startstandoff=ARROW_STANDOFF, text="",
        opacity=1.0 if involved else FADED_OPACITY,
    )


def _relation_hover_trace(relations: Sequence[Tuple[Relation, bool]], nodes: Mapping[str, MapNode]) -> go.Scatter:
    """Invisible points in the middle of each arrow, so hovering an arrow says what the relation means."""
    texts = []
    xs, ys = [], []
    for relation, is_own in relations:
        source, target = nodes[relation.source], nodes[relation.target]
        xs.append((source.x + target.x) / 2)
        ys.append((source.y + target.y) / 2)
        prefix = "vlastní: " if is_own else ""
        note = f"<br>{relation.note}" if relation.note else ""
        texts.append(f"{prefix}{source.label} <b>{kind_info(relation.kind).label}</b> {target.label}{note}")
    return go.Scatter(
        x=xs, y=ys, mode="markers", marker=dict(size=14, opacity=0), text=texts,
        hovertemplate="%{text}<extra></extra>", showlegend=False,
    )


def _node_trace(
    nodes: Sequence[MapNode], neighbours: Optional[set], selected: Optional[str], name: Optional[str] = None,
) -> go.Scatter:
    return go.Scatter(
        x=[node.x for node in nodes], y=[node.y for node in nodes], mode="markers+text", name=name,
        showlegend=name is not None,
        text=[wrap_label(node.label) for node in nodes], textposition=[_text_position(node) for node in nodes],
        textfont=dict(size=11, color=CENTER_COLOR),
        customdata=[node.node_id for node in nodes],
        hovertext=[f"<b>{node.title}</b><br>{wrap_label(node.description, 50)}" for node in nodes],
        hovertemplate="%{hovertext}<extra></extra>",
        marker=dict(
            size=[NODE_SIZES[node.kind] for node in nodes], color=[node.color for node in nodes],
            opacity=[1.0 if neighbours is None or node.node_id in neighbours else FADED_OPACITY for node in nodes],
            line=dict(color=CENTER_COLOR, width=[3 if node.node_id == selected else 0 for node in nodes]),
        ),
    )


def _as_dict(relation: Relation) -> Dict[str, str]:
    return {"source": relation.source, "kind": relation.kind.value, "target": relation.target, "note": relation.note}
