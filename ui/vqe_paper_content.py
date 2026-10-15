"""TL;DR of De León et al., arXiv:2512.22001: VQE for dynamic portfolio optimisation on IBM Fez.

All numbers come from version v1 (26 Dec 2025); the tables of the page are generated from them.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from ui.theory_content import Source

PERCENT = 100

DE_LEON_2025 = Source(
    "De León, I., Arias, D., Martín-Cordero, M. a kol.: *Variational Quantum Eigensolver for Real-World Finance: "
    "Scalable Solutions for Dynamic Portfolio Optimization Problems*, "
    "[arXiv:2512.22001](https://arxiv.org/abs/2512.22001) (v1, 26. 12. 2025) – Global Data Quantum, BBVA Quantum, "
    "IBM Quantum"
)
SCALING_VQE_2024 = Source(
    "Martín-Cordero, M. a kol.: *Scaling the Variational Quantum Eigensolver for Dynamic Portfolio Optimization*, "
    "[arXiv:2412.19150](https://arxiv.org/abs/2412.19150) (2024) – předchozí práce stejné skupiny"
)
MUGEL_2022 = Source(
    "Mugel, S., Kuchkovsky, C., Sánchez, E. a kol.: *Dynamic portfolio optimization with real datasets using "
    "quantum processors and quantum-inspired tensor networks*. Physical Review Research (2022)"
)
SOURCES: Tuple[Source, ...] = (DE_LEON_2025, SCALING_VQE_2024, MUGEL_2022)


@dataclass(frozen=True)
class CostComparison:
    """Minimum optimisation cost Q (lower is better) from Tables 1, 3 and 5 of the paper."""

    problem: str
    random_cost: float
    raw_cost: float
    isqr_cost: float
    cplex_cost: float
    raw_label: str


@dataclass(frozen=True)
class FinancialResult:
    """Annualised Sharpe ratio, effective return and volatility from Tables 2, 4 and 6."""

    problem: str
    cplex: Tuple[float, float, float]
    best_isqr: Tuple[float, float, float]


COST_COMPARISONS: Tuple[CostComparison, ...] = (
    CostComparison("9 aktiv, VQE (144 qubitů)", 2.63e-2, 4.05e-3, -2.55e-2, -3.49e-2, "VQE"),
    CostComparison("9 aktiv, VQEC (36 qubitů na krok)", 2.63e-2, -3.15e-2, -3.59e-2, -3.49e-2, "VQEC"),
    CostComparison("38 aktiv, VQEC (152 qubitů na krok)", 0.63, 0.29, 0.21, -0.07, "VQEC"),
)
FINANCIAL_RESULTS: Tuple[FinancialResult, ...] = (
    FinancialResult("9 aktiv, VQE", (4.10, 21.14, 4.73), (3.74, 22.62, 5.59)),
    FinancialResult("9 aktiv, VQEC", (4.16, 22.65, 5.00), (4.18, 22.13, 4.88)),
    FinancialResult("38 aktiv, VQEC", (9.18, 130.69, 14.05), (7.47, 82.85, 10.85)),
)
VQEC_TABLE_SUSPECT = "9 aktiv, VQEC (36 qubitů na krok)"
"""Its random and CPLEX rows equal those of the full 9-asset problem although the caption speaks of step averages."""


def gap_closed(random_cost: float, method_cost: float, reference_cost: float) -> float:
    """Share of the way from the best random sample (0) to the best known classical solution (1)."""
    return (random_cost - method_cost) / (random_cost - reference_cost)


def cost_table() -> str:
    rows = [
        "| úloha | náhoda | surové kvantové | kvantové + ISQR | CPLEX | surové urazí | s ISQR urazí |",
        "|---|---|---|---|---|---|---|",
    ]
    for comparison in COST_COMPARISONS:
        marker = " *" if comparison.problem == VQEC_TABLE_SUSPECT else ""
        rows.append(
            f"| {comparison.problem}{marker} | {_cost(comparison.random_cost)} | {_cost(comparison.raw_cost)} "
            f"| {_cost(comparison.isqr_cost)} | {_cost(comparison.cplex_cost)} "
            f"| {_share(_gap(comparison, comparison.raw_cost))} | {_share(_gap(comparison, comparison.isqr_cost))} |"
        )
    return "\n".join(rows)


def financial_table() -> str:
    rows = [
        "| úloha | Sharpe CPLEX | Sharpe kvantové | výnos CPLEX | výnos kvantové | volatilita CPLEX "
        "| volatilita kvantové |",
        "|---|---|---|---|---|---|---|",
    ]
    for result in FINANCIAL_RESULTS:
        (cplex_sharpe, cplex_return, cplex_volatility) = result.cplex
        (isqr_sharpe, isqr_return, isqr_volatility) = result.best_isqr
        rows.append(
            f"| {result.problem} | {_decimal(cplex_sharpe)} | {_decimal(isqr_sharpe)} | {_decimal(cplex_return)} % "
            f"| {_decimal(isqr_return)} % | {_decimal(cplex_volatility)} % | {_decimal(isqr_volatility)} % |"
        )
    return "\n".join(rows)


def _gap(comparison: CostComparison, method_cost: float) -> float:
    return gap_closed(comparison.random_cost, method_cost, comparison.cplex_cost)


def _share(value: float) -> str:
    return f"{PERCENT * value:.0f} %"


def _cost(value: float) -> str:
    return f"{value:+.4f}".replace(".", ",").replace("-", "−")


def _decimal(value: float) -> str:
    return f"{value:.2f}".replace(".", ",")


@dataclass(frozen=True)
class PaperSection:
    title: str
    markdown: str


IN_ONE_SENTENCE = (
    "Hybridní VQE s chytrým klasickým post-processingem najde na reálném čipu IBM Fez portfolia podobná řešiči CPLEX "
    "u 9 aktiv, u 38 aktiv slušná, ale znatelně horší. Přínos je hlavně inženýrský (škálování na 152 qubitů "
    "a post-processing), ne kvantová výhoda."
)


def paper_sections() -> List[PaperSection]:
    return [
        PaperSection("Problém: dynamická optimalizace portfolia", PROBLEM),
        PaperSection("Jak to funguje, krok za krokem", HOW_IT_WORKS),
        PaperSection("Výsledky: hodnota cílové funkce", f"{RESULTS_COST_INTRO}\n{cost_table()}\n{RESULTS_COST_NOTE}"),
        PaperSection(
            "Výsledky: finanční metriky", f"{RESULTS_FINANCE_INTRO}\n{financial_table()}\n{RESULTS_FINANCE_NOTE}",
        ),
        PaperSection("Co znamená „srovnatelná s CPLEX“", COMPARABLE),
        PaperSection("Proč inženýrský přínos, ne kvantová výhoda", ENGINEERING),
        PaperSection("Na co si dát pozor", CAVEATS),
        PaperSection("Náměty pro navazující výzkum", FOLLOW_UP),
    ]


PROBLEM = r"""
- **Cíl:** Markowitzova úloha přes čtyři rebalance po 28 dnech: maximalizovat výnos mínus $\tfrac{\gamma}{2}\cdot$
  riziko, odečíst transakční náklady a přidat pokutu $\rho\,(\sum w - 1)^2$ za porušení rozpočtu.
- **Data:** akcie z indexu IBEX 35 (u 38 aktiv celý index plus jeden fond a dva měnové páry EUR/USD a EUR/JPY),
  období 1. 11. 2022 – 20. 2. 2023.
- **Kódování:** každá váha má 4 bity, tedy 16 úrovní mezi minimem a maximem (u 9 aktiv většinou 0–30 %, u 38 aktiv
  0–20 %). Qubitů je aktiva × 4 × časové kroky, pro 9 aktiv 144.
- **QUBO:** transakční náklady jsou úměrné druhé mocnině změny váhy, aby se vešly do kvadratické formulace
  a z ní do Isingova hamiltoniánu. Parametry: $\gamma = 2500$ a $\rho = 0{,}05$ pro 9 aktiv, $\gamma = 1000$
  a $\rho = 0{,}5$ pro 38 aktiv.
"""

HOW_IT_WORKS = r"""
**a) Z portfolia se stane hledání nejlepšího bitového řetězce.** Jeden řetězec (144 bitů u 9 aktiv) popisuje
celou investiční strategii. Každému jde spočítat „cenu“ $Q$ = −výnos + riziko + transakční náklady + pokuta za
rozpočet. Nejlepší strategie má nejnižší $Q$; fyzikálně jde o základní stav Isingova hamiltoniánu.

**b) VQE je laditelný generátor kandidátů.** Kvantový obvod připraví superpozici obrovského množství řetězců
a měření z ní vytáhne jeden. Parametry obvodu $\theta$ fungují jako knoflíky, které mění, které strategie jsou
pravděpodobné. Čip změří průměrnou cenu stavu, klasický optimalizátor (Differential Evolution: u 9 aktiv populace
188 a 20 generací, u 38 aktiv populace 112 a 20–25 generací) navrhne nová $\theta$ a smyčka se opakuje. Nakonec se
stav změří milionkrát a vznikne $10^6$ kandidátních portfolií.

**c) Hardware je šumný.** Mnoho vzorků má náhodně překlopené bity a porušuje rozpočet; QUBO podmínky nevynucuje,
jen je pokutuje. Surové VQE je lepší než náhoda (87 % vzorků má nižší cenu než průměr náhodných řetězců), ale
nejlepší vzorek je od nejlepšího známého řešení ještě daleko.

**d) ISQR: klasická oprava, která dělá velkou část práce.** *Ising Sample-based Quantum configuration Recovery*
přebírá myšlenku „configuration recovery“ z metody SQD od IBM (původně pro kvantovou chemii). Funguje jako
rekonstrukce textu z milionu poškozených kopií hlasováním:

1. vzorky rozdělí do 10 dávek po 100 000 a z každé vezme nejlepší,
2. u nejlepších spočítá, jak často je každý bit 1 – „otisk“ dobrého řešení,
3. každý vzorek pravděpodobnostně opraví: překlápí bity nejvíc odlišné od otisku, přednostně ty s velkou vahou,
   aby součet vah seděl na 100 %,
4. opakuje, dokud se cena mezi dvěma koly nezmění o méně než 2,5 %.

Pak váhy klasicky renormalizuje a z opravených vzorků vybere 1000 nejlepších – to je „mrak“ portfolií v grafech
článku. Po ISQR má nižší cenu než průměr náhody 100 % vzorků.

**e) VQEC: rozklad po časových krocích.** Každý rebalance se řeší zvlášť a výsledek vstupuje do transakčních
nákladů dalšího kroku. Qubitů je jen aktiva × 4, takže 38 aktiv = 152 qubitů na 156qubitovém čipu. Daň: optimalizace
je hladová a nevidí kompromisy mezi kroky.

**f) Zrychlení běhu.** Batch mód (asi 6×), kratší pauza mezi měřeními `rep_delay` 250 → 100 μs (2,5×) a gen3-turbo
(asi 1,3×), dohromady asi 19,5×: výpočet na 8 hodin trvá 30 minut.
"""

RESULTS_COST_INTRO = r"""
Hodnota cílové funkce $Q$ (nižší je lepší) podle tabulek 1, 3 a 5 článku. Přesné optimum nikdo nezná; jako
referenci článek bere klasický řešič IBM CPLEX s limitem 15 minut a neuvádí, zda optimalitu dokázal. CPLEX je tedy
jen nejlepší známé řešení. Sloupce „urazí“ jsme dopočítali my: jakou část cesty od nejlepšího náhodného vzorku (0 %)
k CPLEX (100 %) metoda urazí.
"""

RESULTS_COST_NOTE = r"""

\* U VQEC s 9 aktivy mají náhoda i CPLEX v tabulce 3 přesně stejná čísla jako u plné úlohy v tabulce 1, ačkoli
popisek tabulky tvrdí, že jde o průměry přes časové kroky. Kvantová hodnota průměrem je, takže srovnání nejspíš není
jablka s jablky. Podúloha jednoho kroku má navíc jen 36 binárních proměnných, a tu by CPLEX měl vyřešit přesně –
„poražení“ CPLEX je proto spíš artefakt srovnání.

$Q$ je bezrozměrné skóre bez přímého finančního výkladu a mezi úlohami se nedá porovnávat (jiné $\gamma$ a $\rho$).
V literatuře o QAOA je standardem *approximation ratio*; článek ho neuvádí.
"""

RESULTS_FINANCE_INTRO = r"""
Anualizovaný Sharpeův poměr, efektivní výnos (po transakčních nákladech) a volatilita nejlepšího řešení ISQR
a řešení CPLEX podle tabulek 2, 4 a 6. Bezriziková sazba je 1,72 %.
"""

RESULTS_FINANCE_NOTE = r"""

Cílová funkce $Q$ není totéž co Sharpe, takže řešení s horší $Q$ může mít vyšší výnos. U 9 aktiv (VQE) má nejlepší
kvantové řešení výnos 22,62 %, tedy těsně nad prahem 22,04 % (dvojnásobek dlouhodobého průměru S&P 500), zatímco
CPLEX má 21,14 %. Autoři to prezentují jako výhru; je to ale výhra v jednom kritériu o 1,5 procentního bodu při horším
Sharpe i volatilitě. Výnos 130 % ročně u 38 aktiv vysvětluje sekce „Na co si dát pozor“.
"""

COMPARABLE = r"""
„Srovnatelná“ znamená ve stejném řádu a blízko efektivní hranice, ne systematicky lepší. U malé úlohy urazí VQE s ISQR
asi 85 % cesty od náhody k CPLEX, u velké jen asi 60 % a CPLEX je jasně lepší i finančně (Sharpe 9,18 proti 7,47).

Hlavní argument autorů je **diverzita**: CPLEX vrátí jedno řešení, vzorkování tisíc kvalitních portfolií podél
efektivní hranice a investor si vybere podle jiného kritéria (minimální riziko, maximální Sharpe). To platí, ale není
to nic výlučně kvantového: mnoho řešení umí i solution pool v samotném CPLEX, multi-start heuristiky nebo přímo
výpočet efektivní hranice.
"""

ENGINEERING = r"""
**Kvantová výhoda** by znamenala lepší řešení nebo rychleji než nejlepší klasika. Tady neplatí ani jedno: CPLEX na
pracovní stanici za 15 minut je stejně dobrý nebo lepší, kvantový běh trvá i po všech zrychleních asi 30 minut
a k tomu klasický optimalizátor a ISQR nad milionem vzorků.

**Inženýrský přínos** je, že to vůbec běží na 152 qubitech reálného šumného čipu a dává smysluplné výsledky místo
šumu. To je netriviální: obvod (ansatz) ušitý na topologii čipu z bloků po čtyřech qubitech, paralelní odesílání
úloh, kratší pauzy mezi měřeními, rozklad po časových krocích a post-processing.

**Otevřená otázka:** kolik práce dělá kvantový obvod a kolik ISQR? ISQR je heuristika typu „najdi vzor v dobrých
řešeních a podle něj oprav ostatní“, blízká klasickým evolučním algoritmům (EDA, genetické algoritmy). Chybí test,
co by ISQR udělal se vzorky z obyčejného generátoru náhodných čísel nebo z levné klasické heuristiky. Kdyby dával
podobné výsledky, kvantová část by byla skoro dekorace.
"""

CAVEATS = r"""
- **Znalost budoucnosti:** výnosy i kovariance se počítají z cen ve stejném 28denním okně, do kterého se investuje
  (rovnice 3 a 19 článku). Jde o optimalizaci zpětně, ne o backtest – odtud i nereálných 130 % ročně u 38 aktiv.
- **Chybí ablace:** ISQR nebyl vyzkoušen na náhodných ani klasických vzorcích, takže nevíme, kolik práce dělá
  kvantový obvod.
- **Jediný klasický soupeř:** CPLEX s limitem 15 minut. Chybí simulované žíhání, tabu search i Gurobi.
- **Jedno období, čtyři kroky,** žádná opakování ani rozptyly výsledků.
- **Střet zájmů v interpretaci:** výsledky IBM a BBVA na hardwaru IBM; formulace o „cestě k praktické výhodě“ je
  optimistická.
"""

FOLLOW_UP = r"""
- **Referenční formulace:** hotová a dobře popsaná QUBO formulace dynamické optimalizace včetně transakčních nákladů,
  použitelná jako baseline. Navazuje na arXiv:2412.19150 a na Mugel a kol. 2022.
- **ISQR nezávisí na ansatzu:** jde použít i na vzorky z QAOA.
- **Levný a přesvědčivý experiment:** ablace „kvantové vzorky proti klasickým vzorkům, obojí s ISQR“.
- **Data:** kovariance z obyčejných 28denních oken; nelineární nebo chaotickou strukturu cenových řad článek neřeší.
- **Menší čipy:** rozklad po krocích a post-processing jsou triky, které jsou potřeba na čipech s méně qubity;
  ISQR patří do rodiny „quantum-centric supercomputing“ (kombinace superpočítače a kvantového čipu).
- **Metriky:** u vlastních výsledků reportovat approximation ratio i finanční metriky, aby šly srovnávat s literaturou.
"""
