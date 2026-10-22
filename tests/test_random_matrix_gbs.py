import numpy as np
import pytest

from gbs.expectation import MomentProblem, gbs_error_breakdown, gbs_relative_error_constant
from gbs.sampler import program_from_covariance
from gbs.spectrum_study import equal_weights, equicorrelated, long_short_weights, spectrum_savings
from ui import ids
from ui.gbs_page import squeezing_strength_grid
from ui.navigation import RANDOM_MATRIX_GBS_PATH
from ui.random_matrix_gbs_content import (
    EQUAL_SAVINGS,
    IN_SHORT,
    LONG_SHORT_DEGREE,
    LONG_SHORT_SAVINGS,
    NOISE_EXAMPLE_MOMENT_RATIO,
    NOISY_INPUT,
    SINGULAR_CORRELATION,
    SINGULAR_MISMATCH,
    SINGULAR_STRENGTH,
    SOURCES_ANCHOR,
    STUDY_ASSET_COUNT,
    STUDY_CORRELATIONS,
    STUDY_DEGREES,
    TOPICS,
    saving_label,
    savings_table,
    study_findings,
    times_more_samples,
)
from ui.random_matrix_gbs_page import build_random_matrix_gbs_page
from ui.theory_content import all_sources
from ui.topic_catalog import RESEARCH_DIRECTIONS_TOPIC, RESEARCH_TOPICS, breadcrumb_trail
from tests.test_random_matrix_page import section_ids
from tests.test_topics import active_links, visible_pages


def test_vyzkumne_smery_jsou_samostatnym_tematem_v_horni_liste():
    assert visible_pages(RANDOM_MATRIX_GBS_PATH) == [ids.RANDOM_MATRIX_GBS_PAGE]
    assert active_links(RANDOM_MATRIX_GBS_PATH) == [ids.NAV_RESEARCH_MENU]
    assert RESEARCH_DIRECTIONS_TOPIC in RESEARCH_TOPICS
    assert [label for label, _ in breadcrumb_trail(ids.RANDOM_MATRIX_GBS_PAGE)][:2] == [
        "Témata", "Vlastní výzkum",
    ]


def test_kazda_kapitola_ma_unikatni_kotvu_shrnuti_vyklad_a_zdroj():
    anchors = [topic.anchor for topic in TOPICS]

    assert set(anchors + [SOURCES_ANCHOR]) <= set(section_ids(build_random_matrix_gbs_page()))
    assert len(set(anchors)) == len(anchors)
    assert all(anchor.startswith("vs-") for anchor in anchors)
    for topic in TOPICS:
        assert topic.in_short.strip() and topic.explanation.strip() and topic.further_reading
    assert len(all_sources(TOPICS)) == len(set(all_sources(TOPICS)))


def test_matice_se_spolecnou_korelaci_ma_trzni_mod_a_stejna_vlastni_cisla_sumu():
    eigenvalues = np.linalg.eigvalsh(equicorrelated(6, 0.5))

    assert eigenvalues == pytest.approx([0.5] * 5 + [3.5])


def test_rovnomerne_portfolio_lezi_ve_smeru_trzniho_modu_a_long_short_je_na_nej_kolme():
    market_mode = np.linalg.eigh(equicorrelated(6, 0.3))[1][:, -1]

    assert abs(equal_weights(6) @ market_mode) == pytest.approx(np.linalg.norm(equal_weights(6)))
    assert long_short_weights(6) @ market_mode == pytest.approx(0)


@pytest.mark.parametrize("weights", [np.array([0.4, 0.3, 0.2, 0.1]), np.array([0.4, -0.3, 0.2, -0.1])])
def test_rozklad_chyby_dava_stejnou_konstantu_jako_puvodni_vzorec(weights):
    covariance = equicorrelated(4, 0.3)
    problem = MomentProblem(covariance=covariance, weights=weights, degree=4)
    program = program_from_covariance(covariance, 0.8)
    breakdown = gbs_error_breakdown(problem, program)

    assert breakdown.relative_error_constant == pytest.approx(gbs_relative_error_constant(problem, program))
    assert breakdown.cancellation >= 1 - 1e-12
    assert breakdown.pattern_mismatch >= breakdown.cancellation ** 2 - 1e-12


@pytest.mark.parametrize("stored, weights, degrees", [
    (EQUAL_SAVINGS, equal_weights(STUDY_ASSET_COUNT), STUDY_DEGREES),
    (LONG_SHORT_SAVINGS, long_short_weights(STUDY_ASSET_COUNT), (LONG_SHORT_DEGREE,)),
])
def test_ulozene_tabulky_uspor_odpovidaji_vypoctu(stored, weights, degrees):
    computed = spectrum_savings(weights, STUDY_CORRELATIONS, degrees, squeezing_strength_grid())

    assert len(computed) == len(stored)
    for fresh, kept in zip(computed, stored):
        assert (fresh.correlation, fresh.degree, fresh.best_strength) == (kept.correlation, kept.degree, kept.best_strength)
        assert fresh.market_mode_share == pytest.approx(kept.market_mode_share, abs=1e-4)
        assert fresh.useful_shot_share == pytest.approx(kept.useful_shot_share, abs=1e-4)
        for field in ("sample_saving", "pattern_mismatch", "cancellation"):
            assert getattr(fresh, field) == pytest.approx(getattr(kept, field), rel=1e-3)


def test_nezavisla_aktiva_jsou_vyjimecny_bod():
    weights = equal_weights(STUDY_ASSET_COUNT)

    def mismatch(correlation):
        covariance = equicorrelated(STUDY_ASSET_COUNT, correlation)
        problem = MomentProblem(covariance=covariance, weights=weights, degree=4)
        return gbs_error_breakdown(problem, program_from_covariance(covariance, SINGULAR_STRENGTH)).pattern_mismatch

    assert mismatch(SINGULAR_CORRELATION) == pytest.approx(SINGULAR_MISMATCH, rel=1e-3)
    assert mismatch(SINGULAR_CORRELATION) > 10 * mismatch(0.0)


def test_uspory_se_zobrazi_cesky_i_kdyz_jsou_mensi_nez_jedna():
    assert saving_label(8.991) == "9,0×"
    assert saving_label(0.8161) == "0,82×"
    assert saving_label(0.04467) == "0,045×"
    assert saving_label(4.997e-07) == "5,0·10⁻⁷×"
    assert times_more_samples(0.04467) == "22"
    assert times_more_samples(0.001828) == "550"


def test_cisla_v_textech_odpovidaji_vypoctu():
    findings = study_findings()

    assert NOISE_EXAMPLE_MOMENT_RATIO == pytest.approx(1 / 16)
    assert "16× větší" in NOISY_INPUT.explanation
    assert "9,0× vzorků" in findings and "(0,82×)" in findings and "ustálí na 5,1×" in findings
    assert "potřebuje 22× víc vzorků" in findings and "asi 550× víc" in findings
    assert "$m$ = 1,2" in findings and "$m$ = 11" in findings and "kolem 16" in findings
    assert "jen 11 % výstřelů" in findings and "strop 5,1×" in findings and "7 % a 14,1×" in findings
    assert "9× větší než výsledek" in findings and "už 49×" in findings
    assert "ušetří 5,1× vzorků" in IN_SHORT and "potřebuje 22× víc" in IN_SHORT
    assert "| 0,02 | 18 % | 0,82× | 1,5× | 0,51× |" in savings_table()
    assert "| 0,90 | 92 % | 5,1× | 14,1× | 5,0·10⁻⁷× |" in savings_table()
