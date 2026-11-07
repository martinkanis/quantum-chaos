"""Boson sampling on the photonic chip as a modified Monte Carlo of the bunching sum μ = Σ_S |Perm(U_{S,T})|².

n photons enter the first n waveguides (input T). A shot is the pattern S of photons counted at the outputs, drawn
with P(S) = |Perm(U_{S,T})|² / S!. The GBS-I estimator of Andersen & Shan with all a_S = 1 averages Z(S) = S!,
so it estimates μ = Σ_S |Perm(U_{S,T})|² = E[S!]: how much the photons bunch (μ = 1 if no two photons ever share an
output). The same μ is an expectation over complex Gaussian vectors (complex Wick theorem), which plain Monte Carlo
averages without any photons, only with a far larger variance.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import combinations_with_replacement
from math import comb, factorial

import numpy as np

from gbs.chip_programming import ChipTarget, build_setup, design_phases
from gbs.photonic_chip import ChipError, Chip, MeshPhases, transfer_matrix

MAX_PATTERNS = 200_000
"""Keeps the exact distribution of one callback within seconds and well inside the 256 MiB of the server."""
MAX_SHOTS = 100_000
PATTERN_CHUNK = 4096
DRAW_CHUNK = 8192
SHOT_STREAM = 2
GAUSSIAN_STREAM = 3
"""Random streams of one seed next to the target (0) and the fabrication errors (1) of gbs/chip_programming.py."""


class PhotonKind(str, Enum):
    INDISTINGUISHABLE = "nerozlisitelne"
    DISTINGUISHABLE = "rozlisitelne"


@dataclass(frozen=True)
class PatternDistribution:
    patterns: np.ndarray
    """One row per output pattern S: the number of photons counted at each output."""
    probabilities: np.ndarray
    multiplicities: np.ndarray
    """S! = Π s_i!, the value Z(S) of a shot with pattern S."""

    @property
    def bunching(self) -> float:
        """μ = E[S!] = Σ_S P(S)·S!."""
        return float(self.probabilities @ self.multiplicities)

    @property
    def relative_variance(self) -> float:
        """Variance of one shot value Z = S! divided by μ²."""
        return float(self.probabilities @ self.multiplicities**2) / self.bunching**2 - 1


def pattern_count(mode_count: int, photons: int) -> int:
    return comb(mode_count + photons - 1, photons)


def pattern_distribution(unitary: np.ndarray, photons: int, kind: PhotonKind) -> PatternDistribution:
    """Exact P(S) for photons in the first waveguides: |Perm(U_{S,T})|² / S!, or Perm(|U_{S,T}|²) / S! for
    distinguishable photons, which do not interfere."""
    _check_size(unitary.shape[0], photons)
    occupied = _occupied_outputs(unitary.shape[0], photons)
    columns = unitary[:, :photons]
    if kind == PhotonKind.DISTINGUISHABLE:
        weights = repeated_row_permanents(np.abs(columns) ** 2, occupied).real
    else:
        weights = np.abs(repeated_row_permanents(columns, occupied)) ** 2
    patterns = _patterns(occupied, unitary.shape[0])
    factorials = np.array([factorial(count) for count in range(photons + 1)], dtype=float)
    multiplicities = np.prod(factorials[patterns], axis=1)
    return PatternDistribution(patterns, weights / multiplicities, multiplicities)


def repeated_row_permanents(columns: np.ndarray, occupied: np.ndarray) -> np.ndarray:
    """Perm of the n × n matrix with rows `columns[o]` for o in each row of `occupied`, for all rows at once.

    Ryser: Perm(A) = (−1)^n Σ_Q (−1)^{|Q|} Π_rows Σ_{j∈Q} A_{row,j} over the column subsets Q. The row sums depend
    only on the output and Q, so all patterns share one table of them.
    """
    photons = columns.shape[1]
    subsets = (np.arange(1, 2**photons)[:, None] >> np.arange(photons)) & 1
    signs = (-1.0) ** (photons - subsets.sum(axis=1))
    row_sums = columns @ subsets.T
    permanents = np.empty(len(occupied), dtype=row_sums.dtype)
    for start in range(0, len(occupied), PATTERN_CHUNK):
        chunk = occupied[start:start + PATTERN_CHUNK]
        products = row_sums[chunk[:, 0]]
        for photon in range(1, photons):
            products = products * row_sums[chunk[:, photon]]
        permanents[start:start + len(chunk)] = products @ signs
    return permanents


def complete_homogeneous(values: np.ndarray, degree: int) -> np.ndarray:
    """h_n(x) = Σ_{|S| = n} Π_i x_i^{s_i} for each row of `values`, by h_k ← h_k + x_i·h_{k−1}."""
    polynomials = np.zeros((degree + 1, values.shape[0]), dtype=values.dtype)
    polynomials[0] = 1
    for variable in values.T:
        for power in range(1, degree + 1):
            polynomials[power] = polynomials[power] + variable * polynomials[power - 1]
    return polynomials[degree]


def gaussian_estimator_values(
    unitary: np.ndarray, photons: int, draws: int, rng: np.random.Generator,
) -> np.ndarray:
    """Plain Monte Carlo values with mean μ: Re[h_n(z ∘ z̄') · Π_{j<n} w̄_j w'_j], z, z' ~ CN(0, I), w = U†z.

    Complex Wick theorem: E[z^S w̄^T] = Perm(U_{S,T}), so two independent copies give |Perm(U_{S,T})|², and the
    sum over all patterns S is the complete homogeneous polynomial h_n (our derivation, checked by the tests).
    """
    _check_size(unitary.shape[0], photons)
    values = np.empty(draws)
    for start in range(0, draws, DRAW_CHUNK):
        count = min(DRAW_CHUNK, draws - start)
        first, second = _complex_gaussian(rng, count, unitary.shape[0]), _complex_gaussian(rng, count, unitary.shape[0])
        first_out, second_out = first @ unitary.conj(), second @ unitary.conj()
        inputs = np.prod(first_out[:, :photons].conj() * second_out[:, :photons], axis=1)
        values[start:start + count] = (complete_homogeneous(first * second.conj(), photons) * inputs).real
    return values


@dataclass(frozen=True)
class SamplingStudy:
    chip: Chip
    phases: MeshPhases
    photons: int
    target: PatternDistribution
    """Indistinguishable photons through the target matrix: the μ we want."""
    sampler: PatternDistribution
    """What the chip really samples: its own matrix, possibly distinguishable photons."""
    shot_indices: np.ndarray
    """Index of the pattern of each shot into sampler.patterns."""
    gaussian_values: np.ndarray

    @property
    def shot_values(self) -> np.ndarray:
        return self.sampler.multiplicities[self.shot_indices]

    @property
    def estimate(self) -> float:
        return float(self.shot_values.mean())

    @property
    def standard_error(self) -> float:
        return _standard_error(self.shot_values)

    @property
    def gaussian_estimate(self) -> float:
        return float(self.gaussian_values.mean())

    @property
    def gaussian_standard_error(self) -> float:
        return _standard_error(self.gaussian_values)

    @property
    def gaussian_relative_variance(self) -> float:
        """Estimated from the draws themselves; heavy tails make it rather an underestimate."""
        return float(self.gaussian_values.var(ddof=1)) / self.target.bunching**2

    @property
    def bias(self) -> float:
        """Relative error that no number of shots removes: where the chip converges against the target μ."""
        return self.sampler.bunching / self.target.bunching - 1


def run_sampling_study(
    target: ChipTarget, split_spread: float, seed: int, mode_count: int, photons: int, kind: PhotonKind, shots: int,
) -> SamplingStudy:
    """The chip programmed by the design phases samples `shots` patterns; the same number of Gaussian draws feed
    plain Monte Carlo of the target μ, which a classical computer can do without photons."""
    if not 1 <= shots <= MAX_SHOTS:
        raise ChipError(f"Počet výstřelů musí být mezi 1 a {MAX_SHOTS:,}.".replace(",", " "))
    _check_size(mode_count, photons)
    setup = build_setup(target, split_spread, seed, mode_count)
    phases = design_phases(setup)
    sampler = pattern_distribution(transfer_matrix(setup.chip, phases), photons, kind)
    shot_rng = np.random.default_rng([seed, SHOT_STREAM])
    return SamplingStudy(
        chip=setup.chip,
        phases=phases,
        photons=photons,
        target=pattern_distribution(setup.target, photons, PhotonKind.INDISTINGUISHABLE),
        sampler=sampler,
        shot_indices=shot_rng.choice(len(sampler.probabilities), size=shots, p=_normalised(sampler.probabilities)),
        gaussian_values=gaussian_estimator_values(
            setup.target, photons, shots, np.random.default_rng([seed, GAUSSIAN_STREAM]),
        ),
    )


def running_means(values: np.ndarray, checkpoints: np.ndarray) -> np.ndarray:
    """Mean of the first k values for each k in checkpoints."""
    return np.cumsum(values)[checkpoints - 1] / checkpoints


def _check_size(mode_count: int, photons: int) -> None:
    if not 1 <= photons <= mode_count:
        raise ChipError(f"Počet fotonů musí být mezi 1 a počtem světlovodů ({mode_count}).")
    count = pattern_count(mode_count, photons)
    if count > MAX_PATTERNS:
        raise ChipError(
            f"{photons} fotonů v {mode_count} světlovodech má {count:,} výstupních vzorů, simulátor jich přesně "
            f"spočítá nejvýš {MAX_PATTERNS:,}. Uber foton nebo světlovody.".replace(",", " ")
        )


def _occupied_outputs(mode_count: int, photons: int) -> np.ndarray:
    """Each pattern as the sorted outputs of its photons, e.g. (0, 0, 3) for two photons in output 1, one in 4."""
    return np.array(list(combinations_with_replacement(range(mode_count), photons)), dtype=np.intp)


def _patterns(occupied: np.ndarray, mode_count: int) -> np.ndarray:
    patterns = np.zeros((len(occupied), mode_count), dtype=np.intp)
    np.add.at(patterns, (np.arange(len(occupied))[:, None], occupied), 1)
    return patterns


def _complex_gaussian(rng: np.random.Generator, count: int, mode_count: int) -> np.ndarray:
    """CN(0, I): E[z z†] = I, E[z zᵀ] = 0."""
    return (rng.normal(size=(count, mode_count)) + 1j * rng.normal(size=(count, mode_count))) / np.sqrt(2)


def _standard_error(values: np.ndarray) -> float:
    if len(values) < 2:
        return float("nan")
    return float(values.std(ddof=1) / np.sqrt(len(values)))


def _normalised(probabilities: np.ndarray) -> np.ndarray:
    return probabilities / probabilities.sum()
