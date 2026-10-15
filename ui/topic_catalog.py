"""Research topics of the app and the pages that belong to them; the topics page and the breadcrumbs read it."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from ui import ids
from ui.navigation import (
    ADVANTAGE_PATH,
    CAVEATS_PATH,
    GBS_PATH,
    GUIDE_PATH,
    PORTFOLIO_PATH,
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
        TopicSection("Výklad a literatura", (THEORY, CAVEATS, GUIDE)),
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

RESEARCH_TOPICS: Tuple[ResearchTopic, ...] = (MONTE_CARLO_TOPIC, OPTIMIZATION_TOPIC)


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
