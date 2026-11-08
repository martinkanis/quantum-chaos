"""The GBS-P estimate of a Gaussian monomial on a lossy device: the bias of the plain estimate, the price of the
unbiased correction, threshold detectors and the known boundaries, all against plain Monte Carlo."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, sqrt
from typing import Sequence, Tuple

from gbs.monomial_problem import MonomialProblem, VarianceComparison, compare_variances, gbs_p_estimate
from gbs.photon_loss import (
    IdealPatterns,
    click_probability,
    critical_transmission,
    extra_photons_within_limit,
    ideal_patterns,
    lossy_target,
)
from gbs.photon_tuning import DeviceEncoding, TuningMode

TRANSMISSIONS: Tuple[float, ...] = (
    1.0, 0.99, 0.975, 0.95, 0.925, 0.9, 0.875, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.3, 0.2, 0.1,
)
"""Transmissions of the sweep, dense near the lossless device where the estimate changes fastest."""
SIMULATION_ERROR = 0.01
"""ε of Qi et al. (2020): total-variation distance between the classical samples and the lossy device."""
SQUEEZING_TOLERANCE = 1e-9


@dataclass(frozen=True)
class LossPoint:
    """The estimate at one transmission."""

    transmission: float
    lossy_probability: float
    """p_η(n): how often the lossy device shows exactly the target pattern."""
    probability_reliable: bool
    """False when the kept patterns do not reach far enough for p_η(n), which is then only a lower bound."""
    probability_tail_share: float
    """Estimated part of p_η(n) beyond the kept patterns, relative to the kept sum; infinite when unknown."""
    naive_estimate: float
    """GBS-P estimate from p_η(n) as if the device were ideal."""
    naive_bias: float
    """Relative error of the naive estimate, which no number of shots removes."""
    threshold_estimate: float
    """The same estimate from how often threshold detectors click exactly in the modes of the target."""
    threshold_bias: float
    corrected_relative_variance: float
    """Per-shot relative variance of the unbiased correction; partial when the correction has not converged."""
    correction_converged: bool
    correction_tail_share: float


@dataclass(frozen=True)
class LossStudy:
    problem: MonomialProblem
    """The variables that enter the monomial."""
    mode: TuningMode
    comparison: VarianceComparison
    """The ideal device: exact value, pattern probability, Monte Carlo variance and the encoding."""
    chosen: LossPoint
    sweep: Tuple[LossPoint, ...]
    extra_photons: int
    tail_probability: float
    """Ideal probability of more photons than the sums keep; bounds what the lossy probabilities leave out."""
    critical_transmission: float
    """Below it the variance of the corrected estimate is infinite (our derivation)."""
    simulable_transmission: float
    """Below it Qi et al. (2020) simulate the lossy device classically within SIMULATION_ERROR."""

    @property
    def exponents(self) -> Tuple[int, ...]:
        return self.problem.exponents

    @property
    def resolvable_by_threshold_detectors(self) -> bool:
        """Threshold detectors tell the target apart only when no mode should hold two or more photons."""
        return all(power <= 1 for power in self.exponents)

    def advantage(self, point: LossPoint) -> float:
        """How many times fewer corrected GBS shots than Monte Carlo scenarios reach the same precision."""
        return self.comparison.mc_relative_variance / point.corrected_relative_variance


def run_loss_study(problem: MonomialProblem, mode: TuningMode, transmission: float) -> LossStudy:
    used = problem.used_variables()
    comparison = compare_variances(used, mode)
    extra_photons = extra_photons_within_limit(used.exponents)
    ideal = ideal_patterns(used.covariance, comparison.encoding, used.exponents, extra_photons)
    return LossStudy(
        problem=used,
        mode=mode,
        comparison=comparison,
        chosen=loss_point(ideal, comparison, used.exponents, transmission),
        sweep=tuple(loss_point(ideal, comparison, used.exponents, value) for value in TRANSMISSIONS),
        extra_photons=extra_photons,
        tail_probability=ideal.tail_probability,
        critical_transmission=critical_transmission(comparison.encoding),
        simulable_transmission=simulable_transmission(comparison.encoding),
    )


def loss_point(
    ideal: IdealPatterns, comparison: VarianceComparison, exponents: Sequence[int], transmission: float
) -> LossPoint:
    target = lossy_target(ideal, transmission)
    naive_estimate = gbs_p_estimate(comparison.encoding, exponents, target.probability)
    threshold_estimate = gbs_p_estimate(comparison.encoding, exponents, click_probability(ideal, transmission))
    return LossPoint(
        transmission=transmission,
        lossy_probability=target.probability,
        probability_reliable=target.probability_reliable,
        probability_tail_share=target.probability_tail_share,
        naive_estimate=naive_estimate,
        naive_bias=naive_estimate / comparison.exact - 1,
        threshold_estimate=threshold_estimate,
        threshold_bias=threshold_estimate / comparison.exact - 1,
        corrected_relative_variance=target.correction_relative_variance(comparison.pattern_probability),
        correction_converged=target.correction_converged,
        correction_tail_share=target.correction_tail_share,
    )


def simulable_transmission(encoding: DeviceEncoding, error: float = SIMULATION_ERROR) -> float:
    """Transmission below which Qi et al. (2020) simulate the lossy device classically within error ε.

    For ideal detectors their inequality (1) reads sech[½·ln(1/V)] > exp(−ε²/(4K)), with V = η·e^(−2r) + 1 − η the
    variance of the squeezed quadrature after loss (vacuum 1) and K the number of squeezers. The left side equals
    2√V/(1 + V) and grows with V, so the condition is V > V* and η < (1 − V*)/(1 − e^(−2r)); the most squeezed
    mode decides, because its V is the smallest.
    """
    squeezing = encoding.squeezing
    squeezed = squeezing > SQUEEZING_TOLERANCE
    if not squeezed.any():
        return 1.0
    threshold = exp(-(error**2) / (4 * int(squeezed.sum())))
    variance_limit = ((1 - sqrt(1 - threshold**2)) / threshold) ** 2
    return min(1.0, (1 - variance_limit) / (1 - exp(-2 * float(squeezing.max()))))
