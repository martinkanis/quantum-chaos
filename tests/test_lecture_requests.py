from dataclasses import replace
from datetime import timedelta

import pytest
from dash import dcc, no_update
from flask import Flask

from assistant.lecture_requests import (
    NEW_TOPIC,
    DetailLevel,
    LectureRequestError,
    MemoryLectureRequestStore,
    PresentationStyle,
    RequestStatus,
    new_request,
    worker_update,
)
from auth.login import install_login
from auth.settings import LoginSettings
from tests.test_chip_simulator_page import texts_in
from ui import ids
from ui.lecture_requests_callbacks import handle_lecture_request
from ui.lecture_requests_content import OPEN_NOTES, SUBMITTED
from ui.lecture_requests_page import build_lecture_requests_page, request_list
from ui.navigation import LECTURE_REQUESTS_PATH, PAGE_BY_PATH, PHOTONICS_TOPIC_ANCHOR, TOPICS_PATH
from web.lecture_queue_api import API_PREFIX, NEXT_PATH, TOKEN_ENV, install_lecture_queue_api

TOKEN = "t" * 40
VIDEO = "https://youtu.be/havcJFDaNiw"
FORM = (VIDEO, PHOTONICS_TOPIC_ANCHOR, "", DetailLevel.IN_DEPTH.value, PresentationStyle.FRAMES.value, "Víc o zdrojích.")


def request(**changes):
    return replace(new_request(*FORM), **changes)


def make_client(store, token=TOKEN):
    server = Flask(__name__)
    install_login(server, LoginSettings(user="u", password="p", secret_key="k"), secure_cookies=False,
                  token_protected_prefixes=(API_PREFIX,))
    install_lecture_queue_api(server, store, {TOKEN_ENV: token} if token else {})
    return server.test_client()


def auth(token=TOKEN):
    return {"Authorization": f"Bearer {token}"}


def test_formular_overi_odkaz_tema_a_delku_poznamky():
    queued = new_request(*FORM)

    assert (queued.status, queued.detail, queued.presentation) == (
        RequestStatus.WAITING, DetailLevel.IN_DEPTH, PresentationStyle.FRAMES,
    )
    with pytest.raises(LectureRequestError, match="Vlož odkaz"):
        new_request("", *FORM[1:])
    with pytest.raises(LectureRequestError, match="začíná https://"):
        new_request("youtu.be/abc", *FORM[1:])
    with pytest.raises(LectureRequestError, match="název nového tématu"):
        new_request(VIDEO, NEW_TOPIC, "", *FORM[3:])
    with pytest.raises(LectureRequestError, match="Poznámka je moc dlouhá"):
        new_request(*FORM[:5], "x" * 2001)
    assert new_request(VIDEO, NEW_TOPIC, "Kvantové tečky", *FORM[3:]).new_topic_title == "Kvantové tečky"


def test_pracovnik_bere_nejstarsi_cekajici_pozadavek_jen_jednou():
    store = MemoryLectureRequestStore()
    older, newer = request(), request()
    store.add(replace(newer, created_at=older.created_at + timedelta(seconds=1)))
    store.add(older)

    first, second = store.claim_next(), store.claim_next()

    assert (first.id, first.status) == (older.id, RequestStatus.PROCESSING)
    assert second.id == newer.id and store.claim_next() is None


def test_hotovy_pozadavek_musi_mit_adresu_stranky():
    assert worker_update("hotovo", "", "/zapisky/lu")["page_path"] == "/zapisky/lu"
    with pytest.raises(LectureRequestError, match="adresu stránky"):
        worker_update("hotovo", "", "")
    with pytest.raises(LectureRequestError, match="nemůže"):
        worker_update("ceka", "", "")


def test_api_fronty_chce_token_a_bez_nej_se_neotevre():
    store = MemoryLectureRequestStore()
    store.add(request())

    assert make_client(store, token="").post(NEXT_PATH, headers=auth()).status_code == 503
    assert make_client(store, token="kratky").post(NEXT_PATH, headers=auth("kratky")).status_code == 503
    assert make_client(store).post(NEXT_PATH, headers=auth("spatny")).status_code == 401
    assert make_client(store).post(NEXT_PATH).status_code == 401
    assert make_client(store).get("/jina-stranka").status_code == 302


def test_pracovnik_si_vezme_pozadavek_a_nahlasi_hotovou_stranku():
    store = MemoryLectureRequestStore()
    queued = request()
    store.add(queued)
    client = make_client(store)

    claimed = client.post(NEXT_PATH, headers=auth())
    done = client.post(f"{API_PREFIX}{queued.id}/stav", headers=auth(),
                       json={"status": "hotovo", "message": "Zveřejněno.", "page_path": "/zapisky/lu"})
    missing = client.post(f"{API_PREFIX}neni/stav", headers=auth(), json={"status": "chyba", "message": "x"})

    assert claimed.status_code == 200 and claimed.get_json()["url"] == VIDEO
    assert claimed.get_json()["detail"] == "do-hloubky" and claimed.get_json()["note"] == "Víc o zdrojích."
    assert done.status_code == 200 and store.recent()[0].page_path == "/zapisky/lu"
    assert missing.status_code == 400 and "ve frontě není" in missing.get_json()["error"]
    assert client.post(NEXT_PATH, headers=auth()).status_code == 204


def test_formular_zaradi_pozadavek_a_seznam_ukaze_odkaz_na_hotove_zapisky():
    store = MemoryLectureRequestStore()

    message, queue, url = handle_lecture_request(store, ids.LECTURE_REQUEST_SUBMIT, LECTURE_REQUESTS_PATH, FORM)
    error, _, kept_url = handle_lecture_request(store, ids.LECTURE_REQUEST_SUBMIT, LECTURE_REQUESTS_PATH,
                                                ("", *FORM[1:]))
    elsewhere = handle_lecture_request(store, ids.URL, TOPICS_PATH, FORM)
    store.update(store.recent()[0].id, {"status": RequestStatus.DONE, "page_path": "/zapisky/lu"})
    finished = list(texts_in(request_list(store.recent())[0]))

    assert message.children == SUBMITTED and url == "" and VIDEO in list(texts_in(queue[0]))
    assert "Vlož odkaz" in error.children and kept_url is no_update
    assert elsewhere == (no_update, no_update, no_update)
    assert "hotovo" in finished and OPEN_NOTES in finished


def test_stranka_s_formularem_je_v_layoutu_a_ma_vlastni_adresu():
    page = build_lecture_requests_page()
    dropdown = next(component for component in _components(page) if isinstance(component, dcc.Dropdown))

    assert PAGE_BY_PATH[LECTURE_REQUESTS_PATH] == ids.LECTURE_REQUESTS_PAGE
    assert dropdown.value == PHOTONICS_TOPIC_ANCHOR and dropdown.options[-1]["value"] == NEW_TOPIC


def _components(component):
    yield component
    children = getattr(component, "children", None)
    for child in children if isinstance(children, (list, tuple)) else [children]:
        if child is not None and not isinstance(child, str):
            yield from _components(child)
