"""Chart of the photon counters on the bench: how often each detector clicked against how often it should."""

from __future__ import annotations

import plotly.graph_objects as go

from gbs.bench import PhotonCounts
from gbs.charts import CHART_LEGEND, CHART_LEGEND_MARGIN, EXACT_COLOR, GBS_COLOR

CHART_HEIGHT = 300


def counts_chart(counts: PhotonCounts) -> go.Figure:
    labels = [f"detektor {number}" for number in range(1, len(counts.clicks) + 1)]
    figure = go.Figure()
    figure.add_trace(go.Bar(x=labels, y=counts.clicks, name="cvaknutí", marker_color=GBS_COLOR))
    figure.add_trace(go.Scatter(
        x=labels, y=counts.expected, mode="markers", name="průměr, který se dá čekat",
        marker=dict(color=EXACT_COLOR, size=12, symbol="diamond"),
    ))
    figure.update_layout(
        margin=CHART_LEGEND_MARGIN, legend=CHART_LEGEND, height=CHART_HEIGHT,
        yaxis=dict(title="počet cvaknutí", rangemode="tozero"), xaxis=dict(type="category"),
    )
    return figure
