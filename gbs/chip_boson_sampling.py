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
from math import comb

import numpy as np

from gbs.chip_programming import ChipTarget, build_setup, design_phases
from gbs.photonic_chip import ChipError, Chip, MeshPhases, transfer_matrix

MAX_PATTERNS = 1_000_000
"""Keeps the exact distribution of one callback within seconds and well inside the memory of the server."""
MAX_SHOTS = 100_000
PERMANENT_CHUNK_ELEMENTS = 1 << 20
"""Prefix products and partial sums of one chunk of patterns: 2²⁰ complex numbers = 16 MiB, whatever the task."""
DRAW_CHUNK = 8192
SHOT_STREAM = 2
GAUSSIAN_STREAM = 3
"""Random streams of one seed next to the target (0) and the fabrication errors (1) of gbs/chip_programming.py."""


class PhotonKind(str, Enum):
    INDISTINGUISHABLE = "nerozlisitelne"
    DISTINGUISHABLE = "rozlisitelne"


@dataclass(frozen=True)
class PatternDistribution:
    occupied_outputs: np.ndarray
    """One row per output pattern S: the outputs of its photons in ascending order, e.g. (0, 0, 3) for two photons
    in output 1 and one in output 4. The rows are in lexicographic order, like combinations_with_replacement."""
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

    @property
    def collision_free_share(self) -> float:
        """Probability that no two photons share an output, P(Z = 1)."""
        return float(self.probabilities[self.multiplicities == 1].sum())


def pattern_count(mode_count: int, photons: int) -> int:
    return comb(mode_count + photons - 1, photons)


def pattern_distribution(unitary: np.ndarray, photons: int, kind: PhotonKind) -> PatternDistribution:
    """Exact P(S) for photons in the first waveguides: |Perm(U_{S,T})|² / S!, or Perm(|U_{S,T}|²) / S! for
    distinguishable photons, which do not interfere."""
    mode_count = unitary.shape[0]
    _check_size(mode_count, photons)
    columns = unitary[:, :photons]
    if kind == PhotonKind.DISTINGUISHABLE:
        weights = all_pattern_permanents(np.abs(columns) ** 2).real
    else:
        weights = np.abs(all_pattern_permanents(columns)) ** 2
    occupied = occupied_outputs(mode_count, photons)
    multiplicities = _multiplicities(occupied)
    return PatternDistribution(occupied, weights / multiplicities, multiplicities)


def all_pattern_permanents(columns: np.ndarray) -> np.ndarray:
    """Perm(U_{S,T}) for every output pattern S in the order of occupied_outputs, from the m × n matrix U_{:,T}.

    Glynn: Perm(A) = 2^{1−n} Σ_δ (Π_j δ_j) Π_rows Σ_j δ_j A_{row,j} over δ ∈ {±1}ⁿ with δ₁ = 1. The row sums depend
    only on the output and δ, so all patterns share one table of them. Patterns that share their first n − 1
    photons differ only in the factor of the last one, so one matrix product sums over δ for all of them at once.
    """
    mode_count, photons = columns.shape
    signs = _glynn_signs(photons)
    row_sums = columns @ signs.T
    last_factors = (row_sums * (np.prod(signs, axis=1) / len(signs))).T
    prefixes = occupied_outputs(mode_count, photons - 1)
    permanents = np.empty(pattern_count(mode_count, photons), dtype=row_sums.dtype)
    chunk_size = max(1, PERMANENT_CHUNK_ELEMENTS // (len(signs) + mode_count))
    written = 0
    for start in range(0, len(prefixes), chunk_size):
        chunk = prefixes[start:start + chunk_size]
        sums = _prefix_products(row_sums, chunk) @ last_factors
        values = sums[np.arange(mode_count) >= _first_free_output(chunk)[:, None]]
        permanents[written:written + len(values)] = values
        written += len(values)
    return permanents


def occupied_outputs(mode_count: int, photons: int) -> np.ndarray:
    """Every output pattern as the sorted outputs of its photons, in lexicographic order (see PatternDistribution).

    Zero photons give the one empty pattern, the prefix all patterns of one photon start from. The smallest integer
    type that holds the outputs keeps a million patterns in a few MiB (one byte per photon up to 255 waveguides).
    """
    occupied = np.zeros((1, 0), dtype=np.min_scalar_type(mode_count))
    for _ in range(photons):
        occupied = _append_photon(occupied, mode_count)
    return occupied


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
    """Index of the pattern of each shot into the rows of sampler.occupied_outputs."""
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
    def crowding(self) -> float:
        """n²/m: about the expected number of photon pairs sharing an output, since in a Haar-random interferometer
        a pair of indistinguishable photons ends up together with probability 2/(m + 1)."""
        return self.photons**2 / self.chip.mode_count

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
        raise ChipError(f"Počet výstřelů musí být mezi 1 a {_spaced(MAX_SHOTS)}.")
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
            f"{photons} fotonů v {mode_count} světlovodech má {_spaced(count)} výstupních vzorů, simulátor jich "
            f"přesně spočítá nejvýš {_spaced(MAX_PATTERNS)}. Uber foton nebo světlovody."
        )


def _spaced(count: int) -> str:
    """Czech thousands separator; replacing commas in the whole message would also drop its punctuation."""
    return f"{count:,}".replace(",", " ")


def _append_photon(occupied: np.ndarray, mode_count: int) -> np.ndarray:
    """Each row extended by every output from its last one on, which keeps the rows sorted and in lexicographic
    order."""
    first_free = _first_free_output(occupied)
    repeats = mode_count - first_free
    starts = np.repeat(np.cumsum(repeats) - repeats, repeats)
    last = np.repeat(first_free, repeats) + np.arange(len(starts)) - starts
    return np.column_stack([np.repeat(occupied, repeats, axis=0), last.astype(occupied.dtype)])


def _first_free_output(occupied: np.ndarray) -> np.ndarray:
    """The lowest output the next photon of each row may take without breaking the ascending order."""
    if occupied.shape[1] == 0:
        return np.zeros(len(occupied), dtype=np.intp)
    return occupied[:, -1].astype(np.intp)


def _glynn_signs(photons: int) -> np.ndarray:
    """All δ ∈ {±1}ⁿ with δ₁ = +1, one per row."""
    bits = (np.arange(2 ** (photons - 1))[:, None] >> np.arange(photons - 1)) & 1
    return np.column_stack([np.ones(len(bits)), 1.0 - 2 * bits])


def _prefix_products(row_sums: np.ndarray, prefixes: np.ndarray) -> np.ndarray:
    """Π over the photons of each prefix of their row sums, one column per δ."""
    products = np.ones((len(prefixes), row_sums.shape[1]), dtype=row_sums.dtype)
    for photon in range(prefixes.shape[1]):
        products *= row_sums[prefixes[:, photon]]
    return products


def _multiplicities(occupied: np.ndarray) -> np.ndarray:
    """S! = Π_i s_i!: within a run of photons in one output the k-th photon contributes the factor k."""
    multiplicities = np.ones(len(occupied))
    run = np.ones(len(occupied))
    for photon in range(1, occupied.shape[1]):
        run = np.where(occupied[:, photon] == occupied[:, photon - 1], run + 1, 1.0)
        multiplicities *= run
    return multiplicities


def _complex_gaussian(rng: np.random.Generator, count: int, mode_count: int) -> np.ndarray:
    """CN(0, I): E[z z†] = I, E[z zᵀ] = 0."""
    return (rng.normal(size=(count, mode_count)) + 1j * rng.normal(size=(count, mode_count))) / np.sqrt(2)


def _standard_error(values: np.ndarray) -> float:
    if len(values) < 2:
        return float("nan")
    return float(values.std(ddof=1) / np.sqrt(len(values)))


def _normalised(probabilities: np.ndarray) -> np.ndarray:
    return probabilities / probabilities.sum()
