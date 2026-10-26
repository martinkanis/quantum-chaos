"""Instructions for Claude: who reads the app, how to explain a selection and how to write a new topic page."""

from __future__ import annotations

from typing import Optional, Sequence

from assistant.selection import SelectionContext

APP_CONTEXT = (
    "Pracuješ ve výukové a výzkumné aplikaci o Monte Carlu, Gaussian Boson Samplingu (GBS), fotonických kvantových "
    "počítačích, teorii náhodných matic a odhadu finančního rizika. Čtenář je začínající doktorand: vysvětluj "
    "podrobně, ale polopatě, česky, a buduj intuici dřív než formalismus."
)

FORMATTING = (
    "Piš v Markdownu. Vzorce piš v MathJaxu: krátké inline jako $...$, delší jako blokový vzorec $$ ... $$ "
    "na samostatných řádcích; dlouhé inline vzorce rozbíjejí zobrazení na mobilu. Desetinnou čárku piš v LaTeXu "
    "jako 0{,}5 a v textu jako 0,5. Nepoužívej HTML."
)

HONESTY = (
    "Odlišuj doložené od vlastního odhadu: konkrétní fakt, číslo nebo výsledek z literatury podlož zdrojem "
    "(autoři, rok, název) a vlastní odhad nebo zjednodušení tak výslovně označ. Zdroj si nikdy nevymýšlej; když si "
    "jím nejsi jistý, napiš, že jde o vlastní vysvětlení."
)

EXPLAIN_SYSTEM = "\n\n".join([
    APP_CONTEXT,
    "Čtenář si na stránce označil úryvek a chce ho dovysvětlit. Vysvětli, co úryvek znamená, proč platí a proč na "
    "něm v kontextu stránky záleží. Rozsah: ideálně jeden odstavec, nejvýš jedna normostrana (asi 1 800 znaků). "
    "Žádné nadpisy ani úvodní fráze, rovnou k věci.",
    FORMATTING,
    HONESTY,
])

TOPIC_TOOL_NAME = "odevzdat_stranku"

TOPIC_SYSTEM = "\n\n".join([
    APP_CONTEXT,
    "Čtenář si na stránce označil úryvek a chce ho rozvést jako samostatné téma. Napiš novou studijní stránku, "
    "která téma úryvku vyloží do hloubky, ale stále srozumitelně.",
    "Postup: nejdřív si nástrojem web_search ověř fakta a dohledej spolehlivé zdroje (učebnice, přehledové články, "
    "arXiv, dokumentace výrobců). Pak zavolej nástroj " + TOPIC_TOOL_NAME + " právě jednou s hotovou stránkou.",
    "Stránka: název (krátký, nejvýš asi 60 znaků), jedna věta popisu pro menu, odstavec „V kostce“ (2–4 věty) "
    "a 3–6 kapitol. Každá kapitola má 1–4 odstavce: intuice, pak vzorce, pak konkrétní příklad. Navazuj na stránky, "
    "které už v aplikaci jsou, a neopakuj je. Do zdrojů dej jen to, co jsi skutečně našel, s funkční adresou; "
    "v textu na ně odkazuj jménem autora a rokem.",
    FORMATTING,
    HONESTY,
    "Čísla uváděj jen ze zdrojů nebo z jednoduchého výpočtu, který v textu ukážeš; aplikace je neumí ověřit.",
])

TOPIC_TOOL = {
    "name": TOPIC_TOOL_NAME,
    "description": "Odevzdá hotovou studijní stránku tématu. Zavolej ho právě jednou, až budeš mít ověřené zdroje.",
    "strict": True,
    "input_schema": {
        "type": "object",
        "additionalProperties": False,
        "required": ["title", "description", "in_short", "sections", "sources"],
        "properties": {
            "title": {"type": "string", "description": "Název stránky, nejvýš asi 60 znaků."},
            "description": {"type": "string", "description": "Jedna věta, o čem stránka je; ukáže se v menu."},
            "in_short": {"type": "string", "description": "Odstavec „V kostce“ v Markdownu, 2–4 věty."},
            "sections": {
                "type": "array",
                "description": "3–6 kapitol stránky.",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["heading", "body"],
                    "properties": {
                        "heading": {"type": "string", "description": "Nadpis kapitoly bez čísla."},
                        "body": {"type": "string", "description": "Text kapitoly v Markdownu s MathJaxem."},
                    },
                },
            },
            "sources": {
                "type": "array",
                "description": "Zdroje, které jsi skutečně našel a ze kterých stránka vychází.",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["title", "url", "note"],
                    "properties": {
                        "title": {"type": "string", "description": "Autoři, rok a název."},
                        "url": {"type": "string", "description": "Adresa začínající https://."},
                        "note": {"type": "string", "description": "Co ze zdroje stránka používá."},
                    },
                },
            },
        },
    },
}

SUBMIT_REMINDER = f"Teď zavolej nástroj {TOPIC_TOOL_NAME} s hotovou stránkou."


def explain_message(context: SelectionContext) -> str:
    return "\n".join([
        *_context_lines(context),
        "",
        "Dovysvětli označený úryvek.",
    ])


def topic_message(
    context: SelectionContext, explanation: Optional[str], existing_pages: Sequence[str]
) -> str:
    lines = _context_lines(context)
    if explanation:
        lines += ["", "<dovysvetleni_ktere_ctenar_uz_dostal>", explanation, "</dovysvetleni_ktere_ctenar_uz_dostal>"]
    if existing_pages:
        lines += ["", "<stranky_v_aplikaci>", *[f"- {title}" for title in existing_pages], "</stranky_v_aplikaci>"]
    lines += ["", "Rozveď téma označeného úryvku jako samostatnou stránku."]
    return "\n".join(lines)


def _context_lines(context: SelectionContext) -> list:
    lines = [f"<stranka>{context.page_title or 'neznámá'}</stranka>"]
    if context.section_title:
        lines.append(f"<kapitola>{context.section_title}</kapitola>")
    if context.paragraph and context.paragraph != context.selection:
        lines += ["<okoli_uryvku>", context.paragraph, "</okoli_uryvku>"]
    lines += ["<oznaceny_uryvek>", context.selection, "</oznaceny_uryvek>"]
    return lines
