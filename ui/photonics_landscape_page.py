"""Page on photonic quantum computing worldwide: companies, research groups, suppliers and who can do GBS."""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

from dash import dcc, html

from ui import ids
from ui.navigation import (
    HAFNIAN_PATH,
    HIDDEN,
    PHOTONIC_HARDWARE_PATH,
    QPURPOSE_PATH,
    THEORY_PATH,
    photonics_landscape_href,
)
from ui.photonics_landscape_content import (
    CHAIN_TOPIC,
    FINANCE_TOPIC,
    INTRO,
    KEY_FINDINGS,
    PLAYERS,
    RESEARCH_DATE,
    SINGLE_PHOTON_TOPIC,
    SOURCES_ANCHOR,
    TERMS_TOPIC,
    TITLE,
    TOPICS,
    VERDICT_TOPIC,
    GbsVerdict,
    PhotonicsPlayer,
)
from ui.theory_content import TheoryTopic
from ui.topic_sections import RelatedLink, key_findings_card, related_pages, sources_section, table_of_contents, topic_section

VERDICT_ORDER: Tuple[GbsVerdict, ...] = tuple(GbsVerdict)

RELATED_PAGES: Dict[str, Sequence[RelatedLink]] = {
    TERMS_TOPIC.anchor: (
        ("Hafnián a permanent polopatě", HAFNIAN_PATH),
        ("Teorie: jak se portfolio nahraje do stlačení a módů", THEORY_PATH),
    ),
    CHAIN_TOPIC.anchor: (
        ("Hafnián a permanent polopatě", HAFNIAN_PATH),
        ("Boson sampling, nebo GBS (stránka o Quandele)", PHOTONIC_HARDWARE_PATH),
    ),
    SINGLE_PHOTON_TOPIC.anchor: (("Quandela a fotonický hardware v Evropě", PHOTONIC_HARDWARE_PATH),),
    FINANCE_TOPIC.anchor: (("Co Qpurpose skutečně provozuje u Jyske Bank", QPURPOSE_PATH),),
}


def build_photonics_landscape_page() -> html.Div:
    return html.Div(
        id=ids.PHOTONICS_LANDSCAPE_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            html.H1(TITLE),
            html.P(INTRO, className="lead"),
            key_findings_card(KEY_FINDINGS, photonics_landscape_href),
            table_of_contents(TOPICS, photonics_landscape_href, SOURCES_ANCHOR),
            *[topic_section(number, topic, _illustrations(topic)) for number, topic in enumerate(TOPICS, start=1)],
            sources_section(TOPICS, SOURCES_ANCHOR),
        ],
    )


def players_by_verdict() -> List[PhotonicsPlayer]:
    """Players from those who built GBS to those who cannot run it; the order within a verdict is kept."""
    return sorted(PLAYERS, key=lambda player: VERDICT_ORDER.index(player.verdict))


def players_markdown() -> str:
    rows = [
        "| Kdo (odkud, firma nebo výzkum) | Čím se zabývá | GBS | Proč |",
        "|---|---|---|---|",
    ]
    for player in players_by_verdict():
        rows.append(
            f"| **{player.name}** ({player.country}, {player.kind.value}) | {player.what} "
            f"| **{player.verdict.value}** | {player.reason} |"
        )
    return "\n".join(rows)


def _illustrations(topic: TheoryTopic) -> List:
    illustrations: List = []
    if topic.anchor == VERDICT_TOPIC.anchor:
        illustrations.append(_players_table())
    return illustrations + related_pages(RELATED_PAGES.get(topic.anchor, ()))


def _players_table() -> html.Div:
    return html.Div(className="text-table", children=[
        html.H4("Kdo umí Gaussian Boson Sampling"),
        dcc.Markdown(players_markdown()),
        html.P(
            f"Stav k {RESEARCH_DATE}. „Postavil GBS“ znamená předvedený experiment, ne dostupnou službu; zdroje "
            "ke každému řádku jsou v kapitolách výše.",
            className="hint small",
        ),
    ])
