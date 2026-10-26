"""Callbacks of the assistant: explaining a selection, starting agents, previewing, accepting and rejecting pages.

Every action of the pop-up and of the agents panel goes through one callback, so the pop-up has a single owner;
the work behind each action is in plain functions that return a View, which the tests call directly.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, replace
from typing import Any, Callable, FrozenSet, List, Mapping, Optional, Tuple

from dash import ALL, Dash, Input, Output, State, ctx, dcc, html, no_update

from assistant import claude
from assistant.agent import agent_request, draft_topic
from assistant.claude import AssistantError
from assistant.jobs import (
    ACTIVE,
    DISMISSIBLE,
    AgentRunner,
    Job,
    JobError,
    JobStatus,
    job_store_from_environment,
    recover_jobs,
)
from assistant.publish import PublishError, publish_settings_from_environment, publish_topic
from assistant.selection import SelectionContext, SelectionError, selection_from_request, selection_to_dict
from assistant.topics import TopicError, TopicPage, topic_from_dict, topic_to_dict, unique_slug
from ui import ids
from ui.assistant_content import (
    ACCEPT_HINT,
    AGENT_STARTED,
    AGENT_TITLE,
    COMMIT_LINK,
    DEPLOYED,
    DEPLOYING,
    EXPAND_TITLE,
    EXPLAIN_TITLE,
    EXPLANATION_NOTE,
    MISSING_JOB,
    NO_PLACEMENT,
    OPEN_PAGE,
    PREVIEW_TITLE,
    REJECTED,
    RUNNING_AGENTS_WARNING,
    STILL_RUNNING,
)
from ui.assistant_panel import MODAL_CLASS, OPEN_MODAL_CLASS, agent_items, agents_summary
from ui.generated_page import generated_page_content
from ui.generated_topics import generated_path, published_slugs
from ui.knowledge_map_content import LAYERS
from ui.navigation import HIDDEN, VISIBLE
from ui.topic_catalog import page_entries, placement_for

AGENTS_SHOWN = 10
QUOTE_LENGTH = 300
EXPAND, ACCEPT, REJECT = "expand", "accept", "reject"
ACTION_BUTTONS = (EXPAND, ACCEPT, REJECT)
NOT_READY = "Návrh už není ke schválení."

logger = logging.getLogger(__name__)


@dataclass
class Assistant:
    """What the callbacks work with: the job store, the agent runner, Claude and publishing; tests pass fakes."""

    store: Any
    runner: AgentRunner
    explain: Callable[[SelectionContext], str]
    publish: Callable[[TopicPage], str]


def assistant_from_environment() -> Assistant:
    store = job_store_from_environment()
    try:
        recover_jobs(store, published_slugs())
    except JobError:
        logger.exception("Assistant jobs could not be recovered after the start")
    settings = publish_settings_from_environment()
    return Assistant(
        store=store,
        runner=AgentRunner(store, lambda job: draft_topic(job.request, published_slugs())),
        explain=claude.explain,
        publish=lambda topic: publish_topic(topic, settings),
    )


@dataclass(frozen=True)
class View:
    """What an action changes; fields left at no_update keep the pop-up as it is."""

    open: Any = no_update
    title: Any = no_update
    body: Any = no_update
    message: Any = no_update
    buttons: Any = no_update
    """The action buttons to show (EXPAND, ACCEPT, REJECT); the close button is always there."""
    context: Any = no_update
    poll: bool = False
    """Start polling the agents, because one of them is now running or deploying."""
    refresh: bool = False


def dialog(title: str, body: List, message: str = "", buttons: FrozenSet[str] = frozenset(), **changes: Any) -> View:
    return View(open=True, title=title, body=body, message=message, buttons=buttons, **changes)


def view_outputs(view: View) -> Tuple:
    modal_class = no_update if view.open is no_update else (OPEN_MODAL_CLASS if view.open else MODAL_CLASS)
    if view.buttons is no_update:
        button_styles: Tuple = (no_update,) * len(ACTION_BUTTONS)
    else:
        button_styles = tuple(VISIBLE if button in view.buttons else HIDDEN for button in ACTION_BUTTONS)
    return (
        modal_class, view.title, view.body, view.message, *button_styles, view.context,
        False if view.poll else no_update,
        time.time() if view.poll or view.refresh else no_update,
    )


def handle_action(
    assistant: Assistant, trigger: Any, value: Any, request: Optional[Mapping], context: Optional[Mapping]
) -> View:
    """Dispatches one click or request; a re-rendered agents list re-fires the callback without a click."""
    if trigger == ids.ASSISTANT_REQUEST:
        return ask(assistant, request or {})
    if not value:
        return View()
    context = context or {}
    if trigger == ids.ASSISTANT_EXPAND_BUTTON:
        return start_agent(assistant, context.get("selection"), context.get("explanation"))
    if trigger == ids.ASSISTANT_ACCEPT_BUTTON:
        return accept(assistant, context.get("job_id"))
    if trigger == ids.ASSISTANT_REJECT_BUTTON:
        return reject(assistant, context.get("job_id"))
    if isinstance(trigger, Mapping):
        action = {ids.AGENT_OPEN: show_job, ids.AGENT_RETRY: retry, ids.AGENT_DISMISS: dismiss}.get(trigger.get("type"))
        if action:
            return action(assistant, trigger.get("index"))
    return View()


def ask(assistant: Assistant, request: Mapping) -> View:
    title = EXPAND_TITLE if request.get("action") == EXPAND else EXPLAIN_TITLE
    try:
        selection = selection_from_request(request)
    except SelectionError as error:
        return dialog(title, [], str(error))
    if request.get("action") == EXPAND:
        return start_agent(assistant, selection_to_dict(selection), None)
    try:
        explanation = assistant.explain(selection)
    except AssistantError as error:
        return dialog(title, [quote(selection.selection)], str(error))
    return dialog(
        title,
        [
            quote(selection.selection),
            dcc.Markdown(explanation, mathjax=True, link_target="_blank", className="assistant-explanation"),
            html.P(EXPLANATION_NOTE, className="hint small"),
        ],
        buttons=frozenset({EXPAND}),
        context={"selection": selection_to_dict(selection), "explanation": explanation},
    )


def start_agent(assistant: Assistant, selection: Any, explanation: Optional[str]) -> View:
    try:
        context = selection_from_request(selection)
        placement = placement_for(context.page_id)
        if placement is None:
            raise SelectionError(NO_PLACEMENT)
        existing_pages = [entry.title for entry in page_entries().values()]
        job = assistant.runner.start(agent_request(selection, explanation, placement, existing_pages))
    except (SelectionError, JobError) as error:
        return dialog(EXPAND_TITLE, [], str(error))
    return dialog(
        EXPAND_TITLE, [quote(context.selection), html.P(AGENT_STARTED)], context={"job_id": job.id}, poll=True,
    )


def show_job(assistant: Assistant, job_id: Optional[str], message: str = "", **changes: Any) -> View:
    job = _job(assistant, job_id)
    if job is None:
        return dialog(AGENT_TITLE, [], MISSING_JOB)
    context = {"job_id": job.id}
    selection = quote((job.request.get("selection") or {}).get("selection", ""))
    if job.status == JobStatus.READY:
        try:
            topic = topic_from_dict(job.result or {})
        except TopicError as error:
            return dialog(PREVIEW_TITLE, [selection], str(error), context=context, **changes)
        body = [
            html.P(_accept_hint(assistant, topic, job), className="hint"),
            html.Div(className="assistant-preview", children=generated_page_content(topic, with_anchors=False)),
        ]
        return dialog(PREVIEW_TITLE, body, message, frozenset({ACCEPT, REJECT}), context=context, **changes)
    if job.status == JobStatus.DEPLOYING:
        body = [html.P(DEPLOYING), *_commit_link(job)]
    elif job.status == JobStatus.DEPLOYED:
        slug = (job.result or {}).get("slug", "")
        body = [html.P(DEPLOYED), html.A(OPEN_PAGE, href=generated_path(slug), className="primary-link"), *_commit_link(job)]
    elif job.status == JobStatus.REJECTED:
        body = [selection, html.P(REJECTED)]
    elif job.status == JobStatus.RUNNING:
        body = [selection, html.P(STILL_RUNNING)]
    else:
        body, message = [selection], message or job.error
    return dialog(AGENT_TITLE, body, message, context=context, **changes)


def accept(assistant: Assistant, job_id: Optional[str]) -> View:
    job = _job(assistant, job_id)
    if job is None or job.status != JobStatus.READY:
        return show_job(assistant, job_id, NOT_READY)
    try:
        topic = topic_from_dict(job.result or {})
        taken = published_slugs()
        if topic.slug in taken:
            topic = replace(topic, slug=unique_slug(topic.slug, taken))
        commit_url = assistant.publish(topic)
        assistant.store.update(job.id, {
            "status": JobStatus.DEPLOYING, "commit_url": commit_url, "result": topic_to_dict(topic),
        })
    except (TopicError, PublishError, JobError) as error:
        return show_job(assistant, job_id, str(error))
    return show_job(assistant, job_id, poll=True)


def reject(assistant: Assistant, job_id: Optional[str]) -> View:
    job = _job(assistant, job_id)
    if job is None or job.status != JobStatus.READY:
        return show_job(assistant, job_id, NOT_READY)
    try:
        assistant.store.update(job.id, {"status": JobStatus.REJECTED})
    except JobError as error:
        return show_job(assistant, job_id, str(error))
    return View(open=False, refresh=True)


def retry(assistant: Assistant, job_id: Optional[str]) -> View:
    try:
        assistant.runner.retry(job_id or "")
    except JobError as error:
        return dialog(AGENT_TITLE, [], str(error))
    return View(poll=True)


def dismiss(assistant: Assistant, job_id: Optional[str]) -> View:
    job = _job(assistant, job_id)
    if job is None or job.status not in DISMISSIBLE:
        return View(refresh=True)
    try:
        assistant.store.update(job.id, {"dismissed": True})
    except JobError as error:
        return dialog(AGENT_TITLE, [], str(error))
    return View(refresh=True)


def agents_outputs(assistant: Assistant, previous: Optional[Mapping]) -> Tuple:
    """Panel style, summary, list, state for notifications and whether polling stops; no redraw if nothing changed."""
    try:
        jobs = assistant.store.recent(AGENTS_SHOWN)
    except JobError as error:
        return VISIBLE, agents_summary([]), html.P(str(error), className="error-message"), no_update, False
    signature = [[job.id, job.status.value, job.updated_at.isoformat()] for job in jobs]
    stop_polling = not any(job.status in ACTIVE for job in jobs)
    if previous and previous.get("signature") == signature:
        return no_update, no_update, no_update, no_update, stop_polling
    state = {
        "signature": signature,
        "ready": [_notice(job) for job in jobs if job.status == JobStatus.READY],
        "deployed": [_notice(job) for job in jobs if job.status == JobStatus.DEPLOYED],
    }
    return VISIBLE if jobs else HIDDEN, agents_summary(jobs), agent_items(jobs), state, stop_polling


def quote(text: str) -> html.Blockquote:
    short = text if len(text) <= QUOTE_LENGTH else text[:QUOTE_LENGTH].rsplit(" ", 1)[0] + "…"
    return html.Blockquote(short, className="assistant-quote")


def _accept_hint(assistant: Assistant, topic: TopicPage, job: Job) -> str:
    group = next((info.title for info in LAYERS if info.layer.value == topic.placement.layer), topic.placement.layer)
    parent = page_entries().get(topic.placement.parent_page_id or "")
    hint = ACCEPT_HINT.format(group=group, parent=parent.title if parent else topic.placement.parent_page_id)
    try:
        running = sum(other.status == JobStatus.RUNNING for other in assistant.store.recent(50) if other.id != job.id)
    except JobError:
        running = 0
    return hint + (RUNNING_AGENTS_WARNING.format(count=running) if running else "")


def _commit_link(job: Job) -> List:
    if not job.commit_url:
        return []
    return [html.P(html.A(COMMIT_LINK, href=job.commit_url, target="_blank", rel="noopener noreferrer"))]


def _notice(job: Job) -> dict:
    return {"id": job.id, "title": (job.result or {}).get("title", "")}


def _job(assistant: Assistant, job_id: Optional[str]) -> Optional[Job]:
    if not job_id:
        return None
    try:
        return assistant.store.get(job_id)
    except JobError:
        return None


NOTIFY_JS = "function(state) { if (window.qcAssistant) { window.qcAssistant.notify(state); } }"
CLOSE_JS = "function(clicks) { return clicks ? '" + MODAL_CLASS + "' : window.dash_clientside.no_update; }"


def register_assistant_callbacks(app: Dash, assistant: Optional[Assistant] = None) -> None:
    assistant = assistant or assistant_from_environment()

    def on_action(request, _expand, _accept, _reject, _open, _retry, _dismiss, context):
        value = ctx.triggered[0]["value"] if ctx.triggered else None
        return view_outputs(handle_action(assistant, ctx.triggered_id, value, request, context))

    app.callback(
        Output(ids.ASSISTANT_MODAL, "className", allow_duplicate=True),
        Output(ids.ASSISTANT_MODAL_TITLE, "children"),
        Output(ids.ASSISTANT_MODAL_BODY, "children"),
        Output(ids.ASSISTANT_MODAL_MESSAGE, "children"),
        Output(ids.ASSISTANT_EXPAND_BUTTON, "style"),
        Output(ids.ASSISTANT_ACCEPT_BUTTON, "style"),
        Output(ids.ASSISTANT_REJECT_BUTTON, "style"),
        Output(ids.ASSISTANT_CONTEXT, "data"),
        Output(ids.AGENTS_INTERVAL, "disabled", allow_duplicate=True),
        Output(ids.AGENTS_REFRESH, "data"),
        Input(ids.ASSISTANT_REQUEST, "data"),
        Input(ids.ASSISTANT_EXPAND_BUTTON, "n_clicks"),
        Input(ids.ASSISTANT_ACCEPT_BUTTON, "n_clicks"),
        Input(ids.ASSISTANT_REJECT_BUTTON, "n_clicks"),
        Input({"type": ids.AGENT_OPEN, "index": ALL}, "n_clicks"),
        Input({"type": ids.AGENT_RETRY, "index": ALL}, "n_clicks"),
        Input({"type": ids.AGENT_DISMISS, "index": ALL}, "n_clicks"),
        State(ids.ASSISTANT_CONTEXT, "data"),
        prevent_initial_call=True,
    )(on_action)

    app.callback(
        Output(ids.AGENTS_PANEL, "style"),
        Output(ids.AGENTS_SUMMARY, "children"),
        Output(ids.AGENTS_LIST, "children"),
        Output(ids.AGENTS_STATE, "data"),
        Output(ids.AGENTS_INTERVAL, "disabled"),
        Input(ids.AGENTS_INTERVAL, "n_intervals"),
        Input(ids.AGENTS_REFRESH, "data"),
        State(ids.AGENTS_STATE, "data"),
    )(lambda _intervals, _refresh, previous: agents_outputs(assistant, previous))

    app.clientside_callback(
        CLOSE_JS,
        Output(ids.ASSISTANT_MODAL, "className"),
        Input(ids.ASSISTANT_CLOSE_BUTTON, "n_clicks"),
        prevent_initial_call=True,
    )
    app.clientside_callback(NOTIFY_JS, Input(ids.AGENTS_STATE, "data"))
