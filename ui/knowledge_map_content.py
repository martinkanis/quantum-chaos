"""Structure of the knowledge base: the central question, groups of pages and typed relations between pages."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Collection, Tuple

from assistant.topics import TopicPage
from ui import ids
from ui.generated_topics import GENERATED_TOPICS, generated_page_id

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


BASE_LAYERS: Tuple[LayerInfo, ...] = (
    LayerInfo(
        Layer.FINANCE, "Finance a riziko", "co se ve financích počítá a čím se to dělá dnes", "#2a6fdb",
        (ids.PORTFOLIO_PAGE, ids.RANDOM_MATRIX_PAGE, ids.VQE_PAPER_PAGE),
        ids.NAV_FINANCE_MENU,
    ),
    LayerInfo(
        Layer.PHOTONICS, "Fotonika a GBS", "kvantová optika, na které GBS stojí, a hardware, na kterém běží", "#d9822b",
        (
            ids.PRIMER_BASICS_PAGE, ids.PRIMER_GAUSSIAN_STATES_PAGE, ids.PRIMER_PHASE_SPACE_PAGE, ids.PRIMER_GBS_PAGE,
            ids.PRIMER_APPENDICES_PAGE, ids.HAFNIAN_PAGE, ids.PHOTONIC_HARDWARE_PAGE, ids.PHOTONICS_LANDSCAPE_PAGE,
            ids.PIQUASSO_PAGE, ids.WALTHER_LECTURE_PAGE, ids.GHZ_STATES_PAGE,
        ),
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


def layers_with(layers: Tuple[LayerInfo, ...], topics: Collection[TopicPage]) -> Tuple[LayerInfo, ...]:
    """Accepted topics join the group of the page they expand; an unknown group means our own research."""
    known = {info.layer.value for info in layers}

    def joins(topic: TopicPage, info: LayerInfo) -> bool:
        layer = topic.placement.layer if topic.placement.layer in known else Layer.RESEARCH.value
        return layer == info.layer.value

    return tuple(
        replace(info, page_ids=info.page_ids + tuple(
            generated_page_id(topic.slug) for topic in topics if joins(topic, info)
        ))
        for info in layers
    )


LAYERS = layers_with(BASE_LAYERS, GENERATED_TOPICS)


MAP_LABELS = {
    ids.INTEGRALS_CHEAT_SHEET_PAGE: "Tahák: integrály",
    ids.HAFNIAN_PAGE: "Hafnián a permanent",
    ids.THEORY_PAGE: "Teorie MC na GBS",
    ids.ACADEMY_PAGE: "Quantum Academy",
    ids.PORTFOLIO_PAGE: "Klasické MC",
    ids.GBS_PAGE: "MC na GBS",
    ids.ADVANTAGE_PAGE: "Výhoda GBS",
    ids.CAVEATS_PAGE: "Háčky MC na GBS",
    ids.GUIDE_PAGE: "Průvodce výhodou GBS",
    ids.RANDOM_MATRIX_PAGE: "Náhodné matice",
    ids.LITERATURE_REVIEW_PAGE: "Rešerše GBS",
    ids.ANDERSEN_SHAN_PAPER_PAGE: "Článek Andersena a Shan",
    ids.QPURPOSE_PAGE: "Qpurpose",
    ids.VQE_PAPER_PAGE: "VQE na IBM Fez",
    ids.PHOTONIC_HARDWARE_PAGE: "Quandela a hardware v Evropě",
    ids.PHOTONICS_LANDSCAPE_PAGE: "Fotonika ve světě",
    ids.PIQUASSO_PAGE: "Piquasso",
    ids.PRIMER_BASICS_PAGE: "Skripta 1: základy",
    ids.PRIMER_GAUSSIAN_STATES_PAGE: "Skripta 2: gaussovské stavy",
    ids.PRIMER_PHASE_SPACE_PAGE: "Skripta 3: fázový prostor",
    ids.PRIMER_GBS_PAGE: "Skripta 4: GBS a grafy",
    ids.PRIMER_APPENDICES_PAGE: "Skripta: dodatky A–B",
    ids.WALTHER_LECTURE_PAGE: "Přednáška Walther 2022",
    ids.GHZ_STATES_PAGE: "GHZ stavy",
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


BASE_RELATIONS: Tuple[Relation, ...] = (
    Relation(ids.PORTFOLIO_PAGE, RelationKind.FOLLOWS, ids.GBS_PAGE, "od losování scénářů k odhadu z fotonů"),
    Relation(ids.GBS_PAGE, RelationKind.FOLLOWS, ids.ADVANTAGE_PAGE, "od momentu portfolia k obecným gaussovským úlohám"),
    Relation(ids.LITERATURE_REVIEW_PAGE, RelationKind.FOLLOWS, ids.PHOTONIC_HARDWARE_PAGE, "kdo by úlohu spustil"),
    Relation(
        ids.PHOTONICS_LANDSCAPE_PAGE, RelationKind.EXPANDS, ids.PHOTONIC_HARDWARE_PAGE,
        "od jedné firmy k celému oboru",
    ),
    Relation(
        ids.PIQUASSO_PAGE, RelationKind.EXPANDS, ids.PHOTONICS_LANDSCAPE_PAGE,
        "simulátor z kapitoly o softwaru podrobně",
    ),
    Relation(ids.PIQUASSO_PAGE, RelationKind.CHECKS, ids.ADVANTAGE_PAGE, "stejné pravděpodobnosti vzorů jako aplikace"),
    Relation(ids.PRIMER_BASICS_PAGE, RelationKind.FOLLOWS, ids.PRIMER_GAUSSIAN_STATES_PAGE, "skripta: kapitola 2"),
    Relation(ids.PRIMER_GAUSSIAN_STATES_PAGE, RelationKind.FOLLOWS, ids.PRIMER_PHASE_SPACE_PAGE, "skripta: kapitola 3"),
    Relation(ids.PRIMER_PHASE_SPACE_PAGE, RelationKind.FOLLOWS, ids.PRIMER_GBS_PAGE, "skripta: kapitola 4"),
    Relation(
        ids.PRIMER_APPENDICES_PAGE, RelationKind.EXPLAINS, ids.PRIMER_BASICS_PAGE,
        "kvantová mechanika a odkud se berou obsazovací čísla",
    ),
    Relation(
        ids.PRIMER_GAUSSIAN_STATES_PAGE, RelationKind.EXPLAINS, ids.THEORY_PAGE,
        "gaussovské stavy, stlačení a interferometr, na kterých odhad stojí",
    ),
    Relation(ids.PRIMER_GBS_PAGE, RelationKind.EXPANDS, ids.HAFNIAN_PAGE, "hafnián, perfektní párování a grafy"),
    Relation(ids.PRIMER_BASICS_PAGE, RelationKind.EXPLAINS, ids.PIQUASSO_PAGE, "hradla a měření, která Piquasso simuluje"),
    Relation(
        ids.WALTHER_LECTURE_PAGE, RelationKind.EXPANDS, ids.PRIMER_BASICS_PAGE,
        "hradla, boson sampling a ztráty očima experimentátora",
    ),
    Relation(
        ids.WALTHER_LECTURE_PAGE, RelationKind.EXPLAINS, ids.PHOTONICS_LANDSCAPE_PAGE,
        "proč PsiQuantum staví na fúzích a co je kvantová výhoda",
    ),
    Relation(
        ids.GHZ_STATES_PAGE, RelationKind.EXPANDS, ids.WALTHER_LECTURE_PAGE,
        "třífotonové GHZ stavy z plánu fotonického počítače podrobně",
    ),
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
    Relation(ids.THEORY_PAGE, RelationKind.EXPLAINS, ids.GBS_PAGE, "každý krok podrobně"),
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
    Relation(
        ids.PHOTONICS_LANDSCAPE_PAGE, RelationKind.CHECKS, ids.QPURPOSE_PAGE,
        "Qpurpose mezi ostatními nabídkami pro banky",
    ),
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
        ids.PHOTONICS_LANDSCAPE_PAGE, RelationKind.MOTIVATES, ids.FAILURE_DIAGNOSTICS_PAGE,
        "bez dokladu výhody je nezávislá diagnostika obhajitelnější příspěvek",
    ),
    Relation(
        ids.VQE_PAPER_PAGE, RelationKind.CONTRASTS, ids.LITERATURE_REVIEW_PAGE,
        "hradlová optimalizace proti fotonickému vzorkování",
    ),
)


def relations_with(
    relations: Tuple[Relation, ...], topics: Collection[TopicPage], layers: Tuple[LayerInfo, ...]
) -> Tuple[Relation, ...]:
    """Each accepted topic expands the page whose text it grew from (or the page it sits under)."""
    pages = {page_id for info in layers for page_id in info.page_ids}
    added = []
    for topic in topics:
        target = next(
            (page_id for page_id in (topic.origin.page_id, topic.placement.parent_page_id) if page_id in pages), None
        )
        if target:
            added.append(Relation(
                generated_page_id(topic.slug), RelationKind.EXPANDS, target,
                f"rozvádí úryvek „{_excerpt(topic.origin.selection)}“",
            ))
    return relations + tuple(added)


def _excerpt(text: str, length: int = 60) -> str:
    return text if len(text) <= length else text[:length].rsplit(" ", 1)[0] + "…"


RELATIONS = relations_with(BASE_RELATIONS, GENERATED_TOPICS, LAYERS)
