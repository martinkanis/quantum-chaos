"""Programmable photonic chip: waveguides joined by a rectangular (Clements) mesh of Mach–Zehnder interferometers.

Each MZI is two directional couplers with the phase shifter θ between them and the phase shifter φ on the upper
input: T = B(α₂)·P(θ)·B(α₁)·P(φ), where the coupler B(α) sends the share sin²α of the light into the other
waveguide and P(x) = diag(e^{ix}, 1). An ideal coupler splits 50:50 (α = π/4), a fabricated one is a little off.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import List, Sequence, Tuple

import numpy as np

MODE_COUNT = 4
IDEAL_SPLIT_RATIO = 0.5
IDEAL_SPLIT_ANGLE = np.pi / 4
MAX_SPLIT_SPREAD = 0.2
MIN_SPLIT_RATIO = 0.05
MAX_SPLIT_RATIO = 0.95
"""A fabricated coupler stays a coupler: it never sends (almost) all the light one way."""


class ChipError(ValueError):
    """Raised when the chip, its phases or the laser input are invalid."""


@dataclass(frozen=True)
class MziSlot:
    column: int
    upper_mode: int

    @property
    def lower_mode(self) -> int:
        return self.upper_mode + 1


@lru_cache(maxsize=None)
def mesh_slots(mode_count: int) -> Tuple[MziSlot, ...]:
    """Column c joins the neighbouring waveguides from c mod 2 on; N columns hold all N(N − 1)/2 MZIs.

    Cached: drawing and simulating a chip ask for the slots once per MZI, which costs O(N⁴) for large chips.
    """
    return tuple(
        MziSlot(column, upper_mode)
        for column in range(mode_count)
        for upper_mode in range(column % 2, mode_count - 1, 2)
    )


def mzi_count(mode_count: int) -> int:
    return mode_count * (mode_count - 1) // 2


ESTIMATED_COLUMN_LENGTH_CM = 0.1
"""Our order-of-magnitude estimate of how long one column of MZIs is: about a millimetre."""
ESTIMATED_COLUMN_TRANSIT_SECONDS = 1e-11
"""Our order-of-magnitude estimate: light in a waveguide is two to four times slower than in vacuum, so it crosses
a column about a millimetre long in about 10 ps."""


def estimated_transit_seconds(mode_count: int) -> float:
    """How long real light takes through the mesh, which has as many columns as waveguides (our estimate)."""
    return mode_count * ESTIMATED_COLUMN_TRANSIT_SECONDS


@dataclass(frozen=True)
class MeshPhases:
    internal: Tuple[float, ...]
    """θ of each MZI in the order of mesh_slots: how the light splits between its two outputs."""
    external: Tuple[float, ...]
    """φ of each MZI: phase of its upper input relative to the lower one."""

    def __post_init__(self) -> None:
        if len(self.internal) != len(self.external):
            raise ChipError(
                f"Každý interferometr potřebuje obě fáze, zadáno je {len(self.internal)} θ a {len(self.external)} φ."
            )
        if not np.all(np.isfinite(self.internal + self.external)):
            raise ChipError("Fáze musí být konečná čísla v radiánech.")


def zero_phases(mode_count: int = MODE_COUNT) -> MeshPhases:
    zeros = (0.0,) * mzi_count(mode_count)
    return MeshPhases(zeros, zeros)


def random_phases(mode_count: int, rng: np.random.Generator) -> MeshPhases:
    """Every θ and φ uniform in [0, 2π): a chip that does something arbitrary."""
    count = mzi_count(mode_count)
    return MeshPhases(
        tuple(float(phase) for phase in rng.uniform(0, 2 * np.pi, count)),
        tuple(float(phase) for phase in rng.uniform(0, 2 * np.pi, count)),
    )


@dataclass(frozen=True)
class Chip:
    mode_count: int
    split_angles: Tuple[Tuple[float, float], ...]
    """Angles α₁, α₂ of the two couplers of each MZI in the order of mesh_slots."""

    def __post_init__(self) -> None:
        if self.mode_count < 2:
            raise ChipError("Čip potřebuje aspoň dva světlovody.")
        if len(self.split_angles) != mzi_count(self.mode_count):
            raise ChipError(
                f"Čip se {self.mode_count} světlovody má {mzi_count(self.mode_count)} interferometrů, "
                f"zadáno je {len(self.split_angles)}."
            )

    @property
    def slots(self) -> Tuple[MziSlot, ...]:
        return mesh_slots(self.mode_count)


def ideal_chip(mode_count: int = MODE_COUNT) -> Chip:
    return Chip(mode_count, ((IDEAL_SPLIT_ANGLE, IDEAL_SPLIT_ANGLE),) * mzi_count(mode_count))


def fabricated_chip(mode_count: int, split_spread: float, rng: np.random.Generator) -> Chip:
    """Every coupler splits 50 % ± split_spread (standard deviation of the share that crosses over)."""
    if not 0 <= split_spread <= MAX_SPLIT_SPREAD:
        raise ChipError(f"Rozptyl dělicího poměru musí být mezi 0 a {MAX_SPLIT_SPREAD:.0%}.")
    if split_spread == 0:
        return ideal_chip(mode_count)
    ratios = np.clip(
        rng.normal(IDEAL_SPLIT_RATIO, split_spread, size=(mzi_count(mode_count), 2)), MIN_SPLIT_RATIO, MAX_SPLIT_RATIO,
    )
    angles = np.arcsin(np.sqrt(ratios))
    return Chip(mode_count, tuple((float(first), float(second)) for first, second in angles))


def split_ratios(chip: Chip) -> np.ndarray:
    """Share of the light each coupler sends into the other waveguide, one row per MZI."""
    return np.sin(np.array(chip.split_angles)) ** 2


def coupler_matrix(split_angle: float) -> np.ndarray:
    cosine, sine = np.cos(split_angle), np.sin(split_angle)
    return np.array([[cosine, 1j * sine], [1j * sine, cosine]])


def phase_matrix(phase: float) -> np.ndarray:
    return np.diag([np.exp(1j * phase), 1.0])


def mzi_matrix(
    internal: float, external: float, split_angles: Tuple[float, float] = (IDEAL_SPLIT_ANGLE, IDEAL_SPLIT_ANGLE),
) -> np.ndarray:
    first, second = split_angles
    return coupler_matrix(second) @ phase_matrix(internal) @ coupler_matrix(first) @ phase_matrix(external)


def transfer_matrix(chip: Chip, phases: MeshPhases) -> np.ndarray:
    """U with U_ij the amplitude that goes from input j to output i."""
    _check_phases(chip, phases)
    unitary = np.eye(chip.mode_count, dtype=complex)
    for index, slot in enumerate(chip.slots):
        mzi = mzi_matrix(phases.internal[index], phases.external[index], chip.split_angles[index])
        rows = slice(slot.upper_mode, slot.lower_mode + 1)
        unitary[rows, :] = mzi @ unitary[rows, :]
    return unitary


def transmission(unitary: np.ndarray) -> np.ndarray:
    """|U_ij|²: share of the light from input j that reaches output i (and the single-photon probability)."""
    return np.abs(unitary) ** 2


def pattern_match(chip_transmission: np.ndarray, target_transmission: np.ndarray) -> float:
    """1 − the share of light that lands elsewhere than the target says, averaged over the inputs.

    For each input it is half the sum of |difference| over the outputs (the total variation distance).
    """
    misplaced = 0.5 * np.abs(chip_transmission - target_transmission).sum(axis=0)
    return float(1 - misplaced.mean())


@dataclass(frozen=True)
class MziLight:
    """Light intensity on the upper and the lower waveguide of one MZI."""

    entering: Tuple[float, float]
    inside: Tuple[float, float]
    """Between the two couplers, in the arms of the interferometer."""
    leaving: Tuple[float, float]


@dataclass(frozen=True)
class LightFlow:
    input_modes: Tuple[int, ...]
    columns: Tuple[Tuple[float, ...], ...]
    """Intensity on each waveguide in front of each column of MZIs; the last entry is what the detectors get."""
    mzis: Tuple[MziLight, ...]
    """In the order of mesh_slots."""

    @property
    def detected(self) -> Tuple[float, ...]:
        return self.columns[-1]


def light_flow(chip: Chip, phases: MeshPhases, input_modes: Sequence[int]) -> LightFlow:
    """Where the light shone into the inputs goes, column by column; the intensities of the inputs add up.

    For one photon in each input the sum is the mean number of photons on a waveguide, whether the photons
    interfere or not: the interference shows only in which photons arrive together. Without inputs the laser is
    off and the chip stays dark.
    """
    _check_phases(chip, phases)
    _check_inputs(chip, input_modes)
    amplitudes = np.eye(chip.mode_count, dtype=complex)[:, list(input_modes)]
    columns = [_intensities(amplitudes)]
    mzis: List[MziLight] = []
    for column in range(chip.mode_count):
        for index in _indices_in_column(chip.slots, column):
            pair = slice(chip.slots[index].upper_mode, chip.slots[index].lower_mode + 1)
            first, second = chip.split_angles[index]
            entering = amplitudes[pair].copy()
            inside = coupler_matrix(first) @ phase_matrix(phases.external[index]) @ entering
            leaving = coupler_matrix(second) @ phase_matrix(phases.internal[index]) @ inside
            mzis.append(MziLight(_intensities(entering), _intensities(inside), _intensities(leaving)))
            amplitudes[pair] = leaving
        columns.append(_intensities(amplitudes))
    return LightFlow(tuple(input_modes), tuple(columns), tuple(mzis))


def _check_inputs(chip: Chip, input_modes: Sequence[int]) -> None:
    if not all(0 <= mode < chip.mode_count for mode in input_modes):
        raise ChipError(f"Světlo může vstupovat jen do vstupů 1 až {chip.mode_count}.")
    if len(set(input_modes)) != len(input_modes):
        raise ChipError("Každý vstup může být vybraný jen jednou.")


def _indices_in_column(slots: Sequence[MziSlot], column: int) -> List[int]:
    return [index for index, slot in enumerate(slots) if slot.column == column]


def _intensities(amplitudes: np.ndarray) -> Tuple[float, ...]:
    """Summed over the inputs, one per column of `amplitudes`."""
    return tuple(float(value) for value in (np.abs(amplitudes) ** 2).sum(axis=1))


def _check_phases(chip: Chip, phases: MeshPhases) -> None:
    if len(phases.internal) != len(chip.slots):
        raise ChipError(f"Čip má {len(chip.slots)} interferometrů, zadané fáze patří {len(phases.internal)}.")
