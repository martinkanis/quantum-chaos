from functools import reduce
from itertools import product
from math import ceil, log, sqrt

import numpy as np
import pytest

from ui import ids
from ui.ghz_states_content import (
    BLUEPRINT_SLIDES,
    EXPERIMENT_TOPIC,
    HISTORY_TOPIC,
    KEY_FINDINGS,
    SOURCES_ANCHOR,
    TODAY_TOPIC,
    TOPICS,
    WHAT_TOPIC,
    WHY_THREE_TOPIC,
)
from ui.ghz_states_page import build_ghz_states_page
from ui.navigation import GHZ_STATES_PATH, PAGE_BY_PATH
from ui.study_progress import describe_pager
from ui.theory_content import all_sources
from ui.topic_catalog import breadcrumb_trail
from ui.walther_lecture_content import SLIDES

ZERO, ONE = np.array([1, 0]), np.array([0, 1])
PLUS = (ZERO + ONE) / sqrt(2)
I2 = np.eye(2)
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.diag([1, -1])
H = np.array([[1, 1], [1, -1]]) / sqrt(2)
CZ = np.diag([1, 1, 1, -1])


def kron(*factors):
    return reduce(np.kron, factors)


def ghz(qubits):
    return (kron(*[ZERO] * qubits) + kron(*[ONE] * qubits)) / sqrt(2)


def text_of(topic) -> str:
    return " ".join((topic.in_short + " " + topic.explanation).split())


def test_stranka_je_podstrankou_prednasky_a_poslednim_krokem_fotoniky():
    _, step_label, _, _, _ = describe_pager(GHZ_STATES_PATH, None)

    assert PAGE_BY_PATH[GHZ_STATES_PATH] == ids.GHZ_STATES_PAGE
    assert step_label == "Fotonika · krok 10 / 10"
    assert [label for label, _ in breadcrumb_trail(ids.GHZ_STATES_PAGE)][-2].startswith("Přednáška")


def test_kapitoly_maji_unikatni_kotvy_zdroje_a_slajdy_z_prednasky():
    page = build_ghz_states_page()
    section_ids = [child.id for child in page.children if getattr(child, "id", None)]
    sources = all_sources(TOPICS)

    assert section_ids == [topic.anchor for topic in TOPICS] + [SOURCES_ANCHOR]
    assert all(anchor.startswith("ghz-") for anchor in section_ids)
    assert {finding.anchor for finding in KEY_FINDINGS} <= set(section_ids)
    assert len(sources) == len(set(sources))
    assert set(BLUEPRINT_SLIDES) <= {slide.file_name for slide in SLIDES}


def test_merminova_tabulka_odpovida_vlastnim_cislum():
    state = ghz(3)
    expected = [((X, Y, Y), -1), ((Y, X, Y), -1), ((Y, Y, X), -1), ((X, X, X), 1)]

    for operators, eigenvalue in expected:
        assert np.allclose(kron(*operators) @ state, eigenvalue * state)
    assert "| $X$, $X$, $X$ | $+1$ |" in HISTORY_TOPIC.explanation


def test_lokalni_realismus_predpovida_pro_xxx_opacne_znamenko():
    for x1, x2, x3, y1, y2, y3 in product((1, -1), repeat=6):
        assert (x1 * y2 * y3) * (y1 * x2 * y3) * (y1 * y2 * x3) == x1 * x2 * x3
    assert "x_1 x_2 x_3 = -1" in text_of(HISTORY_TOPIC)


def test_ghz_je_az_na_hadamardy_linearni_klastr_ze_tri_qubitu():
    cluster = kron(CZ, I2) @ kron(I2, CZ) @ kron(PLUS, PLUS, PLUS)

    assert abs(np.vdot(ghz(3), kron(H, I2, H) @ cluster)) ** 2 == pytest.approx(1)
    assert r"(H \otimes I \otimes H)" in text_of(WHAT_TOPIC)


def test_dvoupar_s_polarizacnim_delicem_dava_ghz_s_pravdepodobnosti_ctvrtina():
    bell = (kron(ZERO, ZERO) + kron(ONE, ONE)) / sqrt(2)
    pairs = kron(bell, bell).reshape(2, 2, 2, 2)  # photons a, b, c, d
    same_polarization = np.zeros((2, 2))
    np.fill_diagonal(same_polarization, 1)
    after_splitter = pairs * same_polarization[None, :, :, None]  # b and c leave by different outputs
    parity_probability = np.sum(np.abs(after_splitter) ** 2)
    four = after_splitter / sqrt(parity_probability)
    diagonal = np.einsum("abcd,b->acd", four, PLUS.conj())
    trigger_probability = np.sum(np.abs(diagonal) ** 2)
    three = diagonal.reshape(8) / sqrt(trigger_probability)

    assert np.allclose(four.reshape(16), ghz(4))
    assert parity_probability == pytest.approx(1 / 2)
    assert trigger_probability == pytest.approx(1 / 2)
    assert abs(np.vdot(ghz(3), three)) ** 2 == pytest.approx(1)
    assert "s pravděpodobností $1/2$ a stav čtyř fotonů" in text_of(EXPERIMENT_TOPIC)


def test_fuze_dvou_ghz_stavu_da_ctyrfotonovy_ghz_pro_kazdy_bellovy_vysledek():
    bells = [
        (kron(ZERO, ZERO) + kron(ONE, ONE)) / sqrt(2),
        (kron(ZERO, ZERO) - kron(ONE, ONE)) / sqrt(2),
        (kron(ZERO, ONE) + kron(ONE, ZERO)) / sqrt(2),
        (kron(ZERO, ONE) - kron(ONE, ZERO)) / sqrt(2),
    ]
    corrections = [kron(I2, I2, *pair) for pair in product((I2, X, Z, Z @ X), repeat=2)]
    two_ghz = kron(ghz(3), ghz(3)).reshape(2, 2, 2, 2, 2, 2)

    for bell in bells:
        rest = np.einsum("abcdef,cd->abef", two_ghz, bell.reshape(2, 2).conj()).reshape(16)
        probability = np.vdot(rest, rest).real
        remaining = rest / sqrt(probability)
        assert probability == pytest.approx(1 / 4)
        assert max(abs(np.vdot(ghz(4), fix @ remaining)) ** 2 for fix in corrections) == pytest.approx(1)
    assert "$3 + 3 - 2 = 4$" in text_of(WHY_THREE_TOPIC)
    assert "$2 + 2 - 2 = 2$" in text_of(WHY_THREE_TOPIC)


def test_multiplexovani_ohlasovanych_ghz_v_textu_sedi_s_vypoctem():
    success = 1 / 32
    generators = ceil(log(1 - 0.99) / log(1 - success))

    assert generators == 146
    assert 1 - (1 - success) ** generators >= 0.99 > 1 - (1 - success) ** (generators - 1)
    assert "$N = 146$ generátorů, tedy 876 jednotlivých fotonů" in text_of(TODAY_TOPIC)
    assert generators * 6 == 876
