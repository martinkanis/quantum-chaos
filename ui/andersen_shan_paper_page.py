"""Commented reading of the Andersen & Shan paper: chapters follow the paper, with tables computed by the app."""

from __future__ import annotations

from math import comb, factorial
from typing import Callable, Dict, List, Tuple

import numpy as np
from dash import dcc, html

from gbs.gaussian_moments import moment_table
from ui import ids
from ui.advantage_results import format_number
from ui.andersen_shan_paper_content import (
    CONDITION_TOPIC,
    DENSITY_TOPIC,
    EXPECTATION_TOPIC,
    INTEGRAL_TOPIC,
    INTRO,
    KEY_FINDINGS,
    NEXT_STEPS_TOPIC,
    POLYNOMIAL_TOPIC,
    SOURCES_ANCHOR,
    TITLE,
    TOPICS,
)
from ui.navigation import (
    ADVANTAGE_PATH,
    GBS_PATH,
    HAFNIAN_PATH,
    HIDDEN,
    PHOTONIC_HARDWARE_PATH,
    QPURPOSE_PATH,
    andersen_shan_paper_href,
    guide_href,
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

VARIABLE_COUNTS = (2, 5, 10, 20)
DEGREES = (2, 4, 8, 16)
SERIES_TERMS = 10

RELATED_PAGES: Dict[str, Tuple[RelatedLink, ...]] = {
    INTEGRAL_TOPIC.anchor: (("Monte Carlo a rozptyl jednoho vzorku (Průvodce)", guide_href("pruvodce-monte-carlo")),),
    POLYNOMIAL_TOPIC.anchor: (
        ("Gaussovská úloha: střední hodnota polynomu (Průvodce)", guide_href("pruvodce-gaussovska-uloha")),
        ("Monte Carlo na GBS: moment výnosu portfolia", GBS_PATH),
    ),
    DENSITY_TOPIC.anchor: (
        ("Korelace mezi aktivy (Teorie)", theory_href("korelace")),
        ("Nahrání Σ do zařízení (Teorie)", theory_href("nahrani-matice")),
    ),
    EXPECTATION_TOPIC.anchor: (("Quandela a fotonický hardware v Evropě", PHOTONIC_HARDWARE_PATH),),
    CONDITION_TOPIC.anchor: (
        ("Wickova–Isserlisova věta a hafnián (Teorie)", theory_href("wickova-veta")),
        ("Hafnián a permanent polopatě", HAFNIAN_PATH),
    ),
    NEXT_STEPS_TOPIC.anchor: (
        ("Exponenciální výhoda: co přesně dokázali (Teorie)", theory_href("exponencialni-vyhoda")),
        ("Odhad GBS-P (Průvodce)", guide_href("pruvodce-gbs-p")),
        ("Qpurpose: co skutečně prodávají", QPURPOSE_PATH),
    ),
}


def build_andersen_shan_paper_page() -> html.Div:
    return html.Div(
        id=ids.ANDERSEN_SHAN_PAPER_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            _back_link(),
            html.H1(TITLE),
            html.P(INTRO, className="lead"),
            key_findings_card(KEY_FINDINGS, andersen_shan_paper_href),
            table_of_contents(TOPICS, andersen_shan_paper_href, SOURCES_ANCHOR),
            *[topic_section(number, topic, _illustrations(topic)) for number, topic in enumerate(TOPICS, start=1)],
            sources_section(TOPICS, SOURCES_ANCHOR),
            _back_link(),
        ],
    )


def coefficient_count(variables: int, degree: int) -> int:
    """Monomials of degree at most `degree` in `variables` variables: C(N + K, K)."""
    return comb(variables + degree, degree)


def format_integer(value: int) -> str:
    return f"{value:,}".replace(",", " ")


def coefficient_count_markdown() -> str:
    rows = [
        "| proměnných N | " + " | ".join(f"stupeň K ≤ {degree}" for degree in DEGREES) + " |",
        "|---|" + "---|" * len(DEGREES),
    ]
    for variables in VARIABLE_COUNTS:
        counts = " | ".join(format_integer(coefficient_count(variables, degree)) for degree in DEGREES)
        rows.append(f"| {variables} | {counts} |")
    return "\n".join(rows)


def term_by_term_sums() -> List[Tuple[int, float, float, float, float]]:
    """k, the k-th term and partial sum of E[cosh X] and of E[exp(X²)] integrated term by term, X ~ N(0, 1)."""
    even_moments = moment_table(np.array([[1.0]]), [2 * (SERIES_TERMS - 1)])[::2]
    rows = []
    cosh_sum = square_exp_sum = 0.0
    for order, moment in enumerate(even_moments):
        cosh_term = moment / factorial(2 * order)
        square_exp_term = moment / factorial(order)
        cosh_sum += cosh_term
        square_exp_sum += square_exp_term
        rows.append((order, cosh_term, cosh_sum, square_exp_term, square_exp_sum))
    return rows


def term_by_term_markdown() -> str:
    rows = [
        "| k | člen řady cosh: E\\[X²ᵏ\\]/(2k)! | součet | člen řady exp(x²): E\\[X²ᵏ\\]/k! | součet |",
        "|---|---|---|---|---|",
    ]
    for order, cosh_term, cosh_sum, square_exp_term, square_exp_sum in term_by_term_sums():
        rows.append(
            f"| {order} | {format_number(cosh_term)} | {format_number(cosh_sum)} "
            f"| {format_number(square_exp_term)} | {format_number(square_exp_sum)} |"
        )
    return "\n".join(rows)


def _illustrations(topic: TheoryTopic) -> List:
    build_illustration = ILLUSTRATIONS.get(topic.anchor)
    illustrations = [build_illustration()] if build_illustration else []
    return illustrations + related_pages(RELATED_PAGES.get(topic.anchor, ()))


def _coefficient_count_table() -> html.Div:
    return html.Div([
        html.H4("Kolik koeficientů a_I má polynom stupně nejvýš K v N proměnných"),
        dcc.Markdown(coefficient_count_markdown()),
        html.P(
            "Počet monomů je kombinační číslo (N + K nad K). Každý koeficient je jedno číslo, které úlohu určuje.",
            className="hint small",
        ),
    ])


def _term_by_term_table() -> html.Div:
    return html.Div([
        html.H4(f"Integrace člen po členu pro N = 1, B = 1: prvních {SERIES_TERMS} členů dvou řad"),
        dcc.Markdown(term_by_term_markdown()),
        html.P(
            "E[X²ᵏ] = (2k − 1)!! počítá aplikace přesně (Steinova rekurze). Řada pro cosh se rychle ustálí na "
            "e^(1/2); řada pro exp(x²) roste nade všechny meze, protože (A1) neplatí.",
            className="hint small",
        ),
    ])


def _back_link() -> dcc.Link:
    return dcc.Link("← Zpět na Výhodu GBS", href=ADVANTAGE_PATH, className="back-link")


ILLUSTRATIONS: Dict[str, Callable[[], html.Div]] = {
    POLYNOMIAL_TOPIC.anchor: _coefficient_count_table,
    CONDITION_TOPIC.anchor: _term_by_term_table,
}
