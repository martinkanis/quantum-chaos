"""Callbacks of the knowledge map: filters, node selection and the user's own connections stored in the browser."""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

import plotly.graph_objects as go
from dash import Dash, Input, Output, State, no_update

from ui import ids
from ui.knowledge_map import (
    KnowledgeMapError,
    add_connection,
    build_figure,
    connection_label,
    map_nodes,
    parse_connections,
    remove_connections,
)
from ui.knowledge_map_page import describe_node

StoredConnections = List[Dict[str, str]]


def register_knowledge_map_callbacks(app: Dash) -> None:
    app.callback(
        Output(ids.KNOWLEDGE_MAP_GRAPH, "figure"),
        Input(ids.KNOWLEDGE_MAP_LAYER_FILTER, "value"),
        Input(ids.KNOWLEDGE_MAP_KIND_FILTER, "value"),
        Input(ids.KNOWLEDGE_MAP_CONNECTIONS, "data"),
        Input(ids.KNOWLEDGE_MAP_SELECTION, "data"),
    )(update_figure)
    app.callback(
        Output(ids.KNOWLEDGE_MAP_SELECTION, "data"),
        Input(ids.KNOWLEDGE_MAP_GRAPH, "clickData"),
        prevent_initial_call=True,
    )(select_node)
    app.callback(
        Output(ids.KNOWLEDGE_MAP_SELECTION, "data", allow_duplicate=True),
        Input(ids.KNOWLEDGE_MAP_SHOW_ALL, "n_clicks"),
        prevent_initial_call=True,
    )(clear_selection)
    app.callback(
        Output(ids.KNOWLEDGE_MAP_DETAILS, "children"),
        Input(ids.KNOWLEDGE_MAP_SELECTION, "data"),
        Input(ids.KNOWLEDGE_MAP_CONNECTIONS, "data"),
    )(update_details)
    app.callback(
        Output(ids.KNOWLEDGE_MAP_CONNECTIONS, "data"),
        Output(ids.KNOWLEDGE_MAP_ERROR, "children"),
        Input(ids.KNOWLEDGE_MAP_ADD, "n_clicks"),
        State(ids.KNOWLEDGE_MAP_SOURCE, "value"),
        State(ids.KNOWLEDGE_MAP_KIND, "value"),
        State(ids.KNOWLEDGE_MAP_TARGET, "value"),
        State(ids.KNOWLEDGE_MAP_NOTE, "value"),
        State(ids.KNOWLEDGE_MAP_CONNECTIONS, "data"),
        prevent_initial_call=True,
    )(add_own_connection)
    app.callback(
        Output(ids.KNOWLEDGE_MAP_CONNECTIONS, "data", allow_duplicate=True),
        Input(ids.KNOWLEDGE_MAP_REMOVE, "n_clicks"),
        State(ids.KNOWLEDGE_MAP_OWN_LIST, "value"),
        State(ids.KNOWLEDGE_MAP_CONNECTIONS, "data"),
        prevent_initial_call=True,
    )(remove_own_connections)
    app.callback(
        Output(ids.KNOWLEDGE_MAP_OWN_LIST, "options"),
        Output(ids.KNOWLEDGE_MAP_OWN_LIST, "value"),
        Input(ids.KNOWLEDGE_MAP_CONNECTIONS, "data"),
    )(list_own_connections)


def update_figure(
    layers: Optional[Sequence[str]], kinds: Optional[Sequence[str]], stored: Optional[StoredConnections],
    selected: Optional[str],
) -> go.Figure:
    return build_figure(layers or [], kinds or [], parse_connections(stored), selected)


def select_node(click_data: Optional[dict]) -> object:
    """Only clicks on nodes select something; clicks on arrows (their hover points) keep the current selection."""
    points = (click_data or {}).get("points") or []
    node_id = points[0].get("customdata") if points else None
    return node_id if node_id in map_nodes() else no_update


def clear_selection(_clicks: Optional[int]) -> Optional[str]:
    return None


def update_details(selected: Optional[str], stored: Optional[StoredConnections]) -> List:
    return describe_node(selected, parse_connections(stored))


def add_own_connection(
    _clicks: Optional[int], source: Optional[str], kind: Optional[str], target: Optional[str], note: Optional[str],
    stored: Optional[StoredConnections],
) -> Tuple[object, str]:
    try:
        return add_connection(stored, source, kind, target, note), ""
    except KnowledgeMapError as error:
        return no_update, str(error)


def remove_own_connections(
    _clicks: Optional[int], chosen: Optional[Sequence[int]], stored: Optional[StoredConnections],
) -> StoredConnections:
    return remove_connections(stored, set(chosen or []))


def list_own_connections(stored: Optional[StoredConnections]) -> Tuple[List[Dict[str, object]], List[int]]:
    relations = parse_connections(stored)
    return [{"label": f" {connection_label(relation)}", "value": index} for index, relation in enumerate(relations)], []
