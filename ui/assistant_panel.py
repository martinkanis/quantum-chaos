"""The assistant in the layout: the pop-up with explanations and previews, and the agents panel in the corner.

Both are always in the layout, so that the callbacks have their inputs from the start; assets/assistant.js opens the
pop-up right away when the reader asks the highlighter toolbar for an explanation.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional, Sequence

from dash import dcc, html

from assistant.jobs import DISMISSIBLE, RETRYABLE, Job, JobStatus
from ui import ids
from ui.assistant_content import (
    ACCEPT_LABEL,
    AGENTS_LABEL,
    CLOSE_LABEL,
    DISMISS_JOB,
    EXPAND_LABEL,
    OPEN_JOB,
    REJECT_LABEL,
    RETRY_JOB,
    STATUS_LABELS,
)
from ui.navigation import HIDDEN

POLL_MILLISECONDS = 5000
MODAL_CLASS = "assistant-modal"
OPEN_MODAL_CLASS = "assistant-modal open"
AGENT_TITLE_LENGTH = 70


def build_assistant() -> html.Div:
    return html.Div(className="assistant", children=[
        dcc.Store(id=ids.ASSISTANT_REQUEST),
        dcc.Store(id=ids.ASSISTANT_CONTEXT),
        dcc.Store(id=ids.AGENTS_REFRESH),
        dcc.Store(id=ids.AGENTS_STATE),
        dcc.Interval(id=ids.AGENTS_INTERVAL, interval=POLL_MILLISECONDS, disabled=False),
        _agents_panel(),
        _modal(),
    ])


def _agents_panel() -> html.Div:
    return html.Div(id=ids.AGENTS_PANEL, className="agents-panel", style=HIDDEN, children=html.Details(
        className="agents-box",
        children=[
            html.Summary(id=ids.AGENTS_SUMMARY, children=AGENTS_LABEL),
            html.Div(id=ids.AGENTS_LIST, className="agents-list"),
        ],
    ))


def _modal() -> html.Div:
    return html.Div(id=ids.ASSISTANT_MODAL, className=MODAL_CLASS, children=html.Div(
        className="assistant-dialog",
        role="dialog",
        **{"aria-modal": "true", "aria-labelledby": ids.ASSISTANT_MODAL_TITLE},
        children=[
            html.H2(id=ids.ASSISTANT_MODAL_TITLE, className="assistant-title"),
            dcc.Loading(type="dot", children=html.Div(id=ids.ASSISTANT_MODAL_BODY, className="assistant-body")),
            html.P(id=ids.ASSISTANT_MODAL_MESSAGE, className="error-message"),
            html.Div(className="assistant-actions", children=[
                html.Button(EXPAND_LABEL, id=ids.ASSISTANT_EXPAND_BUTTON, className="primary-button", style=HIDDEN),
                html.Button(ACCEPT_LABEL, id=ids.ASSISTANT_ACCEPT_BUTTON, className="primary-button", style=HIDDEN),
                html.Button(REJECT_LABEL, id=ids.ASSISTANT_REJECT_BUTTON, className="secondary-button", style=HIDDEN),
                html.Button(CLOSE_LABEL, id=ids.ASSISTANT_CLOSE_BUTTON, className="secondary-button"),
            ]),
        ],
    ))


def agents_summary(jobs: Sequence[Job]) -> List:
    waiting = sum(job.status == JobStatus.READY for job in jobs)
    running = sum(job.status == JobStatus.RUNNING for job in jobs)
    deploying = sum(job.status == JobStatus.DEPLOYING for job in jobs)
    children: List = [AGENTS_LABEL]
    if running:
        children.append(html.Span(f"{running} pracuje", className="agents-badge running"))
    if waiting:
        children.append(html.Span(f"{waiting} ke schválení", className="agents-badge ready"))
    if deploying:
        children.append(html.Span(f"{deploying} se nasazuje", className="agents-badge running"))
    return children


def agent_items(jobs: Sequence[Job], now: Optional[datetime] = None) -> List[html.Div]:
    now = now or datetime.now(timezone.utc)
    return [_agent_item(job, now) for job in jobs]


def _agent_item(job: Job, now: datetime) -> html.Div:
    buttons = [html.Button(OPEN_JOB, id={"type": ids.AGENT_OPEN, "index": job.id}, className="secondary-button")]
    if job.status in RETRYABLE:
        buttons.append(html.Button(RETRY_JOB, id={"type": ids.AGENT_RETRY, "index": job.id}, className="secondary-button"))
    if job.status in DISMISSIBLE:
        buttons.append(
            html.Button(DISMISS_JOB, id={"type": ids.AGENT_DISMISS, "index": job.id}, className="secondary-button")
        )
    return html.Div(className=f"agent-item status-{job.status.value}", children=[
        html.Div(agent_title(job), className="agent-title"),
        html.Div(className="agent-status", children=[
            html.Span(className="agent-dot"), f"{STATUS_LABELS[job.status]} · {elapsed_label(job.updated_at, now)}",
        ]),
        html.Div(className="agent-buttons", children=buttons),
    ])


def agent_title(job: Job) -> str:
    title = (job.result or {}).get("title") or (job.request.get("selection") or {}).get("selection") or ""
    return title if len(title) <= AGENT_TITLE_LENGTH else title[:AGENT_TITLE_LENGTH].rsplit(" ", 1)[0] + "…"


def elapsed_label(moment: datetime, now: datetime) -> str:
    minutes = int((now - moment).total_seconds() // 60)
    if minutes < 1:
        return "právě teď"
    if minutes < 60:
        return f"před {minutes} min"
    hours = minutes // 60
    if hours < 24:
        return f"před {hours} h"
    return f"před {hours // 24} d"
