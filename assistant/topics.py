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
MAX_LECTURE_SECTIONS = 20
"""Notes follow the chapters of a recorded lecture, which can have more of them than an expanded topic."""
MAX_SLIDES_PER_SECTION = 40
MAX_KEY_POINTS = 10
MAX_LECTURE_SECONDS = 9999
"""Frames are named slajd_SSSS.jpg after the second they come from (web/lecture_slides.py), so four digits."""
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
URL_PATTERN = re.compile(r"^https?://\S+$")
SLIDE_FILE_PATTERN = re.compile(r"^slajd_\d{4}\.jpg$")
ISO_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

logger = logging.getLogger(__name__)


class TopicError(ValueError):
    """A topic page that cannot be shown; the message says what is wrong in Czech."""


@dataclass(frozen=True)
class SectionSlide:
    file_name: str
    """slajd_SSSS.jpg in content/lectures/<folder>/slajdy, SSSS being the second of the recording."""
    caption: str

    @property
    def seconds(self) -> int:
        return int(self.file_name[len("slajd_"):len("slajd_") + 4])


@dataclass(frozen=True)
class TopicSection:
    heading: str
    body: str
    """Markdown with MathJax formulas."""
    start: Optional[int] = None
    """Second of the recording where the chapter starts; only in lecture notes."""
    slides: Tuple[SectionSlide, ...] = ()


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
    section_title: Optional[str] = None
    """Section of the research topic the page joins; without it the page joins the expanded topics section."""
    topic_title: Optional[str] = None
    """Title of a research topic of its own, used when topic_anchor names no existing topic."""
    topic_summary: Optional[str] = None


@dataclass(frozen=True)
class KeyPoint:
    """One point of the TL;DR on top of lecture notes; section is the 1-based chapter that explains it."""

    text: str
    section: int


@dataclass(frozen=True)
class Lecture:
    """The recorded lecture that a topic page takes notes from."""

    folder: str
    """content/lectures/<folder> holds the frames (slajdy/) and the presentation (prezentace.pptx)."""
    video_url: str
    video_seconds: int
    speaker: str
    event: str
    recorded: str
    """ISO date of the talk."""
    language: str
    how_made: str
    """How the notes were made: transcription, frames, what was left out."""
    has_presentation: bool
    key_points: Tuple[KeyPoint, ...]
    related_page_id: Optional[str] = None
    """The page of the app whose topic the lecture explains most; the knowledge map connects the notes to it."""


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
    lecture: Optional[Lecture] = None
    """Set for notes from a recorded lecture; their chapters then carry times and frames."""

    @property
    def file_name(self) -> str:
        return f"{self.slug}.json"


def section_end(topic: TopicPage, number: int) -> int:
    """Second where the 1-based chapter of lecture notes ends: the next chapter's start or the end of the video."""
    later = [section.start for section in topic.sections[number:] if section.start is not None]
    return later[0] if later else topic.lecture.video_seconds


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
    lecture = _lecture(data["lecture"]) if data.get("lecture") is not None else None
    sections = tuple(_section(section) for section in _list(data, "sections", "Kapitoly"))
    max_sections = MAX_LECTURE_SECTIONS if lecture else MAX_SECTIONS
    if not 1 <= len(sections) <= max_sections:
        raise TopicError(f"Stránka musí mít 1 až {max_sections} kapitol, má jich {len(sections)}.")
    if lecture:
        _check_lecture_sections(lecture, sections)
    sources = tuple(_source(source) for source in _list(data, "sources", "Zdroje"))
    if len(sources) > MAX_SOURCES:
        raise TopicError(f"Stránka smí mít nejvýš {MAX_SOURCES} zdrojů, má jich {len(sources)}.")
    slug = _text(data, "slug", "Adresa stránky", MAX_SLUG_LENGTH)
    if not SLUG_PATTERN.match(slug):
        raise TopicError(f"Adresa stránky „{slug}“ smí obsahovat jen malá písmena bez diakritiky, číslice a pomlčky.")
    placement = _mapping(data, "placement", "Zařazení")
    if _optional_text(placement, "topic_title") and not _optional_text(placement, "topic_anchor"):
        raise TopicError("Nové téma potřebuje kromě názvu i kotvu (topic_anchor).")
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
            section_title=_optional_text(placement, "section_title"),
            topic_title=_optional_text(placement, "topic_title"),
            topic_summary=_optional_text(placement, "topic_summary"),
        ),
        origin=Origin(
            page_id=_text(origin, "page_id", "Zdrojová stránka", MAX_HEADING_LENGTH),
            selection=_text(origin, "selection", "Označený text", MAX_SELECTION_LENGTH),
            created=_text(origin, "created", "Datum", MAX_SLUG_LENGTH),
            model=_text(origin, "model", "Model", MAX_SLUG_LENGTH),
        ),
        lecture=lecture,
    )


def topic_to_dict(topic: TopicPage) -> dict:
    """Plain JSON data (lists, not tuples), as stored in the job database and in the topic file.

    Fields that only lecture notes and pages of a topic of their own use are left out when empty, so that the files
    of other topics stay as they were.
    """
    data = json.loads(json.dumps(asdict(topic)))
    if data["lecture"] is None:
        del data["lecture"]
    for section in data["sections"]:
        if section["start"] is None:
            del section["start"]
        if not section["slides"]:
            del section["slides"]
    for key in ("section_title", "topic_title", "topic_summary"):
        if data["placement"][key] is None:
            del data["placement"][key]
    return data


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


def _section(data: Any) -> TopicSection:
    start = data.get("start") if isinstance(data, Mapping) else None
    if start is not None and not _is_whole_number(start):
        raise TopicError(f"Začátek kapitoly musí být celé číslo sekund, je „{start}“.")
    slides = tuple(_slide(slide) for slide in _list(data, "slides", "Snímky kapitoly", default=()))
    if len(slides) > MAX_SLIDES_PER_SECTION:
        raise TopicError(f"Kapitola smí mít nejvýš {MAX_SLIDES_PER_SECTION} snímků, má jich {len(slides)}.")
    return TopicSection(
        heading=_text(data, "heading", "Nadpis kapitoly", MAX_HEADING_LENGTH),
        body=_text(data, "body", "Text kapitoly", MAX_BODY_LENGTH),
        start=start,
        slides=slides,
    )


def _slide(data: Any) -> SectionSlide:
    file_name = _text(data, "file_name", "Soubor snímku", MAX_SLUG_LENGTH)
    if not SLIDE_FILE_PATTERN.match(file_name):
        raise TopicError(f"Snímek „{file_name}“ se musí jmenovat slajd_SSSS.jpg podle sekundy záznamu.")
    return SectionSlide(file_name=file_name, caption=_text(data, "caption", "Popisek snímku", MAX_HEADING_LENGTH))


def _lecture(data: Any) -> Lecture:
    folder = _text(data, "folder", "Složka přednášky", MAX_SLUG_LENGTH)
    if not SLUG_PATTERN.match(folder):
        raise TopicError(f"Složka přednášky „{folder}“ smí obsahovat jen malá písmena bez diakritiky, číslice a pomlčky.")
    video_url = _text(data, "video_url", "Odkaz na video", 2000)
    if not URL_PATTERN.match(video_url):
        raise TopicError(f"Odkaz na video „{video_url}“ musí začínat http:// nebo https://.")
    video_seconds = data.get("video_seconds")
    if not _is_whole_number(video_seconds) or not 1 <= video_seconds <= MAX_LECTURE_SECONDS:
        raise TopicError(f"Délka videa musí být 1 až {MAX_LECTURE_SECONDS} sekund, je „{video_seconds}“.")
    recorded = _text(data, "recorded", "Datum přednášky", MAX_SLUG_LENGTH)
    if not ISO_DATE_PATTERN.match(recorded):
        raise TopicError(f"Datum přednášky „{recorded}“ musí mít tvar RRRR-MM-DD.")
    key_points = tuple(
        KeyPoint(text=_text(point, "text", "Bod TL;DR", MAX_DESCRIPTION_LENGTH), section=_key_point_section(point))
        for point in _list(data, "key_points", "TL;DR")
    )
    if len(key_points) > MAX_KEY_POINTS:
        raise TopicError(f"TL;DR smí mít nejvýš {MAX_KEY_POINTS} bodů, má jich {len(key_points)}.")
    has_presentation = data.get("has_presentation")
    if not isinstance(has_presentation, bool):
        raise TopicError("U přednášky chybí, jestli má prezentaci (has_presentation: true nebo false).")
    return Lecture(
        folder=folder,
        video_url=video_url,
        video_seconds=video_seconds,
        speaker=_text(data, "speaker", "Přednášející", MAX_HEADING_LENGTH),
        event=_text(data, "event", "Kde přednáška zazněla", MAX_HEADING_LENGTH * 2),
        recorded=recorded,
        language=_text(data, "language", "Jazyk přednášky", MAX_SLUG_LENGTH),
        how_made=_text(data, "how_made", "Jak zápisky vznikly", MAX_IN_SHORT_LENGTH),
        has_presentation=has_presentation,
        key_points=key_points,
        related_page_id=_optional_text(data, "related_page_id"),
    )


def _key_point_section(data: Mapping[str, Any]) -> int:
    section = data.get("section")
    if not _is_whole_number(section) or section < 1:
        raise TopicError(f"Bod TL;DR musí odkazovat na číslo kapitoly od 1, odkazuje na „{section}“.")
    return section


def _check_lecture_sections(lecture: Lecture, sections: Tuple[TopicSection, ...]) -> None:
    """Chapters of the talk come first, each starting later than the previous one and inside the recording, with
    frames from its own part; chapters of our own (without a start and frames) may follow them."""
    timed = [section for section in sections if section.start is not None]
    if not timed or any(section.start is None for section in sections[:len(timed)]):
        raise TopicError("Zápisky začínají kapitolami přednášky se začátkem (start); vlastní kapitoly bez něj jdou až za ně.")
    if any(section.slides for section in sections[len(timed):]):
        raise TopicError("Snímky z přednášky patří jen do kapitol se začátkem ve videu.")
    starts = [section.start for section in timed]
    if starts != sorted(set(starts)) or starts[-1] >= lecture.video_seconds:
        raise TopicError("Začátky kapitol musí jít po sobě a ležet uvnitř záznamu.")
    ends = starts[1:] + [lecture.video_seconds]
    for section, start, end in zip(timed, starts, ends):
        outside = [slide.file_name for slide in section.slides if not start <= slide.seconds < end]
        if outside:
            raise TopicError(f"Snímky {', '.join(outside)} nejsou z kapitoly „{section.heading}“.")
    for point in lecture.key_points:
        if point.section > len(sections):
            raise TopicError(f"Bod TL;DR odkazuje na kapitolu {point.section}, stránka jich má {len(sections)}.")


def _is_whole_number(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


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


def _list(data: Mapping[str, Any], key: str, label: str, default: Optional[Iterable[Any]] = None) -> Iterable[Any]:
    value = data.get(key) if isinstance(data, Mapping) else None
    if value is None and default is not None:
        return default
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
