from math import prod

import numpy as np
import pytest

from gbs.boson_sampling import permanent
from gbs.gaussian_moments import moment_table
from gbs.hafnian import hafnian
from ui import ids
from ui.hafnian_content import (
    BUYERS_DETERMINANT,
    BUYERS_PERMANENT,
    COMPATIBILITY,
    DATA_ASSET_LABELS,
    FIT,
    FOUR_REGIONS_MOMENT,
    HAFNIAN_CODE,
    KEY_FINDINGS,
    MARKETS_TOPIC,
    PAIRING_TOPIC,
    PERMANENT_CODE,
    PRAGUE_BRNO_MOMENT,
    REGION_CORRELATIONS,
    ROOMMATES_HAFNIAN,
    SOURCES_ANCHOR,
    TOPICS,
)
from ui.hafnian_page import (
    RELATED_PAGES,
    build_hafnian_page,
    data_moments,
    double_factorial,
    solution_counts_markdown,
)
from ui.navigation import ACTIVE_LINK_CLASS, HAFNIAN_PATH, NAV_LINK_IDS, PAGE_BY_PATH, PAGE_IDS, show_page
from ui.theory_content import all_sources
from ui.topic_catalog import breadcrumb_trail

SECONDS_PER_YEAR = 365.25 * 24 * 3600
PAIRINGS_PER_SECOND = 1e9


def run_listing(code):
    namespace = {}
    exec(code, namespace)  # the listings are shown on the page, so the test runs exactly what the reader sees
    return namespace


def czech_latex(value):
    return f"{value:.2f}".replace(".", "{,}")


def test_hafnian_je_podstrankou_monte_carla_na_gbs():
    link_classes = show_page(HAFNIAN_PATH)[len(PAGE_IDS):len(PAGE_IDS) + len(NAV_LINK_IDS)]
    active = [link_id for link_id, link_class in zip(NAV_LINK_IDS, link_classes) if link_class == ACTIVE_LINK_CLASS]

    assert PAGE_BY_PATH[HAFNIAN_PATH] == ids.HAFNIAN_PAGE
    assert active == [ids.NAV_MONTE_CARLO_LINK, ids.NAV_GBS_LINK]
    assert [label for label, _ in breadcrumb_trail(ids.HAFNIAN_PAGE)][-2:] == [
        "2 · Monte Carlo na GBS", "Hafnián a permanent polopatě",
    ]


def test_kapitoly_maji_unikatni_kotvy_a_kazdy_zdroj_odkaz():
    anchors = [topic.anchor for topic in TOPICS]
    page = build_hafnian_page()
    section_ids = [child.id for child in page.children if getattr(child, "id", None)]
    sources = all_sources(TOPICS)

    assert section_ids == anchors + [SOURCES_ANCHOR]
    assert all(anchor.startswith("hafnian-") for anchor in section_ids)
    assert {finding.anchor for finding in KEY_FINDINGS} | set(RELATED_PAGES) <= set(anchors)
    assert all("](http" in source.citation for source in sources)
    assert len(sources) == len(set(sources))


def test_priklady_spolubydlicich_a_kupcu_odpovidaji_vypoctu():
    assert hafnian(np.array(COMPATIBILITY, dtype=float)) == ROOMMATES_HAFNIAN
    assert permanent(np.array(FIT, dtype=float)) == pytest.approx(BUYERS_PERMANENT)
    assert np.linalg.det(np.array(FIT, dtype=float)) == pytest.approx(BUYERS_DETERMINANT)
    assert "6 + 4 + 2 = 12" in PAIRING_TOPIC.explanation


def test_kod_na_strance_pocita_stejne_jako_knihovna_aplikace():
    listings = {**run_listing(PERMANENT_CODE), **run_listing(HAFNIAN_CODE)}
    rng = np.random.default_rng(3)
    square = rng.uniform(-1, 1, (4, 4))
    symmetric = rng.uniform(-1, 1, (6, 6))
    symmetric = (symmetric + symmetric.T) / 2

    assert listings["permanent"](FIT) == BUYERS_PERMANENT
    assert listings["hafnian"](COMPATIBILITY) == ROOMMATES_HAFNIAN
    assert listings["permanent"](square.tolist()) == pytest.approx(permanent(square))
    assert listings["hafnian"](symmetric.tolist()) == pytest.approx(hafnian(symmetric))
    assert listings["hafnian"]([[0, 1, 1], [1, 0, 1], [1, 1, 0]]) == 0


def test_permanent_je_hafnian_bipartitni_matice():
    listings = run_listing(HAFNIAN_CODE)
    square = np.random.default_rng(5).uniform(-1, 1, (4, 4))
    bipartite = np.block([[np.zeros((4, 4)), square], [square.T, np.zeros((4, 4))]])
    pairings = list(listings["dvojice"](list(range(8))))
    nonzero = [pairing for pairing in pairings if prod(bipartite[a, b] for a, b in pairing) != 0]

    assert hafnian(bipartite) == pytest.approx(permanent(square))
    assert (len(pairings), len(nonzero)) == (105, 24)


def test_cisla_trhu_s_byty_odpovidaji_wickove_vete():
    correlations = np.array(REGION_CORRELATIONS)
    moments = moment_table(correlations, [4, 2, 1, 1])

    assert np.all(np.linalg.eigvalsh(correlations) > 0)
    assert czech_latex(moments[1, 1, 1, 1]) == FOUR_REGIONS_MOMENT
    assert czech_latex(moments[2, 2, 0, 0]) == PRAGUE_BRNO_MOMENT
    assert moments[4, 0, 0, 0] == pytest.approx(3)
    assert FOUR_REGIONS_MOMENT in MARKETS_TOPIC.explanation and PRAGUE_BRNO_MOMENT in MARKETS_TOPIC.explanation


def test_pocty_reseni_a_doba_hrube_sily():
    rows = solution_counts_markdown().splitlines()

    assert rows[2] == "| 2 | 2 | 4 | 3 |"
    assert rows[-1].startswith("| 20 | 2 432 902 008 176 640 000 | 40 |")
    years = double_factorial(39) / PAIRINGS_PER_SECOND / SECONDS_PER_YEAR
    assert 5e6 < years < 2e7


def test_data_maji_tlustsi_chvosty_nez_gaussovsky_model():
    moments = {label.split(":")[0]: (gaussian, sample) for label, gaussian, sample in data_moments()}

    assert all(moments[label][0] == pytest.approx(3) for label in DATA_ASSET_LABELS.values())
    assert abs(moments["akcie"][1] - 3) < 0.2
    assert 4.5 < moments["zlato"][1] / 3 < 5
    assert moments["státní dluhopisy"][1] > 3.5 and moments["nemovitosti"][1] > 3.5
    gaussian, sample = moments["akcie a nemovitosti"]
    assert sample > 1.3 * gaussian
