"""Results of the advantage lab: verdict, device settings, variance by degree, simulation and the Qiskit plan."""

from __future__ import annotations

from math import floor, log10
from typing import List, Optional, Tuple

from dash import dash_table, dcc, html

from gbs.advantage_charts import TUNING_LABELS, degree_sweep_chart, estimate_spread_chart
from gbs.advantage_lab import LabRun
from gbs.charts import convergence_chart
from gbs.demo import REPETITIONS
from gbs.monomial_problem import VarianceComparison, required_samples
from gbs.photon_tuning import TuningMode
from gbs.qiskit_export import QubitEmulation
from ui.advantage_content import HEAVY_TAIL_NOTE, SIMULATION_HINT
from ui.components import SCROLLABLE_TABLE_STYLE, TABLE_CELL_STYLE, TABLE_HEADER_STYLE, metric_tile

TARGET_RELATIVE_ERROR = 0.01
SIGNIFICANT_DIGITS = 2
LARGEST_PLAIN_NUMBER = 1_000_000
MODERATE_EXPONENTS = range(-3, 6)
"""Values between 0,001 and 999 999 are shown without a power of ten."""
SUPERSCRIPT_DIGITS = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
SAME_PROBABILITY_TOLERANCE = 1e-3
"""Relative difference below which both tunings count as identical (one variable, symmetric problems)."""
OTHER_TUNING_PHRASES = {
    TuningMode.TOTAL: "Při ladění jen celkového počtu fotonů (jako v článku)",
    TuningMode.PER_MODE: "Při ladění fotonů v každém módu zvlášť",
}


def build_advantage_results(run: LabRun, emulation: Optional[QubitEmulation], emulation_error: str) -> html.Div:
    return html.Div(
        className="results",
        children=[
            _summary_section(run),
            _device_section(run),
            _sweep_section(run),
            _simulation_section(run),
            _qiskit_plan_section(emulation, emulation_error),
        ],
    )


def named_monomial(names: List[str], exponents: List[int]) -> str:
    """('Akcie', 'Zlato'), (6, 2) → Akcie⁶·Zlato²."""
    return "·".join(f"{name}{_superscript(power) if power > 1 else ''}" for name, power in zip(names, exponents))


def format_number(value: float) -> str:
    """Four significant digits in Czech notation; very large or small values as mantissa · 10^exponent."""
    if value == 0:
        return "0"
    exponent = floor(log10(abs(value)))
    if exponent in MODERATE_EXPONENTS:
        return _czech(f"{value:,.{max(0, 3 - exponent)}f}")
    return _czech(f"{value / 10**exponent:.3f}") + f" · 10{_superscript(exponent)}"


def format_count(value: float) -> str:
    """Rounded to two significant digits, because sample counts from a variance are only estimates."""
    rounded = _round_significant(value)
    if rounded < LARGEST_PLAIN_NUMBER:
        return _czech(f"{rounded:,.0f}")
    exponent = floor(log10(rounded))
    return _czech(f"{rounded / 10**exponent:.{SIGNIFICANT_DIGITS - 1}f}") + f" · 10{_superscript(exponent)}"


def _summary_section(run: LabRun) -> html.Section:
    comparison = run.comparison
    problem = run.problem.used_variables()
    return _section("Výsledek", [
        html.P(
            f"Monom {named_monomial(list(problem.variable_names), list(problem.exponents))} stupně {problem.degree}.",
            className="hint",
        ),
        html.Div(className="metric-grid", children=[
            metric_tile("Přesná hodnota E[xⁿ]", format_number(comparison.exact), "Spočítaná Wickovou větou."),
            metric_tile(
                "Rozptyl 1 scénáře MC / μ²", format_number(comparison.mc_relative_variance),
                "Kolísání hodnoty xⁿ v jednom náhodném scénáři vzhledem k výsledku. Méně je lépe.",
            ),
            metric_tile(
                "Rozptyl 1 výstřelu GBS-P / μ²", format_number(comparison.gbs_relative_variance),
                "(1 − p)/(4p): binomická chyba četnosti cílového vzoru, odmocnina ji půlí.",
            ),
            metric_tile(*_advantage_tile(comparison)),
            metric_tile(
                "Cílový vzor padá", f"1× za {format_count(1 / comparison.pattern_probability)} výstřelů",
                "p(n), pravděpodobnost, že výstřel ukáže přesně počty fotonů n.",
            ),
        ]),
        dcc.Markdown(_verdict(comparison)),
        dcc.Markdown(_other_tuning_sentence(run)),
    ])


def _advantage_tile(comparison: VarianceComparison) -> Tuple[str, str, str]:
    """Label, value and hint of the tile that names the winner."""
    if comparison.advantage >= 1:
        return (
            "GBS potřebuje méně vzorků", f"{format_count(comparison.advantage)}×",
            "Poměr rozptylů: kolikrát méně výstřelů než scénářů stačí na stejnou přesnost.",
        )
    return (
        "Monte Carlo potřebuje méně vzorků", f"{format_count(1 / comparison.advantage)}×",
        "Tady GBS prohrává: kolikrát víc výstřelů než scénářů by potřeboval.",
    )


def _verdict(comparison: VarianceComparison) -> str:
    mc_samples = required_samples(comparison.mc_relative_variance, TARGET_RELATIVE_ERROR)
    gbs_samples = required_samples(comparison.gbs_relative_variance, TARGET_RELATIVE_ERROR)
    needs = (
        f"Pro relativní chybu 1 % potřebuje klasické Monte Carlo asi **{format_count(mc_samples)}** scénářů "
        f"a GBS-P asi **{format_count(gbs_samples)}** výstřelů"
    )
    if comparison.advantage >= 1:
        return f"{needs} – **{format_count(comparison.advantage)}× méně**."
    return (
        f"{needs}. **Tady vyhrává Monte Carlo** ({format_count(1 / comparison.advantage)}× méně vzorků). Typicky "
        "u nízkého stupně nebo u mnoha proměnných s malými exponenty: cílový vzor je pak jen jeden z mnoha "
        "možných a padá zřídka."
    )


def _other_tuning_sentence(run: LabRun) -> str:
    other_mode = next(mode for mode in TuningMode if mode is not run.mode)
    other = run.comparisons[other_mode]
    if _same_probability(other, run.comparison):
        return (
            "Obě varianty ladění (po módech i jen celkového počtu fotonů jako v článku) tu dávají totéž – "
            "u jedné proměnné nebo u souměrné úlohy se shodují."
        )
    if other.advantage >= 1:
        outcome = f"GBS by potřeboval {format_count(other.advantage)}× méně vzorků než Monte Carlo"
    else:
        outcome = f"GBS by potřeboval {format_count(1 / other.advantage)}× **víc** vzorků než Monte Carlo"
    return (
        f"{OTHER_TUNING_PHRASES[other_mode]} by cílový vzor padal 1× za "
        f"{format_count(1 / other.pattern_probability)} výstřelů a {outcome}."
    )


def _same_probability(first: VarianceComparison, second: VarianceComparison) -> bool:
    difference = abs(first.pattern_probability - second.pattern_probability)
    return difference <= SAME_PROBABILITY_TOLERANCE * second.pattern_probability


def _device_section(run: LabRun) -> html.Section:
    encoding = run.comparison.encoding
    problem = run.problem.used_variables()
    rows = [
        {
            "variable": name,
            "exponent": power,
            "scale": f"{scale:.4g}".replace(".", ","),
            "photons": f"{photons:.3f}".replace(".", ","),
        }
        for name, power, scale, photons in zip(
            problem.variable_names, problem.exponents, encoding.mode_scales, encoding.mean_photons_per_output_mode,
        )
    ]
    squeezing = "; ".join(_czech(f"{value:.2f}") for value in encoding.squeezing)
    mean_photons = _czech(f"{float(encoding.mean_photons_per_squeezer.sum()):.1f}")
    return _section("Nastavení zařízení", [
        dcc.Markdown(
            rf"Do zařízení se nahraje $B = D\Sigma D$ ({TUNING_LABELS[run.mode]}). Stlačovače mají parametry "
            f"*r* = ({squeezing}) a dohromady pošlou v průměru {mean_photons} fotonu – tolik, jaký je stupeň monomu.",
            mathjax=True,
        ),
        dash_table.DataTable(
            data=rows,
            columns=[
                {"id": "variable", "name": "Proměnná (výstupní mód)"},
                {"id": "exponent", "name": "Cílový počet fotonů nᵢ"},
                {"id": "scale", "name": "Škálování dᵢ"},
                {"id": "photons", "name": "Průměrný počet fotonů ⟨nᵢ⟩"},
            ],
            style_cell=TABLE_CELL_STYLE,
            style_header=TABLE_HEADER_STYLE,
            style_table=SCROLLABLE_TABLE_STYLE,
        ),
    ])


def _sweep_section(run: LabRun) -> html.Section:
    return _section("Rozptyl podle stupně: exponenciála proti pomalému růstu", [
        dcc.Graph(figure=degree_sweep_chart(run.sweep, run.problem.degree, run.mode)),
        html.P(
            "Stejný poměr exponentů, rostoucí stupeň. Svislá osa je logaritmická: přímka u Monte Carla znamená "
            "exponenciální růst rozptylu, kdežto GBS-P roste jen pomalu. Kde čáry leží daleko od sebe, tam je "
            "výhoda – u nízkých stupňů naopak může vyhrát Monte Carlo.",
            className="hint small",
        ),
    ])


def _simulation_section(run: LabRun) -> html.Section:
    study = run.study
    largest = f"{int(study.sample_sizes[-1]):,}".replace(",", " ")
    return _section(f"Simulace: {REPETITIONS} opakování pro každý počet vzorků", [
        html.P(SIMULATION_HINT, className="hint"),
        dcc.Graph(figure=convergence_chart(study)),
        html.H4(f"Odhady všech {REPETITIONS} opakování po {largest} vzorcích"),
        dcc.Graph(figure=estimate_spread_chart(study)),
        html.P(HEAVY_TAIL_NOTE, className="hint small"),
    ])


def _qiskit_plan_section(emulation: Optional[QubitEmulation], emulation_error: str) -> html.Section:
    if emulation is None:
        return _section("Skript pro Qiskit", [html.P(emulation_error, className="hint")])
    return _section("Skript pro Qiskit", [
        html.P(
            f"Emulace této úlohy: módy {emulation.mode_count}, qubitů na mód {emulation.qubits_per_mode} "
            f"(až {emulation.fock_cutoff - 1} fotonů v módu), qubitů celkem {emulation.qubit_count}. Ořez zachová "
            f"{_percent(emulation.kept_probability)} pravděpodobnosti stlačeného světla a odhad zbytek opraví. "
            "Skript stáhneš tlačítkem níže.",
            className="hint",
        ),
    ])


def _section(title: str, children: List) -> html.Section:
    return html.Section(className="card", children=[html.H2(title), *children])


def _percent(value: float) -> str:
    return _czech(f"{100 * value:.1f}") + " %"


def _czech(number_text: str) -> str:
    """1,234.5 → 1 234,5."""
    return number_text.replace(",", " ").replace(".", ",")


def _round_significant(value: float) -> float:
    if value <= 0:
        return 0.0
    return round(value, SIGNIFICANT_DIGITS - 1 - floor(log10(value)))


def _superscript(number: int) -> str:
    return str(number).translate(SUPERSCRIPT_DIGITS)
