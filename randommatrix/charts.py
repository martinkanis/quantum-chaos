"""Charts of the random matrix page."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from randommatrix.cleaning import Estimator
from randommatrix.min_variance import predicted_in_sample, predicted_out_of_sample
from randommatrix.study import RatioSweep, SpectrumStudy

SAMPLE_COLOR = "#2a6fdb"
CLIPPED_COLOR = "#2e9e5b"
SHRINKAGE_COLOR = "#d9822b"
THEORY_COLOR = "#7b3fe4"
MUTED_COLOR = "#9aa3b2"
ESTIMATOR_COLORS = {
    Estimator.SAMPLE: SAMPLE_COLOR,
    Estimator.CLIPPED: CLIPPED_COLOR,
    Estimator.LINEAR_SHRINKAGE: SHRINKAGE_COLOR,
}
ESTIMATOR_LABELS = {
    Estimator.SAMPLE: "surová výběrová matice",
    Estimator.CLIPPED: "ořezání vlastních čísel",
    Estimator.LINEAR_SHRINKAGE: "lineární shrinkage (Ledoit–Wolf)",
}
CHART_MARGIN = dict(t=60, b=40, l=10, r=10)
CHART_LEGEND = dict(orientation="h", yanchor="bottom", y=1.02, x=0)
HISTOGRAM_BINS = 60
DENSITY_POINTS = 400
VISIBLE_RANGE_MARGIN = 1.15
"""The market eigenvalue lies far to the right; the axis stops just after the next largest one."""


def spectrum_chart(spectrum: SpectrumStudy) -> go.Figure:
    """Histogram of the sample eigenvalues against the Marchenko–Pastur density of pure noise."""
    market_mode = spectrum.eigenvalues[-1]
    x_max = VISIBLE_RANGE_MARGIN * max(spectrum.eigenvalues[-2], spectrum.band.upper)
    grid = np.linspace(spectrum.band.lower, spectrum.band.upper, DENSITY_POINTS)
    figure = go.Figure()
    figure.add_trace(go.Histogram(
        x=spectrum.eigenvalues[:-1], histnorm="probability density", name="vlastní čísla z dat",
        xbins=dict(start=0, end=x_max, size=x_max / HISTOGRAM_BINS), marker_color=SAMPLE_COLOR, opacity=0.6,
        hovertemplate="λ ≈ %{x:.2f}<extra></extra>",
    ))
    figure.add_trace(go.Scatter(
        x=grid, y=spectrum.band.density(grid), name="Marčenko–Pastur (čistý šum)", mode="lines",
        line=dict(color=THEORY_COLOR, width=3), hoverinfo="skip",
    ))
    figure.add_vline(
        x=spectrum.band.upper, line=dict(color=THEORY_COLOR, dash="dash"), annotation_text="horní mez šumu λ₊",
    )
    figure.add_annotation(
        x=x_max, y=1, yref="paper", xanchor="right", yanchor="top", showarrow=False,
        text=f"tržní mód λ = {market_mode:.0f} leží mimo graf →",
    )
    figure.update_xaxes(title="Vlastní číslo λ výběrové korelační matice", range=[0, x_max])
    figure.update_yaxes(title="Hustota")
    figure.update_layout(height=420, margin=CHART_MARGIN, legend=CHART_LEGEND, bargap=0.05)
    return figure


def ratio_sweep_chart(sweep: RatioSweep, current_ratio: float) -> go.Figure:
    """Variance relative to the optimum against q = N/T: what the raw matrix promises and what each estimator
    delivers, with the large-N predictions for the raw matrix."""
    grid = np.linspace(0, sweep.ratios.max(), DENSITY_POINTS)
    figure = go.Figure()
    figure.add_trace(go.Scatter(
        x=grid, y=[predicted_out_of_sample(ratio) for ratio in grid], name="teorie: skutečný rozptyl 1/(1−q)",
        mode="lines", line=dict(color=THEORY_COLOR, width=2), hoverinfo="skip",
    ))
    figure.add_trace(go.Scatter(
        x=grid, y=[predicted_in_sample(ratio) for ratio in grid], name="teorie: slíbený rozptyl 1−q",
        mode="lines", line=dict(color=THEORY_COLOR, width=2, dash="dash"), hoverinfo="skip",
    ))
    figure.add_trace(go.Scatter(
        x=sweep.ratios, y=sweep.sample_in_sample, name="surová matice: slíbený", mode="markers",
        marker=dict(color=SAMPLE_COLOR, symbol="circle-open", size=10),
        hovertemplate="q = %{x:.1f}: %{y:.2f}× optimum<extra>slíbený</extra>",
    ))
    for estimator, values in sweep.out_of_sample.items():
        label = ESTIMATOR_LABELS[estimator]
        figure.add_trace(go.Scatter(
            x=sweep.ratios, y=values, name=f"{label}: skutečný", mode="lines+markers",
            line=dict(color=ESTIMATOR_COLORS[estimator], width=3),
            hovertemplate=f"q = %{{x:.1f}}: %{{y:.2f}}× optimum<extra>{label}</extra>",
        ))
    figure.add_hline(y=1, line=dict(color=MUTED_COLOR, dash="dot"), annotation_text="optimum (zná pravdu)")
    figure.add_vline(x=current_ratio, line=dict(color=MUTED_COLOR, dash="dot"), annotation_text="tvoje q")
    figure.update_xaxes(title="q = N / T (akcií na jedno pozorování)")
    figure.update_yaxes(title="Rozptyl portfolia / nejmenší možný", rangemode="tozero")
    figure.update_layout(height=460, margin=CHART_MARGIN, legend=CHART_LEGEND)
    return figure
