from math import comb, exp, sqrt

import numpy as np
import pytest

from gbs.gaussian_moments import moment_table
from ui import ids
from ui.andersen_shan_paper_content import (
    COEFFICIENT_COUNT_EXAMPLE,
    CONDITION_TOPIC,
    COSH_EXPECTATION,
    DENSITY_TOPIC,
    EXAMPLE_COVARIANCE,
    EXAMPLE_FOURTH_ORDER_MOMENT,
    EXAMPLE_PORTFOLIO_SECOND_MOMENT,
    EXAMPLE_WEIGHTS,
    KEY_FINDINGS,
    POLYNOMIAL_TOPIC,
    SOURCES_ANCHOR,
    TOPICS,
)
from ui.andersen_shan_paper_page import (
    RELATED_PAGES,
    SERIES_TERMS,
    build_andersen_shan_paper_page,
    coefficient_count,
    coefficient_count_markdown,
    format_integer,
    term_by_term_sums,
)
from ui.navigation import (
    ACTIVE_LINK_CLASS,
    ANDERSEN_SHAN_PAPER_PATH,
    NAV_LINK_IDS,
    PAGE_BY_PATH,
    PAGE_IDS,
    show_page,
)
from ui.theory_content import all_sources
from ui.topic_catalog import breadcrumb_trail

COVARIANCE = np.array(EXAMPLE_COVARIANCE)


def czech_latex(value: float, digits: int) -> str:
    return f"{value:.{digits}f}".replace(".", "{,}")


def test_clanek_je_podstrankou_vyhody_gbs():
    link_classes = show_page(ANDERSEN_SHAN_PAPER_PATH)[len(PAGE_IDS):len(PAGE_IDS) + len(NAV_LINK_IDS)]
    active = [link_id for link_id, link_class in zip(NAV_LINK_IDS, link_classes) if link_class == ACTIVE_LINK_CLASS]

    assert PAGE_BY_PATH[ANDERSEN_SHAN_PAPER_PATH] == ids.ANDERSEN_SHAN_PAPER_PAGE
    assert active == [ids.NAV_CORE_MENU]
    assert [label for label, _ in breadcrumb_trail(ids.ANDERSEN_SHAN_PAPER_PAGE)][-2:] == [
        "3 · Výhoda GBS", "Článek Andersena a Shan krok za krokem",
    ]


def test_kapitoly_maji_unikatni_kotvy_a_kazdy_zdroj_odkaz():
    anchors = [topic.anchor for topic in TOPICS]
    page = build_andersen_shan_paper_page()
    section_ids = [child.id for child in page.children if getattr(child, "id", None)]
    sources = all_sources(TOPICS)

    assert section_ids == anchors + [SOURCES_ANCHOR]
    assert all(anchor.startswith("clanek-") for anchor in section_ids)
    assert {finding.anchor for finding in KEY_FINDINGS} | set(RELATED_PAGES) <= set(anchors)
    assert all("](http" in source.citation for source in sources)
    assert len(sources) == len(set(sources))


def test_pocet_koeficientu_v_textu_odpovida_kombinacnimu_cislu():
    assert coefficient_count(2, 2) == 6
    assert format_integer(coefficient_count(20, 8)) == COEFFICIENT_COUNT_EXAMPLE == "3 108 105"
    assert COEFFICIENT_COUNT_EXAMPLE in POLYNOMIAL_TOPIC.explanation
    assert coefficient_count_markdown().splitlines()[2] == "| 2 | 6 | 15 | 45 | 153 |"
    assert comb(36, 16) == coefficient_count(20, 16)


def test_priklady_v_textu_odpovidaji_momentum_normalniho_rozdeleni():
    moments = moment_table(COVARIANCE, [2, 2])
    weights = np.array(EXAMPLE_WEIGHTS)

    assert czech_latex(moments[2, 2], 3) == EXAMPLE_FOURTH_ORDER_MOMENT
    assert czech_latex(weights @ COVARIANCE @ weights, 2) == EXAMPLE_PORTFOLIO_SECOND_MOMENT
    assert EXAMPLE_FOURTH_ORDER_MOMENT in CONDITION_TOPIC.explanation
    assert EXAMPLE_PORTFOLIO_SECOND_MOMENT in CONDITION_TOPIC.explanation
    assert "0{,}36" in POLYNOMIAL_TOPIC.explanation and "0{,}48" in POLYNOMIAL_TOPIC.explanation
    assert (weights[0] ** 2, 2 * weights[0] * weights[1], weights[1] ** 2) == pytest.approx((0.36, 0.48, 0.16))
    np.testing.assert_allclose(np.linalg.eigvalsh(COVARIANCE), [0.25, 0.75])
    assert "0,75" in DENSITY_TOPIC.explanation


def test_rada_pro_cosh_konverguje_k_odmocnine_z_e_a_rada_pro_exp_x2_diverguje():
    rows = term_by_term_sums()
    _, _, cosh_sum, _, square_exp_sum = rows[-1]

    assert len(rows) == SERIES_TERMS
    assert [row[1] for row in rows[:3]] == pytest.approx([1, 0.5, 0.125])
    assert cosh_sum == pytest.approx(exp(0.5), rel=1e-9)
    assert czech_latex(exp(0.5), 3) == COSH_EXPECTATION
    assert square_exp_sum > 200
    assert [row[3] for row in rows[:4]] == pytest.approx([1, 1, 1.5, 2.5])


def test_sude_momenty_normovane_normalni_veliciny_jsou_dvojite_faktorialy():
    moments = moment_table(np.array([[1.0]]), [8])

    assert list(moments[::2]) == pytest.approx([1, 1, 3, 15, 105])
    assert list(moments[1::2]) == pytest.approx([0, 0, 0, 0])
    assert sqrt(2 * np.pi) == pytest.approx(2.5066, abs=1e-4)
