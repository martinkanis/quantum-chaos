"""Topic pages written by the assistant: their content, validation and the JSON files in content/topics."""

from __future__ import annotations

import json
import logging
import re
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Collection, Iterable, Mapping, Optional, Tuple

TOPICS_DIRECTORY = Path(__file__).resolve().parent.parent / "content" / "topics"
REPOSITORY_DIRECTORY = "content/topics"
"""The same directory as a path inside the git repository, where accepted topics are committed."""

MAX_SLUG_LENGTH = 60
MAX_TITLE_LENGTH = 120
MAX_DESCRIPTION_LENGTH = 400
MAX_IN_SHORT_LENGTH = 2000
MAX_SECTIONS = 10
MAX_HEADING_LENGTH = 160
MAX_BODY_LENGTH = 12000
MAX_SOURCES = 30
MAX_SELECTION_LENGTH = 2000
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
URL_PATTERN = re.compile(r"^https?://\S+$")

logger = logging.getLogger(__name__)


class TopicError(ValueError):
    """A topic page that cannot be shown; the message says what is wrong in Czech."""


@dataclass(frozen=True)
class TopicSection:
    heading: str
    body: str
    """Markdown with MathJax formulas."""


@dataclass(frozen=True)
class TopicSource:
    title: str
    url: str
    note: str
    """What the source supports on the page."""


@dataclass(frozen=True)
class Placement:
    """Where the page sits in the app: a group of the menu, a research topic and the page it expands."""

    layer: str
    topic_anchor: Optional[str]
    parent_page_id: Optional[str]


@dataclass(frozen=True)
class Origin:
    page_id: str
    """The page whose selected text the topic expands."""
    selection: str
    created: str
    """ISO date."""
    model: str


@dataclass(frozen=True)
class TopicPage:
    slug: str
    title: str
    description: str
    """One sentence for the menu and the topics dashboard."""
    in_short: str
    sections: Tuple[TopicSection, ...]
    sources: Tuple[TopicSource, ...]
    placement: Placement
    origin: Origin

    @property
    def file_name(self) -> str:
        return f"{self.slug}.json"


def slugify(title: str) -> str:
    """Address part of a title: without diacritics, lower case, words joined by hyphens."""
    words = re.sub(r"[^\w]+", " ", title)
    ascii_title = unicodedata.normalize("NFKD", words).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_title.lower()).strip("-")
    if len(slug) > MAX_SLUG_LENGTH:
        slug = slug[:MAX_SLUG_LENGTH].rsplit("-", 1)[0]
    return slug or "tema"


def unique_slug(slug: str, taken: Collection[str]) -> str:
    candidate, number = slug, 2
    while candidate in taken:
        candidate = f"{slug}-{number}"
        number += 1
    return candidate


def topic_from_dict(data: Mapping[str, Any]) -> TopicPage:
    if not isinstance(data, Mapping):
        raise TopicError("Stránka tématu musí být objekt JSON.")
    sections = tuple(
        TopicSection(
            heading=_text(section, "heading", "Nadpis kapitoly", MAX_HEADING_LENGTH),
            body=_text(section, "body", "Text kapitoly", MAX_BODY_LENGTH),
        )
        for section in _list(data, "sections", "Kapitoly")
    )
    if not 1 <= len(sections) <= MAX_SECTIONS:
        raise TopicError(f"Stránka musí mít 1 až {MAX_SECTIONS} kapitol, má jich {len(sections)}.")
    sources = tuple(_source(source) for source in _list(data, "sources", "Zdroje"))
    if len(sources) > MAX_SOURCES:
        raise TopicError(f"Stránka smí mít nejvýš {MAX_SOURCES} zdrojů, má jich {len(sources)}.")
    slug = _text(data, "slug", "Adresa stránky", MAX_SLUG_LENGTH)
    if not SLUG_PATTERN.match(slug):
        raise TopicError(f"Adresa stránky „{slug}“ smí obsahovat jen malá písmena bez diakritiky, číslice a pomlčky.")
    placement = _mapping(data, "placement", "Zařazení")
    origin = _mapping(data, "origin", "Původ")
    return TopicPage(
        slug=slug,
        title=_text(data, "title", "Název", MAX_TITLE_LENGTH),
        description=_text(data, "description", "Popis", MAX_DESCRIPTION_LENGTH),
        in_short=_text(data, "in_short", "V kostce", MAX_IN_SHORT_LENGTH),
        sections=sections,
        sources=sources,
        placement=Placement(
            layer=_text(placement, "layer", "Skupina", MAX_SLUG_LENGTH),
            topic_anchor=_optional_text(placement, "topic_anchor"),
            parent_page_id=_optional_text(placement, "parent_page_id"),
        ),
        origin=Origin(
            page_id=_text(origin, "page_id", "Zdrojová stránka", MAX_HEADING_LENGTH),
            selection=_text(origin, "selection", "Označený text", MAX_SELECTION_LENGTH),
            created=_text(origin, "created", "Datum", MAX_SLUG_LENGTH),
            model=_text(origin, "model", "Model", MAX_SLUG_LENGTH),
        ),
    )


def topic_to_dict(topic: TopicPage) -> dict:
    """Plain JSON data (lists, not tuples), as stored in the job database and in the topic file."""
    return json.loads(json.dumps(asdict(topic)))


def topic_to_json(topic: TopicPage) -> str:
    return json.dumps(topic_to_dict(topic), ensure_ascii=False, indent=2) + "\n"


def load_topics(directory: Path = TOPICS_DIRECTORY) -> Tuple[TopicPage, ...]:
    """Accepted topics in the order they were created; a broken file is logged and left out, not fatal."""
    topics = []
    for path in sorted(directory.glob("*.json")) if directory.is_dir() else []:
        try:
            topic = topic_from_dict(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, ValueError) as error:
            logger.error("Topic file %s skipped: %s", path.name, error)
            continue
        if topic.file_name != path.name:
            logger.error("Topic file %s skipped: its slug is %s", path.name, topic.slug)
            continue
        topics.append(topic)
    return tuple(sorted(topics, key=lambda topic: (topic.origin.created, topic.slug)))


def _source(data: Any) -> TopicSource:
    url = _text(data, "url", "Odkaz zdroje", 2000)
    if not URL_PATTERN.match(url):
        raise TopicError(f"Odkaz zdroje „{url}“ musí začínat http:// nebo https://.")
    return TopicSource(
        title=_text(data, "title", "Název zdroje", MAX_HEADING_LENGTH * 2),
        url=url,
        note=_text(data, "note", "Poznámka ke zdroji", MAX_DESCRIPTION_LENGTH, required=False),
    )


def _mapping(data: Mapping[str, Any], key: str, label: str) -> Mapping[str, Any]:
    value = data.get(key)
    if not isinstance(value, Mapping):
        raise TopicError(f"{label} chybí nebo nemá správný tvar.")
    return value


def _list(data: Mapping[str, Any], key: str, label: str) -> Iterable[Any]:
    value = data.get(key)
    if not isinstance(value, (list, tuple)):
        raise TopicError(f"{label} musí být seznam.")
    return value


def _text(data: Any, key: str, label: str, max_length: int, required: bool = True) -> str:
    value = data.get(key) if isinstance(data, Mapping) else None
    if not isinstance(value, str) or (required and not value.strip()):
        raise TopicError(f"{label} chybí.")
    value = value.strip()
    if len(value) > max_length:
        raise TopicError(f"{label} je moc dlouhý: {len(value)} znaků, povoleno je nejvýš {max_length}.")
    return value


def _optional_text(data: Mapping[str, Any], key: str) -> Optional[str]:
    value = data.get(key)
    return value.strip() if isinstance(value, str) and value.strip() else None
