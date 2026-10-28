import math

import numpy as np
import pytest

from ui.generated_topics import GENERATED_TOPICS, generated_page_id, generated_path
from ui.knowledge_map_content import RELATIONS
from ui.photonics_landscape_content import TOPICS as PHOTONICS_TOPICS
from ui.primer_chapter1_content import SECTION_1_1
from ui.topic_catalog import breadcrumb_trail

SLUG = "co-je-kvantovy-mod-a-zebrikove-operatory"


def topic_text() -> str:
    topic = next(topic for topic in GENERATED_TOPICS if topic.slug == SLUG)
    return " ".join([topic.in_short, *(section.body for section in topic.sections)])


def czech_latex(value: float, digits: int) -> str:
    return f"{value:.{digits}f}".replace(".", "{,}")


def annihilation(levels: int) -> np.ndarray:
    """The annihilation operator on the Fock states |0⟩ … |levels − 1⟩."""
    return np.diag(np.sqrt(np.arange(1, levels)), 1)


def squeezed_vacuum(z: complex, levels: int = 120) -> np.ndarray:
    """S(z)|0⟩ with S(z) from definition 1.2.6 of the primer, the matrix exponential through eigenvectors."""
    a = annihilation(levels).astype(complex)
    generator = 0.5 * (np.conj(z) * a @ a - z * a.conj().T @ a.conj().T)
    eigenvalues, vectors = np.linalg.eigh(1j * generator)
    return (vectors @ np.diag(np.exp(-1j * eigenvalues)) @ vectors.conj().T)[:, 0]


def test_cisla_na_strance_o_kvantovem_modu_odpovidaji_vypoctu():
    text = topic_text()
    a = annihilation(4)

    assert np.allclose(np.diag(a.T @ a), [0, 1, 2, 3])
    assert r"\operatorname{diag}(0, 1, 2, 3)" in text
    assert np.allclose(np.diag(a @ a.T - a.T @ a), [1, 1, 1, -3])
    assert r"\operatorname{diag}(1, 1, 1, -3)" in text
    assert np.linalg.matrix_power(a.T, 3)[3, 0] == pytest.approx(math.sqrt(math.factorial(3)))
    assert r"= \sqrt{6}\, |3\rangle" in text

    beam_splitter = np.array([[1, 1], [1, -1]]) / math.sqrt(2)
    assert beam_splitter[0, 0] * beam_splitter[1, 1] + beam_splitter[0, 1] * beam_splitter[1, 0] == pytest.approx(0)

    probabilities = np.abs(squeezed_vacuum(1.0)) ** 2
    assert probabilities[0] == pytest.approx(1 / math.cosh(1))
    for photons in (0, 2, 4):
        assert f"P({photons}) " in text and czech_latex(probabilities[photons], 3) in text
    assert np.allclose(probabilities[1::2], 0)
    assert f"asi {round(100 * probabilities[6:].sum())} % připadá na šest a více fotonů" in text
    assert (np.arange(len(probabilities)) * probabilities).sum() == pytest.approx(math.sinh(1) ** 2)
    assert rf"\sinh^2 1 \approx {czech_latex(math.sinh(1) ** 2, 2)}" in text

    amplitudes = 11 ** 20
    mantissa, exponent = f"{amplitudes:.1e}".split("e+")
    assert rf"11^{{20}} \approx {mantissa.replace('.', '{,}')} \cdot 10^{{{int(exponent)}}}" in text
    assert 16 * amplitudes > 10 ** 22 and r"přes $10^{22}$ bajtů" in text
    assert f"$40 \\times 40$, tedy {(2 * 20) ** 2 // 1000} {(2 * 20) ** 2 % 1000:03d} čísel" in text


def test_stranka_o_kvantovem_modu_rozvadi_skripta_1_a_vedou_na_ni_odkazy():
    page_id = generated_page_id(SLUG)
    link = f"]({generated_path(SLUG)})"

    assert [label for label, _ in breadcrumb_trail(page_id)] == [
        "Témata", "Fotonika a GBS", "Skripta 1: Základy fotonického kvantového počítání",
        "Co je kvantový mód a jak po něm chodí žebříkové operátory",
    ]
    assert any(relation.source == page_id and relation.target == "primer-basics-page" for relation in RELATIONS)
    assert link in SECTION_1_1.body
    assert link in next(topic.explanation for topic in PHOTONICS_TOPICS if topic.anchor == "svet-pojmy")
