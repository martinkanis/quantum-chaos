import base64
import json

import pytest
from dash import no_update

from ui import ids
from ui.knowledge_map import (
    CENTER_ID,
    build_elements,
    describe_hover,
    map_nodes,
    node_options,
    page_ids,
    positions_of,
    relations_of,
)
from ui.knowledge_map_callbacks import click_node, upload_backup
from ui.knowledge_map_content import LAYERS, RELATION_KINDS, RELATIONS, RelationKind
from ui.knowledge_map_notes import (
    KnowledgeMapError,
    add_connection,
    add_subtopic,
    export_backup,
    import_backup,
    parse_connections,
    parse_subtopics,
    remove_connections,
    remove_subtopics,
)
from ui.knowledge_map_page import ClickMode, describe_node
from ui.navigation import ACTIVE_LINK_CLASS, KNOWLEDGE_MAP_PATH, NAV_LINK_IDS, PAGE_IDS, show_page
from ui.topic_catalog import RESEARCH_TOPICS

ALL_LAYERS = [info.layer.value for info in LAYERS]
ALL_KINDS = [info.kind.value for info in RELATION_KINDS]
PAGES = page_ids()


def relation_edges(elements):
    return [item for item in elements if "relation" in item.get("classes", "")]


def encoded(backup):
    return "data:application/json;base64," + base64.b64encode(json.dumps(backup).encode("utf-8")).decode("ascii")


def test_kazda_stranka_temat_je_v_prave_jedne_skupine_mapy():
    topic_pages = {page.page_id for topic in RESEARCH_TOPICS for page in topic.pages}

    assert len(PAGES) == len(set(PAGES))
    assert set(PAGES) == topic_pages | {ids.ACADEMY_PAGE}


def test_vztahy_spojuji_ruzne_existujici_stranky_a_kazda_stranka_nejaky_ma():
    nodes = map_nodes()
    connected = {relation.source for relation in RELATIONS} | {relation.target for relation in RELATIONS}

    assert all(relation.source in nodes and relation.target in nodes for relation in RELATIONS)
    assert all(relation.source != relation.target for relation in RELATIONS)
    assert set(PAGES) <= connected


def test_mapa_je_na_uvodni_strance_a_stara_adresa_tam_vede():
    styles = show_page(KNOWLEDGE_MAP_PATH)
    link_classes = styles[len(PAGE_IDS):len(PAGE_IDS) + len(NAV_LINK_IDS)]
    active = [link_id for link_id, link_class in zip(NAV_LINK_IDS, link_classes) if link_class == ACTIVE_LINK_CLASS]

    assert styles[PAGE_IDS.index(ids.TOPICS_PAGE)] == {}
    assert active == [ids.NAV_TOPICS_LINK]


def test_filtry_skryji_skupiny_i_druhy_vztahu():
    full = relation_edges(build_elements(ALL_LAYERS, ALL_KINDS, []))
    without_research = relation_edges(build_elements([layer for layer in ALL_LAYERS if layer != "vyzkum"], ALL_KINDS, []))
    only_follows = relation_edges(build_elements(ALL_LAYERS, [RelationKind.FOLLOWS.value], []))

    assert len(full) == len(RELATIONS)
    assert len(without_research) < len(full)
    assert len(only_follows) == sum(r.kind == RelationKind.FOLLOWS for r in RELATIONS)


def test_klik_na_stranku_ji_otevre_a_v_rezimu_souvislosti_ji_vybere():
    click = {"id": ids.HAFNIAN_PAGE, "path": "/gbs/hafnian"}

    assert click_node(click, ClickMode.OPEN_PAGE.value, None) == ("/gbs/hafnian", no_update)
    assert click_node(click, ClickMode.SHOW_LINKS.value, None) == (no_update, ids.HAFNIAN_PAGE)
    assert click_node({"id": CENTER_ID}, ClickMode.OPEN_PAGE.value, None) == (no_update, CENTER_ID)
    assert click_node({"id": "neexistuje"}, ClickMode.OPEN_PAGE.value, None) == (no_update, no_update)
    assert click_node(None, ClickMode.OPEN_PAGE.value, None) == (no_update, no_update)


def test_podtema_se_objevi_v_mape_u_sve_stranky_a_jde_propojit():
    stored = add_subtopic(None, "  Steinovo lemma ", "Per partes pro gaussovské momenty.", [ids.HAFNIAN_PAGE], PAGES)
    subtopics = parse_subtopics(stored, PAGES)
    nodes = map_nodes(subtopics)
    subtopic = nodes["vlastni-1"]

    assert stored[0]["title"] == "Steinovo lemma"
    assert subtopic.kind == "subtopic" and subtopic.layer == nodes[ids.HAFNIAN_PAGE].layer
    assert {"label": "Steinovo lemma (vlastní podtéma)", "value": "vlastni-1"} in node_options(subtopics)
    connections = add_connection(None, "vlastni-1", "vysvetluje", ids.GBS_PAGE, "", nodes)
    own = parse_connections(connections, nodes)
    assert {relation.kind_label for relation in relations_of("vlastni-1", own, subtopics)} == {"rozvíjí", "vysvětluje"}
    elements = build_elements(ALL_LAYERS, ALL_KINDS, own, subtopics)
    assert len(relation_edges(elements)) == len(RELATIONS) + 2
    assert "subtopic" in next(item for item in elements if item["data"]["id"] == "vlastni-1")["classes"]


def test_spatne_zadane_podtema_ma_ceskou_hlasku():
    stored = add_subtopic(None, "Steinovo lemma", "", [ids.HAFNIAN_PAGE], PAGES)

    with pytest.raises(KnowledgeMapError, match="Napiš název"):
        add_subtopic(None, "  ", "", [ids.HAFNIAN_PAGE], PAGES)
    with pytest.raises(KnowledgeMapError, match="aspoň jednu stránku"):
        add_subtopic(None, "Chaos", "", [], PAGES)
    with pytest.raises(KnowledgeMapError, match="už máš"):
        add_subtopic(stored, "steinovo LEMMA", "", [ids.GBS_PAGE], PAGES)
    assert add_subtopic(stored, "0-1 test chaosu", "", [ids.FAILURE_DIAGNOSTICS_PAGE], PAGES)[1]["id"] == "vlastni-2"


def test_odebrani_podtematu_odebere_i_jeho_propojeni():
    stored = add_subtopic(None, "Steinovo lemma", "", [ids.HAFNIAN_PAGE], PAGES)
    nodes = map_nodes(parse_subtopics(stored, PAGES))
    connections = add_connection(None, "vlastni-1", "vysvetluje", ids.GBS_PAGE, "", nodes)
    connections = add_connection(connections, ids.HAFNIAN_PAGE, "vysvetluje", ids.PORTFOLIO_PAGE, "", nodes)

    subtopics_left, connections_left = remove_subtopics(stored, connections, {0}, PAGES)

    assert subtopics_left == []
    assert [item["source"] for item in connections_left] == [ids.HAFNIAN_PAGE]
    assert remove_connections(connections_left, {0}, nodes) == []


def test_vlastni_propojeni_hlida_spatne_zadani():
    nodes = map_nodes()

    with pytest.raises(KnowledgeMapError, match="samu se sebou"):
        add_connection(None, ids.HAFNIAN_PAGE, "vysvetluje", ids.HAFNIAN_PAGE, "", nodes)
    with pytest.raises(KnowledgeMapError, match="Vyber obě stránky"):
        add_connection(None, ids.HAFNIAN_PAGE, None, ids.GBS_PAGE, "", nodes)
    stored = add_connection(None, ids.HAFNIAN_PAGE, "vysvetluje", ids.GBS_PAGE, "", nodes)
    with pytest.raises(KnowledgeMapError, match="Takové propojení už máš"):
        add_connection(stored, ids.HAFNIAN_PAGE, "vysvetluje", ids.GBS_PAGE, "", nodes)


def test_poskozena_ulozena_data_se_preskoci():
    assert parse_connections([{"source": "neexistuje", "kind": "vysvetluje", "target": ids.GBS_PAGE}, {}], map_nodes()) == []
    assert parse_subtopics([{"id": "vlastni-1", "title": "X", "pages": ["neexistuje"]}, {"title": 1}], PAGES) == []


def test_zaloha_jde_stahnout_a_nahrat_bez_duplicit():
    subtopics = add_subtopic(None, "Steinovo lemma", "poznámka", [ids.HAFNIAN_PAGE], PAGES)
    nodes = map_nodes(parse_subtopics(subtopics, PAGES))
    connections = add_connection(None, "vlastni-1", "vysvetluje", ids.GBS_PAGE, "", nodes)
    backup = json.loads(export_backup(subtopics, connections))

    merged_subtopics, merged_connections = import_backup(encoded(backup), subtopics, connections, PAGES)
    restored_subtopics, restored_connections = import_backup(encoded(backup), None, None, PAGES)

    assert (len(merged_subtopics), len(merged_connections)) == (1, 1)
    assert restored_subtopics == subtopics and restored_connections == connections


def test_nahrani_cizeho_souboru_ma_ceskou_hlasku():
    _, _, message = upload_backup(encoded({"neco": 1}), None, None)
    _, _, broken = upload_backup("data:application/json;base64,bm90IGpzb24=", None, None)

    assert "není záloha mapy znalostí" in message.children
    assert "není platná záloha" in broken.children


def test_detail_podtematu_ukaze_poznamku_a_stranky_ktere_rozviji():
    stored = add_subtopic(None, "Steinovo lemma", "Per partes pro **momenty**.", [ids.HAFNIAN_PAGE], PAGES)
    subtopics = parse_subtopics(stored, PAGES)

    details = describe_node("vlastni-1", [], subtopics)

    assert details[1].children == "Per partes pro **momenty**."
    assert click_node({"id": "vlastni-1"}, ClickMode.OPEN_PAGE.value, stored) == (
        no_update, "vlastni-1",
    )


def test_presunuty_uzel_zustane_kde_ho_uzivatel_nechal():
    elements = build_elements(ALL_LAYERS, ALL_KINDS, [])
    hafnian = next(item for item in elements if item["data"]["id"] == ids.HAFNIAN_PAGE)
    hafnian["position"] = {"x": 12.5, "y": -40.0}

    remembered = positions_of(elements)
    redrawn = build_elements(ALL_LAYERS, ALL_KINDS, [], selected=ids.GBS_PAGE, positions=remembered)

    assert remembered[ids.HAFNIAN_PAGE] == {"x": 12.5, "y": -40.0}
    assert all("source" not in item["data"] for item in elements if item["data"]["id"] in remembered)
    assert next(item for item in redrawn if item["data"]["id"] == ids.HAFNIAN_PAGE)["position"] == {"x": 12.5, "y": -40.0}


def test_vyber_uzlu_ztlumi_nesouvisejici_a_najeti_mysi_popise_prvek():
    elements = build_elements(ALL_LAYERS, ALL_KINDS, [], selected=ids.HAFNIAN_PAGE)
    by_id = {item["data"]["id"]: item for item in elements}

    assert "chosen" in by_id[ids.HAFNIAN_PAGE]["classes"]
    assert "faded" not in by_id[ids.GBS_PAGE]["classes"]
    assert "faded" in by_id[ids.VQE_PAPER_PAGE]["classes"]
    assert describe_hover(by_id[ids.HAFNIAN_PAGE]["data"]).startswith("Hafnián a permanent polopatě: ")
    assert describe_hover(None) == ""
