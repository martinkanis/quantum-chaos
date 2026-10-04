"""Five Gaussian monomial problems on which the GBS-P estimator needs far fewer samples than plain Monte Carlo."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Sequence, Tuple

import numpy as np

from gbs.monomial_problem import MonomialProblem
from montecarlo.historical_returns import AssetClass
from montecarlo.presets import LONG_RUN_PRESET, MarketPreset

HISTORICAL_CLASSES = (AssetClass.STOCKS, AssetClass.BONDS, AssetClass.GOLD)
HISTORICAL_DECIMALS = 6
"""The historical covariance is rounded so that the table shows readable numbers that a reader can retype."""
PAIR_CORRELATION = 0.5
FACTOR_LOADINGS = (0.9, 0.8, 0.7, 0.6)


@dataclass(frozen=True)
class BenchmarkProblem:
    key: str
    title: str
    description: str
    """Markdown: what the problem models and why the GBS-P estimator suits it."""
    problem: MonomialProblem


def equicorrelated_matrix(size: int, correlation: float) -> np.ndarray:
    matrix = np.full((size, size), correlation)
    np.fill_diagonal(matrix, 1.0)
    return matrix


def one_factor_matrix(loadings: Sequence[float]) -> np.ndarray:
    """Correlations β_i·β_j of a one-factor (market) model with unit variances."""
    matrix = np.outer(loadings, loadings)
    np.fill_diagonal(matrix, 1.0)
    return matrix


def historical_covariance(preset: MarketPreset, asset_classes: Sequence[AssetClass]) -> np.ndarray:
    volatilities = np.array([preset.volatilities[asset_class] for asset_class in asset_classes])
    correlation = np.eye(len(asset_classes))
    for first, second in combinations(range(len(asset_classes)), 2):
        pair = (asset_classes[first], asset_classes[second])
        value = preset.correlations.get(pair, preset.correlations.get(pair[::-1]))
        correlation[first, second] = correlation[second, first] = value
    return np.round(correlation * np.outer(volatilities, volatilities), HISTORICAL_DECIMALS)


def find_benchmark(key: str) -> BenchmarkProblem:
    for benchmark in BENCHMARK_PROBLEMS:
        if benchmark.key == key:
            return benchmark
    raise KeyError(f"Neznámá připravená úloha: {key}")


PAIR_NAMES = ("Aktivum A", "Aktivum B")

BENCHMARK_PROBLEMS: Tuple[BenchmarkProblem, ...] = (
    BenchmarkProblem(
        key="extremni-moment",
        title="1 · Extrémní moment jedné veličiny: E[X²⁰]",
        description=r"""
Jedna normovaná veličina $X \sim \mathcal{N}(0, 1)$, třeba denní výnos vydělený svou volatilitou, a její
20. moment. Přesná hodnota je $19!! = 1\cdot 3\cdot 5 \cdots 19 = 654\,729\,075$.

**Proč se hodí:** $X^{20}$ ovládají vzácné obří hodnoty. Scénář o velikosti 4 směrodatných odchylek přispěje
$4^{20} \approx 10^{12}$krát víc než obyčejný scénář, takže Monte Carlo potřebuje obrovský počet scénářů.
GBS s jedním módem přitom ukáže vzor „20 fotonů“ zhruba v každém 42. výstřelu.
""",
        problem=MonomialProblem(covariance=np.array([[1.0]]), exponents=(20,), variable_names=("X",)),
    ),
    BenchmarkProblem(
        key="spolecny-extrem",
        title="2 · Společný extrém dvou aktiv: E[X₁⁸X₂⁸]",
        description=r"""
Dvě normované veličiny s korelací 0,5 a součin jejich osmých mocnin. Měří, jak často jsou obě aktiva
**zároveň** daleko od průměru, tedy „společné chvosty“.

**Proč se hodí:** vysoký stupeň (16) při pouhých dvou proměnných. GBS stačí dva módy a vzor $(8, 8)$ padne
zhruba v jednom výstřelu z 250.
""",
        problem=MonomialProblem(
            covariance=equicorrelated_matrix(2, PAIR_CORRELATION), exponents=(8, 8), variable_names=PAIR_NAMES,
        ),
    ),
    BenchmarkProblem(
        key="nesoumerny-monom",
        title="3 · Nesouměrný monom: E[X₁¹²X₂⁴]",
        description=r"""
Stejná dvojice aktiv, ale s exponenty 12 a 4: rozhoduje hlavně extrém prvního aktiva, druhé ho jen „váží“.

**Proč se hodí:** pořád vysoký stupeň při malém počtu proměnných. Ukazuje navíc, proč je dobré ladit stlačení
pro každý mód zvlášť: při ladění jen celkového počtu fotonů (jako v článku) padá vzor $(12, 4)$ zhruba
3× méně často.
""",
        problem=MonomialProblem(
            covariance=equicorrelated_matrix(2, PAIR_CORRELATION), exponents=(12, 4), variable_names=PAIR_NAMES,
        ),
    ),
    BenchmarkProblem(
        key="historie-usa",
        title="4 · Akcie, dluhopisy a zlato (USA 1928–2023): E[X₁⁶X₂⁶X₃⁶]",
        description=r"""
Kovarianční matice ročních výnosů amerických akcií, desetiletých státních dluhopisů a zlata za roky 1928–2023
(volatility 19,6 %, 8,0 % a 20,8 %, korelace skoro nulové; data A. Damodaran, NYU Stern). Monom je společný
šestý moment všech tří aktiv.

**Proč se hodí:** stupeň 18 při třech proměnných. Je to ale i varování: dluhopisy kolísají 2,5× méně než
akcie, takže při ladění jen celkového počtu fotonů (jako v článku) jdou skoro všechny fotony do akcií a zlata
a vzor $(6, 6, 6)$ téměř nepadá – GBS by pak potřeboval asi 250× **víc** vzorků než Monte Carlo. Ladění
po módech to spraví a GBS vyjde zhruba 170× lépe.
""",
        problem=MonomialProblem(
            covariance=historical_covariance(LONG_RUN_PRESET, HISTORICAL_CLASSES),
            exponents=(6, 6, 6),
            variable_names=("Akcie", "Dluhopisy", "Zlato"),
        ),
    ),
    BenchmarkProblem(
        key="trzni-faktor",
        title="5 · Čtyři aktiva s tržním faktorem: E[X₁⁴X₂⁴X₃⁴X₄⁴]",
        description=r"""
Čtyři normovaná aktiva, jejichž korelace vznikají z jednoho společného faktoru – trhu – s citlivostmi 0,9;
0,8; 0,7 a 0,6 (jednofaktorový model, korelace mezi 0,42 a 0,72). Monom stupně 16 je společný čtvrtý moment.

**Proč se hodí:** pořád vysoký stupeň, ale proměnných je víc, a výhoda je proto menší – desítky, ne tisíce.
Ukazuje, že stupeň musí růst rychleji než počet proměnných (u Andersena a Shan aspoň s jeho druhou mocninou).
""",
        problem=MonomialProblem(
            covariance=one_factor_matrix(FACTOR_LOADINGS),
            exponents=(4, 4, 4, 4),
            variable_names=("Aktivum A", "Aktivum B", "Aktivum C", "Aktivum D"),
        ),
    ),
)
DEFAULT_BENCHMARK = BENCHMARK_PROBLEMS[0]
