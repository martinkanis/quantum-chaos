from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

from flask import Flask

from auth.login import LOGIN_PATH, LOGOUT_PATH, install_login
from auth.rate_limit import MAX_FAILED_ATTEMPTS
from auth.settings import PASSWORD_ENV, SECRET_KEY_ENV, USER_ENV, LoginSettings, settings_from_environment

USER = "doktorand"
PASSWORD = "dlouhe-nahodne-heslo"
CONFIGURED = LoginSettings(user=USER, password=PASSWORD, secret_key="test-secret")


def make_client(settings=CONFIGURED):
    server = Flask(__name__)

    @server.route("/")
    def home():
        return "aplikace"

    @server.route("/_dash-update-component", methods=["POST"])
    def dash_update():
        return "{}"

    @server.route("/healthz")
    def health():
        return "ok"

    install_login(server, settings, secure_cookies=False)
    return server.test_client()


def log_in(client, user=USER, password=PASSWORD, next_path="/"):
    return client.post(LOGIN_PATH, data={"user": user, "password": password, "next": next_path})


def test_bez_prihlaseni_stranka_presmeruje_na_prihlaseni_s_navratem():
    response = make_client().get("/gbs/teorie?x=1")

    assert response.status_code == 302
    assert response.headers["Location"] == "/login?next=%2Fgbs%2Fteorie%3Fx%3D1"


def test_health_check_a_prihlasovaci_stranka_jsou_verejne():
    client = make_client()

    assert client.get("/healthz").data == b"ok"
    assert client.get(LOGIN_PATH).status_code == 200


def test_pozadavek_dashe_bez_prihlaseni_dostane_401():
    response = make_client().post("/_dash-update-component")

    assert response.status_code == 401
    assert "Přihlášení vypršelo" in response.get_json()["error"]


def test_spravne_udaje_prihlasi_na_30_dni():
    client = make_client()

    response = log_in(client, next_path="/gbs")

    assert response.status_code == 302 and response.headers["Location"] == "/gbs"
    expires = parsedate_to_datetime(response.headers["Set-Cookie"].split("Expires=")[1].split(";")[0])
    assert abs(expires - datetime.now(timezone.utc) - timedelta(days=30)) < timedelta(minutes=1)
    assert client.get("/").data == b"aplikace"


def test_spatne_heslo_neprihlasi():
    client = make_client()

    response = log_in(client, password="spatne")

    assert response.status_code == 401
    assert "Neplatné jméno nebo heslo" in response.get_data(as_text=True)
    assert client.get("/").status_code == 302


def test_bez_nastavenych_promennych_se_neprihlasi_nikdo():
    client = make_client(LoginSettings(user=None, password=None, secret_key="test-secret"))

    assert log_in(client, user="", password="").status_code == 401


def test_po_opakovanych_neuspesich_se_prihlaseni_zablokuje():
    client = make_client()
    for _ in range(MAX_FAILED_ATTEMPTS):
        log_in(client, password="spatne")

    response = log_in(client)

    assert response.status_code == 429


def test_podvrzena_adresa_v_x_forwarded_for_zablokovani_neobejde():
    client = make_client()
    for attempt in range(MAX_FAILED_ATTEMPTS):
        client.post(
            LOGIN_PATH,
            data={"user": USER, "password": "spatne", "next": "/"},
            headers={"X-Forwarded-For": f"10.0.0.{attempt}, 203.0.113.7"},
        )

    response = client.post(
        LOGIN_PATH,
        data={"user": USER, "password": PASSWORD, "next": "/"},
        headers={"X-Forwarded-For": "10.0.0.99, 203.0.113.7"},
    )

    assert response.status_code == 429


def test_navrat_po_prihlaseni_nevede_na_cizi_web():
    response = log_in(make_client(), next_path="//evil.example/")

    assert response.headers["Location"] == "/"


def test_odhlaseni_ukonci_session():
    client = make_client()
    log_in(client)

    client.get(LOGOUT_PATH)

    assert client.get("/").status_code == 302


def test_session_cookie_je_ve_vychozim_stavu_secure_a_httponly():
    server = Flask(__name__)
    install_login(server, CONFIGURED)

    assert server.config["SESSION_COOKIE_SECURE"] and server.config["SESSION_COOKIE_HTTPONLY"]


def test_nastaveni_se_cte_z_promennych_prostredi():
    settings = settings_from_environment({USER_ENV: USER, PASSWORD_ENV: PASSWORD, SECRET_KEY_ENV: "klic"})
    missing = settings_from_environment({})

    assert settings == LoginSettings(user=USER, password=PASSWORD, secret_key="klic")
    assert not missing.is_configured and len(missing.secret_key) == 64
