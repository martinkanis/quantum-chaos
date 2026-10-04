"""Charts of the advantage lab (page 3)."""

from __future__ import annotations

import plotly.graph_objects as go

from gbs.charts import CHART_LEGEND, CHART_LEGEND_MARGIN, CHART_MARGIN, EXACT_COLOR, GBS_COLOR, MC_COLOR, MUTED_COLOR
from gbs.monomial_problem import DegreeSweep
from gbs.monomial_study import MonomialStudy
from gbs.photon_tuning import TuningMode

TUNING_LABELS = {
    TuningMode.PER_MODE: "GBS-P, ladění po módech",
    TuningMode.TOTAL: "GBS-P, ladění celkem (článek)",
}


def degree_sweep_chart(sweep: DegreeSweep, current_degree: int, mode: TuningMode) -> go.Figure:
    """Per-sample relative variance against the degree: exponential growth for MC, slow growth for GBS-P."""
    figure = go.Figure()
    figure.add_trace(go.Scatter(
        x=sweep.degrees, y=sweep.mc_relative_variances, name="klasické Monte Carlo", mode="lines+markers",
        line=dict(color=MC_COLOR, width=3), hovertemplate="stupeň %{x}: %{y:.3g}<extra>Monte Carlo</extra>",
    ))
    for tuning in (mode, *[other for other in TuningMode if other is not mode]):
        is_selected = tuning is mode
        figure.add_trace(go.Scatter(
            x=sweep.degrees, y=sweep.gbs_relative_variances[tuning], name=TUNING_LABELS[tuning], mode="lines+markers",
            line=dict(color=GBS_COLOR if is_selected else MUTED_COLOR, width=3 if is_selected else 2,
                      dash="solid" if is_selected else "dash"),
            hovertemplate=f"stupeň %{{x}}: %{{y:.3g}}<extra>{TUNING_LABELS[tuning]}</extra>",
        ))
    figure.add_vline(x=current_degree, line=dict(color=MUTED_COLOR, dash="dot"), annotation_text="zadaný monom")
    figure.update_xaxes(title="Stupeň monomu |n| (stejný poměr exponentů)")
    figure.update_yaxes(type="log", title="Rozptyl jednoho vzorku / μ²", exponentformat="power")
    figure.update_layout(height=420, margin=CHART_LEGEND_MARGIN, legend=CHART_LEGEND)
    return figure


def estimate_spread_chart(study: MonomialStudy) -> go.Figure:
    """Every repetition's estimate after the largest sample size, relative to the exact value."""
    figure = go.Figure()
    for name, estimates, color in (
        ("klasické Monte Carlo", study.mc_final_estimates, MC_COLOR),
        ("GBS-P", study.gbs_final_estimates, GBS_COLOR),
    ):
        figure.add_trace(go.Box(
            y=estimates / study.exact, name=name, boxpoints="all", jitter=0.5, pointpos=0, marker_color=color,
            line_color=color, fillcolor="rgba(0,0,0,0)",
            hovertemplate="odhad / přesná hodnota: %{y:.3f}<extra></extra>",
        ))
    figure.add_hline(y=1, line=dict(color=EXACT_COLOR, dash="dash", width=2), annotation_text="přesná hodnota")
    figure.update_yaxes(title="Odhad / přesná hodnota", rangemode="tozero")
    figure.update_layout(height=380, margin=CHART_MARGIN, showlegend=False)
    return figure
