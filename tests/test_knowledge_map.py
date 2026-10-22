import pytest
from dash import no_update

from ui import ids
from ui.knowledge_map import (
    CENTER_ID,
    KnowledgeMapError,
    add_connection,
    build_figure,
    map_nodes,
    parse_connections,
    relations_of,
    remove_connections,
)
from ui.knowledge_map_callbacks import select_node
from ui.knowledge_map_content import LAYERS, RELATION_KINDS, RELATIONS, RelationKind
from ui.navigation import ACTIVE_LINK_CLASS, KNOWLEDGE_MAP_PATH, NAV_LINK_IDS, PAGE_IDS, show_page
from ui.topic_catalog import RESEARCH_TOPICS

ALL_LAYERS = [info.layer.value for info in LAYERS]
ALL_KINDS = [info.kind.value for info in RELATION_KINDS]


def test_kazda_stranka_temat_je_v_prave_jedne_vrstve_mapy():
    layer_pages = [page_id for info in LAYERS for page_id in info.page_ids]
    topic_pages = {page.page_id for topic in RESEARCH_TOPICS for page in topic.pages}

    assert len(layer_pages) == len(set(layer_pages))
    assert set(layer_pages) == topic_pages | {ids.ACADEMY_PAGE}


def test_vztahy_spojuji_ruzne_existujici_stranky_a_kazda_stranka_nejaky_ma():
    nodes = map_nodes()
    connected = {relation.source for relation in RELATIONS} | {relation.target for relation in RELATIONS}

    assert all(relation.source in nodes and relation.target in nodes for relation in RELATIONS)
    assert all(relation.source != relation.target for relation in RELATIONS)
    assert {page_id for info in LAYERS for page_id in info.page_ids} <= connected


def test_mapa_ma_vlastni_odkaz_v_horni_liste():
    link_classes = show_page(KNOWLEDGE_MAP_PATH)[len(PAGE_IDS):len(PAGE_IDS) + len(NAV_LINK_IDS)]
    active = [link_id for link_id, link_class in zip(NAV_LINK_IDS, link_classes) if link_class == ACTIVE_LINK_CLASS]

    assert active == [ids.NAV_KNOWLEDGE_MAP_LINK]


def test_filtry_skryji_vrstvy_i_druhy_vztahu():
    full = build_figure(ALL_LAYERS, ALL_KINDS, [])
    without_research = build_figure([layer for layer in ALL_LAYERS if layer != "vyzkum"], ALL_KINDS, [])
    only_follows = build_figure(ALL_LAYERS, [RelationKind.FOLLOWS.value], [])

    assert len(full.layout.annotations) == len(RELATIONS)
    assert len(without_research.layout.annotations) < len(full.layout.annotations)
    assert len(only_follows.layout.annotations) == sum(r.kind == RelationKind.FOLLOWS for r in RELATIONS)


def test_vlastni_propojeni_jde_pridat_odebrat_a_spatne_zadani_ma_ceskou_hlasku():
    stored = add_connection(None, ids.HAFNIAN_PAGE, "vysvetluje", ids.RANDOM_MATRIX_PAGE, "  spektrum a páry  ")

    assert stored == [{
        "source": ids.HAFNIAN_PAGE, "kind": "vysvetluje", "target": ids.RANDOM_MATRIX_PAGE, "note": "spektrum a páry",
    }]
    assert any(item.is_own for item in relations_of(ids.HAFNIAN_PAGE, parse_connections(stored)))
    assert len(build_figure(ALL_LAYERS, ALL_KINDS, parse_connections(stored)).layout.annotations) == len(RELATIONS) + 1
    assert remove_connections(stored, {0}) == []
    with pytest.raises(KnowledgeMapError, match="Takové propojení už máš"):
        add_connection(stored, ids.HAFNIAN_PAGE, "vysvetluje", ids.RANDOM_MATRIX_PAGE, "")
    with pytest.raises(KnowledgeMapError, match="samu se sebou"):
        add_connection(None, ids.HAFNIAN_PAGE, "vysvetluje", ids.HAFNIAN_PAGE, "")
    with pytest.raises(KnowledgeMapError, match="Vyber obě stránky"):
        add_connection(None, ids.HAFNIAN_PAGE, None, ids.GBS_PAGE, "")


def test_poskozena_ulozena_propojeni_se_preskoci():
    stored = [{"source": "neexistuje", "kind": "vysvetluje", "target": ids.GBS_PAGE}, {"kind": "zadny"}]

    assert parse_connections(stored) == []


def test_klik_vybere_jen_uzel():
    assert select_node({"points": [{"customdata": ids.GBS_PAGE}]}) == ids.GBS_PAGE
    assert select_node({"points": [{"customdata": CENTER_ID}]}) == CENTER_ID
    assert select_node({"points": [{"x": 0.5, "y": 0.5}]}) is no_update
