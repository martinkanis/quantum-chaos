"""Charts of the photon loss lab: samples needed against the transmission, and the estimates without correction."""

from __future__ import annotations

from typing import List, Optional

import plotly.graph_objects as go

from gbs.charts import CHART_LEGEND, CHART_LEGEND_MARGIN, EXACT_COLOR, GBS_COLOR, MC_COLOR, MUTED_COLOR
from gbs.loss_study import LossStudy
from gbs.monomial_problem import required_samples

THRESHOLD_COLOR = "#d9822b"
DIVERGENCE_FILL = "rgba(154, 163, 178, 0.18)"
PERCENT = 100
BENCH_LABEL_DROP = 22
"""Pixels the bench label moves down, below the label of the classical-simulation line next to it."""


def samples_chart(study: LossStudy, relative_error: float, bench_transmission: Optional[float]) -> go.Figure:
    """Samples for the relative error against the transmission: Monte Carlo does not care, the corrected GBS-P
    estimate needs ever more shots and below the critical transmission none suffice."""
    converged = [point for point in study.sweep if point.correction_converged]
    figure = go.Figure()
    figure.add_trace(go.Scatter(
        x=_percent([point.transmission for point in study.sweep]),
        y=[required_samples(study.comparison.mc_relative_variance, relative_error)] * len(study.sweep),
        name="klasické Monte Carlo", mode="lines", line=dict(color=MC_COLOR, width=3),
        hovertemplate="%{y:.3s} scénářů<extra>Monte Carlo</extra>",
    ))
    figure.add_trace(go.Scatter(
        x=_percent([point.transmission for point in converged]),
        y=[required_samples(point.corrected_relative_variance, relative_error) for point in converged],
        name="GBS-P s nestrannou opravou ztrát", mode="lines+markers", line=dict(color=GBS_COLOR, width=3),
        hovertemplate="η = %{x} %: %{y:.3s} výstřelů<extra>GBS-P s opravou</extra>",
    ))
    if study.chosen.correction_converged:
        figure.add_trace(go.Scatter(
            x=_percent([study.chosen.transmission]),
            y=[required_samples(study.chosen.corrected_relative_variance, relative_error)],
            name="zvolená propustnost", mode="markers",
            marker=dict(color=GBS_COLOR, size=14, symbol="diamond", line=dict(color="white", width=2)),
            hovertemplate="η = %{x} %: %{y:.3s} výstřelů<extra>zvolená propustnost</extra>",
        ))
    figure.add_vrect(
        x0=0, x1=PERCENT * study.critical_transmission, fillcolor=DIVERGENCE_FILL, line_width=0,
        annotation_text="oprava má nekonečný rozptyl", annotation_position="bottom right",
    )
    _add_boundaries(figure, study, bench_transmission)
    figure.update_xaxes(title="Propustnost η (%): podíl fotonů, které dorazí k detektorům", range=[0, PERCENT + 2])
    figure.update_yaxes(
        type="log", title=f"Vzorků pro relativní chybu {_percent_label(relative_error)}", exponentformat="power",
    )
    figure.update_layout(height=460, margin=CHART_LEGEND_MARGIN, legend=CHART_LEGEND)
    return figure


def bias_chart(study: LossStudy) -> go.Figure:
    """Estimate over exact value without any correction, for photon counters and for threshold detectors.

    Transmissions where the kept patterns do not reach far enough for p_η(n) are left out of the counter curve.
    """
    reliable = [point for point in study.sweep if point.probability_reliable]
    figure = go.Figure()
    figure.add_trace(go.Scatter(
        x=_percent([point.transmission for point in reliable]),
        y=[1 + point.naive_bias for point in reliable],
        name="detektory počítající fotony, bez opravy", mode="lines+markers", line=dict(color=GBS_COLOR, width=3),
        hovertemplate="η = %{x} %: odhad = %{y:.3f} × přesná hodnota<extra>bez opravy</extra>",
    ))
    figure.add_trace(go.Scatter(
        x=_percent([point.transmission for point in study.sweep]),
        y=[1 + point.threshold_bias for point in study.sweep],
        name="prahové detektory (klik ano/ne)", mode="lines+markers",
        line=dict(color=THRESHOLD_COLOR, width=2, dash="dash"),
        hovertemplate="η = %{x} %: odhad = %{y:.3f} × přesná hodnota<extra>prahové detektory</extra>",
    ))
    figure.add_trace(go.Scatter(
        x=_percent([study.chosen.transmission]), y=[1 + study.chosen.naive_bias], name="zvolená propustnost",
        mode="markers", marker=dict(color=GBS_COLOR, size=14, symbol="diamond", line=dict(color="white", width=2)),
        hovertemplate="η = %{x} %: odhad = %{y:.3f} × přesná hodnota<extra>zvolená propustnost</extra>",
    ))
    figure.add_hline(y=1, line=dict(color=EXACT_COLOR, dash="dash", width=2), annotation_text="přesná hodnota")
    figure.update_xaxes(title="Propustnost η (%)", range=[0, PERCENT + 2])
    figure.update_yaxes(type="log", title="Odhad / přesná hodnota", exponentformat="power")
    figure.update_layout(height=420, margin=CHART_LEGEND_MARGIN, legend=CHART_LEGEND)
    return figure


def _add_boundaries(figure: go.Figure, study: LossStudy, bench_transmission: Optional[float]) -> None:
    """The labels sit in different corners of their lines, so that they do not overlap near the left edge."""
    figure.add_vline(
        x=PERCENT * study.critical_transmission, line=dict(color=MUTED_COLOR, dash="dot"),
        annotation_text="kritická propustnost", annotation_position="top right",
    )
    figure.add_vline(
        x=PERCENT * study.simulable_transmission, line=dict(color=MC_COLOR, dash="dot"),
        annotation_text="klasická simulace (Qi 2020)", annotation_position="top right",
    )
    if bench_transmission is not None:
        figure.add_vline(
            x=PERCENT * bench_transmission, line=dict(color=THRESHOLD_COLOR, dash="dashdot"),
            annotation_text="pracovní stůl simulátoru čipu", annotation_position="top left",
            annotation_yshift=-BENCH_LABEL_DROP,
        )


def _percent(values: List[float]) -> List[float]:
    return [PERCENT * value for value in values]


def _percent_label(value: float) -> str:
    return f"{PERCENT * value:g} %".replace(".", ",")
