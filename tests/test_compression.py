import gzip
import json

import pytest
from flask import Flask, Response, send_file

from app import app
from web.compression import MIN_COMPRESSED_SIZE, compress_response, install_compression

LARGE_JSON = {"rows": ["fotonový pár"] * MIN_COMPRESSED_SIZE}


@pytest.fixture
def client(tmp_path):
    server = Flask(__name__)
    script = tmp_path / "plotly.js"
    script.write_text("var x = 1;\n" * MIN_COMPRESSED_SIZE)

    server.add_url_rule("/json", "json", lambda: LARGE_JSON)
    server.add_url_rule("/small", "small", lambda: {"ok": True})
    server.add_url_rule("/image", "image", lambda: Response(b"\x89PNG" * MIN_COMPRESSED_SIZE, mimetype="image/png"))
    server.add_url_rule("/script", "script", lambda: send_file(script, mimetype="application/javascript", etag=True))
    install_compression(server)
    return server.test_client()


def test_velka_textova_odpoved_se_zkomprimuje_a_jde_rozbalit(client):
    response = client.get("/json", headers={"Accept-Encoding": "gzip, deflate"})

    assert response.headers["Content-Encoding"] == "gzip"
    assert "Accept-Encoding" in response.headers["Vary"]
    assert json.loads(gzip.decompress(response.data)) == LARGE_JSON


def test_staticky_soubor_se_zkomprimuje_a_jeho_etag_je_slaby(client):
    response = client.get("/script", headers={"Accept-Encoding": "gzip"})

    assert response.headers["Content-Encoding"] == "gzip"
    assert gzip.decompress(response.data).startswith(b"var x = 1;")
    assert response.headers["ETag"].startswith("W/")


@pytest.mark.parametrize(
    ("path", "accept_encoding"),
    [("/json", "identity"), ("/small", "gzip"), ("/image", "gzip")],
)
def test_bez_gzipu_v_prohlizeci_male_a_binarni_odpovedi_zustanou_jak_jsou(client, path, accept_encoding):
    response = client.get(path, headers={"Accept-Encoding": accept_encoding})

    assert "Content-Encoding" not in response.headers


def test_aplikace_kompresi_pouziva():
    assert compress_response in app.server.after_request_funcs[None]
