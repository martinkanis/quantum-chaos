"""Results of the random matrix lab: the spectrum against pure noise and the risk the portfolios really carry."""

from __future__ import annotations

from typing import List

from dash import dash_table, dcc, html

from randommatrix.charts import ESTIMATOR_LABELS, ratio_sweep_chart, spectrum_chart
from randommatrix.study import SWEEP_REPETITIONS, RandomMatrixStudy
from ui.components import SCROLLABLE_TABLE_STYLE, TABLE_CELL_STYLE, TABLE_HEADER_STYLE, metric_tile
from ui.random_matrix_content import RISK_TABLE_HINT, SPECTRUM_HINT, SWEEP_HINT

ESTIMATOR_COLUMN = "estimator"


def build_random_matrix_results(study: RandomMatrixStudy) -> html.Div:
    return html.Div(
        className="results",
        children=[_spectrum_section(study), _risk_section(study), _sweep_section(study)],
    )


def _spectrum_section(study: RandomMatrixStudy) -> html.Section:
    spectrum = study.spectrum
    return _section("Spektrum: co je informace a co šum", [
        html.Div(className="metric-grid", children=[
            metric_tile("q = N / T", decimal(study.ratio), "Počet akcií na jedno pozorování."),
            metric_tile(
                "Vlastních čísel v pásu šumu", percent(spectrum.share_inside_band),
                "Podíl vlastních čísel pod horní mezí λ₊ Marčenkova–Pasturova rozdělení.",
            ),
            metric_tile(
                "Nad pásem (informace)", str(spectrum.count_above_band),
                f"Model má 1 tržní faktor a {study.market.sector_count} sektorů.",
            ),
            metric_tile(
                "σ² šumu: odhad / skutečnost",
                f"{decimal(spectrum.band.variance)} / {decimal(spectrum.true_noise_variance)}",
                "Odhad 1 − λ_max/N ubere jen tržní mód; skutečnost ubírá i sektory.",
            ),
        ]),
        dcc.Graph(figure=spectrum_chart(spectrum)),
        dcc.Markdown(SPECTRUM_HINT, mathjax=True, className="hint small"),
    ])


def _risk_section(study: RandomMatrixStudy) -> html.Section:
    rows = [
        {
            ESTIMATOR_COLUMN: ESTIMATOR_LABELS[estimator],
            "in_sample": decimal(risk.in_sample),
            "out_of_sample": decimal(risk.out_of_sample),
            "underestimation": f"{decimal(risk.underestimation)}×",
        }
        for estimator, risk in study.risks.items()
    ]
    return _section("Portfolio s minimálním rozptylem: slib a skutečnost", [
        dash_table.DataTable(
            data=rows,
            columns=[
                {"id": ESTIMATOR_COLUMN, "name": "Odhad korelační matice"},
                {"id": "in_sample", "name": "Slíbený rozptyl / optimum"},
                {"id": "out_of_sample", "name": "Skutečný rozptyl / optimum"},
                {"id": "underestimation", "name": "Skutečný / slíbený"},
            ],
            style_cell=TABLE_CELL_STYLE,
            style_cell_conditional=[{"if": {"column_id": ESTIMATOR_COLUMN}, "textAlign": "left"}],
            style_header=TABLE_HEADER_STYLE,
            style_table=SCROLLABLE_TABLE_STYLE,
        ),
        dcc.Markdown(RISK_TABLE_HINT, mathjax=True, className="hint small"),
    ])


def _sweep_section(study: RandomMatrixStudy) -> html.Section:
    return _section("Jak chyba roste s poměrem q = N/T", [
        dcc.Graph(figure=ratio_sweep_chart(study.sweep, study.ratio)),
        dcc.Markdown(
            SWEEP_HINT.format(asset_count=study.market.asset_count, repetitions=SWEEP_REPETITIONS),
            mathjax=True, className="hint small",
        ),
    ])


def _section(title: str, children: List) -> html.Section:
    return html.Section(className="card", children=[html.H2(title), *children])


def decimal(value: float) -> str:
    return f"{value:.2f}".replace(".", ",")


def percent(value: float) -> str:
    return f"{100 * value:.0f} %"
