from ui import ids
from ui.navigation import (
    ACTIVE_LINK_CLASS,
    LITERATURE_REVIEW_PATH,
    NAV_LINK_IDS,
    PAGE_BY_PATH,
    PAGE_IDS,
    PHOTONIC_HARDWARE_PATH,
    photonic_hardware_href,
    show_page,
)
from ui.photonic_hardware_content import (
    KEY_FINDINGS,
    NOISE_SCENARIOS,
    PHOTONIC_MACHINES,
    SOURCES_ANCHOR,
    TOPICS,
)
from ui.photonic_hardware_page import build_photonic_hardware_page, machines_markdown, noise_markdown
from ui.study_progress import describe_pager
from ui.theory_content import all_sources
from ui.topic_catalog import breadcrumb_trail


def test_stranka_je_druhym_krokem_reserse_gbs():
    link_classes = show_page(PHOTONIC_HARDWARE_PATH)[len(PAGE_IDS):len(PAGE_IDS) + len(NAV_LINK_IDS)]
    active = [link_id for link_id, link_class in zip(NAV_LINK_IDS, link_classes) if link_class == ACTIVE_LINK_CLASS]
    _, step_label, links, _, _ = describe_pager(PHOTONIC_HARDWARE_PATH, None)

    assert PAGE_BY_PATH[PHOTONIC_HARDWARE_PATH] == ids.PHOTONIC_HARDWARE_PAGE
    assert active == [ids.NAV_LITERATURE_REVIEW_LINK]
    assert step_label.endswith("krok 2 / 2")
    assert links[0].children.href == LITERATURE_REVIEW_PATH
    assert [label for label, _ in breadcrumb_trail(ids.PHOTONIC_HARDWARE_PAGE)][-1] == (
        "Quandela a fotonický hardware v Evropě"
    )


def test_kapitoly_maji_unikatni_kotvy_a_tldr_na_ne_odkazuje():
    anchors = [topic.anchor for topic in TOPICS]
    page = build_photonic_hardware_page()
    section_ids = [child.id for child in page.children if getattr(child, "id", None)]

    assert section_ids == anchors + [SOURCES_ANCHOR]
    assert all(anchor.startswith("fotonika-") for anchor in section_ids)
    assert {finding.anchor for finding in KEY_FINDINGS} <= set(anchors)
    assert photonic_hardware_href(anchors[0]) == f"{PHOTONIC_HARDWARE_PATH}#{anchors[0]}"


def test_kazda_kapitola_ma_zdroje_s_odkazem_a_zadny_zdroj_se_neopakuje():
    sources = all_sources(TOPICS)

    assert all(topic.further_reading for topic in TOPICS)
    assert all("](http" in source.citation for source in sources)
    assert len(sources) == len(set(sources))


def test_tabulka_sumu_ukazuje_kazdy_scenar_a_ztraty_odhad_nevychyluji():
    rows = noise_markdown().splitlines()[2:]

    assert len(rows) == len(NOISE_SCENARIOS)
    assert any("nevychýlený" in row for row in rows if "propustnost" in row)
    assert all("−" in row for row in rows if "nerozlišitelnost" in row or "g²" in row)


def test_tabulka_hardwaru_ma_radek_pro_kazdy_stroj():
    rows = machines_markdown().splitlines()[2:]

    assert len(rows) == len(PHOTONIC_MACHINES)
    assert any(row.startswith("| Quandela |") and "| ne |" in row for row in rows)
