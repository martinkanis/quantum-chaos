"""Results of the boson sampling lab: both Monte Carlo estimates, the chip with its photons and the shots."""

from __future__ import annotations

from typing import List

import numpy as np
from dash import dcc, html

from gbs.chip_charts import LightSource, chip_figure, figure_height
from gbs.chip_boson_sampling import SamplingStudy
from gbs.chip_sampling_charts import convergence_chart, shot_value_chart
from gbs.photonic_chip import light_flow
from ui.chip_sampling_content import (
    BOSON_HINT,
    BOSON_SHOTS_HINT,
    CONVERGENCE_HINT,
    EXACT_HINT,
    FIRST_SHOTS_HINT,
    GAUSSIAN_HINT,
    GAUSSIAN_SHOTS_HINT,
    LIMIT_HINT,
    SHOT_VALUES_HINT,
    TARGET_RELATIVE_ERROR,
)
from ui.components import metric_tile

FIRST_SHOTS_SHOWN = 8
MIN_FIGURE_WIDTH = 680
FIGURE_WIDTH_PER_MODE = 70
"""Large chips scroll sideways on narrow screens instead of squeezing their MZIs together."""


def build_sampling_results(study: SamplingStudy) -> html.Div:
    return html.Div(className="results", children=[
        html.Div(className="metric-grid", children=_metric_tiles(study)),
        html.Div(className="chip-figure", children=dcc.Graph(
            figure=chip_figure(
                study.chip, study.phases, light_flow(study.chip, study.phases, range(study.photons)),
                LightSource.PHOTONS,
            ),
            style={"minWidth": f"{max(MIN_FIGURE_WIDTH, FIGURE_WIDTH_PER_MODE * study.chip.mode_count)}px",
                   "height": f"{figure_height(study.chip.mode_count)}px"},
            config={"displayModeBar": False, "responsive": True},
        )),
        html.H3("Jak se odhady blíží k μ"),
        dcc.Graph(figure=convergence_chart(study), config={"displayModeBar": False}),
        html.P(CONVERGENCE_HINT, className="hint small"),
        html.H3("Hodnoty výstřelů"),
        dcc.Graph(figure=shot_value_chart(study), config={"displayModeBar": False}),
        html.P(SHOT_VALUES_HINT, className="hint small"),
        html.H3("První výstřely"),
        html.Ol(className="chip-shots", children=[html.Li(label) for label in _first_shot_labels(study)]),
        html.P(FIRST_SHOTS_HINT, className="hint small"),
    ])


def _metric_tiles(study: SamplingStudy) -> List[html.Div]:
    samples = len(study.shot_indices)
    return [
        metric_tile("Výstupních vzorů", czech_count(len(study.target.patterns)),
                    f"{study.photons} fotonů v {study.chip.mode_count} světlovodech."),
        metric_tile("Přesné μ", czech_decimal(study.target.bunching), EXACT_HINT),
        metric_tile(f"Boson sampling, {czech_count(samples)} výstřelů",
                    _with_error(study.estimate, study.standard_error), BOSON_HINT),
        metric_tile(f"Klasické MC, {czech_count(samples)} vzorků",
                    _with_error(study.gaussian_estimate, study.gaussian_standard_error), GAUSSIAN_HINT),
        metric_tile("Výstřelů na 1 % přesnost", czech_count(_samples_for_target(study.sampler.relative_variance)),
                    BOSON_SHOTS_HINT),
        metric_tile("Klasických vzorků na 1 %", czech_count(_samples_for_target(study.gaussian_relative_variance)),
                    GAUSSIAN_SHOTS_HINT),
        metric_tile("Kam konverguje čip", f"{czech_decimal(study.sampler.bunching)} ({_signed_percent(study.bias)})",
                    LIMIT_HINT),
    ]


def _first_shot_labels(study: SamplingStudy) -> List[str]:
    labels = []
    for index in study.shot_indices[:FIRST_SHOTS_SHOWN]:
        pattern = study.sampler.patterns[index]
        outputs = np.repeat(np.arange(1, len(pattern) + 1), pattern)
        labels.append(f"výstupy {', '.join(str(output) for output in outputs)} → Z = {study.sampler.multiplicities[index]:.0f}")
    return labels


def _samples_for_target(relative_variance: float) -> int:
    return int(np.ceil(relative_variance / TARGET_RELATIVE_ERROR**2))


def _with_error(value: float, error: float) -> str:
    return f"{czech_decimal(value)} ± {czech_decimal(error)}"


def czech_decimal(value: float) -> str:
    """Three significant digits, at least two decimals, with a decimal comma and spaces between thousands."""
    digits = max(2, 2 - int(np.floor(np.log10(abs(value))))) if value and np.isfinite(value) else 2
    return f"{value:,.{digits}f}".replace(",", " ").replace(".", ",")


def czech_count(value: int) -> str:
    return f"{value:,}".replace(",", " ")


def _signed_percent(share: float) -> str:
    percent = round(100 * share, 1)
    if percent == 0:
        return "0,0 %"
    return f"{percent:+.1f} %".replace(".", ",")
