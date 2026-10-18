"""Research topics of the app and the pages that belong to them; the topics page and the breadcrumbs read it."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Collection, List, Optional, Tuple

from ui import ids
from ui.navigation import (
    ADVANTAGE_PATH,
    CAVEATS_PATH,
    GBS_PATH,
    GUIDE_PATH,
    LITERATURE_REVIEW_PATH,
    PORTFOLIO_PATH,
    QPURPOSE_PATH,
    RANDOM_MATRIX_PATH,
    RANDOM_MATRIX_GBS_PATH,
    THEORY_PATH,
    TOPICS_PATH,
    VQE_PAPER_PATH,
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
    ids.PORTFOLIO_PAGE, "1 · Klasické Monte Carlo", PORTFOLIO_PATH,
    "Simulace portfolia korelovaným geometrickým Brownovým pohybem, předvolby trhu z historie USA 1928–2023 "
    "a stresové scénáře.",
)
GBS = PageEntry(
    ids.GBS_PAGE, "2 · Monte Carlo na GBS", GBS_PATH,
    "Moment výnosu portfolia odhadnutý z četností fotonů Gaussian Boson Sampleru, krok za krokem od Wickovy věty "
    "po srovnání s klasickým Monte Carlem.",
)
ADVANTAGE = PageEntry(
    ids.ADVANTAGE_PAGE, "3 · Výhoda GBS", ADVANTAGE_PATH,
    "Laboratoř s vlastní maticí, pět úloh s exponenciální výhodou, skript pro Qiskit a rozbor tvrzení Qpurpose.",
)
THEORY = PageEntry(
    ids.THEORY_PAGE, "Teorie Monte Carla na GBS", THEORY_PATH,
    "Podrobný výklad každého kroku 2. stránky s českou i původní literaturou.", parent_page_id=ids.GBS_PAGE,
)
CAVEATS = PageEntry(
    ids.CAVEATS_PAGE, "Háčky Monte Carla na GBS", CAVEATS_PATH,
    "Kde má GBS odhad omezení a co se s nimi dá dělat.", parent_page_id=ids.GBS_PAGE,
)
GUIDE = PageEntry(
    ids.GUIDE_PAGE, "Průvodce pro začínajícího doktoranda", GUIDE_PATH,
    "13 kapitol o tom, proč a jak výhoda GBS funguje, včetně Qiskitu a námětů na další práci.",
    parent_page_id=ids.ADVANTAGE_PAGE,
)

QPURPOSE_CHECK = PageEntry(
    ids.QPURPOSE_PAGE, "Qpurpose: co skutečně prodávají", QPURPOSE_PATH,
    "Co má Qpurpose v provozu u Jyske Bank a jak to funguje, co z metody zbude na klasickém počítači a chyba, "
    "kterou jsme našli ve vzorci pro rozptyl GBS-I.",
    parent_page_id=ids.ADVANTAGE_PAGE,
)

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
        TopicSection("Výklad a literatura", (THEORY, CAVEATS, GUIDE, QPURPOSE_CHECK)),
    ),
)

VQE_PAPER = PageEntry(
    ids.VQE_PAPER_PAGE, "VQE na IBM Fez (De León a kol. 2025)", VQE_PAPER_PATH,
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
    "TL;DR a přehled literatury, patentů, hardwaru a kritiky: co je o Gaussian Boson Samplingu jako náhradě "
    "Monte Carla ve financích doložené, co ne a kde jsou otevřené otázky. Na konci kontrolní otázky.",
)

LITERATURE_REVIEW_TOPIC = ResearchTopic(
    anchor="tema-reserse-gbs",
    title="Rešerše: Gaussian Boson Sampling a finanční riziko",
    summary=(
        "Shrnutí rešerše k otázce, jestli může fotonický Gaussian Boson Sampler nahradit Monte Carlo při odhadu "
        "finančního rizika: případ Jyske Bank a Qpurpose, teorie, konkurenční výzkum, hardware a kritická "
        "literatura. Začni krátkým TL;DR, podrobnosti jsou v kapitolách."
    ),
    sections=(TopicSection("Přehled literatury", (LITERATURE_REVIEW,)),),
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

RANDOM_MATRIX_GBS = PageEntry(
    ids.RANDOM_MATRIX_GBS_PAGE, "Náhodné matice a GBS: hypotéza", RANDOM_MATRIX_GBS_PATH,
    "Vlastní námět: rozhoduje o výhodě GBS tvar spektra korelační matice? První výpočet na šesti aktivech, "
    "háček se šumem v odhadnuté matici a pět otevřených otázek.",
)

RESEARCH_DIRECTIONS_TOPIC = ResearchTopic(
    anchor="tema-vyzkumne-smery",
    title="Výzkumné směry",
    summary=(
        "Vlastní výzkumné náměty, které propojují ostatní témata. Nejsou to doložené výsledky: každá stránka "
        "odlišuje hypotézu, náš výpočet a literaturu a končí otázkami, na které by výzkum musel odpovědět."
    ),
    sections=(TopicSection("Náměty", (RANDOM_MATRIX_GBS,)),),
)

RESEARCH_TOPICS: Tuple[ResearchTopic, ...] = (
    MONTE_CARLO_TOPIC, LITERATURE_REVIEW_TOPIC, OPTIMIZATION_TOPIC, RANDOM_MATRIX_TOPIC, RESEARCH_DIRECTIONS_TOPIC,
)


def study_path(topic: ResearchTopic) -> Tuple[PageEntry, ...]:
    """Recommended study order: every main page directly followed by the subpages that explain it."""
    ordered: List[PageEntry] = []
    for page in topic.pages:
        if page.parent_page_id is None:
            ordered.append(page)
            ordered.extend(subpage for subpage in topic.pages if subpage.parent_page_id == page.page_id)
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


def breadcrumb_trail(page_id: str) -> List[Crumb]:
    """Témata › topic › parent page › page; empty for pages outside every topic."""
    for topic in RESEARCH_TOPICS:
        pages_by_id = {page.page_id: page for page in topic.pages}
        if page_id not in pages_by_id:
            continue
        page = pages_by_id[page_id]
        trail: List[Crumb] = [(TOPICS_TITLE, TOPICS_PATH), (topic.title, topic_href(topic))]
        if page.parent_page_id:
            parent = pages_by_id[page.parent_page_id]
            trail.append((parent.title, parent.path))
        trail.append((page.title, None))
        return trail
    return []
