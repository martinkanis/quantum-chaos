"""Lab run of the random matrix page: the spectrum of one simulated history and the risk of the portfolios."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import numpy as np

from randommatrix.cleaning import Estimator, estimate, sample_covariance
from randommatrix.factor_market import FactorMarket, FactorMarketError
from randommatrix.marchenko_pastur import NoiseBand, market_mode_noise_variance
from randommatrix.min_variance import RiskComparison, compare_risk

MAX_RATIO = 0.9
"""Closer to q = 1 the sample matrix is nearly singular and its portfolio meaningless."""
SWEEP_RATIOS: Tuple[float, ...] = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8)
SWEEP_REPETITIONS = 5


@dataclass(frozen=True)
class SpectrumStudy:
    eigenvalues: np.ndarray
    """Eigenvalues of the sample matrix, ascending."""
    band: NoiseBand
    """Noise band fitted from the data (σ² = 1 − λ_max / N)."""
    true_noise_variance: float

    @property
    def share_inside_band(self) -> float:
        return float(np.mean(self.eigenvalues <= self.band.upper))

    @property
    def count_above_band(self) -> int:
        return int(np.sum(self.eigenvalues > self.band.upper))


@dataclass(frozen=True)
class RatioSweep:
    """Average variance relative to the optimum for each q, one array per estimator."""

    ratios: np.ndarray
    out_of_sample: Dict[Estimator, np.ndarray]
    sample_in_sample: np.ndarray


@dataclass(frozen=True)
class RandomMatrixStudy:
    market: FactorMarket
    observation_count: int
    spectrum: SpectrumStudy
    risks: Dict[Estimator, RiskComparison]
    sweep: RatioSweep

    @property
    def ratio(self) -> float:
        return self.market.asset_count / self.observation_count


def run_study(market: FactorMarket, observation_count: int, seed: Optional[int]) -> RandomMatrixStudy:
    ratio = market.asset_count / observation_count
    if ratio >= MAX_RATIO:
        raise FactorMarketError(
            f"Na {market.asset_count} akcií je {observation_count} pozorování málo: q = N/T vychází "
            f"{_decimal(ratio)}, potřebuje být pod {_decimal(MAX_RATIO)}. Přidej pozorování nebo uber akcie."
        )
    rng = np.random.default_rng(seed)
    true = market.true_correlation()
    returns = market.simulate_returns(observation_count, rng)
    return RandomMatrixStudy(
        market=market,
        observation_count=observation_count,
        spectrum=_spectrum(returns, market),
        risks={estimator: compare_risk(estimate(estimator, returns), true) for estimator in Estimator},
        sweep=ratio_sweep(market, rng),
    )


def ratio_sweep(market: FactorMarket, rng: np.random.Generator) -> RatioSweep:
    true = market.true_correlation()
    out_of_sample = {estimator: np.zeros(len(SWEEP_RATIOS)) for estimator in Estimator}
    sample_in_sample = np.zeros(len(SWEEP_RATIOS))
    for index, ratio in enumerate(SWEEP_RATIOS):
        observation_count = round(market.asset_count / ratio)
        for _ in range(SWEEP_REPETITIONS):
            returns = market.simulate_returns(observation_count, rng)
            for estimator in Estimator:
                risk = compare_risk(estimate(estimator, returns), true)
                out_of_sample[estimator][index] += risk.out_of_sample / SWEEP_REPETITIONS
                if estimator is Estimator.SAMPLE:
                    sample_in_sample[index] += risk.in_sample / SWEEP_REPETITIONS
    return RatioSweep(np.array(SWEEP_RATIOS), out_of_sample, sample_in_sample)


def _spectrum(returns: np.ndarray, market: FactorMarket) -> SpectrumStudy:
    eigenvalues = np.linalg.eigvalsh(sample_covariance(returns))
    band = NoiseBand(market.asset_count / len(returns), market_mode_noise_variance(eigenvalues))
    return SpectrumStudy(eigenvalues, band, market.idiosyncratic_variance)


def _decimal(value: float) -> str:
    return f"{value:.2f}".replace(".", ",")
