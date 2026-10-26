import os
import re
import textwrap
from datetime import datetime, timezone
from pathlib import Path

import pytest
from dash import dcc, html, no_update

from assistant.jobs import libpq_dsn
from edits.blocks import block_key, split_blocks
from edits.store import (
    DATABASE_UNAVAILABLE,
    EMPTY_TEXT,
    MAX_TEXT_LENGTH,
    MemoryTextEditStore,
    PostgresTextEditStore,
    TextEdit,
    TextEditError,
    TextEdits,
    checked_text,
)
from ui import ids
from ui.editable_text import EditablePages, editable, editable_id
from ui.lazy_pages import LAZY_PAGE_IDS, built_page
from ui.text_edit_callbacks import editor_outputs, handle_editor_action
from ui.text_edit_content import MARKDOWN_HINT, MEMORY_HINT, MISSING_BLOCK, PLAIN_HINT
from ui.text_edit_panel import MODAL_CLASS, OPEN_MODAL_CLASS

ASSETS = Path(__file__).resolve().parent.parent / "assets"
PAGE = ids.GBS_PAGE
"""A page with forms, so the tests build its layout themselves; the lazy pages come from built_page."""
EXPLANATION = """
    První odstavec se vzorcem $x$.

    Druhý odstavec
    na dva řádky.

    $$
    a = b
    $$
"""


def page(*children):
    return html.Div(id=PAGE, children=list(children))


def no_edits(_page_id):
    return {}


def markdowns(component):
    return [item for item in component._traverse() if isinstance(item, dcc.Markdown)]


class FailingStore(MemoryTextEditStore):
    def __init__(self):
        super().__init__()
        self.failing = True
        self.loads = 0

    def all(self):
        self.loads += 1
        if self.failing:
            raise TextEditError(DATABASE_UNAVAILABLE)
        return super().all()


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


def editable_pages(source):
    return EditablePages(TextEdits(MemoryTextEditStore()), lambda: source, built_page, LAZY_PAGE_IDS)


def request(text):
    return {"page": PAGE, "key": block_key(text)}


def normalized(text):
    """Dedented, without trailing spaces and with single blank lines, which renders the same."""
    lines = [line.rstrip() for line in textwrap.dedent(text).split("\n")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


# ---- Blocks -------------------------------------------------------------------------------------------------

def test_markdown_se_deli_na_odstavce_po_odsazeni_jako_v_dcc_markdown():
    assert split_blocks(EXPLANATION) == [
        "První odstavec se vzorcem $x$.",
        "Druhý odstavec\nna dva řádky.",
        "$$\na = b\n$$",
    ]
    assert split_blocks("\n  \n") == []


def test_volny_seznam_a_pokracovani_polozky_zustanou_jednim_blokem():
    text = "1. první\n\n2. druhá\n\n   pokračování druhé\n- jiná\n\nOdstavec za seznamem."

    assert split_blocks(text) == ["1. první\n\n2. druhá\n\n   pokračování druhé\n- jiná", "Odstavec za seznamem."]


def test_prazdny_radek_ve_vzorci_ani_v_kodu_blok_neukonci():
    formula = "$$\na\n\nb\n$$"
    code = "```\nx = 1\n\ny = 2\n```"

    assert split_blocks(f"{formula}\n\nText.\n\n{code}") == [formula, "Text.", code]
    assert split_blocks("Vzorec $$x$$ v řádku.\n\nDalší.") == ["Vzorec $$x$$ v řádku.", "Další."]


def test_bloky_textu_vsech_stranek_spojene_prazdnym_radkem_davaji_puvodni_text():
    for page_id in LAZY_PAGE_IDS:
        for markdown in markdowns(built_page(page_id)):
            if isinstance(markdown.children, str):
                joined = "\n\n".join(split_blocks(markdown.children))
                assert normalized(joined) == normalized(markdown.children), page_id


def test_klic_bloku_zavisi_jen_na_jeho_textu():
    assert block_key("Odstavec.") == block_key("Odstavec.")
    assert block_key("Odstavec.") != block_key("Odstavec!")


# ---- Store --------------------------------------------------------------------------------------------------

def test_prazdny_nebo_moc_dlouhy_text_se_neulozi():
    with pytest.raises(TextEditError, match="nesmí být prázdný"):
        checked_text("  \n ")
    with pytest.raises(TextEditError, match="nejvýš 20 000 znaků"):
        checked_text("a" * (MAX_TEXT_LENGTH + 1))
    assert checked_text(" text\r\n") == "text"


def test_ulozena_uprava_zvysi_verzi_a_text_shodny_s_puvodnim_ji_smaze():
    edits = TextEdits(MemoryTextEditStore())
    start = edits.version()

    edit = edits.save(PAGE, "abc", "Původní.", " Nový text. ")

    assert edit.text == "Nový text." and edits.version() > start
    assert edits.for_page(PAGE) == {"abc": "Nový text."} and edits.for_page("jina-stranka") == {}
    assert edits.save(PAGE, "abc", "Původní.", "Původní.") is None
    assert edits.get(PAGE, "abc") is None and edits.store.all() == []


def test_nedostupna_databaze_stranky_neshodi_a_nacteni_se_zkusi_po_pauze():
    store, clock = FailingStore(), Clock()
    edits = TextEdits(store, clock)

    assert edits.for_page(PAGE) == {} and edits.for_page(PAGE) == {}
    assert store.loads == 1
    store.failing = False
    store.save(TextEdit(PAGE, "abc", "Původní.", "Upraveno.", datetime.now(timezone.utc)))
    clock.now = 61

    assert edits.for_page(PAGE) == {"abc": "Upraveno."}


# ---- Pages --------------------------------------------------------------------------------------------------

def test_markdown_na_strance_se_rozdeli_a_kazdy_odstavec_dostane_id():
    source = page(html.H2("Nadpis"), dcc.Markdown(EXPLANATION, mathjax=True, link_target="_blank"))

    edited, blocks = editable(source, no_edits)
    parts = markdowns(edited)

    assert [part.children for part in parts] == split_blocks(EXPLANATION)
    assert all(part.mathjax and part.link_target == "_blank" for part in parts)
    assert [part.id for part in parts] == [editable_id(PAGE, block_key(text)) for text in split_blocks(EXPLANATION)]
    assert {block.markdown for block in blocks.values()} == {True} and len(blocks) == 3
    assert markdowns(source)[0].children == EXPLANATION and not hasattr(markdowns(source)[0], "id")


def test_upravy_se_promitnou_a_komponenty_s_id_ani_text_mimo_stranky_se_nemeni():
    key = block_key("Úvod stránky.")
    filled_by_callback = html.P("Výsledek", id="vysledek")
    outside = html.P("Mimo stránky.")
    source = html.Div([page(html.P("Úvod stránky.", className="lead"), filled_by_callback), outside])

    edited, blocks = editable(source, lambda page_id: {key: "Upravený úvod."} if page_id == PAGE else {})
    paragraph = edited.children[0].children[0]

    assert (paragraph.children, paragraph.className, paragraph.id) == ("Upravený úvod.", "lead", editable_id(PAGE, key))
    assert edited.children[0].children[1] is filled_by_callback and edited.children[1] is outside
    assert not blocks[(PAGE, key)].markdown and blocks[(PAGE, key)].original == "Úvod stránky."


def test_stejny_odstavec_dvakrat_na_strance_ma_ruzna_id():
    _, blocks = editable(page(html.P("Znovu."), html.P("Znovu.")), no_edits)

    assert sorted(key for _, key in blocks) == [block_key("Znovu."), block_key("Znovu.") + "-2"]


def test_stranka_se_postavi_znovu_az_po_zmene_upravy():
    pages = editable_pages(page(dcc.Markdown("Odstavec.")))
    key = block_key("Odstavec.")

    first = pages.layout()
    assert pages.layout() is first
    pages.text_edits.save(PAGE, key, "Odstavec.", "Lepší odstavec.")

    assert pages.layout() is not first
    assert markdowns(pages.layout())[0].children == "Lepší odstavec."
    assert pages.block(PAGE, key).original == "Odstavec."


def test_odlozena_stranka_se_posle_s_upravou():
    pages = editable_pages(page())
    block = next(iter(editable(built_page(ids.THEORY_PAGE), no_edits)[1].values()))

    pages.text_edits.save(block.page_id, block.key, block.original, "Ručně přeložený odstavec.")
    texts = [item.children for item in html.Div(pages.page_children(ids.THEORY_PAGE))._traverse()
             if getattr(item, "id", None) == editable_id(block.page_id, block.key)]

    assert texts == ["Ručně přeložený odstavec."]
    assert pages.block(ids.THEORY_PAGE, block.key) == block


# ---- Editor -------------------------------------------------------------------------------------------------

def test_otevreny_odstavec_ukaze_zdrojovy_text_a_napovedu():
    pages = editable_pages(page(dcc.Markdown("Text se **vzorcem** $x$."), html.P("Prostý text.")))

    markdown = handle_editor_action(pages, ids.TEXT_EDIT_REQUEST, request("Text se **vzorcem** $x$."), None, None)
    plain = handle_editor_action(pages, ids.TEXT_EDIT_REQUEST, request("Prostý text."), None, None)

    assert (markdown.open, markdown.text, markdown.can_revert, markdown.original) == (
        True, "Text se **vzorcem** $x$.", False, None,
    )
    assert markdown.hint == [MARKDOWN_HINT, " " + MEMORY_HINT] and plain.hint[0] == PLAIN_HINT
    assert markdown.context == request("Text se **vzorcem** $x$.")


def test_ulozeni_zmeni_odstavec_na_strance_a_zavre_okno():
    pages = editable_pages(page(dcc.Markdown("Špatný překlad.")))
    context = request("Špatný překlad.")

    view = handle_editor_action(pages, ids.TEXT_EDIT_SAVE_BUTTON, None, "Správný překlad.", context)
    reopened = handle_editor_action(pages, ids.TEXT_EDIT_REQUEST, context, None, None)

    assert view.changed == (editable_id(PAGE, context["key"]), "Správný překlad.")
    assert editor_outputs(view)[0] == MODAL_CLASS
    assert (reopened.text, reopened.original, reopened.can_revert) == ("Správný překlad.", "Špatný překlad.", True)
    assert editor_outputs(reopened)[0] == OPEN_MODAL_CLASS


def test_vraceni_puvodniho_znovu_ukaze_text_ze_zdroje():
    pages = editable_pages(page(dcc.Markdown("Původní.")))
    context = request("Původní.")
    handle_editor_action(pages, ids.TEXT_EDIT_SAVE_BUTTON, None, "Upravený.", context)

    view = handle_editor_action(pages, ids.TEXT_EDIT_REVERT_BUTTON, None, None, context)

    assert view.changed == (editable_id(PAGE, context["key"]), "Původní.")
    assert pages.text_edits.get(PAGE, context["key"]) is None


def test_chybu_ukaze_okno_a_text_v_nem_necha():
    pages = editable_pages(page(dcc.Markdown("Odstavec.")))
    context = request("Odstavec.")

    empty = handle_editor_action(pages, ids.TEXT_EDIT_SAVE_BUTTON, None, "   ", context)
    missing = handle_editor_action(pages, ids.TEXT_EDIT_REQUEST, {"page": PAGE, "key": "neexistuje"}, None, None)

    assert (empty.message, empty.changed) == (EMPTY_TEXT, None)
    assert editor_outputs(empty)[:2] == (no_update, no_update)
    assert missing.message == MISSING_BLOCK and missing.context is None
    assert handle_editor_action(pages, ids.TEXT_EDIT_REQUEST, {"page": 1, "key": None}, None, None).message == MISSING_BLOCK


def test_skript_editoru_pouziva_id_z_aplikace_a_lista_ma_tlacitko():
    script = (ASSETS / "text_edit.js").read_text(encoding="utf-8")
    highlighter = (ASSETS / "highlighter.js").read_text(encoding="utf-8")
    used = set(re.findall(r'"(text-edit[a-z-]*)"', script))

    assert used <= {value for name, value in vars(ids).items() if name.startswith("TEXT_EDIT")}
    assert {ids.TEXT_EDIT, ids.TEXT_EDIT_REQUEST, ids.TEXT_EDIT_MODAL} <= used
    assert "data-text-edit" in highlighter and "qcTextEdit" in highlighter


@pytest.mark.skipif(not os.environ.get("TEST_DATABASE_URL"), reason="TEST_DATABASE_URL není nastavená")
def test_upravy_se_ukladaji_do_postgresu():
    store = PostgresTextEditStore(libpq_dsn(os.environ["TEST_DATABASE_URL"] + "?uselibpqcompat=true"))
    edits = TextEdits(store)

    edits.save("test-page", "test-key", "Původní.", "První úprava.")
    edits.save("test-page", "test-key", "Původní.", "Druhá úprava.")

    assert TextEdits(store).for_page("test-page") == {"test-key": "Druhá úprava."}
    edits.revert("test-page", "test-key")
    assert TextEdits(store).for_page("test-page") == {}
