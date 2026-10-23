"""Callbacks of the knowledge map: filters, dragging and clicking nodes, and the user's own notes in the browser."""

from __future__ import annotations

import time
from typing import Dict, List, Optional, Sequence, Tuple

from dash import Dash, Input, Output, State, callback_context, dcc, html, no_update

from ui import ids
from ui.knowledge_map import (
    build_elements,
    connection_label,
    describe_hover,
    map_nodes,
    node_options,
    page_ids,
    positions_of,
)
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
from ui.knowledge_map_page import DEFAULT_LAYOUT, ClickMode, describe_node
from ui.navigation import PAGE_BY_PATH

Stored = Optional[List[Dict[str, object]]]
IMPORT_SUCCESS = "Záloha je nahraná: {subtopics} podtémat a {connections} propojení."


def register_knowledge_map_callbacks(app: Dash) -> None:
    app.callback(
        Output(ids.KNOWLEDGE_MAP_GRAPH, "elements"),
        Input(ids.KNOWLEDGE_MAP_LAYER_FILTER, "value"),
        Input(ids.KNOWLEDGE_MAP_KIND_FILTER, "value"),
        Input(ids.KNOWLEDGE_MAP_CONNECTIONS, "data"),
        Input(ids.KNOWLEDGE_MAP_SUBTOPICS, "data"),
        Input(ids.KNOWLEDGE_MAP_SELECTION, "data"),
        Input(ids.KNOWLEDGE_MAP_RESET_LAYOUT, "n_clicks"),
        State(ids.KNOWLEDGE_MAP_POSITIONS, "data"),
    )(update_elements)
    app.callback(
        Output(ids.KNOWLEDGE_MAP_POSITIONS, "data"),
        Input(ids.KNOWLEDGE_MAP_GRAPH, "elements"),
        prevent_initial_call=True,
    )(remember_positions)
    app.callback(
        Output(ids.KNOWLEDGE_MAP_GRAPH, "layout"),
        Input(ids.KNOWLEDGE_MAP_FIT, "n_clicks"),
        Input(ids.KNOWLEDGE_MAP_RESET_LAYOUT, "n_clicks"),
        Input(ids.URL, "pathname"),
        prevent_initial_call=True,
    )(fit_map)
    app.callback(
        Output(ids.KNOWLEDGE_MAP_HOVER, "children"),
        Input(ids.KNOWLEDGE_MAP_GRAPH, "mouseoverNodeData"),
        Input(ids.KNOWLEDGE_MAP_GRAPH, "mouseoverEdgeData"),
        prevent_initial_call=True,
    )(show_hover)
    app.callback(
        Output(ids.URL, "pathname"),
        Output(ids.KNOWLEDGE_MAP_SELECTION, "data"),
        Input(ids.KNOWLEDGE_MAP_GRAPH, "tapNodeData"),
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


def update_elements(
    layers: Optional[Sequence[str]], kinds: Optional[Sequence[str]], stored_connections: Stored,
    stored_subtopics: Stored, selected: Optional[str], _reset_clicks: Optional[int],
    stored_positions: Optional[Dict[str, Dict[str, float]]],
) -> List[dict]:
    """Redraws the map and keeps every node where the user dragged it, unless the original layout was asked for."""
    subtopics = _subtopics(stored_subtopics)
    positions = None if _triggered_by(ids.KNOWLEDGE_MAP_RESET_LAYOUT) else stored_positions
    return build_elements(
        layers or [], kinds or [], _connections(stored_connections, subtopics), subtopics, selected, positions,
    )


def remember_positions(elements: Optional[List[dict]]) -> Dict[str, Dict[str, float]]:
    return positions_of(elements)


def fit_map(fit_clicks: Optional[int], reset_clicks: Optional[int], pathname: Optional[str]) -> object:
    """A changed layout prop makes Cytoscape place the nodes from the elements again and fit the whole map.

    The home page is only hidden while another page is shown, and a map drawn while hidden has no size, so the
    map is fitted again every time the user comes back to it.
    """
    if _triggered_by(ids.URL) and PAGE_BY_PATH.get(pathname or "") != ids.TOPICS_PAGE:
        return no_update
    return {**DEFAULT_LAYOUT, "refit": f"{fit_clicks or 0}-{reset_clicks or 0}-{pathname}-{time.monotonic()}"}


def show_hover(node_data: Optional[dict], edge_data: Optional[dict]) -> str:
    if _triggered_by(ids.KNOWLEDGE_MAP_GRAPH, "mouseoverEdgeData"):
        return describe_hover(edge_data)
    return describe_hover(node_data)


def click_node(node_data: Optional[dict], mode: Optional[str], stored_subtopics: Stored) -> Tuple[object, object]:
    """A click on a page opens it (or selects it in the „show links“ mode); hubs and subtopics are always selected.

    Dragging a node is not a click, so moving pages around never opens them.
    """
    node_id = (node_data or {}).get("id")
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


def _triggered_by(component_id: str, prop: Optional[str] = None) -> bool:
    triggered = callback_context.triggered[0]["prop_id"] if callback_context.triggered else ""
    return triggered.startswith(f"{component_id}.") and (prop is None or triggered.endswith(f".{prop}"))


def _subtopics(stored_subtopics: Stored) -> List[Subtopic]:
    return parse_subtopics(stored_subtopics, page_ids())


def _connections(stored_connections: Stored, subtopics: Sequence[Subtopic]) -> list:
    return parse_connections(stored_connections, map_nodes(subtopics))
