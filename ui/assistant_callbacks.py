"""Callbacks of the assistant: explaining a selection, starting agents, previewing, accepting and rejecting pages.

Every action of the pop-up and of the agents page goes through one callback, so the pop-up has a single owner;
the work behind each action is in plain functions that return a View, which the tests call directly.
"""

from __future__ import annotations

import logging
import re
import time
from dataclasses import asdict, dataclass, replace
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
from assistant.topics import (
    Placement,
    TopicError,
    TopicPage,
    placement_with_summary,
    topic_from_dict,
    topic_to_dict,
    unique_slug,
)
from ui import ids
from ui.agents_page import agent_history, agents_link_label
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
    PLACEMENT_HINT,
    PREVIEW_TITLE,
    REJECTED,
    RUNNING_AGENTS_WARNING,
    STILL_RUNNING,
)
from ui.assistant_panel import MODAL_CLASS, OPEN_MODAL_CLASS
from ui.generated_page import generated_page_content
from ui.generated_topics import generated_path, published_slugs
from ui.knowledge_map_content import LAYERS
from ui.navigation import AGENTS_PATH, HIDDEN, VISIBLE
from ui.topic_catalog import (
    TopicChoice,
    TopicChoiceError,
    choice_of,
    default_choice,
    page_entries,
    placement_for,
    placement_with_choice,
)

AGENTS_SHOWN = 100
"""Runs listed on the agents page, from the newest; hidden runs are left out by the store."""
QUOTE_LENGTH = 300
DISPLAY_FORMULA = re.compile(r"\s*\$\$(.+?)\$\$\s*")
"""A display formula as the browser sends it, on one line; dcc.Markdown typesets it only on lines of its own."""
EXPAND, START, ACCEPT, REJECT = "expand", "start", "accept", "reject"
ACTION_BUTTONS = (EXPAND, START, ACCEPT, REJECT)
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
    """The action buttons to show (EXPAND, START, ACCEPT, REJECT); the close button is always there."""
    placement: Any = no_update
    """Whether the topic chooser is shown, with the choice it starts from."""
    choice: Any = no_update
    context: Any = no_update
    poll: bool = False
    """Start polling the agents, because one of them is now running or deploying."""
    refresh: bool = False


def dialog(title: str, body: List, message: str = "", buttons: FrozenSet[str] = frozenset(), **changes: Any) -> View:
    """A dialog hides the topic chooser unless it asks for it (placement=True with the choice to start from)."""
    return View(open=True, title=title, body=body, message=message, buttons=buttons, **{"placement": False, **changes})


def view_outputs(view: View) -> Tuple:
    modal_class = no_update if view.open is no_update else (OPEN_MODAL_CLASS if view.open else MODAL_CLASS)
    if view.buttons is no_update:
        button_styles: Tuple = (no_update,) * len(ACTION_BUTTONS)
    else:
        button_styles = tuple(VISIBLE if button in view.buttons else HIDDEN for button in ACTION_BUTTONS)
    placement_style = no_update if view.placement is no_update else (VISIBLE if view.placement else HIDDEN)
    choice = view.choice if isinstance(view.choice, TopicChoice) else None
    return (
        modal_class, view.title, view.body, view.message, *button_styles, placement_style,
        choice.anchor if choice else no_update, choice.new_title if choice else no_update, view.context,
        False if view.poll else no_update,
        time.time() if view.poll or view.refresh else no_update,
    )


def handle_action(
    assistant: Assistant,
    trigger: Any,
    value: Any,
    request: Optional[Mapping],
    context: Optional[Mapping],
    choice: Optional[TopicChoice] = None,
) -> View:
    """Dispatches one click or request; a re-rendered agents list re-fires the callback without a click."""
    if trigger == ids.ASSISTANT_REQUEST:
        return ask(assistant, request or {})
    if not value:
        return View()
    context = context or {}
    if trigger == ids.ASSISTANT_EXPAND_BUTTON:
        return offer_placement(context.get("selection"), context.get("explanation"))
    if trigger == ids.ASSISTANT_START_BUTTON:
        return start_agent(assistant, context.get("selection"), context.get("explanation"), choice)
    if trigger == ids.ASSISTANT_ACCEPT_BUTTON:
        return accept(assistant, context.get("job_id"), choice)
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
        return offer_placement(selection_to_dict(selection), None)
    try:
        explanation = assistant.explain(selection)
    except AssistantError as error:
        return dialog(title, [quote(selection.selection, selection.has_formula)], str(error))
    return dialog(
        title,
        [
            quote(selection.selection, selection.has_formula),
            dcc.Markdown(explanation, mathjax=True, link_target="_blank", className="assistant-explanation"),
            html.P(EXPLANATION_NOTE, className="hint small"),
        ],
        buttons=frozenset({EXPAND}),
        context={"selection": selection_to_dict(selection), "explanation": explanation},
    )


def offer_placement(selection: Any, explanation: Optional[str]) -> View:
    """Before an agent starts, the reader picks the research topic the new page will join."""
    try:
        context = selection_from_request(selection)
        if placement_for(context.page_id) is None:
            raise SelectionError(NO_PLACEMENT)
    except SelectionError as error:
        return dialog(EXPAND_TITLE, [], str(error))
    return dialog(
        EXPAND_TITLE,
        [quote(context.selection, context.has_formula), html.P(PLACEMENT_HINT, className="hint")],
        buttons=frozenset({START}),
        placement=True,
        choice=default_choice(),
        context={"selection": selection_to_dict(context), "explanation": explanation},
    )


def start_agent(
    assistant: Assistant, selection: Any, explanation: Optional[str], choice: Optional[TopicChoice] = None
) -> View:
    try:
        context = selection_from_request(selection)
        placement = placement_for(context.page_id)
        if placement is None:
            raise SelectionError(NO_PLACEMENT)
        placement = placement_with_choice(placement, choice)
    except (SelectionError, TopicChoiceError) as error:
        return _placement_problem(selection, explanation, str(error))
    try:
        existing_pages = [entry.title for entry in page_entries().values()]
        job = assistant.runner.start(agent_request(selection, explanation, placement, existing_pages))
    except JobError as error:
        return dialog(EXPAND_TITLE, [], str(error))
    return dialog(
        EXPAND_TITLE,
        [quote(context.selection, context.has_formula), html.P(AGENT_STARTED)],
        context={"job_id": job.id},
        poll=True,
    )


def show_job(assistant: Assistant, job_id: Optional[str], message: str = "", **changes: Any) -> View:
    """A proposal waiting for approval comes with the topic chooser set to where the agent placed it."""
    job = _job(assistant, job_id)
    if job is None:
        return dialog(AGENT_TITLE, [], MISSING_JOB)
    context = {"job_id": job.id}
    requested = job.request.get("selection") or {}
    selection = quote(requested.get("selection", ""), requested.get("has_formula") is True)
    if job.status == JobStatus.READY:
        try:
            topic = topic_from_dict(job.result or {})
        except TopicError as error:
            return dialog(PREVIEW_TITLE, [selection], str(error), context=context, **changes)
        body = [
            html.P(_accept_hint(assistant, topic, job), className="hint"),
            html.Div(className="assistant-preview", children=generated_page_content(topic, with_anchors=False)),
        ]
        chooser = {"placement": True, "choice": choice_of(topic.placement), **changes}
        return dialog(PREVIEW_TITLE, body, message, frozenset({ACCEPT, REJECT}), context=context, **chooser)
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


def accept(assistant: Assistant, job_id: Optional[str], choice: Optional[TopicChoice] = None) -> View:
    """Publishes the proposal in the topic chosen now; a choice that fails keeps the proposal and the typed title."""
    job = _job(assistant, job_id)
    if job is None or job.status != JobStatus.READY:
        return show_job(assistant, job_id, NOT_READY)
    try:
        topic = topic_from_dict(job.result or {})
        topic = replace(topic, placement=_chosen_placement(topic, choice))
        taken = published_slugs()
        if topic.slug in taken:
            topic = replace(topic, slug=unique_slug(topic.slug, taken))
        commit_url = assistant.publish(topic)
        assistant.store.update(job.id, {
            "status": JobStatus.DEPLOYING, "commit_url": commit_url, "result": topic_to_dict(topic),
        })
    except TopicChoiceError as error:
        return show_job(assistant, job_id, str(error), choice=choice)
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


def refresh_agents(assistant: Assistant, trigger: Any, pathname: Optional[str], previous: Optional[Mapping]) -> Tuple:
    """A page switch reads the agents only when it leads to their page; the timer, actions and the load always do."""
    if trigger == ids.URL and pathname != AGENTS_PATH:
        return (no_update,) * len(AGENTS_OUTPUTS)
    return agents_outputs(assistant, previous)


def agents_outputs(assistant: Assistant, previous: Optional[Mapping]) -> Tuple:
    """Menu link, history, state for notifications and whether polling stops; no redraw if nothing changed."""
    try:
        jobs = assistant.store.recent(AGENTS_SHOWN)
    except JobError as error:
        return no_update, html.P(str(error), className="error-message"), no_update, False
    signature = [[job.id, job.status.value, job.updated_at.isoformat()] for job in jobs]
    stop_polling = not any(job.status in ACTIVE for job in jobs)
    if previous and previous.get("signature") == signature:
        return no_update, no_update, no_update, stop_polling
    state = {
        "signature": signature,
        "ready": [_notice(job) for job in jobs if job.status == JobStatus.READY],
        "deployed": [_notice(job) for job in jobs if job.status == JobStatus.DEPLOYED],
    }
    return agents_link_label(jobs), agent_history(jobs), state, stop_polling


def quote(text: str, with_formulas: bool = False) -> html.Blockquote:
    """The selection as the reader saw it; with formulas it is typeset whole, so that no TeX is cut in half."""
    if with_formulas:
        return html.Blockquote(dcc.Markdown(formula_blocks(text), mathjax=True), className="assistant-quote")
    short = text if len(text) <= QUOTE_LENGTH else text[:QUOTE_LENGTH].rsplit(" ", 1)[0] + "…"
    return html.Blockquote(short, className="assistant-quote")


def formula_blocks(text: str) -> str:
    """Markdown of a selection with its display formulas on lines of their own, as dcc.Markdown needs them."""
    return DISPLAY_FORMULA.sub(lambda match: f"\n\n$$\n{match.group(1).strip()}\n$$\n\n", text).strip()


def _placement_problem(selection: Any, explanation: Optional[str], message: str) -> View:
    """The chooser stays open with the reader's choice, so that a missing title can be filled in."""
    view = offer_placement(selection, explanation)
    return replace(view, message=message, choice=no_update) if view.placement else view


def _chosen_placement(topic: TopicPage, choice: Optional[TopicChoice]) -> Placement:
    """The agent's placement with the topic chosen at approval; a topic founded now takes the page's description."""
    if choice is None:
        return topic.placement
    placement = placement_with_choice(asdict(topic.placement), choice)
    return Placement(**placement_with_summary(placement, topic.description))


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


AGENTS_OUTPUTS = (
    (ids.NAV_AGENTS_LINK, "children"), (ids.AGENTS_LIST, "children"), (ids.AGENTS_STATE, "data"),
    (ids.AGENTS_INTERVAL, "disabled"),
)
NOTIFY_JS = "function(state) { if (window.qcAssistant) { window.qcAssistant.notify(state); } }"
CLOSE_JS = "function(clicks) { return clicks ? '" + MODAL_CLASS + "' : window.dash_clientside.no_update; }"


def register_assistant_callbacks(app: Dash, assistant: Optional[Assistant] = None) -> None:
    assistant = assistant or assistant_from_environment()

    def on_action(request, _expand, _start, _accept, _reject, _open, _retry, _dismiss, context, topic, new_topic):
        value = ctx.triggered[0]["value"] if ctx.triggered else None
        choice = TopicChoice(topic or "", new_topic or "")
        return view_outputs(handle_action(assistant, ctx.triggered_id, value, request, context, choice))

    app.callback(
        Output(ids.ASSISTANT_MODAL, "className", allow_duplicate=True),
        Output(ids.ASSISTANT_MODAL_TITLE, "children"),
        Output(ids.ASSISTANT_MODAL_BODY, "children"),
        Output(ids.ASSISTANT_MODAL_MESSAGE, "children"),
        Output(ids.ASSISTANT_EXPAND_BUTTON, "style"),
        Output(ids.ASSISTANT_START_BUTTON, "style"),
        Output(ids.ASSISTANT_ACCEPT_BUTTON, "style"),
        Output(ids.ASSISTANT_REJECT_BUTTON, "style"),
        Output(ids.ASSISTANT_PLACEMENT, "style"),
        Output(ids.ASSISTANT_TOPIC_DROPDOWN, "value"),
        Output(ids.ASSISTANT_NEW_TOPIC_INPUT, "value"),
        Output(ids.ASSISTANT_CONTEXT, "data"),
        Output(ids.AGENTS_INTERVAL, "disabled", allow_duplicate=True),
        Output(ids.AGENTS_REFRESH, "data"),
        Input(ids.ASSISTANT_REQUEST, "data"),
        Input(ids.ASSISTANT_EXPAND_BUTTON, "n_clicks"),
        Input(ids.ASSISTANT_START_BUTTON, "n_clicks"),
        Input(ids.ASSISTANT_ACCEPT_BUTTON, "n_clicks"),
        Input(ids.ASSISTANT_REJECT_BUTTON, "n_clicks"),
        Input({"type": ids.AGENT_OPEN, "index": ALL}, "n_clicks"),
        Input({"type": ids.AGENT_RETRY, "index": ALL}, "n_clicks"),
        Input({"type": ids.AGENT_DISMISS, "index": ALL}, "n_clicks"),
        State(ids.ASSISTANT_CONTEXT, "data"),
        State(ids.ASSISTANT_TOPIC_DROPDOWN, "value"),
        State(ids.ASSISTANT_NEW_TOPIC_INPUT, "value"),
        prevent_initial_call=True,
    )(on_action)

    def on_agents(_intervals, _refresh, pathname, previous):
        return refresh_agents(assistant, ctx.triggered_id, pathname, previous)

    app.callback(
        *[Output(component_id, prop) for component_id, prop in AGENTS_OUTPUTS],
        Input(ids.AGENTS_INTERVAL, "n_intervals"),
        Input(ids.AGENTS_REFRESH, "data"),
        Input(ids.URL, "pathname"),
        State(ids.AGENTS_STATE, "data"),
    )(on_agents)

    app.clientside_callback(
        CLOSE_JS,
        Output(ids.ASSISTANT_MODAL, "className"),
        Input(ids.ASSISTANT_CLOSE_BUTTON, "n_clicks"),
        prevent_initial_call=True,
    )
    app.clientside_callback(NOTIFY_JS, Input(ids.AGENTS_STATE, "data"))
