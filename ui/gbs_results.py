from __future__ import annotations

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
from gbs.expectation import hafnian_terms
from ui.components import TABLE_CELL_STYLE, TABLE_HEADER_STYLE, metric_tile

PERCENT = 100
HAFNIAN_TABLE_ROWS = 8
COMPARABLE_ERROR_RATIO = 1.2
DEGREE_SUPERSCRIPTS = {2: "²", 4: "⁴", 6: "⁶"}


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


def _problem_step(run: GbsDemoRun, mode_labels: Sequence[str]) -> html.Section:
    problem = run.problem
    portfolio_volatility = float(np.sqrt(problem.weights @ problem.covariance @ problem.weights))
    return _step(1, "Úloha: moment výnosu portfolia", [
        html.Div(className="two-columns", children=[
            html.Div([
                _markdown(
                    rf"Výnos portfolia je $L = w^\top X$, kde $X \sim \mathcal{{N}}(0, \Sigma)$ jsou roční výnosy "
                    rf"aktiv očištěné o střední hodnotu. Hledáme $\mathbb{{E}}[L^{problem.degree}]$."
                ),
                html.Div(className="metric-grid", children=[
                    metric_tile(f"Přesná hodnota E[L{DEGREE_SUPERSCRIPTS[problem.degree]}]", _scientific(run.study.exact)),
                    metric_tile("Volatilita portfolia √(wᵀΣw)", f"{portfolio_volatility * PERCENT:.2f} %"),
                ]),
            ]),
            html.Div([
                html.H4("Kovarianční matice Σ"),
                dcc.Graph(figure=covariance_heatmap(problem.covariance, mode_labels)),
            ]),
        ]),
    ])


def _hafnian_step(run: GbsDemoRun) -> html.Section:
    terms = sorted(hafnian_terms(run.problem), key=lambda term: term.contribution, reverse=True)
    total = sum(term.contribution for term in terms)
    rows = [
        {
            "pattern": pattern_label(term.pattern),
            "coefficient": f"{term.coefficient:.4g}",
            "hafnian": _scientific(term.hafnian),
            "contribution": _scientific(term.contribution),
            "share": f"{term.contribution / total * PERCENT:.1f} %",
        }
        for term in terms[:HAFNIAN_TABLE_ROWS]
    ]
    return _step(2, "Wickova věta: moment = vážený součet hafniánů", [
        _markdown(
            rf"Roznásobením $(w^\top X)^{run.problem.degree}$ vznikne {len(terms)} monomů $x^n$ "
            rf"se součtem mocnin $|n| = {run.problem.degree}$. Každý má očekávanou hodnotu "
            r"$\mathbb{E}[x^n] = \mathrm{Haf}(\Sigma_n)$, kde $\Sigma_n$ opakuje řádek a sloupec $i$ "
            r"$n_i$-krát. Hafnián je součet přes všechna perfektní párování – obecně #P-těžký výpočet."
        ),
        dash_table.DataTable(
            data=rows,
            columns=[
                {"id": "pattern", "name": "Vzor n"},
                {"id": "coefficient", "name": "Koeficient c_n"},
                {"id": "hafnian", "name": "Haf(Σ_n)"},
                {"id": "contribution", "name": "Příspěvek c_n·Haf"},
                {"id": "share", "name": "Podíl"},
            ],
            style_cell=TABLE_CELL_STYLE,
            style_header=TABLE_HEADER_STYLE,
        ),
        html.P(f"Zobrazeno {len(rows)} největších z {len(terms)} členů.", className="hint small"),
    ])


def _encoding_step(run: GbsDemoRun, mode_labels: Sequence[str]) -> html.Section:
    program = run.program
    return _step(3, "Nahrání do GBS: stlačení a interferometr", [
        _markdown(
            rf"Matice se přeškáluje ($\gamma = {program.scale:.2f}$) a rozloží jako "
            r"$B = \gamma\Sigma = U\,\mathrm{diag}(\tanh r)\,U^\top$. Každý vstupní mód nese jednu "
            r"**hlavní komponentu** portfolia (eigen-portfolio): čím větší její rozptyl, tím silnější stlačení "
            r"$r_j$. Interferometr $U$ je pak smíchá tak, že **každý výstupní mód (detektor) odpovídá "
            r"jednomu aktivu**."
        ),
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
    ])


def _measurement_step(run: GbsDemoRun, mode_labels: Sequence[str]) -> html.Section:
    degree = run.problem.degree
    return _step(4, "Měření: výstřely a počty fotonů", [
        _markdown(
            "Jeden výstřel = jedno změření počtu fotonů v každém módu. Pro odhad jsou užitečné jen výstřely "
            rf"s přesně {degree} fotony (✓), tj. **{run.study.useful_shot_fraction * PERCENT:.1f} %** výstřelů. "
            "Liché počty fotonů stlačené vakuum nikdy nevytvoří."
        ),
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
    ])


def _frequency_step(run: GbsDemoRun) -> html.Section:
    return _step(5, "Z četností zpět k hafniánům", [
        _markdown(
            r"Z relativní četnosti $\hat p(n)$ každého vzoru se dopočítá hafnián a z hafniánů celý moment: "
            r"$\mathrm{Haf}(\Sigma_n) \approx \gamma^{-d/2}\sqrt{\hat p(n)\; n!\,\prod_j \cosh r_j}$. "
            "Čím víc výstřelů, tím blíž jsou četnosti přesným pravděpodobnostem."
        ),
        dcc.Graph(figure=pattern_frequency_chart(run.study)),
    ])


def _comparison_step(run: GbsDemoRun) -> html.Section:
    study = run.study
    sample_size = f"{study.sample_sizes[-1]:,}".replace(",", " ")
    gbs_error, mc_error = study.gbs_relative_rmse[-1], study.mc_relative_rmse[-1]
    return _step(6, "Srovnání s klasickým Monte Carlem", [
        _markdown(
            f"Obě metody dostanou stejný počet vzorků. Chyba je průměrná (RMSE) přes {REPETITIONS} "
            f"nezávislých opakování. {_verdict(gbs_error, mc_error, sample_size)}"
        ),
        html.Div(className="metric-grid", children=[
            metric_tile(f"GBS odhad (N = {sample_size})", _scientific(study.gbs_trajectory[-1])),
            metric_tile(f"MC odhad (N = {sample_size})", _scientific(study.mc_trajectory[-1])),
            metric_tile("Relativní chyba GBS", f"{gbs_error * PERCENT:.2f} %"),
            metric_tile("Relativní chyba MC", f"{mc_error * PERCENT:.2f} %"),
        ]),
        html.Div(className="two-columns", children=[
            dcc.Graph(figure=convergence_chart(study)),
            dcc.Graph(figure=trajectory_chart(study)),
        ]),
    ])


def _verdict(gbs_error: float, mc_error: float, sample_size: str) -> str:
    if max(gbs_error, mc_error) / min(gbs_error, mc_error) < COMPARABLE_ERROR_RATIO:
        return f"Při N = {sample_size} mají **obě metody srovnatelnou chybu**."
    if gbs_error < mc_error:
        return f"Při N = {sample_size} má **GBS estimátor {mc_error / gbs_error:.1f}× menší chybu** než klasické MC."
    return f"Při N = {sample_size} má **klasické MC {gbs_error / mc_error:.1f}× menší chybu** než GBS estimátor."


def _step(number: int, title: str, children: List) -> html.Section:
    return html.Section(
        className="card step",
        children=[html.H2([html.Span(str(number), className="step-number"), title])] + children,
    )


def _markdown(text: str) -> dcc.Markdown:
    return dcc.Markdown(text, mathjax=True)


def _scientific(value: float) -> str:
    return f"{value:.4e}"
