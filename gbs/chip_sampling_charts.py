"""Charts of boson sampling on the chip: how both Monte Carlo estimates converge and what values the shots take."""

from __future__ import annotations

from typing import Any, Dict, List

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
CZECH_SEPARATORS = ", "
"""Plotly separators: decimal comma, then a space between thousands."""
AROUND_EXACT_PADDING = 0.25
"""Share of the chip curve's span added above and below it when the y axis zooms in around μ."""
MIN_AROUND_EXACT_SPAN = 0.01
"""Smallest span of the zoomed y axis relative to μ, so that a flat chip curve still gets an axis."""
CONVERGENCE_HEIGHT = 480
MODEBAR_ROOM = 34
"""Pixels kept free at the top of the chart for Plotly's zoom buttons, so they do not cover the axis buttons."""
AXIS_BUTTON_ROW = 32
"""One row of axis buttons; x and y get a row each so that they fit next to each other on a phone."""
LEGEND_ROOM = 66
"""Pixels between the axis buttons and the plot; the legend wraps to two rows there on a phone."""
CONVERGENCE_MARGIN = dict(CHART_LEGEND_MARGIN, t=MODEBAR_ROOM + 2 * AXIS_BUTTON_ROW + LEGEND_ROOM)
PLOT_HEIGHT = CONVERGENCE_HEIGHT - CONVERGENCE_MARGIN["t"] - CONVERGENCE_MARGIN["b"]
AXIS_BUTTON_FONT = dict(size=12)


def convergence_chart(study: SamplingStudy) -> go.Figure:
    """Running estimates of μ; menus above the plot switch the x axis scale and zoom the y axis around μ."""
    samples = len(study.shot_indices)
    checkpoints = np.unique(np.geomspace(min(FIRST_CHECKPOINT, samples), samples, CHECKPOINT_COUNT).astype(int))
    exact = study.target.bunching
    chip_means = running_means(study.shot_values, checkpoints)
    figure = go.Figure()
    figure.add_trace(go.Scatter(
        x=checkpoints, y=running_means(study.gaussian_values, checkpoints), mode="lines",
        name="klasické MC (gaussovské vektory)", line=dict(color=MC_COLOR),
    ))
    figure.add_trace(go.Scatter(
        x=checkpoints, y=chip_means, mode="lines",
        name="boson sampling na čipu", line=dict(color=GBS_COLOR, width=3),
    ))
    figure.add_hline(y=exact, line=dict(color=EXACT_COLOR, dash="dash"), annotation_text="přesné μ")
    if abs(study.bias) > VISIBLE_BIAS:
        figure.add_hline(
            y=study.sampler.bunching, line=dict(color=LIMIT_COLOR, dash="dot"),
            annotation_text="kam konverguje čip", annotation_position="bottom right",
        )
    default_range = [0, Y_RANGE_FACTOR * exact]
    figure.update_layout(
        margin=CONVERGENCE_MARGIN, legend=CHART_LEGEND, height=CONVERGENCE_HEIGHT, separators=CZECH_SEPARATORS,
        xaxis=dict(type="log", title="počet vzorků N", exponentformat="none"),
        yaxis=dict(title="odhad μ", range=default_range),
        updatemenus=_axis_buttons(default_range, range_around_exact(study, chip_means)),
    )
    return figure


def range_around_exact(study: SamplingStudy, chip_means: np.ndarray) -> List[float]:
    """Y range that shows how the chip estimate wanders around μ once the first shots stop dominating it."""
    settled = chip_means[len(chip_means) // 2:]
    levels = [study.target.bunching, study.sampler.bunching, float(settled.min()), float(settled.max())]
    low, high = min(levels), max(levels)
    span = max(high - low, MIN_AROUND_EXACT_SPAN * study.target.bunching)
    padding = AROUND_EXACT_PADDING * span
    return [low - padding, high + padding]


def _axis_buttons(default_range: List[float], around_exact: List[float]) -> List[Dict[str, Any]]:
    """Rows of buttons that change the axes. They act like commands and do not mark a chosen one: Dash redraws the
    chart after each change and Plotly would mark the first button again, while the axes keep the change."""
    x_scales = [
        _menu_button("X logaritmicky", {"xaxis.type": "log", "xaxis.autorange": True}),
        _menu_button("X lineárně", {"xaxis.type": "linear", "xaxis.autorange": True}),
    ]
    y_ranges = [
        _menu_button(f"Y 0 až {Y_RANGE_FACTOR:g}μ", {"yaxis.range": default_range}),
        _menu_button("Y kolem μ", {"yaxis.range": around_exact}),
        _menu_button("Y vše", {"yaxis.autorange": True}),
    ]
    return [_button_row(x_scales, rows_above_legend=2), _button_row(y_ranges, rows_above_legend=1)]


def _button_row(buttons: List[Dict[str, Any]], rows_above_legend: int) -> Dict[str, Any]:
    bottom_pixels = LEGEND_ROOM + (rows_above_legend - 1) * AXIS_BUTTON_ROW
    return dict(
        type="buttons", direction="right", buttons=buttons, showactive=False, x=0, xanchor="left",
        y=1 + bottom_pixels / PLOT_HEIGHT, yanchor="bottom", font=AXIS_BUTTON_FONT, pad=dict(t=0, b=0, l=0, r=0),
    )


def _menu_button(label: str, layout_change: Dict[str, Any]) -> Dict[str, Any]:
    return dict(label=label, method="relayout", args=[layout_change])


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
