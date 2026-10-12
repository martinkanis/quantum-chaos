"""Quantum Academy: curated links for learning quantum computing, next to the topics of the app."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from dash import html

from ui import ids
from ui.advantage_content import QISKIT_DOCUMENTATION
from ui.guide_practice import STRAWBERRY_FIELDS
from ui.navigation import HIDDEN
from ui.theory_content import (
    AARONSON_ARKHIPOV,
    ANDERSEN_SHAN_EXPECTATIONS,
    DRIMAL_MONTE_CARLO,
    DVORAKOVA_MONTE_CARLO,
    GERRY_KNIGHT,
    GLASSERMAN,
    HAMILTON,
    KRUSE,
    SALEH_TEICH,
    WALRUS_HAFNIAN,
    Source,
)
from ui.topic_sections import markdown_list, source_items

LEAD = (
    "Kde se učit kvantové počítání: interaktivní kurz, videa, blog a materiály, ze kterých vychází tato aplikace. "
    "Odkazy se otevírají v nové záložce."
)


@dataclass(frozen=True)
class AcademyLink:
    title: str
    url: str
    description: str


@dataclass(frozen=True)
class AcademySection:
    title: str
    links: Tuple[AcademyLink, ...] = ()
    sources: Tuple[Source, ...] = ()


ACADEMY_SECTIONS: Tuple[AcademySection, ...] = (
    AcademySection(
        "Začni tady: kvantové počítání od základů",
        links=(
            AcademyLink(
                "Quantum Country", "https://quantum.country",
                "Interaktivní esej Andyho Matuschaka a Michaela Nielsena o kvantovém počítání a kvantové mechanice, "
                "s opakováním v rozestupech, aby si člověk látku opravdu zapamatoval.",
            ),
            AcademyLink(
                "Looking Glass Universe", "https://www.youtube.com/@LookingGlassUniverse",
                "YouTube kanál Mithuny Yoganathan: kvantová mechanika a kvantové počítání srozumitelně a do hloubky.",
            ),
        ),
    ),
    AcademySection(
        "Blogy a diskuse",
        links=(
            AcademyLink(
                "Shtetl-Optimized", "https://scottaaronson.blog",
                "Blog Scotta Aaronsona o kvantové složitosti a kvantové výhodě, včetně boson samplingu; střízlivý "
                "pohled na tvrzení o kvantovém zrychlení.",
            ),
        ),
    ),
    AcademySection(
        "Monte Carlo",
        sources=(DRIMAL_MONTE_CARLO, DVORAKOVA_MONTE_CARLO, GLASSERMAN),
    ),
    AcademySection(
        "Gaussian Boson Sampling a fotonika",
        sources=(HAMILTON, KRUSE, AARONSON_ARKHIPOV, ANDERSEN_SHAN_EXPECTATIONS, SALEH_TEICH, GERRY_KNIGHT),
    ),
    AcademySection(
        "Software",
        sources=(QISKIT_DOCUMENTATION, STRAWBERRY_FIELDS, WALRUS_HAFNIAN),
    ),
)


def build_academy_page() -> html.Div:
    return html.Div(
        id=ids.ACADEMY_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            html.H1("Quantum Academy"),
            html.P(LEAD, className="lead"),
            *[_section(section) for section in ACADEMY_SECTIONS],
        ],
    )


def _section(section: AcademySection) -> html.Section:
    items = [f"- [{link.title}]({link.url}) – {link.description}" for link in section.links]
    return html.Section(
        className="card theory-section",
        children=[html.H2(section.title), markdown_list(items + source_items(section.sources))],
    )
