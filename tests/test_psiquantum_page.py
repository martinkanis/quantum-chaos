import pytest

from ui import ids
from ui.navigation import PAGE_BY_PATH, PHOTONICS_LANDSCAPE_PATH, PSIQUANTUM_PATH
from ui.psiquantum_content import (
    FUNDING_ROUNDS,
    KEY_FINDINGS,
    LECTURE_SLIDES,
    MONEY_TOPIC,
    SERIES_D_VALUATION_BUSD,
    SERIES_E_VALUATION_BUSD,
    SOURCES_ANCHOR,
    TOPICS,
    WHO_TOPIC,
)
from ui.psiquantum_page import build_psiquantum_page, funding_markdown
from ui.study_progress import describe_pager
from ui.theory_content import all_sources
from ui.topic_catalog import breadcrumb_trail
from ui.walther_lecture_content import SLIDES

SQUARE_METRES_PER_SQUARE_FOOT = 0.09290304


def text_of(topic) -> str:
    return " ".join((topic.in_short + " " + topic.explanation).split())


def test_stranka_je_podstrankou_fotoniky_ve_svete_hned_za_prehledem():
    _, step_label, links, _, _ = describe_pager(PSIQUANTUM_PATH, None)

    assert PAGE_BY_PATH[PSIQUANTUM_PATH] == ids.PSIQUANTUM_PAGE
    assert step_label == "Fotonika · krok 7 / 10"
    assert links[0].children.href == PHOTONICS_LANDSCAPE_PATH
    assert [label for label, _ in breadcrumb_trail(ids.PSIQUANTUM_PAGE)][-2] == (
        "Fotonika ve světě: konkurence a partneři"
    )


def test_kapitoly_maji_unikatni_kotvy_a_zdroje_se_neopakuji():
    page = build_psiquantum_page()
    section_ids = [child.id for child in page.children if getattr(child, "id", None)]
    sources = all_sources(TOPICS)

    assert section_ids == [topic.anchor for topic in TOPICS] + [SOURCES_ANCHOR]
    assert all(anchor.startswith("psiq-") for anchor in section_ids)
    assert {finding.anchor for finding in KEY_FINDINGS} <= set(section_ids)
    assert len(sources) == len(set(sources))
    assert set(LECTURE_SLIDES) <= {slide.file_name for slide in SLIDES}


def test_soucet_kol_a_rust_oceneni_v_textu_sedi():
    total = sum(funding.amount_musd for funding in FUNDING_ROUNDS)
    growth = SERIES_E_VALUATION_BUSD / SERIES_D_VALUATION_BUSD

    assert total == 1665
    assert "1,665 mld. USD" in text_of(MONEY_TOPIC)
    assert "1,665 mld. USD" in " ".join(finding.text for finding in KEY_FINDINGS)
    assert f"{growth:.1f}".replace(".", ",") + "krát" in text_of(MONEY_TOPIC)


def test_tabulka_kol_pise_castky_cesky():
    table = funding_markdown()

    assert "| 215 mil. USD |" in table
    assert "| 1 mld. USD |" in table


def test_plocha_zavodu_v_milpitas_je_prevedena_na_metry():
    assert 140_000 * SQUARE_METRES_PER_SQUARE_FOOT == pytest.approx(13_006, abs=1)
    assert "asi 13 000 m²" in text_of(WHO_TOPIC)
