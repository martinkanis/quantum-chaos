"""Hafnian and permanent explained from scratch, with code, a finance example and a check on historical data."""

from __future__ import annotations

from math import factorial, prod
from typing import Callable, Dict, List, Sequence, Tuple

import numpy as np
from dash import dcc, html

from gbs.gaussian_moments import moment_table
from montecarlo.historical_returns import sample_moment, standardized_annual_returns
from ui import ids
from ui.hafnian_content import (
    DATA_ASSET_LABELS,
    DATA_ASSETS,
    DATA_STRUCTURES_TOPIC,
    DATA_TOPIC,
    HAFNIAN_CODE,
    HARDNESS_TOPIC,
    INTRO,
    KEY_FINDINGS,
    MARKETS_TOPIC,
    PERMANENT_CODE,
    PHOTONS_TOPIC,
    SOURCES_ANCHOR,
    TITLE,
    TOPICS,
)
from ui.navigation import (
    FAILURE_DIAGNOSTICS_PATH,
    GBS_PATH,
    HIDDEN,
    guide_href,
    hafnian_href,
    photonic_hardware_href,
    theory_href,
)
from ui.theory_content import TheoryTopic
from ui.topic_sections import (
    RelatedLink,
    key_findings_card,
    related_pages,
    sources_section,
    table_of_contents,
    topic_section,
)

GROUP_SIZES = (2, 3, 5, 10, 20)
DECIMALS = 2
PAIRED_ASSETS = (0, 2)
"""Stocks and real estate: the pair whose joint swings the data table compares."""

RELATED_PAGES: Dict[str, Tuple[RelatedLink, ...]] = {
    MARKETS_TOPIC.anchor: (
        ("Wickova–Isserlisova věta a hafnián (Teorie)", theory_href("wickova-veta")),
        ("Gaussovská úloha: střední hodnota polynomu (Průvodce)", guide_href("pruvodce-gaussovska-uloha")),
        ("2 · Monte Carlo na GBS: moment výnosu portfolia", GBS_PATH),
    ),
    PHOTONS_TOPIC.anchor: (
        ("Boson sampling, nebo GBS (stránka o Quandele)", photonic_hardware_href("fotonika-bs-a-gbs")),
        ("Gaussian Boson Sampler: co je to za zařízení (Teorie)", theory_href("gbs-zarizeni")),
    ),
    DATA_TOPIC.anchor: (("Kdy odhad rizika přes GBS selže", FAILURE_DIAGNOSTICS_PATH),),
}


def build_hafnian_page() -> html.Div:
    return html.Div(
        id=ids.HAFNIAN_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            _back_link(),
            html.H1(TITLE),
            html.P(INTRO, className="lead"),
            key_findings_card(KEY_FINDINGS, hafnian_href),
            table_of_contents(TOPICS, hafnian_href, SOURCES_ANCHOR),
            *[topic_section(number, topic, _illustrations(topic)) for number, topic in enumerate(TOPICS, start=1)],
            sources_section(TOPICS, SOURCES_ANCHOR),
            _back_link(),
        ],
    )


def double_factorial(value: int) -> int:
    return prod(range(value, 0, -2))


def solution_counts_markdown() -> str:
    rows = [
        "| kupců n | přiřazení n! (permanent n × n) | lidí 2n | rozdělení do dvojic (2n − 1)!! (hafnián 2n × 2n) |",
        "|---|---|---|---|",
    ]
    for size in GROUP_SIZES:
        rows.append(
            f"| {size} | {_integer(factorial(size))} | {2 * size} | {_integer(double_factorial(2 * size - 1))} |"
        )
    return "\n".join(rows)


def data_moments() -> List[Tuple[str, float, float]]:
    """Label, Gaussian prediction (hafnian of the sample correlations) and sample value of selected moments."""
    standardized = standardized_annual_returns(DATA_ASSETS)
    correlations = np.corrcoef(standardized.T)
    labels = [DATA_ASSET_LABELS[asset] for asset in DATA_ASSETS]
    moments = [
        (f"{label}: E[Z⁴]", _single_exponent(index, 4, len(labels))) for index, label in enumerate(labels)
    ]
    first, second = PAIRED_ASSETS
    paired = [2 if index in PAIRED_ASSETS else 0 for index in range(len(labels))]
    moments.append((f"{labels[first]} a {labels[second]}: E[Z₁²Z₂²]", paired))
    moments.append(("všechna čtyři aktiva: E[Z₁Z₂Z₃Z₄]", [1] * len(labels)))
    return [
        (label, _gaussian_moment(correlations, exponents), sample_moment(standardized, exponents))
        for label, exponents in moments
    ]


def data_moments_markdown() -> str:
    rows = ["| moment | normální rozdělení (hafnián) | data 1928–2023 |", "|:---|---|---|"]
    for label, gaussian, sample in data_moments():
        rows.append(f"| {_escape_brackets(label)} | {_decimal(gaussian)} | {_decimal(sample)} |")
    return "\n".join(rows)


def _gaussian_moment(correlations: np.ndarray, exponents: Sequence[int]) -> float:
    return float(moment_table(correlations, exponents)[tuple(exponents)])


def _single_exponent(index: int, exponent: int, size: int) -> List[int]:
    return [exponent if position == index else 0 for position in range(size)]


def _illustrations(topic: TheoryTopic) -> List:
    build_illustration = ILLUSTRATIONS.get(topic.anchor)
    illustrations = [build_illustration()] if build_illustration else []
    return illustrations + related_pages(RELATED_PAGES.get(topic.anchor, ()))


def _code_listings() -> html.Div:
    return html.Div([
        html.H4("Permanent: součet přes permutace"),
        dcc.Markdown(f"```python\n{PERMANENT_CODE}```"),
        html.H4("Hafnián: součet přes rozdělení do dvojic"),
        dcc.Markdown(f"```python\n{HAFNIAN_CODE}```"),
        html.P(
            "permanent([[3, 1], [2, 4]]) vrátí 14, hafnian([[0, 3, 1, 2], [3, 0, 1, 4], [1, 1, 0, 2], [2, 4, 2, 0]]) "
            "vrátí 12 – příklady z kapitol 1 a 2.",
            className="hint small",
        ),
    ])


def _solution_counts_table() -> html.Div:
    return html.Div([
        html.H4("Kolik je přiřazení a rozdělení do dvojic"),
        dcc.Markdown(solution_counts_markdown()),
    ])


def _data_moments_table() -> html.Div:
    return html.Div([
        html.H4("Normované roční výnosy v USA: co předpovídá hafnián a co ukazují data"),
        dcc.Markdown(data_moments_markdown()),
        html.P(
            "Sloupec „normální rozdělení“ je hafnián korelační matice spočítané z týchž dat (pro E[Z⁴] vždy 3). "
            "Data: A. Damodaran, roční výnosy 1928–2023.",
            className="hint small",
        ),
    ])


def _escape_brackets(text: str) -> str:
    """Markdown would otherwise read E[Z⁴] as a link reference and drop the brackets."""
    return text.replace("[", "\\[").replace("]", "\\]")


def _integer(value: int) -> str:
    return f"{value:,}".replace(",", " ")


def _decimal(value: float) -> str:
    return f"{value:.{DECIMALS}f}".replace(".", ",")


def _back_link() -> dcc.Link:
    return dcc.Link("← Zpět na 2 · Monte Carlo na GBS", href=GBS_PATH, className="back-link")


ILLUSTRATIONS: Dict[str, Callable[[], html.Div]] = {
    DATA_STRUCTURES_TOPIC.anchor: _code_listings,
    HARDNESS_TOPIC.anchor: _solution_counts_table,
    DATA_TOPIC.anchor: _data_moments_table,
}
