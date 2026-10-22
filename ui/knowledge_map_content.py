"""Structure of the knowledge base: the central question, groups of pages and typed relations between pages."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from ui import ids

CENTRAL_QUESTION = (
    "Kdy může fotonický Gaussian Boson Sampler zrychlit Monte Carlo odhad finančního rizika – a jak z dat poznat, "
    "že selže?"
)
CENTRAL_QUESTION_SHORT = "Ústřední otázka"
OWN_CONNECTIONS_HINT = (
    "Propoj dvě stránky nebo svá podtémata, třeba „tohle by šlo použít tam“. Ukládá se jen v tomto prohlížeči."
)
SUBTOPICS_HINT = (
    "Když tě při studiu něco zavede hlouběji, založ si podtéma: název, poznámka a stránky, které rozvíjí. Na mapě se "
    "objeví jako kosočtverec u první vybrané stránky a dál ho můžeš propojovat s dalšími tématy."
)
BACKUP_HINT = (
    "Podtémata a propojení se ukládají jen v tomto prohlížeči. Záloha je soubor JSON, který jde nahrát na jiném "
    "zařízení nebo po smazání dat prohlížeče; nahrání ji přidá ke stávajícím poznámkám."
)


class Layer(str, Enum):
    FINANCE = "finance"
    PHOTONICS = "fotonika"
    CORE = "gbs-ve-financich"
    RESEARCH = "vyzkum"
    FOUNDATIONS = "zaklady"


@dataclass(frozen=True)
class LayerInfo:
    layer: Layer
    title: str
    role: str
    """What the group contributes to the central question."""
    color: str
    page_ids: Tuple[str, ...]
    menu_id: str
    """The drop-down of the top navigation that lists the pages of the group."""

    @property
    def anchor(self) -> str:
        """Section of the group on the topics dashboard; breadcrumbs link to it."""
        return f"skupina-{self.layer.value}"


LAYERS: Tuple[LayerInfo, ...] = (
    LayerInfo(
        Layer.FINANCE, "Finance a riziko", "co se ve financích počítá a čím se to dělá dnes", "#2a6fdb",
        (ids.PORTFOLIO_PAGE, ids.RANDOM_MATRIX_PAGE, ids.VQE_PAPER_PAGE),
        ids.NAV_FINANCE_MENU,
    ),
    LayerInfo(
        Layer.PHOTONICS, "Fotonika a GBS", "kvantová optika, na které GBS stojí, a hardware, na kterém běží", "#d9822b",
        (ids.HAFNIAN_PAGE, ids.PHOTONIC_HARDWARE_PAGE),
        ids.NAV_PHOTONICS_MENU,
    ),
    LayerInfo(
        Layer.CORE, "GBS ve financích", "průnik obou oborů a jádro disertace: odhad rizika z výstřelů GBS", "#7b3fe4",
        (
            ids.GBS_PAGE, ids.THEORY_PAGE, ids.CAVEATS_PAGE, ids.ADVANTAGE_PAGE, ids.GUIDE_PAGE,
            ids.ANDERSEN_SHAN_PAPER_PAGE, ids.QPURPOSE_PAGE, ids.LITERATURE_REVIEW_PAGE,
        ),
        ids.NAV_CORE_MENU,
    ),
    LayerInfo(
        Layer.RESEARCH, "Vlastní výzkum", "otevřené otázky a hypotézy disertace", "#c53d3d",
        (ids.FAILURE_DIAGNOSTICS_PAGE, ids.RANDOM_MATRIX_GBS_PAGE),
        ids.NAV_RESEARCH_MENU,
    ),
    LayerInfo(
        Layer.FOUNDATIONS, "Základy", "matematika a zdroje pro samostudium", "#2e9e5b",
        (ids.INTEGRALS_CHEAT_SHEET_PAGE, ids.ACADEMY_PAGE),
        ids.NAV_FOUNDATIONS_MENU,
    ),
)
"""Five groups: the two fields, their intersection, our own research and the foundations."""


MAP_LABELS = {
    ids.INTEGRALS_CHEAT_SHEET_PAGE: "Tahák: integrály",
    ids.HAFNIAN_PAGE: "Hafnián a permanent",
    ids.THEORY_PAGE: "Teorie MC na GBS",
    ids.ACADEMY_PAGE: "Quantum Academy",
    ids.PORTFOLIO_PAGE: "1 · Klasické MC",
    ids.GBS_PAGE: "2 · MC na GBS",
    ids.ADVANTAGE_PAGE: "3 · Výhoda GBS",
    ids.CAVEATS_PAGE: "Háčky MC na GBS",
    ids.GUIDE_PAGE: "Průvodce doktoranda",
    ids.RANDOM_MATRIX_PAGE: "Náhodné matice",
    ids.LITERATURE_REVIEW_PAGE: "Rešerše GBS",
    ids.ANDERSEN_SHAN_PAPER_PAGE: "Článek Andersena a Shan",
    ids.QPURPOSE_PAGE: "Qpurpose",
    ids.VQE_PAPER_PAGE: "VQE na IBM Fez",
    ids.PHOTONIC_HARDWARE_PAGE: "Quandela a hardware v Evropě",
    ids.FAILURE_DIAGNOSTICS_PAGE: "Kdy GBS selže",
    ids.RANDOM_MATRIX_GBS_PAGE: "Náhodné matice a GBS",
}
"""Short labels for the map; the full page titles are in the hover text and in the details."""


class RelationKind(str, Enum):
    FOLLOWS = "navazuje"
    EXPLAINS = "vysvetluje"
    BASED_ON = "vychazi"
    CHECKS = "proveruje"
    MOTIVATES = "motivuje"
    CONTRASTS = "srovnava"
    EXPANDS = "rozviji"


@dataclass(frozen=True)
class RelationKindInfo:
    kind: RelationKind
    label: str
    """Reads as „zdroj <label> cíl“."""
    color: str


RELATION_KINDS: Tuple[RelationKindInfo, ...] = (
    RelationKindInfo(RelationKind.FOLLOWS, "pokračuje na", "#5b6474"),
    RelationKindInfo(RelationKind.EXPLAINS, "vysvětluje", "#2e9e5b"),
    RelationKindInfo(RelationKind.BASED_ON, "vychází z", "#7b3fe4"),
    RelationKindInfo(RelationKind.CHECKS, "prověřuje", "#d9822b"),
    RelationKindInfo(RelationKind.MOTIVATES, "otevírá otázku pro", "#c53d3d"),
    RelationKindInfo(RelationKind.CONTRASTS, "srovnává se", "#9aa3b2"),
    RelationKindInfo(RelationKind.EXPANDS, "rozvíjí", "#139a9a"),
)


@dataclass(frozen=True)
class Relation:
    source: str
    kind: RelationKind
    target: str
    note: str


RELATIONS: Tuple[Relation, ...] = (
    Relation(ids.PORTFOLIO_PAGE, RelationKind.FOLLOWS, ids.GBS_PAGE, "od losování scénářů k odhadu z fotonů"),
    Relation(ids.GBS_PAGE, RelationKind.FOLLOWS, ids.ADVANTAGE_PAGE, "od momentu portfolia k obecným gaussovským úlohám"),
    Relation(ids.LITERATURE_REVIEW_PAGE, RelationKind.FOLLOWS, ids.PHOTONIC_HARDWARE_PAGE, "kdo by úlohu spustil"),
    Relation(
        ids.FAILURE_DIAGNOSTICS_PAGE, RelationKind.FOLLOWS, ids.RANDOM_MATRIX_GBS_PAGE,
        "podrobný rozbor 2. a 3. zdroje chyby",
    ),
    Relation(ids.INTEGRALS_CHEAT_SHEET_PAGE, RelationKind.EXPLAINS, ids.PORTFOLIO_PAGE, "Monte Carlo jako odhad integrálu"),
    Relation(
        ids.INTEGRALS_CHEAT_SHEET_PAGE, RelationKind.EXPLAINS, ids.ANDERSEN_SHAN_PAPER_PAGE,
        "gaussovské integrály a podmínka (A1)",
    ),
    Relation(ids.HAFNIAN_PAGE, RelationKind.EXPLAINS, ids.GBS_PAGE, "proč jsou pravděpodobnosti GBS hafniány"),
    Relation(
        ids.HAFNIAN_PAGE, RelationKind.EXPLAINS, ids.PHOTONIC_HARDWARE_PAGE,
        "permanent proti hafniánu = boson sampling proti GBS",
    ),
    Relation(ids.THEORY_PAGE, RelationKind.EXPLAINS, ids.GBS_PAGE, "každý krok 2. stránky podrobně"),
    Relation(ids.GUIDE_PAGE, RelationKind.EXPLAINS, ids.ADVANTAGE_PAGE, "proč a kdy je výhoda exponenciální"),
    Relation(ids.ACADEMY_PAGE, RelationKind.EXPLAINS, ids.PHOTONIC_HARDWARE_PAGE, "Perceval, Classiq, CUDA-Q"),
    Relation(ids.ADVANTAGE_PAGE, RelationKind.BASED_ON, ids.ANDERSEN_SHAN_PAPER_PAGE, "odhady GBS-I a GBS-P"),
    Relation(ids.QPURPOSE_PAGE, RelationKind.BASED_ON, ids.ANDERSEN_SHAN_PAPER_PAGE, "Qpurpose prodává metodu z článku"),
    Relation(
        ids.LITERATURE_REVIEW_PAGE, RelationKind.BASED_ON, ids.ANDERSEN_SHAN_PAPER_PAGE,
        "hlavní teoretický zdroj rešerše",
    ),
    Relation(
        ids.RANDOM_MATRIX_GBS_PAGE, RelationKind.BASED_ON, ids.RANDOM_MATRIX_PAGE,
        "spektrum korelační matice a šum v ní",
    ),
    Relation(ids.CAVEATS_PAGE, RelationKind.CHECKS, ids.GBS_PAGE, "kde má odhad z fotonů omezení"),
    Relation(
        ids.QPURPOSE_PAGE, RelationKind.CHECKS, ids.ADVANTAGE_PAGE,
        "co z výhody zbude na klasickém počítači a chyba ve vzorci",
    ),
    Relation(ids.LITERATURE_REVIEW_PAGE, RelationKind.CHECKS, ids.QPURPOSE_PAGE, "případ Jyske Bank"),
    Relation(ids.CAVEATS_PAGE, RelationKind.MOTIVATES, ids.FAILURE_DIAGNOSTICS_PAGE, "omezení GBS jako výzkumná otázka"),
    Relation(
        ids.HAFNIAN_PAGE, RelationKind.MOTIVATES, ids.FAILURE_DIAGNOSTICS_PAGE,
        "skutečné výnosy mají tlustší chvosty, než hafnián předpovídá",
    ),
    Relation(ids.RANDOM_MATRIX_PAGE, RelationKind.MOTIVATES, ids.RANDOM_MATRIX_GBS_PAGE, "šum v odhadnuté matici"),
    Relation(
        ids.PHOTONIC_HARDWARE_PAGE, RelationKind.MOTIVATES, ids.FAILURE_DIAGNOSTICS_PAGE,
        "šum zdroje fotonů vychyluje odhad",
    ),
    Relation(
        ids.VQE_PAPER_PAGE, RelationKind.CONTRASTS, ids.LITERATURE_REVIEW_PAGE,
        "hradlová optimalizace proti fotonickému vzorkování",
    ),
)
