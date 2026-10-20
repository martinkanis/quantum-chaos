"""Emulate a small Gaussian boson sampler in Quandela's Perceval, which has no squeezed states of its own.

Single-mode squeezed vacuum is a superposition of even photon numbers,
|ψ_r⟩ = (cosh r)^(-1/2) Σ_k (-tanh r)^k √((2k)!) / (2^k k!) |2k⟩, so it can be written as a Perceval StateVector
cut at CUTOFF photons per mode. The interferometer conserves photon number, so every output pattern with at most
CUTOFF photons is exact and is compared with the hafnian formula of gbs/sampler.py. This works only in the simulator:
the hardware takes single photons as input and cannot prepare such a superposition. Run like
scripts/perceval_boson_sampling.py, for example with Podman from the repository root:

    podman run --rm -v "$PWD":/repo -w /repo docker.io/library/python:3.12 \
        sh -c "pip install -q perceval-quandela==1.3.1 numpy && PYTHONPATH=/repo python scripts/perceval_gbs_emulation.py"
"""

from __future__ import annotations

import itertools
import math
from typing import Dict

import numpy as np
import perceval as pcvl

from gbs.sampler import GbsProgram, pattern_probability, patterns_with_total, program_from_covariance

COVARIANCE = np.array([[1.0, 0.5, 0.2], [0.5, 1.0, 0.3], [0.2, 0.3, 1.0]])
SQUEEZING_STRENGTH = 0.6
CUTOFF = 6


def squeezed_vacuum_amplitudes(squeezing: float) -> Dict[int, float]:
    return {
        2 * pairs: (-math.tanh(squeezing)) ** pairs * math.sqrt(math.factorial(2 * pairs))
        / (2**pairs * math.factorial(pairs) * math.sqrt(math.cosh(squeezing)))
        for pairs in range(CUTOFF // 2 + 1)
    }


def truncated_input(program: GbsProgram) -> pcvl.StateVector:
    per_mode = [squeezed_vacuum_amplitudes(squeezing) for squeezing in program.squeezing]
    state = pcvl.StateVector()
    for counts in itertools.product(*[sorted(amplitudes) for amplitudes in per_mode]):
        amplitude = math.prod(per_mode[mode][count] for mode, count in enumerate(counts))
        state += amplitude * pcvl.StateVector(pcvl.BasicState(list(counts)))
    return state


def kept_norm(program: GbsProgram) -> float:
    """Probability that no mode holds more than CUTOFF photons; Perceval renormalises the truncated state."""
    return math.prod(
        sum(amplitude**2 for amplitude in squeezed_vacuum_amplitudes(squeezing).values())
        for squeezing in program.squeezing
    )


def main() -> None:
    program = program_from_covariance(COVARIANCE, SQUEEZING_STRENGTH)
    simulator = pcvl.Simulator(pcvl.SLOSBackend())
    simulator.set_circuit(pcvl.Unitary(pcvl.Matrix(program.interferometer)))
    output = simulator.evolve(truncated_input(program))
    probabilities = {tuple(state): abs(amplitude) ** 2 for state, amplitude in output}
    rescale = kept_norm(program) / sum(probabilities.values())

    deviations = [
        abs(probabilities.get(tuple(int(count) for count in pattern), 0.0) * rescale - pattern_probability(program, pattern))
        for total in range(0, CUTOFF + 1, 2)
        for pattern in patterns_with_total(program.mode_count, total)
    ]
    odd_mass = sum(probability for state, probability in probabilities.items() if sum(state) % 2)
    print(f"input components: {(CUTOFF // 2 + 1) ** program.mode_count}, kept norm {kept_norm(program):.6f}")
    print(f"max |P_Perceval − Haf²/(n!·Π cosh r)| over totals ≤ {CUTOFF}: {max(deviations):.1e}")
    print(f"probability of an odd photon number: {odd_mass:.1e}")


if __name__ == "__main__":
    main()
