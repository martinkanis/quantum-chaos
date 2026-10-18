"""Page on what Qpurpose actually sells and how its method behaves on classical hardware, with our own computations."""

from __future__ import annotations

from typing import Callable, Dict, List

from dash import dcc, html

from gbs.hafnian_squared import PAPER_EXAMPLE_MATRIX, compare_estimators, uniform_problem
from gbs.monomial_problem import required_samples
from ui import ids
from ui.advantage_results import format_count, format_number
from ui.navigation import ADVANTAGE_PATH, HIDDEN, qpurpose_href
from ui.qpurpose_content import (
    CLASSICAL_TOPIC,
    INTRO,
    KEY_FINDINGS,
    PAPER_CHECK_TOPIC,
    REPLICATION_COEFFICIENT_VECTORS,
    REPLICATION_MATRICES,
    REPLICATION_SHARES,
    SOURCES_ANCHOR,
    TITLE,
    TOPICS,
)
from ui.theory_content import TheoryTopic
from ui.topic_sections import key_findings_card, sources_section, table_of_contents, topic_section

SWEEP_DEGREES = tuple(range(1, 9))
TARGET_RELATIVE_ERROR = 0.01
PERCENT_DIGITS = 1


def build_qpurpose_page() -> html.Div:
    return html.Div(
        id=ids.QPURPOSE_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            _back_link(),
            html.H1(TITLE),
            html.P(INTRO, className="lead"),
            key_findings_card(KEY_FINDINGS, qpurpose_href),
            table_of_contents(TOPICS, qpurpose_href, SOURCES_ANCHOR),
            *[topic_section(number, topic, _illustrations(topic)) for number, topic in enumerate(TOPICS, start=1)],
            sources_section(TOPICS, SOURCES_ANCHOR),
            _back_link(),
        ],
    )


def degree_sweep_markdown() -> str:
    """GBS-I against plain Monte Carlo for the matrix of Example 6.1 and all a_I = 1."""
    rows = [
        "| K | vzorů = hafniánů pro přesný výpočet | Monte Carlo: vzorků pro 1 % | GBS-I: vzorků pro 1 % "
        "| GBS-I méně vzorků | užitečných výstřelů |",
        "|---|---|---|---|---|---|",
    ]
    for degree in SWEEP_DEGREES:
        comparison = compare_estimators(uniform_problem(PAPER_EXAMPLE_MATRIX, degree))
        mc_samples = required_samples(comparison.mc_relative_variance, TARGET_RELATIVE_ERROR)
        gbs_samples = required_samples(comparison.gbs_i_relative_variance, TARGET_RELATIVE_ERROR)
        rows.append(
            f"| {degree} | {comparison.pattern_count} | {format_count(mc_samples)} | {format_count(gbs_samples)} "
            f"| {format_number(mc_samples / gbs_samples)}× | {_percent(100 * comparison.useful_shot_fraction)} |"
        )
    return "\n".join(rows)


def replication_markdown() -> str:
    """Our recomputation of Fig. 2 in arXiv:2502.19362 with the printed and the derived variance factor."""
    rows = [
        "| N | K | GBS-I lepší, vzorec z článku (t⁻⁴ᴷ) | GBS-I lepší, správný vzorec (t⁻²ᴷ) | medián t "
        "| medián V_MC / V_GBS-I |",
        "|---|---|---|---|---|---|",
    ]
    for share in REPLICATION_SHARES:
        rows.append(
            f"| {share.mode_count} | {share.degree} | {_percent(share.printed_percent)} | {_percent(share.derived_percent)} "
            f"| {format_number(share.median_scale)} | {format_number(share.median_variance_ratio)} |"
        )
    return "\n".join(rows)


def _illustrations(topic: TheoryTopic) -> List[html.Div]:
    build_illustration = ILLUSTRATIONS.get(topic.anchor)
    return [build_illustration()] if build_illustration else []


def _degree_sweep_table() -> html.Div:
    return html.Div([
        html.H4("Matice z příkladu 6.1, všechna a_I = 1: kolik vzorků potřebují odhady a kolik hafniánů přesný výpočet"),
        dcc.Markdown(degree_sweep_markdown()),
        html.P(
            "Vzorků pro 1 % = relativní rozptyl jednoho vzorku / 0,01² (jedna směrodatná odchylka). Užitečné výstřely "
            "mají přesně 2K fotonů; ostatní k odhadu GBS-I nepřispějí.",
            className="hint small",
        ),
    ])


def _replication_table() -> html.Div:
    return html.Div([
        html.H4(
            f"Náš přepočet obrázku 2: {REPLICATION_MATRICES} náhodných matic × {REPLICATION_COEFFICIENT_VECTORS} "
            "vektorů koeficientů na buňku (podíl úloh, kde GBS-I potřebuje méně vzorků než Monte Carlo)"
        ),
        dcc.Markdown(replication_markdown()),
        html.P(
            "Článek uvádí pro K = 2 hodnoty 96,55 % (N = 3) a 93,14 % (N = 4) a pro K ≥ 4 všude 100 %. Rozdíly v řádu "
            "procent jsou dané počtem náhodných vzorků.",
            className="hint small",
        ),
    ])


def _percent(value: float) -> str:
    return f"{value:.{PERCENT_DIGITS}f}".replace(".", ",") + " %"


def _back_link() -> dcc.Link:
    return dcc.Link("← Zpět na Výhodu GBS", href=ADVANTAGE_PATH, className="back-link")


ILLUSTRATIONS: Dict[str, Callable[[], html.Div]] = {
    CLASSICAL_TOPIC.anchor: _degree_sweep_table,
    PAPER_CHECK_TOPIC.anchor: _replication_table,
}
