"""Gaussian monomial expectation E[x^n], x ~ N(0, Σ): exact value and per-sample variance of plain Monte Carlo
and of the GBS-P estimator of Andersen & Shan."""

from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from math import exp, gcd, lgamma, log
from typing import Dict, List, Sequence, Tuple

import numpy as np

from gbs.gaussian_moments import moment_table, moment_table_size
from gbs.photon_tuning import DeviceEncoding, TuningMode, tune_encoding

MAX_VARIABLES = 6
MAX_DEGREE = 40
MAX_MOMENT_TABLE_SIZE = 2_000_000
"""Bound on Π(2·n_i + 1), the number of moments needed for the variance of x^n."""
SWEEP_MAX_DEGREE = 48
SYMMETRY_TOLERANCE = 1e-10
EIGENVALUE_TOLERANCE = 1e-10


class MonomialProblemError(ValueError):
    """Raised when a monomial expectation problem is invalid or too large for the exact computation."""


@dataclass(frozen=True)
class MonomialProblem:
    covariance: np.ndarray
    exponents: Tuple[int, ...]
    variable_names: Tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_dimensions(self.covariance, self.exponents, self.variable_names)
        _validate_exponents(self.exponents)
        _validate_covariance(self.covariance)
        _validate_used_variances(self.covariance, self.exponents, self.variable_names)
        _validate_known_sign(self.covariance, self.exponents)
        if moment_table_size([2 * power for power in self.exponents]) > MAX_MOMENT_TABLE_SIZE:
            raise MonomialProblemError(
                "Úloha je na přesný výpočet rozptylu příliš velká – sniž exponenty nebo počet proměnných."
            )

    @property
    def degree(self) -> int:
        return sum(self.exponents)

    def used_variables(self) -> MonomialProblem:
        """Variables with exponent 0 do not enter x^n; leaving them out saves modes and photons on the device."""
        used = [index for index, power in enumerate(self.exponents) if power > 0]
        return MonomialProblem(
            covariance=self.covariance[np.ix_(used, used)],
            exponents=tuple(self.exponents[index] for index in used),
            variable_names=tuple(self.variable_names[index] for index in used),
        )


@dataclass(frozen=True)
class VarianceComparison:
    exact: float
    """E[x^n]."""
    mc_relative_variance: float
    """var(x^n) / E[x^n]², the squared relative error of one Monte Carlo scenario."""
    pattern_probability: float
    """p(n): the share of GBS shots that show exactly the photon pattern n."""
    encoding: DeviceEncoding

    @property
    def gbs_relative_variance(self) -> float:
        """N × squared relative error of GBS-P for large N: the delta method halves the binomial error of p̂."""
        return (1 - self.pattern_probability) / (4 * self.pattern_probability)

    @property
    def advantage(self) -> float:
        """How many times fewer GBS shots than Monte Carlo scenarios reach the same precision."""
        return self.mc_relative_variance / self.gbs_relative_variance


@dataclass(frozen=True)
class DegreeSweep:
    """The same monomial direction at increasing degree, e.g. X₁X₂, X₁²X₂², X₁³X₂³, …"""

    degrees: np.ndarray
    mc_relative_variances: np.ndarray
    gbs_relative_variances: Dict[TuningMode, np.ndarray]


def required_samples(relative_variance: float, relative_error: float) -> float:
    """Samples for a relative error (one standard deviation) of the given size: N ≈ v / ε²."""
    return relative_variance / relative_error**2


def compare_variances(problem: MonomialProblem, mode: TuningMode) -> VarianceComparison:
    used = problem.used_variables()
    exponents = np.array(used.exponents)
    table = moment_table(used.covariance, 2 * exponents)
    exact = float(table[tuple(exponents)])
    if exact <= 0:
        raise MonomialProblemError(
            "Střední hodnota monomu vyšla nulová (třeba lichý exponent u proměnné, která s ostatními nekoreluje), "
            "takže relativní chybu nejde spočítat. Změň exponenty nebo korelace."
        )
    return _comparison(used.covariance, exponents, table, mode)


def degree_sweep(problem: MonomialProblem) -> DegreeSweep:
    used = problem.used_variables()
    base = np.array(used.exponents) // reduce(gcd, used.exponents)
    multiples = _sweep_multiples(base)
    table = moment_table(used.covariance, 2 * multiples[-1] * base)
    valid = [multiple for multiple in multiples if table[tuple(multiple * base)] > 0]
    comparisons = {
        mode: [_comparison(used.covariance, multiple * base, table, mode) for multiple in valid] for mode in TuningMode
    }
    # Monte Carlo does not depend on the tuning, so either list of comparisons gives its variances.
    mc_variances = [comparison.mc_relative_variance for comparison in comparisons[TuningMode.TOTAL]]
    return DegreeSweep(
        degrees=np.array([multiple * int(base.sum()) for multiple in valid]),
        mc_relative_variances=np.array(mc_variances),
        gbs_relative_variances={
            mode: np.array([comparison.gbs_relative_variance for comparison in mode_comparisons])
            for mode, mode_comparisons in comparisons.items()
        },
    )


def pattern_probability(encoding: DeviceEncoding, exponents: Sequence[int], moment: float) -> float:
    """p(n) = Haf(B_n)² / (n!·Π cosh r_j), where Haf(B_n) = Π d_i^{n_i}·E[x^n] because B = D·Σ·D."""
    log_hafnian = log(abs(moment)) + _log_scale_power(encoding, exponents)
    return exp(2 * log_hafnian - _log_pattern_factorial(exponents) - encoding.log_normalization)


def gbs_p_estimate(encoding: DeviceEncoding, exponents: Sequence[int], frequency: float) -> float:
    """Inverts pattern_probability for an observed frequency p̂; the sign of E[x^n] is known to be positive."""
    if frequency <= 0:
        return 0.0
    log_hafnian = 0.5 * (log(frequency) + _log_pattern_factorial(exponents) + encoding.log_normalization)
    return exp(log_hafnian - _log_scale_power(encoding, exponents))


def _comparison(
    covariance: np.ndarray, exponents: np.ndarray, table: np.ndarray, mode: TuningMode
) -> VarianceComparison:
    exact = float(table[tuple(exponents)])
    second_moment = float(table[tuple(2 * exponents)])
    encoding = tune_encoding(covariance, exponents, mode)
    return VarianceComparison(
        exact=exact,
        mc_relative_variance=max(0.0, second_moment / exact**2 - 1),
        pattern_probability=pattern_probability(encoding, exponents, exact),
        encoding=encoding,
    )


def _sweep_multiples(base: np.ndarray) -> List[int]:
    """Multiples with an even degree that stay within the degree and table-size limits."""
    multiples = []
    multiple = 1
    while multiple * base.sum() <= SWEEP_MAX_DEGREE and moment_table_size(2 * multiple * base) <= MAX_MOMENT_TABLE_SIZE:
        if multiple * base.sum() % 2 == 0:
            multiples.append(multiple)
        multiple += 1
    return multiples


def _log_scale_power(encoding: DeviceEncoding, exponents: Sequence[int]) -> float:
    return float(np.asarray(exponents) @ np.log(encoding.mode_scales))


def _log_pattern_factorial(exponents: Sequence[int]) -> float:
    return sum(lgamma(int(power) + 1) for power in exponents)


def _validate_dimensions(covariance: np.ndarray, exponents: Tuple[int, ...], names: Tuple[str, ...]) -> None:
    if not 1 <= len(exponents) <= MAX_VARIABLES:
        raise MonomialProblemError(f"Zadej 1 až {MAX_VARIABLES} proměnných.")
    if covariance.shape != (len(exponents), len(exponents)) or len(names) != len(exponents):
        raise MonomialProblemError("Matice musí mít tolik řádků a sloupců, kolik je proměnných.")


def _validate_exponents(exponents: Tuple[int, ...]) -> None:
    if any(not isinstance(power, int) or power < 0 for power in exponents):
        raise MonomialProblemError("Exponenty musí být nezáporná celá čísla.")
    degree = sum(exponents)
    if degree == 0:
        raise MonomialProblemError("Aspoň jeden exponent musí být kladný.")
    if degree % 2:
        raise MonomialProblemError(
            "Součet exponentů (stupeň monomu) musí být sudý: liché momenty normálního rozdělení jsou nulové."
        )
    if degree > MAX_DEGREE:
        raise MonomialProblemError(f"Stupeň monomu může být nejvýš {MAX_DEGREE}, zadaný má {degree}.")


def _validate_covariance(covariance: np.ndarray) -> None:
    if not np.all(np.isfinite(covariance)):
        raise MonomialProblemError("Všechny prvky matice musí být čísla.")
    if not np.allclose(covariance, covariance.T, atol=SYMMETRY_TOLERANCE):
        raise MonomialProblemError("Kovarianční matice musí být symetrická.")
    smallest = float(np.linalg.eigvalsh(covariance).min())
    if smallest < -EIGENVALUE_TOLERANCE * max(1.0, float(np.abs(covariance).max())):
        raise MonomialProblemError(
            f"Matice není kovarianční (pozitivně semidefinitní): nejmenší vlastní číslo vyšlo {smallest:.3g}. "
            "Zmenši korelace nebo zvětši rozptyly na diagonále."
        )


def _validate_used_variances(covariance: np.ndarray, exponents: Tuple[int, ...], names: Tuple[str, ...]) -> None:
    for index, power in enumerate(exponents):
        if power > 0 and covariance[index, index] <= 0:
            raise MonomialProblemError(
                f"Proměnná '{names[index]}' má nulový rozptyl, ale je v monomu – moment by byl nulový."
            )


def _validate_known_sign(covariance: np.ndarray, exponents: Tuple[int, ...]) -> None:
    """GBS measures Haf(B_n)², so the sign of the moment must be known in advance.

    With all exponents even, x^n is a square and its mean is positive. Otherwise non-negative entries guarantee
    a non-negative hafnian.
    """
    if all(power % 2 == 0 for power in exponents):
        return
    used = [index for index, power in enumerate(exponents) if power > 0]
    if np.any(covariance[np.ix_(used, used)] < 0):
        raise MonomialProblemError(
            "Při lichém exponentu musí být všechny prvky matice mezi použitými proměnnými nezáporné: GBS měří "
            "jen |Haf|², takže by nepoznal znaménko výsledku (znaménkový problém). Se sudými exponenty záporné "
            "korelace nevadí."
        )
