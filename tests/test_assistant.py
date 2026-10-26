import base64
import io
import json
import os
import time
import urllib.error
from types import SimpleNamespace

import pytest

from assistant import claude
from assistant.agent import agent_request, draft_topic
from assistant.claude import AssistantError, explain, write_topic
from assistant.jobs import (
    CRASH_MESSAGE,
    INTERRUPTED_MESSAGE,
    MAX_RUNNING_AGENTS,
    AgentRunner,
    JobError,
    JobStatus,
    MemoryJobStore,
    PostgresJobStore,
    recover_jobs,
)
from assistant.prompts import TOPIC_TOOL_NAME
from assistant.publish import PublishError, PublishSettings, publish_topic
from assistant.selection import SelectionError, selection_from_request
from assistant.topics import (
    TopicError,
    load_topics,
    slugify,
    topic_from_dict,
    topic_to_dict,
    topic_to_json,
    unique_slug,
)

SELECTION = {
    "page_id": "theory-page",
    "page_title": "Teorie Monte Carla na GBS",
    "section_title": "Wickova–Isserlisova věta",
    "selection": "Wickova–Isserlisova věta   a\n hafnián",
    "paragraph": "Momenty gaussovského rozdělení se rozkládají na párování.",
}
PLACEMENT = {"layer": "gbs-ve-financich", "topic_anchor": "tema-rozvedena", "parent_page_id": "theory-page"}
SUBMITTED = {
    "title": "Wickova věta a párování",
    "description": "Proč se momenty gaussovského rozdělení rozkládají na součty přes párování.",
    "in_short": "Moment je součet součinů kovariancí přes všechna párování.",
    "sections": [{"heading": "Intuice", "body": "Text s $x$."}, {"heading": "Příklad", "body": "$E[x^4] = 3$"}],
    "sources": [
        {"title": "Isserlis (1918)", "url": "https://doi.org/10.1093/biomet/12.1-2.134", "note": "původní věta"},
        {"title": "Bez odkazu", "url": "neuvedeno", "note": ""},
    ],
}


def topic_data(**changes):
    data = {
        **SUBMITTED,
        "sources": SUBMITTED["sources"][:1],
        "slug": "wickova-veta-a-parovani",
        "placement": PLACEMENT,
        "origin": {"page_id": "theory-page", "selection": "Wickova věta", "created": "2026-10-26", "model": "m"},
    }
    data.update(changes)
    return data


def response(*blocks, stop_reason="end_turn"):
    return SimpleNamespace(content=list(blocks), stop_reason=stop_reason, model="claude-opus-5-5")


def text(value):
    return SimpleNamespace(type="text", text=value)


def tool_use(payload):
    return SimpleNamespace(type="tool_use", name=TOPIC_TOOL_NAME, input=payload)


class FakeClient:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests = []
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self.create))

    def create(self, **request):
        self.requests.append({**request, "messages": list(request["messages"])})
        return self.responses.pop(0)


def wait_until_done(store, job_id):
    for _ in range(200):
        job = store.get(job_id)
        if job.status != JobStatus.RUNNING:
            return job
        time.sleep(0.01)
    raise AssertionError("agent did not finish")


def test_adresa_tematu_je_bez_diakritiky_a_jedinecna():
    assert slugify("Wickova–Isserlisova věta: párování & hafnián") == "wickova-isserlisova-veta-parovani-hafnian"
    assert slugify("???") == "tema"
    assert len(slugify("velmi dlouhý název " * 10)) <= 60
    assert unique_slug("tema", {"tema", "tema-2"}) == "tema-3"


def test_stranka_tematu_projde_ulozenim_beze_zmeny():
    topic = topic_from_dict(topic_data())

    assert topic_from_dict(json.loads(topic_to_json(topic))) == topic
    assert topic.file_name == "wickova-veta-a-parovani.json"


@pytest.mark.parametrize("changes, message", [
    ({"title": " "}, "Název chybí"),
    ({"sections": []}, "1 až 10 kapitol"),
    ({"slug": "Špatná adresa"}, "malá písmena"),
    ({"sources": [{"title": "x", "url": "javascript:alert(1)", "note": ""}]}, "http"),
    ({"in_short": "x" * 3000}, "moc dlouhý"),
])
def test_neplatna_stranka_tematu_rekne_co_je_spatne(changes, message):
    with pytest.raises(TopicError, match=message):
        topic_from_dict(topic_data(**changes))


def test_rozbity_soubor_tematu_aplikaci_neshodi(tmp_path):
    (tmp_path / "wickova-veta-a-parovani.json").write_text(json.dumps(topic_data()), encoding="utf-8")
    (tmp_path / "rozbite.json").write_text("{nejde", encoding="utf-8")
    (tmp_path / "jiny-nazev.json").write_text(json.dumps(topic_data()), encoding="utf-8")

    assert [topic.slug for topic in load_topics(tmp_path)] == ["wickova-veta-a-parovani"]
    assert load_topics(tmp_path / "neexistuje") == ()


def test_oznaceny_text_se_overi_a_mezery_sjednoti():
    assert selection_from_request(SELECTION).selection == "Wickova–Isserlisova věta a hafnián"
    with pytest.raises(SelectionError, match="Chybí označený text"):
        selection_from_request({"selection": "  "})
    with pytest.raises(SelectionError, match="moc dlouhý"):
        selection_from_request({"selection": "x" * 2001})


def test_vysvetleni_vrati_text_a_posle_kontext_strany():
    client = FakeClient(response(text("Wickova věta říká, že…")))

    assert explain(selection_from_request(SELECTION), client) == "Wickova věta říká, že…"
    request = client.requests[0]
    assert request["fallbacks"] == "default" and request["betas"] == [claude.FALLBACK_BETA]
    assert request["output_config"] == {"effort": claude.EXPLAIN_EFFORT}
    assert "Teorie Monte Carla na GBS" in request["messages"][0]["content"]


def test_odmitnuti_a_chybejici_klic_maji_ceskou_hlasku(monkeypatch):
    with pytest.raises(AssistantError, match="odmítl"):
        explain(selection_from_request(SELECTION), FakeClient(response(stop_reason="refusal")))
    monkeypatch.delenv(claude.API_KEY_ENV, raising=False)
    with pytest.raises(AssistantError, match="ANTHROPIC_API_KEY"):
        explain(selection_from_request(SELECTION))


def test_agent_pokracuje_po_pauze_pripomene_odevzdani_a_vrati_stranku():
    client = FakeClient(
        response(text("Hledám…"), stop_reason="pause_turn"),
        response(text("Mám zdroje."), stop_reason="end_turn"),
        response(tool_use(SUBMITTED), stop_reason="tool_use"),
    )

    draft = write_topic(selection_from_request(SELECTION), None, ["Teorie Monte Carla na GBS"], client)

    assert draft.content == SUBMITTED
    assert [len(request["messages"]) for request in client.requests] == [1, 2, 4]
    assert client.requests[2]["messages"][-1]["content"].startswith("Teď zavolej nástroj")
    tools = client.requests[0]["tools"]
    assert tools[0]["type"] == "web_search_20260209" and tools[1]["strict"] is True


def test_agent_ktery_stranku_neodevzda_skonci_chybou():
    client = FakeClient(response(text("Hotovo.")), response(text("Pořád nic.")))

    with pytest.raises(AssistantError, match="neodevzdal"):
        write_topic(selection_from_request(SELECTION), None, [], client)


def test_navrh_tematu_vynecha_zdroje_bez_odkazu_a_vybere_volnou_adresu():
    client = FakeClient(response(tool_use(SUBMITTED), stop_reason="tool_use"))
    request = agent_request(SELECTION, "Vysvětlení", PLACEMENT, ["Teorie"])

    page = topic_from_dict(draft_topic(request, {"wickova-veta-a-parovani"}, client))

    assert page.slug == "wickova-veta-a-parovani-2"
    assert [source.title for source in page.sources] == ["Isserlis (1918)"]
    assert page.placement.parent_page_id == "theory-page"
    assert page.origin.selection == "Wickova–Isserlisova věta a hafnián"


def test_agent_dobehne_selze_nebo_spadne_a_stav_se_ulozi():
    def time_out(job):
        raise AssistantError("Claude neodpověděl včas.")

    store = MemoryJobStore()
    done = AgentRunner(store, lambda job: {"slug": "x"}).start({"selection": SELECTION})
    failed = AgentRunner(store, time_out).start({})
    crashed = AgentRunner(store, lambda job: 1 / 0).start({})

    assert wait_until_done(store, done.id).status == JobStatus.READY
    assert wait_until_done(store, failed.id).error == "Claude neodpověděl včas."
    assert wait_until_done(store, crashed.id).error == CRASH_MESSAGE


def test_bezi_nejvys_tri_agenti_a_znovu_jde_spustit_jen_neuspesny():
    store = MemoryJobStore()
    runner = AgentRunner(store, lambda job: time.sleep(0.2) or {"slug": "x"})
    jobs = [runner.start({}) for _ in range(MAX_RUNNING_AGENTS)]

    with pytest.raises(JobError, match="Už běží"):
        runner.start({})
    with pytest.raises(JobError, match="Znovu jde spustit"):
        runner.retry(jobs[0].id)
    store.update(jobs[0].id, {"status": JobStatus.INTERRUPTED})
    assert runner.retry(jobs[0].id).status == JobStatus.RUNNING


def test_po_restartu_se_bezici_agenti_preruseni_a_nasazene_tema_oznaci():
    store = MemoryJobStore()
    running = store.create({})
    deploying = store.update(store.create({}).id, {"status": JobStatus.DEPLOYING, "result": {"slug": "nove"}})
    waiting = store.update(store.create({}).id, {"status": JobStatus.DEPLOYING, "result": {"slug": "jine"}})

    recover_jobs(store, {"nove"})

    assert store.get(running.id).status == JobStatus.INTERRUPTED
    assert store.get(running.id).error == INTERRUPTED_MESSAGE
    assert store.get(deploying.id).status == JobStatus.DEPLOYED
    assert store.get(waiting.id).status == JobStatus.DEPLOYING


@pytest.mark.skipif(not os.environ.get("TEST_DATABASE_URL"), reason="TEST_DATABASE_URL není nastavená")
def test_agenti_se_ukladaji_do_postgresu():
    store = PostgresJobStore(os.environ["TEST_DATABASE_URL"])
    job = store.create({"selection": SELECTION})

    updated = store.update(job.id, {"status": JobStatus.READY, "result": topic_data()})
    store.update(job.id, {"dismissed": True})

    assert updated.status == JobStatus.READY and updated.result["slug"] == "wickova-veta-a-parovani"
    assert store.get(job.id).request["selection"]["page_id"] == "theory-page"
    assert job.id not in [other.id for other in store.recent(50)]
    assert store.get("neexistuje") is None


class FakeOpener:
    def __init__(self, answer=None, error=None):
        self.answer, self.error, self.requests = answer, error, []

    def __call__(self, request, timeout):
        self.requests.append(request)
        if self.error:
            raise self.error
        return io.BytesIO(json.dumps(self.answer).encode("utf-8"))


def test_prijate_tema_se_commitne_jednim_souborem_do_main():
    opener = FakeOpener({"commit": {"html_url": "https://github.com/o/r/commit/abc"}})
    topic = topic_from_dict(topic_data())

    url = publish_topic(topic, PublishSettings("token", "o/r", "main"), opener)

    request = opener.requests[0]
    body = json.loads(request.data)
    assert url == "https://github.com/o/r/commit/abc"
    assert request.get_method() == "PUT"
    assert request.full_url == "https://api.github.com/repos/o/r/contents/content/topics/wickova-veta-a-parovani.json"
    assert body["branch"] == "main" and body["message"].startswith("Nové téma: Wickova věta a párování")
    assert topic_from_dict(json.loads(base64.b64decode(body["content"]))) == topic


def test_chyby_githubu_maji_ceskou_hlasku():
    topic = topic_from_dict(topic_data())
    exists = urllib.error.HTTPError("u", 422, "Unprocessable", {}, None)

    with pytest.raises(PublishError, match="už v repozitáři je"):
        publish_topic(topic, PublishSettings("token", "o/r", "main"), FakeOpener(error=exists))
    with pytest.raises(PublishError, match="GITHUB_TOKEN"):
        publish_topic(topic, PublishSettings(None, "o/r", "main"), FakeOpener())


def test_navrh_lze_ulozit_jako_vysledek_agenta():
    assert topic_to_dict(topic_from_dict(topic_data()))["placement"] == PLACEMENT


def api_message(content, stop_reason):
    return {
        "id": "msg", "type": "message", "role": "assistant", "model": "claude-opus-5-5", "content": content,
        "stop_reason": stop_reason, "stop_sequence": None, "usage": {"input_tokens": 1, "output_tokens": 1},
    }


def test_skutecne_sdk_prijme_parametry_a_pokracuje_po_pauze():
    import anthropic
    import httpx

    bodies = []

    def answer(request):
        body = json.loads(request.content)
        bodies.append((request.headers.get("anthropic-beta"), body))
        if len(body["messages"]) == 1:
            search = {"type": "server_tool_use", "id": "srvtoolu_1", "name": "web_search", "input": {"query": "Isserlis"}}
            return httpx.Response(200, json=api_message([search], "pause_turn"))
        submit = {"type": "tool_use", "id": "toolu_1", "name": TOPIC_TOOL_NAME, "input": SUBMITTED}
        return httpx.Response(200, json=api_message([submit], "tool_use"))

    client = anthropic.Anthropic(
        api_key="test", http_client=anthropic.DefaultHttpxClient(transport=httpx.MockTransport(answer))
    )

    draft = write_topic(selection_from_request(SELECTION), None, [], client)

    beta, body = bodies[-1]
    assert draft.content == SUBMITTED
    assert beta == claude.FALLBACK_BETA and body["fallbacks"] == "default"
    assert body["output_config"] == {"effort": claude.TOPIC_EFFORT}
    assert body["messages"][1]["content"][0]["type"] == "server_tool_use"
