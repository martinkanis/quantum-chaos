"""Run the boson-sampling estimator of gbs/boson_sampling.py on Quandela's Perceval simulator.

Checks that Perceval's output probabilities equal |Perm(U_{S,T})|² / S!, samples the estimator and measures how
source noise (distinguishable photons, multiphoton emission, losses) biases it. Perceval needs Python ≥ 3.10, so it
is not a dependency of the app; run for example with Podman from the repository root:

    podman run --rm -v "$PWD":/repo -w /repo docker.io/library/python:3.12 \
        sh -c "pip install -q perceval-quandela==1.3.1 numpy && PYTHONPATH=/repo python scripts/perceval_boson_sampling.py"
"""

from __future__ import annotations

import time

import numpy as np
import perceval as pcvl
from perceval.algorithm import Sampler

from gbs.boson_sampling import estimate, reference_problem

SHOTS = 20_000
NOISE_SCENARIOS = (
    ("nerozlišitelnost 0,95", dict(indistinguishability=0.95)),
    ("nerozlišitelnost 0,90", dict(indistinguishability=0.90)),
    ("propustnost 0,5", dict(transmittance=0.5)),
    ("g2 = 0,02", dict(g2=0.02)),
    ("vše dohromady", dict(indistinguishability=0.90, transmittance=0.5, g2=0.02)),
)


def processor(problem, noise=None) -> pcvl.Processor:
    proc = pcvl.Processor("SLOS", pcvl.Unitary(pcvl.Matrix(problem.unitary)), noise=noise)
    proc.with_input(pcvl.BasicState([1] * problem.photons + [0] * (problem.modes - problem.photons)))
    proc.min_detected_photons_filter(problem.photons)
    return proc


def perceval_probabilities(problem, noise=None) -> np.ndarray:
    results = Sampler(processor(problem, noise)).probs()["results"]
    by_pattern = {tuple(state): float(probability) for state, probability in results.items()}
    return np.array([by_pattern.get(tuple(int(count) for count in pattern), 0.0) for pattern in problem.patterns])


def main() -> None:
    problem = reference_problem()
    exact = estimate(problem)
    ideal = perceval_probabilities(problem)
    print(f"max |P_Perceval − |Perm|²/S!| = {np.max(np.abs(ideal - exact.probabilities)):.1e}")
    print(f"μ = {exact.exact_value:.6f}, relativní rozptyl výstřelu = {exact.relative_variance:.4f}")

    start = time.time()
    samples = Sampler(processor(problem)).samples(SHOTS)["results"]
    value_by_pattern = {tuple(int(count) for count in pattern): value
                        for pattern, value in zip(problem.patterns, exact.shot_values)}
    sampled = float(np.mean([value_by_pattern[tuple(state)] for state in samples]))
    print(f"{SHOTS} výstřelů: odhad {sampled:.6f}, relativní chyba {abs(sampled / exact.exact_value - 1):.4f} "
          f"({time.time() - start:.1f} s)")

    for label, parameters in NOISE_SCENARIOS:
        noisy = perceval_probabilities(problem, pcvl.NoiseModel(**parameters))
        biased = float(noisy @ exact.shot_values)
        print(f"{label}: odchylka střední hodnoty odhadu {biased / exact.exact_value - 1:+.4f}")


if __name__ == "__main__":
    main()
