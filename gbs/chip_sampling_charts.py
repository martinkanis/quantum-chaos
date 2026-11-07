"""Charts of boson sampling on the chip: how both Monte Carlo estimates converge and what values the shots take."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from gbs.charts import CHART_LEGEND, CHART_LEGEND_MARGIN, EXACT_COLOR, GBS_COLOR, MC_COLOR, MUTED_COLOR
from gbs.chip_boson_sampling import PatternDistribution, SamplingStudy, running_means

CHECKPOINT_COUNT = 80
FIRST_CHECKPOINT = 10
LIMIT_COLOR = "#d9822b"
VISIBLE_BIAS = 1e-6
"""Below this relative difference the chip limit coincides with the exact value and is not drawn."""
Y_RANGE_FACTOR = 2.0


def convergence_chart(study: SamplingStudy) -> go.Figure:
    samples = len(study.shot_indices)
    checkpoints = np.unique(np.geomspace(min(FIRST_CHECKPOINT, samples), samples, CHECKPOINT_COUNT).astype(int))
    exact = study.target.bunching
    figure = go.Figure()
    figure.add_trace(go.Scatter(
        x=checkpoints, y=running_means(study.gaussian_values, checkpoints), mode="lines",
        name="klasické MC (gaussovské vektory)", line=dict(color=MC_COLOR),
    ))
    figure.add_trace(go.Scatter(
        x=checkpoints, y=running_means(study.shot_values, checkpoints), mode="lines",
        name="boson sampling na čipu", line=dict(color=GBS_COLOR, width=3),
    ))
    figure.add_hline(y=exact, line=dict(color=EXACT_COLOR, dash="dash"), annotation_text="přesné μ")
    if abs(study.bias) > VISIBLE_BIAS:
        figure.add_hline(
            y=study.sampler.bunching, line=dict(color=LIMIT_COLOR, dash="dot"),
            annotation_text="kam konverguje čip", annotation_position="bottom right",
        )
    figure.update_layout(
        margin=CHART_LEGEND_MARGIN, legend=CHART_LEGEND, height=380,
        xaxis=dict(type="log", title="počet vzorků N"),
        yaxis=dict(title="odhad μ", range=[0, Y_RANGE_FACTOR * exact]),
    )
    return figure


def shot_value_chart(study: SamplingStudy) -> go.Figure:
    """Share of shots per value Z = S!: exact for the target and the chip, and as observed."""
    values = np.unique(np.concatenate([study.target.multiplicities, study.sampler.multiplicities]))
    observed = np.array([np.mean(study.shot_values == value) for value in values])
    labels = [f"{value:.0f}" for value in values]
    figure = go.Figure()
    figure.add_trace(go.Bar(
        x=labels, y=_share_per_value(study.target, values), name="cíl, nerozlišitelné fotony (přesně)",
        marker_color=EXACT_COLOR,
    ))
    figure.add_trace(go.Bar(
        x=labels, y=_share_per_value(study.sampler, values), name="tento čip a fotony (přesně)", marker_color=MUTED_COLOR,
    ))
    figure.add_trace(go.Scatter(
        x=labels, y=observed, mode="markers", name="naměřeno", marker=dict(color=GBS_COLOR, size=11, symbol="diamond"),
    ))
    figure.update_layout(
        margin=CHART_LEGEND_MARGIN, legend=CHART_LEGEND, height=340, barmode="group",
        xaxis=dict(title="hodnota výstřelu Z = S!", type="category"),
        yaxis=dict(title="podíl výstřelů", tickformat=".0%"),
    )
    return figure


def _share_per_value(distribution: PatternDistribution, values: np.ndarray) -> np.ndarray:
    return np.array([distribution.probabilities[distribution.multiplicities == value].sum() for value in values])
