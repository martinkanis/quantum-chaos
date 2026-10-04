import subprocess
import sys

import numpy as np
import pytest

from gbs.benchmark_problems import BENCHMARK_PROBLEMS, equicorrelated_matrix, find_benchmark
from gbs.monomial_problem import MonomialProblem
from gbs.photon_tuning import TuningMode
from gbs.qiskit_export import MAX_QUBITS, QiskitExportError, build_qiskit_script, emulation_for

SCRIPT_TIMEOUT_SECONDS = 120


@pytest.mark.parametrize("benchmark", BENCHMARK_PROBLEMS, ids=lambda benchmark: benchmark.key)
@pytest.mark.parametrize("mode", list(TuningMode))
def test_skript_je_platny_python_pro_kazdou_pripravenou_ulohu(benchmark, mode):
    script = build_qiskit_script(benchmark.problem, mode, seed=42)

    compile(script, "gbs_monom_qiskit.py", "exec")
    assert repr(benchmark.problem.exponents) in script


@pytest.mark.parametrize("benchmark", BENCHMARK_PROBLEMS, ids=lambda benchmark: benchmark.key)
def test_emulace_ma_orez_nad_stupnem_a_nejvys_20_qubitu(benchmark):
    emulation = emulation_for(benchmark.problem, TuningMode.PER_MODE)

    assert emulation.fock_cutoff > benchmark.problem.degree
    assert emulation.qubit_count <= MAX_QUBITS
    assert 0.8 < emulation.kept_probability <= 1


def test_prilis_velka_uloha_nejde_emulovat():
    too_large = MonomialProblem(
        covariance=equicorrelated_matrix(4, 0.5), exponents=(10, 10, 10, 10), variable_names=("A", "B", "C", "D"),
    )

    with pytest.raises(QiskitExportError, match="příliš velká"):
        build_qiskit_script(too_large, TuningMode.PER_MODE, seed=None)


def test_nazvy_promennych_s_uvozovkami_a_lomitky_nerozbiji_skript():
    tricky = MonomialProblem(
        covariance=np.eye(2), exponents=(2, 2), variable_names=('Akcie """ \\N', "Zlato\nnový řádek"),
    )

    compile(build_qiskit_script(tricky, TuningMode.PER_MODE, seed=1), "gbs_monom_qiskit.py", "exec")


def test_skript_v_qiskitu_odhadne_moment_a_projde_kontrolou(tmp_path):
    pytest.importorskip("qiskit")
    script_path = tmp_path / "gbs_monom_qiskit.py"
    script_path.write_text(
        build_qiskit_script(find_benchmark("extremni-moment").problem, TuningMode.PER_MODE, seed=42),
        encoding="utf-8",
    )

    output = subprocess.run(
        [sys.executable, str(script_path)], capture_output=True, text=True, check=True, timeout=SCRIPT_TIMEOUT_SECONDS,
    ).stdout

    assert "Kontrola: p(n) ze stavového vektoru 0.0236046, z hafniánu 0.0236046" in output
