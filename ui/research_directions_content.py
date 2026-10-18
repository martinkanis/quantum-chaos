"""Texts of the research directions page: our hypothesis that random matrix spectra decide the GBS advantage."""

from __future__ import annotations

from typing import Tuple

from gbs.spectrum_study import SpectrumSaving
from randommatrix.min_variance import predicted_in_sample, predicted_out_of_sample
from ui.caveats_content import CLASSICAL_SIMULATION, CLOSED_FORM
from ui.literature_review_content import BULMER_BOUNDARY
from ui.random_matrix_content import BOUCHAUD_POTTERS_REVIEW, BUN_BOUCHAUD_POTTERS, LALOUX_1999, czech_decimal
from ui.theory_content import ANDERSEN_SHAN_ADVANTAGE, ANDERSEN_SHAN_EXPECTATIONS, Reading, Source, TheoryTopic

SOURCES_ANCHOR = "vs-zdroje"

STUDY_ASSET_COUNT = 6
STUDY_CORRELATIONS = (0.0, 0.1, 0.25, 0.5, 0.75, 0.9)
STUDY_DEGREES = (4, 6)
STUDY_SAVINGS: Tuple[SpectrumSaving, ...] = (
    SpectrumSaving(0.0, 4, market_mode_share=0.1667, best_strength=0.65, sample_saving=8.991),
    SpectrumSaving(0.0, 6, market_mode_share=0.1667, best_strength=0.7, sample_saving=20.281),
    SpectrumSaving(0.1, 4, market_mode_share=0.2500, best_strength=0.85, sample_saving=2.178),
    SpectrumSaving(0.1, 6, market_mode_share=0.2500, best_strength=0.9, sample_saving=5.702),
    SpectrumSaving(0.25, 4, market_mode_share=0.3750, best_strength=0.9, sample_saving=3.949),
    SpectrumSaving(0.25, 6, market_mode_share=0.3750, best_strength=0.9, sample_saving=10.966),
    SpectrumSaving(0.5, 4, market_mode_share=0.5833, best_strength=0.9, sample_saving=4.892),
    SpectrumSaving(0.5, 6, market_mode_share=0.5833, best_strength=0.9, sample_saving=13.491),
    SpectrumSaving(0.75, 4, market_mode_share=0.7917, best_strength=0.9, sample_saving=5.093),
    SpectrumSaving(0.75, 6, market_mode_share=0.7917, best_strength=0.9, sample_saving=14.024),
    SpectrumSaving(0.9, 4, market_mode_share=0.9167, best_strength=0.9, sample_saving=5.122),
    SpectrumSaving(0.9, 6, market_mode_share=0.9167, best_strength=0.9, sample_saving=14.099),
)
"""gbs.spectrum_study.spectrum_savings(STUDY_ASSET_COUNT, STUDY_CORRELATIONS, STUDY_DEGREES, squeezing slider grid
of page 2). Stored because it takes seconds; a test recomputes it."""

NOISE_EXAMPLE_RATIO = 0.5
NOISE_EXAMPLE_DEGREE = 4
NOISE_EXAMPLE_MOMENT_RATIO = (
    predicted_in_sample(NOISE_EXAMPLE_RATIO) / predicted_out_of_sample(NOISE_EXAMPLE_RATIO)
) ** (NOISE_EXAMPLE_DEGREE / 2)
"""Promised over realised d-th moment of the optimised portfolio, ((1 − q)²)^(d/2) = (1 − q)^d."""

QUESADA_SPEEDUP = Source(
    "Quesada, N., Chadwick, R. S., Bell, B. A., Arrazola, J. M., Vincent, T., Qi, H., García-Patrón, R.: "
    "*Quadratic speed-up for simulating Gaussian boson sampling*. PRX Quantum 3 (2022), 010306, "
    "[doi:10.1103/PRXQuantum.3.010306](https://doi.org/10.1103/PRXQuantum.3.010306), "
    "[arXiv:2010.15595](https://arxiv.org/abs/2010.15595)"
)

LEAD = (
    "Vlastní výzkumný námět, ne doložený výsledek: spojit teorii náhodných matic s Monte Carlem na Gaussian Boson "
    "Sampleru. Stránka popisuje hypotézu, první výpočet na malém modelu, háčky a otázky, které by bylo potřeba "
    "zodpovědět. Čísla jsou z kódu aplikace a hlídá je test; literatura je u každé kapitoly."
)

IN_SHORT = (
    "GBS kóduje do stlačení a interferometru vlastní čísla a vlastní vektory kovarianční matice. Teorie náhodných "
    "matic říká, jak spektrum skutečné korelační matice akcií vypadá: jeden velký tržní mód a pás šumu. Hypotéza "
    "zní, že právě tvar spektra rozhoduje, kolik vzorků GBS ušetří. První výpočet na šesti aktivech to podporuje, "
    "zároveň ale ukazuje, že šum v odhadnuté matici je mnohem větší problém než chyba vzorkování."
)


def saving(correlation: float, degree: int) -> SpectrumSaving:
    return next(item for item in STUDY_SAVINGS if item.correlation == correlation and item.degree == degree)


def savings_table() -> str:
    rows = [
        "| korelace ρ | podíl tržního módu | stupeň 4: úspora vzorků | stupeň 6: úspora vzorků |",
        "|---|---|---|---|",
    ]
    for correlation in STUDY_CORRELATIONS:
        fourth, sixth = saving(correlation, 4), saving(correlation, 6)
        rows.append(
            f"| {czech_decimal(correlation)} | {czech_decimal(100 * fourth.market_mode_share, 0)} % "
            f"| {czech_decimal(fourth.sample_saving, 1)}× | {czech_decimal(sixth.sample_saving, 1)}× |"
        )
    return "\n".join(rows)


def study_findings() -> str:
    independent = saving(0.0, 4).sample_saving
    weak = saving(0.1, 4).sample_saving
    strong = saving(0.9, 4).sample_saving
    return (
        "**Co z tabulky plyne (náš výpočet).** U nezávislých aktiv ušetří GBS pro moment 4. stupně "
        f"{czech_decimal(independent, 1)}× vzorků. Slabá korelace ρ = 0,1 úsporu sníží na "
        f"{czech_decimal(weak, 1)}×; s rostoucím tržním módem se vrací a ustálí kolem "
        f"{czech_decimal(strong, 1)}×. Závislost na spektru tedy existuje a není monotónní.\n\n"
        "**Náš výklad.** Stlačení se nastavuje podle největšího vlastního čísla. U nezávislých aktiv jsou všechna "
        "vlastní čísla stejná a všechny módy jsou stlačené stejně. Při slabé korelaci tržní mód „spotřebuje“ "
        "stlačení a ostatní módy dostanou méně, přestože portfolio je potřebuje. Při silné korelaci leží "
        "rovnoměrné portfolio skoro celé ve směru tržního módu a GBS vzorkuje přesně to, co je potřeba. Ověřit "
        "by to šlo změnou vah portfolia, aby s tržním módem svíraly různý úhel.\n"
    )


def _noise_example() -> str:
    moment_ratio = 1 / NOISE_EXAMPLE_MOMENT_RATIO
    return (
        f"\n**Příklad (náš dopočet).** Při q = {czech_decimal(NOISE_EXAMPLE_RATIO, 1)} a momentu "
        f"{NOISE_EXAMPLE_DEGREE}. stupně je skutečný moment optimalizovaného portfolia "
        f"{czech_decimal(moment_ratio, 0)}× větší, než jaký by GBS z odhadnuté matice velmi přesně spočítal. "
        "Chyba vzorkování GBS je proti tomu zanedbatelná: se 100 000 vzorky jsou to jednotky promile.\n"
    )


HYPOTHESIS = TheoryTopic(
    anchor="vs-hypoteza",
    title="Hypotéza: spektrum rozhoduje o výhodě GBS",
    in_short=(
        "Výhoda GBS závisí na kovarianční matici. Teorie náhodných matic popisuje, jak tyto matice u akcií "
        "vypadají. Spojení obojího by mohlo říct, kde ve financích GBS dává smysl (vlastní hypotéza)."
    ),
    explanation=r"""
**Co víme.** Andersen a Shan ukazují, že odhad GBS-P potřebuje pro některé gaussovské integrály řádově méně
vzorků než klasické Monte Carlo, ale ne pro všechny: podíl matic s výhodou závisí na rozměru a stupni úlohy.
GBS přitom matici zpracovává přes její rozklad na vlastní čísla (síly stlačení) a vlastní vektory
(interferometr).

**Co víme o maticích akcií.** Spektrum skutečné korelační matice má jedno velké vlastní číslo (tržní mód,
u Laloux a kol. asi 25× nad horní mezí šumu), několik sektorových a široký pás šumu podle Marčenka
a Pastura.

**Hypotéza (náš odhad).** O úspoře vzorků nerozhoduje „náhodná matice“ z článků o GBS, ale tvar spektra
a poloha vah portfolia vůči tržnímu módu. Teorie náhodných matic dává realistické rodiny spekter, na kterých
by šlo výhodu GBS měřit systematicky – místo náhodně vybraných matic.
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_ADVANTAGE, "podíl matic, pro které má GBS-P výhodu"),
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "odhad GBS-P a jeho rozptyl"),
        Reading(LALOUX_1999, "jak vypadá spektrum korelační matice akcií"),
    ),
)

FIRST_STUDY = TheoryTopic(
    anchor="vs-prvni-vypocet",
    title="První výpočet: šest aktiv a jeden tržní mód",
    in_short=(
        "Rovnoměrné portfolio šesti aktiv se společnou korelací ρ. Pro každé ρ najdeme nejlepší sílu stlačení "
        "a spočítáme, kolikrát méně vzorků GBS potřebuje než Monte Carlo pro stejnou relativní chybu."
    ),
    explanation=r"""
**Model.** Korelační matice se stejnou korelací ρ mezi všemi dvojicemi má jedno vlastní číslo $1 + 5\rho$
(tržní mód) a pět stejných vlastních čísel $1 - \rho$. Je to nejjednodušší spektrum „tržní mód plus šum“.

**Co měříme.** Konstanty relativní chyby $c$ z 2. stránky: chyba po $N$ vzorcích je $c/\sqrt{N}$. Úspora
vzorků je $(c_{\text{MC}}/c_{\text{GBS}})^2$, u GBS pro nejlepší sílu stlačení na mřížce posuvníku 2. stránky
(0,1 až 0,95). Je to teoretická hodnota pro velké $N$, ne simulace.

**Omezení.** Jen šest módů (víc simulátor v aplikaci nezvládne), rovnoměrné váhy a jeden typ spektra.
Sektory ani pás šumu podle Marčenka a Pastura tu nejsou.
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "odhad GBS-P, ze kterého vychází konstanta chyby"),
    ),
    related_caveats=(CLOSED_FORM,),
)

NOISY_INPUT = TheoryTopic(
    anchor="vs-sum-v-matici",
    title="Háček: GBS dostane odhadnutou matici",
    in_short=(
        "Do GBS se kóduje matice odhadnutá z historie, ne ta pravá. Chyba z odhadu matice je o řády větší než "
        "chyba vzorkování, kterou GBS zmenšuje. Vyčistit matici je proto potřeba vždy."
    ),
    explanation=r"""
**Proč.** Pro portfolio optimalizované na odhadnuté matici $E$ uvádějí Bouchaud a Potters slíbený rozptyl
$(1-q)$ a skutečný $1/(1-q)$ krát optimum. Moment $d$-tého stupně gaussovského výnosu je úměrný rozptylu na
$d/2$, takže slíbený moment je ke skutečnému v poměru

$$
\left( \frac{1-q}{1/(1-q)} \right)^{d/2} = (1-q)^{d} .
$$

Tento vztah jsme odvodili sami ze vzorců Bouchauda a Potterse; platí ve stejné limitě jako ony.
""" + _noise_example() + r"""
**Důsledek pro výzkum.** Srovnávat GBS s Monte Carlem na „pravé“ matici měří jen chybu vzorkování. Pro
finanční použití je potřeba nejdřív matici vyčistit (ořezání, shrinkage, RIE) a teprve pak řešit, čím ji
vzorkovat. Čištění je klasický krok a GBS ho nenahradí.
""",
    further_reading=(
        Reading(BOUCHAUD_POTTERS_REVIEW, "slíbené a skutečné riziko"),
        Reading(BUN_BOUCHAUD_POTTERS, "jak matici vyčistit"),
    ),
)

OPEN_QUESTIONS = TheoryTopic(
    anchor="vs-otazky",
    title="Otevřené otázky a co by bylo potřeba",
    in_short=(
        "Pět otázek, které by z hypotézy udělaly výsledek – a háčky, kvůli kterým může vyjít negativně. "
        "I negativní výsledek by šel publikovat."
    ),
    explanation=r"""
1. **Úhel vah a tržního módu.** Jak se úspora mění, když portfolio není rovnoměrné (např. long–short nebo
   portfolio s minimálním rozptylem, které tržní mód potlačuje)?
2. **Realistická spektra.** Spektrum „tržní mód + sektory + pás Marčenka a Pastura“ pro desítky aktiv. To je
   mimo dosah simulátoru v aplikaci (6 módů) a vyžaduje rychlejší klasickou simulaci GBS.
3. **Surová vs. vyčištěná matice.** Mění čištění spektrum tak, že se výhoda GBS zvětší, nebo zmenší?
4. **Úlohy bez vzorce.** Momenty portfolia mají uzavřený vzorec, takže GBS tu slouží jen jako test. Smysl
   mají úlohy bez vzorce, např. monomy z 3. stránky nebo nelineární payoffy – na spektrech z teorie
   náhodných matic.
5. **Hranice klasické simulace.** Kde je GBS s takovou maticí ještě klasicky simulovatelný? Bulmer a kol.
   a Quesada a kol. tuto hranici posunuli; výhoda ve vzorcích se musí porovnat s cenou simulace.

**Jak by vypadal výsledek.** Mapa „spektrum × váhy → úspora vzorků“, ze které je vidět, pro jaké portfolio
a trh má smysl GBS vůbec zkoušet. Pokud by mapa ukázala, že realistická spektra výhodu nemají, je to také
užitečný (negativní) výsledek.
""",
    further_reading=(
        Reading(BULMER_BOUNDARY, "hranice kvantové výhody GBS"),
        Reading(QUESADA_SPEEDUP, "rychlejší klasická simulace GBS"),
        Reading(ANDERSEN_SHAN_ADVANTAGE, "úlohy, kde GBS-P výhodu má"),
    ),
    related_caveats=(CLASSICAL_SIMULATION,),
)

TOPICS: Tuple[TheoryTopic, ...] = (HYPOTHESIS, FIRST_STUDY, NOISY_INPUT, OPEN_QUESTIONS)
