from dash import dcc, html

from ui import ids
from ui.knowledge_map import page_entries
from ui.knowledge_map_content import LAYERS
from ui.main_menu import build_main_menu
from ui.navigation import KNOWLEDGE_MAP_PATH, NAV_LINK_IDS, PAGE_BY_PATH
from ui.topics_page import build_topics_page


def components(component):
    yield component
    children = getattr(component, "children", None)
    for child in children if isinstance(children, list) else [children]:
        if child is not None and not isinstance(child, str):
            yield from components(child)


def group_links(menu, menu_id):
    group = next(item for item in components(menu) if getattr(item, "id", None) == menu_id)
    return [link.href for link in components(group) if isinstance(link, dcc.Link)]


def test_horni_menu_ma_stejne_skupiny_a_poradi_stranek_jako_dashboard_temata():
    menu = build_main_menu()
    groups = [item for item in components(menu) if isinstance(item, html.Details)]
    entries = page_entries()

    assert [group.id for group in groups] == [info.menu_id for info in LAYERS]
    assert NAV_LINK_IDS == (ids.NAV_TOPICS_LINK,) + tuple(info.menu_id for info in LAYERS)
    for info in LAYERS:
        assert group_links(menu, info.menu_id) == [entries[page_id].path for page_id in info.page_ids]
    dashboard_links = [link.href for link in components(build_topics_page()) if isinstance(link, dcc.Link)]
    for info in LAYERS:
        paths = [entries[page_id].path for page_id in info.page_ids]
        assert all(path in dashboard_links for path in paths)


def test_kazda_stranka_aplikace_je_dostupna_z_horniho_menu():
    menu = build_main_menu()
    menu_paths = {link.href for link in components(menu) if isinstance(link, dcc.Link)}

    assert set(PAGE_BY_PATH) - {KNOWLEDGE_MAP_PATH} <= menu_paths


def test_skupiny_jsou_zavrene_a_menu_ma_tlacitko_pro_mobil():
    menu = build_main_menu()
    groups = [item for item in components(menu) if isinstance(item, html.Details)]

    assert all(group.open is False for group in groups)
    assert any(getattr(item, "id", None) == ids.MENU_TOGGLE for item in components(menu))
