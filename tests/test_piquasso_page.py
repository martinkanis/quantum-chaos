from math import comb, log10, sqrt

import numpy as np
import pytest

from gbs.benchmark_problems import find_benchmark
from gbs.monomial_problem import gbs_p_estimate
from gbs.photon_tuning import TuningMode, tune_encoding
from ui import ids
from ui.guide_practice import QISKIT
from ui.navigation import (
    ACTIVE_LINK_CLASS,
    NAV_LINK_IDS,
    PAGE_BY_PATH,
    PAGE_IDS,
    PHOTONICS_LANDSCAPE_PATH,
    PIQUASSO_PATH,
    piquasso_href,
    show_page,
)
from ui.piquasso_content import (
    ASSUMED_GATE_FIDELITY,
    DUAL_RAIL_CNOT_SUCCESS,
    FAILING_MEASUREMENT_CUTOFF,
    KEY_FINDINGS,
    OPERATIONS_PER_CZ_ON_STAR,
    PIQUASSO_PROBABILITIES,
    PIQUASSO_SAMPLING,
    PITFALLS_TOPIC,
    QISKIT_NATIVE_GATE_COUNTS,
    QUBITS_TOPIC,
    SAMPLED_PROBLEM,
    SIMULATORS_TOPIC,
    SOURCES_ANCHOR,
    TOPICS,
    TWO_QUBIT_GATES_EXAMPLE,
    VERIFICATION_TOPIC,
)
from ui.piquasso_page import (
    app_probability,
    build_piquasso_page,
    exact_moment,
    gate_counts_markdown,
    probabilities_markdown,
    sampling_markdown,
    target_pattern,
)
from ui.study_progress import describe_pager
from ui.theory_content import all_sources
from ui.topic_catalog import breadcrumb_trail


def czech(value: float, digits: int) -> str:
    return f"{value:,.{digits}f}".replace(",", " ").replace(".", ",")


def text_of(topic) -> str:
    return " ".join((topic.in_short + " " + topic.explanation).split())


def test_stranka_je_druhym_krokem_tematu_fotonika_ve_svete():
    link_classes = show_page(PIQUASSO_PATH)[len(PAGE_IDS):len(PAGE_IDS) + len(NAV_LINK_IDS)]
    active = [link_id for link_id, link_class in zip(NAV_LINK_IDS, link_classes) if link_class == ACTIVE_LINK_CLASS]
    _, step_label, links, _, _ = describe_pager(PIQUASSO_PATH, None)

    assert PAGE_BY_PATH[PIQUASSO_PATH] == ids.PIQUASSO_PAGE
    assert active == [ids.NAV_PHOTONICS_MENU]
    assert step_label == "Fotonika ve světě · krok 2 / 2"
    assert links[0].children.href == PHOTONICS_LANDSCAPE_PATH
    assert [label for label, _ in breadcrumb_trail(ids.PIQUASSO_PAGE)] == [
        "Témata", "Fotonika a GBS", "Fotonika ve světě: konkurence a partneři",
        "Piquasso: simulátor fotonického kvantového počítače",
    ]


def test_kapitoly_maji_unikatni_kotvy_zdroje_s_odkazem_a_tldr_na_ne_odkazuje():
    anchors = [topic.anchor for topic in TOPICS]
    page = build_piquasso_page()
    section_ids = [child.id for child in page.children if getattr(child, "id", None)]

    assert section_ids == anchors + [SOURCES_ANCHOR]
    assert all(anchor.startswith("piquasso-") for anchor in section_ids)
    assert {finding.anchor for finding in KEY_FINDINGS} <= set(anchors)
    assert piquasso_href(anchors[0]) == f"{PIQUASSO_PATH}#{anchors[0]}"
    assert all(topic.further_reading for topic in TOPICS)
    assert all("](http" in source.citation for source in all_sources(TOPICS))


def test_pravdepodobnosti_z_piquassa_se_shoduji_se_vzorcem_aplikace():
    differences = [abs(stored.probability / app_probability(stored.problem_key) - 1) for stored in PIQUASSO_PROBABILITIES]
    rows = probabilities_markdown().splitlines()[2:]

    assert [stored.problem_key for stored in PIQUASSO_PROBABILITIES] == [
        "extremni-moment", "spolecny-extrem", "nesoumerny-monom", "historie-usa", "trzni-faktor",
    ]
    assert max(differences) < 1e-10
    assert f"{max(differences):.0e}" == "6e-11" and "6 · 10⁻¹¹" in text_of(VERIFICATION_TOPIC)
    assert len(rows) == len(PIQUASSO_PROBABILITIES)


def test_cisla_o_vzorkovani_odpovidaji_ulozenym_vysledkum():
    problem = find_benchmark(SAMPLED_PROBLEM).problem
    encoding = tune_encoding(problem.covariance, problem.exponents, TuningMode.PER_MODE)
    pattern = target_pattern(SAMPLED_PROBLEM)
    probability = app_probability(SAMPLED_PROBLEM)
    default, *large = PIQUASSO_SAMPLING
    run = large[0]
    relative_error = run.estimate / exact_moment(SAMPLED_PROBLEM) - 1
    statistical_error = sqrt((1 - probability) / (4 * run.shots * probability))
    text = text_of(VERIFICATION_TOPIC) + " " + text_of(PITFALLS_TOPIC)

    assert pattern == (8, 8) and default.measurement_cutoff == 5
    assert default.max_photons_per_mode < max(pattern) and default.hits == 0
    assert all(other.hits == run.hits and other.max_photons_per_mode >= max(pattern) for other in large)
    assert all(abs(other.estimate - gbs_p_estimate(encoding, pattern, other.hits / other.shots)) < 1 for other in large)
    assert f"asi {czech(run.shots * probability, 1)}krát" in text and f"padl {run.hits}krát" in text
    assert f"moment {czech(run.estimate, 0)} proti přesným {czech(exact_moment(SAMPLED_PROBLEM), 1)}" in text
    assert f"o {czech(-100 * relative_error, 1)} % méně" in text and abs(relative_error) < 2 * statistical_error
    assert f"asi {czech(100 * statistical_error, 1)} %" in text
    assert round(float(np.sum(encoding.mean_photons_per_squeezer)), 6) == 16
    assert ", ".join(czech(other.mean_photons, 2) for other in PIQUASSO_SAMPLING[:2]) in text
    assert f"a {czech(PIQUASSO_SAMPLING[2].mean_photons, 2)} proti teoretickým 16" in text
    assert f"s hodnotou {FAILING_MEASUREMENT_CUTOFF} skončí" in text
    assert len(sampling_markdown().splitlines()[2:]) == len(PIQUASSO_SAMPLING)


def test_velikost_fockova_prostoru_v_textu_sedi():
    amplitudes = comb(16 + 4, 4)
    text = text_of(SIMULATORS_TOPIC)

    assert f"celkem {czech(amplitudes, 0)} amplitud" in text
    assert f"{czech(amplitudes, 0)}² ≈ {czech(amplitudes**2 / 1e6, 1)} milionu" in text
    assert any(czech(amplitudes, 0) in finding.text for finding in KEY_FINDINGS)


def test_cisla_o_qubitech_a_vlq_odpovidaji_ulozenym_vysledkum():
    first, second = QISKIT_NATIVE_GATE_COUNTS
    text = text_of(QUBITS_TOPIC)
    guide = " ".join(QISKIT.explanation.split())
    error_free = OPERATIONS_PER_CZ_ON_STAR * first.cz * log10(ASSUMED_GATE_FIDELITY)

    assert (first.problem_key, second.problem_key) == ("extremni-moment", "spolecny-extrem")
    assert abs(DUAL_RAIL_CNOT_SUCCESS - 2 / 27) < 1e-4 and "pravděpodobností 0,0741, tedy 2/27" in text
    assert f"{(2 / 27) ** TWO_QUBIT_GATES_EXAMPLE:.0e}" == "5e-12" and "pravděpodobností 5 · 10⁻¹²" in text
    assert f"úlohy 1 je to {czech(first.cz, 0)} bran CZ" in text and f"na 10 qubitech {czech(second.cz, 0)}" in text
    assert f"jen {first.state_preparation_cz} bran CZ" in text
    assert f"{czech(first.cz, 0)} bran CZ u úlohy 1 a {czech(second.cz, 0)} u úlohy 2" in guide
    assert round(error_free) == -220 and "asi 10⁻²²⁰" in text
    assert first.cz >= (4**8 - 3 * 8 - 1) / 4 and second.cz >= (4**10 - 3 * 10 - 1) / 4
    assert len(gate_counts_markdown().splitlines()[2:]) == len(QISKIT_NATIVE_GATE_COUNTS)


def test_ulozene_hodnoty_vytvori_piquasso_znovu():
    """Runs only where Piquasso is installed (Python 3.10 or newer); the app does not depend on it."""
    pq = pytest.importorskip("piquasso")
    stored = next(stored for stored in PIQUASSO_PROBABILITIES if stored.problem_key == SAMPLED_PROBLEM)
    problem = find_benchmark(SAMPLED_PROBLEM).problem
    encoding = tune_encoding(problem.covariance, problem.exponents, TuningMode.PER_MODE)
    with pq.Program() as program:
        for mode, squeezing in enumerate(encoding.squeezing):
            pq.Q(mode) | pq.Squeezing(float(squeezing))
        pq.Q(0, 1) | pq.Interferometer(np.asarray(encoding.interferometer))
    state = pq.GaussianSimulator(d=2).execute(program).state

    assert state.get_particle_detection_probability(occupation_number=np.array([8, 8])) == pytest.approx(
        stored.probability, rel=1e-12
    )
    assert pq.Config().measurement_cutoff == PIQUASSO_SAMPLING[0].measurement_cutoff
