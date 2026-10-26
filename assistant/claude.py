"""Calls to Claude: an explanation of a selection, and an agent run that researches and writes a topic page."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any, List, Mapping, Optional, Sequence

from assistant.prompts import (
    EXPLAIN_SYSTEM,
    SUBMIT_REMINDER,
    TOPIC_SYSTEM,
    TOPIC_TOOL,
    TOPIC_TOOL_NAME,
    explain_message,
    topic_message,
)
from assistant.selection import SelectionContext

API_KEY_ENV = "ANTHROPIC_API_KEY"
MODEL = os.environ.get("ASSISTANT_MODEL") or "claude-opus-5-5"
FALLBACK_BETA = "server-side-fallback-2026-07-01"
"""When a safety classifier declines a request, the API retries it on a fallback model chosen by the refusal kind."""
EXPLAIN_EFFORT = "low"
"""The reader waits in the pop-up, so the explanation should come within seconds."""
TOPIC_EFFORT = "high"
EXPLAIN_MAX_TOKENS = 4000
TOPIC_MAX_TOKENS = 16000
EXPLAIN_TIMEOUT_SECONDS = 60.0
EXPLAIN_RETRIES = 1
"""The explanation is a callback the reader waits for, so it gives up sooner than an agent."""
TOPIC_TIMEOUT_SECONDS = 600.0
TOPIC_RETRIES = 2
MAX_WEB_SEARCHES = 8
MAX_REQUESTS = 6
"""A long web search pauses the turn (pause_turn); each continuation is one more request."""
WEB_SEARCH_TOOL = {"type": "web_search_20260209", "name": "web_search", "max_uses": MAX_WEB_SEARCHES}

logger = logging.getLogger(__name__)


class AssistantError(ValueError):
    """Claude could not answer; the message says why and what to do, in Czech."""


@dataclass(frozen=True)
class TopicDraft:
    content: Mapping[str, Any]
    """Input of the submit tool: title, description, in_short, sections and sources."""
    model: str


def is_configured() -> bool:
    return bool(os.environ.get(API_KEY_ENV))


def make_client(timeout: float, max_retries: int) -> Any:
    if not is_configured():
        raise AssistantError(
            f"Asistent není nastavený: službě chybí proměnná prostředí {API_KEY_ENV} s klíčem k Claude API."
        )
    import anthropic  # Imported on first use: the SDK costs memory that most requests never need.

    return anthropic.Anthropic(timeout=timeout, max_retries=max_retries)


def explain(context: SelectionContext, client: Optional[Any] = None) -> str:
    response = _create(
        client or make_client(EXPLAIN_TIMEOUT_SECONDS, EXPLAIN_RETRIES),
        system=EXPLAIN_SYSTEM,
        messages=[{"role": "user", "content": explain_message(context)}],
        effort=EXPLAIN_EFFORT,
        max_tokens=EXPLAIN_MAX_TOKENS,
    )
    text = "".join(block.text for block in response.content if block.type == "text").strip()
    if not text:
        raise AssistantError("Claude nevrátil žádné vysvětlení. Zkus to znovu.")
    return text


def write_topic(
    context: SelectionContext,
    explanation: Optional[str],
    existing_pages: Sequence[str],
    client: Optional[Any] = None,
) -> TopicDraft:
    """Lets Claude search the web and submit the page through a strict tool, continuing paused turns."""
    client = client or make_client(TOPIC_TIMEOUT_SECONDS, TOPIC_RETRIES)
    messages: List[dict] = [{"role": "user", "content": topic_message(context, explanation, existing_pages)}]
    reminded = False
    for _ in range(MAX_REQUESTS):
        response = _create(
            client,
            system=TOPIC_SYSTEM,
            messages=messages,
            effort=TOPIC_EFFORT,
            max_tokens=TOPIC_MAX_TOKENS,
            tools=[WEB_SEARCH_TOOL, TOPIC_TOOL],
        )
        submitted = next(
            (block.input for block in response.content if block.type == "tool_use" and block.name == TOPIC_TOOL_NAME),
            None,
        )
        if submitted is not None:
            return TopicDraft(content=submitted, model=response.model)
        messages.append({"role": "assistant", "content": response.content})
        if response.stop_reason == "pause_turn":
            continue
        if reminded:
            break
        messages.append({"role": "user", "content": SUBMIT_REMINDER})
        reminded = True
    raise AssistantError("Agent stránku neodevzdal. Spusť ho znovu, případně označ kratší nebo jasnější úryvek.")


def _create(
    client: Any,
    *,
    system: str,
    messages: List[dict],
    effort: str,
    max_tokens: int,
    tools: Optional[list] = None,
) -> Any:
    import anthropic

    request = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "system": system,
        "messages": messages,
        "output_config": {"effort": effort},
        "betas": [FALLBACK_BETA],
        "fallbacks": "default",
    }
    if tools:
        request["tools"] = tools
    try:
        response = client.beta.messages.create(**request)
    except anthropic.AuthenticationError as error:
        raise AssistantError(f"Claude odmítl klíč z {API_KEY_ENV}. Zkontroluj ho v nastavení služby.") from error
    except anthropic.PermissionDeniedError as error:
        raise AssistantError("Klíč k Claude API nemá oprávnění k tomuto modelu nebo nástroji.") from error
    except anthropic.RateLimitError as error:
        raise AssistantError("Claude API teď hlásí překročený limit. Zkus to za minutu znovu.") from error
    except anthropic.APITimeoutError as error:
        raise AssistantError("Claude neodpověděl včas. Zkus to znovu.") from error
    except anthropic.APIConnectionError as error:
        raise AssistantError("Nepodařilo se spojit s Claude API. Zkus to znovu.") from error
    except anthropic.APIStatusError as error:
        logger.error("Claude API error %s (request %s): %s", error.status_code, error.request_id, error.message)
        raise AssistantError(f"Claude API vrátilo chybu {error.status_code}. Zkus to znovu.") from error
    if response.stop_reason == "refusal":
        raise AssistantError("Claude odmítl na tenhle úryvek odpovědět. Zkus označit jiný text.")
    return response
