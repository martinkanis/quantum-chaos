"""Texts of the photon loss page: the fourth source of error of a GBS risk estimate, with the numbers computed here."""

from __future__ import annotations

from math import log10
from typing import Dict, Tuple

import numpy as np

from gbs.bench import DETECTORS, DetectorKind, Losses, bench_transmission
from gbs.benchmark_problems import BENCHMARK_PROBLEMS, BenchmarkProblem
from gbs.loss_study import LossPoint, LossStudy, run_loss_study
from gbs.monomial_problem import MonomialProblem, compare_variances
from gbs.photon_loss import click_probability, ideal_patterns
from gbs.photon_tuning import TuningMode
from ui.advantage_results import format_count
from ui.caveats_content import CLASSICAL_SIMULATION, REAL_HARDWARE
from ui.chip_bench_content import DEFAULT_COUPLING_LOSS_DB, DEFAULT_WAVEGUIDE_LOSS_DB_PER_CM
from ui.literature_review_content import BULMER_BOUNDARY, QI_NOISY_SIMULABILITY
from ui.random_matrix_content import czech_decimal
from ui.theory_content import (
    ANDERSEN_SHAN_ADVANTAGE,
    ANDERSEN_SHAN_EXPECTATIONS,
    HAMILTON,
    OH_CLASSICAL_SIMULATION,
    Reading,
    Source,
    TheoryTopic,
)

SOURCES_ANCHOR = "zt-zdroje"
LAB_ANCHOR = "zt-laborator"
PERCENT = 100
EXAMPLE_BENCHMARK_KEY = "spolecny-extrem"
EXAMPLE_TRANSMISSION = 0.9
SMALL_LOSS_TRANSMISSION = 0.99
MODERATE_LOSS_TRANSMISSION = 0.95
LARGE_LOSS_TRANSMISSION = 0.8
TABLE_TRANSMISSIONS = (SMALL_LOSS_TRANSMISSION, MODERATE_LOSS_TRANSMISSION, EXAMPLE_TRANSMISSION)
ADVANTAGE_TABLE_TRANSMISSIONS = (1.0, MODERATE_LOSS_TRANSMISSION, EXAMPLE_TRANSMISSION, LARGE_LOSS_TRANSMISSION)
COLLISION_FREE_COVARIANCE = np.array([[1.0, 0.5], [0.5, 1.0]])
"""Two assets with correlation 0,5 and the pattern (1, 1): the only kind of target threshold detectors can show."""
BENCH_DETECTOR = DetectorKind.SNSPD
BENCH_MODE_COUNT = 2

KISS_HERZOG_LEONHARDT_1995 = Source(
    "Kiss, T., Herzog, U., Leonhardt, U.: *Compensation of losses in photodetection and in quantum-state "
    "measurements*. Physical Review A 52 (1995), 2433, "
    "[doi:10.1103/PhysRevA.52.2433](https://doi.org/10.1103/PhysRevA.52.2433)"
)
RAHIMI_KESHARI_2016 = Source(
    "Rahimi-Keshari, S., Ralph, T. C., Caves, C. M.: *Sufficient conditions for efficient classical simulation of "
    "quantum optics*. Physical Review X 6 (2016), 021039, "
    "[doi:10.1103/PhysRevX.6.021039](https://doi.org/10.1103/PhysRevX.6.021039)"
)
GARCIA_PATRON_2019 = Source(
    "García-Patrón, R., Renema, J. J., Shchesnovich, V.: *Simulating boson sampling in lossy architectures*. "
    "Quantum 3 (2019), 169, [doi:10.22331/q-2019-08-05-169](https://doi.org/10.22331/q-2019-08-05-169)"
)
OSZMANIEC_BROD_2018 = Source(
    "Oszmaniec, M., Brod, D. J.: *Classical simulation of photonic linear optics with lost particles*. New Journal "
    "of Physics 20 (2018), 092002, [doi:10.1088/1367-2630/aadfa8](https://doi.org/10.1088/1367-2630/aadfa8)"
)
QUESADA_THRESHOLD_2018 = Source(
    "Quesada, N., Arrazola, J. M., Killoran, N.: *Gaussian boson sampling using threshold detectors*. Physical "
    "Review A 98 (2018), 062322, [doi:10.1103/PhysRevA.98.062322](https://doi.org/10.1103/PhysRevA.98.062322)"
)


def typical_bench_transmission(mode_count: int) -> float:
    """Transmission of the bench of the chip simulator with its default losses and a photon-counting SNSPD."""
    losses = Losses(DEFAULT_COUPLING_LOSS_DB, DEFAULT_WAVEGUIDE_LOSS_DB_PER_CM)
    return bench_transmission(losses, mode_count) * DETECTORS[BENCH_DETECTOR].efficiency


def loss_decibels(transmission: float) -> float:
    return -10 * log10(transmission)


def percent_label(value: float, decimals: int = 0) -> str:
    return czech_decimal(PERCENT * value, decimals) + " %"


def signed_percent(value: float, decimals: int = 0) -> str:
    """−27 % for a shortfall, +12 % for an excess."""
    sign = "−" if value < 0 else "+"
    return sign + czech_decimal(PERCENT * abs(value), decimals) + " %"


def times_label(value: float) -> str:
    return format_count(value) + "×"


BENCHMARK_STUDIES: Dict[str, LossStudy] = {
    benchmark.key: run_loss_study(benchmark.problem, TuningMode.PER_MODE, EXAMPLE_TRANSMISSION)
    for benchmark in BENCHMARK_PROBLEMS
}
"""Every prepared problem at every transmission of the sweep; the texts below quote these numbers."""
EXAMPLE = BENCHMARK_STUDIES[EXAMPLE_BENCHMARK_KEY]


def study_point(study: LossStudy, transmission: float) -> LossPoint:
    return next(point for point in study.sweep if point.transmission == transmission)


def example_point(transmission: float) -> LossPoint:
    return study_point(EXAMPLE, transmission)


def example_advantage(transmission: float) -> float:
    return EXAMPLE.advantage(example_point(transmission))


def collision_free_click_ratios() -> Tuple[float, float]:
    """For E[X₁X₂] without loss: how many times more often threshold detectors click in both modes than the ideal
    pattern (1, 1) falls, and how many times too high the estimate from the clicks comes out."""
    problem = MonomialProblem(COLLISION_FREE_COVARIANCE, (1, 1), ("X₁", "X₂"))
    comparison = compare_variances(problem, TuningMode.PER_MODE)
    ideal = ideal_patterns(problem.covariance, comparison.encoding, problem.exponents, extra_photons=40)
    frequency_ratio = click_probability(ideal, 1.0) / comparison.pattern_probability
    return frequency_ratio, float(np.sqrt(frequency_ratio))


def simulable_transmission_range() -> Tuple[float, float]:
    boundaries = [study.simulable_transmission for study in BENCHMARK_STUDIES.values()]
    return min(boundaries), max(boundaries)


def bias_range(transmission: float) -> Tuple[float, float]:
    """The smallest and the largest shortfall of the uncorrected estimate across the prepared problems."""
    shortfalls = [-study_point(study, transmission).naive_bias for study in BENCHMARK_STUDIES.values()]
    return min(shortfalls), max(shortfalls)


def extra_samples_range(transmission: float) -> Tuple[float, float]:
    """How many times more corrected shots than Monte Carlo scenarios the prepared problems need, least and most."""
    factors = [1 / study.advantage(study_point(study, transmission)) for study in BENCHMARK_STUDIES.values()]
    return min(factors), max(factors)


def _short_title(benchmark: BenchmarkProblem) -> str:
    """„2 · Společný extrém dvou aktiv: E[X₁⁸X₂⁸]“ → „2 · E[X₁⁸X₂⁸]“."""
    number, _, rest = benchmark.title.partition(" · ")
    return f"{number} · {rest.split(': ')[-1]}"


def bias_table() -> str:
    header = "| úloha | stupeň | " + " | ".join(
        f"{percent_label(1 - value)} ztrát" for value in TABLE_TRANSMISSIONS
    ) + " |"
    rows = [header, "|---|---|" + "---|" * len(TABLE_TRANSMISSIONS)]
    for benchmark in BENCHMARK_PROBLEMS:
        study = BENCHMARK_STUDIES[benchmark.key]
        biases = " | ".join(signed_percent(study_point(study, value).naive_bias) for value in TABLE_TRANSMISSIONS)
        rows.append(f"| {_short_title(benchmark)} | {study.problem.degree} | {biases} |")
    return "\n".join(rows)


def advantage_table() -> str:
    header = "| úloha | " + " | ".join(
        "bez ztrát" if value == 1 else f"{percent_label(1 - value)} ztrát" for value in ADVANTAGE_TABLE_TRANSMISSIONS
    ) + " |"
    rows = [header, "|---|" + "---|" * len(ADVANTAGE_TABLE_TRANSMISSIONS)]
    for benchmark in BENCHMARK_PROBLEMS:
        study = BENCHMARK_STUDIES[benchmark.key]
        cells = " | ".join(advantage_label(study, study_point(study, value)) for value in ADVANTAGE_TABLE_TRANSMISSIONS)
        rows.append(f"| {_short_title(benchmark)} | {cells} |")
    return "\n".join(rows)


def advantage_label(study: LossStudy, point: LossPoint) -> str:
    """„12× méně“ when GBS wins, „330× víc“ when Monte Carlo wins, „∞“ when the correction has infinite variance."""
    if not point.correction_converged:
        return "∞ (rozptyl nekonverguje)"
    advantage = study.advantage(point)
    return f"{times_label(advantage)} méně" if advantage >= 1 else f"{times_label(1 / advantage)} víc"


LEAD = (
    "Čtvrtý zdroj chyby odhadu rizika přes GBS: přístroj ztrácí fotony. Laboratoř spočítá, co rovnoměrné ztráty "
    "udělají s odhadem GBS-P pěti úloh ze stránky Výhoda GBS – o kolik se vychýlí odhad, který se ztrátami nepočítá, "
    "kolik stojí nestranná oprava a kde výhoda proti Monte Carlu končí. Vše je spočítané přesně, bez losování "
    "výstřelů, a u každého tvrzení je vidět, jestli je doložené literaturou, nebo je to náš výpočet či odvození."
)

IN_SHORT = (
    "Rovnoměrné ztráty jdou spočítat přesně: každý foton dorazí k detektoru s pravděpodobností η nezávisle na "
    "ostatních, takže ztrátový přístroj je ideální přístroj s mincí za každý foton. Odhad GBS-P, který se ztrátami "
    f"nepočítá, je vychýlený – u úlohy 2 (E[X₁⁸X₂⁸]) o {percent_label(-example_point(SMALL_LOSS_TRANSMISSION).naive_bias)} "
    f"už při 1 % ztrát a o {percent_label(-example_point(EXAMPLE_TRANSMISSION).naive_bias)} při 10 % ztrát – a žádný "
    "počet výstřelů to nespraví. Nestranná oprava existuje, ale její rozptyl roste tak rychle, že při 10 % ztrát "
    f"klesne úspora vzorků proti Monte Carlu z {times_label(EXAMPLE.comparison.advantage)} na "
    f"{times_label(example_advantage(EXAMPLE_TRANSMISSION))} a při 20 % ztrát potřebuje GBS "
    f"{times_label(1 / example_advantage(LARGE_LOSS_TRANSMISSION))} víc výstřelů než Monte Carlo scénářů; pod "
    f"kritickou propustností η_c ≈ {czech_decimal(EXAMPLE.critical_transmission, 2)} je rozptyl nekonečný. Prahové "
    "detektory na odhad GBS-P nestačí vůbec. Postačující podmínka klasické simulace podle Qi a kol. přitom vyloučí "
    f"výhodu jen pod propustností kolem {percent_label(EXAMPLE.simulable_transmission)}: hranici určuje sám estimátor, "
    "ne známé věty o simulovatelnosti."
)

LAB_INTRO = (
    "Vyber úlohu a ladění jako na [stránce Výhoda GBS](/vyhoda-gbs) a nastav propustnost η – podíl fotonů, které "
    "dorazí k detektorům (ztráty v dB = −10·log₁₀ η). Laboratoř počítá přesně, ne simulací: četnost cílového vzoru "
    "se ztrátami, vychýlení odhadu bez opravy, rozptyl nestranné opravy a kolik výstřelů by GBS potřeboval proti "
    "Monte Carlu; pro celou řadu propustností nakreslí grafy. Čísla platí pro detektory počítající fotony, prahové "
    "detektory ukazuje zvlášť."
)

TRANSMISSION_HINT = (
    "Propustnost zahrnuje vše od zdroje po detektor: vazbu vlákno–čip, útlum světlovodů i účinnost detektoru. "
    f"Pracovní stůl simulátoru čipu s výchozími hodnotami dává kolem "
    f"{percent_label(typical_bench_transmission(BENCH_MODE_COUNT))} (dvoumódový čip, detektor SNSPD)."
)

THINNING = TheoryTopic(
    anchor="zt-rozdeleni",
    title="Co ztráty udělají s výstřely",
    in_short=(
        "Stejná propustnost η na všech módech komutuje s interferometrem, takže ztrátový přístroj je ideální přístroj, "
        "za kterým každý foton zvlášť hází mincí. Rozdělení vzorů se binomicky ředí a ideální pravděpodobnosti dává "
        "tabulka gaussovských momentů, bez jediného hafniánu."
    ),
    explanation=r"""
**Doložené.** Ztráta fotonů se modeluje jako dělič svazku, který část světla odvede do prostředí
([háček „Reálný hardware není ideální“](/gbs/hacky#realny-hardware)). Když je propustnost $\eta$ na všech módech
stejná, dá se celá ztráta přesunout před interferometr i za něj: lineární optika zachovává počet fotonů a rovnoměrná
ztráta komutuje s každou unitární maticí $U$. Qi a kol. (2020) tak slučují ztráty zdroje a interferometru do jediného
kanálu s propustností $\eta = \eta_S\eta_I$ (jejich obr. 1) a stejně postupují analýzy ztrátového boson samplingu
(Oszmaniec a Brod 2018, García-Patrón a kol. 2019).

**Co z toho plyne (náš výpočet).** Za interferometrem je ztráta jen mince: z $k_i$ fotonů v módu $i$ jich detektor
uvidí $n_i$ s pravděpodobností $\binom{k_i}{n_i}\eta^{n_i}(1-\eta)^{k_i-n_i}$. Pravděpodobnost, že ztrátový přístroj
ukáže přesně cílový vzor $n$, je proto

$$
p_\eta(n) = \sum_{k \ge n} p(k)\,\prod_i \binom{k_i}{n_i}\,\eta^{n_i}(1-\eta)^{k_i-n_i},
$$

kde $p(k)$ jsou pravděpodobnosti ideálního přístroje. Ty nepotřebují hafniány: přístroj nese $B = D\Sigma D$, takže
$\mathrm{Haf}(B_k) = \prod_i d_i^{k_i}\,\mathbb{E}[x^k]$ a $p(k) = \mathrm{Haf}(B_k)^2/(k!\,\prod_j \cosh r_j)$ – stačí
tabulka momentů ze Steinovy rekurze, stejná jako na stránce Výhoda GBS. Součet bereme přes vzory s nejvýš $|n| + E$
fotony ($E$ fotonů navíc, až 60); co zbude, odhadujeme geometricky z posledních dvou vrstev a hrubě omezujeme shora
pravděpodobností, že ideální přístroj vyšle víc než $|n| + E$ fotonů (plyne z rozdělení počtu fotonů stlačeného
vakua, také bez hafniánů).

**Kontrola.** Ztrátový stav je smíšený gaussovský stav a jeho pravděpodobnosti dává vzorec
$p(n) = \mathrm{Haf}(A_n)/(n!\sqrt{\det\sigma_Q})$ s maticí $A$ dvojnásobného rozměru (Hamilton a kol. 2017).
Testy aplikace počítají obě cesty pro dva módy a shodují se na devět platných číslic.
""",
    further_reading=(
        Reading(HAMILTON, "pravděpodobnosti vzorů smíšeného gaussovského stavu"),
        Reading(QI_NOISY_SIMULABILITY, "model šumu: ztráty zdroje a interferometru v jednom kanálu"),
        Reading(OSZMANIEC_BROD_2018, "ztrátový boson sampling s jednotlivými fotony"),
        Reading(GARCIA_PATRON_2019, "ztráty rostoucí s hloubkou obvodu"),
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "odhad GBS-P, se kterým laboratoř pracuje"),
    ),
    related_caveats=(REAL_HARDWARE,),
)

NAIVE_BIAS = TheoryTopic(
    anchor="zt-sklon",
    title="Odhad bez opravy je vychýlený",
    in_short=(
        "Kdo vezme četnost cílového vzoru ze ztrátového přístroje a dosadí ji do vzorce pro ideální přístroj, dostane "
        f"u všech pěti úloh příliš nízké číslo: u úlohy 2 o {percent_label(-example_point(SMALL_LOSS_TRANSMISSION).naive_bias)} "
        f"při 1 % ztrát a o {percent_label(-example_point(EXAMPLE_TRANSMISSION).naive_bias)} při 10 % ztrát. Je to "
        "systematická chyba, kterou žádný počet výstřelů nezmenší."
    ),
    explanation=r"""
**Proč.** Odhad GBS-P invertuje vzorec $p(n) = \mathrm{Haf}(B_n)^2/(n!\prod_j\cosh r_j)$: z četnosti $\hat p$
spočítá $\mathrm{Haf}(B_n)$ a z něj $\mathbb{E}[x^n]$. Ztrátový přístroj ale míří na $p_\eta(n)$, ne na $p(n)$.
Stlačení je naladěné tak, aby průměrný počet fotonů v každém módu byl roven exponentu; po ztrátě klesne na
$\eta n_i$ a cílový vzor se ocitne nad průměrem, kam dopadne méně výstřelů. Výstřely s více fotony, které ztráta
„sestřelí“ právě na vzor $n$, to u pěti úloh laboratoře nevyváží: $p_\eta(n) < p(n)$ a odhad vyjde nízko (náš
výpočet, ne věta – u jiné matice může převážit přítok shora).

**Čísla (náš výpočet, ladění po módech): o kolik je odhad bez opravy nižší než přesná hodnota.**

""" + bias_table() + r"""

Odhad je úměrný odmocnině z četnosti, takže relativní chyba četnosti se v něm zhruba půlí. I tak je už při 1 %
ztrát několikanásobně větší než cílová přesnost 1 %, se kterou stránka Výhoda GBS srovnává počty vzorků. Nápravou
není víc výstřelů, ale oprava modelu – další kapitola.
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "odhad GBS-P z četnosti cílového vzoru"),
        Reading(ANDERSEN_SHAN_ADVANTAGE, "ladění stlačení na stupeň úlohy"),
    ),
)

CORRECTION = TheoryTopic(
    anchor="zt-oprava",
    title="Nestranná oprava a její cena",
    in_short=(
        "Ztráty jde odečíst: místo „padl vzor n“ dostane každý výstřel hodnotu Z, jejíž průměr míří přesně na "
        "ideální p(n). Platí se rozptylem, který roste zhruba jako ((1 − η)/η) na počet fotonů: při 10 % ztrát klesne "
        f"úspora vzorků úlohy 2 z {times_label(EXAMPLE.comparison.advantage)} na "
        f"{times_label(example_advantage(EXAMPLE_TRANSMISSION))} a při 20 % ztrát je GBS "
        f"{times_label(1 / example_advantage(LARGE_LOSS_TRANSMISSION))} horší než Monte Carlo. Pod kritickou "
        "propustností η_c = tanh r_max/(1 + tanh r_max) je rozptyl nekonečný."
    ),
    explanation=r"""
**Doložené.** Binomické ředění má inverzi: Kiss, Herzog a Leonhardt (1995) ukázali, že ztráty v detekci jde
numericky kompenzovat až po měření – pro každý stav spolehlivě při účinnosti nad 1/2, pod ní podle stavu.

**Oprava (náš přepis pro GBS-P).** Výstřel, ve kterém detektory napočítaly $m_i$ fotonů v módu $i$, dostane hodnotu

$$
Z(m) = \prod_i \binom{m_i}{n_i}\,\eta^{-n_i}\Bigl(1 - \tfrac{1}{\eta}\Bigr)^{m_i - n_i}
\quad\text{pro } m \ge n,\ \text{jinak } 0,
$$

a platí $\sum_m \mathrm{Bin}(k, m; \eta)\,Z(m) = [k = n]$: průměr $Z$ přes výstřely míří přesně na ideální $p(n)$,
ať je ztráta jakákoli – musí ale být známá. Hodnoty $Z$ střídají znaménko a rostou s počtem fotonů, a s nimi roste
rozptyl:

$$
\mathrm{Var}\,Z = \sum_k p(k)\prod_i g_i(k_i) - p(n)^2,\qquad
g_i(k) = \mathbb{E}_{m \sim \mathrm{Bin}(k,\eta)}\bigl[Z_i(m)^2\bigr] \approx \Bigl(\tfrac{1-\eta}{\eta}\Bigr)^{k}.
$$

**Kritická propustnost (naše odvození).** Ideální přístroj vyšle $t$ fotonů s pravděpodobností, která klesá jako
$(\tanh r_{\max})^t$, kdežto $\prod_i g_i$ roste jako $((1-\eta)/\eta)^t$. Součet konverguje jen pro
$\tanh r_{\max}\,(1-\eta)/\eta < 1$, tedy pro

$$
\eta > \eta_c = \frac{\tanh r_{\max}}{1 + \tanh r_{\max}} < \tfrac{1}{2}.
$$

U pěti úloh laboratoře je stlačení silné a $\eta_c \approx 0{,}49$. Je to hranice Kisse a kol. pro stlačené vakuum:
jeho rozdělení počtu fotonů má geometrický chvost a právě ten rozhoduje, kde kompenzace pod 1/2 ještě funguje. Nad
$\eta_c$ je rozptyl konečný, ale obrovský – relativní rozptyl jednoho výstřelu, a s ním počet výstřelů pro danou
přesnost, roste s klesající propustností exponenciálně.

**Čísla (náš výpočet, ladění po módech): kolikrát méně výstřelů GBS-P s opravou potřebuje než Monte Carlo scénářů.**

""" + advantage_table() + rf"""

Pro srovnání: pracovní stůl [simulátoru čipu](/fotonika/simulator-cipu) má ve výchozím nastavení ztrátu vazby
{czech_decimal(DEFAULT_COUPLING_LOSS_DB, 1)} dB na každém přechodu vlákno–čip, útlum světlovodů
{czech_decimal(DEFAULT_WAVEGUIDE_LOSS_DB_PER_CM, 1)} dB/cm a detektor SNSPD s účinností
{percent_label(DETECTORS[BENCH_DETECTOR].efficiency)}, dohromady pro dvoumódový čip propustnost
kolem {percent_label(typical_bench_transmission(BENCH_MODE_COUNT))} – hluboko pod $\eta_c$. Laboratoř tuto hodnotu
kreslí do grafu.
""",
    further_reading=(
        Reading(KISS_HERZOG_LEONHARDT_1995, "kompenzace ztrát inverzní binomickou transformací a hranice 1/2"),
        Reading(ANDERSEN_SHAN_ADVANTAGE, "rozptyl odhadu GBS-P bez ztrát"),
    ),
    related_caveats=(REAL_HARDWARE,),
)

THRESHOLD_DETECTORS = TheoryTopic(
    anchor="zt-prahove",
    title="Prahové detektory na odhad GBS-P nestačí",
    in_short=(
        "Prahový detektor pozná jen „aspoň jeden foton“. Odhad GBS-P ale potřebuje přesný počet fotonů v každém "
        "módu – všech pět úloh má v některém módu aspoň dva, takže cílový vzor vůbec nerozliší. I u vzoru bez "
        f"opakování, třeba (1, 1), by četnost kliků dala odhad {czech_decimal(collision_free_click_ratios()[1], 1)}× "
        "vyšší než správný, a to bez jediné ztráty."
    ),
    explanation=r"""
**Co prahový detektor vidí.** Vzor kliků $c \in \{0, 1\}^M$: v módu $i$ klikne, když dorazí aspoň jeden foton.
Jeho pravděpodobnost je součet $p_\eta(m)$ přes všechny vzory $m$ se stejnou „podporou“ – v módech s klikem
$m_i \ge 1$, jinde $m_i = 0$:

$$
P(c) = \sum_k p(k)\prod_{i:\,c_i = 1}\bigl(1 - (1-\eta)^{k_i}\bigr)\prod_{i:\,c_i = 0}(1-\eta)^{k_i}.
$$

V literatuře se počítá torontiánem (Quesada, Arrazola a Killoran 2018); tady stačí stejné ředění jako výše.

""" + rf"""
**Proč to nestačí (náš výpočet).** Vzory $(8, 8)$, $(12, 4)$ nebo $(6, 6, 6)$ prahové detektory nikdy neukážou –
vidí jen „oba módy kliknuly“, a to se stane skoro v každém výstřelu. Laboratoř přesto spočítá, co by dosazení četnosti
kliků do vzorce GBS-P dalo: u úlohy 2 při 10 % ztrát odhad
{czech_decimal(1 + example_point(EXAMPLE_TRANSMISSION).threshold_bias, 0)}× vyšší než správná hodnota. U vzoru bez
opakování, třeba $(1, 1)$ pro $\mathbb{{E}}[X_1 X_2]$ dvou aktiv s korelací 0{{,}}5, jsou kliky k vzoru blíž, ale
pořád do nich spadnou i výstřely $(3, 1)$, $(2, 2)$ a všechny další: bez ztrát je četnost kliků
{czech_decimal(collision_free_click_ratios()[0], 1)}× vyšší než $p(1, 1)$ a odhad
{czech_decimal(collision_free_click_ratios()[1], 1)}× vyšší než správně. Odhad GBS-P tedy vyžaduje detektory
rozlišující počet fotonů – TES, nebo multiplexované SNSPD, jak popisuje háček o hardwaru.
""",
    further_reading=(
        Reading(QUESADA_THRESHOLD_2018, "GBS s prahovými detektory a torontián"),
        Reading(QI_NOISY_SIMULABILITY, "prahové detektory s účinností a temnými kliky v modelu šumu"),
    ),
    related_caveats=(REAL_HARDWARE,),
)

SIMULABILITY = TheoryTopic(
    anchor="zt-simulace",
    title="Hranice klasické simulace podle Qi a kol.",
    in_short=(
        "Postačující podmínka Qi a kol. (2020) pro klasickou simulaci ztrátového GBS závisí na povolené chybě ε. Pro "
        "bezšumové detektory a přesnou simulaci nedává nic – ztrátový stlačený stav není nikdy přesně klasický. "
        f"S ε = 1 % vyjde pro úlohy laboratoře propustnost kolem {percent_label(EXAMPLE.simulable_transmission)}: "
        "výhodu z této strany nic nevylučuje dřív, než ji zničí ztráty v samotném estimátoru."
    ),
    explanation=r"""
**Co dokázali.** Qi, Brod, Quesada a García-Patrón (2020) dávají podmínku, za které jde šumové GBS simulovat
klasicky v polynomiálním čase s chybou nejvýš $\varepsilon$ (vzdálenost rozdělení výstřelů) – jejich nerovnost (1):

$$
\operatorname{sech}\!\left[\tfrac12\,\Theta\!\left(\ln\frac{1 - 2q_D}{\eta e^{-2r} + 1 - \eta}\right)\right]
> e^{-\varepsilon^2/(4K)},
$$

kde $r$ je parametr stlačení, $\eta$ celková propustnost, $q_D = p_D/\eta_D$ kvalita detektorů (temné kliky $p_D$
ku účinnosti $\eta_D$), $K$ počet stlačených módů a $\Theta(x) = \max(x, 0)$. Postup stojí na pozorování
Rahimiho-Keshariho, Ralpha a Cavese (2016): když má stav nezápornou kvazipravděpodobnost v nějakém uspořádání
a detektory v uspořádání opačném, je celé měření klasické vzorkování. Autoři sami píší, že pro bezšumové detektory
($q_D = 0$) a přesnou simulaci ($\varepsilon = 0$) dává nerovnost triviální $\eta < 0$: stlačený stav se ztrátou
nikdy nestane přesně klasickým, jen se mu libovolně blíží. Asymptoticky je ztrátové GBS simulovatelné, když
průměrný počet přeživších fotonů klesne pod řád $\varepsilon\sqrt{\bar N}$.

""" + rf"""
**Co to dává pro úlohy laboratoře (náš dopočet).** Bez temných kliků je levá strana rovna $2\sqrt{{V}}/(1+V)$, kde
$V = \eta e^{{-2r}} + 1 - \eta$ je rozptyl stlačené kvadratury po ztrátě (vakuum 1). Podmínka tedy říká
$V > V^*(\varepsilon, K)$, čili $\eta < (1 - V^*)/(1 - e^{{-2r}})$; rozhoduje nejsilněji stlačený mód.
S $\varepsilon = 1\,\%$ vychází u pěti úloh hranice mezi {percent_label(simulable_transmission_range()[0], 1)} a {percent_label(simulable_transmission_range()[1], 1)} propustnosti.
Laboratoř ji kreslí, ale o ničem nerozhoduje: estimátor přestane být použitelný už kolem 90 % propustnosti.

**Co z toho neplyne.** Nad touto hranicí není těžkost dokázaná – podmínka je postačující, ne nutná. Malé úlohy
laboratoře navíc simuluje klasicky sama aplikace ([háček „GBS je tady simulované klasicky“](/gbs/hacky#klasicka-simulace))
a u velkých experimentů posouvají hranici tenzorové sítě Oha a kol. (2024) a algoritmy Bulmera a kol. (2022). Závěr
pro disertaci: požadavek na hardware neurčují věty o simulovatelnosti, ale sám estimátor.
""",
    further_reading=(
        Reading(QI_NOISY_SIMULABILITY, "nerovnost (1) a její asymptotika"),
        Reading(RAHIMI_KESHARI_2016, "kvazipravděpodobnosti stavu a detektorů jako klasické vzorkování"),
        Reading(OSZMANIEC_BROD_2018, "ztrátový boson sampling klasicky"),
        Reading(GARCIA_PATRON_2019, "ztráty s hloubkou obvodu"),
        Reading(OH_CLASSICAL_SIMULATION, "tenzorové sítě proti velkým experimentům"),
        Reading(BULMER_BOUNDARY, "hranice přesné klasické simulace ideálního GBS"),
    ),
    related_caveats=(CLASSICAL_SIMULATION,),
)

OPEN_QUESTIONS = TheoryTopic(
    anchor="zt-otazky",
    title="Co z toho plyne a otevřené otázky",
    in_short=(
        "Pro odhad GBS-P z četnosti jednoho vzoru musí k detektorům dorazit přes 90 % fotonů a detektory musí "
        "fotony počítat, jinak výhoda proti Monte Carlu zmizí; dnešní fotonické čipy jsou hluboko pod tím. Otevřené "
        "zůstává, jestli existuje odhad, který se ztrátami počítá od začátku a platí za ně méně."
    ),
    explanation=r"""
**Shrnutí (náš závěr).** Čtvrtý zdroj chyby je ze čtyř nejtvrdší: zdroje 1–3 jsou vlastnosti dat a úlohy, které
jde předem změřit a částečně napravit, ztráty jsou vlastnost přístroje a u dnešních přístrojů překračují to, co odhad
GBS-P snese, několikanásobně. Diagnostika je tu jednoduchá – stačí změřit propustnost a srovnat ji s $\eta_c$
a s křivkou úspory vzorků –, lék ale zatím chybí.

**Otevřené otázky (náš návrh dalšího výzkumu).**

1. **Odhad, který se ztrátami počítá.** Inverzní binomická transformace je jen jeden nestranný odhad. Regularizované
   inverze a odhady maximální věrohodnosti z rekonstrukce fotonových statistik mění kousek vychýlení za mnohem menší
   rozptyl – kolik výhody by zachránily?
2. **Přeladit stlačení na ztráty.** Naladit přístroj tak, aby *po* ztrátě dorazilo do každého módu v průměru $n_i$
   fotonů. Mění to tvar rozdělení, ne jen průměr, takže vychýlení neodstraní – může ho ale zmenšit.
3. **Jiná cílová veličina.** Ztrátový přístroj vzorkuje přesně ze smíšeného gaussovského stavu s maticí $A$. Je
   nějaký finanční integrál, pro který je právě jeho pravděpodobnost vzoru tím správným číslem, bez opravy?
4. **Nerovnoměrné ztráty.** Na čipu se cesty liší délkou i počtem děličů; taková ztráta s interferometrem nekomutuje
   a vyžaduje hafniány smíšeného stavu. Simulátor čipu má součástky i ztráty, chybí mu stlačené světlo.
5. **Další šum.** Temné kliky, částečná rozlišitelnost fotonů a chyby fází; a jak si vede druhý odhad Andersena
   a Shan, GBS-I, který sčítá přes všechny vzory daného stupně.
6. **Experiment.** Změřit vychýlení a rozptyl proti ztrátě na skutečném přístroji; pro jednofotonovou obdobu
   (boson sampling na čipu) je kandidátem ORCA PT-1 v PSNC dostupný přes EuroHPC.
""",
    further_reading=(
        Reading(KISS_HERZOG_LEONHARDT_1995, "odkud vzít lepší kompenzaci ztrát"),
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "odhady GBS-P a GBS-I"),
        Reading(QI_NOISY_SIMULABILITY, "temné kliky a účinnost detektorů v jednom modelu"),
    ),
)

TOPICS: Tuple[TheoryTopic, ...] = (THINNING, NAIVE_BIAS, CORRECTION, THRESHOLD_DETECTORS, SIMULABILITY, OPEN_QUESTIONS)
