"""Page on Piquasso: what it is, how to write a photonic program, its simulators, our check and qubits versus photons."""

from __future__ import annotations

from typing import Callable, Dict, List, Tuple

import numpy as np
from dash import dcc, html

from gbs.benchmark_problems import find_benchmark
from gbs.gaussian_moments import moment_table
from gbs.monomial_problem import pattern_probability
from gbs.photon_tuning import TuningMode, tune_encoding
from ui import ids
from ui.advantage_results import format_number
from ui.navigation import HIDDEN, PHOTONICS_LANDSCAPE_PATH, piquasso_href
from ui.piquasso_content import (
    INTRO,
    KEY_FINDINGS,
    PIQUASSO_PROBABILITIES,
    PIQUASSO_SAMPLING,
    QISKIT_NATIVE_GATE_COUNTS,
    QUBITS_TOPIC,
    RELATED_LINKS,
    SAMPLED_PROBLEM,
    SIMULATOR_ROWS,
    SIMULATORS_TOPIC,
    SOURCES_ANCHOR,
    TITLE,
    TOPICS,
    VERIFICATION_TOPIC,
)
from ui.random_matrix_content import czech_decimal
from ui.theory_content import TheoryTopic
from ui.topic_sections import key_findings_card, related_pages, sources_section, table_of_contents, topic_section


def build_piquasso_page() -> html.Div:
    return html.Div(
        id=ids.PIQUASSO_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            _back_link(),
            html.H1(TITLE),
            html.P(INTRO, className="lead"),
            key_findings_card(KEY_FINDINGS, piquasso_href),
            table_of_contents(TOPICS, piquasso_href, SOURCES_ANCHOR),
            *[topic_section(number, topic, _illustrations(topic)) for number, topic in enumerate(TOPICS, start=1)],
            sources_section(TOPICS, SOURCES_ANCHOR),
            _back_link(),
        ],
    )


def target_pattern(key: str) -> Tuple[int, ...]:
    return tuple(int(power) for power in find_benchmark(key).problem.exponents)


def exact_moment(key: str) -> float:
    """E[x^n] of a problem of the advantage page from Stein's recursion."""
    problem = find_benchmark(key).problem
    return float(moment_table(np.asarray(problem.covariance), list(target_pattern(key)))[target_pattern(key)])


def app_probability(key: str) -> float:
    """p(n) of the target pattern from the app's hafnian formula, with the tuning of the export (per mode)."""
    problem = find_benchmark(key).problem
    encoding = tune_encoding(problem.covariance, problem.exponents, TuningMode.PER_MODE)
    return pattern_probability(encoding, target_pattern(key), exact_moment(key))


def probabilities_markdown() -> str:
    rows = [
        "| Úloha | Vzor $n$ | $p(n)$ v aplikaci | $p(n)$ z Piquassa | Relativní rozdíl |",
        "|---|---|---|---|---|",
    ]
    for stored in PIQUASSO_PROBABILITIES:
        ours = app_probability(stored.problem_key)
        rows.append(
            f"| {short_title(stored.problem_key)} | {_pattern(target_pattern(stored.problem_key))} "
            f"| {format_number(ours)} "
            f"| {format_number(stored.probability)} | {format_number(abs(stored.probability / ours - 1))} |"
        )
    return "\n".join(rows)


def sampling_markdown() -> str:
    rows = [
        "| Měřicí ořez | Výstřelů se vzorem | Nejvíc fotonů v módu | Průměr fotonů na výstřel | Odhad momentu |",
        "|---|---|---|---|---|",
    ]
    for run in PIQUASSO_SAMPLING:
        rows.append(
            f"| {run.measurement_cutoff} | {run.hits} z {_integer(run.shots)} | {run.max_photons_per_mode} "
            f"| {czech_decimal(run.mean_photons)} ± {czech_decimal(run.mean_photons_error)} "
            f"| {_integer(round(run.estimate))} |"
        )
    return "\n".join(rows)


def gate_counts_markdown() -> str:
    rows = [
        "| Úloha | Qubitů | Bran CZ | Řádků OpenQASM 3 | Příprava stavu přes StatePreparation |",
        "|---|---|---|---|---|",
    ]
    for count in QISKIT_NATIVE_GATE_COUNTS:
        rows.append(
            f"| {short_title(count.problem_key)} | {count.qubits} | {_integer(count.cz)} "
            f"| {_integer(count.qasm_lines)} | {_integer(count.state_preparation_cz)} CZ |"
        )
    return "\n".join(rows)


def short_title(key: str) -> str:
    """„1 · Extrémní moment jedné veličiny“ without the formula, which is long and has brackets Markdown would eat."""
    return find_benchmark(key).title.split(":")[0]


def _integer(value: int) -> str:
    return f"{value:,}".replace(",", " ")


def _decimal(value: float, digits: int) -> str:
    return f"{value:,.{digits}f}".replace(",", " ").replace(".", ",")


def _pattern(pattern: Tuple[int, ...]) -> str:
    return "(" + ", ".join(str(photons) for photons in pattern) + ")"


def _verification() -> html.Div:
    return html.Div([
        html.H4("Pravděpodobnost cílového vzoru: aplikace a Piquasso"),
        dcc.Markdown(probabilities_markdown(), mathjax=True),
        html.H4(
            f"Vzorkování úlohy „{short_title(SAMPLED_PROBLEM)}“, vzor {_pattern(target_pattern(SAMPLED_PROBLEM))}"
        ),
        dcc.Markdown(sampling_markdown()),
        html.P(
            f"Přesný moment je {_decimal(exact_moment(SAMPLED_PROBLEM), 1)}, pravděpodobnost vzoru "
            f"{format_number(app_probability(SAMPLED_PROBLEM))}. Hodnoty z Piquassa jsou uložené; vytváří je skript "
            "scripts/piquasso_gbs_check.py (Piquasso není závislost aplikace).",
            className="hint small",
        ),
    ])


def simulators_markdown() -> str:
    rows = ["| Simulátor | Co drží v paměti | Umí navíc | Na co se hodí |", "|---|---|---|---|"]
    rows += [f"| `{row.name}` | {row.memory} | {row.extras} | {row.use} |" for row in SIMULATOR_ROWS]
    return "\n".join(rows)


def _simulators_table() -> html.Div:
    return html.Div(className="text-table", children=dcc.Markdown(simulators_markdown()))


def _gate_counts() -> html.Div:
    return html.Div([
        html.H4("Náš export do Qiskitu po překladu do nativních bran IQM (PRX a CZ)"),
        dcc.Markdown(gate_counts_markdown()),
        html.P(
            "Předpokládá se propojení každého qubitu s každým, počty jsou tedy dolní mez; na hvězdicové topologii "
            "VLQ stojí každá brána CZ mezi dvěma qubity ještě dvě operace MOVE. Čísla vytváří skript "
            "scripts/qiskit_native_gate_counts.py (Qiskit není závislost aplikace).",
            className="hint small",
        ),
    ])


def _illustrations(topic: TheoryTopic) -> List:
    build_illustration = ILLUSTRATIONS.get(topic.anchor)
    illustrations = [build_illustration()] if build_illustration else []
    if topic.anchor == QUBITS_TOPIC.anchor:
        illustrations += related_pages(RELATED_LINKS)
    return illustrations


def _back_link() -> dcc.Link:
    return dcc.Link("← Zpět na Fotonika ve světě", href=PHOTONICS_LANDSCAPE_PATH, className="back-link")


ILLUSTRATIONS: Dict[str, Callable[[], html.Div]] = {
    SIMULATORS_TOPIC.anchor: _simulators_table,
    VERIFICATION_TOPIC.anchor: _verification,
    QUBITS_TOPIC.anchor: _gate_counts,
}
