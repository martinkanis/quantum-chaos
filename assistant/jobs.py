"""Agents that expand a selection into a topic page: their state in Postgres (or in memory) and their threads.

The state outlives the process: accepting a topic redeploys the app, and the jobs that were waiting for approval
must still be there afterwards. Agents that were running when the process ended are marked interrupted.
"""

from __future__ import annotations

import logging
import os
import threading
import uuid
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Collection, Dict, List, Mapping, Optional

MAX_RUNNING_AGENTS = 3
DATABASE_URL_ENV = "DATABASE_URL"
INTERRUPTED_MESSAGE = "Aplikace se mezitím restartovala (třeba kvůli nasazení), agent nedoběhl. Spusť ho znovu."
CRASH_MESSAGE = "Agent spadl na neočekávané chybě. Spusť ho znovu."

logger = logging.getLogger(__name__)


class JobStatus(str, Enum):
    RUNNING = "running"
    READY = "ready"
    """Done and waiting for the reader to accept or reject the page."""
    FAILED = "failed"
    INTERRUPTED = "interrupted"
    REJECTED = "rejected"
    DEPLOYING = "deploying"
    """Committed and pushed; the platform is building the new version."""
    DEPLOYED = "deployed"


RETRYABLE = frozenset({JobStatus.FAILED, JobStatus.INTERRUPTED})
DISMISSIBLE = frozenset({JobStatus.FAILED, JobStatus.INTERRUPTED, JobStatus.REJECTED, JobStatus.DEPLOYED})
ACTIVE = frozenset({JobStatus.RUNNING, JobStatus.DEPLOYING})
"""States that change without the reader, so the agents panel keeps polling while a job is in one."""


class JobError(ValueError):
    """A job action that cannot be done; the message says why in Czech."""


@dataclass(frozen=True)
class Job:
    id: str
    status: JobStatus
    created_at: datetime
    updated_at: datetime
    request: Mapping[str, Any]
    """Selection, optional explanation, placement and the titles of existing pages."""
    result: Optional[Mapping[str, Any]] = None
    """The drafted topic page (assistant.topics) once the agent is done."""
    error: str = ""
    commit_url: str = ""
    dismissed: bool = False


Changes = Dict[str, Any]
UPDATABLE = frozenset({"status", "result", "error", "commit_url", "dismissed"})


class MemoryJobStore:
    """Jobs of one process; used locally and in tests when no database is configured."""

    def __init__(self) -> None:
        self._jobs: Dict[str, Job] = {}
        self._lock = threading.Lock()

    def create(self, request: Mapping[str, Any]) -> Job:
        now = _now()
        job = Job(id=uuid.uuid4().hex, status=JobStatus.RUNNING, created_at=now, updated_at=now, request=request)
        with self._lock:
            self._jobs[job.id] = job
        return job

    def get(self, job_id: str) -> Optional[Job]:
        with self._lock:
            return self._jobs.get(job_id)

    def recent(self, limit: int) -> List[Job]:
        with self._lock:
            jobs = [job for job in self._jobs.values() if not job.dismissed]
        return sorted(jobs, key=lambda job: job.created_at, reverse=True)[:limit]

    def update(self, job_id: str, changes: Changes) -> Job:
        changes = _checked(changes)
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                raise JobError("Agent už neexistuje.")
            job = replace(job, updated_at=_now(), **changes)
            self._jobs[job_id] = job
            return job


class PostgresJobStore:
    """Jobs in the table assistant_jobs; the table is created on first use."""

    SCHEMA = """
        CREATE TABLE IF NOT EXISTS assistant_jobs (
            id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL,
            updated_at TIMESTAMPTZ NOT NULL,
            request JSONB NOT NULL,
            result JSONB,
            error TEXT NOT NULL DEFAULT '',
            commit_url TEXT NOT NULL DEFAULT '',
            dismissed BOOLEAN NOT NULL DEFAULT FALSE
        )
    """
    COLUMNS = "id, status, created_at, updated_at, request, result, error, commit_url, dismissed"

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._schema_ready = False

    def create(self, request: Mapping[str, Any]) -> Job:
        from psycopg.types.json import Jsonb

        now = _now()
        job = Job(id=uuid.uuid4().hex, status=JobStatus.RUNNING, created_at=now, updated_at=now, request=request)
        self._execute(
            "INSERT INTO assistant_jobs (id, status, created_at, updated_at, request) VALUES (%s, %s, %s, %s, %s)",
            (job.id, job.status.value, now, now, Jsonb(dict(request))),
        )
        return job

    def get(self, job_id: str) -> Optional[Job]:
        rows = self._execute(f"SELECT {self.COLUMNS} FROM assistant_jobs WHERE id = %s", (job_id,))
        return _job_from_row(rows[0]) if rows else None

    def recent(self, limit: int) -> List[Job]:
        rows = self._execute(
            f"SELECT {self.COLUMNS} FROM assistant_jobs WHERE NOT dismissed ORDER BY created_at DESC LIMIT %s",
            (limit,),
        )
        return [_job_from_row(row) for row in rows]

    def update(self, job_id: str, changes: Changes) -> Job:
        from psycopg.types.json import Jsonb

        values = {
            key: Jsonb(dict(value)) if key == "result" and value is not None else value
            for key, value in _checked(changes).items()
        }
        if "status" in values:
            values["status"] = values["status"].value
        assignments = ", ".join(f"{key} = %s" for key in values)
        rows = self._execute(
            f"UPDATE assistant_jobs SET {assignments}, updated_at = %s WHERE id = %s RETURNING {self.COLUMNS}",
            (*values.values(), _now(), job_id),
        )
        if not rows:
            raise JobError("Agent už neexistuje.")
        return _job_from_row(rows[0])

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
            logger.error("Assistant job database error: %s", error)
            raise JobError("Databáze agentů je teď nedostupná. Zkus to za chvíli znovu.") from error


JobStore = Any
"""MemoryJobStore or PostgresJobStore; both have create, get, recent and update."""


def job_store_from_environment(environment: Mapping[str, str] = os.environ) -> JobStore:
    dsn = environment.get(DATABASE_URL_ENV)
    if dsn:
        return PostgresJobStore(dsn)
    logger.warning("%s is not set: assistant agents are kept in memory and end with the process.", DATABASE_URL_ENV)
    return MemoryJobStore()


def recover_jobs(store: JobStore, published_slugs: Collection[str]) -> None:
    """After a start: running agents died with the old process, and a deploying topic that is now loaded is live."""
    for job in store.recent(200):
        if job.status == JobStatus.RUNNING:
            store.update(job.id, {"status": JobStatus.INTERRUPTED, "error": INTERRUPTED_MESSAGE})
        elif job.status == JobStatus.DEPLOYING and job.result and job.result.get("slug") in published_slugs:
            store.update(job.id, {"status": JobStatus.DEPLOYED})


class AgentRunner:
    """Runs each agent in its own thread; the work function returns the drafted topic as a dict."""

    def __init__(self, store: JobStore, work: Callable[[Job], Mapping[str, Any]]) -> None:
        self.store = store
        self._work = work

    def start(self, request: Mapping[str, Any]) -> Job:
        running = [job for job in self.store.recent(50) if job.status == JobStatus.RUNNING]
        if len(running) >= MAX_RUNNING_AGENTS:
            raise JobError(f"Už běží {len(running)} agenti. Počkej, až některý doběhne.")
        job = self.store.create(request)
        self._launch(job)
        return job

    def retry(self, job_id: str) -> Job:
        job = self.store.get(job_id)
        if job is None or job.status not in RETRYABLE:
            raise JobError("Znovu jde spustit jen agent, který selhal nebo byl přerušen.")
        job = self.store.update(job_id, {"status": JobStatus.RUNNING, "error": "", "result": None})
        self._launch(job)
        return job

    def _launch(self, job: Job) -> None:
        threading.Thread(target=self._run, args=(job,), name=f"agent-{job.id}", daemon=True).start()

    def _run(self, job: Job) -> None:
        try:
            result = self._work(job)
        except ValueError as error:
            self._finish(job.id, {"status": JobStatus.FAILED, "error": str(error)})
        except Exception:
            logger.exception("Assistant agent %s crashed", job.id)
            self._finish(job.id, {"status": JobStatus.FAILED, "error": CRASH_MESSAGE})
        else:
            self._finish(job.id, {"status": JobStatus.READY, "result": result})

    def _finish(self, job_id: str, changes: Changes) -> None:
        try:
            self.store.update(job_id, changes)
        except JobError:
            logger.exception("Assistant agent %s finished, but its state could not be saved", job_id)


def _checked(changes: Changes) -> Changes:
    unknown = set(changes) - UPDATABLE
    if unknown:
        raise ValueError(f"Unknown job fields: {sorted(unknown)}")
    if "status" in changes:
        return {**changes, "status": JobStatus(changes["status"])}
    return dict(changes)


def _job_from_row(row: tuple) -> Job:
    job_id, status, created_at, updated_at, request, result, error, commit_url, dismissed = row
    return Job(
        id=job_id,
        status=JobStatus(status),
        created_at=created_at,
        updated_at=updated_at,
        request=request,
        result=result,
        error=error,
        commit_url=commit_url,
        dismissed=dismissed,
    )


def _now() -> datetime:
    return datetime.now(timezone.utc)
