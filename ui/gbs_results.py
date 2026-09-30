from __future__ import annotations

from collections import Counter
from math import floor, log10, prod
from typing import List, Sequence

import numpy as np
from dash import dash_table, dcc, html

from gbs.charts import (
    circuit_diagram,
    convergence_chart,
    covariance_heatmap,
    interferometer_heatmap,
    pattern_frequency_chart,
    pattern_label,
    photon_total_chart,
    shot_stream_heatmap,
    trajectory_chart,
)
from gbs.demo import REPETITIONS, SHOT_PREVIEW_MAX_TOTAL, GbsDemoRun
from gbs.expectation import HafnianTerm, hafnian_terms
from gbs.hafnian import hafnian_expansion
from ui.components import SCROLLABLE_TABLE_STYLE, TABLE_CELL_STYLE, TABLE_HEADER_STYLE, details_link, metric_tile
from ui.navigation import theory_href
from ui.theory_content import (
    COMPARISON,
    ENCODING,
    ESTIMATOR,
    PORTFOLIO_MOMENT,
    SHOTS,
    WICK_THEOREM,
    TheoryTopic,
)

PERCENT = 100
HAFNIAN_TABLE_ROWS = 8
COMPARABLE_ERROR_RATIO = 1.2
TARGET_RELATIVE_ERROR = 0.01
SAMPLE_COUNT_SIGNIFICANT_DIGITS = 3
SUBSCRIPT_DIGITS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUPERSCRIPT_DIGITS = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
FORMULA_COLUMNS = ("monomial", "wick")



def build_gbs_results(run: GbsDemoRun, mode_labels: Sequence[str]) -> html.Div:
    return html.Div(
        className="results",
        children=[
            _problem_step(run, mode_labels),
            _hafnian_step(run),
            _encoding_step(run, mode_labels),
            _measurement_step(run, mode_labels),
            _frequency_step(run),
            _comparison_step(run),
        ],
    )


def hafnian_table(terms: Sequence[HafnianTerm], moment: float) -> dash_table.DataTable:
    rows = [
        {
            "pattern": pattern_label(term.pattern),
            "monomial": monomial_label(term.pattern),
            "wick": wick_formula(term.pattern),
            "coefficient": f"{term.coefficient:.4g}",
            "hafnian": _scientific(term.hafnian),
            "contribution": _scientific(term.contribution),
            "share": f"{term.contribution / moment * PERCENT:.1f} %",
        }
        for term in terms
    ]
    return dash_table.DataTable(
        data=rows,
        columns=[
            {"id": "pattern", "name": "Vzor n"},
            {"id": "monomial", "name": "Monom xⁿ"},
            {"id": "wick", "name": "E[xⁿ] podle Wicka"},
            {"id": "coefficient", "name": "Koeficient c_n"},
            {"id": "hafnian", "name": "Haf(Σ_n)"},
            {"id": "contribution", "name": "Příspěvek c_n·Haf"},
            {"id": "share", "name": "Podíl"},
        ],
        style_cell=TABLE_CELL_STYLE,
        style_cell_conditional=[{"if": {"column_id": column}, "textAlign": "left"} for column in FORMULA_COLUMNS],
        style_data={"whiteSpace": "normal", "height": "auto"},
        style_header=TABLE_HEADER_STYLE,
        style_table=SCROLLABLE_TABLE_STYLE,
    )


def monomial_label(pattern: Sequence[int]) -> str:
    """Pattern (2, 1, 0) is the monomial X₁²X₂."""
    return "".join(f"X{_subscript(asset + 1)}{_power(count)}" for asset, count in enumerate(pattern) if count)


def wick_formula(pattern: Sequence[int]) -> str:
    """E[xⁿ] as a sum over pairings, e.g. Σ₁₁Σ₂₂ + 2Σ₁₂² for pattern (2, 2)."""
    terms = []
    for product, multiplicity in hafnian_expansion(pattern).items():
        entries = "".join(
            f"Σ{_subscript(row + 1)}{_subscript(column + 1)}{_power(power)}"
            for (row, column), power in Counter(product).items()
        )
        terms.append(f"{multiplicity if multiplicity > 1 else ''}{entries}")
    return " + ".join(terms)


def _problem_step(run: GbsDemoRun, mode_labels: Sequence[str]) -> html.Section:
    problem = run.problem
    degree = problem.degree
    volatility = float(np.sqrt(problem.portfolio_variance))
    pairing_count = prod(range(degree - 1, 0, -2))
    moment_factor = str(pairing_count) if pairing_count > 1 else ""
    return _step(1, "Úloha: moment výnosu portfolia", [
        html.Div(className="two-columns", children=[
            html.Div([
                _markdown(rf"""
Výnos portfolia je $L = w^\top X$, kde $X \sim \mathcal{{N}}(0, \Sigma)$ jsou roční výnosy aktiv očištěné
o střední hodnotu. Hledáme $\mathbb{{E}}[L^{degree}]$. Protože $L$ je sama normální, přesně platí
$\mathbb{{E}}[L^{degree}] = {moment_factor}\sigma_p^{degree}$ – další kroky se k tomuto číslu musí dopracovat přes
hafniány a fotony.
"""),
                html.Div(className="metric-grid", children=[
                    metric_tile(f"Přesná hodnota E[L{_power(degree)}]", _scientific(run.study.exact)),
                    metric_tile("Volatilita portfolia σ_p = √(wᵀΣw)", f"{volatility * PERCENT:.2f} %"),
                    metric_tile(
                        f"(E[L{_power(degree)}])^(1/{degree})", f"{run.study.exact ** (1 / degree) * PERCENT:.2f} %",
                        hint="Odmocnina momentu převede „výnos na d-tou“ zpět na procenta výnosu. "
                        "Pro d = 2 je to volatilita, vyšší momenty dají víc, protože zdůrazňují velké výkyvy.",
                    ),
                ]),
            ]),
            html.Div([
                html.H4("Kovarianční matice Σ"),
                dcc.Graph(figure=covariance_heatmap(problem.covariance, mode_labels)),
            ]),
        ]),
        _details_link(PORTFOLIO_MOMENT),
    ])


def _hafnian_step(run: GbsDemoRun) -> html.Section:
    degree = run.problem.degree
    terms = sorted(hafnian_terms(run.problem), key=lambda term: term.contribution, reverse=True)
    moment = sum(term.contribution for term in terms)
    shown_terms = terms[:HAFNIAN_TABLE_ROWS]
    return _step(2, "Wickova věta: moment = vážený součet hafniánů", [
        _markdown(rf"""
Roznásobením $(w^\top X)^{degree}$ vznikne {_count_noun(len(terms), "monom", "monomy", "monomů")} $c_n\,x^n$
se součtem mocnin $|n| = {degree}$. Každý má podle Wickovy věty střední hodnotu
$\mathbb{{E}}[x^n] = \mathrm{{Haf}}(\Sigma_n)$, kde $\Sigma_n$ opakuje řádek a sloupec $i$ celkem $n_i$-krát.
Sloupec „E[xⁿ] podle Wicka“ ukazuje rozdělení činitelů do dvojic.
"""),
        hafnian_table(shown_terms, moment),
        html.P(f"Zobrazeno {len(shown_terms)} největších z {len(terms)} členů.", className="hint small"),
        _details_link(WICK_THEOREM),
    ])


def _encoding_step(run: GbsDemoRun, mode_labels: Sequence[str]) -> html.Section:
    program = run.program
    squeezing_values = ", ".join(f"{squeezing:.2f}" for squeezing in program.squeezing)
    return _step(3, "Nahrání do GBS: stlačení a interferometr", [
        _markdown(rf"""
Matice se přeškáluje ($\gamma = {program.scale:.2f}$) a rozloží jako
$B = \gamma\Sigma = U\,\mathrm{{diag}}(\tanh r)\,U^\top$. Každý vstupní mód nese jednu **hlavní komponentu**
portfolia (eigen-portfolio): čím větší její rozptyl, tím silnější stlačení – tady $r = ({squeezing_values})$.
Interferometr $U$ je pak smíchá tak, že **každý výstupní mód (detektor) odpovídá jednomu aktivu**.
"""),
        dcc.Graph(figure=circuit_diagram(program, mode_labels), config={"displayModeBar": False}),
        html.Div(className="two-columns", children=[
            html.Div([
                html.H4("Interferometr |U| (řádky = aktiva, sloupce = vstupní módy)"),
                dcc.Graph(figure=interferometer_heatmap(program, mode_labels)),
            ]),
            html.Div(className="metric-grid", children=[
                metric_tile("Škálování γ", f"{program.scale:.2f}"),
                metric_tile("Největší stlačení r_max", f"{program.squeezing.max():.2f}"),
                metric_tile(
                    "Střední počet fotonů n̄", f"{program.mean_photon_number:.2f}",
                    hint="Součet sinh²(r_j) přes všechny módy.",
                ),
            ]),
        ]),
        _details_link(ENCODING),
    ])


def _measurement_step(run: GbsDemoRun, mode_labels: Sequence[str]) -> html.Section:
    degree = run.problem.degree
    return _step(4, "Měření: výstřely a počty fotonů", [
        _markdown(rf"""
Jeden výstřel = jedno změření počtu fotonů v každém módu. Fotony vznikají v párech a interferometr je jen
přerozděluje, takže celkový počet je vždy sudý. Pro odhad jsou užitečné jen výstřely s přesně
{_photon_count(degree)} (✓), tj. **{run.study.useful_shot_fraction * PERCENT:.1f} %** výstřelů.
"""),
        html.Div(className="two-columns", children=[
            html.Div([
                html.H4(f"Prvních {len(run.shots)} výstřelů"),
                dcc.Graph(figure=shot_stream_heatmap(run.shots, degree, mode_labels, SHOT_PREVIEW_MAX_TOTAL)),
            ]),
            html.Div([
                html.H4("Rozdělení celkového počtu fotonů"),
                dcc.Graph(figure=photon_total_chart(run.total_photon_probabilities, degree)),
            ]),
        ]),
        _details_link(SHOTS),
    ])


def _frequency_step(run: GbsDemoRun) -> html.Section:
    return _step(5, "Z četností zpět k hafniánům", [
        _markdown(r"""
Z relativní četnosti $\hat p(n)$ každého vzoru se dopočítá hafnián a z hafniánů celý moment:
$\mathrm{Haf}(\Sigma_n) \approx \gamma^{-d/2}\sqrt{\hat p(n)\; n!\,\prod_j \cosh r_j}$. Čím víc výstřelů, tím
blíž jsou četnosti přesným pravděpodobnostem.
"""),
        dcc.Graph(figure=pattern_frequency_chart(run.study)),
        _details_link(ESTIMATOR),
    ])


def _comparison_step(run: GbsDemoRun) -> html.Section:
    study = run.study
    sample_count = study.sample_sizes[-1]
    sample_size = _format_count(sample_count)
    gbs_error, mc_error = study.gbs_relative_rmse[-1], study.mc_relative_rmse[-1]
    gbs_constant, mc_constant = study.gbs_error_constant, study.mc_error_constant
    return _step(6, "Srovnání s klasickým Monte Carlem", [
        _markdown(rf"""
Obě metody dostanou stejný počet vzorků $N$; chyba je relativní RMSE přes {REPETITIONS} nezávislých opakování.
Obě chyby klesají jako $c/\sqrt{{N}}$ a rozhoduje konstanta: $c_{{\mathrm{{MC}}}} = {mc_constant:.2f}$,
$c_{{\mathrm{{GBS}}}} = {gbs_constant:.2f}$. Pro chybu {TARGET_RELATIVE_ERROR * PERCENT:.0f} % tak MC potřebuje
asi **{_format_count(_samples_for(mc_constant))}** scénářů a GBS asi
**{_format_count(_samples_for(gbs_constant))}** výstřelů. {_theory_verdict(gbs_constant, mc_constant)}
{_measured_verdict(gbs_error, mc_error, sample_size)}
"""),
        html.P(
            f"Chyba odhadnutá z {REPETITIONS} opakování je sama náhodná (zhruba ±{_rmse_noise_percent():.0f} %); "
            "čárkované čáry v grafu ukazují teorii c/√N.",
            className="hint small",
        ),
        html.H4(f"Naměřeno ({REPETITIONS} opakování, N = {sample_size})"),
        html.Div(className="metric-grid", children=[
            metric_tile("GBS odhad", _scientific(study.gbs_trajectory[-1])),
            metric_tile("MC odhad", _scientific(study.mc_trajectory[-1])),
            metric_tile("Relativní chyba GBS", f"{gbs_error * PERCENT:.2f} %"),
            metric_tile("Relativní chyba MC", f"{mc_error * PERCENT:.2f} %"),
        ]),
        html.H4(f"Teorie pro velké N (chyba ≈ c/√N, N = {sample_size})"),
        html.Div(className="metric-grid", children=[
            metric_tile("Teoretická chyba GBS", f"{gbs_constant / np.sqrt(sample_count) * PERCENT:.2f} %"),
            metric_tile("Teoretická chyba MC", f"{mc_constant / np.sqrt(sample_count) * PERCENT:.2f} %"),
            metric_tile(
                f"Výstřelů GBS pro chybu {TARGET_RELATIVE_ERROR * PERCENT:.0f} %",
                _format_count(_samples_for(gbs_constant)),
            ),
            metric_tile(
                f"Scénářů MC pro chybu {TARGET_RELATIVE_ERROR * PERCENT:.0f} %",
                _format_count(_samples_for(mc_constant)),
            ),
        ]),
        html.Div(className="two-columns", children=[
            dcc.Graph(figure=convergence_chart(study)),
            dcc.Graph(figure=trajectory_chart(study)),
        ]),
        _details_link(COMPARISON),
    ])


def _measured_verdict(gbs_error: float, mc_error: float, sample_size: str) -> str:
    if _is_comparable(gbs_error, mc_error):
        return f"Při N = {sample_size} mají **obě metody srovnatelnou chybu**."
    if gbs_error < mc_error:
        return f"Při N = {sample_size} má **GBS estimátor {mc_error / gbs_error:.1f}× menší chybu** než klasické MC."
    return f"Při N = {sample_size} má **klasické MC {gbs_error / mc_error:.1f}× menší chybu** než GBS estimátor."


def _theory_verdict(gbs_constant: float, mc_constant: float) -> str:
    """Error ∝ c/√N, so the ratio of required samples is the squared ratio of the constants."""
    if _is_comparable(gbs_constant, mc_constant):
        return "Teoreticky jsou tedy obě metody zhruba stejně dobré."
    sample_ratio = (gbs_constant / mc_constant) ** 2
    if sample_ratio < 1:
        return f"GBS tedy potřebuje zhruba **{1 / sample_ratio:.1f}× méně** vzorků."
    return f"GBS tedy potřebuje zhruba **{sample_ratio:.1f}× víc** vzorků."


def _is_comparable(first: float, second: float) -> bool:
    return max(first, second) / min(first, second) < COMPARABLE_ERROR_RATIO


def _samples_for(error_constant: float) -> int:
    """Error ≈ c/√N reaches the target at N = (c / target)², rounded because the constant is approximate."""
    samples = (error_constant / TARGET_RELATIVE_ERROR) ** 2
    rounding_digits = SAMPLE_COUNT_SIGNIFICANT_DIGITS - 1 - floor(log10(samples))
    return int(round(samples, rounding_digits))


def _rmse_noise_percent() -> float:
    """Relative standard error of an RMSE estimated from R repetitions is roughly 1/√(2R)."""
    return PERCENT / np.sqrt(2 * REPETITIONS)


def _details_link(topic: TheoryTopic) -> dcc.Link:
    return details_link(topic.title, theory_href(topic.anchor))


def _step(number: int, title: str, children: List) -> html.Section:
    return html.Section(
        className="card step",
        children=[html.H2([html.Span(str(number), className="step-number"), title])] + children,
    )


def _markdown(text: str) -> dcc.Markdown:
    return dcc.Markdown(text, mathjax=True)


def _subscript(number: int) -> str:
    return str(number).translate(SUBSCRIPT_DIGITS)


def _power(exponent: int) -> str:
    return str(exponent).translate(SUPERSCRIPT_DIGITS) if exponent > 1 else ""


def _photon_count(count: int) -> str:
    return _count_noun(count, "foton", "fotony", "fotonů")


def _count_noun(count: int, one: str, two_to_four: str, other: str) -> str:
    """Czech plural in the nominative/accusative: 1 foton, 2–4 fotony, 0 and 5+ fotonů."""
    if count == 1:
        return f"{count} {one}"
    if 2 <= count <= 4:
        return f"{count} {two_to_four}"
    return f"{count} {other}"


def _format_count(count: int) -> str:
    return f"{count:,}".replace(",", " ")


def _scientific(value: float) -> str:
    return f"{value:.4e}"
