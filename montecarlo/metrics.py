from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Sequence

import numpy as np

from montecarlo.simulation import MONTHS_PER_YEAR, SimulationResult

CONFIDENCE_LEVEL = 0.95
BAND_PERCENTILES = (5, 25, 50, 75, 95)


@dataclass(frozen=True)
class SummaryMetrics:
    total_contributed: float
    mean: float
    median: float
    standard_deviation: float
    percentile_5: float
    percentile_95: float
    value_at_risk: float
    """Loss versus contributed capital not exceeded with CONFIDENCE_LEVEL probability."""
    conditional_value_at_risk: float
    """Average loss versus contributed capital in the worst (1 - CONFIDENCE_LEVEL) tail."""
    probability_of_loss: float
    median_annual_return: Optional[float]
    """Median CAGR; None when contributions make CAGR meaningless."""


def summarize(result: SimulationResult) -> SummaryMetrics:
    final_values = result.final_values
    losses = result.total_contributed - final_values
    value_at_risk = float(np.percentile(losses, CONFIDENCE_LEVEL * 100))
    tail_losses = losses[losses >= value_at_risk]

    return SummaryMetrics(
        total_contributed=result.total_contributed,
        mean=float(final_values.mean()),
        median=float(np.median(final_values)),
        standard_deviation=float(final_values.std()),
        percentile_5=float(np.percentile(final_values, 5)),
        percentile_95=float(np.percentile(final_values, 95)),
        value_at_risk=value_at_risk,
        conditional_value_at_risk=float(tail_losses.mean()),
        probability_of_loss=float((final_values < result.total_contributed).mean()),
        median_annual_return=_median_annual_return(result),
    )


def percentile_bands(
    result: SimulationResult, percentiles: Sequence[int] = BAND_PERCENTILES
) -> Dict[int, np.ndarray]:
    values = np.percentile(result.paths, percentiles, axis=0)
    return dict(zip(percentiles, values))


def _median_annual_return(result: SimulationResult) -> Optional[float]:
    initial_value = result.paths[0, 0]
    has_only_initial_investment = initial_value > 0 and result.total_contributed == initial_value
    if not has_only_initial_investment:
        return None
    years = (result.paths.shape[1] - 1) / MONTHS_PER_YEAR
    median_growth = np.median(result.final_values) / initial_value
    return float(median_growth ** (1 / years) - 1)
