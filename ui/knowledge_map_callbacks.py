"""Callbacks of the knowledge map: filters, clicks on nodes and the user's own notes stored in the browser."""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

import plotly.graph_objects as go
from dash import Dash, Input, Output, State, dcc, html, no_update

from ui import ids
from ui.knowledge_map import build_figure, connection_label, map_nodes, node_options, page_ids
from ui.knowledge_map_notes import (
    BACKUP_FILENAME,
    KnowledgeMapError,
    Subtopic,
    add_connection,
    add_subtopic,
    export_backup,
    import_backup,
    parse_connections,
    parse_subtopics,
    remove_connections,
    remove_subtopics,
)
from ui.knowledge_map_page import ClickMode, describe_node

Stored = Optional[List[Dict[str, object]]]
IMPORT_SUCCESS = "Záloha je nahraná: {subtopics} podtémat a {connections} propojení."


def register_knowledge_map_callbacks(app: Dash) -> None:
    app.callback(
        Output(ids.KNOWLEDGE_MAP_GRAPH, "figure"),
        Input(ids.KNOWLEDGE_MAP_LAYER_FILTER, "value"),
        Input(ids.KNOWLEDGE_MAP_KIND_FILTER, "value"),
        Input(ids.KNOWLEDGE_MAP_CONNECTIONS, "data"),
        Input(ids.KNOWLEDGE_MAP_SUBTOPICS, "data"),
        Input(ids.KNOWLEDGE_MAP_SELECTION, "data"),
    )(update_figure)
    app.callback(
        Output(ids.URL, "pathname"),
        Output(ids.KNOWLEDGE_MAP_SELECTION, "data"),
        Input(ids.KNOWLEDGE_MAP_GRAPH, "clickData"),
        State(ids.KNOWLEDGE_MAP_CLICK_MODE, "value"),
        State(ids.KNOWLEDGE_MAP_SUBTOPICS, "data"),
        prevent_initial_call=True,
    )(click_node)
    app.callback(
        Output(ids.KNOWLEDGE_MAP_SELECTION, "data", allow_duplicate=True),
        Input(ids.KNOWLEDGE_MAP_SHOW_ALL, "n_clicks"),
        prevent_initial_call=True,
    )(clear_selection)
    app.callback(
        Output(ids.KNOWLEDGE_MAP_DETAILS, "children"),
        Input(ids.KNOWLEDGE_MAP_SELECTION, "data"),
        Input(ids.KNOWLEDGE_MAP_CONNECTIONS, "data"),
        Input(ids.KNOWLEDGE_MAP_SUBTOPICS, "data"),
    )(update_details)
    _register_subtopic_callbacks(app)
    _register_connection_callbacks(app)
    _register_backup_callbacks(app)


def _register_subtopic_callbacks(app: Dash) -> None:
    app.callback(
        Output(ids.KNOWLEDGE_MAP_SUBTOPICS, "data"),
        Output(ids.KNOWLEDGE_MAP_SUBTOPIC_ERROR, "children"),
        Output(ids.KNOWLEDGE_MAP_SUBTOPIC_TITLE, "value"),
        Output(ids.KNOWLEDGE_MAP_SUBTOPIC_NOTE, "value"),
        Output(ids.KNOWLEDGE_MAP_SUBTOPIC_PAGES, "value"),
        Input(ids.KNOWLEDGE_MAP_ADD_SUBTOPIC, "n_clicks"),
        State(ids.KNOWLEDGE_MAP_SUBTOPIC_TITLE, "value"),
        State(ids.KNOWLEDGE_MAP_SUBTOPIC_NOTE, "value"),
        State(ids.KNOWLEDGE_MAP_SUBTOPIC_PAGES, "value"),
        State(ids.KNOWLEDGE_MAP_SUBTOPICS, "data"),
        prevent_initial_call=True,
    )(add_own_subtopic)
    app.callback(
        Output(ids.KNOWLEDGE_MAP_SUBTOPICS, "data", allow_duplicate=True),
        Output(ids.KNOWLEDGE_MAP_CONNECTIONS, "data", allow_duplicate=True),
        Input(ids.KNOWLEDGE_MAP_REMOVE_SUBTOPICS, "n_clicks"),
        State(ids.KNOWLEDGE_MAP_SUBTOPIC_LIST, "value"),
        State(ids.KNOWLEDGE_MAP_SUBTOPICS, "data"),
        State(ids.KNOWLEDGE_MAP_CONNECTIONS, "data"),
        prevent_initial_call=True,
    )(remove_own_subtopics)
    app.callback(
        Output(ids.KNOWLEDGE_MAP_SUBTOPIC_LIST, "options"),
        Output(ids.KNOWLEDGE_MAP_SUBTOPIC_LIST, "value"),
        Output(ids.KNOWLEDGE_MAP_SOURCE, "options"),
        Output(ids.KNOWLEDGE_MAP_TARGET, "options"),
        Input(ids.KNOWLEDGE_MAP_SUBTOPICS, "data"),
    )(list_own_subtopics)


def _register_connection_callbacks(app: Dash) -> None:
    app.callback(
        Output(ids.KNOWLEDGE_MAP_CONNECTIONS, "data"),
        Output(ids.KNOWLEDGE_MAP_ERROR, "children"),
        Input(ids.KNOWLEDGE_MAP_ADD, "n_clicks"),
        State(ids.KNOWLEDGE_MAP_SOURCE, "value"),
        State(ids.KNOWLEDGE_MAP_KIND, "value"),
        State(ids.KNOWLEDGE_MAP_TARGET, "value"),
        State(ids.KNOWLEDGE_MAP_NOTE, "value"),
        State(ids.KNOWLEDGE_MAP_CONNECTIONS, "data"),
        State(ids.KNOWLEDGE_MAP_SUBTOPICS, "data"),
        prevent_initial_call=True,
    )(add_own_connection)
    app.callback(
        Output(ids.KNOWLEDGE_MAP_CONNECTIONS, "data", allow_duplicate=True),
        Input(ids.KNOWLEDGE_MAP_REMOVE, "n_clicks"),
        State(ids.KNOWLEDGE_MAP_OWN_LIST, "value"),
        State(ids.KNOWLEDGE_MAP_CONNECTIONS, "data"),
        State(ids.KNOWLEDGE_MAP_SUBTOPICS, "data"),
        prevent_initial_call=True,
    )(remove_own_connections)
    app.callback(
        Output(ids.KNOWLEDGE_MAP_OWN_LIST, "options"),
        Output(ids.KNOWLEDGE_MAP_OWN_LIST, "value"),
        Input(ids.KNOWLEDGE_MAP_CONNECTIONS, "data"),
        Input(ids.KNOWLEDGE_MAP_SUBTOPICS, "data"),
    )(list_own_connections)


def _register_backup_callbacks(app: Dash) -> None:
    app.callback(
        Output(ids.KNOWLEDGE_MAP_DOWNLOAD, "data"),
        Input(ids.KNOWLEDGE_MAP_EXPORT, "n_clicks"),
        State(ids.KNOWLEDGE_MAP_SUBTOPICS, "data"),
        State(ids.KNOWLEDGE_MAP_CONNECTIONS, "data"),
        prevent_initial_call=True,
    )(download_backup)
    app.callback(
        Output(ids.KNOWLEDGE_MAP_SUBTOPICS, "data", allow_duplicate=True),
        Output(ids.KNOWLEDGE_MAP_CONNECTIONS, "data", allow_duplicate=True),
        Output(ids.KNOWLEDGE_MAP_IMPORT_MESSAGE, "children"),
        Input(ids.KNOWLEDGE_MAP_IMPORT, "contents"),
        State(ids.KNOWLEDGE_MAP_SUBTOPICS, "data"),
        State(ids.KNOWLEDGE_MAP_CONNECTIONS, "data"),
        prevent_initial_call=True,
    )(upload_backup)


def update_figure(
    layers: Optional[Sequence[str]], kinds: Optional[Sequence[str]], stored_connections: Stored,
    stored_subtopics: Stored, selected: Optional[str],
) -> go.Figure:
    subtopics = _subtopics(stored_subtopics)
    return build_figure(layers or [], kinds or [], _connections(stored_connections, subtopics), subtopics, selected)


def click_node(click_data: Optional[dict], mode: Optional[str], stored_subtopics: Stored) -> Tuple[object, object]:
    """A click on a page opens it (or selects it in the „show links“ mode); hubs and subtopics are always selected.

    Clicks on arrows (their invisible hover points) carry no node id and change nothing.
    """
    points = (click_data or {}).get("points") or []
    node_id = points[0].get("customdata") if points else None
    node = map_nodes(_subtopics(stored_subtopics)).get(node_id)
    if node is None:
        return no_update, no_update
    if node.path and mode == ClickMode.OPEN_PAGE.value:
        return node.path, no_update
    return no_update, node.node_id


def clear_selection(_clicks: Optional[int]) -> Optional[str]:
    return None


def update_details(selected: Optional[str], stored_connections: Stored, stored_subtopics: Stored) -> List:
    subtopics = _subtopics(stored_subtopics)
    return describe_node(selected, _connections(stored_connections, subtopics), subtopics)


def add_own_subtopic(
    _clicks: Optional[int], title: Optional[str], note: Optional[str], pages: Optional[Sequence[str]],
    stored_subtopics: Stored,
) -> Tuple[object, str, object, object, object]:
    try:
        updated = add_subtopic(stored_subtopics, title, note, pages, page_ids())
    except KnowledgeMapError as error:
        return no_update, str(error), no_update, no_update, no_update
    return updated, "", "", "", []


def remove_own_subtopics(
    _clicks: Optional[int], chosen: Optional[Sequence[int]], stored_subtopics: Stored, stored_connections: Stored,
) -> Tuple[List, List]:
    return remove_subtopics(stored_subtopics, stored_connections, set(chosen or []), page_ids())


def list_own_subtopics(stored_subtopics: Stored) -> Tuple[List[Dict[str, object]], List[int], List, List]:
    subtopics = _subtopics(stored_subtopics)
    options = [{"label": f" {subtopic.title}", "value": index} for index, subtopic in enumerate(subtopics)]
    nodes = node_options(subtopics)
    return options, [], nodes, nodes


def add_own_connection(
    _clicks: Optional[int], source: Optional[str], kind: Optional[str], target: Optional[str], note: Optional[str],
    stored_connections: Stored, stored_subtopics: Stored,
) -> Tuple[object, str]:
    node_ids = map_nodes(_subtopics(stored_subtopics))
    try:
        return add_connection(stored_connections, source, kind, target, note, node_ids), ""
    except KnowledgeMapError as error:
        return no_update, str(error)


def remove_own_connections(
    _clicks: Optional[int], chosen: Optional[Sequence[int]], stored_connections: Stored, stored_subtopics: Stored,
) -> List:
    return remove_connections(stored_connections, set(chosen or []), map_nodes(_subtopics(stored_subtopics)))


def list_own_connections(stored_connections: Stored, stored_subtopics: Stored) -> Tuple[List[Dict[str, object]], List[int]]:
    subtopics = _subtopics(stored_subtopics)
    relations = _connections(stored_connections, subtopics)
    options = [
        {"label": f" {connection_label(relation, subtopics)}", "value": index} for index, relation in enumerate(relations)
    ]
    return options, []


def download_backup(_clicks: Optional[int], stored_subtopics: Stored, stored_connections: Stored) -> dict:
    return dcc.send_string(export_backup(stored_subtopics, stored_connections), BACKUP_FILENAME)


def upload_backup(contents: Optional[str], stored_subtopics: Stored, stored_connections: Stored) -> Tuple[object, object, object]:
    try:
        subtopics, connections = import_backup(contents, stored_subtopics, stored_connections, page_ids())
    except KnowledgeMapError as error:
        return no_update, no_update, html.P(str(error), className="error-message")
    message = IMPORT_SUCCESS.format(subtopics=len(subtopics), connections=len(connections))
    return subtopics, connections, html.P(message, className="hint")


def _subtopics(stored_subtopics: Stored) -> List[Subtopic]:
    return parse_subtopics(stored_subtopics, page_ids())


def _connections(stored_connections: Stored, subtopics: Sequence[Subtopic]) -> list:
    return parse_connections(stored_connections, map_nodes(subtopics))
