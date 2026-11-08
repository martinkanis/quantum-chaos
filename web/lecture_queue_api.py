"""The worker's side of the lecture queue: take the next request and report how it went.

Claude Code on the author's computer calls these routes (scripts/lecture_queue.py). They sit outside the password
login (auth/login.py) and check a bearer token from LECTURE_WORKER_TOKEN instead; without the variable the queue
cannot be worked and the routes say so.
"""

from __future__ import annotations

import hmac
import logging
import os
from typing import Mapping, Optional

from flask import Flask, Response, jsonify, request

from assistant.lecture_requests import (
    LectureRequestError,
    LectureRequestStore,
    request_to_dict,
    worker_update,
)

API_PREFIX = "/api/prednasky/"
NEXT_PATH = f"{API_PREFIX}dalsi"
TOKEN_ENV = "LECTURE_WORKER_TOKEN"
MIN_TOKEN_LENGTH = 32
"""A shorter token could be guessed; the app then refuses to open the queue to the worker at all."""
NO_TOKEN = f"Fronta přednášek nemá nastavený {TOKEN_ENV} (aspoň {MIN_TOKEN_LENGTH} znaků), pracovník se nepřipojí."
WRONG_TOKEN = "Neplatný token pracovníka."

logger = logging.getLogger(__name__)


def install_lecture_queue_api(
    server: Flask, store: LectureRequestStore, environment: Mapping[str, str] = os.environ,
) -> None:
    token = environment.get(TOKEN_ENV, "")
    if len(token) < MIN_TOKEN_LENGTH:
        logger.warning("%s is missing or too short: the lecture queue cannot be worked.", TOKEN_ENV)
        token = ""

    @server.route(NEXT_PATH, methods=["POST"])
    def next_lecture_request() -> Response:
        refusal = _refusal(token)
        if refusal:
            return refusal
        try:
            claimed = store.claim_next()
        except LectureRequestError as error:
            return _error(str(error), 503)
        if claimed is None:
            return Response(status=204)
        logger.info("Lecture request %s handed to the worker: %s", claimed.id, claimed.url)
        return jsonify(request_to_dict(claimed))

    @server.route(f"{API_PREFIX}<request_id>/stav", methods=["POST"])
    def lecture_request_status(request_id: str) -> Response:
        refusal = _refusal(token)
        if refusal:
            return refusal
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return _error("Tělo požadavku musí být objekt JSON se stavem.", 400)
        try:
            changes = worker_update(payload.get("status"), payload.get("message"), payload.get("page_path"))
            updated = store.update(request_id, changes)
        except LectureRequestError as error:
            return _error(str(error), 400)
        logger.info("Lecture request %s is now %s", request_id, updated.status.value)
        return jsonify(request_to_dict(updated))


def _refusal(token: str) -> Optional[Response]:
    if not token:
        return _error(NO_TOKEN, 503)
    sent = request.headers.get("Authorization", "")
    if not hmac.compare_digest(sent.encode("utf-8"), f"Bearer {token}".encode("utf-8")):
        return _error(WRONG_TOKEN, 401)
    return None


def _error(message: str, status: int) -> Response:
    response = jsonify({"error": message})
    response.status_code = status
    return response
