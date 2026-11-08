"""Topic pages that the assistant wrote and the reader accepted (content/topics): their ids and addresses.

They are read once when the app starts; an accepted topic reaches the app through a commit and a redeploy.
"""

from __future__ import annotations

from typing import Dict, Tuple

from assistant.topics import TopicPage, load_topics

GENERATED_PATH_PREFIX = "/rozvedena-temata/"
LECTURE_NOTES_PATH_PREFIX = "/zapisky/"
GENERATED_SECTION_TITLE = "Rozvedená témata"

GENERATED_TOPICS: Tuple[TopicPage, ...] = load_topics()


def generated_page_id(slug: str) -> str:
    return f"rozvedene-tema-{slug}-page"


def generated_path(slug: str) -> str:
    return f"{GENERATED_PATH_PREFIX}{slug}"


def topic_path(topic: TopicPage) -> str:
    """Notes from a lecture have addresses of their own; other accepted topics sit under the expanded topics."""
    return f"{LECTURE_NOTES_PATH_PREFIX}{topic.slug}" if topic.lecture else generated_path(topic.slug)


def generated_page_ids(topics: Tuple[TopicPage, ...] = GENERATED_TOPICS) -> Tuple[str, ...]:
    return tuple(generated_page_id(topic.slug) for topic in topics)


def generated_paths(topics: Tuple[TopicPage, ...] = GENERATED_TOPICS) -> Dict[str, str]:
    """Address → page id of every accepted topic."""
    return {topic_path(topic): generated_page_id(topic.slug) for topic in topics}


def published_slugs(topics: Tuple[TopicPage, ...] = GENERATED_TOPICS) -> Tuple[str, ...]:
    return tuple(topic.slug for topic in topics)
