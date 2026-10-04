"""Downloadable Qiskit script that emulates the GBS-P estimate of E[x^n] on qubits."""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, log2, prod
from pathlib import Path
from string import Template
from typing import Optional

from gbs.monomial_problem import MonomialProblem
from gbs.photon_tuning import DeviceEncoding, TuningMode, tune_encoding
from gbs.sampler import squeezed_vacuum_distribution

TEMPLATE = Template((Path(__file__).parent / "qiskit_script_template.txt").read_text(encoding="utf-8"))
SCRIPT_FILE_NAME = "gbs_monom_qiskit.py"
DEFAULT_SHOTS = 100_000
MAX_QUBITS = 20
"""A 20-qubit state vector takes tens of seconds on a laptop; more would be impractical."""
MAX_QUBITS_PER_MODE = 5
"""A beam splitter acts on two modes as a dense 2^(2q) × 2^(2q) matrix: 1024 × 1024 for q = 5."""
MAX_QUBITS_SINGLE_MODE = 8
"""Without beam splitters only the 2^q × 2^q state preparation is needed."""
TARGET_KEPT_PROBABILITY = 0.99

TUNING_DESCRIPTIONS = {
    TuningMode.TOTAL: "střední celkový počet fotonů = stupeň monomu (Andersen a Shan)",
    TuningMode.PER_MODE: "střední počet fotonů v každém módu = jeho exponent",
}


class QiskitExportError(ValueError):
    """Raised when the problem is too large to be emulated on qubits."""


@dataclass(frozen=True)
class QubitEmulation:
    mode_count: int
    qubits_per_mode: int
    kept_probability: float
    """Probability that no squeezer emits more photons than the qubits of its mode can hold."""

    @property
    def qubit_count(self) -> int:
        return self.mode_count * self.qubits_per_mode

    @property
    def fock_cutoff(self) -> int:
        return 2**self.qubits_per_mode


def plan_emulation(encoding: DeviceEncoding, degree: int) -> QubitEmulation:
    """Fewest qubits per mode that hold the target pattern exactly and keep almost all of the squeezed light.

    The interferometer conserves the photon number, so the target pattern only depends on states with at most
    `degree` photons per mode: a cutoff above the degree makes its amplitude exact.
    """
    mode_count = len(encoding.tanh_squeezing)
    fewest = max(1, ceil(log2(degree + 1)))
    most = min(MAX_QUBITS_SINGLE_MODE if mode_count == 1 else MAX_QUBITS_PER_MODE, MAX_QUBITS // mode_count)
    if fewest > most:
        raise QiskitExportError(
            f"Na emulaci v Qiskitu je úloha příliš velká: potřebovala by aspoň {mode_count * fewest} qubitů "
            f"({mode_count} módů × {fewest}), ale rozumně se dá simulovat nejvýš {mode_count * most}. "
            "Sniž stupeň monomu nebo počet proměnných."
        )
    qubits = fewest
    while qubits < most and kept_probability(encoding, 2**qubits) < TARGET_KEPT_PROBABILITY:
        qubits += 1
    return QubitEmulation(
        mode_count=mode_count, qubits_per_mode=qubits, kept_probability=kept_probability(encoding, 2**qubits),
    )


def kept_probability(encoding: DeviceEncoding, cutoff: int) -> float:
    return prod(
        float(squeezed_vacuum_distribution(squeezing, cutoff - 1).sum()) for squeezing in encoding.squeezing
    )


def emulation_for(problem: MonomialProblem, mode: TuningMode) -> QubitEmulation:
    used = problem.used_variables()
    return plan_emulation(tune_encoding(used.covariance, used.exponents, mode), used.degree)


def build_qiskit_script(problem: MonomialProblem, mode: TuningMode, seed: Optional[int]) -> str:
    used = problem.used_variables()
    encoding = tune_encoding(used.covariance, used.exponents, mode)
    emulation = plan_emulation(encoding, used.degree)
    return TEMPLATE.substitute(
        formula=monomial_formula(used),
        encoding=TUNING_DESCRIPTIONS[mode],
        file_name=SCRIPT_FILE_NAME,
        covariance=repr(used.covariance.tolist()),
        exponents=repr(used.exponents),
        variable_names=repr(list(used.variable_names)),
        mode_scales=repr(encoding.mode_scales.tolist()),
        qubits_per_mode=emulation.qubits_per_mode,
        shots=DEFAULT_SHOTS,
        seed=repr(seed),
    )


def monomial_formula(problem: MonomialProblem) -> str:
    factors = [f"{name}^{power}" for name, power in zip(problem.variable_names, problem.exponents) if power]
    return _docstring_text(f"E[{' · '.join(factors)}]")


def _docstring_text(text: str) -> str:
    """Names come from the form; quotes, backslashes or line breaks would break the docstring of the script."""
    return " ".join(text.replace("\\", "/").replace('"', "'").split())
