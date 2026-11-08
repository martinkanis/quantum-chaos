"""Step labels of the hand-written pages of the topic Fotonika, which the page tests check."""

from ui.generated_topics import GENERATED_TOPICS
from ui.navigation import PHOTONICS_TOPIC_ANCHOR

HAND_WRITTEN_PAGES = 12


def photonics_step(number: int) -> str:
    """Accepted topics and lecture notes join the topic after the hand-written pages and only add to the total."""
    added = sum(1 for topic in GENERATED_TOPICS if topic.placement.topic_anchor == PHOTONICS_TOPIC_ANCHOR)
    return f"Fotonika · krok {number} / {HAND_WRITTEN_PAGES + added}"
