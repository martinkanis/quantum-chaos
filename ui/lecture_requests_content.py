"""Texts of the page where the reader asks for notes from a recorded lecture."""

from __future__ import annotations

from typing import Dict, Tuple

from assistant.lecture_requests import DetailLevel, PresentationStyle, RequestStatus

TITLE = "Zápisky z přednášky"
LEAD = (
    "Vlož odkaz na záznam přednášky a vyber, kam zápisky patří a jak je udělat. Zbytek proběhne na pozadí: "
    "Claude Code na autorově počítači si požadavek vezme z fronty, stáhne záznam, přepíše řeč, vybere snímky, "
    "napíše zápisky (a když chceš, i prezentaci) a zveřejní je jako novou stránku."
)
HOW_IT_WORKS = (
    "Frontu kontroluje naplánovaná úloha Claude Code na autorově Macu, takže se požadavek zpracuje, až je počítač "
    "zapnutý a úloha poběží.",
    "Zpracování používá předplatné Claude Code, ne placené API aplikace.",
    "Hotové zápisky se zveřejní commitem do aplikace; stránka se objeví po nasazení, odkaz na ni bude v seznamu níže.",
    "Snímky z přednášky i prezentace jsou jako u ostatních přednášek jen pro přihlášené.",
)

URL_LABEL = "Odkaz na video"
URL_PLACEHOLDER = "https://youtu.be/…"
TOPIC_LABEL = "Kam zápisky zařadit"
NEW_TOPIC_OPTION = "Nové téma…"
NEW_TOPIC_LABEL = "Název nového tématu (jen když vybereš „Nové téma…“)"
DETAIL_LABEL = "Jak podrobně"
PRESENTATION_LABEL = "Prezentace (.pptx)"
NOTE_LABEL = "Na co se zaměřit (nepovinné)"
NOTE_PLACEHOLDER = "Třeba: víc o detektorech, vysvětli každý vzorec, srovnej s Waltherovou přednáškou…"
SUBMIT_LABEL = "Zařadit do fronty"
REFRESH_LABEL = "Obnovit seznam"
QUEUE_TITLE = "Fronta a hotové zápisky"
EMPTY_QUEUE = "Zatím žádný požadavek."
SUBMITTED = "Přednáška je ve frontě. Stav uvidíš v seznamu níže."
OPEN_NOTES = "Otevřít zápisky →"

DETAIL_OPTIONS: Tuple[Tuple[DetailLevel, str], ...] = (
    (DetailLevel.OVERVIEW, "Přehled: hlavní myšlenky a čísla, pár kapitol"),
    (DetailLevel.DETAILED, "Podrobné zápisky: každá část přednášky se snímky"),
    (DetailLevel.IN_DEPTH, "Do hloubky pro doktoranda: vysvětlit každý pojem, vzorce, literatura a souvislosti"),
)
PRESENTATION_OPTIONS: Tuple[Tuple[PresentationStyle, str], ...] = (
    (PresentationStyle.FRAMES, "Ano, se snímky z přednášky vedle textu"),
    (PresentationStyle.OWN, "Ano, vlastní slajdy s textem a tabulkami, bez snímků"),
    (PresentationStyle.NONE, "Bez prezentace"),
)
DEFAULT_DETAIL = DetailLevel.IN_DEPTH
DEFAULT_PRESENTATION = PresentationStyle.FRAMES

STATUS_LABELS: Dict[RequestStatus, str] = {
    RequestStatus.WAITING: "čeká ve frontě",
    RequestStatus.PROCESSING: "zpracovává se",
    RequestStatus.DONE: "hotovo",
    RequestStatus.FAILED: "chyba",
}
DETAIL_LABELS: Dict[DetailLevel, str] = {
    DetailLevel.OVERVIEW: "přehled",
    DetailLevel.DETAILED: "podrobně",
    DetailLevel.IN_DEPTH: "do hloubky",
}
PRESENTATION_LABELS: Dict[PresentationStyle, str] = {
    PresentationStyle.FRAMES: "prezentace se snímky",
    PresentationStyle.OWN: "vlastní prezentace",
    PresentationStyle.NONE: "bez prezentace",
}
