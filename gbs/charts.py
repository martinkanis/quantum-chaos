from __future__ import annotations

from typing import Dict, Optional, Sequence

import numpy as np
import plotly.graph_objects as go

from gbs.expectation import ConvergenceStudy
from gbs.sampler import GbsProgram

GBS_COLOR = "#7b3fe4"
MC_COLOR = "#2a6fdb"
EXACT_COLOR = "#2e9e5b"
MUTED_COLOR = "#9aa3b2"
WIRE_COLOR = "#1c2330"
SQUEEZER_FILL = "#efe7fd"
INTERFEROMETER_FILL = "rgba(154, 163, 178, 0.18)"
DETECTOR_FILL = "#e3f4ea"
DEGREE_COLORS = {2: MC_COLOR, 4: GBS_COLOR, 6: "#d9822b"}

SQUEEZER_X = (0.6, 2.2)
INTERFEROMETER_X = (3.0, 7.0)
DETECTOR_X = (7.8, 8.6)
WIRE_END_X = 9.2
OUTPUT_LABEL_X = 9.35
BOX_HALF_HEIGHT = 0.32
PATTERN_BAR_COUNT = 12
CHART_MARGIN = dict(t=30, b=40, l=10, r=10)
CHART_LEGEND_MARGIN = dict(t=60, b=40, l=10, r=10)
CHART_LEGEND = dict(orientation="h", yanchor="bottom", y=1.02, x=0)


def circuit_diagram(program: GbsProgram, asset_labels: Sequence[str]) -> go.Figure:
    """Optical circuit: squeezed vacuum → interferometer U → photon counters.

    Input mode j carries the j-th principal component of Σ; output mode i is asset i.
    """
    figure = go.Figure()
    mode_count = program.mode_count
    top, bottom = _wire_y(0, mode_count) + 0.5, _wire_y(mode_count - 1, mode_count) - 0.5
    figure.add_shape(
        type="rect", x0=INTERFEROMETER_X[0], x1=INTERFEROMETER_X[1], y0=bottom, y1=top,
        fillcolor=INTERFEROMETER_FILL, line=dict(color=MUTED_COLOR),
    )
    for mode in range(mode_count):
        wire_y = _wire_y(mode, mode_count)
        figure.add_shape(type="line", x0=0, x1=WIRE_END_X, y0=wire_y, y1=wire_y, line=dict(color=WIRE_COLOR, width=1.5))
        _add_box(figure, SQUEEZER_X, wire_y, SQUEEZER_FILL, GBS_COLOR, f"S(r = {program.squeezing[mode]:.2f})")
        _add_box(figure, DETECTOR_X, wire_y, DETECTOR_FILL, EXACT_COLOR, f"n<sub>{mode + 1}</sub>")
        figure.add_annotation(x=-0.1, y=wire_y, text=f"vstup {mode + 1}  |0⟩", showarrow=False, xanchor="right")
        figure.add_annotation(
            x=OUTPUT_LABEL_X, y=wire_y, text=asset_labels[mode], showarrow=False, xanchor="left",
        )
    _add_beam_splitter_mesh(figure, mode_count)

    for x, label in (
        (np.mean(SQUEEZER_X), "① stlačení"),
        (np.mean(INTERFEROMETER_X), "② interferometr U"),
        (np.mean(DETECTOR_X), "③ detekce"),
    ):
        figure.add_annotation(x=x, y=top + 0.35, text=f"<b>{label}</b>", showarrow=False)

    figure.update_xaxes(visible=False, range=[-2.2, OUTPUT_LABEL_X + 2.2])
    figure.update_yaxes(visible=False, range=[bottom - 0.2, top + 0.7])
    figure.update_layout(
        height=110 + 70 * mode_count, margin=dict(t=10, b=10, l=10, r=10),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
    )
    return figure


def covariance_heatmap(covariance: np.ndarray, asset_labels: Sequence[str]) -> go.Figure:
    return _heatmap(covariance, list(asset_labels), list(asset_labels), ".4f", "Blues")


def interferometer_heatmap(program: GbsProgram, asset_labels: Sequence[str]) -> go.Figure:
    """Rows are output modes (assets), columns input modes; column j is the j-th principal component."""
    input_labels = [f"vstup {mode + 1}" for mode in range(program.mode_count)]
    return _heatmap(np.abs(program.interferometer), list(asset_labels), input_labels, ".2f", "Purples")


def shot_stream_heatmap(
    shots: Sequence[Optional[np.ndarray]], target_total: int, mode_labels: Sequence[str], max_listed_total: int
) -> go.Figure:
    counts = [shot if shot is not None else np.full(len(mode_labels), np.nan) for shot in shots]
    row_labels = [_shot_label(index, shot, target_total, max_listed_total) for index, shot in enumerate(shots)]
    figure = go.Figure(
        go.Heatmap(
            z=np.array(counts, dtype=float), x=list(mode_labels), y=row_labels, colorscale="Purples",
            text=[["" if np.isnan(value) else str(int(value)) for value in row] for row in np.array(counts, dtype=float)],
            texttemplate="%{text}", hovertemplate="%{y}, %{x}: %{text} fotonů<extra></extra>",
            showscale=False, xgap=2, ygap=2,
        )
    )
    figure.update_yaxes(autorange="reversed")
    figure.update_layout(height=80 + 22 * len(shots), margin=CHART_MARGIN)
    return figure


def photon_total_chart(total_probabilities: np.ndarray, target_total: int) -> go.Figure:
    totals = np.arange(0, len(total_probabilities), 2)
    probabilities = total_probabilities[totals]
    remainder = max(0.0, 1.0 - total_probabilities.sum())
    labels = [str(total) for total in totals] + [f"> {totals[-1]}"]
    colors = [GBS_COLOR if total == target_total else MUTED_COLOR for total in totals] + [MUTED_COLOR]
    figure = go.Figure(
        go.Bar(
            x=labels, y=list(probabilities) + [remainder], marker_color=colors,
            hovertemplate="Celkem %{x} fotonů: %{y:.2%}<extra></extra>",
        )
    )
    figure.update_layout(
        xaxis_title="Celkový počet fotonů ve výstřelu", yaxis_title="Pravděpodobnost",
        yaxis_tickformat=".0%", height=320, margin=CHART_MARGIN,
    )
    return figure


def pattern_frequency_chart(study: ConvergenceStudy) -> go.Figure:
    top_indices = np.argsort(study.pattern_probabilities)[::-1][:PATTERN_BAR_COUNT]
    labels = [pattern_label(study.patterns[index]) for index in top_indices]
    shot_count = study.sample_sizes[-1]
    figure = go.Figure()
    figure.add_trace(go.Bar(
        x=labels, y=study.pattern_probabilities[top_indices], name="přesná p(n)", marker_color=EXACT_COLOR,
    ))
    figure.add_trace(go.Bar(
        x=labels, y=study.observed_pattern_counts[top_indices] / shot_count,
        name=f"četnost z {shot_count:,} výstřelů".replace(",", " "), marker_color=GBS_COLOR,
    ))
    figure.update_layout(
        barmode="group", xaxis_title="Vzor počtů fotonů n = (n₁, …, n_k)", yaxis_title="Pravděpodobnost",
        height=360, margin=CHART_LEGEND_MARGIN, legend=CHART_LEGEND,
    )
    return figure


def convergence_chart(study: ConvergenceStudy) -> go.Figure:
    sizes = study.sample_sizes
    inverse_root = 1 / np.sqrt(sizes)
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=sizes, y=study.gbs_relative_rmse, name="GBS estimátor", mode="lines+markers", line=dict(color=GBS_COLOR, width=3)))
    figure.add_trace(go.Scatter(x=sizes, y=study.mc_relative_rmse, name="klasické Monte Carlo", mode="lines+markers", line=dict(color=MC_COLOR, width=3)))
    for constant, label, color in (
        (study.gbs_error_constant, "GBS", GBS_COLOR),
        (study.mc_error_constant, "MC", MC_COLOR),
    ):
        figure.add_trace(go.Scatter(
            x=sizes, y=constant * inverse_root, name=f"teorie {label}: {constant:.2f}/√N", mode="lines",
            line=dict(color=color, dash="dash"),
        ))
    figure.update_xaxes(type="log", title="Počet vzorků N", dtick=1)
    figure.update_yaxes(type="log", title="Relativní chyba (RMSE)", tickformat=".1%", dtick="D2")
    figure.update_layout(height=400, margin=CHART_LEGEND_MARGIN, legend=CHART_LEGEND)
    return figure


def trajectory_chart(study: ConvergenceStudy) -> go.Figure:
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=study.sample_sizes, y=study.gbs_trajectory, name="GBS odhad", mode="lines+markers", line=dict(color=GBS_COLOR)))
    figure.add_trace(go.Scatter(x=study.sample_sizes, y=study.mc_trajectory, name="MC odhad", mode="lines+markers", line=dict(color=MC_COLOR)))
    figure.add_hline(y=study.exact, line=dict(color=EXACT_COLOR, dash="dash", width=2), annotation_text="přesná hodnota")
    figure.update_xaxes(type="log", title="Počet vzorků N", dtick=1)
    figure.update_yaxes(title="Odhad", exponentformat="e")
    figure.update_layout(height=400, margin=CHART_LEGEND_MARGIN, legend=CHART_LEGEND)
    return figure


def _heatmap(
    matrix: np.ndarray, row_labels: list, column_labels: list, value_format: str, colorscale: str
) -> go.Figure:
    figure = go.Figure(
        go.Heatmap(
            z=matrix, x=column_labels, y=row_labels, colorscale=colorscale,
            text=[[format(value, value_format) for value in row] for row in matrix],
            texttemplate="%{text}", hovertemplate="%{y} × %{x}: %{text}<extra></extra>", showscale=False,
        )
    )
    figure.update_yaxes(autorange="reversed")
    figure.update_layout(height=120 + 45 * len(row_labels), margin=CHART_MARGIN)
    return figure


def useful_fraction_chart(
    strengths: np.ndarray, fractions_by_degree: Dict[int, np.ndarray], highlighted_strength: float
) -> go.Figure:
    figure = go.Figure()
    for degree, fractions in fractions_by_degree.items():
        figure.add_trace(go.Scatter(
            x=strengths, y=fractions, mode="lines+markers", name=f"d = {degree}",
            line=dict(color=DEGREE_COLORS.get(degree, MUTED_COLOR), width=3),
            hovertemplate=f"d = {degree}, tanh r_max = %{{x:.2f}}: %{{y:.1%}}<extra></extra>",
        ))
    figure.add_vline(
        x=highlighted_strength, line=dict(color=MUTED_COLOR, dash="dash"), annotation_text="výchozí nastavení",
    )
    figure.update_xaxes(title="Síla stlačení tanh(r_max)")
    figure.update_yaxes(title="Podíl užitečných výstřelů", tickformat=".0%", rangemode="tozero")
    figure.update_layout(height=360, margin=CHART_LEGEND_MARGIN, legend=CHART_LEGEND)
    return figure


def error_constant_chart(
    strengths: np.ndarray,
    gbs_constants_by_degree: Dict[int, np.ndarray],
    mc_constants_by_degree: Dict[int, float],
    highlighted_strength: float,
) -> go.Figure:
    """Solid lines: GBS constant per squeezing strength; dashed: the strength-independent MC constant."""
    figure = go.Figure()
    for degree, constants in gbs_constants_by_degree.items():
        color = DEGREE_COLORS.get(degree, MUTED_COLOR)
        figure.add_trace(go.Scatter(
            x=strengths, y=constants, mode="lines+markers", name=f"GBS, d = {degree}", line=dict(color=color, width=3),
            hovertemplate=f"GBS, d = {degree}, tanh r_max = %{{x:.2f}}: c = %{{y:.2f}}<extra></extra>",
        ))
        mc_constant = mc_constants_by_degree[degree]
        figure.add_trace(go.Scatter(
            x=[strengths[0], strengths[-1]], y=[mc_constant, mc_constant], mode="lines", name=f"MC, d = {degree}",
            line=dict(color=color, dash="dash"),
            hovertemplate=f"MC, d = {degree}: c = {mc_constant:.2f}<extra></extra>",
        ))
    figure.add_vline(
        x=highlighted_strength, line=dict(color=MUTED_COLOR, dash="dot"), annotation_text="výchozí nastavení",
    )
    figure.update_xaxes(title="Síla stlačení tanh(r_max)")
    figure.update_yaxes(type="log", title="Konstanta chyby c (chyba ≈ c/√N)", dtick="D2")
    figure.update_layout(height=400, margin=CHART_LEGEND_MARGIN, legend=CHART_LEGEND)
    return figure


def _wire_y(mode: int, mode_count: int) -> float:
    return float(mode_count - 1 - mode)


def _add_box(figure: go.Figure, x_range, wire_y: float, fill: str, border: str, label: str) -> None:
    figure.add_shape(
        type="rect", x0=x_range[0], x1=x_range[1], y0=wire_y - BOX_HALF_HEIGHT, y1=wire_y + BOX_HALF_HEIGHT,
        fillcolor=fill, line=dict(color=border),
    )
    figure.add_annotation(x=float(np.mean(x_range)), y=wire_y, text=label, showarrow=False)


def _add_beam_splitter_mesh(figure: go.Figure, mode_count: int) -> None:
    """Rectangular (Clements) mesh: any k×k unitary needs k layers of neighbouring beam splitters."""
    if mode_count < 2:
        return
    margin = 0.4
    step = (INTERFEROMETER_X[1] - INTERFEROMETER_X[0] - 2 * margin) / max(mode_count - 1, 1)
    for layer in range(mode_count):
        x = INTERFEROMETER_X[0] + margin + layer * step
        for upper_mode in range(layer % 2, mode_count - 1, 2):
            upper, lower = _wire_y(upper_mode, mode_count), _wire_y(upper_mode + 1, mode_count)
            for start, end in ((upper, lower), (lower, upper)):
                figure.add_shape(
                    type="line", x0=x - 0.2, x1=x + 0.2, y0=start, y1=end, line=dict(color=MUTED_COLOR, width=2),
                )


def _shot_label(index: int, shot: Optional[np.ndarray], target_total: int, max_listed_total: int) -> str:
    if shot is None:
        return f"#{index + 1} (> {max_listed_total} fotonů)"
    marker = " ✓" if shot.sum() == target_total else ""
    return f"#{index + 1}{marker}"


def pattern_label(pattern: np.ndarray) -> str:
    return "(" + ", ".join(str(int(photons)) for photons in pattern) + ")"
