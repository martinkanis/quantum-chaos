"""Uniform photon loss in Gaussian boson sampling: the output of the ideal device thinned photon by photon.

The same transmission η on every mode commutes with the interferometer, so a lossy device behaves like the ideal
sampler followed by a coin for each photon, which reaches its detector with probability η. Every lossy quantity is
therefore a sum over the ideal patterns k, each weighted by a product of one factor per mode. The ideal probabilities
come from the Gaussian moment table instead of hafnians, p(k) = (Π_i d_i^{k_i}·E[x^k])² / (k!·Π_j cosh r_j), because
the device carries B = D·Σ·D (gbs/monomial_problem.py). Only patterns with at most |n| + E photons enter, n being the
target pattern and E the extra photons; what the cut leaves out is bounded by the ideal probability of more than
|n| + E photons, which needs no hafnians either. The tests check the thinning against the hafnian formula for the
mixed Gaussian state of the lossy device.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Tuple

import numpy as np

from gbs.gaussian_moments import moment_table, moment_table_size
from gbs.photon_tuning import DeviceEncoding
from gbs.sampler import total_photons_from_squeezing

MAX_TABLE_SIZE = 1_500_000
"""Bound on the moment table Π(n_i + E + 1): this many entries take well under a second and about 100 MiB."""
MIN_EXTRA_PHOTONS = 8
MAX_EXTRA_PHOTONS = 60
CONVERGED_TAIL_SHARE = 0.01
"""The estimated tail of the second-moment sum must stay below this share of the kept sum."""


class PhotonLossError(ValueError):
    """Raised when the transmission is out of range or the problem is too large for the lossy computation."""


@dataclass(frozen=True)
class IdealPatterns:
    """Every ideal output pattern with at most degree + extra_photons photons, with its probability."""

    exponents: np.ndarray
    """Target pattern n; the extra photons are counted above its degree |n|."""
    patterns: np.ndarray
    """One row per pattern k from the box 0 ≤ k_i ≤ n_i + E, in the order of the moment table."""
    probabilities: np.ndarray
    extra_photons: int
    tail_probability: float
    """Ideal P(total > |n| + E): an upper bound on what any sum over the kept patterns leaves out."""

    @property
    def degree(self) -> int:
        return int(self.exponents.sum())

    @property
    def max_total(self) -> int:
        return self.degree + self.extra_photons

    @property
    def totals(self) -> np.ndarray:
        return self.patterns.sum(axis=1)


@dataclass(frozen=True)
class LossyTarget:
    """The target pattern as the lossy device shows it."""

    transmission: float
    probability: float
    """p_η(n): the kept patterns plus a geometric estimate of the tail where the shells of the sum shrink."""
    probability_tail_share: float
    """Estimated tail over the kept sum of p_η(n); infinite when the shells do not shrink and the kept sum is only
    a lower bound (the ideal tail probability of the patterns bounds the rest)."""
    correction_second_moment: float
    """E[Z²] of one corrected shot: the kept patterns plus a geometric estimate of the tail."""
    correction_tail_share: float
    """Estimated tail over the kept sum; infinite when the shells of the sum do not shrink."""

    @property
    def probability_reliable(self) -> bool:
        return self.probability_tail_share < CONVERGED_TAIL_SHARE

    @property
    def correction_converged(self) -> bool:
        return bool(np.isfinite(self.correction_second_moment)) and self.correction_tail_share < CONVERGED_TAIL_SHARE

    def correction_relative_variance(self, ideal_probability: float) -> float:
        """Var Z / (4p²): per-shot relative variance of the corrected GBS-P estimate by the delta method, the same
        (1 − p)/(4p) as for the ideal device when η = 1."""
        return (self.correction_second_moment - ideal_probability**2) / (4 * ideal_probability**2)


def extra_photons_within_limit(exponents: Sequence[int]) -> int:
    """The most extra photons whose moment table fits the size limit; even, so that the last kept total has photons."""
    for extra in range(MAX_EXTRA_PHOTONS, MIN_EXTRA_PHOTONS - 1, -2):
        if moment_table_size([int(power) + extra for power in exponents]) <= MAX_TABLE_SIZE:
            return extra
    raise PhotonLossError(
        "Úloha je na výpočet se ztrátami fotonů příliš velká – sniž exponenty nebo počet proměnných."
    )


def ideal_patterns(
    covariance: np.ndarray, encoding: DeviceEncoding, exponents: Sequence[int], extra_photons: int
) -> IdealPatterns:
    target = np.asarray(exponents, dtype=int)
    bounds = target + extra_photons
    if moment_table_size(bounds) > MAX_TABLE_SIZE:
        raise PhotonLossError(
            f"Tabulka vzorů s {extra_photons} fotony navíc má {moment_table_size(bounds):,} položek, nejvýš jich "
            f"může mít {MAX_TABLE_SIZE:,}.".replace(",", " ")
        )
    patterns = np.indices(bounds + 1).reshape(len(target), -1).T
    moments = moment_table(covariance, bounds).reshape(-1)
    kept = patterns.sum(axis=1) <= target.sum() + extra_photons
    return IdealPatterns(
        exponents=target,
        patterns=patterns[kept],
        probabilities=_pattern_probabilities(encoding, patterns[kept], moments[kept]),
        extra_photons=extra_photons,
        tail_probability=_tail_probability(encoding.squeezing, int(target.sum()) + extra_photons),
    )


def lossy_target(ideal: IdealPatterns, transmission: float) -> LossyTarget:
    """The target pattern seen through loss η, and the second moment of the shot values that undo the loss."""
    _validate_transmission(transmission)
    max_count = int(ideal.patterns.max())
    survival = np.ones(len(ideal.patterns))
    second_moments = np.ones(len(ideal.patterns))
    for mode, target in enumerate(ideal.exponents):
        counts = ideal.patterns[:, mode]
        survival *= survival_weights(int(target), transmission, max_count)[counts]
        second_moments *= correction_second_moments(int(target), transmission, max_count)[counts]
    kept_probability, probability_tail, probability_tail_share = _summed_with_tail(ideal, ideal.probabilities * survival)
    kept_second_moment, second_moment_tail, second_moment_tail_share = _summed_with_tail(
        ideal, ideal.probabilities * second_moments
    )
    return LossyTarget(
        transmission=transmission,
        probability=kept_probability + (probability_tail if np.isfinite(probability_tail) else 0.0),
        probability_tail_share=probability_tail_share,
        correction_second_moment=kept_second_moment + second_moment_tail,
        correction_tail_share=second_moment_tail_share,
    )


def click_probability(ideal: IdealPatterns, transmission: float) -> float:
    """How often threshold detectors show the support of the target: a click exactly in the modes with n_i > 0."""
    _validate_transmission(transmission)
    silence = (1 - transmission) ** ideal.patterns
    clicked = ideal.exponents > 0
    weights = np.where(clicked[None, :], 1 - silence, silence).prod(axis=1)
    return float(ideal.probabilities @ weights)


def critical_transmission(encoding: DeviceEncoding) -> float:
    """Below it the variance of the corrected estimate is infinite: the ideal probability of t photons falls like
    (tanh r_max)^t while the corrected shot values grow like ((1 − η)/η)^t, so their product converges only when
    tanh r_max·(1 − η)/η < 1 (our derivation; the tests check it against the shells of the sum)."""
    strongest = float(encoding.tanh_squeezing.max())
    return strongest / (1 + strongest)


def survival_weights(target: int, transmission: float, max_count: int) -> np.ndarray:
    """P(exactly `target` of k photons reach the detector) for k = 0..max_count: C(k, n)·η^n·(1 − η)^(k−n)."""
    counts = np.arange(max_count + 1)
    log_factorials = _log_factorials(max_count)
    excess = np.clip(counts - target, 0, None)
    with np.errstate(divide="ignore", invalid="ignore"):
        log_choose = log_factorials[counts] - log_factorials[target] - log_factorials[excess]
        weights = np.exp(log_choose + target * np.log(transmission) + _log_power(np.log1p(-transmission), excess))
    return np.where(counts >= target, weights, 0.0)


def correction_values(target: int, transmission: float, max_count: int) -> np.ndarray:
    """Z(m) for m = 0..max_count detected photons: C(m, n)·η^(−n)·(1 − 1/η)^(m−n) for m ≥ n, otherwise 0.

    It undoes the thinning, Σ_m Bin(k, m; η)·Z(m) = [k = n], so averaging Z over the shots estimates the ideal p(n)
    without bias (the inverse binomial transformation of Kiss, Herzog & Leonhardt 1995).
    """
    counts = np.arange(max_count + 1)
    signs = np.where((counts - target) % 2 == 0, 1.0, -1.0)
    with np.errstate(over="ignore"):
        magnitudes = np.exp(_log_correction_magnitudes(target, transmission, max_count))
    return signs * magnitudes


def correction_second_moments(target: int, transmission: float, max_count: int) -> np.ndarray:
    """E[Z(m)²] for m ~ Bin(k, η) and k = 0..max_count: what one shot adds to the variance of the corrected estimate
    when the ideal device would have sent k photons into the mode."""
    log_terms = _log_binomial_matrix(transmission, max_count) + 2 * _log_correction_magnitudes(
        target, transmission, max_count
    )[None, :]
    peaks = log_terms.max(axis=1)
    with np.errstate(invalid="ignore", over="ignore"):
        scaled_sums = np.exp(log_terms - peaks[:, None]).sum(axis=1)
        return np.where(np.isfinite(peaks), np.exp(peaks) * scaled_sums, 0.0)


def _pattern_probabilities(encoding: DeviceEncoding, patterns: np.ndarray, moments: np.ndarray) -> np.ndarray:
    """p(k) = (Π_i d_i^{k_i}·E[x^k])² / (k!·Π_j cosh r_j) in logarithms; a zero moment gives probability zero."""
    log_factorials = _log_factorials(int(patterns.max()))
    with np.errstate(divide="ignore"):
        log_hafnian = patterns @ np.log(encoding.mode_scales) + np.log(np.abs(moments))
    return np.exp(2 * log_hafnian - log_factorials[patterns].sum(axis=1) - encoding.log_normalization)


def _tail_probability(squeezing: np.ndarray, max_total: int) -> float:
    return max(0.0, 1.0 - float(total_photons_from_squeezing(squeezing, max_total).sum()))


def _summed_with_tail(ideal: IdealPatterns, terms: np.ndarray) -> Tuple[float, float, float]:
    """Sum of the terms over the kept patterns, the geometric estimate of the rest and its share of the kept sum.

    The shells are the totals of the patterns from the degree up; the odd totals in between carry no probability.
    """
    shells = np.bincount(ideal.totals, weights=terms, minlength=ideal.max_total + 1)[ideal.degree::2]
    tail, tail_share = _geometric_tail(shells)
    return float(shells.sum()), tail, tail_share


def _geometric_tail(shells: np.ndarray) -> Tuple[float, float]:
    """Estimated sum beyond the last shell and its share of the kept sum, if the shells keep shrinking by the ratio
    of the last two: tail = last·ρ/(1 − ρ). Infinite when they do not shrink."""
    kept = float(shells.sum())
    if len(shells) < 2 or shells[-1] == 0:
        return 0.0, 0.0
    if not np.isfinite(kept) or shells[-2] <= 0 or shells[-1] >= shells[-2]:
        return np.inf, np.inf
    ratio = float(shells[-1] / shells[-2])
    tail = float(shells[-1]) * ratio / (1 - ratio)
    return tail, tail / kept


def _log_binomial_matrix(transmission: float, max_count: int) -> np.ndarray:
    """log Bin(k, m; η) with k along the rows and m along the columns; −∞ where m > k."""
    counts = np.arange(max_count + 1)
    sent, detected = counts[:, None], counts[None, :]
    log_factorials = _log_factorials(max_count)
    lost = np.clip(sent - detected, 0, None)
    with np.errstate(divide="ignore", invalid="ignore"):
        log_choose = log_factorials[sent] - log_factorials[detected] - log_factorials[lost]
        values = log_choose + detected * np.log(transmission) + _log_power(np.log1p(-transmission), lost)
    return np.where(detected <= sent, values, -np.inf)


def _log_correction_magnitudes(target: int, transmission: float, max_count: int) -> np.ndarray:
    """log |Z(m)| for m = 0..max_count; −∞ below the target."""
    counts = np.arange(max_count + 1)
    log_factorials = _log_factorials(max_count)
    excess = np.clip(counts - target, 0, None)
    with np.errstate(divide="ignore", invalid="ignore"):
        log_choose = log_factorials[counts] - log_factorials[target] - log_factorials[excess]
        log_ratio = np.log1p(-transmission) - np.log(transmission)
        values = log_choose - target * np.log(transmission) + _log_power(log_ratio, excess)
    return np.where(counts >= target, values, -np.inf)


def _log_power(log_base: float, exponents: np.ndarray) -> np.ndarray:
    """exponents·log_base with 0·(−∞) = 0, so that (1 − η)^0 = 1 also for η = 1."""
    return np.where(exponents == 0, 0.0, exponents * log_base)


def _log_factorials(count: int) -> np.ndarray:
    """log k! for k = 0..count."""
    return np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, count + 1)))])


def _validate_transmission(transmission: float) -> None:
    if not 0 < transmission <= 1:
        raise PhotonLossError("Propustnost musí být mezi 0 a 1: k detektorům musí dorazit víc než 0 % fotonů.")
