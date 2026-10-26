"""Run the five problems of the advantage page in Piquasso and compare them with the hafnian formula of this app.

Piquasso (https://piquasso.com) is not a dependency of the app, so ui/piquasso_content.py stores what this
script prints. It needs Python 3.10 or newer (Piquasso 8 dropped 3.9). For example from the repository root:

    python3.12 -m venv /tmp/pq && /tmp/pq/bin/pip install -q "piquasso==8.0.2" "qiskit>=1.0"
    PYTHONPATH=. /tmp/pq/bin/python scripts/piquasso_gbs_check.py

Three checks:
 1. The probability of the target pattern n from GaussianSimulator against p(n) = Haf(B_n)² / (n!·Π cosh r_j).
 2. Sampling the "společný extrém" problem with growing measurement cutoffs: how often the pattern comes up, the
    GBS-P estimate of the moment from that frequency and the mean photon number against Σ sinh² r_j. The largest
    cutoff ends with an error in Piquasso 8.0.2, which the script reports.
 3. The Bell circuit H + CNOT from Qiskit through Piquasso's dual-rail encoding: the norm of the post-selected
    state is the success probability of the linear-optics CNOT.
"""

from __future__ import annotations

import numpy as np
import piquasso as pq
from qiskit import QuantumCircuit
from piquasso.dual_rail_encoding import dual_rail_encode_from_qiskit

from gbs.benchmark_problems import BENCHMARK_PROBLEMS, find_benchmark
from gbs.gaussian_moments import moment_table
from gbs.monomial_problem import gbs_p_estimate, pattern_probability
from gbs.photon_tuning import TuningMode, tune_encoding

SAMPLED_PROBLEM = "spolecny-extrem"
SHOTS = 20000
SEED = 42
MEASUREMENT_CUTOFFS = (5, 40, 80)
"""The default of pq.Config, one that still cuts the tail of the photon number, and one large enough."""
FAILING_MEASUREMENT_CUTOFF = 160
FAILING_SHOTS = 200


def gbs_program(encoding, measure: bool) -> pq.Program:
    modes = len(encoding.squeezing)
    with pq.Program() as program:
        for mode, squeezing in enumerate(encoding.squeezing):
            pq.Q(mode) | pq.Squeezing(float(squeezing))
        pq.Q(*range(modes)) | pq.Interferometer(np.asarray(encoding.interferometer))
        if measure:
            pq.Q(*range(modes)) | pq.ParticleNumberMeasurement()
    return program


def exact_moment(problem) -> float:
    exponents = tuple(int(power) for power in problem.exponents)
    return float(moment_table(np.asarray(problem.covariance), list(exponents))[exponents])


def compare_probabilities() -> None:
    print("PIQUASSO_PROBABILITIES = (")
    for benchmark in BENCHMARK_PROBLEMS:
        problem = benchmark.problem
        encoding = tune_encoding(problem.covariance, problem.exponents, TuningMode.PER_MODE)
        ours = pattern_probability(encoding, problem.exponents, exact_moment(problem))
        simulator = pq.GaussianSimulator(d=len(problem.exponents))
        state = simulator.execute(gbs_program(encoding, measure=False)).state
        theirs = float(state.get_particle_detection_probability(occupation_number=np.asarray(problem.exponents)))
        print(f'    PiquassoProbability("{benchmark.key}", {theirs!r}),  # relative difference {theirs / ours - 1:.1e}')
    print(")")


def sample() -> None:
    problem = find_benchmark(SAMPLED_PROBLEM).problem
    encoding = tune_encoding(problem.covariance, problem.exponents, TuningMode.PER_MODE)
    target = tuple(int(power) for power in problem.exponents)
    moment = exact_moment(problem)
    print(f"# {SAMPLED_PROBLEM}: pattern {target}, exact probability {pattern_probability(encoding, target, moment):.6f}, "
          f"exact moment {moment!r}, mean photons {float(np.sum(encoding.mean_photons_per_squeezer)):.3f}")
    print("PIQUASSO_SAMPLING = (")
    for cutoff in MEASUREMENT_CUTOFFS:
        samples = run_sampler(encoding, cutoff, SHOTS)
        totals = np.array([sum(sample_) for sample_ in samples])
        hits = sum(1 for sample_ in samples if tuple(sample_) == target)
        print(f"    PiquassoSampling(measurement_cutoff={cutoff}, shots={SHOTS}, hits={hits}, "
              f"max_photons_per_mode={max(max(sample_) for sample_ in samples)}, "
              f"mean_photons={totals.mean():.2f}, mean_photons_error={totals.std() / np.sqrt(SHOTS):.2f}, "
              f"estimate={gbs_p_estimate(encoding, target, hits / SHOTS):.0f}),")
    print(")")
    try:
        run_sampler(encoding, FAILING_MEASUREMENT_CUTOFF, FAILING_SHOTS)
        print(f"# measurement_cutoff={FAILING_MEASUREMENT_CUTOFF}: no error")
    except ValueError as error:
        print(f"# measurement_cutoff={FAILING_MEASUREMENT_CUTOFF}: {type(error).__name__}: {error}")


def run_sampler(encoding, cutoff: int, shots: int):
    config = pq.Config(measurement_cutoff=cutoff, seed_sequence=SEED)
    simulator = pq.GaussianSimulator(d=len(encoding.squeezing), config=config)
    return simulator.execute(gbs_program(encoding, True), shots=shots).samples


def dual_rail_cnot() -> None:
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    program = dual_rail_encode_from_qiskit(circuit)
    modes = 1 + max(max(instruction.modes) for instruction in program.instructions if instruction.modes)
    state = pq.PureFockSimulator(d=modes, config=pq.Config(cutoff=7)).execute(program).state
    print(f"DUAL_RAIL_CNOT_SUCCESS = {float(state.norm)!r}  # modes {modes}, 2/27 = {2 / 27!r}")


if __name__ == "__main__":
    print(f"# Piquasso {pq.__version__}")
    compare_probabilities()
    sample()
    dual_rail_cnot()
