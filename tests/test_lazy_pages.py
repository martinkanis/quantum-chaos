from dash import no_update

from app import app
from ui import ids
from ui.lazy_pages import LAZY_PAGE_IDS, built_page, page_placeholder, render_visited_page
from ui.navigation import GBS_PATH, HIDDEN, PAGE_IDS, THEORY_PATH


def callback_component_ids():
    found = set()
    for callback in app.callback_map.values():
        outputs = callback["output"] if isinstance(callback["output"], list) else [callback["output"]]
        found |= {output.component_id for output in outputs}
        found |= {dependency["id"] for dependency in callback["inputs"] + callback["state"]}
    return found


def test_odlozene_stranky_nemaji_formulare_na_ktere_by_cekal_callback():
    used_by_callbacks = callback_component_ids()

    for page_id in LAZY_PAGE_IDS:
        assert set(built_page(page_id)) & used_by_callbacks == set(), page_id


def test_kazda_odlozena_stranka_ma_v_layoutu_prazdny_skryty_kontejner():
    placeholder = page_placeholder(ids.THEORY_PAGE)

    assert set(LAZY_PAGE_IDS) <= set(PAGE_IDS)
    assert set(LAZY_PAGE_IDS) <= set(app.layout)
    assert (placeholder.id, placeholder.style, placeholder.children) == (ids.THEORY_PAGE, HIDDEN, [])
    assert placeholder.className == built_page(ids.THEORY_PAGE).className


def test_stranka_se_posle_pri_prvni_navsteve_a_pak_uz_ne():
    theory_index = LAZY_PAGE_IDS.index(ids.THEORY_PAGE)

    *contents, rendered = render_visited_page(THEORY_PATH, [])
    *again, unchanged = render_visited_page(THEORY_PATH, rendered)

    assert contents[theory_index] == built_page(ids.THEORY_PAGE).children
    assert all(content is no_update for index, content in enumerate(contents) if index != theory_index)
    assert rendered == [ids.THEORY_PAGE]
    assert all(content is no_update for content in again) and unchanged is no_update


def test_stranky_s_formulari_se_neposilaji():
    assert all(item is no_update for item in render_visited_page(GBS_PATH, None))
    assert all(item is no_update for item in render_visited_page("/neexistuje", None))
