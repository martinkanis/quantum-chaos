from math import ceil, log

import pytest

from ui import ids
from ui.navigation import PAGE_BY_PATH, PSIQUANTUM_PATH, PSIQUANTUM_VIDEO_PATH
from ui.psiquantum_video_content import (
    CHAPTER_TIMES,
    CLOCK_TOPIC,
    DEMONSTRATOR_TOPIC,
    DETECTOR_TOPIC,
    KEY_FINDINGS,
    LECTURE,
    MATH_TOPIC,
    SLIDES,
    SOURCES_ANCHOR,
    SPONSOR_END,
    SPONSOR_START,
    TIME_TOPIC,
    TOPICS,
    VIDEO_SECONDS,
    chapter_slides,
)
from ui.psiquantum_video_page import DOWNLOAD_LABEL, build_psiquantum_video_page
from ui.study_progress import describe_pager
from ui.theory_content import all_sources
from ui.topic_catalog import breadcrumb_trail
from web.lecture_slides import LECTURES_DIRECTORY, PRESENTATION_NAME, SLIDES_FOLDER, slide_url

LIGHT_SPEED = 299_792_458
FIBRE_INDEX = 1.468


def text_of(topic) -> str:
    return " ".join((topic.in_short + " " + topic.explanation).split())


def components(component):
    yield component
    children = getattr(component, "children", None)
    for child in children if isinstance(children, (list, tuple)) else [children]:
        if child is not None and not isinstance(child, str):
            yield from components(child)


def test_stranka_je_podstrankou_psiquantum_hned_za_ni():
    _, step_label, links, _, _ = describe_pager(PSIQUANTUM_VIDEO_PATH, None)

    assert PAGE_BY_PATH[PSIQUANTUM_VIDEO_PATH] == ids.PSIQUANTUM_VIDEO_PAGE
    assert step_label == "Fotonika · krok 9 / 12"
    assert links[0].children.href == PSIQUANTUM_PATH
    assert [label for label, _ in breadcrumb_trail(ids.PSIQUANTUM_VIDEO_PAGE)][-2].startswith("PsiQuantum")


def test_kapitoly_maji_unikatni_kotvy_snimky_a_odkaz_na_prezentaci():
    page = build_psiquantum_video_page()
    section_ids = [child.id for child in page.children if getattr(child, "id", None)]
    download = next(link for link in components(page) if getattr(link, "children", None) == DOWNLOAD_LABEL)

    assert section_ids == [topic.anchor for topic in TOPICS] + [SOURCES_ANCHOR]
    assert all(anchor.startswith("psiv-") for anchor in section_ids)
    assert {finding.anchor for finding in KEY_FINDINGS} <= set(section_ids)
    assert all(chapter_slides(chapter.anchor) for chapter in CHAPTER_TIMES)
    assert download.href == slide_url(LECTURE, PRESENTATION_NAME)
    assert len(all_sources(TOPICS)) == len(set(all_sources(TOPICS)))


def test_snimky_maji_soubor_a_zadny_neni_z_reklamy():
    files = sorted(path.name for path in (LECTURES_DIRECTORY / LECTURE / SLIDES_FOLDER).glob("*.jpg"))
    shown = [slide for chapter in CHAPTER_TIMES for slide in chapter_slides(chapter.anchor)]

    assert [slide.file_name for slide in SLIDES] == files
    assert shown == list(SLIDES)
    assert all(0 <= slide.seconds < VIDEO_SECONDS for slide in SLIDES)
    assert not any(SPONSOR_START <= slide.seconds < SPONSOR_END for slide in SLIDES)


def test_prezentace_je_ulozena_vedle_snimku():
    assert (LECTURES_DIRECTORY / LECTURE / PRESENTATION_NAME).is_file()


def test_multiplexovani_zdroju_v_textu_sedi_s_vypoctem():
    clock = text_of(CLOCK_TOPIC)

    for probability, sources in ((0.05, 90), (0.10, 44)):
        assert ceil(log(0.01) / log(1 - probability)) == sources
    assert "$N = 90$ zdrojů, při $p = 10\\,\\%$ jen 44" in clock


def test_detekce_vsech_fotonu_v_textu_sedi_s_vypoctem():
    detectors = text_of(DETECTOR_TOPIC)

    assert f"{100 * 0.93 ** 50:.1f}" == "2.7" and "asi 2,7 %" in detectors
    assert f"{100 * 0.99 ** 50:.0f}" == "61" and "asi 61 %" in detectors


def test_chlazeni_a_cas_letu_ve_vlakne_v_textu_sedi_s_vypoctem():
    seconds_250_m = 250 / (LIGHT_SPEED / FIBRE_INDEX)
    metres_800_ns = 800e-9 * LIGHT_SPEED / FIBRE_INDEX

    assert 2 / 0.020 == pytest.approx(100) and "**stokrát**" in text_of(MATH_TOPIC)
    assert f"{seconds_250_m * 1e6:.1f}" == "1.2" and "asi 1,2 µs" in text_of(DEMONSTRATOR_TOPIC)
    assert round(metres_800_ns) == 163 and "asi 163 m" in text_of(DEMONSTRATOR_TOPIC)
    assert round(LIGHT_SPEED * 1e-9 * 100) == 30 and "ve vakuu 30 cm" in text_of(TIME_TOPIC)
