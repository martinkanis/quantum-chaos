"""Pages of the translated primer on photonic quantum computing: one page per chapter (ui/primer_content.py).

Each page has the chapter's sections with their original numbering, a table of contents and the works the chapter
cites, taken from the bibliography of the original by their numbers.
"""

from __future__ import annotations

import re
from typing import Dict, List, Tuple

from dash import dcc, html

from ui import ids
from ui.navigation import HIDDEN, PAGE_BY_PATH, PHOTONICS_TOPIC_HREF
from ui.primer_appendices_content import CHAPTER as APPENDICES
from ui.primer_chapter1_content import CHAPTER as CHAPTER_1
from ui.primer_chapter2_content import CHAPTER as CHAPTER_2
from ui.primer_chapter3_content import CHAPTER as CHAPTER_3
from ui.primer_chapter4_content import CHAPTER as CHAPTER_4
from ui.primer_content import BIBLIOGRAPHY, TRANSLATION_NOTE, PrimerChapter, PrimerSection
from ui.reading_time import reading_minutes, reading_time_label
from ui.topic_sections import toc_item

PRIMER_CHAPTERS: Dict[str, PrimerChapter] = {
    ids.PRIMER_BASICS_PAGE: CHAPTER_1,
    ids.PRIMER_GAUSSIAN_STATES_PAGE: CHAPTER_2,
    ids.PRIMER_PHASE_SPACE_PAGE: CHAPTER_3,
    ids.PRIMER_GBS_PAGE: CHAPTER_4,
    ids.PRIMER_APPENDICES_PAGE: APPENDICES,
}
"""In the order of the original."""
CITATION = re.compile(r"\[(\d+(?:\s*[,–-]\s*\d+)*)\]")
"""„[29]“, „[1, 2]“ or „[5–7]“ in the text; math like [x, p] or [d] has letters and does not match."""
CODE = re.compile(r"```.*?```|`[^`\n]*`", re.S)
"""Code blocks and inline code, whose lists such as [0, 1, 0] are not citations."""
VERBATIM = re.compile(r"(\$\$.*?\$\$|\$[^$]+\$|```.*?```|`[^`\n]*`|\[[^\[\]]*\]\([^)\s]*\))", re.S)
"""Math, code and Markdown links: the parts of a text whose brackets stay as they are."""


def build_primer_page(page_id: str) -> html.Div:
    chapter = PRIMER_CHAPTERS[page_id]
    return html.Div(
        id=page_id,
        className="gbs-page",
        style=HIDDEN,
        children=[
            _back_link(),
            html.H1(f"{chapter.label}: {chapter.title}"),
            dcc.Markdown(TRANSLATION_NOTE + f" Tato část odpovídá stranám {chapter.original_pages} originálu.",
                         className="hint small"),
            *([dcc.Markdown(markdown_text(chapter.intro), mathjax=True, className="lead primer-text")]
              if chapter.intro.strip() else []),
            _table_of_contents(chapter, _path_of(page_id)),
            *[_section(section) for section in chapter.sections],
            _citations(chapter),
            _back_link(),
        ],
    )


def markdown_text(text: str) -> str:
    """The text with its other brackets escaped: dcc.Markdown would turn „[29]“ into an empty link without them."""
    return "".join(
        part if index % 2 else part.replace("[", "\\[").replace("]", "\\]")
        for index, part in enumerate(VERBATIM.split(text))
    )


def section_heading(section: PrimerSection) -> str:
    if not section.number:
        return section.title
    if len(section.number) == 1 and section.number.isalpha():
        return f"Dodatek {section.number}: {section.title}"
    return f"{section.number} {section.title}"


def cited_numbers(chapter: PrimerChapter) -> List[int]:
    """Numbers of the cited works in the order of their first citation, each once."""
    numbers: List[int] = []
    for text in [chapter.intro] + [section.body for section in chapter.sections]:
        for group in CITATION.findall(CODE.sub("", text)):
            for number in _expanded(group):
                if number not in numbers:
                    numbers.append(number)
    return numbers


def _expanded(group: str) -> List[int]:
    numbers: List[int] = []
    for part in re.split(r"\s*,\s*", group):
        bounds = re.split(r"\s*[–-]\s*", part)
        if len(bounds) == 2:
            numbers.extend(range(int(bounds[0]), int(bounds[1]) + 1))
        else:
            numbers.append(int(part))
    return numbers


def _path_of(page_id: str) -> str:
    return next(path for path, known_id in PAGE_BY_PATH.items() if known_id == page_id)


def _table_of_contents(chapter: PrimerChapter, path: str) -> html.Nav:
    minutes: List[Tuple[PrimerSection, int]] = [
        (section, reading_minutes([section.body])) for section in chapter.sections
    ]
    return html.Nav(className="card toc", children=[
        html.H2("Obsah"),
        html.P(f"Celkem asi {reading_time_label(sum(count for _, count in minutes))}", className="hint small"),
        html.Ol([
            toc_item(section_heading(section), f"{path}#{section.anchor}", count) for section, count in minutes
        ]),
    ])


def _section(section: PrimerSection) -> html.Section:
    return html.Section(id=section.anchor, className="card step theory-section", children=[
        html.H2(section_heading(section)),
        dcc.Markdown(markdown_text(section.body), mathjax=True, className="primer-text"),
    ])


def _citations(chapter: PrimerChapter) -> html.Section:
    items = [f"- [{number}] {BIBLIOGRAPHY[number - 1]}" for number in sorted(cited_numbers(chapter))]
    return html.Section(className="card step theory-section", children=[
        html.H2("Literatura citovaná v této části"),
        html.P("Čísla odpovídají seznamu literatury originálu, na který odkazují čísla v hranatých závorkách.",
               className="hint small"),
        dcc.Markdown(markdown_text("\n".join(items)) if items else "Tato část necituje žádnou literaturu."),
    ])


def _back_link() -> dcc.Link:
    return dcc.Link("← Zpět na téma Fotonika", href=PHOTONICS_TOPIC_HREF, className="back-link")
