import cmath
from itertools import product
from math import comb, log10, pi, sqrt

import numpy as np
import pytest
from flask import Flask

from auth.login import install_login
from gbs.boson_sampling import permanent
from tests.test_auth import CONFIGURED, log_in
from ui import ids
from ui.navigation import (
    ACTIVE_LINK_CLASS,
    NAV_LINK_IDS,
    PAGE_BY_PATH,
    PAGE_IDS,
    WALTHER_LECTURE_PATH,
    show_page,
)
from ui.study_progress import describe_pager
from ui.theory_content import all_sources
from ui.topic_catalog import PHOTONICS_TOPIC, breadcrumb_trail
from ui.walther_lecture_content import (
    BLIND_TOPIC,
    BOSON_SAMPLING_TOPIC,
    CHAPTER_TIMES,
    GATES_TOPIC,
    HARDWARE_TOPIC,
    KEY_FINDINGS,
    LECTURE,
    SLIDES,
    SOURCES_ANCHOR,
    SUPERPOSITION_TOPIC,
    SWITCH_TOPIC,
    TOPICS,
    VIDEO_SECONDS,
    chapter_slides,
    timestamp,
)
from ui.walther_lecture_page import build_walther_lecture_page
from web.lecture_slides import LECTURES_DIRECTORY, SLIDES_FOLDER, install_lecture_slides, slide_path, slide_url

PAULI = {
    "I": np.eye(2),
    "X": np.array([[0, 1], [1, 0]]),
    "Y": np.array([[0, -1j], [1j, 0]]),
    "Z": np.array([[1, 0], [0, -1]]),
}


def text_of(topic) -> str:
    return " ".join((topic.in_short + " " + topic.explanation).split())


def slide_client():
    server = Flask(__name__)
    install_login(server, CONFIGURED, secure_cookies=False)
    install_lecture_slides(server)
    return server.test_client()


def test_prednaska_je_devatym_krokem_tematu_fotonika_a_v_menu_fotoniky():
    link_classes = show_page(WALTHER_LECTURE_PATH)[len(PAGE_IDS):len(PAGE_IDS) + len(NAV_LINK_IDS)]
    active = [link_id for link_id, link_class in zip(NAV_LINK_IDS, link_classes) if link_class == ACTIVE_LINK_CLASS]

    _, step_label, _, _, _ = describe_pager(WALTHER_LECTURE_PATH, None)

    assert PAGE_BY_PATH[WALTHER_LECTURE_PATH] == ids.WALTHER_LECTURE_PAGE
    assert step_label == "Fotonika · krok 9 / 10"
    assert active == [ids.NAV_PHOTONICS_MENU]
    assert ids.WALTHER_LECTURE_PAGE in [page.page_id for page in PHOTONICS_TOPIC.pages]
    assert breadcrumb_trail(ids.WALTHER_LECTURE_PAGE)[-1][0].startswith("Přednáška")


def test_kapitoly_maji_unikatni_kotvy_a_kazda_ma_slajdy_a_cas_ve_videu():
    page = build_walther_lecture_page()
    section_ids = [child.id for child in page.children if getattr(child, "id", None)]
    anchors = [topic.anchor for topic in TOPICS]

    assert section_ids == anchors + [SOURCES_ANCHOR]
    assert all(anchor.startswith("walther-") for anchor in section_ids)
    assert [chapter.anchor for chapter in CHAPTER_TIMES] == anchors
    starts = [chapter.start for chapter in CHAPTER_TIMES]
    assert starts == sorted(starts) and starts[0] == 0 and starts[-1] < VIDEO_SECONDS
    assert all(chapter_slides(anchor) for anchor in anchors)
    assert {finding.anchor for finding in KEY_FINDINGS} <= set(anchors)


def test_kazdy_slajd_ma_soubor_a_kazdy_soubor_je_na_strance():
    files_on_disk = sorted(path.name for path in (LECTURES_DIRECTORY / LECTURE / SLIDES_FOLDER).glob("*.jpg"))
    shown = [slide for anchor in (topic.anchor for topic in TOPICS) for slide in chapter_slides(anchor)]

    assert [slide.file_name for slide in SLIDES] == files_on_disk
    assert shown == list(SLIDES)
    assert all(0 <= slide.seconds < VIDEO_SECONDS for slide in SLIDES)
    assert len({slide.caption for slide in SLIDES}) == len(SLIDES)


def test_casy_se_pisou_jako_na_youtube():
    assert timestamp(0) == "0:00"
    assert timestamp(1547) == "25:47"
    assert timestamp(3765) == "1:02:45"


def test_zdroje_se_neopakuji():
    sources = all_sources(TOPICS)

    assert len(sources) == len(set(sources))
    assert len({source.citation for source in sources}) == len(sources)


def test_slajdy_vidi_jen_prihlaseny_ctenar():
    client = slide_client()
    url = slide_url(LECTURE, SLIDES[0].file_name)

    assert client.get(url).status_code == 302
    log_in(client)
    response = client.get(url)
    assert response.status_code == 200
    assert response.mimetype == "image/jpeg"
    assert response.data == slide_path(LECTURE, SLIDES[0].file_name).read_bytes()
    assert "private" in response.headers["Cache-Control"]
    assert "public" not in response.headers["Cache-Control"]


@pytest.mark.parametrize("path", [
    "/prednasky/walther-2022/neexistuje.jpg",
    "/prednasky/walther-2022/slajd_9999.jpg",
    "/prednasky/walther-2022/..%2F..%2Fapp.py",
    "/prednasky/Walther_2022/slajd_0005.jpg",
])
def test_jine_soubory_nez_slajdy_server_nevyda(path):
    client = slide_client()
    log_in(client)

    assert client.get(path).status_code == 404


def test_hong_ou_mandel_permanent_delice_50_50_je_nula():
    transmission = reflection = 1 / sqrt(2)
    splitter = np.array([[transmission, 1j * reflection], [1j * reflection, transmission]])

    assert abs(permanent(splitter)) == pytest.approx(0, abs=1e-15)
    assert permanent(splitter) == pytest.approx(transmission**2 - reflection**2)
    assert "|T^2 - R^2|^2" in text_of(BOSON_SAMPLING_TOPIC)


def test_pocty_stavu_a_vystupu_v_textu_sedi_s_vypoctem():
    hardware, bosons, superposition = text_of(HARDWARE_TOPIC), text_of(BOSON_SAMPLING_TOPIC), text_of(SUPERPOSITION_TOPIC)

    assert f"{2**50 / 1e15:.1f}".replace(".", "{,}") + r" \cdot 10^{15}" in superposition
    assert round(2**50 * 16 / 1e15) == 18 and "18 petabajtů" in superposition
    assert round(log10(comb(269, 70))) == 66 and r"\binom{269}{70} \approx 10^{66}" in bosons
    assert f"{2**53 / 1e15:.0f}" == "9" and r"2^{53} \approx 9 \cdot 10^{15}" in bosons
    assert f"{2**100 / 1e30:.1f}" == "1.3" and r"2^{100} \approx 1{,}3 \cdot 10^{30}" in bosons
    assert f"{100 * 0.95**70:.1f}" == "2.8" and r"0{,}95^{70} \approx 2{,}8\,\%" in hardware
    assert 0.01**10 == pytest.approx(1e-20) and "$10^{-20}$" in hardware


def test_pocet_delicu_univerzalniho_interferometru():
    def splitters(modes):
        return modes * (modes - 1) // 2

    hardware = text_of(HARDWARE_TOPIC)
    assert splitters(26) == 325 and "Pro 26 módů je to 325" in hardware
    assert max(modes for modes in range(2, 27) if splitters(modes) <= 88) == 13
    assert "nejvýš pro 13 módů" in hardware


def test_machuv_zehnderuv_interferometr_dava_sin_a_cos_polovicni_faze():
    splitter = np.array([[1, 1j], [1j, 1]]) / sqrt(2)
    for phase in np.linspace(0, 2 * pi, 9):
        output = splitter @ np.diag([1, cmath.exp(1j * phase)]) @ splitter @ np.array([1, 0])
        assert abs(output[0]) ** 2 == pytest.approx(np.sin(phase / 2) ** 2)
        assert abs(output[1]) ** 2 == pytest.approx(np.cos(phase / 2) ** 2)


def test_uspesnost_destruktivniho_cnot_je_jedna_devitina():
    assert f"{100 / 9:.0f}" == "11"
    assert r"$p = 1/9 \approx 11\,\%$" in text_of(GATES_TOPIC)
    assert "(1/3)^2 = 1/9" in text_of(GATES_TOPIC)


@pytest.mark.parametrize("first, second", list(product(PAULI, repeat=2)))
def test_kvantovy_prepinac_pozna_zda_pauliho_matice_komutuji(first, second):
    u1, u2 = PAULI[first], PAULI[second]
    commute = np.allclose(u1 @ u2, u2 @ u1)
    rng = np.random.default_rng(7)
    state = rng.normal(size=2) + 1j * rng.normal(size=2)
    state /= np.linalg.norm(state)
    # Control |+>, branch |0> applies U1 then U2, branch |1> the other order; the control is then measured in |±>.
    plus = (u2 @ u1 @ state + u1 @ u2 @ state) / 2
    minus = (u2 @ u1 @ state - u1 @ u2 @ state) / 2

    assert np.linalg.norm(plus) ** 2 == pytest.approx(1.0 if commute else 0.0, abs=1e-12)
    assert np.linalg.norm(minus) ** 2 == pytest.approx(0.0 if commute else 1.0, abs=1e-12)


def test_prepinac_v_textu_odpovida_vypoctu():
    switch = text_of(SWITCH_TOPIC)

    assert r"Pro $X, X$ vychází 1 a 0, pro $X, Y$ 0 a 1" in switch
    assert np.allclose(PAULI["X"] @ PAULI["Y"], -PAULI["Y"] @ PAULI["X"])


def test_server_slepeho_pocitani_vidi_uhel_mereni_rovnomerne_rozlozeny():
    angles = [k * pi / 4 for k in range(8)]

    def seen_by_server(secret):
        counts = {}
        for theta, bit in product(angles, (0, 1)):
            delta = round(((secret + theta + bit * pi) % (2 * pi)) / (pi / 4)) % 8
            counts[delta] = counts.get(delta, 0) + 1
        return counts

    for secret in angles:
        assert seen_by_server(secret) == {k: 2 for k in range(8)}
    assert r"\delta_j = \phi_j + \theta_j + r_j\pi" in text_of(BLIND_TOPIC)
