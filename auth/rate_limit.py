"""Lockout after repeated failed logins from one client, kept in memory (the app runs a single worker)."""

from __future__ import annotations

import threading
import time
from typing import Callable, Dict, List

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_SECONDS = 15 * 60


class FailedLoginLimiter:
    def __init__(self, clock: Callable[[], float] = time.monotonic) -> None:
        self._clock = clock
        self._failures: Dict[str, List[float]] = {}
        self._lock = threading.Lock()

    def is_locked(self, client: str) -> bool:
        with self._lock:
            return len(self._recent_failures(client)) >= MAX_FAILED_ATTEMPTS

    def record_failure(self, client: str) -> None:
        with self._lock:
            self._failures[client] = self._recent_failures(client) + [self._clock()]

    def reset(self, client: str) -> None:
        with self._lock:
            self._failures.pop(client, None)

    def _recent_failures(self, client: str) -> List[float]:
        cutoff = self._clock() - LOCKOUT_SECONDS
        return [moment for moment in self._failures.get(client, []) if moment > cutoff]
