"""Slide images of recorded lectures, served only to logged-in readers.

Files under /assets/ are public (the login page needs the stylesheet), so the slides, which belong to their authors,
have their own route behind the login (auth/login.py checks every route except the public ones).
"""

from __future__ import annotations

import re
from pathlib import Path

from flask import Flask, Response, abort, send_from_directory

LECTURES_DIRECTORY = Path(__file__).resolve().parent.parent / "content" / "lectures"
SLIDES_FOLDER = "slajdy"
SLIDES_URL_PREFIX = "/prednasky"
LECTURE_NAME = re.compile(r"[a-z0-9-]+")
SLIDE_NAME = re.compile(r"slajd_\d{4}\.jpg")
CACHE_SECONDS = 7 * 24 * 3600
"""Slides never change under the same name; the browser keeps them for a week, privately (they need a login)."""


def slide_url(lecture: str, file_name: str) -> str:
    return f"{SLIDES_URL_PREFIX}/{lecture}/{file_name}"


def slide_path(lecture: str, file_name: str) -> Path:
    return LECTURES_DIRECTORY / lecture / SLIDES_FOLDER / file_name


def install_lecture_slides(server: Flask) -> None:
    @server.route(f"{SLIDES_URL_PREFIX}/<lecture>/<file_name>")
    def lecture_slide(lecture: str, file_name: str) -> Response:
        if not LECTURE_NAME.fullmatch(lecture) or not SLIDE_NAME.fullmatch(file_name):
            abort(404)
        response = send_from_directory(LECTURES_DIRECTORY / lecture / SLIDES_FOLDER, file_name, max_age=CACHE_SECONDS)
        response.cache_control.public = False
        response.cache_control.private = True
        return response
