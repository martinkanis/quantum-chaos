"""Hand edits of page text in Postgres (or in memory) and the copy in the process that the pages are built from.

The app runs one process (a single gunicorn worker), so the copy changes with every save made in it and is read
from the database only once after the start. Without DATABASE_URL the edits live in memory until a restart.
"""

from __future__ import annotations

import logging
import os
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple

from assistant.jobs import DATABASE_URL_ENV, libpq_dsn

MAX_TEXT_LENGTH = 20000
RELOAD_AFTER_FAILURE_SECONDS = 60
EMPTY_TEXT = "Text odstavce nesmí být prázdný. Původní znění vrátí tlačítko „Vrátit původní“."
DATABASE_UNAVAILABLE = "Databáze úprav je teď nedostupná. Zkus to za chvíli znovu."

logger = logging.getLogger(__name__)

Key = Tuple[str, str]
"""Page id and block key."""


class TextEditError(ValueError):
    """An edit that cannot be saved; the message says why in Czech."""


@dataclass(frozen=True)
class TextEdit:
    page_id: str
    block_key: str
    original: str
    """The block as the page builds it, kept for comparison and for moving the edit into the source later."""
    text: str
    updated_at: datetime


def checked_text(text: Any) -> str:
    text = (text if isinstance(text, str) else "").replace("\r\n", "\n").strip()
    if not text:
        raise TextEditError(EMPTY_TEXT)
    if len(text) > MAX_TEXT_LENGTH:
        limit = f"{MAX_TEXT_LENGTH:,}".replace(",", " ")
        raise TextEditError(f"Text je moc dlouhý ({len(text)} znaků). Odstavec může mít nejvýš {limit} znaků.")
    return text


class MemoryTextEditStore:
    """Edits of one process; used locally and in tests when no database is configured."""

    persistent = False

    def __init__(self) -> None:
        self._edits: Dict[Key, TextEdit] = {}
        self._lock = threading.Lock()

    def all(self) -> List[TextEdit]:
        with self._lock:
            return list(self._edits.values())

    def save(self, edit: TextEdit) -> None:
        with self._lock:
            self._edits[(edit.page_id, edit.block_key)] = edit

    def delete(self, page_id: str, block_key: str) -> None:
        with self._lock:
            self._edits.pop((page_id, block_key), None)


class PostgresTextEditStore:
    """Edits in the table text_edits; the table is created on first use."""

    persistent = True
    SCHEMA = """
        CREATE TABLE IF NOT EXISTS text_edits (
            page_id TEXT NOT NULL,
            block_key TEXT NOT NULL,
            original TEXT NOT NULL,
            text TEXT NOT NULL,
            updated_at TIMESTAMPTZ NOT NULL,
            PRIMARY KEY (page_id, block_key)
        )
    """

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._schema_ready = False

    def all(self) -> List[TextEdit]:
        rows = self._execute("SELECT page_id, block_key, original, text, updated_at FROM text_edits", ())
        return [TextEdit(*row) for row in rows]

    def save(self, edit: TextEdit) -> None:
        self._execute(
            "INSERT INTO text_edits (page_id, block_key, original, text, updated_at) VALUES (%s, %s, %s, %s, %s) "
            "ON CONFLICT (page_id, block_key) DO UPDATE "
            "SET original = EXCLUDED.original, text = EXCLUDED.text, updated_at = EXCLUDED.updated_at",
            (edit.page_id, edit.block_key, edit.original, edit.text, edit.updated_at),
        )

    def delete(self, page_id: str, block_key: str) -> None:
        self._execute("DELETE FROM text_edits WHERE page_id = %s AND block_key = %s", (page_id, block_key))

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
            logger.error("Text edit database error: %s", error)
            raise TextEditError(DATABASE_UNAVAILABLE) from error


TextEditStore = Any
"""MemoryTextEditStore or PostgresTextEditStore; both have all, save, delete and persistent."""


def text_edit_store_from_environment(environment: Mapping[str, str] = os.environ) -> TextEditStore:
    dsn = environment.get(DATABASE_URL_ENV)
    if dsn:
        return PostgresTextEditStore(libpq_dsn(dsn))
    logger.warning("%s is not set: text edits are kept in memory and end with the process.", DATABASE_URL_ENV)
    return MemoryTextEditStore()


class TextEdits:
    """The edits the pages are built with; the version grows with every change, so built pages are cached by it."""

    def __init__(self, store: TextEditStore, clock: Callable[[], float] = time.monotonic) -> None:
        self.store = store
        self._clock = clock
        self._edits: Optional[Dict[Key, TextEdit]] = None
        self._version = 0
        self._failed_at: Optional[float] = None
        self._lock = threading.Lock()

    @property
    def persistent(self) -> bool:
        return self.store.persistent

    def version(self) -> int:
        self._loaded()
        return self._version

    def for_page(self, page_id: str) -> Dict[str, str]:
        """Edited text of each edited block of the page, by block key."""
        return {key: edit.text for (edited_page, key), edit in self._loaded().items() if edited_page == page_id}

    def get(self, page_id: str, block_key: str) -> Optional[TextEdit]:
        return self._loaded().get((page_id, block_key))

    def save(self, page_id: str, block_key: str, original: str, text: Any) -> Optional[TextEdit]:
        """Saves the new text; text equal to the original removes the edit instead and returns None."""
        text = checked_text(text)
        if text == original.strip():
            self.revert(page_id, block_key)
            return None
        edit = TextEdit(page_id, block_key, original, text, datetime.now(timezone.utc))
        self.store.save(edit)
        self._changed(page_id, block_key, edit)
        return edit

    def revert(self, page_id: str, block_key: str) -> None:
        self.store.delete(page_id, block_key)
        self._changed(page_id, block_key, None)

    def _changed(self, page_id: str, block_key: str, edit: Optional[TextEdit]) -> None:
        with self._lock:
            if self._edits is not None:
                if edit is None:
                    self._edits.pop((page_id, block_key), None)
                else:
                    self._edits[(page_id, block_key)] = edit
            self._failed_at = None
            self._version += 1

    def _loaded(self) -> Dict[Key, TextEdit]:
        """A copy, so that a save in another thread does not change it while the caller iterates."""
        with self._lock:
            if self._edits is not None:
                return dict(self._edits)
            if self._failed_at is not None and self._clock() - self._failed_at < RELOAD_AFTER_FAILURE_SECONDS:
                return {}
            try:
                edits = self.store.all()
            except TextEditError:
                # The pages are built without the edits meanwhile; the next try comes after a pause.
                self._failed_at = self._clock()
                return {}
            self._edits = {(edit.page_id, edit.block_key): edit for edit in edits}
            self._version += 1
            return dict(self._edits)
