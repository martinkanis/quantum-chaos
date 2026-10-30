import math

from ui import guide_basics, ids, theory_content
from ui.academy_page import ACADEMY_SECTIONS
from ui.navigation import (
    ACTIVE_LINK_CLASS,
    NAV_LINK_IDS,
    PAGE_BY_PATH,
    PAGE_IDS,
    PHOTONICS_LANDSCAPE_PATH,
    PHOTONICS_TERMS_HREF,
    photonics_landscape_href,
    show_page,
)
from ui.photonic_hardware_content import SAMPLING_KINDS_TOPIC
from ui.photonics_landscape_content import (
    BUILT_TOPIC,
    CHAIN_TOPIC,
    KEY_FINDINGS,
    PLAYERS,
    SOURCES_ANCHOR,
    SUPPLY_TOPIC,
    TERMS_TOPIC,
    TOPICS,
    GbsVerdict,
)
from ui.photonics_landscape_page import build_photonics_landscape_page, players_markdown
from ui.study_progress import describe_pager
from ui.theory_content import all_sources
from ui.topic_catalog import PHOTONICS_TOPIC, RESEARCH_TOPICS, breadcrumb_trail


def player(name_start):
    return next(item for item in PLAYERS if item.name.startswith(name_start))


def test_stranka_je_v_tematu_fotonika_hned_po_skriptech():
    link_classes = show_page(PHOTONICS_LANDSCAPE_PATH)[len(PAGE_IDS):len(PAGE_IDS) + len(NAV_LINK_IDS)]
    active = [link_id for link_id, link_class in zip(NAV_LINK_IDS, link_classes) if link_class == ACTIVE_LINK_CLASS]
    _, step_label, _, _, _ = describe_pager(PHOTONICS_LANDSCAPE_PATH, None)

    assert PAGE_BY_PATH[PHOTONICS_LANDSCAPE_PATH] == ids.PHOTONICS_LANDSCAPE_PAGE
    assert PHOTONICS_TOPIC in RESEARCH_TOPICS
    assert active == [ids.NAV_PHOTONICS_MENU]
    assert step_label == "Fotonika · krok 6 / 10"
    assert [label for label, _ in breadcrumb_trail(ids.PHOTONICS_LANDSCAPE_PAGE)] == [
        "Témata", "Fotonika a GBS", "Fotonika ve světě: konkurence a partneři",
    ]


def test_kapitoly_maji_unikatni_kotvy_a_tldr_na_ne_odkazuje():
    anchors = [topic.anchor for topic in TOPICS]
    page = build_photonics_landscape_page()
    section_ids = [child.id for child in page.children if getattr(child, "id", None)]

    assert section_ids == anchors + [SOURCES_ANCHOR]
    assert all(anchor.startswith("svet-") for anchor in section_ids)
    assert {finding.anchor for finding in KEY_FINDINGS} <= set(anchors)
    assert photonics_landscape_href(anchors[0]) == f"{PHOTONICS_LANDSCAPE_PATH}#{anchors[0]}"


def test_kazda_kapitola_ma_zdroje_s_odkazem():
    sources = all_sources(TOPICS)

    assert all(topic.further_reading for topic in TOPICS)
    assert all("](http" in source.citation for source in sources)


def test_tabulka_ma_radek_pro_kazdeho_a_radi_od_tech_kdo_gbs_postavil():
    rows = players_markdown().splitlines()[2:]
    verdicts_in_rows = [next(verdict for verdict in GbsVerdict if f"**{verdict.value}**" in row) for row in rows]

    assert len(rows) == len(PLAYERS)
    assert verdicts_in_rows == sorted(verdicts_in_rows, key=list(GbsVerdict).index)
    assert set(verdicts_in_rows) == set(GbsVerdict)


def test_verdikty_pro_firmy_ze_zadani():
    assert player("Xanadu").verdict == GbsVerdict.BUILT
    assert player("Q.ANT").verdict == GbsVerdict.COMPONENTS
    assert player("QuiX").verdict == GbsVerdict.COMPONENTS
    assert player("Thorlabs").verdict == GbsVerdict.COMPONENTS
    assert player("Infleqtion (dříve ColdQuanta)").verdict == GbsVerdict.NO
    assert player("Pasqal").verdict == GbsVerdict.NO
    assert player("Quandela").verdict == GbsVerdict.NO


def test_quantum_academy_upozornuje_na_archivovany_software_xanadu():
    software = next(section for section in ACADEMY_SECTIONS if section.title == "Software")

    assert "archivované" in software.tldr
    assert f"]({PHOTONICS_LANDSCAPE_PATH})" in software.tldr


def test_cisla_o_stlaceni_v_pojmech_odpovidaji_vypoctu():
    decibels_per_r = 20 * math.log10(math.e)
    r_for_ten_decibels = 10 / decibels_per_r
    mean_photons = math.sinh(r_for_ten_decibels) ** 2

    assert f"{decibels_per_r:.2f}".replace(".", "{,}") in TERMS_TOPIC.explanation
    assert f"r \\approx {r_for_ten_decibels:.2f}".replace(".", "{,}") in TERMS_TOPIC.explanation
    assert round(mean_photons) == 2 and "asi 2 fotonům" in TERMS_TOPIC.explanation


def test_texty_zminujici_mody_a_nelinearni_krystal_odkazuji_na_pojmy():
    mentioning_topics = (
        theory_content.GBS_DEVICE, guide_basics.GBS_DEVICE, SAMPLING_KINDS_TOPIC, CHAIN_TOPIC, BUILT_TOPIC, SUPPLY_TOPIC,
    )

    assert PHOTONICS_TERMS_HREF == photonics_landscape_href(TERMS_TOPIC.anchor)
    assert all(f"]({PHOTONICS_TERMS_HREF})" in topic.explanation for topic in mentioning_topics)
