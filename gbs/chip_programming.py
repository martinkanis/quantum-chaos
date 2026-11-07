"""Programming the photonic chip: target matrices, phases from the design and tuned on a fabricated chip, readout."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict

import numpy as np

from gbs.boson_sampling import random_unitary
from gbs.clements import clements_decomposition
from gbs.photonic_chip import (
    IDEAL_SPLIT_ANGLE,
    MODE_COUNT,
    Chip,
    ChipError,
    LightFlow,
    MeshPhases,
    coupler_matrix,
    fabricated_chip,
    light_flow,
    pattern_match,
    transfer_matrix,
    transmission,
)

TARGET_STREAM = 0
CHIP_STREAM = 1
"""The seed drives two independent random streams: the random target and the fabrication errors."""
MAX_CALIBRATION_SWEEPS = 40
CALIBRATION_TOLERANCE = 1e-12
FOURIER_SAMPLES = 5
"""The squared error of |U|² is a trigonometric polynomial of degree 2 in each phase: five samples fix it."""
PHASE_GRID = np.linspace(0, 2 * np.pi, 4096, endpoint=False)


class ChipTarget(str, Enum):
    PASS_THROUGH = "pruchod"
    REVERSE = "obraceni"
    TWO_SPLITTERS = "dva-delice"
    SPREAD_EVENLY = "rovnomerne"
    RANDOM = "nahodna"


def _two_splitters(mode_count: int, _rng: np.random.Generator) -> np.ndarray:
    """50:50 couplers on the waveguide pairs (1, 2), (3, 4), …; an odd last waveguide passes through."""
    unitary = np.eye(mode_count, dtype=complex)
    for upper_mode in range(0, mode_count - 1, 2):
        unitary[upper_mode:upper_mode + 2, upper_mode:upper_mode + 2] = coupler_matrix(IDEAL_SPLIT_ANGLE)
    return unitary


def _discrete_fourier(mode_count: int, _rng: np.random.Generator) -> np.ndarray:
    indices = np.arange(mode_count)
    return np.exp(2j * np.pi * np.outer(indices, indices) / mode_count) / np.sqrt(mode_count)


TARGET_BUILDERS: Dict[ChipTarget, Callable[[int, np.random.Generator], np.ndarray]] = {
    ChipTarget.PASS_THROUGH: lambda mode_count, _rng: np.eye(mode_count, dtype=complex),
    ChipTarget.REVERSE: lambda mode_count, _rng: np.eye(mode_count, dtype=complex)[::-1],
    ChipTarget.TWO_SPLITTERS: _two_splitters,
    ChipTarget.SPREAD_EVENLY: _discrete_fourier,
    ChipTarget.RANDOM: random_unitary,
}


def target_unitary(target: ChipTarget, mode_count: int, rng: np.random.Generator) -> np.ndarray:
    return TARGET_BUILDERS[target](mode_count, rng)


@dataclass(frozen=True)
class ChipSetup:
    chip: Chip
    target: np.ndarray
    """Unitary matrix the chip should realise."""


def build_setup(target: ChipTarget, split_spread: float, seed: int, mode_count: int = MODE_COUNT) -> ChipSetup:
    """The same seed gives the same random target and the same fabricated chip."""
    if seed < 0:
        raise ChipError("Seed musí být nezáporné celé číslo.")
    chip = fabricated_chip(mode_count, split_spread, np.random.default_rng([seed, CHIP_STREAM]))
    return ChipSetup(chip, target_unitary(target, mode_count, np.random.default_rng([seed, TARGET_STREAM])))


def design_phases(setup: ChipSetup) -> MeshPhases:
    """Phases from the Clements decomposition of the target; exact on the ideal chip, blind to fabrication errors."""
    return clements_decomposition(setup.target).phases


def calibrated_phases(setup: ChipSetup) -> MeshPhases:
    """Design phases tuned on this chip: each phase in turn moves to where the squared error of |U|² is smallest.

    In a lab the coupler errors are first measured (chip characterisation); the simulator knows them directly.
    The squared error is not the match the page shows, so the design phases stay when tuning does not raise it.
    """
    design = design_phases(setup)
    target = transmission(setup.target)
    values = np.array(design.internal + design.external)
    error = _squared_error(setup.chip, values, target)
    for _ in range(MAX_CALIBRATION_SWEEPS):
        for index in range(values.size):
            values[index] = _better_phase(setup.chip, values, index, target)
        new_error = _squared_error(setup.chip, values, target)
        if error - new_error < CALIBRATION_TOLERANCE:
            break
        error = new_error
    tuned = _mesh_phases(values)
    return tuned if _match(setup, tuned) > _match(setup, design) else design


def _match(setup: ChipSetup, phases: MeshPhases) -> float:
    return pattern_match(transmission(transfer_matrix(setup.chip, phases)), transmission(setup.target))


def _better_phase(chip: Chip, values: np.ndarray, index: int, target: np.ndarray) -> float:
    """Minimum of the error over one phase, read from its exact Fourier series; the old value if that is better."""

    def error_at(phase: float) -> float:
        trial = values.copy()
        trial[index] = phase
        return _squared_error(chip, trial, target)

    samples = [error_at(2 * np.pi * sample / FOURIER_SAMPLES) for sample in range(FOURIER_SAMPLES)]
    coefficients = np.fft.rfft(samples) / FOURIER_SAMPLES
    curve = coefficients[0].real + 2 * np.real(
        coefficients[1] * np.exp(1j * PHASE_GRID) + coefficients[2] * np.exp(2j * PHASE_GRID)
    )
    candidate = float(PHASE_GRID[np.argmin(curve)])
    return candidate if error_at(candidate) < error_at(values[index]) else float(values[index])


def _squared_error(chip: Chip, values: np.ndarray, target: np.ndarray) -> float:
    chip_transmission = transmission(transfer_matrix(chip, _mesh_phases(values)))
    return float(np.sum((chip_transmission - target) ** 2))


def _mesh_phases(values: np.ndarray) -> MeshPhases:
    """The flat vector holds all θ first, then all φ."""
    count = len(values) // 2
    return MeshPhases(tuple(float(value) for value in values[:count]), tuple(float(value) for value in values[count:]))


@dataclass(frozen=True)
class ChipReadout:
    chip_transmission: np.ndarray
    target_transmission: np.ndarray
    flow: LightFlow

    @property
    def match(self) -> float:
        return pattern_match(self.chip_transmission, self.target_transmission)

    @property
    def largest_deviation(self) -> float:
        """Largest |difference| of one element of |U|², in shares of the input light."""
        return float(np.abs(self.chip_transmission - self.target_transmission).max())


def read_out(setup: ChipSetup, phases: MeshPhases, input_mode: int) -> ChipReadout:
    return ChipReadout(
        chip_transmission=transmission(transfer_matrix(setup.chip, phases)),
        target_transmission=transmission(setup.target),
        flow=light_flow(setup.chip, phases, (input_mode,)),
    )
