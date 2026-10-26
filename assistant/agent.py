"""What one agent does: lets Claude write the page and turns the submission into a valid topic page."""

from __future__ import annotations

from datetime import date
from typing import Any, Collection, Mapping, Optional

from assistant.claude import write_topic
from assistant.selection import selection_from_request, selection_to_dict
from assistant.topics import URL_PATTERN, slugify, topic_from_dict, topic_to_dict, unique_slug


def agent_request(
    selection: Mapping[str, Any],
    explanation: Optional[str],
    placement: Mapping[str, Optional[str]],
    existing_pages: Collection[str],
) -> dict:
    """Everything the agent needs, stored with the job so that a retry after a restart can run it again."""
    return {
        "selection": selection_to_dict(selection_from_request(selection)),
        "explanation": explanation or "",
        "placement": dict(placement),
        "existing_pages": list(existing_pages),
    }


def draft_topic(request: Mapping[str, Any], taken_slugs: Collection[str], client: Optional[Any] = None) -> dict:
    context = selection_from_request(request.get("selection"))
    draft = write_topic(context, request.get("explanation") or None, request.get("existing_pages") or [], client)
    content = dict(draft.content)
    # A source without a usable link would fail the whole page; it is dropped instead.
    content["sources"] = [
        source for source in content.get("sources") or []
        if isinstance(source, Mapping) and URL_PATTERN.match(str(source.get("url", "")).strip())
    ]
    page = topic_from_dict({
        **content,
        "slug": unique_slug(slugify(str(content.get("title", ""))), taken_slugs),
        "placement": request.get("placement") or {},
        "origin": {
            "page_id": context.page_id or "neznama-stranka",
            "selection": context.selection,
            "created": date.today().isoformat(),
            "model": draft.model,
        },
    })
    return topic_to_dict(page)
