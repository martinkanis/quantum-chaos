import json
import math
from pathlib import Path

import pytest
from dash import dcc, html

from assistant.topics import TopicError, topic_from_dict, topic_to_dict
from tests.test_assistant import topic_data
from tests.test_chip_simulator_page import texts_in
from ui import ids
from ui.generated_page import build_generated_page
from ui.generated_topics import GENERATED_TOPICS, generated_page_id, topic_path
from ui.knowledge_map_content import RELATIONS
from ui.navigation import PAGE_BY_PATH, PHOTONICS_TOPIC_ANCHOR
from ui.topic_catalog import BASE_RESEARCH_TOPICS, RESEARCH_TOPICS, topics_with
from web.lecture_slides import LECTURES_DIRECTORY, PRESENTATION_NAME, slide_path
from web.offline import slide_urls

LU_SLUG = "lu-gaussian-boson-sampling-a-kvantova-vyhoda"
LECTURE_NOTES = [topic for topic in GENERATED_TOPICS if topic.lecture]


def lecture(**changes):
    data = {
        "folder": "prednaska-test", "video_url": "https://youtu.be/test", "video_seconds": 600,
        "speaker": "Jana Nováková", "event": "Seminář", "recorded": "2025-01-15", "language": "česky",
        "how_made": "Přepis a snímky.", "has_presentation": False,
        "key_points": [{"text": "Hlavní myšlenka.", "section": 2}],
    }
    data.update(changes)
    return data


def lecture_topic(sections=None, **lecture_changes):
    sections = sections or [
        {"heading": "Úvod", "body": "Text.", "start": 0, "slides": [{"file_name": "slajd_0010.jpg", "caption": "A"}]},
        {"heading": "Jádro", "body": "Text.", "start": 120, "slides": [{"file_name": "slajd_0300.jpg", "caption": "B"}]},
        {"heading": "Naše poznámka", "body": "Text."},
    ]
    return topic_data(slug="prednaska-test", sections=sections, lecture=lecture(**lecture_changes))


def lu_text() -> str:
    topic = next(topic for topic in GENERATED_TOPICS if topic.slug == LU_SLUG)
    return " ".join(" ".join(section.body for section in topic.sections).split())


def test_zapisky_z_prednasky_maji_snimky_a_prezentaci_ve_slozce_prednasky():
    assert LECTURE_NOTES
    for topic in LECTURE_NOTES:
        folder = LECTURES_DIRECTORY / topic.lecture.folder
        for section in topic.sections:
            assert all(slide_path(topic.lecture.folder, slide.file_name).is_file() for slide in section.slides)
        if topic.lecture.has_presentation:
            assert (folder / PRESENTATION_NAME).is_file()
            deck = json.loads((folder / "prezentace.json").read_text(encoding="utf-8"))
            images = [slide["image"] for slide in deck["slides"] if "image" in slide]
            assert all(slide_path(topic.lecture.folder, image).is_file() for image in images)


def test_kapitoly_prednasky_jdou_po_sobe_a_vlastni_kapitoly_az_na_konci():
    topic = topic_from_dict(lecture_topic())

    assert [section.start for section in topic.sections] == [0, 120, None]
    with pytest.raises(TopicError, match="vlastní kapitoly bez něj jdou až za ně"):
        topic_from_dict(lecture_topic(sections=[
            {"heading": "Naše", "body": "Text."}, {"heading": "Úvod", "body": "Text.", "start": 0},
        ]))
    with pytest.raises(TopicError, match="nejsou z kapitoly „Úvod“"):
        topic_from_dict(lecture_topic(sections=[
            {"heading": "Úvod", "body": "T.", "start": 0, "slides": [{"file_name": "slajd_0200.jpg", "caption": "X"}]},
            {"heading": "Jádro", "body": "T.", "start": 120},
        ]))
    with pytest.raises(TopicError, match="ležet uvnitř záznamu"):
        topic_from_dict(lecture_topic(sections=[{"heading": "Úvod", "body": "T.", "start": 700}]))
    with pytest.raises(TopicError, match="slajd_SSSS.jpg"):
        topic_from_dict(lecture_topic(sections=[
            {"heading": "Úvod", "body": "T.", "start": 0, "slides": [{"file_name": "foto.png", "caption": "X"}]},
        ]))
    with pytest.raises(TopicError, match="odkazuje na kapitolu 5"):
        topic_from_dict(lecture_topic(key_points=[{"text": "Bod.", "section": 5}]))


def test_temata_bez_prednasky_se_ukladaji_beze_zmeny():
    data = topic_to_dict(topic_from_dict(topic_data()))

    assert "lecture" not in data and all(set(section) == {"heading", "body"} for section in data["sections"])
    assert set(data["placement"]) == {"layer", "topic_anchor", "parent_page_id"}
    assert topic_from_dict(topic_to_dict(topic_from_dict(lecture_topic()))) == topic_from_dict(lecture_topic())


def test_stranka_zapisku_ukaze_video_casy_snimky_a_prezentaci():
    topic = topic_from_dict(lecture_topic(has_presentation=True))
    page = build_generated_page(topic)
    texts = list(texts_in(page))
    links = [component for component in _components(page) if isinstance(component, html.A)]
    hrefs = [link.href for link in links]

    assert topic_path(topic) == "/zapisky/prednaska-test"
    assert "Ve videu od " in texts and " do 2:00." in texts and "Naše kapitola, ve videu nezazní." in texts
    assert "https://youtu.be/test?t=120" in hrefs and "/prednasky/prednaska-test/slajd_0300.jpg" in hrefs
    assert "/prednasky/prednaska-test/prezentace.pptx" in hrefs
    key_point_links = [c.href for c in _components(page) if isinstance(c, dcc.Link) and "#" in (c.href or "")]
    assert "/zapisky/prednaska-test#prednaska-test-2" in key_point_links


def test_zapisky_lu_jsou_v_tematu_fotonika_mezi_prednaskami_a_na_mape():
    photonics = next(topic for topic in RESEARCH_TOPICS if topic.anchor == PHOTONICS_TOPIC_ANCHOR)
    lectures = next(section for section in photonics.sections if section.title == "Přednášky")
    page_id = generated_page_id(LU_SLUG)

    assert page_id in [page.page_id for page in lectures.pages]
    assert PAGE_BY_PATH[f"/zapisky/{LU_SLUG}"] == page_id
    assert any(relation.source == page_id and relation.target == ids.PRIMER_GBS_PAGE for relation in RELATIONS)
    assert "/prednasky/lu-gbs-2021/slajd_0388.jpg" in slide_urls()


def test_zapisky_mohou_zalozit_vlastni_tema():
    topic = topic_from_dict(topic_data(placement={
        "layer": "fotonika", "topic_anchor": "tema-kvantove-teckky", "parent_page_id": None,
        "section_title": "Přednášky", "topic_title": "Kvantové tečky", "topic_summary": "Zdroje jednotlivých fotonů.",
    }))
    topics = topics_with(BASE_RESEARCH_TOPICS, [topic])
    founded = topics[-1]

    assert (founded.anchor, founded.title, founded.summary) == (
        "tema-kvantove-teckky", "Kvantové tečky", "Zdroje jednotlivých fotonů.",
    )
    assert [section.title for section in founded.sections] == ["Přednášky"]
    with pytest.raises(TopicError, match="potřebuje kromě názvu i kotvu"):
        topic_from_dict(topic_data(placement={"layer": "fotonika", "topic_title": "Bez kotvy"}))


def test_cisla_v_zapiskach_lu_odpovidaji_vypoctu():
    text = lu_text()
    per_photon = 0.008 * 0.2 * 0.875
    phase = 2 * math.pi * 15 / 1550

    assert round(per_photon, 4) == 0.0014 and r"0{,}008 \cdot 0{,}2 \cdot 0{,}875 \approx 0{,}0014" in text
    assert round(50 * math.log10(per_photon)) == -143 and r"0{,}0014^{50} \approx 10^{-143}" in text
    low, high = (0.008 * 0.1 * 0.875) ** 50, (0.008 * 0.3 * 0.875) ** 50
    assert (round(math.log10(low)), round(math.log10(high))) == (-158, -134)
    assert "vychází $10^{-158}$ až $10^{-134}$" in text
    assert round(phase, 2) == 0.06 and round(math.degrees(phase), 1) == 3.5
    assert r"\approx 0{,}06$ rad, asi 3,5°" in text
    assert f"{15e-9 / 22:.0e}" == "7e-10" and r"\approx 7 \cdot 10^{-10}" in text


def _components(component):
    yield component
    children = getattr(component, "children", None)
    for child in children if isinstance(children, (list, tuple)) else [children]:
        if child is not None and not isinstance(child, str):
            yield from _components(child)


def test_skript_na_podklady_najde_obrazovky_ktere_vydrzi_aspon_tri_sekundy():
    import numpy as np

    from scripts.lecture_sources import frame_name, screen_seconds

    first, second = np.zeros((90, 160), dtype=np.uint8), np.full((90, 160), 200, dtype=np.uint8)
    flash = np.full((90, 160), 90, dtype=np.uint8)
    probes = np.array([first] * 5 + [flash] * 2 + [second] * 4)

    assert screen_seconds(probes) == [4, 10]
    assert frame_name(7) == "slajd_0007.jpg" and Path(frame_name(1234)).suffix == ".jpg"
