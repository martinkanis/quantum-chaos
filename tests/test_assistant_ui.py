import re
import time
from pathlib import Path

from dash import dcc, html, no_update

from assistant.claude import AssistantError
from assistant.jobs import AgentRunner, JobStatus, MemoryJobStore
from assistant.publish import PublishError
from assistant.topics import topic_from_dict
from tests.test_assistant import SELECTION, topic_data
from ui import ids
from ui.assistant_callbacks import (
    ACCEPT,
    EXPAND,
    REJECT,
    Assistant,
    View,
    agents_outputs,
    handle_action,
    view_outputs,
)
from ui.assistant_content import NO_PLACEMENT
from ui.assistant_panel import OPEN_MODAL_CLASS
from ui.generated_page import build_generated_page, generated_page_content
from ui.generated_topics import generated_page_id, generated_path
from ui.knowledge_map_content import BASE_LAYERS, BASE_RELATIONS, Layer, layers_with, relations_with
from ui.navigation import HIDDEN, VISIBLE
from ui.topic_catalog import BASE_RESEARCH_TOPICS, EXPANDED_TOPIC, study_path, topics_with

ASSETS = Path(__file__).resolve().parent.parent / "assets"


class FakeAssistant(Assistant):
    def __init__(self, explanation="Vysvětlení s $x$.", error=None, publish_error=None):
        store = MemoryJobStore()
        self.published = []
        self.explained = []

        def explain(context):
            self.explained.append(context)
            if error:
                raise error
            return explanation

        def publish(topic):
            if publish_error:
                raise publish_error
            self.published.append(topic)
            return "https://github.com/o/r/commit/abc"

        super().__init__(store=store, runner=AgentRunner(store, lambda job: topic_data()), explain=explain, publish=publish)


def components(component):
    yield component
    children = getattr(component, "children", None)
    for child in children if isinstance(children, (list, tuple)) else [children]:
        if child is not None and not isinstance(child, str):
            yield from components(child)


def texts(view_body):
    return " ".join(
        child for item in view_body for component in components(item)
        for child in ([component.children] if isinstance(getattr(component, "children", None), str) else [])
    )


def ready_job(assistant):
    job = assistant.runner.start({"selection": SELECTION})
    for _ in range(200):
        if assistant.store.get(job.id).status != JobStatus.RUNNING:
            break
        time.sleep(0.01)
    return assistant.store.get(job.id)


def test_dovysvetleni_otevre_okno_s_textem_a_nabidne_rozvedeni():
    assistant = FakeAssistant()

    view = handle_action(assistant, ids.ASSISTANT_REQUEST, None, {"action": "explain", **SELECTION}, None)

    assert view.open is True and view.buttons == frozenset({EXPAND}) and view.message == ""
    assert any(isinstance(item, dcc.Markdown) and item.children == "Vysvětlení s $x$." for item in view.body)
    assert view.context["explanation"] == "Vysvětlení s $x$."
    assert assistant.explained[0].page_title == "Teorie Monte Carla na GBS"


def test_chyba_claude_se_ukaze_v_okne_bez_tlacitek():
    view = handle_action(
        FakeAssistant(error=AssistantError("Claude neodpověděl včas.")), ids.ASSISTANT_REQUEST, None,
        {"action": "explain", **SELECTION}, None,
    )

    assert (view.open, view.message, view.buttons) == (True, "Claude neodpověděl včas.", frozenset())


def test_rozvedeni_spusti_agenta_a_zapne_sledovani():
    assistant = FakeAssistant()
    explained = handle_action(assistant, ids.ASSISTANT_REQUEST, None, {"action": "explain", **SELECTION}, None)

    view = handle_action(assistant, ids.ASSISTANT_EXPAND_BUTTON, 1, None, explained.context)

    job = assistant.store.get(view.context["job_id"])
    assert view.poll is True and view.buttons == frozenset()
    assert job.request["explanation"] == "Vysvětlení s $x$."
    assert job.request["placement"]["parent_page_id"] == "theory-page"
    outputs = view_outputs(view)
    assert outputs[0] == OPEN_MODAL_CLASS and outputs[-2] is False and outputs[-1] is not no_update


def test_z_uvodni_stranky_nejde_tema_rozvest():
    view = handle_action(
        FakeAssistant(), ids.ASSISTANT_REQUEST, None, {"action": "expand", **SELECTION, "page_id": ids.TOPICS_PAGE}, None
    )

    assert view.message == NO_PLACEMENT


def test_hotovy_navrh_ukaze_nahled_a_po_prijeti_se_commitne():
    assistant = FakeAssistant()
    job = ready_job(assistant)

    preview = handle_action(assistant, {"type": ids.AGENT_OPEN, "index": job.id}, 1, None, None)
    accepted = handle_action(assistant, ids.ASSISTANT_ACCEPT_BUTTON, 1, None, preview.context)

    assert preview.buttons == frozenset({ACCEPT, REJECT})
    assert "Wickova věta a párování" in texts(preview.body)
    assert [topic.slug for topic in assistant.published] == ["wickova-veta-a-parovani"]
    assert assistant.store.get(job.id).status == JobStatus.DEPLOYING
    assert assistant.store.get(job.id).commit_url == "https://github.com/o/r/commit/abc"
    assert accepted.buttons == frozenset() and accepted.poll is True


def test_neuspesne_publikovani_necha_navrh_ke_schvaleni():
    assistant = FakeAssistant(publish_error=PublishError("GitHub odmítl token."))
    job = ready_job(assistant)

    view = handle_action(assistant, ids.ASSISTANT_ACCEPT_BUTTON, 1, None, {"job_id": job.id})

    assert view.message == "GitHub odmítl token."
    assert view.buttons == frozenset({ACCEPT, REJECT})
    assert assistant.store.get(job.id).status == JobStatus.READY


def test_zamitnuty_navrh_zavre_okno_a_jde_skryt():
    assistant = FakeAssistant()
    job = ready_job(assistant)

    rejected = handle_action(assistant, ids.ASSISTANT_REJECT_BUTTON, 1, None, {"job_id": job.id})
    handle_action(assistant, {"type": ids.AGENT_DISMISS, "index": job.id}, 1, None, None)

    assert rejected.open is False and rejected.refresh is True
    assert assistant.store.get(job.id).status == JobStatus.REJECTED
    assert assistant.store.recent(10) == []


def test_prekresleny_seznam_agentu_bez_kliknuti_nic_nezmeni():
    assert handle_action(FakeAssistant(), {"type": ids.AGENT_OPEN, "index": "x"}, None, None, None) == View()


def test_okenko_agentu_se_prekresli_jen_pri_zmene_a_sleduje_jen_aktivni():
    assistant = FakeAssistant()
    style, _summary, _items, state, stop = agents_outputs(assistant, None)
    assert (style, stop) == (HIDDEN, True)

    job = ready_job(assistant)
    style, summary, items, state, stop = agents_outputs(assistant, None)
    again = agents_outputs(assistant, state)

    assert style == VISIBLE and stop is True and len(items) == 1
    assert state["ready"] == [{"id": job.id, "title": "Wickova věta a párování"}]
    assert again[:4] == (no_update,) * 4


def test_prijate_tema_se_zaradi_do_skupiny_tematu_a_mapy():
    topic = topic_from_dict(topic_data())
    page_id = generated_page_id(topic.slug)

    layers = layers_with(BASE_LAYERS, [topic])
    topics = topics_with(BASE_RESEARCH_TOPICS, [topic])
    relations = relations_with(BASE_RELATIONS, [topic], layers)

    core = next(info for info in layers if info.layer == Layer.CORE)
    assert core.page_ids[-1] == page_id
    expanded = next(research for research in topics if research.anchor == EXPANDED_TOPIC.anchor)
    assert [page.page_id for page in study_path(expanded)] == [page_id]
    assert expanded.pages[0].path == generated_path(topic.slug) == "/rozvedena-temata/wickova-veta-a-parovani"
    assert relations[-1].source == page_id and relations[-1].target == ids.THEORY_PAGE


def test_studijni_cesta_zahrne_i_podstranky_podstranek():
    parent = topic_from_dict(topic_data())
    child = topic_from_dict(topic_data(
        slug="dalsi", placement={**topic_data()["placement"], "parent_page_id": generated_page_id(parent.slug)},
    ))

    expanded = topics_with(BASE_RESEARCH_TOPICS, [parent, child])[-1]

    assert [page.page_id for page in study_path(expanded)] == [generated_page_id("wickova-veta-a-parovani"),
                                                              generated_page_id("dalsi")]


def test_stranka_tematu_ma_kotvy_a_nahled_zadna_id():
    topic = topic_from_dict(topic_data())

    page = build_generated_page(topic)
    preview_ids = [getattr(item, "id", None) for part in generated_page_content(topic, with_anchors=False)
                   for item in components(part)]

    assert page.id == generated_page_id(topic.slug) and page.style == HIDDEN
    assert [item.id for item in components(page) if isinstance(item, html.Section) and getattr(item, "id", None)] == [
        "wickova-veta-a-parovani-1", "wickova-veta-a-parovani-2",
    ]
    assert not any(preview_ids)
    assert any(isinstance(item, html.A) and item.href.startswith("https://doi.org") for item in components(page))


def test_skript_asistenta_pouziva_id_z_aplikace():
    script = (ASSETS / "assistant.js").read_text(encoding="utf-8")
    used = set(re.findall(r'"(assistant-[a-z-]+)"', script))

    assert used <= {value for name, value in vars(ids).items() if name.startswith("ASSISTANT_")}
    assert {ids.ASSISTANT_REQUEST, ids.ASSISTANT_MODAL, ids.ASSISTANT_MODAL_BODY} <= used
