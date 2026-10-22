"""Knowledge map page: the central question, the layers of the app as a mind map and the user's own connections."""

from __future__ import annotations

from typing import List, Optional, Sequence

from dash import dcc, html

from ui import ids
from ui.knowledge_map import (
    CENTER_ID,
    NodeRelation,
    build_figure,
    map_nodes,
    page_options,
    relations_of,
)
from ui.knowledge_map_content import (
    CENTRAL_QUESTION,
    INTRO,
    LAYERS,
    OWN_CONNECTIONS_HINT,
    RELATION_KINDS,
    TITLE,
    Relation,
)
from ui.navigation import HIDDEN

ALL_LAYERS = [info.layer.value for info in LAYERS]
ALL_KINDS = [info.kind.value for info in RELATION_KINDS]
SELECTION_HINT = "Klikni na uzel v mapě: ukáže se, co stránka obsahuje a s čím souvisí."


def build_knowledge_map_page() -> html.Div:
    return html.Div(
        id=ids.KNOWLEDGE_MAP_PAGE,
        className="gbs-page knowledge-map-page",
        style=HIDDEN,
        children=[
            html.H1(TITLE),
            html.P(INTRO, className="lead"),
            html.Section(className="card central-question", children=[
                html.H2("Ústřední otázka"),
                html.P(CENTRAL_QUESTION, className="central-question-text"),
            ]),
            _map_card(),
            html.Section(id=ids.KNOWLEDGE_MAP_DETAILS, className="card", children=describe_node(None, [])),
            _connections_card(),
            _layers_card(),
            dcc.Store(id=ids.KNOWLEDGE_MAP_CONNECTIONS, storage_type="local"),
            dcc.Store(id=ids.KNOWLEDGE_MAP_SELECTION),
        ],
    )


def describe_node(node_id: Optional[str], own: Sequence[Relation]) -> List:
    nodes = map_nodes()
    if node_id is None or node_id not in nodes:
        return [html.H2("Souvislosti"), html.P(SELECTION_HINT, className="hint")]
    node = nodes[node_id]
    children: List = [html.H2(node.title), html.P(node.description)]
    if node.path:
        children.append(dcc.Link("Otevřít stránku →", href=node.path, className="primary-link"))
    if node_id == CENTER_ID:
        children.append(html.P("Vrstvy kolem ní jsou popsané níže pod mapou.", className="hint"))
        return children
    if node.kind == "layer":
        layer = next(info for info in LAYERS if info.layer == node.layer)
        children.append(html.Ul([
            html.Li(dcc.Link(nodes[page_id].title, href=nodes[page_id].path)) for page_id in layer.page_ids
        ]))
        return children
    relations = relations_of(node_id, own)
    children.append(html.H3("Souvislosti"))
    if not relations:
        children.append(html.P("Zatím žádné – přidej vlastní propojení níže.", className="hint"))
        return children
    children.append(html.Ul([_relation_item(relation) for relation in relations]))
    return children


def _relation_item(relation: NodeRelation) -> html.Li:
    other = dcc.Link(relation.other.title, href=relation.other.path) if relation.other.path else relation.other.title
    sentence = (
        ["tato stránka ", html.Strong(relation.kind_label), " ", other]
        if relation.direction == "out"
        else [other, " ", html.Strong(relation.kind_label), " tuto stránku"]
    )
    note = [html.Span(f" – {relation.note}", className="hint")] if relation.note else []
    own = [html.Span(" (vlastní)", className="hint")] if relation.is_own else []
    return html.Li(sentence + note + own)


def _map_card() -> html.Section:
    return html.Section(className="card", children=[
        html.Div(className="map-filters", children=[
            html.Div([
                html.Strong("Vrstvy"),
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
            html.Button("Zrušit výběr uzlu", id=ids.KNOWLEDGE_MAP_SHOW_ALL, className="secondary-button"),
        ]),
        html.Div(className="map-scroll", children=dcc.Graph(
            id=ids.KNOWLEDGE_MAP_GRAPH, figure=build_figure(ALL_LAYERS, ALL_KINDS, []),
            config={"displayModeBar": False, "scrollZoom": True, "responsive": True},
        )),
        html.P(
            "Šipka vede od stránky, která něco dělá, ke stránce, které se to týká; najetím na šipku uvidíš, co vztah "
            "znamená. Mapu jde posouvat tažením a přibližovat kolečkem.",
            className="hint small",
        ),
    ])


def _connections_card() -> html.Section:
    return html.Section(className="card", children=[
        html.H2("Vlastní propojení"),
        html.P(OWN_CONNECTIONS_HINT, className="hint"),
        html.Div(className="connection-form", children=[
            dcc.Dropdown(id=ids.KNOWLEDGE_MAP_SOURCE, options=page_options(), placeholder="Stránka…"),
            dcc.Dropdown(
                id=ids.KNOWLEDGE_MAP_KIND, placeholder="vztah…", clearable=False,
                options=[{"label": info.label, "value": info.kind.value} for info in RELATION_KINDS],
            ),
            dcc.Dropdown(id=ids.KNOWLEDGE_MAP_TARGET, options=page_options(), placeholder="…se stránkou"),
            dcc.Input(
                id=ids.KNOWLEDGE_MAP_NOTE, type="text", placeholder="Poznámka (nepovinná)", debounce=True,
                maxLength=200,
            ),
            html.Button("Přidat propojení", id=ids.KNOWLEDGE_MAP_ADD, className="primary-button"),
        ]),
        html.Div(id=ids.KNOWLEDGE_MAP_ERROR, className="error-message"),
        dcc.Checklist(id=ids.KNOWLEDGE_MAP_OWN_LIST, options=[], value=[], className="own-connections"),
        html.Button("Odebrat vybraná propojení", id=ids.KNOWLEDGE_MAP_REMOVE, className="secondary-button"),
    ])


def layer_overview() -> html.Div:
    """The layers as a compact list of links; shared by the map page and the topics page."""
    nodes = map_nodes()
    return html.Div(className="layer-overview", children=[
        html.Div(className="map-layer", children=[
            html.H3([html.Span(className="layer-dot", style={"background": info.color}), info.title]),
            html.P(info.role, className="hint small"),
            html.Ul([html.Li(dcc.Link(nodes[page_id].title, href=nodes[page_id].path)) for page_id in info.page_ids]),
        ])
        for info in LAYERS
    ])


def _layers_card() -> html.Section:
    return html.Section(className="card", children=[html.H2("Vrstvy v textu"), layer_overview()])
