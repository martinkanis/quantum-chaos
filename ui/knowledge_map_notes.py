"""The user's own additions to the knowledge map: subtopics, connections and their backup, all kept in the browser.

Everything arrives from the browser's local storage or an uploaded file, so it is validated here before it reaches
the map; malformed entries are skipped and logged instead of breaking the page.
"""

from __future__ import annotations

import base64
import binascii
import json
import logging
from dataclasses import dataclass
from typing import Collection, Dict, List, Mapping, Optional, Sequence, Tuple

from ui.knowledge_map_content import Relation, RelationKind

SUBTOPIC_PREFIX = "vlastni-"
MAX_TITLE_LENGTH = 80
MAX_SUBTOPIC_NOTE_LENGTH = 2000
MAX_CONNECTION_NOTE_LENGTH = 200
MAX_BACKUP_BYTES = 500_000
BACKUP_VERSION = 1
BACKUP_FILENAME = "mapa-znalosti-zaloha.json"

StoredItems = Optional[Sequence[Mapping[str, object]]]

logger = logging.getLogger(__name__)


class KnowledgeMapError(ValueError):
    """Raised when a subtopic, a connection or a backup cannot be added; the message is shown to the user."""


@dataclass(frozen=True)
class Subtopic:
    subtopic_id: str
    title: str
    note: str
    page_ids: Tuple[str, ...]
    """Pages the subtopic expands; the first one decides where it sits on the map."""


def parse_subtopics(stored: StoredItems, page_ids: Collection[str]) -> List[Subtopic]:
    subtopics = []
    for item in stored or []:
        try:
            subtopic = Subtopic(
                str(item["id"]), str(item["title"]), str(item.get("note", "")),
                tuple(page_id for page_id in item["pages"] if page_id in page_ids),
            )
        except (KeyError, TypeError) as error:
            logger.warning("Skipping malformed knowledge map subtopic %r: %s", item, error)
            continue
        if subtopic.subtopic_id.startswith(SUBTOPIC_PREFIX) and subtopic.title and subtopic.page_ids:
            subtopics.append(subtopic)
        else:
            logger.warning("Skipping knowledge map subtopic without a title or a known page: %r", item)
    return subtopics


def parse_connections(stored: StoredItems, node_ids: Collection[str]) -> List[Relation]:
    relations = []
    for item in stored or []:
        try:
            relation = Relation(
                str(item["source"]), RelationKind(item["kind"]), str(item["target"]), str(item.get("note", "")),
            )
        except (KeyError, ValueError, TypeError) as error:
            logger.warning("Skipping malformed knowledge map connection %r: %s", item, error)
            continue
        if relation.source in node_ids and relation.target in node_ids:
            relations.append(relation)
        else:
            logger.warning("Skipping knowledge map connection to an unknown node: %r", item)
    return relations


def add_subtopic(
    stored: StoredItems, title: Optional[str], note: Optional[str], page_ids: Optional[Sequence[str]],
    known_page_ids: Collection[str],
) -> List[Dict[str, object]]:
    clean_title = (title or "").strip()
    if not clean_title:
        raise KnowledgeMapError("Napiš název podtématu.")
    if len(clean_title) > MAX_TITLE_LENGTH:
        raise KnowledgeMapError(f"Název podtématu může mít nejvýš {MAX_TITLE_LENGTH} znaků.")
    chosen = [page_id for page_id in page_ids or [] if page_id in known_page_ids]
    if not chosen:
        raise KnowledgeMapError("Vyber aspoň jednu stránku, kterou podtéma rozvíjí.")
    existing = [_subtopic_dict(subtopic) for subtopic in parse_subtopics(stored, known_page_ids)]
    if any(item["title"].casefold() == clean_title.casefold() for item in existing):
        raise KnowledgeMapError("Podtéma s tímto názvem už máš – připoj ho k dalším stránkám propojením.")
    new = Subtopic(_next_id(existing), clean_title, (note or "").strip()[:MAX_SUBTOPIC_NOTE_LENGTH], tuple(chosen))
    return existing + [_subtopic_dict(new)]


def remove_subtopics(
    stored_subtopics: StoredItems, stored_connections: StoredItems, indices: Collection[int],
    known_page_ids: Collection[str],
) -> Tuple[List[Dict[str, object]], List[Dict[str, str]]]:
    """Removes the chosen subtopics together with every connection that leads to or from them."""
    subtopics = parse_subtopics(stored_subtopics, known_page_ids)
    removed = {subtopic.subtopic_id for index, subtopic in enumerate(subtopics) if index in indices}
    kept = [subtopic for subtopic in subtopics if subtopic.subtopic_id not in removed]
    node_ids = set(known_page_ids) | {subtopic.subtopic_id for subtopic in kept}
    connections = [
        _connection_dict(relation) for relation in parse_connections(stored_connections, node_ids | removed)
        if relation.source not in removed and relation.target not in removed
    ]
    return [_subtopic_dict(subtopic) for subtopic in kept], connections


def add_connection(
    stored: StoredItems, source: Optional[str], kind: Optional[str], target: Optional[str], note: Optional[str],
    node_ids: Collection[str],
) -> List[Dict[str, str]]:
    if not source or not target or not kind:
        raise KnowledgeMapError("Vyber obě stránky i typ vztahu.")
    if source == target:
        raise KnowledgeMapError("Stránku nejde propojit samu se sebou – vyber dvě různé.")
    if source not in node_ids or target not in node_ids:
        raise KnowledgeMapError("Jedna z vybraných položek už v mapě není, načti stránku znovu.")
    existing = [_connection_dict(relation) for relation in parse_connections(stored, node_ids)]
    if any(item["source"] == source and item["target"] == target and item["kind"] == kind for item in existing):
        raise KnowledgeMapError("Takové propojení už máš.")
    clean_note = (note or "").strip()[:MAX_CONNECTION_NOTE_LENGTH]
    return existing + [{"source": source, "kind": RelationKind(kind).value, "target": target, "note": clean_note}]


def remove_connections(stored: StoredItems, indices: Collection[int], node_ids: Collection[str]) -> List[Dict[str, str]]:
    return [
        _connection_dict(relation) for index, relation in enumerate(parse_connections(stored, node_ids))
        if index not in indices
    ]


def export_backup(stored_subtopics: StoredItems, stored_connections: StoredItems) -> str:
    return json.dumps(
        {"verze": BACKUP_VERSION, "podtemata": list(stored_subtopics or []), "propojeni": list(stored_connections or [])},
        ensure_ascii=False, indent=2,
    )


def import_backup(
    contents: Optional[str], stored_subtopics: StoredItems, stored_connections: StoredItems,
    known_page_ids: Collection[str],
) -> Tuple[List[Dict[str, object]], List[Dict[str, str]]]:
    """Merges an uploaded backup into the current notes; items that already exist are kept only once."""
    backup = _decode_backup(contents)
    merged_subtopics = {
        subtopic.subtopic_id: subtopic
        for subtopic in parse_subtopics(list(stored_subtopics or []) + backup["podtemata"], known_page_ids)
    }
    node_ids = set(known_page_ids) | set(merged_subtopics)
    merged_connections = {
        (relation.source, relation.kind, relation.target): relation
        for relation in parse_connections(list(stored_connections or []) + backup["propojeni"], node_ids)
    }
    return (
        [_subtopic_dict(subtopic) for subtopic in merged_subtopics.values()],
        [_connection_dict(relation) for relation in merged_connections.values()],
    )


def _decode_backup(contents: Optional[str]) -> Dict[str, List]:
    if not contents or "," not in contents:
        raise KnowledgeMapError("Soubor se nepodařilo načíst – nahraj zálohu stáhnutou z této stránky.")
    encoded = contents.split(",", 1)[1]
    if len(encoded) * 3 / 4 > MAX_BACKUP_BYTES:
        raise KnowledgeMapError("Záloha je větší než 500 kB – to není záloha z této stránky.")
    try:
        backup = json.loads(base64.b64decode(encoded).decode("utf-8"))
    except (binascii.Error, UnicodeDecodeError, json.JSONDecodeError) as error:
        logger.warning("Rejected knowledge map backup: %s", error)
        raise KnowledgeMapError("Soubor není platná záloha ve formátu JSON.") from error
    if not isinstance(backup, dict) or backup.get("verze") != BACKUP_VERSION:
        raise KnowledgeMapError("Soubor není záloha mapy znalostí z této aplikace.")
    if not isinstance(backup.get("podtemata"), list) or not isinstance(backup.get("propojeni"), list):
        raise KnowledgeMapError("Záloze chybí seznam podtémat nebo propojení.")
    return backup


def _next_id(existing: Sequence[Mapping[str, object]]) -> str:
    numbers = [int(str(item["id"])[len(SUBTOPIC_PREFIX):]) for item in existing if str(item["id"])[len(SUBTOPIC_PREFIX):].isdigit()]
    return f"{SUBTOPIC_PREFIX}{max(numbers, default=0) + 1}"


def _subtopic_dict(subtopic: Subtopic) -> Dict[str, object]:
    return {"id": subtopic.subtopic_id, "title": subtopic.title, "note": subtopic.note, "pages": list(subtopic.page_ids)}


def _connection_dict(relation: Relation) -> Dict[str, str]:
    return {"source": relation.source, "kind": relation.kind.value, "target": relation.target, "note": relation.note}
