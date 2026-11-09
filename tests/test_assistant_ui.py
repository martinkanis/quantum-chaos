import re
import time
from datetime import datetime, timezone
from pathlib import Path

import pytest
from dash import dcc, html, no_update

from assistant.agent import agent_request
from assistant.claude import AssistantError
from assistant.jobs import AgentRunner, JobStatus, MemoryJobStore
from assistant.publish import PublishError
from assistant.topics import NEW_TOPIC, placement_with_summary, topic_from_dict
from auth.login import LOGOUT_PATH
from tests.test_assistant import FORMULA_SELECTION, PLACEMENT, SELECTION, topic_data
from ui import ids
from ui.agents_page import agent_history, agents_link_label, czech_moment
from ui.assistant_callbacks import (
    ACCEPT,
    AGENTS_OUTPUTS,
    EXPAND,
    REJECT,
    START,
    Assistant,
    View,
    agents_outputs,
    handle_action,
    refresh_agents,
    view_outputs,
)
from ui.assistant_content import (
    AGENTS_LABEL,
    DISMISS_JOB,
    EMPTY_HISTORY,
    NO_PLACEMENT,
    OPEN_JOB,
    OPEN_PROPOSAL,
    RETRY_JOB,
    STATUS_LABELS,
)
from ui.assistant_panel import OPEN_MODAL_CLASS, build_assistant, topic_options
from ui.generated_page import build_generated_page, generated_page_content
from ui.generated_topics import generated_page_id, generated_path
from ui.knowledge_map_content import BASE_LAYERS, BASE_RELATIONS, Layer, layers_with, relations_with
from ui.layout import build_layout
from ui.main_menu import build_main_menu
from ui.navigation import (
    ACTIVE_LINK_CLASS,
    AGENTS_PATH,
    HIDDEN,
    NAV_LINK_IDS,
    PAGE_IDS,
    TOPICS_PATH,
    VISIBLE,
    show_page,
)
from ui.text_edit_panel import build_text_editor
from ui.topic_catalog import (
    BASE_RESEARCH_TOPICS,
    EXPANDED_TOPIC,
    TopicChoice,
    TopicChoiceError,
    placement_with_choice,
    study_path,
    topics_with,
)

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


def buttons_in(component):
    return [item.children for item in components(component) if isinstance(item, html.Button)]


def job_in_state(store, status, **changes):
    """A finished run in the given state, as the agent and the reader leave it behind."""
    job = store.create(agent_request(SELECTION, None, PLACEMENT, []))
    if status in (JobStatus.READY, JobStatus.DEPLOYING, JobStatus.DEPLOYED):
        changes.setdefault("result", topic_data())
    if status in (JobStatus.DEPLOYING, JobStatus.DEPLOYED):
        changes.setdefault("commit_url", "https://github.com/o/r/commit/abc")
    return store.update(job.id, {"status": status, **changes})


def ready_job(assistant):
    job = assistant.runner.start({"selection": SELECTION})
    for _ in range(200):
        if assistant.store.get(job.id).status != JobStatus.RUNNING:
            break
        time.sleep(0.01)
    return assistant.store.get(job.id)


def dialog_of(modal):
    return next(item for item in components(modal) if getattr(item, "className", None) == "assistant-dialog")


def test_obsah_okna_roluje_mezi_nadpisem_a_tlacitky_ktera_ho_neprekryvaji():
    for modal, inner_ids in (
        (build_assistant(), (ids.ASSISTANT_MODAL_BODY, ids.ASSISTANT_PLACEMENT, ids.ASSISTANT_MODAL_MESSAGE)),
        (build_text_editor(), (ids.TEXT_EDIT_TEXT, ids.TEXT_EDIT_MESSAGE)),
    ):
        dialog = dialog_of(modal)
        assert [child.className for child in dialog.children] == ["assistant-title", "assistant-scroll", "assistant-actions"]
        scroll = dialog.children[1]
        assert {getattr(item, "id", None) for item in components(scroll)} >= set(inner_ids)
        assert not any(isinstance(item, html.Button) for item in components(scroll))


def test_dovysvetleni_otevre_okno_s_textem_a_nabidne_rozvedeni():
    assistant = FakeAssistant()

    view = handle_action(assistant, ids.ASSISTANT_REQUEST, None, {"action": "explain", **SELECTION}, None)

    assert view.open is True and view.buttons == frozenset({EXPAND}) and view.message == ""
    assert any(isinstance(item, dcc.Markdown) and item.children == "Vysvětlení s $x$." for item in view.body)
    assert view.context["explanation"] == "Vysvětlení s $x$."
    assert assistant.explained[0].page_title == "Teorie Monte Carla na GBS"


def test_citace_vzorce_se_sazi_mathjaxem_a_blokovy_vzorec_dostane_vlastni_radky():
    assistant = FakeAssistant()

    view = handle_action(assistant, ids.ASSISTANT_REQUEST, None, {"action": "explain", **FORMULA_SELECTION}, None)
    plain = handle_action(assistant, ids.ASSISTANT_REQUEST, None, {"action": "explain", **SELECTION}, None)

    quoted = view.body[0]
    assert isinstance(quoted, html.Blockquote) and isinstance(quoted.children, dcc.Markdown)
    assert quoted.children.mathjax is True
    assert quoted.children.children == (
        "Rozptyl odhadu je\n\n$$\n\\operatorname{Var}(\\hat\\mu) = \\frac{\\sigma^2}{N}\n$$\n\na chyba klesá jako "
        "$1/\\sqrt{N}$."
    )
    assert assistant.explained[0].has_formula is True
    assert isinstance(plain.body[0].children, str)


def test_chyba_claude_se_ukaze_v_okne_bez_tlacitek():
    view = handle_action(
        FakeAssistant(error=AssistantError("Claude neodpověděl včas.")), ids.ASSISTANT_REQUEST, None,
        {"action": "explain", **SELECTION}, None,
    )

    assert (view.open, view.message, view.buttons) == (True, "Claude neodpověděl včas.", frozenset())


def test_rozvedeni_nejdriv_nabidne_vyber_tematu_a_agenta_spusti_az_tlacitko():
    assistant = FakeAssistant()
    explained = handle_action(assistant, ids.ASSISTANT_REQUEST, None, {"action": "explain", **SELECTION}, None)

    offered = handle_action(assistant, ids.ASSISTANT_EXPAND_BUTTON, 1, None, explained.context)
    from_toolbar = handle_action(assistant, ids.ASSISTANT_REQUEST, None, {"action": "expand", **SELECTION}, None)
    nothing_yet = assistant.store.recent(10)
    view = handle_action(
        assistant, ids.ASSISTANT_START_BUTTON, 1, None, offered.context, TopicChoice("tema-fotonika")
    )

    assert offered.buttons == frozenset({START}) and offered.placement is True
    assert offered.choice == TopicChoice(EXPANDED_TOPIC.anchor) and offered.context["explanation"] == "Vysvětlení s $x$."
    assert from_toolbar.buttons == frozenset({START}) and from_toolbar.context["explanation"] is None
    offered_outputs = view_outputs(offered)
    assert offered_outputs[8:11] == (VISIBLE, EXPANDED_TOPIC.anchor, "")
    assert nothing_yet == []
    job = assistant.store.get(view.context["job_id"])
    assert view.poll is True and view.buttons == frozenset() and view.placement is False
    assert job.request["explanation"] == "Vysvětlení s $x$."
    assert job.request["placement"] == {
        "layer": "gbs-ve-financich", "topic_anchor": "tema-fotonika", "parent_page_id": "theory-page",
        "topic_title": None, "topic_summary": None,
    }
    outputs = view_outputs(view)
    assert outputs[0] == OPEN_MODAL_CLASS and outputs[8] == HIDDEN and outputs[-2] is False
    assert outputs[-1] is not no_update


def test_nove_tema_dostane_kotvu_z_nazvu_a_shrnuti_z_popisu_stranky():
    assistant = FakeAssistant()
    offered = handle_action(assistant, ids.ASSISTANT_REQUEST, None, {"action": "expand", **SELECTION}, None)

    missing = handle_action(
        assistant, ids.ASSISTANT_START_BUTTON, 1, None, offered.context, TopicChoice(NEW_TOPIC, " ")
    )
    started = handle_action(
        assistant, ids.ASSISTANT_START_BUTTON, 1, None, offered.context, TopicChoice(NEW_TOPIC, "Kvantové tečky")
    )

    assert "Napiš název nového tématu" in missing.message and missing.placement is True
    assert missing.buttons == frozenset({START}) and missing.choice is no_update
    placement = assistant.store.get(started.context["job_id"]).request["placement"]
    assert (placement["topic_anchor"], placement["topic_title"], placement["topic_summary"]) == (
        "tema-kvantove-tecky", "Kvantové tečky", None,
    )
    assert placement_with_summary(placement, "Zdroje fotonů.")["topic_summary"] == "Zdroje fotonů."
    assert placement_with_summary({**placement, "topic_summary": "Vlastní."}, "Popis")["topic_summary"] == "Vlastní."
    assert placement_with_summary(PLACEMENT, "Popis") == PLACEMENT


def test_volba_tematu_zaradi_stranku_do_vybraneho_nebo_vychoziho_tematu():
    joined = placement_with_choice(PLACEMENT, TopicChoice(NEW_TOPIC, "Fotonika"))
    options = topic_options()

    assert placement_with_choice(PLACEMENT, None)["topic_anchor"] == EXPANDED_TOPIC.anchor
    assert placement_with_choice(PLACEMENT, TopicChoice(""))["topic_anchor"] == EXPANDED_TOPIC.anchor
    assert (joined["topic_anchor"], joined["topic_title"], joined["layer"]) == ("tema-fotonika", None, PLACEMENT["layer"])
    with pytest.raises(TopicChoiceError, match="nezná"):
        placement_with_choice(PLACEMENT, TopicChoice("tema-neexistuje"))
    with pytest.raises(TopicChoiceError, match="moc dlouhý"):
        placement_with_choice(PLACEMENT, TopicChoice(NEW_TOPIC, "x" * 121))
    assert options[0]["value"] == EXPANDED_TOPIC.anchor and "(výchozí)" in options[0]["label"]
    assert {"tema-fotonika", "tema-monte-carlo", "tema-kvantova-optimalizace"} <= {option["value"] for option in options}
    assert options[-1]["value"] == NEW_TOPIC


def test_pri_schvalovani_jde_tema_zmenit_a_ulozi_se_do_stranky():
    assistant = FakeAssistant()
    job = ready_job(assistant)
    founding = job_in_state(assistant.store, JobStatus.READY, result=topic_data(
        placement={**PLACEMENT, "topic_anchor": "tema-kvantove-tecky", "topic_title": "Kvantové tečky"},
    ))

    preview = handle_action(assistant, {"type": ids.AGENT_OPEN, "index": job.id}, 1, None, None)
    founded_preview = handle_action(assistant, {"type": ids.AGENT_OPEN, "index": founding.id}, 1, None, None)
    refused = handle_action(
        assistant, ids.ASSISTANT_ACCEPT_BUTTON, 1, None, preview.context, TopicChoice(NEW_TOPIC, "")
    )
    still_ready = assistant.store.get(job.id).status
    accepted = handle_action(
        assistant, ids.ASSISTANT_ACCEPT_BUTTON, 1, None, preview.context, TopicChoice(NEW_TOPIC, "Kvantové tečky")
    )
    reopened = handle_action(assistant, {"type": ids.AGENT_OPEN, "index": job.id}, 1, None, None)

    assert preview.placement is True and preview.choice == TopicChoice(EXPANDED_TOPIC.anchor)
    assert founded_preview.choice == TopicChoice(NEW_TOPIC, "Kvantové tečky")
    assert "Napiš název" in refused.message and refused.choice == TopicChoice(NEW_TOPIC, "")
    assert refused.buttons == frozenset({ACCEPT, REJECT}) and still_ready == JobStatus.READY
    published = assistant.published[0]
    assert (published.placement.topic_anchor, published.placement.topic_title, published.placement.topic_summary) == (
        "tema-kvantove-tecky", "Kvantové tečky", published.description,
    )
    assert assistant.store.get(job.id).result["placement"]["topic_anchor"] == "tema-kvantove-tecky"
    assert accepted.poll is True and reopened.placement is False


def test_stranka_se_zvolenym_tematem_je_v_nem_a_nove_tema_vznikne_v_katalogu():
    in_photonics = topic_from_dict(topic_data(placement={**PLACEMENT, "topic_anchor": "tema-fotonika"}))
    founded_placement = {
        **PLACEMENT, "topic_anchor": "tema-kvantove-tecky", "topic_title": "Kvantové tečky",
        "topic_summary": "Zdroje fotonů.",
    }
    founding = topic_from_dict(topic_data(slug="tecky", placement=founded_placement))
    joining = topic_from_dict(topic_data(slug="tecky-2", placement=founded_placement))

    topics = topics_with(BASE_RESEARCH_TOPICS, [in_photonics, founding, joining])
    layers = layers_with(BASE_LAYERS, [in_photonics, founding])

    photonics = next(topic for topic in topics if topic.anchor == "tema-fotonika")
    assert photonics.sections[-1].title == "Rozvedená témata"
    assert [page.page_id for page in photonics.sections[-1].pages] == [generated_page_id(in_photonics.slug)]
    assert study_path(photonics)[-1].page_id == generated_page_id(in_photonics.slug)
    founded = next(topic for topic in topics if topic.anchor == "tema-kvantove-tecky")
    assert (founded.title, founded.summary) == ("Kvantové tečky", "Zdroje fotonů.")
    assert [page.page_id for page in founded.pages] == [generated_page_id("tecky"), generated_page_id("tecky-2")]
    assert all(topic.anchor != EXPANDED_TOPIC.anchor for topic in topics)
    core = next(info for info in layers if info.layer == Layer.CORE)
    assert set(core.page_ids[-2:]) == {generated_page_id(in_photonics.slug), generated_page_id("tecky")}


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


def test_seznam_agentu_se_prekresli_jen_pri_zmene_a_sleduje_jen_aktivni():
    assistant = FakeAssistant()
    label, history, _state, stop = agents_outputs(assistant, None)
    assert label == [AGENTS_LABEL] and EMPTY_HISTORY in texts(history) and stop is True

    job = ready_job(assistant)
    label, history, state, stop = agents_outputs(assistant, None)
    again = agents_outputs(assistant, state)

    assert stop is True and len(history[0].children) == 1
    assert label[0] == AGENTS_LABEL and label[-1].children == "(1)"
    assert state["ready"] == [{"id": job.id, "title": "Wickova věta a párování"}]
    assert again[:3] == (no_update,) * 3


def test_odkaz_agenti_pocita_jen_navrhy_ke_schvaleni():
    store = MemoryJobStore()
    for status in JobStatus:
        job_in_state(store, status)
    job_in_state(store, JobStatus.READY)

    label = agents_link_label(store.recent(100))

    assert label[0] == AGENTS_LABEL and label[-1].children == "(2)"
    assert agents_link_label([]) == [AGENTS_LABEL]


def test_prepnuti_stranky_cte_agenty_jen_na_jejich_strance():
    assistant = FakeAssistant()

    elsewhere = refresh_agents(assistant, ids.URL, TOPICS_PATH, None)
    on_page = refresh_agents(assistant, ids.URL, AGENTS_PATH, None)
    on_load = refresh_agents(assistant, None, TOPICS_PATH, None)

    assert elsewhere == (no_update,) * len(AGENTS_OUTPUTS)
    assert on_page[0] == [AGENTS_LABEL] and on_load[0] == [AGENTS_LABEL]


def test_v_liste_je_vedle_odhlaseni_odkaz_agenti_a_stranka_historie_je_v_layoutu():
    menu = build_main_menu()
    nav = next(item for item in components(menu) if getattr(item, "id", None) == ids.MAIN_MENU)
    agents_link, logout = nav.children[-1].children
    layout_ids = {component_id for component_id in build_layout() if isinstance(component_id, str)}
    styles = show_page(AGENTS_PATH)

    assert isinstance(agents_link, dcc.Link) and agents_link.id == ids.NAV_AGENTS_LINK
    assert (agents_link.href, agents_link.children) == (AGENTS_PATH, AGENTS_LABEL)
    assert isinstance(logout, html.A) and logout.href == LOGOUT_PATH
    assert {ids.AGENTS_PAGE, ids.AGENTS_LIST, ids.NAV_AGENTS_LINK} <= layout_ids
    assert not any(getattr(item, "className", None) == "agents-panel" for item in components(build_layout()))
    assert [page_id for page_id, style in zip(PAGE_IDS, styles) if style == VISIBLE] == [ids.AGENTS_PAGE]
    link_classes = styles[len(PAGE_IDS):]
    assert [link for link, cls in zip(NAV_LINK_IDS, link_classes) if cls == ACTIVE_LINK_CLASS] == [
        ids.NAV_AGENTS_LINK
    ]


def test_historie_ukaze_kazdy_stav_s_puvodem_casy_a_akcemi():
    store = MemoryJobStore()
    for status in JobStatus:
        job_in_state(store, status, **({"error": "Agent spadl."} if status is JobStatus.FAILED else {}))
    jobs = store.recent(100)

    items = agent_history(jobs)[0].children
    by_status = {job.status: item for job, item in zip(jobs, items)}
    deployed, failed, ready, running = (
        by_status[JobStatus.DEPLOYED], by_status[JobStatus.FAILED], by_status[JobStatus.READY],
        by_status[JobStatus.RUNNING],
    )

    assert [item.className for item in items] == [f"agent-item status-{job.status.value}" for job in jobs]
    assert all(STATUS_LABELS[job.status] in texts([item]) for job, item in zip(jobs, items))
    assert "Wickova věta a párování" in texts([deployed]) and "Wickova věta a párování" in texts([ready])
    assert "„Wickova–Isserlisova věta a hafnián“" in texts([running])
    assert "Ze stránky „Teorie Monte Carla na GBS“, téma „Rozvedená témata“" in texts([running])
    assert "úryvek: „Wickova–Isserlisova věta a hafnián“" in texts([ready])
    assert "Začátek" in texts([running]) and "zatím běží" in texts([running]) and "Konec" not in texts([running])
    assert "Konec" in texts([ready]) and "Agent spadl." in texts([failed])
    assert buttons_in(ready) == [OPEN_PROPOSAL] and buttons_in(running) == [OPEN_JOB]
    assert buttons_in(failed) == [OPEN_JOB, RETRY_JOB, DISMISS_JOB]
    assert buttons_in(deployed) == [OPEN_JOB, DISMISS_JOB]
    links = [item for item in components(deployed) if isinstance(item, html.A)]
    assert [link.href for link in links] == [generated_path("wickova-veta-a-parovani"), "https://github.com/o/r/commit/abc"]
    ready_job_id = next(job.id for job in jobs if job.status is JobStatus.READY)
    assert next(item for item in components(ready) if isinstance(item, html.Button)).id == {
        "type": ids.AGENT_OPEN, "index": ready_job_id,
    }


def test_casy_behu_jsou_v_ceskem_tvaru_a_v_prazskem_case():
    assert czech_moment(datetime(2026, 11, 9, 13, 2, tzinfo=timezone.utc)) == "9. 11. 2026 14:02"
    assert czech_moment(datetime(2026, 7, 1, 22, 30)) == "2. 7. 2026 00:30"


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


def test_skript_asistenta_posila_vzorce_jako_tex_ze_zdroje_mathjaxu():
    script = (ASSETS / "assistant.js").read_text(encoding="utf-8")

    assert "startup.document" in script and '"mjx-container"' in script
    assert "has_formula" in script and "$$ " in script
