"""Page on Quandela, its software Perceval and the European photonic hardware that could run GBS or boson sampling."""

from __future__ import annotations

from typing import Callable, Dict, List

from dash import dcc, html

from gbs.boson_sampling import REFERENCE_MODES, REFERENCE_PHOTONS, estimate, reference_problem
from gbs.monomial_problem import required_samples
from ui import ids
from ui.advantage_results import format_count, format_number
from ui.navigation import HIDDEN, LITERATURE_REVIEW_PATH, photonic_hardware_href
from ui.photonic_hardware_content import (
    EUROPE_TOPIC,
    INTRO,
    KEY_FINDINGS,
    NOISE_SCENARIOS,
    PERCEVAL_AGREEMENT,
    PHOTONIC_MACHINES,
    SOURCES_ANCHOR,
    TITLE,
    TOPICS,
    USE_CASE_TOPIC,
)
from ui.theory_content import TheoryTopic
from ui.topic_sections import key_findings_card, sources_section, table_of_contents, topic_section

TARGET_RELATIVE_ERROR = 0.01
PERCENT_DIGITS = 2


def build_photonic_hardware_page() -> html.Div:
    return html.Div(
        id=ids.PHOTONIC_HARDWARE_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            _back_link(),
            html.H1(TITLE),
            html.P(INTRO, className="lead"),
            key_findings_card(KEY_FINDINGS, photonic_hardware_href),
            table_of_contents(TOPICS, photonic_hardware_href, SOURCES_ANCHOR),
            *[topic_section(number, topic, _illustrations(topic)) for number, topic in enumerate(TOPICS, start=1)],
            sources_section(TOPICS, SOURCES_ANCHOR),
            _back_link(),
        ],
    )


def perceval_summary_markdown() -> str:
    """Ideal values of the reference problem, recomputed here with permanents."""
    result = estimate(reference_problem())
    shots = required_samples(result.relative_variance, TARGET_RELATIVE_ERROR)
    return "\n".join([
        f"- Přesná hodnota $\\mu$ = {format_number(result.exact_value)}.",
        f"- Relativní rozptyl jednoho výstřelu {format_number(result.relative_variance)}, tedy asi "
        f"{format_count(shots)} výstřelů pro chybu 1 %.",
        f"- {PERCEVAL_AGREEMENT}",
    ])


def noise_markdown() -> str:
    """Stored Perceval biases next to the shot count from which the bias outweighs the statistical error."""
    relative_variance = estimate(reference_problem()).relative_variance
    rows = [
        "| Šum zdroje | systematická odchylka odhadu | od kolika výstřelů je větší než statistická chyba |",
        "|---|---|---|",
    ]
    for scenario in NOISE_SCENARIOS:
        rows.append(
            f"| {scenario.label} | {_signed_percent(scenario.relative_bias)} "
            f"| {_crossover_shots(relative_variance, scenario.relative_bias)} |"
        )
    return "\n".join(rows)


def machines_markdown() -> str:
    rows = [
        "| Kdo | Stroj | Vstupní světlo | GBS se stlačeným světlem | Přístup |",
        "|---|---|---|---|---|",
    ]
    for machine in PHOTONIC_MACHINES:
        rows.append(
            f"| {machine.operator} | {machine.machine} | {machine.input_light} | {machine.runs_gbs} | {machine.access} |"
        )
    return "\n".join(rows)


def _crossover_shots(relative_variance: float, relative_bias: float) -> str:
    """One standard deviation √(v/N) falls below |bias| from N = v / bias² shots on."""
    if relative_bias == 0:
        return "nikdy – odhad zůstává nevychýlený"
    return format_count(relative_variance / relative_bias**2)


def _signed_percent(value: float) -> str:
    if value == 0:
        return "0 %"
    return f"{100 * value:+.{PERCENT_DIGITS}f}".replace(".", ",").replace("-", "−") + " %"


def _illustrations(topic: TheoryTopic) -> List[html.Div]:
    build_illustration = ILLUSTRATIONS.get(topic.anchor)
    return [build_illustration()] if build_illustration else []


def _perceval_experiment() -> html.Div:
    return html.Div([
        html.H4(
            f"Náš experiment v Percevalu: {REFERENCE_MODES} módů, {REFERENCE_PHOTONS} fotony, "
            "počítají se jen výstřely se všemi fotony"
        ),
        dcc.Markdown(perceval_summary_markdown(), mathjax=True),
        dcc.Markdown(noise_markdown()),
        html.P(
            "Odchylka = (střední hodnota odhadu se šumem − μ) / μ, spočítaná v Percevalu z přesného rozdělení výstupů. "
            "Statistická chyba (jedna směrodatná odchylka) klesá s počtem výstřelů N jako √(v/N); od uvedeného počtu "
            "výstřelů je menší než systematická odchylka a další měření už nepomůže. Perceval není závislost aplikace, "
            "proto jsou hodnoty se šumem uložené; vytváří je skript scripts/perceval_boson_sampling.py.",
            className="hint small",
        ),
    ])


def _machines_table() -> html.Div:
    return html.Div([
        html.H4("Kdo by mohl úlohu spustit"),
        dcc.Markdown(machines_markdown()),
        html.P(
            "Stav k datu ověření zdrojů. „Sporné“ u PT-2: nezávislý benchmark a článek ORCA popisují vstupní stav "
            "různě.",
            className="hint small",
        ),
    ])


def _back_link() -> dcc.Link:
    return dcc.Link("← Zpět na rešerši GBS", href=LITERATURE_REVIEW_PATH, className="back-link")


ILLUSTRATIONS: Dict[str, Callable[[], html.Div]] = {
    USE_CASE_TOPIC.anchor: _perceval_experiment,
    EUROPE_TOPIC.anchor: _machines_table,
}
