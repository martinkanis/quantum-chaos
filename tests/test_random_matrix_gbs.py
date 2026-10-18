import numpy as np
import pytest

from gbs.spectrum_study import equicorrelated, spectrum_savings
from ui import ids
from ui.gbs_page import squeezing_strength_grid
from ui.navigation import RANDOM_MATRIX_GBS_PATH
from ui.random_matrix_gbs_content import (
    NOISE_EXAMPLE_MOMENT_RATIO,
    NOISY_INPUT,
    SOURCES_ANCHOR,
    STUDY_ASSET_COUNT,
    STUDY_CORRELATIONS,
    STUDY_DEGREES,
    STUDY_SAVINGS,
    TOPICS,
    savings_table,
    study_findings,
)
from ui.random_matrix_gbs_page import build_random_matrix_gbs_page
from ui.theory_content import all_sources
from ui.topic_catalog import RESEARCH_DIRECTIONS_TOPIC, RESEARCH_TOPICS, breadcrumb_trail
from tests.test_random_matrix_page import section_ids
from tests.test_topics import active_links, visible_pages


def test_vyzkumne_smery_jsou_samostatnym_tematem_v_horni_liste():
    assert visible_pages(RANDOM_MATRIX_GBS_PATH) == [ids.RANDOM_MATRIX_GBS_PAGE]
    assert active_links(RANDOM_MATRIX_GBS_PATH) == [ids.NAV_RESEARCH_DIRECTIONS_LINK]
    assert RESEARCH_DIRECTIONS_TOPIC in RESEARCH_TOPICS
    assert [label for label, _ in breadcrumb_trail(ids.RANDOM_MATRIX_GBS_PAGE)][:2] == [
        "Témata", RESEARCH_DIRECTIONS_TOPIC.title,
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


def test_ulozena_tabulka_uspor_odpovida_vypoctu():
    computed = spectrum_savings(STUDY_ASSET_COUNT, STUDY_CORRELATIONS, STUDY_DEGREES, squeezing_strength_grid())

    assert len(computed) == len(STUDY_SAVINGS)
    for fresh, stored in zip(computed, STUDY_SAVINGS):
        assert (fresh.correlation, fresh.degree, fresh.best_strength) == (
            stored.correlation, stored.degree, stored.best_strength,
        )
        assert fresh.market_mode_share == pytest.approx(stored.market_mode_share, abs=1e-4)
        assert fresh.sample_saving == pytest.approx(stored.sample_saving, abs=1e-3)


def test_cisla_v_textech_odpovidaji_vypoctu():
    assert NOISE_EXAMPLE_MOMENT_RATIO == pytest.approx(1 / 16)
    assert "16× větší" in NOISY_INPUT.explanation
    assert "9,0× vzorků" in study_findings() and "na 2,2×" in study_findings() and "kolem 5,1×" in study_findings()
    assert "| 0,10 | 25 % | 2,2× | 5,7× |" in savings_table()
