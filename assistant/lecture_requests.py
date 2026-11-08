"""Requests for notes from a recorded lecture: what the reader entered in the app and how far the worker got.

The app only queues them. Claude Code on the author's computer takes them one by one (scripts/lecture_queue.py and
the skill .claude/skills/zapisky-z-prednasky), writes the notes, commits them to main and reports back; the push
redeploys the app with the new page. The queue lives in Postgres (table lecture_requests), without DATABASE_URL in
memory.
"""

from __future__ import annotations

import logging
import os
import re
import threading
import uuid
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional

from assistant.jobs import DATABASE_URL_ENV, libpq_dsn

MAX_URL_LENGTH = 500
MAX_TOPIC_TITLE_LENGTH = 120
MAX_NOTE_LENGTH = 2000
MAX_MESSAGE_LENGTH = 2000
RECENT_LIMIT = 20
URL_PATTERN = re.compile(r"^https?://[^\s/]+\.[^\s/]+(/\S*)?$")
PAGE_PATH_PATTERN = re.compile(r"^/[a-z0-9/-]*$")
NEW_TOPIC = "nove-tema"
"""Value of the topic choice that asks for a research topic of its own."""
DATABASE_UNAVAILABLE = "Fronta přednášek je teď nedostupná. Zkus to za chvíli znovu."

logger = logging.getLogger(__name__)


class LectureRequestError(ValueError):
    """A request that cannot be queued or a change of state that is not allowed; the message says why in Czech."""


class DetailLevel(str, Enum):
    OVERVIEW = "prehled"
    DETAILED = "podrobne"
    IN_DEPTH = "do-hloubky"


class PresentationStyle(str, Enum):
    NONE = "zadna"
    FRAMES = "snimky"
    """Slides with frames of the recording next to the text."""
    OWN = "vlastni"
    """Slides of our own, text and tables without frames."""


class RequestStatus(str, Enum):
    WAITING = "ceka"
    PROCESSING = "zpracovava-se"
    DONE = "hotovo"
    FAILED = "chyba"


WORKER_STATUSES = frozenset({RequestStatus.PROCESSING, RequestStatus.DONE, RequestStatus.FAILED})
"""States the worker may report; waiting is only the state a request starts in."""


@dataclass(frozen=True)
class LectureRequest:
    id: str
    url: str
    topic_anchor: str
    """An existing research topic, or NEW_TOPIC with new_topic_title."""
    new_topic_title: str
    detail: DetailLevel
    presentation: PresentationStyle
    note: str
    """What the reader wants the notes to focus on."""
    status: RequestStatus
    created_at: datetime
    updated_at: datetime
    message: str = ""
    """The worker's last word: progress, or what went wrong."""
    page_path: str = ""
    """Address of the finished notes in the app."""


def new_request(
    url: Any, topic_anchor: Any, new_topic_title: Any, detail: Any, presentation: Any, note: Any,
) -> LectureRequest:
    """A waiting request from the form; raises LectureRequestError with a message for the reader."""
    now = _now()
    topic_anchor = _text(topic_anchor)
    new_topic_title = _text(new_topic_title)
    if not topic_anchor:
        raise LectureRequestError("Vyber téma, do kterého zápisky patří, nebo „Nové téma“.")
    if topic_anchor == NEW_TOPIC and not new_topic_title:
        raise LectureRequestError("Napiš název nového tématu.")
    if len(new_topic_title) > MAX_TOPIC_TITLE_LENGTH:
        raise LectureRequestError(f"Název tématu je moc dlouhý, povoleno je nejvýš {MAX_TOPIC_TITLE_LENGTH} znaků.")
    note = _text(note)
    if len(note) > MAX_NOTE_LENGTH:
        raise LectureRequestError(f"Poznámka je moc dlouhá ({len(note)} znaků), povoleno je nejvýš {MAX_NOTE_LENGTH}.")
    return LectureRequest(
        id=uuid.uuid4().hex,
        url=_checked_url(url),
        topic_anchor=topic_anchor,
        new_topic_title=new_topic_title if topic_anchor == NEW_TOPIC else "",
        detail=_choice(DetailLevel, detail, "Vyber, jak podrobné mají zápisky být."),
        presentation=_choice(PresentationStyle, presentation, "Vyber, jestli a jakou prezentaci udělat."),
        note=note,
        status=RequestStatus.WAITING,
        created_at=now,
        updated_at=now,
    )


def worker_update(status: Any, message: Any, page_path: Any) -> Dict[str, Any]:
    """Checked changes the worker reports; a finished request must say where its page is."""
    status = _choice(RequestStatus, status, "Neznámý stav požadavku.")
    if status not in WORKER_STATUSES:
        raise LectureRequestError(f"Stav „{status.value}“ pracovník hlásit nemůže.")
    message, page_path = _text(message), _text(page_path)
    if len(message) > MAX_MESSAGE_LENGTH:
        message = message[:MAX_MESSAGE_LENGTH]
    if status is RequestStatus.DONE and not PAGE_PATH_PATTERN.match(page_path):
        raise LectureRequestError("Hotový požadavek musí uvést adresu stránky v aplikaci, třeba /zapisky/nazev.")
    return {"status": status, "message": message, "page_path": page_path}


def request_to_dict(request: LectureRequest) -> Dict[str, Any]:
    """JSON for the worker: everything it needs to write the notes."""
    return {
        "id": request.id,
        "url": request.url,
        "topic_anchor": request.topic_anchor,
        "new_topic_title": request.new_topic_title,
        "detail": request.detail.value,
        "presentation": request.presentation.value,
        "note": request.note,
        "status": request.status.value,
        "created_at": request.created_at.isoformat(),
    }


class MemoryLectureRequestStore:
    """Requests of one process; used locally and in tests when no database is configured."""

    persistent = False

    def __init__(self) -> None:
        self._requests: Dict[str, LectureRequest] = {}
        self._lock = threading.Lock()

    def add(self, request: LectureRequest) -> None:
        with self._lock:
            self._requests[request.id] = request

    def recent(self, limit: int = RECENT_LIMIT) -> List[LectureRequest]:
        with self._lock:
            requests = sorted(self._requests.values(), key=lambda request: request.created_at, reverse=True)
        return requests[:limit]

    def claim_next(self) -> Optional[LectureRequest]:
        """The oldest waiting request, switched to processing so that a second worker does not take it too."""
        with self._lock:
            waiting = [request for request in self._requests.values() if request.status is RequestStatus.WAITING]
            if not waiting:
                return None
            oldest = min(waiting, key=lambda request: request.created_at)
            claimed = replace(oldest, status=RequestStatus.PROCESSING, updated_at=_now())
            self._requests[claimed.id] = claimed
            return claimed

    def update(self, request_id: str, changes: Mapping[str, Any]) -> LectureRequest:
        changes = _checked_changes(changes)
        with self._lock:
            request = self._requests.get(request_id)
            if request is None:
                raise LectureRequestError(f"Požadavek {request_id} ve frontě není.")
            updated = replace(request, updated_at=_now(), **changes)
            self._requests[request_id] = updated
            return updated


class PostgresLectureRequestStore:
    """Requests in the table lecture_requests; the table is created on first use."""

    persistent = True
    COLUMNS = (
        "id, url, topic_anchor, new_topic_title, detail, presentation, note, status, created_at, updated_at, "
        "message, page_path"
    )
    SCHEMA = """
        CREATE TABLE IF NOT EXISTS lecture_requests (
            id TEXT PRIMARY KEY,
            url TEXT NOT NULL,
            topic_anchor TEXT NOT NULL,
            new_topic_title TEXT NOT NULL,
            detail TEXT NOT NULL,
            presentation TEXT NOT NULL,
            note TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL,
            updated_at TIMESTAMPTZ NOT NULL,
            message TEXT NOT NULL,
            page_path TEXT NOT NULL
        )
    """

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._schema_ready = False

    def add(self, request: LectureRequest) -> None:
        self._execute(
            f"INSERT INTO lecture_requests ({self.COLUMNS}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            _row(request),
        )

    def recent(self, limit: int = RECENT_LIMIT) -> List[LectureRequest]:
        rows = self._execute(
            f"SELECT {self.COLUMNS} FROM lecture_requests ORDER BY created_at DESC LIMIT %s", (limit,),
        )
        return [_request_from_row(row) for row in rows]

    def claim_next(self) -> Optional[LectureRequest]:
        rows = self._execute(
            "UPDATE lecture_requests SET status = %s, updated_at = %s WHERE id = ("
            "SELECT id FROM lecture_requests WHERE status = %s ORDER BY created_at LIMIT 1 FOR UPDATE SKIP LOCKED"
            f") RETURNING {self.COLUMNS}",
            (RequestStatus.PROCESSING.value, _now(), RequestStatus.WAITING.value),
        )
        return _request_from_row(rows[0]) if rows else None

    def update(self, request_id: str, changes: Mapping[str, Any]) -> LectureRequest:
        changes = _checked_changes(changes)
        assignments = ", ".join(f"{column} = %s" for column in changes)
        values = tuple(value.value if isinstance(value, Enum) else value for value in changes.values())
        rows = self._execute(
            f"UPDATE lecture_requests SET {assignments}, updated_at = %s WHERE id = %s RETURNING {self.COLUMNS}",
            values + (_now(), request_id),
        )
        if not rows:
            raise LectureRequestError(f"Požadavek {request_id} ve frontě není.")
        return _request_from_row(rows[0])

    def _execute(self, query: str, parameters: tuple) -> List[tuple]:
        import psycopg

        try:
            with psycopg.connect(self._dsn, autocommit=True, connect_timeout=5) as connection:
                if not self._schema_ready:
                    connection.execute(self.SCHEMA)
                    self._schema_ready = True
                cursor = connection.execute(query, parameters)
                return cursor.fetchall() if cursor.description else []
        except psycopg.Error as error:
            logger.error("Lecture request database error: %s", error)
            raise LectureRequestError(DATABASE_UNAVAILABLE) from error


LectureRequestStore = Any
"""MemoryLectureRequestStore or PostgresLectureRequestStore; both have add, recent, claim_next and update."""
UPDATABLE = frozenset({"status", "message", "page_path"})


def lecture_request_store_from_environment(environment: Mapping[str, str] = os.environ) -> LectureRequestStore:
    dsn = environment.get(DATABASE_URL_ENV)
    if dsn:
        return PostgresLectureRequestStore(libpq_dsn(dsn))
    logger.warning("%s is not set: lecture requests are kept in memory and end with the process.", DATABASE_URL_ENV)
    return MemoryLectureRequestStore()


def _checked_changes(changes: Mapping[str, Any]) -> Mapping[str, Any]:
    """Only the worker's fields change; the column names also go into the SQL, so they must be known ones."""
    unknown = set(changes) - UPDATABLE
    if unknown:
        raise ValueError(f"Lecture request fields that cannot change: {sorted(unknown)}")
    return changes


def _checked_url(url: Any) -> str:
    url = _text(url)
    if not url:
        raise LectureRequestError("Vlož odkaz na video přednášky.")
    if len(url) > MAX_URL_LENGTH or not URL_PATTERN.match(url):
        raise LectureRequestError("Odkaz musí být celá adresa videa, která začíná https://, třeba https://youtu.be/…")
    return url


def _choice(enum: Any, value: Any, message: str) -> Any:
    try:
        return enum(value)
    except ValueError as error:
        raise LectureRequestError(message) from error


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _row(request: LectureRequest) -> tuple:
    return (
        request.id, request.url, request.topic_anchor, request.new_topic_title, request.detail.value,
        request.presentation.value, request.note, request.status.value, request.created_at, request.updated_at,
        request.message, request.page_path,
    )


def _request_from_row(row: tuple) -> LectureRequest:
    (request_id, url, topic_anchor, new_topic_title, detail, presentation, note, status, created_at, updated_at,
     message, page_path) = row
    return LectureRequest(
        id=request_id, url=url, topic_anchor=topic_anchor, new_topic_title=new_topic_title,
        detail=DetailLevel(detail), presentation=PresentationStyle(presentation), note=note,
        status=RequestStatus(status), created_at=created_at, updated_at=updated_at, message=message,
        page_path=page_path,
    )


def _now() -> datetime:
    return datetime.now(timezone.utc)
