"""Offline reading: a service worker keeps the app and the content of its pages in the browser.

Dash sends a page's content as answers to callbacks keyed by the URL, so the worker (web/service_worker.js) stores
those answers and replays them when the network is down. The manifest tells it what to download in advance: every
page path, the callbacks that depend only on the path (page switching, lazy pages, breadcrumbs, study pager), the
code chunks Dash loads on demand and the lecture slides. Pages with forms show offline, but their calculations
need the server. Both routes sit behind the login like the rest of the app, so the stored copy is the reader's own.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Dict, List

import dash
from dash import Dash
from flask import Response

from ui import ids
from ui.navigation import PAGE_BY_PATH
from ui.walther_lecture_content import LECTURE, SLIDES
from web.lecture_slides import slide_url

SERVICE_WORKER_PATH = "/sw.js"
MANIFEST_PATH = "/offline-manifest.json"
SERVICE_WORKER_FILE = Path(__file__).resolve().parent / "service_worker.js"
STARTED_AT = str(int(time.time()))
"""A new deployment restarts the app, and a new version makes the browsers download everything again."""
URL_PATHNAME = (ids.URL, "pathname")
STORE_SUFFIX = "-store"
"""Stores (rendered lazy pages, study progress) only remember what the browser already has; replaying an answer
for a path does not depend on them."""
DASH_SUITES = "/_dash-component-suites"
LAZY_CHUNK_FOLDERS = ("dcc", "dash_table")
PLOTLY_BUNDLE = f"{DASH_SUITES}/plotly/package_data/plotly.min.js"


def install_offline(app: Dash) -> None:
    """Register after all callbacks, the manifest lists the ones that depend only on the path."""
    server = app.server

    @server.route(SERVICE_WORKER_PATH)
    def service_worker() -> Response:
        response = Response(SERVICE_WORKER_FILE.read_text(encoding="utf-8"), mimetype="application/javascript")
        response.headers["Cache-Control"] = "no-cache"
        return response

    @server.route(MANIFEST_PATH)
    def offline_manifest() -> Response:
        response = Response(json.dumps(build_manifest(app.callback_map)), mimetype="application/json")
        response.headers["Cache-Control"] = "no-store"
        return response


def build_manifest(callback_map: Dict[str, dict]) -> dict:
    return {
        "version": STARTED_AT,
        "paths": sorted(PAGE_BY_PATH),
        "urls": ["/_dash-layout", "/_dash-dependencies", *lazy_chunk_urls(), *slide_urls()],
        "callbacks": path_callbacks(callback_map),
    }


def path_callbacks(callback_map: Dict[str, dict]) -> List[dict]:
    """Request bodies of the server callbacks whose answer depends only on the path; the worker sets the path."""
    return [
        _request_template(output, spec) for output, spec in callback_map.items()
        if "callback" in spec and _depends_only_on_path(spec)
    ]


def lazy_chunk_urls() -> List[str]:
    """Code Dash loads only when a page needs it (Markdown, MathJax, graphs, tables)."""
    package = Path(dash.__file__).resolve().parent
    return [
        f"{DASH_SUITES}/dash/{folder}/{chunk.name}"
        for folder in LAZY_CHUNK_FOLDERS for chunk in sorted((package / folder).glob("async-*.js"))
    ] + [PLOTLY_BUNDLE]


def slide_urls() -> List[str]:
    return [slide_url(LECTURE, slide.file_name) for slide in SLIDES]


def _depends_only_on_path(spec: dict) -> bool:
    inputs = [(item["id"], item["property"]) for item in spec["inputs"]]
    states = [(item["id"], item["property"]) for item in spec["state"]]
    return URL_PATHNAME in inputs and all(
        dependency == URL_PATHNAME or _is_store(dependency) for dependency in inputs + states
    )


def _is_store(dependency) -> bool:
    component_id, prop = dependency
    return isinstance(component_id, str) and component_id.endswith(STORE_SUFFIX) and prop == "data"


def _request_template(output: str, spec: dict) -> dict:
    """The body the renderer would send; stores start empty, the path is filled in by the worker."""
    return {
        "output": output,
        "outputs": _outputs(output),
        "inputs": [_dependency(item) for item in spec["inputs"]],
        "changedPropIds": [".".join(URL_PATHNAME)],
        "state": [_dependency(item) for item in spec["state"]],
    }


def _outputs(output: str):
    """„..a.style...b.style..“ is a list of outputs, „a.style“ a single one."""
    if output.startswith(".."):
        items = output[2:-2].split("...")
        return [_output(item) for item in items]
    return _output(output)


def _output(item: str) -> dict:
    component_id, prop = item.rsplit(".", 1)
    return {"id": component_id, "property": prop}


def _dependency(item: dict) -> dict:
    return {"id": item["id"], "property": item["property"], "value": None}
