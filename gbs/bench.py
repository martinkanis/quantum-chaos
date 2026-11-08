"""The optical bench around the chip: the light source, the losses between fibre and chip, and the detectors.

Losses are the same for every path, so they shrink what the detectors see without changing its shape. The values of
the detectors and losses are our estimates of typical numbers at 1550 nm (see the texts of the bench on the page).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict

import numpy as np

from gbs.photonic_chip import ESTIMATED_COLUMN_LENGTH_CM, ChipError

FIBRE_CHIP_TRANSITIONS = 2
"""Light enters the chip from a fibre and leaves it into another one."""
MAX_COUPLING_LOSS_DB = 10.0
MAX_WAVEGUIDE_LOSS_DB_PER_CM = 5.0
MAX_PHOTON_SHOTS = 100_000


class LightSource(str, Enum):
    LASER = "laser"
    PHOTONS = "fotony"
    """Single photons; the detectors count them and show the mean number of photons."""


class DetectorKind(str, Enum):
    PHOTODIODE = "fotodioda"
    APD = "apd"
    SNSPD = "snspd"


@dataclass(frozen=True)
class Detector:
    efficiency: float
    """Probability that a photon reaching the detector registers; for the photodiode its quantum efficiency."""
    dark_click_probability: float
    """Probability of a click without any photon in one detection window."""
    counts_photons: bool


DETECTORS: Dict[DetectorKind, Detector] = {
    DetectorKind.PHOTODIODE: Detector(efficiency=0.8, dark_click_probability=0.0, counts_photons=False),
    DetectorKind.APD: Detector(efficiency=0.2, dark_click_probability=1e-4, counts_photons=True),
    DetectorKind.SNSPD: Detector(efficiency=0.9, dark_click_probability=1e-6, counts_photons=True),
}
DEFAULT_DETECTORS: Dict[LightSource, DetectorKind] = {
    LightSource.LASER: DetectorKind.PHOTODIODE,
    LightSource.PHOTONS: DetectorKind.SNSPD,
}


@dataclass(frozen=True)
class Losses:
    coupling_db: float
    """Loss of one transition between fibre and chip."""
    waveguide_db_per_cm: float

    def __post_init__(self) -> None:
        if not 0 <= self.coupling_db <= MAX_COUPLING_LOSS_DB:
            raise ChipError(f"Ztráta vazby vlákno–čip musí být mezi 0 a {MAX_COUPLING_LOSS_DB:.0f} dB.")
        if not 0 <= self.waveguide_db_per_cm <= MAX_WAVEGUIDE_LOSS_DB_PER_CM:
            raise ChipError(f"Útlum světlovodů musí být mezi 0 a {MAX_WAVEGUIDE_LOSS_DB_PER_CM:.0f} dB/cm.")


@dataclass(frozen=True)
class Bench:
    source: LightSource
    detector_kind: DetectorKind
    losses: Losses

    def __post_init__(self) -> None:
        if compatible_detector(self.source, self.detector_kind) != self.detector_kind:
            raise ChipError("Fotodioda měří jen laser a jednotlivé fotony počítá jen APD nebo SNSPD.")

    @property
    def detector(self) -> Detector:
        return DETECTORS[self.detector_kind]


def compatible_detector(source: LightSource, chosen: DetectorKind) -> DetectorKind:
    """The chosen detector if it suits the source: a photodiode reads the power of the laser, single photons need a
    detector that counts them."""
    if DETECTORS[chosen].counts_photons == (source == LightSource.PHOTONS):
        return chosen
    return DEFAULT_DETECTORS[source]


def loss_db(losses: Losses, mode_count: int) -> float:
    """Both fibre–chip transitions and the waveguides across all columns of the mesh."""
    return FIBRE_CHIP_TRANSITIONS * losses.coupling_db + losses.waveguide_db_per_cm * chip_length_cm(mode_count)


def chip_length_cm(mode_count: int) -> float:
    return mode_count * ESTIMATED_COLUMN_LENGTH_CM


def bench_transmission(losses: Losses, mode_count: int) -> float:
    return 10 ** (-loss_db(losses, mode_count) / 10)


def registered_shares(chip_shares: np.ndarray, losses: Losses, detector: Detector, mode_count: int) -> np.ndarray:
    """Share of the light (or probability for one photon) that each detector registers: the chip's |U_ij|² for the
    input, times the transmission of the bench and the efficiency of the detector."""
    return np.asarray(chip_shares) * bench_transmission(losses, mode_count) * detector.efficiency


@dataclass(frozen=True)
class PhotonCounts:
    clicks: np.ndarray
    """Clicks of each detector."""
    expected: np.ndarray
    """Mean number of clicks of each detector."""
    shots: int
    silent_shots: int
    """Shots in which no detector clicked: the photon was lost or missed."""


def count_photons(
    registered: np.ndarray, detector: Detector, shots: int, rng: np.random.Generator,
) -> PhotonCounts:
    """One heralded photon after another: it registers at detector i with the probability registered[i] or nowhere,
    and every detector can also click in the dark."""
    if not detector.counts_photons:
        raise ChipError("Fotodioda jednotlivé fotony nezaznamená, zvol APD nebo SNSPD.")
    if not 1 <= shots <= MAX_PHOTON_SHOTS:
        raise ChipError(f"Počet fotonů musí být mezi 1 a {MAX_PHOTON_SHOTS:,}.".replace(",", " "))
    detector_count = len(registered)
    outcomes = rng.choice(detector_count + 1, size=shots, p=[*registered, max(0.0, 1 - float(np.sum(registered)))])
    by_photon = outcomes[:, None] == np.arange(detector_count)
    in_dark = rng.random((shots, detector_count)) < detector.dark_click_probability
    clicked = by_photon | in_dark
    dark = detector.dark_click_probability
    return PhotonCounts(
        clicks=clicked.sum(axis=0),
        expected=shots * (registered + (1 - registered) * dark),
        shots=shots,
        silent_shots=int(np.sum(~clicked.any(axis=1))),
    )
