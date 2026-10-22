"""Building blocks of the knowledge map on the home page: the mind map, node details and the user's own notes."""

from __future__ import annotations

from enum import Enum
from typing import List, Optional, Sequence

from dash import dcc, html

from ui import ids
from ui.knowledge_map import CENTER_ID, NodeRelation, build_figure, map_nodes, node_options, relations_of
from ui.knowledge_map_content import (
    BACKUP_HINT,
    LAYERS,
    OWN_CONNECTIONS_HINT,
    RELATION_KINDS,
    SUBTOPICS_HINT,
    LayerInfo,
    Relation,
)
from ui.knowledge_map_notes import MAX_CONNECTION_NOTE_LENGTH, MAX_SUBTOPIC_NOTE_LENGTH, MAX_TITLE_LENGTH, Subtopic

ALL_LAYERS = [info.layer.value for info in LAYERS]
ALL_KINDS = [info.kind.value for info in RELATION_KINDS]
SELECTION_HINT = "Klikni na skupinu nebo podtéma a ukáže se tu, s čím souvisí."
MAP_CONFIG = {
    "scrollZoom": True,
    "responsive": True,
    "displaylogo": False,
    "displayModeBar": True,
    "modeBarButtons": [["zoomIn2d", "zoomOut2d", "resetScale2d"]],
}
"""Zoom with the wheel, two fingers or the buttons in the corner; drag to move around."""


class ClickMode(str, Enum):
    OPEN_PAGE = "otevrit"
    SHOW_LINKS = "souvislosti"


def map_stores() -> List[dcc.Store]:
    return [
        dcc.Store(id=ids.KNOWLEDGE_MAP_CONNECTIONS, storage_type="local"),
        dcc.Store(id=ids.KNOWLEDGE_MAP_SUBTOPICS, storage_type="local"),
        dcc.Store(id=ids.KNOWLEDGE_MAP_SELECTION),
    ]


def details_card() -> html.Section:
    return html.Section(id=ids.KNOWLEDGE_MAP_DETAILS, className="card", children=describe_node(None, [], []))


def notes_cards() -> List[html.Section]:
    """Own subtopics, own connections and their backup, in the order in which they are usually needed."""
    return [_subtopics_card(), _connections_card(), _backup_card()]


def describe_node(node_id: Optional[str], own: Sequence[Relation], subtopics: Sequence[Subtopic]) -> List:
    nodes = map_nodes(subtopics)
    if node_id is None or node_id not in nodes:
        return [html.H2("Souvislosti"), html.P(SELECTION_HINT, className="hint")]
    node = nodes[node_id]
    children: List = [html.H2(node.title)]
    subtopic = next((item for item in subtopics if item.subtopic_id == node_id), None)
    if subtopic is not None:
        children.append(dcc.Markdown(subtopic.note or "*Bez poznámky.*", mathjax=True))
    else:
        children.append(html.P(node.description))
    if node.path:
        children.append(dcc.Link("Otevřít stránku →", href=node.path, className="primary-link"))
    if node_id == CENTER_ID:
        children.append(html.P("Skupiny kolem ní jsou popsané níže pod mapou.", className="hint"))
        return children
    if node.kind == "layer":
        layer = next(info for info in LAYERS if info.layer == node.layer)
        children.append(html.Ul([
            html.Li(dcc.Link(nodes[page_id].title, href=nodes[page_id].path)) for page_id in layer.page_ids
        ]))
        return children
    relations = relations_of(node_id, own, subtopics)
    children.append(html.H3("Souvislosti"))
    if not relations:
        children.append(html.P("Zatím žádné – přidej vlastní propojení níže.", className="hint"))
        return children
    children.append(html.Ul([_relation_item(relation) for relation in relations]))
    return children


def layer_overview() -> html.Div:
    """The groups as a compact list of links, each with the anchor the breadcrumbs point to."""
    return html.Div(className="layer-overview", children=[_layer_block(info) for info in LAYERS])


def _layer_block(info: LayerInfo) -> html.Div:
    nodes = map_nodes()
    return html.Div(id=info.anchor, className="map-layer", children=[
        html.H3([html.Span(className="layer-dot", style={"background": info.color}), info.title]),
        html.P(info.role, className="hint small"),
        html.Ul([html.Li(dcc.Link(nodes[page_id].title, href=nodes[page_id].path)) for page_id in info.page_ids]),
    ])


def _relation_item(relation: NodeRelation) -> html.Li:
    other = dcc.Link(relation.other.title, href=relation.other.path) if relation.other.path else relation.other.title
    sentence = (
        ["tato položka ", html.Strong(relation.kind_label), " ", other]
        if relation.direction == "out"
        else [other, " ", html.Strong(relation.kind_label), " tuto položku"]
    )
    note = [html.Span(f" – {relation.note}", className="hint")] if relation.note else []
    own = [html.Span(" (vlastní)", className="hint")] if relation.is_own else []
    return html.Li(sentence + note + own)


def map_card() -> html.Section:
    return html.Section(className="card map-card", children=[
        html.Div(className="map-filters", children=[
            html.Div([
                html.Strong("Kliknutí na stránku"),
                dcc.RadioItems(
                    id=ids.KNOWLEDGE_MAP_CLICK_MODE, value=ClickMode.OPEN_PAGE.value, inline=True,
                    options=[
                        {"label": " otevře téma", "value": ClickMode.OPEN_PAGE.value},
                        {"label": " ukáže souvislosti", "value": ClickMode.SHOW_LINKS.value},
                    ],
                ),
            ]),
            html.Div([
                html.Strong("Skupiny"),
                dcc.Checklist(
                    id=ids.KNOWLEDGE_MAP_LAYER_FILTER, value=ALL_LAYERS, inline=True,
                    options=[{"label": f" {info.title}", "value": info.layer.value} for info in LAYERS],
                ),
            ]),
            html.Div([
                html.Strong("Vztahy"),
                dcc.Checklist(
                    id=ids.KNOWLEDGE_MAP_KIND_FILTER, value=ALL_KINDS, inline=True,
                    options=[{"label": f" {info.label}", "value": info.kind.value} for info in RELATION_KINDS],
                ),
            ]),
            html.Button("Zrušit výběr", id=ids.KNOWLEDGE_MAP_SHOW_ALL, className="secondary-button"),
        ]),
        html.Div(className="map-scroll", children=dcc.Graph(
            id=ids.KNOWLEDGE_MAP_GRAPH, figure=build_figure(ALL_LAYERS, ALL_KINDS, []), config=MAP_CONFIG,
            className="map-graph",
        )),
        html.P(
            "Přibližuj kolečkem myši, dvěma prsty nebo tlačítky + a − vpravo nahoře, posouvej tažením; dvojklik vrátí "
            "celou mapu. Najetím na šipku uvidíš, co vztah znamená.",
            className="hint small",
        ),
    ])


def _subtopics_card() -> html.Section:
    return html.Section(className="card", children=[
        html.H2("Vlastní podtémata"),
        html.P(SUBTOPICS_HINT, className="hint"),
        html.Div(className="subtopic-form", children=[
            dcc.Input(
                id=ids.KNOWLEDGE_MAP_SUBTOPIC_TITLE, type="text", placeholder="Název, třeba „Steinovo lemma“",
                maxLength=MAX_TITLE_LENGTH, debounce=True,
            ),
            dcc.Dropdown(
                id=ids.KNOWLEDGE_MAP_SUBTOPIC_PAGES, options=node_options(), multi=True,
                placeholder="Které stránky rozvíjí…",
            ),
            dcc.Textarea(
                id=ids.KNOWLEDGE_MAP_SUBTOPIC_NOTE, maxLength=MAX_SUBTOPIC_NOTE_LENGTH,
                placeholder="Poznámka – co jsem zjistil, odkazy na literaturu; jde psát Markdown i vzorce $x^2$.",
            ),
            html.Button("Přidat podtéma", id=ids.KNOWLEDGE_MAP_ADD_SUBTOPIC, className="primary-button"),
        ]),
        html.Div(id=ids.KNOWLEDGE_MAP_SUBTOPIC_ERROR, className="error-message"),
        dcc.Checklist(id=ids.KNOWLEDGE_MAP_SUBTOPIC_LIST, options=[], value=[], className="own-connections"),
        html.Button("Odebrat vybraná podtémata", id=ids.KNOWLEDGE_MAP_REMOVE_SUBTOPICS, className="secondary-button"),
    ])


def _connections_card() -> html.Section:
    return html.Section(className="card", children=[
        html.H2("Vlastní propojení"),
        html.P(OWN_CONNECTIONS_HINT, className="hint"),
        html.Div(className="connection-form", children=[
            dcc.Dropdown(id=ids.KNOWLEDGE_MAP_SOURCE, options=node_options(), placeholder="Stránka nebo podtéma…"),
            dcc.Dropdown(
                id=ids.KNOWLEDGE_MAP_KIND, placeholder="vztah…", clearable=False,
                options=[{"label": info.label, "value": info.kind.value} for info in RELATION_KINDS],
            ),
            dcc.Dropdown(id=ids.KNOWLEDGE_MAP_TARGET, options=node_options(), placeholder="…se stránkou nebo podtématem"),
            dcc.Input(
                id=ids.KNOWLEDGE_MAP_NOTE, type="text", placeholder="Poznámka (nepovinná)", debounce=True,
                maxLength=MAX_CONNECTION_NOTE_LENGTH,
            ),
            html.Button("Přidat propojení", id=ids.KNOWLEDGE_MAP_ADD, className="primary-button"),
        ]),
        html.Div(id=ids.KNOWLEDGE_MAP_ERROR, className="error-message"),
        dcc.Checklist(id=ids.KNOWLEDGE_MAP_OWN_LIST, options=[], value=[], className="own-connections"),
        html.Button("Odebrat vybraná propojení", id=ids.KNOWLEDGE_MAP_REMOVE, className="secondary-button"),
    ])


def _backup_card() -> html.Section:
    return html.Section(className="card", children=[
        html.H2("Záloha poznámek"),
        html.P(BACKUP_HINT, className="hint"),
        html.Div(className="backup-actions", children=[
            html.Button("Stáhnout zálohu (JSON)", id=ids.KNOWLEDGE_MAP_EXPORT, className="secondary-button"),
            dcc.Upload(
                id=ids.KNOWLEDGE_MAP_IMPORT, accept=".json,application/json", multiple=False,
                children=html.Button("Nahrát zálohu…", className="secondary-button"),
            ),
        ]),
        html.Div(id=ids.KNOWLEDGE_MAP_IMPORT_MESSAGE),
        dcc.Download(id=ids.KNOWLEDGE_MAP_DOWNLOAD),
    ])

