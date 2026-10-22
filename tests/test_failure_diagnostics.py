from dash import dcc

from ui import ids
from ui.failure_diagnostics_content import (
    ESTIMATOR_SOURCE,
    INPUT_SOURCE,
    SOURCES_ANCHOR,
    TOPICS,
    failure_sources_table,
)
from ui.failure_diagnostics_page import DETAIL_LINKS, build_failure_diagnostics_page
from ui.knowledge_map_content import LAYERS, Layer
from ui.navigation import FAILURE_DIAGNOSTICS_PATH, RANDOM_MATRIX_GBS_PATH, RANDOM_MATRIX_PATH
from ui.random_matrix_content import LAB_ANCHOR
from ui.random_matrix_gbs_content import FIRST_STUDY
from ui.random_matrix_gbs_page import build_random_matrix_gbs_page
from ui.random_matrix_page import build_random_matrix_page
from ui.topic_catalog import RESEARCH_DIRECTIONS_TOPIC, breadcrumb_trail, study_path
from tests.test_random_matrix_page import section_ids
from tests.test_topics import active_links, visible_pages


def link_with_id(component, component_id):
    if isinstance(component, dcc.Link) and getattr(component, "id", None) == component_id:
        return component
    children = getattr(component, "children", None)
    for child in children if isinstance(children, list) else [children]:
        if child is not None and not isinstance(child, str):
            found = link_with_id(child, component_id)
            if found is not None:
                return found
    return None


def test_vyzkumne_smery_zacinaji_strankou_o_selhani_gbs():
    assert visible_pages(FAILURE_DIAGNOSTICS_PATH) == [ids.FAILURE_DIAGNOSTICS_PAGE]
    assert active_links(FAILURE_DIAGNOSTICS_PATH) == [ids.NAV_RESEARCH_MENU]
    research = next(info for info in LAYERS if info.layer == Layer.RESEARCH)
    assert research.page_ids[0] == ids.FAILURE_DIAGNOSTICS_PAGE
    assert [page.page_id for page in study_path(RESEARCH_DIRECTIONS_TOPIC)] == [
        ids.FAILURE_DIAGNOSTICS_PAGE, ids.RANDOM_MATRIX_GBS_PAGE,
    ]


def test_stranka_nahodne_matice_a_gbs_je_podstrankou_diagnostiky():
    assert [label for label, _ in breadcrumb_trail(ids.RANDOM_MATRIX_GBS_PAGE)] == [
        "Témata", "Vlastní výzkum", "Kdy odhad rizika přes GBS selže", "Náhodné matice a GBS: hypotéza",
    ]
    assert breadcrumb_trail(ids.RANDOM_MATRIX_GBS_PAGE)[2][1] == FAILURE_DIAGNOSTICS_PATH


def test_kazda_kapitola_ma_unikatni_kotvu_shrnuti_vyklad_a_zdroj():
    anchors = [topic.anchor for topic in TOPICS]

    assert set(anchors + [SOURCES_ANCHOR]) <= set(section_ids(build_failure_diagnostics_page()))
    assert len(set(anchors)) == len(anchors)
    assert all(anchor.startswith("ds-") for anchor in anchors)
    for topic in TOPICS:
        assert topic.in_short.strip() and topic.explanation.strip() and topic.further_reading


def test_odkazy_na_podrobny_rozbor_vedou_na_existujici_kotvy():
    assert DETAIL_LINKS[ESTIMATOR_SOURCE.anchor][1] == f"{RANDOM_MATRIX_GBS_PATH}#{FIRST_STUDY.anchor}"
    assert DETAIL_LINKS[INPUT_SOURCE.anchor][1] == f"{RANDOM_MATRIX_PATH}#{LAB_ANCHOR}"
    assert FIRST_STUDY.anchor in set(section_ids(build_random_matrix_gbs_page()))
    assert LAB_ANCHOR in set(section_ids(build_random_matrix_page()))


def test_tabulka_ma_tri_zdroje_chyby_a_odkazuje_na_kapitoly():
    rows = [row for row in failure_sources_table().splitlines() if row.startswith("| ") and row[2].isdigit()]

    assert [row[2] for row in rows] == ["1", "2", "3"]
    assert "kapitoly 2 a 3" in rows[0] and "kapitola 4" in rows[1] and "kapitola 5" in rows[2]
    assert [topic.anchor for topic in TOPICS][1:5] == ["ds-data", "ds-nastroje", "ds-vyhoda", "ds-vstup"]


def test_cisla_v_textech_odpovidaji_vypoctu():
    assert "ušetří 5,1× vzorků" in ESTIMATOR_SOURCE.explanation
    assert "(0,82×)" in ESTIMATOR_SOURCE.explanation
    assert "22× víc vzorků" in ESTIMATOR_SOURCE.explanation
    assert "16× menší" in INPUT_SOURCE.explanation
