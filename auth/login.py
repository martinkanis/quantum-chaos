"""Password login in front of the whole Dash app: every route except the health check and the login page needs a
session, which lasts SESSION_LIFETIME from the moment of login."""

from __future__ import annotations

import hmac
import logging
from typing import Optional
from urllib.parse import urlencode

from flask import Flask, Response, jsonify, redirect, render_template_string, request, session

from auth.login_page import LOGIN_TEMPLATE
from auth.rate_limit import FailedLoginLimiter
from auth.settings import SESSION_LIFETIME, LoginSettings

LOGIN_PATH = "/login"
LOGOUT_PATH = "/logout"
HEALTH_PATH = "/healthz"
PUBLIC_PATHS = frozenset({LOGIN_PATH, HEALTH_PATH})
PUBLIC_PREFIXES = ("/assets/",)
"""The login page uses the app stylesheet."""
DASH_REQUEST_PREFIX = "/_dash-"
SESSION_USER_KEY = "user"
INVALID_CREDENTIALS = "Neplatné jméno nebo heslo."
TOO_MANY_ATTEMPTS = "Příliš mnoho neúspěšných pokusů. Zkus to znovu za 15 minut."

logger = logging.getLogger(__name__)


def install_login(server: Flask, settings: LoginSettings, secure_cookies: bool = True) -> None:
    server.secret_key = settings.secret_key
    server.config.update(
        PERMANENT_SESSION_LIFETIME=SESSION_LIFETIME,
        SESSION_REFRESH_EACH_REQUEST=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=secure_cookies,
    )
    limiter = FailedLoginLimiter()

    @server.before_request
    def require_login() -> Optional[Response]:
        if _is_public(request.path) or session.get(SESSION_USER_KEY):
            return None
        if request.path.startswith(DASH_REQUEST_PREFIX):
            return _json_error("Přihlášení vypršelo, načti stránku znovu.", 401)
        return redirect(f"{LOGIN_PATH}?{urlencode({'next': request.full_path.rstrip('?')})}")

    @server.route(LOGIN_PATH, methods=["GET", "POST"])
    def login() -> Response:
        next_path = _safe_next_path(request.values.get("next"))
        if request.method == "GET":
            return _login_form(next_path)
        client = _client_address()
        if limiter.is_locked(client):
            logger.warning("Login rejected: too many failed attempts from %s", client)
            return _login_form(next_path, TOO_MANY_ATTEMPTS, 429)
        if not _credentials_match(settings, request.form.get("user", ""), request.form.get("password", "")):
            limiter.record_failure(client)
            logger.warning("Failed login from %s", client)
            return _login_form(next_path, INVALID_CREDENTIALS, 401)
        limiter.reset(client)
        session.clear()
        session[SESSION_USER_KEY] = settings.user
        session.permanent = True
        return redirect(next_path)

    @server.route(LOGOUT_PATH)
    def logout() -> Response:
        session.clear()
        return redirect(LOGIN_PATH)


def _credentials_match(settings: LoginSettings, user: str, password: str) -> bool:
    """Both comparisons always run and take constant time, so the response time does not leak which one failed."""
    if not settings.is_configured:
        return False
    user_matches = hmac.compare_digest(user.encode(), settings.user.encode())
    password_matches = hmac.compare_digest(password.encode(), settings.password.encode())
    return user_matches and password_matches


def _is_public(path: str) -> bool:
    return path in PUBLIC_PATHS or path.startswith(PUBLIC_PREFIXES)


def _safe_next_path(next_path: Optional[str]) -> str:
    """Only local paths, so the login form cannot be abused to redirect to another site."""
    if next_path and next_path.startswith("/") and not next_path.startswith("//") and "\\" not in next_path:
        return next_path
    return "/"


def _client_address() -> str:
    """The last X-Forwarded-For entry is added by our proxy; earlier ones come from the client and can be forged."""
    return request.access_route[-1] if request.access_route else (request.remote_addr or "unknown")


def _login_form(next_path: str, error: Optional[str] = None, status: int = 200) -> Response:
    page = render_template_string(LOGIN_TEMPLATE, next_path=next_path, error=error)
    return Response(page, status=status, mimetype="text/html")


def _json_error(message: str, status: int) -> Response:
    response = jsonify(error=message)
    response.status_code = status
    return response
