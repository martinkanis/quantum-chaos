"""Count the two-qubit gates of the exported Qiskit circuits after translation to the native gates of IQM machines.

The Qiskit export (gbs/qiskit_export.py) emulates photonic modes on qubits. Sending such a circuit to a qubit
computer, for example VLQ in Ostrava (IQM, 24 qubits), first needs it in native gates: PRX (Qiskit's "r") and CZ.
Qiskit is not a dependency of the app, so ui/piquasso_content.py stores what this script prints. Run from the
repository root, for example:

    python3.12 -m venv /tmp/qk && /tmp/qk/bin/pip install -q "qiskit>=1.0" numpy
    PYTHONPATH=. /tmp/qk/bin/python scripts/qiskit_native_gate_counts.py

All-to-all connectivity is assumed, so the counts are a lower bound for a real chip; on VLQ's star topology every
CZ between two qubits also needs two MOVE operations through the central resonator. The second number replaces
the full preparation unitary of one mode by Qiskit's StatePreparation, the cheaper way to load the same state.
"""

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path

from qiskit import QuantumCircuit, qasm3, transpile
from qiskit.circuit.library import StatePreparation

from gbs.benchmark_problems import find_benchmark
from gbs.photon_tuning import TuningMode
from gbs.qiskit_export import build_qiskit_script

PROBLEMS = ("extremni-moment", "spolecny-extrem")
"""The two smallest problems; each beam splitter of the larger ones is another 10-qubit unitary like the second."""
NATIVE_GATES = ["r", "cz"]


def exported_module(key: str, directory: Path):
    path = directory / f"{key.replace('-', '_')}.py"
    path.write_text(build_qiskit_script(find_benchmark(key).problem, TuningMode.PER_MODE, seed=42), encoding="utf-8")
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def native(circuit: QuantumCircuit) -> QuantumCircuit:
    return transpile(circuit, basis_gates=NATIVE_GATES, optimization_level=1, seed_transpiler=1)


def main() -> None:
    print("QISKIT_NATIVE_GATE_COUNTS = (")
    with tempfile.TemporaryDirectory() as directory:
        for key in PROBLEMS:
            module = exported_module(key, Path(directory))
            kernel = module.MODE_SCALES[:, None] * module.COVARIANCE * module.MODE_SCALES[None, :]
            squeezing, orthogonal = module.device_settings(kernel)
            cutoff = 2**module.QUBITS_PER_MODE
            circuit = native(module.gbs_circuit(squeezing, orthogonal, cutoff))
            state, _ = module.squeezed_vacuum(squeezing[0], cutoff)
            preparation = QuantumCircuit(module.QUBITS_PER_MODE)
            preparation.append(StatePreparation(state / (sum(abs(amplitude) ** 2 for amplitude in state) ** 0.5)),
                               range(module.QUBITS_PER_MODE))
            print(f'    NativeGateCount("{key}", qubits={circuit.num_qubits}, cz={circuit.count_ops().get("cz", 0)}, '
                  f'qasm_lines={len(qasm3.dumps(circuit).splitlines())}, '
                  f'state_preparation_cz={native(preparation).count_ops().get("cz", 0)}),')
    print(")")


if __name__ == "__main__":
    main()
