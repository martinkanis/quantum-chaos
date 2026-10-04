"""One run of the advantage lab: variances under both tunings, the degree sweep and the repeated simulation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np

from gbs.demo import REPETITIONS, sample_sizes_up_to
from gbs.monomial_problem import DegreeSweep, MonomialProblem, VarianceComparison, compare_variances, degree_sweep
from gbs.monomial_study import MonomialStudy, run_monomial_study
from gbs.photon_tuning import TuningMode


@dataclass(frozen=True)
class LabRun:
    problem: MonomialProblem
    mode: TuningMode
    comparisons: Dict[TuningMode, VarianceComparison]
    """Both tunings, so that the page can say what the other one would give."""
    sweep: DegreeSweep
    study: MonomialStudy

    @property
    def comparison(self) -> VarianceComparison:
        return self.comparisons[self.mode]


def run_lab(problem: MonomialProblem, mode: TuningMode, max_sample_size: int, seed: Optional[int]) -> LabRun:
    sizes = sample_sizes_up_to(max_sample_size)
    comparisons = {tuning: compare_variances(problem, tuning) for tuning in TuningMode}
    study = run_monomial_study(problem, comparisons[mode], sizes, REPETITIONS, np.random.default_rng(seed))
    return LabRun(problem=problem, mode=mode, comparisons=comparisons, sweep=degree_sweep(problem), study=study)
