import json

import pytest

import app as application
from auth.login import SESSION_USER_KEY
from ui import ids
from ui.navigation import PAGE_BY_PATH, WALTHER_LECTURE_PATH
from ui.walther_lecture_content import LECTURE, SLIDES
from web.lecture_slides import slide_url
from web.offline import MANIFEST_PATH, SERVICE_WORKER_PATH, build_manifest, lazy_chunk_urls, path_callbacks

CALLBACK_PATH = "/_dash-update-component"


@pytest.fixture
def reader():
    client = application.server.test_client()
    with client.session_transaction() as session:
        session[SESSION_USER_KEY] = "ctenar"
    return client


def with_path(template, path):
    body = json.loads(json.dumps(template))
    for item in body["inputs"]:
        if (item["id"], item["property"]) == (ids.URL, "pathname"):
            item["value"] = path
    return body


def test_service_worker_a_seznam_stranek_jsou_jen_pro_prihlasene(reader):
    anonymous = application.server.test_client()

    assert anonymous.get(SERVICE_WORKER_PATH).status_code == 302
    assert anonymous.get(MANIFEST_PATH).status_code == 302
    worker = reader.get(SERVICE_WORKER_PATH)
    assert worker.status_code == 200
    assert worker.mimetype == "application/javascript"
    assert worker.headers["Cache-Control"] == "no-cache"
    assert CALLBACK_PATH in worker.get_data(as_text=True)
    assert reader.get(MANIFEST_PATH).get_json()["paths"] == sorted(PAGE_BY_PATH)


def test_seznam_obsahuje_vsechny_stranky_slajdy_a_odlozeny_kod():
    manifest = build_manifest(application.app.callback_map)
    chunks = lazy_chunk_urls()

    assert manifest["paths"] == sorted(PAGE_BY_PATH)
    assert {slide_url(LECTURE, slide.file_name) for slide in SLIDES} <= set(manifest["urls"])
    assert {"/_dash-layout", "/_dash-dependencies"} <= set(manifest["urls"])
    assert any(url.endswith("/async-markdown.js") for url in chunks)
    assert any(url.endswith("/async-mathjax.js") for url in chunks)


def test_predem_se_ukladaji_jen_callbacky_zavisle_na_ceste():
    outputs = [template["output"] for template in path_callbacks(application.app.callback_map)]

    assert len(outputs) == 4
    assert any(f"{ids.RENDERED_PAGES_STORE}.data" in output for output in outputs)
    assert any(f"{ids.BREADCRUMB}.children" in output for output in outputs)
    assert any(f"{ids.TOPICS_PAGE}.style" in output for output in outputs)
    assert any(f"{ids.STUDY_PAGER}.style" in output for output in outputs)
    assert not any("results" in output for output in outputs)


def test_server_odpovi_na_kazdy_predem_ukladany_callback(reader):
    for template in path_callbacks(application.app.callback_map):
        response = reader.post(CALLBACK_PATH, json=with_path(template, WALTHER_LECTURE_PATH))

        assert response.status_code == 200, template["output"]
        assert response.get_json()["multi"] is True


def test_odlozena_stranka_prijde_cela_i_bez_predchozich_stranek(reader):
    lazy = next(
        template for template in path_callbacks(application.app.callback_map)
        if f"{ids.RENDERED_PAGES_STORE}.data" in template["output"]
    )
    answer = reader.post(CALLBACK_PATH, json=with_path(lazy, WALTHER_LECTURE_PATH)).get_json()["response"]

    assert answer[ids.RENDERED_PAGES_STORE]["data"] == [ids.WALTHER_LECTURE_PAGE]
    assert answer[ids.WALTHER_LECTURE_PAGE]["children"]
