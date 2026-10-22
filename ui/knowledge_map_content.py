"""Structure of the knowledge base: the central question, layers of pages and typed relations between pages."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from ui import ids

TITLE = "Mapa znalostí"
CENTRAL_QUESTION = (
    "Kdy může fotonický Gaussian Boson Sampler zrychlit Monte Carlo odhad finančního rizika – a jak z dat poznat, "
    "že selže?"
)
CENTRAL_QUESTION_SHORT = "Ústřední otázka"
INTRO = (
    "Celá aplikace stojí na jedné otázce a pět vrstev na ni odpovídá z různých stran: základy dávají jazyk, metody "
    "a laboratoře počítají, literatura a trh říkají, co je doložené, hardware ukazuje, kde se to dá spustit, a vlastní "
    "výzkum hledá, kde to selže. Klikni na uzel a uvidíš, s čím souvisí; vlastní propojení si můžeš přidat dole."
)
OWN_CONNECTIONS_HINT = (
    "Vlastní propojení se ukládají jen v tomto prohlížeči. Hodí se na poznámky typu „tohle by šlo použít tam“."
)


class Layer(str, Enum):
    FOUNDATIONS = "zaklady"
    METHODS = "metody"
    LITERATURE = "literatura"
    HARDWARE = "hardware"
    RESEARCH = "vyzkum"


@dataclass(frozen=True)
class LayerInfo:
    layer: Layer
    title: str
    role: str
    """What the layer contributes to the central question."""
    color: str
    page_ids: Tuple[str, ...]


LAYERS: Tuple[LayerInfo, ...] = (
    LayerInfo(
        Layer.FOUNDATIONS, "Základy", "matematika a fyzika, bez kterých se zbytek nedá číst", "#2e9e5b",
        (ids.INTEGRALS_CHEAT_SHEET_PAGE, ids.HAFNIAN_PAGE, ids.THEORY_PAGE, ids.ACADEMY_PAGE),
    ),
    LayerInfo(
        Layer.METHODS, "Metody a laboratoře", "výpočty, ve kterých si metody vyzkoušíš na číslech", "#2a6fdb",
        (
            ids.PORTFOLIO_PAGE, ids.GBS_PAGE, ids.ADVANTAGE_PAGE, ids.CAVEATS_PAGE, ids.GUIDE_PAGE,
            ids.RANDOM_MATRIX_PAGE,
        ),
    ),
    LayerInfo(
        Layer.LITERATURE, "Literatura a trh", "co je doložené, kdo co tvrdí a jak to obstojí", "#7b3fe4",
        (ids.LITERATURE_REVIEW_PAGE, ids.ANDERSEN_SHAN_PAPER_PAGE, ids.QPURPOSE_PAGE, ids.VQE_PAPER_PAGE),
    ),
    LayerInfo(
        Layer.HARDWARE, "Hardware", "kde a na čem se dá výpočet skutečně spustit", "#d9822b",
        (ids.PHOTONIC_HARDWARE_PAGE,),
    ),
    LayerInfo(
        Layer.RESEARCH, "Vlastní výzkum", "otevřené otázky a hypotézy disertace", "#c53d3d",
        (ids.FAILURE_DIAGNOSTICS_PAGE, ids.RANDOM_MATRIX_GBS_PAGE),
    ),
)


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
