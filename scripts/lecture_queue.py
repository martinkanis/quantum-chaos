"""The worker's end of the lecture queue in the app (web/lecture_queue_api.py), run by Claude Code on the author's Mac.

    python scripts/lecture_queue.py dalsi
        takes the oldest waiting request, prints it as JSON and marks it as being processed;
        exit code 3 when the queue is empty
    python scripts/lecture_queue.py stav ID zpracovava-se|hotovo|chyba [--zprava TEXT] [--stranka /zapisky/...]
        reports progress, the finished page or what went wrong

The token is read from LECTURE_WORKER_TOKEN or from ~/.config/quantum-chaos/lecture-worker-token (never from the
repository); the app address from LECTURE_QUEUE_URL, by default the production app.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional, Sequence

DEFAULT_APP_URL = "https://quantum-chaos.rock8cloud.app"
APP_URL_ENV = "LECTURE_QUEUE_URL"
TOKEN_ENV = "LECTURE_WORKER_TOKEN"
TOKEN_FILE = Path.home() / ".config" / "quantum-chaos" / "lecture-worker-token"
API_PREFIX = "/api/prednasky/"
TIMEOUT_SECONDS = 30
EMPTY_QUEUE_EXIT_CODE = 3


class QueueError(RuntimeError):
    """The app refused or could not be reached; the message says what to fix."""


def worker_token() -> str:
    token = os.environ.get(TOKEN_ENV, "").strip()
    if not token and TOKEN_FILE.exists():
        token = TOKEN_FILE.read_text(encoding="utf-8").strip()
    if not token:
        raise QueueError(f"Chybí token pracovníka: nastav {TOKEN_ENV} nebo ho ulož do {TOKEN_FILE}.")
    return token


def call(path: str, payload: Optional[dict] = None) -> Optional[dict]:
    """POST to the queue API; None when the app answers 204 (nothing waiting)."""
    app_url = os.environ.get(APP_URL_ENV, DEFAULT_APP_URL).rstrip("/")
    request = urllib.request.Request(
        f"{app_url}{API_PREFIX}{path}",
        data=json.dumps(payload or {}).encode("utf-8"),
        headers={"Authorization": f"Bearer {worker_token()}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            body = response.read()
            return json.loads(body) if response.status != 204 and body else None
    except urllib.error.HTTPError as error:
        raise QueueError(f"Aplikace odmítla {path} ({error.code}): {_error_text(error)}") from error
    except urllib.error.URLError as error:
        raise QueueError(f"Aplikace {app_url} není dostupná: {error.reason}") from error


def _error_text(error: urllib.error.HTTPError) -> str:
    try:
        return json.loads(error.read()).get("error", "")
    except ValueError:
        return ""


def main(arguments: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("dalsi", help="vzít nejstarší čekající požadavek")
    status = commands.add_parser("stav", help="nahlásit stav požadavku")
    status.add_argument("id")
    status.add_argument("stav", choices=["zpracovava-se", "hotovo", "chyba"])
    status.add_argument("--zprava", default="")
    status.add_argument("--stranka", default="")
    options = parser.parse_args(arguments)
    try:
        if options.command == "dalsi":
            claimed = call("dalsi")
            if claimed is None:
                print("Fronta je prázdná.")
                return EMPTY_QUEUE_EXIT_CODE
            print(json.dumps(claimed, ensure_ascii=False, indent=2))
            return 0
        payload = {"status": options.stav, "message": options.zprava, "page_path": options.stranka}
        print(json.dumps(call(f"{options.id}/stav", payload), ensure_ascii=False, indent=2))
        return 0
    except QueueError as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
