"""Research topics of the app and the pages that belong to them; the topics page and the breadcrumbs read it."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Collection, Dict, List, Optional, Tuple

from assistant.topics import TopicPage
from ui import ids
from ui.generated_topics import GENERATED_SECTION_TITLE, GENERATED_TOPICS, generated_page_id, generated_path
from ui.knowledge_map_content import LAYERS, LayerInfo
from ui.navigation import (
    ACADEMY_PATH,
    ADVANTAGE_PATH,
    ANDERSEN_SHAN_PAPER_PATH,
    CAVEATS_PATH,
    FAILURE_DIAGNOSTICS_PATH,
    GBS_PATH,
    GUIDE_PATH,
    HAFNIAN_PATH,
    INTEGRALS_CHEAT_SHEET_PATH,
    LITERATURE_REVIEW_PATH,
    PHOTONIC_HARDWARE_PATH,
    PHOTONICS_LANDSCAPE_PATH,
    PHOTONICS_TOPIC_ANCHOR,
    PIQUASSO_PATH,
    PSIQUANTUM_PATH,
    PORTFOLIO_PATH,
    PRIMER_APPENDICES_PATH,
    PRIMER_BASICS_PATH,
    PRIMER_GAUSSIAN_STATES_PATH,
    PRIMER_GBS_PATH,
    PRIMER_PHASE_SPACE_PATH,
    QPURPOSE_PATH,
    RANDOM_MATRIX_PATH,
    RANDOM_MATRIX_GBS_PATH,
    THEORY_PATH,
    TOPICS_PATH,
    VQE_PAPER_PATH,
    WALTHER_LECTURE_PATH,
    GHZ_STATES_PATH,
)

TOPICS_TITLE = "Témata"


@dataclass(frozen=True)
class PageEntry:
    page_id: str
    title: str
    path: str
    description: str
    parent_page_id: Optional[str] = None
    """Subpages (theory, caveats, guide) sit under the page they explain."""


@dataclass(frozen=True)
class TopicSection:
    title: str
    pages: Tuple[PageEntry, ...]


@dataclass(frozen=True)
class ResearchTopic:
    anchor: str
    title: str
    summary: str
    sections: Tuple[TopicSection, ...]

    @property
    def pages(self) -> Tuple[PageEntry, ...]:
        return tuple(page for section in self.sections for page in section.pages)


@dataclass(frozen=True)
class StudyStep:
    topic: ResearchTopic
    number: int
    """1-based position of the page in the recommended study order of its topic."""
    total: int
    previous: Optional[PageEntry]
    next: Optional[PageEntry]


Crumb = Tuple[str, Optional[str]]
"""Label and link; the current page has no link."""

PORTFOLIO = PageEntry(
    ids.PORTFOLIO_PAGE, "Klasické Monte Carlo", PORTFOLIO_PATH,
    "Simulace portfolia korelovaným geometrickým Brownovým pohybem, předvolby trhu z historie USA 1928–2023 "
    "a stresové scénáře.",
)
GBS = PageEntry(
    ids.GBS_PAGE, "Monte Carlo na GBS", GBS_PATH,
    "Moment výnosu portfolia odhadnutý z četností fotonů Gaussian Boson Sampleru, krok za krokem od Wickovy věty "
    "po srovnání s klasickým Monte Carlem.",
)
ADVANTAGE = PageEntry(
    ids.ADVANTAGE_PAGE, "Výhoda GBS", ADVANTAGE_PATH,
    "Laboratoř s vlastní maticí, pět úloh s exponenciální výhodou, skript pro Qiskit a rozbor tvrzení Qpurpose.",
)
THEORY = PageEntry(
    ids.THEORY_PAGE, "Teorie Monte Carla na GBS", THEORY_PATH,
    "Podrobný výklad každého kroku stránky „Monte Carlo na GBS“ s českou i původní literaturou.",
    parent_page_id=ids.GBS_PAGE,
)
HAFNIAN = PageEntry(
    ids.HAFNIAN_PAGE, "Hafnián a permanent polopatě", HAFNIAN_PATH,
    "Co jsou hafnián a permanent, v čem se liší (i v datových strukturách a kódu), proč se objevují ve financích "
    "a v GBS a co na to říkají skutečná data o nemovitostech.",
    parent_page_id=ids.GBS_PAGE,
)
CAVEATS = PageEntry(
    ids.CAVEATS_PAGE, "Háčky Monte Carla na GBS", CAVEATS_PATH,
    "Kde má GBS odhad omezení a co se s nimi dá dělat.", parent_page_id=ids.GBS_PAGE,
)
GUIDE = PageEntry(
    ids.GUIDE_PAGE, "Průvodce: proč a jak funguje výhoda GBS", GUIDE_PATH,
    "13 kapitol o tom, proč a jak výhoda GBS funguje, včetně Qiskitu a námětů na další práci.",
    parent_page_id=ids.ADVANTAGE_PAGE,
)

QPURPOSE_CHECK = PageEntry(
    ids.QPURPOSE_PAGE, "Qpurpose: co skutečně prodávají", QPURPOSE_PATH,
    "Co má Qpurpose v provozu u Jyske Bank a jak to funguje, co z metody zbude na klasickém počítači a chyba, "
    "kterou jsme našli ve vzorci pro rozptyl GBS-I.",
    parent_page_id=ids.ADVANTAGE_PAGE,
)

ANDERSEN_SHAN_PAPER = PageEntry(
    ids.ANDERSEN_SHAN_PAPER_PAGE, "Článek Andersena a Shan krok za krokem", ANDERSEN_SHAN_PAPER_PATH,
    "Čtení s komentářem k hlavnímu článku o výhodě GBS: motivace, zadání gaussovské úlohy, multiindexy, hustota "
    "normálního rozdělení a podmínka (A1), každý vzorec po částech a s příkladem.",
    parent_page_id=ids.ADVANTAGE_PAGE,
)

ACADEMY = PageEntry(
    ids.ACADEMY_PAGE, "Quantum Academy", ACADEMY_PATH,
    "Kurzy, videa, blogy a platformy (Classiq, CUDA-Q, Quandela) pro samostudium kvantového počítání.",
)
"""Not part of any study path, but of the foundations group in the menu, on the dashboard and in the map."""

MONTE_CARLO_TOPIC = ResearchTopic(
    anchor="tema-monte-carlo",
    title="Monte Carlo a modifikované Monte Carlo",
    summary=(
        "Jak odhadovat střední hodnoty náhodných veličin: klasicky losováním scénářů a modifikovaně pomocí "
        "Gaussian Boson Sampleru, fotonického kvantového přístroje. Od simulace portfolia přes Monte Carlo na GBS "
        "po tvrzení firmy Qpurpose o exponenciální výhodě."
    ),
    sections=(
        TopicSection("Klasické Monte Carlo", (PORTFOLIO,)),
        TopicSection("Modifikované Monte Carlo: Gaussian Boson Sampling", (GBS, ADVANTAGE)),
        TopicSection("Výklad a literatura", (THEORY, HAFNIAN, CAVEATS, GUIDE, ANDERSEN_SHAN_PAPER, QPURPOSE_CHECK)),
    ),
)

VQE_PAPER = PageEntry(
    ids.VQE_PAPER_PAGE, "Článek De Leóna a kol.: VQE na IBM Fez", VQE_PAPER_PATH,
    "TL;DR článku o dynamické optimalizaci portfolia až 38 aktiv na 156qubitovém čipu: jak funguje VQE s opravou "
    "ISQR, co znamená „srovnatelné s CPLEX“ a proč to není kvantová výhoda.",
)

OPTIMIZATION_TOPIC = ResearchTopic(
    anchor="tema-kvantova-optimalizace",
    title="Kvantová optimalizace portfolia",
    summary=(
        "Výběr portfolia jako hledání základního stavu Isingova hamiltoniánu (QUBO) a variační kvantové algoritmy, "
        "které ho řeší na dnešních šumných čipech. Rozbory článků s ověřenými čísly a kritickým hodnocením."
    ),
    sections=(TopicSection("Rozbory článků", (VQE_PAPER,)),),
)


LITERATURE_REVIEW = PageEntry(
    ids.LITERATURE_REVIEW_PAGE, "Rešerše: GBS pro odhad finančního rizika", LITERATURE_REVIEW_PATH,
    "TL;DR a přehled literatury, patentů, hardwaru a kritiky: co je o Gaussian Boson Samplingu jako zdroji vzorků "
    "pro Monte Carlo ve financích doložené, co ne a kde jsou otevřené otázky. Na konci kontrolní otázky.",
)

PHOTONIC_HARDWARE = PageEntry(
    ids.PHOTONIC_HARDWARE_PAGE, "Quandela a fotonický hardware v Evropě", PHOTONIC_HARDWARE_PATH,
    "Co dělá Quandela, jak funguje jejich hardware a software Perceval, co z toho jde použít na modifikované "
    "Monte Carlo a kdo v Evropě umí spustit GBS se stlačeným světlem.",
    parent_page_id=ids.LITERATURE_REVIEW_PAGE,
)

LITERATURE_REVIEW_TOPIC = ResearchTopic(
    anchor="tema-reserse-gbs",
    title="Rešerše: Gaussian Boson Sampling a finanční riziko",
    summary=(
        "Shrnutí rešerše k otázce, jestli může fotonický Gaussian Boson Sampler jako zdroj vzorků zrychlit Monte "
        "Carlo odhad finančního rizika: případ Jyske Bank a Qpurpose, teorie, konkurenční výzkum, hardware a kritická "
        "literatura. Začni krátkým TL;DR, podrobnosti jsou v kapitolách."
    ),
    sections=(TopicSection("Přehled literatury", (LITERATURE_REVIEW, PHOTONIC_HARDWARE)),),
)

PHOTONICS_LANDSCAPE = PageEntry(
    ids.PHOTONICS_LANDSCAPE_PAGE, "Fotonika ve světě: konkurence a partneři", PHOTONICS_LANDSCAPE_PATH,
    "Kdo ve světě staví fotonické kvantové počítače, co prodává a kdo dodává součástky; tabulka, kdo umí GBS, "
    "a odhad, kdo je pro disertaci konkurence a kdo partner.",
)

PIQUASSO = PageEntry(
    ids.PIQUASSO_PAGE, "Piquasso: simulátor fotonického kvantového počítače", PIQUASSO_PATH,
    "Open-source simulátor z Budapešti: jak v něm napsat GBS, který simulátor zvolit, ověření výpočtů aplikace, "
    "pasti s ořezy a překlad mezi qubity a fotony včetně otázky, jestli jde GBS spustit na VLQ.",
    parent_page_id=ids.PHOTONICS_LANDSCAPE_PAGE,
)

PSIQUANTUM = PageEntry(
    ids.PSIQUANTUM_PAGE, "PsiQuantum: cesta od Rudolphova plánu k milionu qubitů", PSIQUANTUM_PATH,
    "Zakladatelé, jak se plán z roku 2017 změnil ve fúzní kvantové počítání, čipy Omega z GlobalFoundries, peníze "
    "a vládní zakázky, stavby v Brisbane a Chicagu s posouvanými termíny, kritika a videa a články k samostudiu.",
    parent_page_id=ids.PHOTONICS_LANDSCAPE_PAGE,
)

PRIMER_BASICS = PageEntry(
    ids.PRIMER_BASICS_PAGE, "Skripta 1: Základy fotonického kvantového počítání", PRIMER_BASICS_PATH,
    "Úvod a 1. kapitola skript Kolarovszkiho a Zimboráse v češtině: Fockův prostor, kvantové módy, fotonická "
    "hradla, interferometry a permanent, měření počtu fotonů, Boson Sampling a ztráty fotonů.",
)
PRIMER_GAUSSIAN_STATES = PageEntry(
    ids.PRIMER_GAUSSIAN_STATES_PAGE, "Skripta 2: Gaussovské stavy", PRIMER_GAUSSIAN_STATES_PATH,
    "Stlačené a koherentní stavy, lineární hradla a symplektická grupa, kovarianční matice, rozklad na normální "
    "módy a Blochův–Messiahův rozklad.",
)
PRIMER_PHASE_SPACE = PageEntry(
    ids.PRIMER_PHASE_SPACE_PAGE, "Skripta 3: Kvantová optika ve fázovém prostoru", PRIMER_PHASE_SPACE_PATH,
    "Weylovy operátory a koherentní stavy, charakteristické funkce, Wignerova funkce, P-reprezentace a Husimiho "
    "Q-funkce: jazyk, ve kterém se gaussovské stavy popisují nejpřirozeněji.",
)
PRIMER_GBS = PageEntry(
    ids.PRIMER_GBS_PAGE, "Skripta 4: Gaussian Boson Sampling", PRIMER_GBS_PATH,
    "Pravděpodobnosti detekce fotonů v gaussovských stavech, hafnián a perfektní párování v grafech a hledání "
    "hustých podgrafů pomocí GBS.",
)
PRIMER_APPENDICES = PageEntry(
    ids.PRIMER_APPENDICES_PAGE, "Skripta A–B: Kvantová mechanika a první kvantování", PRIMER_APPENDICES_PATH,
    "Dodatky skript: opakování kvantové mechaniky (Hilbertovy prostory, stavy, vývoj, měření, složené systémy, "
    "harmonický oscilátor) a odvození obsazovacích čísel z prvního kvantování.",
)

WALTHER_LECTURE = PageEntry(
    ids.WALTHER_LECTURE_PAGE, "Přednáška: Walther o fotonickém kvantovém počítání (2022)", WALTHER_LECTURE_PATH,
    "Zápisky ze Schrödingerovy přednášky Philipa Walthera (Vídeň 2022) se všemi slajdy: zdroje fotonů, čipy "
    "a detektory, hradla KLM, klastrové stavy a fúze, slepé počítání, superpozice pořadí hradel a boson sampling.",
)

GHZ_STATES = PageEntry(
    ids.GHZ_STATES_PAGE, "GHZ stavy: od Greenbergera, Horna a Zeilingera k fotonickému počítači", GHZ_STATES_PATH,
    "Co je třífotonový GHZ stav, Bellova věta bez nerovností, první GHZ z fotonů ve Vídni (1999), proč plán "
    "fotonického počítače potřebuje právě tři fotony a kde se dnes ohlašované a deterministické GHZ stavy berou.",
    parent_page_id=ids.WALTHER_LECTURE_PAGE,
)

PHOTONICS_TOPIC = ResearchTopic(
    anchor=PHOTONICS_TOPIC_ANCHOR,
    title="Fotonika",
    summary=(
        "Fotonické kvantové počítání od základů: česky přeložená skripta Kolarovszkiho a Zimboráse (IT4I, 2025) "
        "o Fockově prostoru, gaussovských stavech, fázovém prostoru a Gaussian Boson Samplingu, potom přehled firem "
        "a výzkumných skupin, které fotonický hardware stavějí, simulátor Piquasso od autorů skript a zápisky "
        "z přednášky Philipa Walthera."
    ),
    sections=(
        TopicSection(
            "Skripta: fotonické kvantové počítání a GBS",
            (PRIMER_BASICS, PRIMER_GAUSSIAN_STATES, PRIMER_PHASE_SPACE, PRIMER_GBS, PRIMER_APPENDICES),
        ),
        TopicSection("Firmy a výzkum", (PHOTONICS_LANDSCAPE, PSIQUANTUM)),
        TopicSection("Software", (PIQUASSO,)),
        TopicSection("Přednášky", (WALTHER_LECTURE, GHZ_STATES)),
    ),
)

RANDOM_MATRIX = PageEntry(
    ids.RANDOM_MATRIX_PAGE, "Náhodné matice a riziko portfolia", RANDOM_MATRIX_PATH,
    "Laboratoř se syntetickým trhem a výklad: Marčenkovo–Pasturovo rozdělení, proč Markowitz podhodnocuje riziko, "
    "čištění korelační matice, stavy trhu a fázový přechod u Expected Shortfall.",
)

RANDOM_MATRIX_TOPIC = ResearchTopic(
    anchor="tema-nahodne-matice",
    title="Náhodné matice: od kvantového chaosu k portfoliu",
    summary=(
        "Teorie náhodných matic vznikla pro spektra jader a chaotických kvantových systémů. Od roku 1999 slouží "
        "i k tomu, aby se v korelační matici akcií oddělila informace od šumu. Jde o doložený a v praxi používaný "
        "přenos poznatků z kvantového chaosu do řízení portfolií."
    ),
    sections=(TopicSection("Laboratoř a výklad", (RANDOM_MATRIX,)),),
)

FAILURE_DIAGNOSTICS = PageEntry(
    ids.FAILURE_DIAGNOSTICS_PAGE, "Kdy odhad rizika přes GBS selže", FAILURE_DIAGNOSTICS_PATH,
    "Vlastní námět: tři zdroje chyby – negaussovská data, matice a portfolio, pro které GBS nemá výhodu, a šum "
    "v odhadnuté matici – a jak každý z nich poznat z dat dřív, než se přístroj spustí.",
)
RANDOM_MATRIX_GBS = PageEntry(
    ids.RANDOM_MATRIX_GBS_PAGE, "Náhodné matice a GBS: hypotéza", RANDOM_MATRIX_GBS_PATH,
    "Podrobný rozbor 2. a 3. zdroje chyby: jak o úspoře vzorků rozhoduje spektrum spolu s polohou vah portfolia "
    "(šest aktiv, dvě portfolia), šum v odhadnuté matici a šest otevřených otázek.",
    parent_page_id=ids.FAILURE_DIAGNOSTICS_PAGE,
)

RESEARCH_DIRECTIONS_TOPIC = ResearchTopic(
    anchor="tema-vyzkumne-smery",
    title="Vlastní výzkum",
    summary=(
        "Vlastní výzkumné náměty, které propojují ostatní témata. Nejsou to doložené výsledky: každá stránka "
        "odlišuje hypotézu, náš výpočet a literaturu a končí otázkami, na které by výzkum musel odpovědět."
    ),
    sections=(TopicSection("Náměty", (FAILURE_DIAGNOSTICS, RANDOM_MATRIX_GBS)),),
)

INTEGRALS_CHEAT_SHEET = PageEntry(
    ids.INTEGRALS_CHEAT_SHEET_PAGE, "Tahák: integrály", INTEGRALS_CHEAT_SHEET_PATH,
    "Kuchařka základních integrálů, per partes, substituce, určitý a nevlastní integrál, Fubiniova věta "
    "a gaussovské integrály, na kterých stojí GBS a Monte Carlo.",
)

CHEAT_SHEETS_TOPIC = ResearchTopic(
    anchor="tema-tahaky",
    title="Matematické taháky",
    summary=(
        "Stručné přehledy matematiky, kterou potřebují ostatní témata: vzorce a pravidla s krátkými příklady "
        "a odkazy na výklad v aplikaci i na videa a učebnice."
    ),
    sections=(TopicSection("Taháky", (INTEGRALS_CHEAT_SHEET,)),),
)

BASE_RESEARCH_TOPICS: Tuple[ResearchTopic, ...] = (
    MONTE_CARLO_TOPIC, LITERATURE_REVIEW_TOPIC, PHOTONICS_TOPIC, RESEARCH_DIRECTIONS_TOPIC,
    RANDOM_MATRIX_TOPIC, OPTIMIZATION_TOPIC, CHEAT_SHEETS_TOPIC,
)
"""In the order of the story: the method, what the literature says, who builds the hardware, our own research,
its supporting topic, a contrasting quantum approach and the maths cheat sheets."""

EXPANDED_TOPIC = ResearchTopic(
    anchor="tema-rozvedena",
    title=GENERATED_SECTION_TITLE,
    summary=(
        "Témata, která asistent rozvedl z úryvků ostatních stránek a která jsi schválil. Píše je model Claude podle "
        "nalezených zdrojů, tvrzení proto ověřuj podle odkazů na konci každé stránky. V menu a na mapě je každé "
        "u stránky, ze které vzešlo."
    ),
    sections=(),
)
"""Accepted topics stay apart from the hand-written study paths; a topic file can name another topic to join."""


def generated_entry(topic: TopicPage) -> PageEntry:
    return PageEntry(
        generated_page_id(topic.slug), topic.title, generated_path(topic.slug), topic.description,
        parent_page_id=topic.placement.parent_page_id,
    )


def topics_with(topics: Tuple[ResearchTopic, ...], generated: Collection[TopicPage]) -> Tuple[ResearchTopic, ...]:
    """Accepted topics join the topic their file names, in a section of their own; the rest form EXPANDED_TOPIC."""
    anchors = {topic.anchor for topic in topics}
    extended = []
    for topic in topics:
        pages = tuple(generated_entry(page) for page in generated if page.placement.topic_anchor == topic.anchor)
        if pages:
            topic = replace(topic, sections=topic.sections + (TopicSection(GENERATED_SECTION_TITLE, pages),))
        extended.append(topic)
    homeless = tuple(generated_entry(page) for page in generated if page.placement.topic_anchor not in anchors)
    if homeless:
        extended.append(replace(EXPANDED_TOPIC, sections=(TopicSection("Stránky", homeless),)))
    return tuple(extended)


RESEARCH_TOPICS = topics_with(BASE_RESEARCH_TOPICS, GENERATED_TOPICS)


def study_path(topic: ResearchTopic) -> Tuple[PageEntry, ...]:
    """Recommended study order: every page directly followed by the subpages that explain it, at any depth.

    A page whose parent is in another topic starts a branch of its own.
    """
    in_topic = {page.page_id for page in topic.pages}
    ordered: List[PageEntry] = []

    def add_with_subpages(page: PageEntry) -> None:
        ordered.append(page)
        for subpage in topic.pages:
            if subpage.parent_page_id == page.page_id:
                add_with_subpages(subpage)

    for page in topic.pages:
        if page.parent_page_id not in in_topic:
            add_with_subpages(page)
    return tuple(ordered)


def study_step(page_id: str) -> Optional[StudyStep]:
    for topic in RESEARCH_TOPICS:
        path = study_path(topic)
        page_ids = [page.page_id for page in path]
        if page_id not in page_ids:
            continue
        index = page_ids.index(page_id)
        return StudyStep(
            topic=topic,
            number=index + 1,
            total=len(path),
            previous=path[index - 1] if index > 0 else None,
            next=path[index + 1] if index + 1 < len(path) else None,
        )
    return None


def next_unstudied_page(topic: ResearchTopic, studied_page_ids: Collection[str]) -> Optional[PageEntry]:
    return next((page for page in study_path(topic) if page.page_id not in studied_page_ids), None)


def section_title(topic: ResearchTopic, page_id: str) -> str:
    return next(section.title for section in topic.sections if any(page.page_id == page_id for page in section.pages))


def topic_href(topic: ResearchTopic) -> str:
    return f"{TOPICS_PATH}#{topic.anchor}"


def page_entries() -> Dict[str, PageEntry]:
    """Every page that belongs to a group: the pages of all topics and Quantum Academy."""
    entries = {page.page_id: page for topic in RESEARCH_TOPICS for page in topic.pages}
    entries[ACADEMY.page_id] = ACADEMY
    return entries


def group_of(page_id: str) -> Optional[LayerInfo]:
    return next((info for info in LAYERS if page_id in info.page_ids), None)


def group_href(group: LayerInfo) -> str:
    return f"{TOPICS_PATH}#{group.anchor}"


def breadcrumb_trail(page_id: str) -> List[Crumb]:
    """Témata › group › parent page (when it is in the same group) › page, the same groups as the top menu.

    Empty for the topics dashboard and the knowledge map, which sit outside the groups.
    """
    group = group_of(page_id)
    if group is None:
        return []
    entries = page_entries()
    page = entries[page_id]
    trail: List[Crumb] = [(TOPICS_TITLE, TOPICS_PATH), (group.title, group_href(group))]
    if page.parent_page_id in group.page_ids:
        parent = entries[page.parent_page_id]
        trail.append((parent.title, parent.path))
    trail.append((page.title, None))
    return trail


def placement_for(page_id: str) -> Optional[Dict[str, Optional[str]]]:
    """Where a topic expanded from this page belongs: the page's group, the expanded topics, under the page itself.

    None for pages outside every group (the topics dashboard), which have nothing to expand.
    """
    group = group_of(page_id)
    if group is None:
        return None
    return {"layer": group.layer.value, "topic_anchor": EXPANDED_TOPIC.anchor, "parent_page_id": page_id}
