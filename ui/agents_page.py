"""History of the assistant's agents: every run from the newest, its state and what the reader can do with it.

The page has buttons, so it stays in the layout (hidden) like the other form pages. Its list is filled by the polling
callback (ui/assistant_callbacks.agents_outputs), which also writes the number of proposals waiting for approval
into the Agenti link of the top menu, so that a finished agent is noticed from any page.
"""

from __future__ import annotations

from datetime import datetime, timezone, tzinfo
from typing import List, Mapping, Sequence, Tuple
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from dash import html

from assistant.jobs import DISMISSIBLE, RETRYABLE, Job, JobStatus
from ui import ids
from ui.assistant_content import (
    AGENTS_HINT,
    AGENTS_LABEL,
    AGENTS_LEAD,
    AGENTS_TITLE,
    COMMIT_LINK,
    DISMISS_JOB,
    EMPTY_HISTORY,
    EXCERPT_LABEL,
    FINISHED_LABEL,
    HISTORY_TITLE,
    LOADING_HISTORY,
    OPEN_JOB,
    OPEN_PAGE,
    OPEN_PROPOSAL,
    ORIGIN_LABEL,
    RETRY_JOB,
    STARTED_LABEL,
    STATUS_LABELS,
    STILL_RUNNING_LABEL,
    TOPIC_META_LABEL,
    UNKNOWN_PAGE,
)
from ui.generated_topics import generated_path
from ui.navigation import HIDDEN
from ui.topic_catalog import EXPANDED_TOPIC, PageEntry, choosable_topics, page_entries

DISPLAY_TIME_ZONE = "Europe/Prague"
"""The reader's time zone; the jobs keep UTC and the server runs in UTC."""
TITLE_LENGTH = 70
EXCERPT_LENGTH = 160


def build_agents_page() -> html.Div:
    return html.Div(
        id=ids.AGENTS_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            html.H1(AGENTS_TITLE),
            html.P(AGENTS_LEAD, className="lead"),
            html.P(AGENTS_HINT, className="hint"),
            html.Section(className="card", children=[
                html.H2(HISTORY_TITLE),
                html.Div(id=ids.AGENTS_LIST, children=html.P(LOADING_HISTORY, className="hint")),
            ]),
        ],
    )


def agents_link_label(jobs: Sequence[Job]) -> List:
    """„Agenti“, with the number of proposals waiting for approval as „Agenti (1)“ so that a new one is noticed."""
    waiting = sum(job.status == JobStatus.READY for job in jobs)
    if not waiting:
        return [AGENTS_LABEL]
    return [AGENTS_LABEL, " ", html.Span(f"({waiting})", className="agents-count")]


def agent_history(jobs: Sequence[Job]) -> List:
    if not jobs:
        return [html.P(EMPTY_HISTORY, className="hint")]
    entries = page_entries()
    return [html.Ul(className="agent-history", children=[_history_item(job, entries) for job in jobs])]


def agent_title(job: Job) -> str:
    """The title of the drafted page; until the agent has one, the excerpt it works from."""
    title = (job.result or {}).get("title")
    return title if title else f"„{excerpt(_selection(job).get('selection', ''), TITLE_LENGTH)}“"


def czech_moment(moment: datetime) -> str:
    """„9. 11. 2026 14:02“ in the reader's time zone; a moment without a zone is taken as UTC."""
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    local = moment.astimezone(DISPLAY_ZONE)
    return f"{local.day}. {local.month}. {local.year} {local:%H:%M}{ZONE_SUFFIX}"


def excerpt(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0] + "…"


def _history_item(job: Job, entries: Mapping[str, PageEntry]) -> html.Li:
    return html.Li(className=f"agent-item status-{job.status.value}", children=[
        html.Div(className="agent-head", children=[
            html.Span(className="agent-dot"),
            html.Span(STATUS_LABELS[job.status], className="agent-state"),
            html.Span(agent_title(job), className="agent-title"),
        ]),
        html.Div(_origin(job, entries), className="agent-meta"),
        html.Div(_times(job), className="agent-meta"),
        *([html.Div(job.error, className="agent-error")] if job.error else []),
        html.Div(className="agent-buttons", children=_buttons(job)),
    ])


def _origin(job: Job, entries: Mapping[str, PageEntry]) -> str:
    """The page the selection came from, the topic the page joins and, when the title line shows the drafted
    title, the selection itself."""
    selection = _selection(job)
    entry = entries.get(selection.get("page_id", ""))
    page_title = entry.title if entry else (selection.get("page_title") or selection.get("page_id") or UNKNOWN_PAGE)
    origin = f"{ORIGIN_LABEL} „{page_title}“, {TOPIC_META_LABEL} „{_topic_title(job)}“"
    if (job.result or {}).get("title"):
        origin += f", {EXCERPT_LABEL}: „{excerpt(selection.get('selection', ''), EXCERPT_LENGTH)}“"
    return origin


def _topic_title(job: Job) -> str:
    """The research topic of the page: the one approved with the result, else the one chosen at the start."""
    placement = (job.result or {}).get("placement") or job.request.get("placement") or {}
    anchor = placement.get("topic_anchor") or EXPANDED_TOPIC.anchor
    known = next((topic.title for topic in choosable_topics() if topic.anchor == anchor), None)
    return known or placement.get("topic_title") or anchor


def _times(job: Job) -> str:
    """Start of the run and the moment it reached its state: finished, accepted, rejected or deployed."""
    started = f"{STARTED_LABEL} {czech_moment(job.created_at)}"
    if job.status == JobStatus.RUNNING:
        return f"{started} · {STILL_RUNNING_LABEL}"
    return f"{started} · {FINISHED_LABEL} {czech_moment(job.updated_at)}"


def _buttons(job: Job) -> List:
    if job.status == JobStatus.READY:
        buttons: List = [_button(OPEN_PROPOSAL, ids.AGENT_OPEN, job, "primary-button")]
    else:
        buttons = [_button(OPEN_JOB, ids.AGENT_OPEN, job, "secondary-button")]
    if job.status == JobStatus.DEPLOYED:
        # A full page load, because the new page is in the app only after the redeploy, not in the layout of this tab.
        buttons.append(html.A(OPEN_PAGE, href=generated_path((job.result or {}).get("slug", "")), className="primary-link"))
    if job.commit_url:
        buttons.append(html.A(COMMIT_LINK, href=job.commit_url, target="_blank", rel="noopener noreferrer"))
    if job.status in RETRYABLE:
        buttons.append(_button(RETRY_JOB, ids.AGENT_RETRY, job, "secondary-button"))
    if job.status in DISMISSIBLE:
        buttons.append(_button(DISMISS_JOB, ids.AGENT_DISMISS, job, "secondary-button"))
    return buttons


def _button(label: str, button_type: str, job: Job, class_name: str) -> html.Button:
    return html.Button(label, id={"type": button_type, "index": job.id}, className=class_name)


def _selection(job: Job) -> Mapping[str, str]:
    selection = job.request.get("selection")
    return selection if isinstance(selection, Mapping) else {}


def _display_zone() -> Tuple[tzinfo, str]:
    """The reader's zone and the suffix shown after the times; without the zone database the times stay in UTC."""
    try:
        return ZoneInfo(DISPLAY_TIME_ZONE), ""
    except ZoneInfoNotFoundError:
        return timezone.utc, " UTC"


DISPLAY_ZONE, ZONE_SUFFIX = _display_zone()
