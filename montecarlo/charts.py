from __future__ import annotations

from typing import Dict

import numpy as np
import plotly.graph_objects as go

from montecarlo.metrics import SummaryMetrics
from montecarlo.simulation import MONTHS_PER_YEAR

HISTOGRAM_BIN_COUNT = 60
SAMPLE_PATH_COUNT = 30

MAIN_COLOR = "#2a6fdb"
BAND_OUTER_COLOR = "rgba(42, 111, 219, 0.15)"
BAND_INNER_COLOR = "rgba(42, 111, 219, 0.30)"
SAMPLE_PATH_COLOR = "rgba(120, 120, 120, 0.25)"
LOSS_COLOR = "#d64545"
GAIN_COLOR = "#2e9e5b"
NEUTRAL_COLOR = "#555555"


def final_value_histogram(final_values: np.ndarray, metrics: SummaryMetrics) -> go.Figure:
    figure = go.Figure(
        go.Histogram(
            x=final_values,
            nbinsx=HISTOGRAM_BIN_COUNT,
            marker_color=MAIN_COLOR,
            opacity=0.85,
            name="Konečná hodnota",
            hovertemplate="Hodnota: %{x:,.0f}<br>Počet simulací: %{y}<extra></extra>",
        )
    )
    # Contributed capital and the 5th percentile are often close; labelling them on opposite
    # sides of their lines keeps the annotations from overlapping.
    reference_lines = (
        (metrics.total_contributed, "Vloženo", NEUTRAL_COLOR, "dash", "top right"),
        (metrics.percentile_5, "5. percentil", LOSS_COLOR, "dot", "top left"),
        (metrics.median, "Medián", MAIN_COLOR, "solid", "top"),
        (metrics.percentile_95, "95. percentil", GAIN_COLOR, "dot", "top"),
    )
    for value, label, color, dash, label_position in reference_lines:
        figure.add_vline(
            x=value,
            line=dict(color=color, dash=dash, width=2),
            annotation_text=label,
            annotation_position=label_position,
        )
    figure.update_layout(
        xaxis_title="Hodnota portfolia na konci horizontu",
        yaxis_title="Počet simulací",
        bargap=0.02,
        showlegend=False,
        margin=dict(t=40, b=40),
    )
    return figure


def percentile_fan_chart(bands: Dict[int, np.ndarray], sample_paths: np.ndarray) -> go.Figure:
    years = np.arange(len(bands[50])) / MONTHS_PER_YEAR
    figure = go.Figure()

    for path in sample_paths[:SAMPLE_PATH_COUNT]:
        figure.add_trace(
            go.Scatter(
                x=years, y=path, mode="lines", line=dict(color=SAMPLE_PATH_COLOR, width=1),
                hoverinfo="skip", showlegend=False,
            )
        )

    _add_band(figure, years, bands[5], bands[95], BAND_OUTER_COLOR, "5.–95. percentil")
    _add_band(figure, years, bands[25], bands[75], BAND_INNER_COLOR, "25.–75. percentil")
    figure.add_trace(
        go.Scatter(
            x=years, y=bands[50], mode="lines", line=dict(color=MAIN_COLOR, width=3),
            name="Medián", hovertemplate="Rok %{x:.1f}<br>Medián: %{y:,.0f}<extra></extra>",
        )
    )
    figure.update_layout(
        xaxis_title="Roky",
        yaxis_title="Hodnota portfolia",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(t=40, b=40),
    )
    return figure


def _add_band(
    figure: go.Figure, years: np.ndarray, lower: np.ndarray, upper: np.ndarray, color: str, name: str
) -> None:
    figure.add_trace(
        go.Scatter(x=years, y=upper, mode="lines", line=dict(width=0), hoverinfo="skip", showlegend=False)
    )
    figure.add_trace(
        go.Scatter(
            x=years, y=lower, mode="lines", line=dict(width=0), fill="tonexty", fillcolor=color,
            name=name, hoverinfo="skip",
        )
    )
