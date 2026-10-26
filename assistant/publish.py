"""Publishing an accepted topic: one commit of its JSON file to the repository through the GitHub API.

The push to main is what deploys the app (the platform deploys every push), so after this the new page goes live
on its own. The token needs only Contents read and write on this one repository.
"""

from __future__ import annotations

import base64
import json
import logging
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Optional

from assistant.topics import REPOSITORY_DIRECTORY, TopicPage, topic_to_json

TOKEN_ENV = "GITHUB_TOKEN"
REPOSITORY_ENV = "GITHUB_REPOSITORY"
BRANCH_ENV = "GITHUB_BRANCH"
DEFAULT_REPOSITORY = "martinkanis/quantum-chaos"
DEFAULT_BRANCH = "main"
API_URL = "https://api.github.com"
TIMEOUT_SECONDS = 20

logger = logging.getLogger(__name__)

Opener = Callable[..., Any]


class PublishError(ValueError):
    """The topic could not be committed; the message says why in Czech."""


@dataclass(frozen=True)
class PublishSettings:
    token: Optional[str]
    repository: str
    branch: str

    @property
    def is_configured(self) -> bool:
        return bool(self.token)


def publish_settings_from_environment(environment: Mapping[str, str] = os.environ) -> PublishSettings:
    return PublishSettings(
        token=environment.get(TOKEN_ENV) or None,
        repository=environment.get(REPOSITORY_ENV) or DEFAULT_REPOSITORY,
        branch=environment.get(BRANCH_ENV) or DEFAULT_BRANCH,
    )


def commit_message(topic: TopicPage) -> str:
    return (
        f"Nové téma: {topic.title}\n\n"
        f"Rozvedl ho asistent v aplikaci z textu na stránce {topic.origin.page_id} a uživatel ho schválil."
    )


def publish_topic(topic: TopicPage, settings: PublishSettings, opener: Opener = urllib.request.urlopen) -> str:
    """Commits content/topics/<slug>.json to the branch and returns the link to the commit."""
    if not settings.is_configured:
        raise PublishError(f"Publikování není nastavené: službě chybí proměnná prostředí {TOKEN_ENV}.")
    path = f"{REPOSITORY_DIRECTORY}/{topic.file_name}"
    body = {
        "message": commit_message(topic),
        "content": base64.b64encode(topic_to_json(topic).encode("utf-8")).decode("ascii"),
        "branch": settings.branch,
    }
    request = urllib.request.Request(
        f"{API_URL}/repos/{settings.repository}/contents/{path}",
        data=json.dumps(body).encode("utf-8"),
        method="PUT",
        headers={
            "Authorization": f"Bearer {settings.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )
    try:
        with opener(request, timeout=TIMEOUT_SECONDS) as response:
            answer = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        raise PublishError(_http_error_message(error.code, path)) from error
    except (urllib.error.URLError, TimeoutError) as error:
        raise PublishError("GitHub teď neodpovídá. Zkus schválení za chvíli znovu.") from error
    return str((answer.get("commit") or {}).get("html_url") or "")


def _http_error_message(status: int, path: str) -> str:
    if status in (401, 403):
        return f"GitHub odmítl token z {TOKEN_ENV}. Zkontroluj, že platí a má právo zapisovat obsah repozitáře."
    if status == 404:
        return "GitHub repozitář nebo větev nenašel, nebo k nim token nemá přístup."
    if status in (409, 422):
        return f"Soubor {path} už v repozitáři je. Zamítni tento návrh a rozveď téma znovu."
    logger.error("GitHub API returned %s for %s", status, path)
    return f"GitHub vrátil chybu {status}. Zkus schválení znovu."
