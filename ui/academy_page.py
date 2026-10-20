"""Quantum Academy: curated links for learning quantum computing, next to the topics of the app."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from dash import dcc, html

from ui import ids
from ui.advantage_content import QISKIT_DOCUMENTATION
from ui.guide_practice import STRAWBERRY_FIELDS
from ui.navigation import HIDDEN, PHOTONIC_HARDWARE_PATH
from ui.theory_content import (
    AARONSON_ARKHIPOV,
    ANDERSEN_SHAN_EXPECTATIONS,
    DRIMAL_MONTE_CARLO,
    DVORAKOVA_MONTE_CARLO,
    GERRY_KNIGHT,
    GLASSERMAN,
    HAMILTON,
    KRUSE,
    SALEH_TEICH,
    WALRUS_HAFNIAN,
    Source,
)
from ui.topic_sections import markdown_list, source_items

LEAD = (
    "Kde se učit kvantové počítání: interaktivní kurz, videa, blog a materiály, ze kterých vychází tato aplikace. "
    "Odkazy se otevírají v nové záložce."
)


@dataclass(frozen=True)
class AcademyLink:
    title: str
    url: str
    description: str


@dataclass(frozen=True)
class AcademySection:
    title: str
    links: Tuple[AcademyLink, ...] = ()
    sources: Tuple[Source, ...] = ()
    tldr: str = ""
    """Optional Markdown summary shown above the links."""


ACADEMY_SECTIONS: Tuple[AcademySection, ...] = (
    AcademySection(
        "Začni tady: kvantové počítání od základů",
        links=(
            AcademyLink(
                "Quantum Country", "https://quantum.country",
                "Interaktivní esej Andyho Matuschaka a Michaela Nielsena o kvantovém počítání a kvantové mechanice, "
                "s opakováním v rozestupech, aby si člověk látku opravdu zapamatoval.",
            ),
            AcademyLink(
                "Looking Glass Universe", "https://www.youtube.com/@LookingGlassUniverse",
                "YouTube kanál Mithuny Yoganathan: kvantová mechanika a kvantové počítání srozumitelně a do hloubky.",
            ),
        ),
    ),
    AcademySection(
        "Blogy a diskuse",
        links=(
            AcademyLink(
                "Shtetl-Optimized", "https://scottaaronson.blog",
                "Blog Scotta Aaronsona o kvantové složitosti a kvantové výhodě, včetně boson samplingu; střízlivý "
                "pohled na tvrzení o kvantovém zrychlení.",
            ),
        ),
    ),
    AcademySection(
        "Monte Carlo",
        sources=(DRIMAL_MONTE_CARLO, DVORAKOVA_MONTE_CARLO, GLASSERMAN),
    ),
    AcademySection(
        "Gaussian Boson Sampling a fotonika",
        sources=(HAMILTON, KRUSE, AARONSON_ARKHIPOV, ANDERSEN_SHAN_EXPECTATIONS, SALEH_TEICH, GERRY_KNIGHT),
    ),
    AcademySection(
        "Software",
        sources=(QISKIT_DOCUMENTATION, STRAWBERRY_FIELDS, WALRUS_HAFNIAN),
    ),
    AcademySection(
        "Platformy pro kvantové algoritmy: Classiq a CUDA-Q",
        tldr=(
            "**Classiq** je vysokoúrovňový jazyk Qmod s Python SDK: popíšeš, *co* má obvod dělat, a platforma ho "
            "sama sestaví (syntéza obvodu). Jeho veřejná knihovna (licence MIT) má hotové finanční příklady – "
            "třeba výpočet VaR iterativní kvantovou amplitudovou estimací (IQAE), tedy hradlovou cestu z rešerše. "
            "Háček: ke spouštění je potřeba účet a přístup je teď jen na pozvánku; kód ale jde volně číst.\n\n"
            "**CUDA-Q** od NVIDIA je otevřený (Apache 2.0) programovací model pro hybridní výpočty CPU + GPU + "
            "kvantový procesor v Pythonu i C++ (`pip install cudaq`). Nabízí rychlé simulátory – akcelerované "
            "na GPU v Linuxu, na Macu s Apple Silicon běží na CPU – a napojení na reálné přístroje včetně "
            "fotonického boson sampleru ORCA. Pro tuto aplikaci je zajímavý hlavně jako cesta k fotonickému "
            "hardwaru a k velkým simulacím."
        ),
        links=(
            AcademyLink(
                "Classiq Library", "https://github.com/Classiq/classiq-library",
                "Sbírka algoritmů, aplikací a tutoriálů v Qmod a Pythonu (složky algorithms, applications, "
                "tutorials, functions), notebooky .ipynb i modely .qmod.",
            ),
            AcademyLink(
                "Classiq: finanční aplikace", "https://github.com/Classiq/classiq-library/tree/main/applications/finance",
                "Oceňování opcí (option_pricing, autocallable_options, rainbow_options), value_at_risk "
                "a optimalizace portfolia – dobré čtení ke kapitole o hradlovém kvantovém Monte Carlu v rešerši.",
            ),
            AcademyLink(
                "Classiq: registrace a instalace",
                "https://docs.classiq.io/latest/classiq_101/registration_installations/",
                "Jak získat účet a nainstalovat SDK (`pip install classiq`); přístup je podle dokumentace "
                "jen na pozvánku a bezplatný nekomerční přístup zatím není.",
            ),
            AcademyLink(
                "CUDA-Q: dokumentace", "https://nvidia.github.io/cuda-quantum/latest/",
                "Rychlý start, simulátory (stavový vektor, tensor networks, šumové simulace) a seznam "
                "podporovaných kvantových procesorů a cloudů.",
            ),
            AcademyLink(
                "CUDA-Q: kód na GitHubu", "https://github.com/NVIDIA/cuda-quantum",
                "Zdrojový kód pod licencí Apache 2.0.",
            ),
            AcademyLink(
                "CUDA-Q a reálný hardware",
                "https://nvidia.github.io/cuda-quantum/latest/using/examples/hardware_providers.html",
                "Příklady připojení k poskytovatelům, mj. k fotonickému boson sampleru ORCA s časovými biny.",
            ),
        ),
    ),
    AcademySection(
        "Quandela: fotonický hardware a Perceval",
        tldr=(
            "**Quandela** (Francie) staví fotonické kvantové počítače na jednotlivých fotonech z kvantových teček. "
            "Procesor **Belenos** (12 qubitů, 24 módů) je v jejich cloudu a stejný typ stroje, **Lucy**, provozuje "
            "EuroHPC v TGCC u Paříže; výzkumníci z Evropy na něj mohou žádat zdarma v pilotní výzvě s měsíčními "
            "uzávěrkami.\n\n"
            "**Perceval** je jejich otevřený framework v Pythonu (verze ≥ 3.10, `pip install perceval-quandela`, "
            "licence MIT): lineárně optické obvody, realistický šum zdroje, přesné i vzorkovací simulátory "
            "a odesílání úloh na skutečné procesory přes cloud Quandela nebo Scaleway.\n\n"
            "**Pro naši úlohu:** GBS se stlačeným světlem Quandela neumí, umí ale boson sampling s jednotlivými "
            "fotony, na který jde odhad GBS-I přeložit pomocí permanentů. Rozbor, náš experiment v Percevalu "
            "a přehled, kdo v Evropě umí GBS, je na stránce [Quandela a fotonický hardware v Evropě]"
            f"({PHOTONIC_HARDWARE_PATH})."
        ),
        links=(
            AcademyLink(
                "Perceval: dokumentace", "https://perceval.quandela.net/docs/",
                "Rychlý start, tutoriály pro začátečníky, pokročilé i experty, reference simulátorů a backendů "
                "a příklady algoritmů.",
            ),
            AcademyLink(
                "Perceval: příklady boson samplingu",
                "https://perceval.quandela.net/docs/v1.3/examples_boson_sampling.html",
                "Ideální boson sampling, sampling s nedokonalými zdroji a simulace metodou MPS – nejbližší start "
                "pro naši permanentní variantu odhadu GBS-I.",
            ),
            AcademyLink(
                "Perceval: kód na GitHubu", "https://github.com/Quandela/Perceval",
                "Zdrojový kód pod licencí MIT; výpočetní jádro exqalibur smí přes Perceval používat podle výjimky "
                "v licenci.",
            ),
            AcademyLink(
                "Perceval: white paper", "https://arxiv.org/abs/2204.00602",
                "Heurtel a kol.: architektura frameworku, simulátory a model zdroje fotonů.",
            ),
            AcademyLink(
                "Quandela Cloud", "https://cloud.quandela.com",
                "Cloudová platforma, přes kterou Perceval posílá úlohy na simulátory a procesory Quandela.",
            ),
            AcademyLink(
                "Procesor Belenos", "https://www.quandela.com/qpus/belenos/",
                "Parametry procesoru dostupného v cloudu.",
            ),
            AcademyLink(
                "EuroHPC: pilotní přístup ke kvantovým počítačům", "https://access.eurohpc-ju.europa.eu/calls/61",
                "Přihláška do výzvy, přes kterou jde žádat o čas na stroji Lucy (přístup na 3 nebo 6 měsíců).",
            ),
        ),
    ),
)


def build_academy_page() -> html.Div:
    return html.Div(
        id=ids.ACADEMY_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            html.H1("Quantum Academy"),
            html.P(LEAD, className="lead"),
            *[_section(section) for section in ACADEMY_SECTIONS],
        ],
    )


def _section(section: AcademySection) -> html.Section:
    items = [f"- [{link.title}]({link.url}) – {link.description}" for link in section.links]
    return html.Section(
        className="card theory-section",
        children=[
            html.H2(section.title),
            *_tldr(section),
            markdown_list(items + source_items(section.sources)),
        ],
    )


def _tldr(section: AcademySection) -> list:
    if not section.tldr:
        return []
    return [html.Div(className="tldr-box", children=[html.Strong("TL;DR"), dcc.Markdown(section.tldr)])]
