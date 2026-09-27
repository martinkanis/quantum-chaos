"""One end-to-end run of the GBS-based estimator next to classical Monte Carlo."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from gbs.expectation import ConvergenceStudy, MomentProblem, run_convergence_study
from gbs.sampler import GbsProgram, program_from_covariance, sample_shots, total_photon_distribution

REPETITIONS = 20
MIN_SAMPLE_SIZE = 100
MAX_SAMPLE_SIZE = 1_000_000
SAMPLE_SIZE_POINTS = 13
SHOT_PREVIEW_COUNT = 24
SHOT_PREVIEW_MAX_TOTAL = 8
PHOTON_CHART_MAX_TOTAL = 12


class DemoParametersError(ValueError):
    """Raised when the requested run is outside the supported range."""


@dataclass(frozen=True)
class GbsDemoRun:
    problem: MomentProblem
    program: GbsProgram
    study: ConvergenceStudy
    shots: List[Optional[np.ndarray]]
    """Individual detector readouts for illustration; None when a shot has too many photons to list."""
    total_photon_probabilities: np.ndarray


def run_gbs_demo(
    problem: MomentProblem, squeezing_strength: float, max_sample_size: int, seed: Optional[int]
) -> GbsDemoRun:
    program = program_from_covariance(problem.covariance, squeezing_strength)
    rng = np.random.default_rng(seed)
    study = run_convergence_study(problem, program, sample_sizes_up_to(max_sample_size), REPETITIONS, rng)
    return GbsDemoRun(
        problem=problem,
        program=program,
        study=study,
        shots=sample_shots(program, SHOT_PREVIEW_COUNT, rng, SHOT_PREVIEW_MAX_TOTAL),
        total_photon_probabilities=total_photon_distribution(program, PHOTON_CHART_MAX_TOTAL),
    )


def sample_sizes_up_to(max_sample_size: int) -> np.ndarray:
    if not MIN_SAMPLE_SIZE < max_sample_size <= MAX_SAMPLE_SIZE:
        raise DemoParametersError(
            f"Počet vzorků musí být mezi {MIN_SAMPLE_SIZE} a {MAX_SAMPLE_SIZE:,}.".replace(",", " ")
        )
    sizes = np.logspace(np.log10(MIN_SAMPLE_SIZE), np.log10(max_sample_size), SAMPLE_SIZE_POINTS)
    return np.unique(sizes.round().astype(int))
