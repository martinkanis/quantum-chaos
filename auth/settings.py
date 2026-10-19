"""Login configuration read from environment variables; without them nobody can log in (deny by default)."""

from __future__ import annotations

import logging
import os
import secrets
from dataclasses import dataclass
from datetime import timedelta
from typing import Mapping, Optional

USER_ENV = "APP_LOGIN_USER"
PASSWORD_ENV = "APP_LOGIN_PASSWORD"
SECRET_KEY_ENV = "APP_SECRET_KEY"
SESSION_LIFETIME = timedelta(days=30)
EPHEMERAL_SECRET_BYTES = 32

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LoginSettings:
    user: Optional[str]
    password: Optional[str]
    secret_key: str
    """Signs the session cookie; a random key logs everybody out on every restart."""

    @property
    def is_configured(self) -> bool:
        return bool(self.user) and bool(self.password)


def settings_from_environment(environment: Mapping[str, str] = os.environ) -> LoginSettings:
    settings = LoginSettings(
        user=environment.get(USER_ENV) or None,
        password=environment.get(PASSWORD_ENV) or None,
        secret_key=environment.get(SECRET_KEY_ENV) or _ephemeral_secret_key(),
    )
    if not settings.is_configured:
        logger.error(
            "Login is not configured: set %s and %s, until then every login attempt fails.", USER_ENV, PASSWORD_ENV
        )
    return settings


def _ephemeral_secret_key() -> str:
    logger.warning("%s is not set: sessions are signed with a random key and end on every restart.", SECRET_KEY_ENV)
    return secrets.token_hex(EPHEMERAL_SECRET_BYTES)
