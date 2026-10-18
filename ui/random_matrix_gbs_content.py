"""Texts of the random matrices and GBS page: our hypothesis that the spectrum decides the GBS advantage."""

from __future__ import annotations

from math import floor, log10
from typing import Tuple

from gbs.spectrum_study import SpectrumSaving
from randommatrix.min_variance import predicted_in_sample, predicted_out_of_sample
from ui.caveats_content import CLASSICAL_SIMULATION, CLOSED_FORM, DISCARDED_SHOTS, SIGN_PROBLEM
from ui.literature_review_content import BULMER_BOUNDARY
from ui.random_matrix_content import BOUCHAUD_POTTERS_REVIEW, BUN_BOUCHAUD_POTTERS, LALOUX_1999, czech_decimal
from ui.theory_content import ANDERSEN_SHAN_ADVANTAGE, ANDERSEN_SHAN_EXPECTATIONS, Reading, Source, TheoryTopic

SOURCES_ANCHOR = "vs-zdroje"

STUDY_ASSET_COUNT = 6
STUDY_CORRELATIONS = (0.0, 0.02, 0.05, 0.1, 0.25, 0.5, 0.9)
STUDY_DEGREES = (4, 6)
LONG_SHORT_DEGREE = 4
EQUAL_SAVINGS: Tuple[SpectrumSaving, ...] = (
    SpectrumSaving(0.0, 4, market_mode_share=0.1667, best_strength=0.65, sample_saving=8.991,
                   useful_shot_share=0.2063, pattern_mismatch=1.185, cancellation=1),
    SpectrumSaving(0.0, 6, market_mode_share=0.1667, best_strength=0.7, sample_saving=20.28,
                   useful_shot_share=0.1561, pattern_mismatch=1.547, cancellation=1),
    SpectrumSaving(0.02, 4, market_mode_share=0.1833, best_strength=0.7, sample_saving=0.8161,
                   useful_shot_share=0.2064, pattern_mismatch=11.0, cancellation=1),
    SpectrumSaving(0.02, 6, market_mode_share=0.1833, best_strength=0.75, sample_saving=1.529,
                   useful_shot_share=0.1534, pattern_mismatch=18.29, cancellation=1),
    SpectrumSaving(0.05, 4, market_mode_share=0.2083, best_strength=0.75, sample_saving=1.292,
                   useful_shot_share=0.2004, pattern_mismatch=6.818, cancellation=1),
    SpectrumSaving(0.05, 6, market_mode_share=0.2083, best_strength=0.85, sample_saving=2.957,
                   useful_shot_share=0.1467, pattern_mismatch=9.115, cancellation=1),
    SpectrumSaving(0.1, 4, market_mode_share=0.2500, best_strength=0.85, sample_saving=2.178,
                   useful_shot_share=0.1803, pattern_mismatch=3.712, cancellation=1),
    SpectrumSaving(0.1, 6, market_mode_share=0.2500, best_strength=0.9, sample_saving=5.702,
                   useful_shot_share=0.1213, pattern_mismatch=3.967, cancellation=1),
    SpectrumSaving(0.25, 4, market_mode_share=0.3750, best_strength=0.9, sample_saving=3.949,
                   useful_shot_share=0.1283, pattern_mismatch=1.514, cancellation=1),
    SpectrumSaving(0.25, 6, market_mode_share=0.3750, best_strength=0.9, sample_saving=10.97,
                   useful_shot_share=0.0828, pattern_mismatch=1.449, cancellation=1),
    SpectrumSaving(0.5, 4, market_mode_share=0.5833, best_strength=0.9, sample_saving=4.892,
                   useful_shot_share=0.1104, pattern_mismatch=1.073, cancellation=1),
    SpectrumSaving(0.5, 6, market_mode_share=0.5833, best_strength=0.9, sample_saving=13.49,
                   useful_shot_share=0.0739, pattern_mismatch=1.064, cancellation=1),
    SpectrumSaving(0.9, 4, market_mode_share=0.9167, best_strength=0.9, sample_saving=5.122,
                   useful_shot_share=0.1073, pattern_mismatch=1.001, cancellation=1),
    SpectrumSaving(0.9, 6, market_mode_share=0.9167, best_strength=0.9, sample_saving=14.10,
                   useful_shot_share=0.0724, pattern_mismatch=1.001, cancellation=1),
)
"""spectrum_savings(equal_weights(6), STUDY_CORRELATIONS, STUDY_DEGREES, squeezing slider grid of page 2)."""
LONG_SHORT_SAVINGS: Tuple[SpectrumSaving, ...] = (
    SpectrumSaving(0.0, 4, market_mode_share=0.1667, best_strength=0.65, sample_saving=8.991,
                   useful_shot_share=0.2063, pattern_mismatch=1.185, cancellation=1),
    SpectrumSaving(0.02, 4, market_mode_share=0.1833, best_strength=0.7, sample_saving=0.5105,
                   useful_shot_share=0.2064, pattern_mismatch=17.45, cancellation=1.26),
    SpectrumSaving(0.05, 4, market_mode_share=0.2083, best_strength=0.75, sample_saving=0.4225,
                   useful_shot_share=0.2004, pattern_mismatch=20.44, cancellation=1.731),
    SpectrumSaving(0.1, 4, market_mode_share=0.2500, best_strength=0.85, sample_saving=0.2702,
                   useful_shot_share=0.1803, pattern_mismatch=28.64, cancellation=2.778),
    SpectrumSaving(0.25, 4, market_mode_share=0.3750, best_strength=0.9, sample_saving=0.04467,
                   useful_shot_share=0.1283, pattern_mismatch=122.7, cancellation=9.0),
    SpectrumSaving(0.5, 4, market_mode_share=0.5833, best_strength=0.9, sample_saving=0.001828,
                   useful_shot_share=0.1104, pattern_mismatch=2576, cancellation=49.0),
    SpectrumSaving(0.9, 4, market_mode_share=0.9167, best_strength=0.9, sample_saving=4.997e-07,
                   useful_shot_share=0.1073, pattern_mismatch=9.161e06, cancellation=3025),
)
"""spectrum_savings(long_short_weights(6), STUDY_CORRELATIONS, (LONG_SHORT_DEGREE,), same grid). Both tables are
stored because they take seconds; a test recomputes them."""

SINGULAR_CORRELATION = 1e-4
SINGULAR_STRENGTH = 0.65
SINGULAR_MISMATCH = 15.97
"""Mismatch of the equally weighted portfolio for degree 4 at ρ = SINGULAR_CORRELATION and the strength that is best
at ρ = 0: tiny correlations do not bring back the mismatch of independent assets. A test recomputes it."""

NOISE_EXAMPLE_RATIO = 0.5
NOISE_EXAMPLE_DEGREE = 4
NOISE_EXAMPLE_MOMENT_RATIO = (
    predicted_in_sample(NOISE_EXAMPLE_RATIO) / predicted_out_of_sample(NOISE_EXAMPLE_RATIO)
) ** (NOISE_EXAMPLE_DEGREE / 2)
"""Promised over realised d-th moment of the optimised portfolio, ((1 − q)²)^(d/2) = (1 − q)^d."""

SIGNIFICANT_DIGITS = 2
SMALLEST_PLAIN_SAVING = 1e-3
SUPERSCRIPT_DIGITS = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")

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


def saving(savings: Tuple[SpectrumSaving, ...], correlation: float, degree: int) -> SpectrumSaving:
    return next(item for item in savings if item.correlation == correlation and item.degree == degree)


def round_significant(value: float, digits: int = SIGNIFICANT_DIGITS) -> float:
    return round(value, digits - 1 - floor(log10(abs(value))))


def saving_label(value: float) -> str:
    """9,0× for savings, 0,045× for losses; below 0,001 as a power of ten, 5,0·10⁻⁷×."""
    if value >= 1:
        return f"{czech_decimal(value, 1)}×"
    if value >= SMALLEST_PLAIN_SAVING:
        decimals = SIGNIFICANT_DIGITS - 1 - floor(log10(value))
        return f"{czech_decimal(value, decimals)}×"
    exponent = floor(log10(value))
    mantissa = czech_decimal(value / 10 ** exponent, 1)
    return f"{mantissa}·10{str(exponent).translate(SUPERSCRIPT_DIGITS)}×"


def times_more_samples(sample_saving: float) -> str:
    """How many times more samples GBS needs, for savings below 1: 0,045 → 22."""
    return f"{round_significant(1 / sample_saving):.0f}"


def percent(value: float) -> str:
    return f"{czech_decimal(100 * value, 0)} %"


def _in_short() -> str:
    aligned = saving(EQUAL_SAVINGS, 0.9, 4).sample_saving
    hedged = saving(LONG_SHORT_SAVINGS, 0.25, LONG_SHORT_DEGREE).sample_saving
    return (
        "GBS kóduje do stlačení a interferometru vlastní čísla a vlastní vektory kovarianční matice. Teorie "
        "náhodných matic říká, jak spektrum skutečné korelační matice akcií vypadá: jeden velký tržní mód a pás "
        "šumu. Hypotéza zní, že o úspoře vzorků rozhoduje tvar spektra spolu s polohou vah portfolia. První výpočet "
        "na šesti aktivech to podporuje: pro portfolio ve směru trhu GBS při silné korelaci ušetří "
        f"{saving_label(aligned)} vzorků, portfolio long–short jich při ρ = 0,25 potřebuje "
        f"{times_more_samples(hedged)}× víc než Monte Carlo. Šum v odhadnuté matici je přitom ještě větší problém "
        "než chyba vzorkování."
    )


IN_SHORT = _in_short()


def savings_table() -> str:
    rows = [
        "| korelace ρ | podíl tržního módu | rovnoměrné, stupeň 4 | rovnoměrné, stupeň 6 | long–short, stupeň 4 |",
        "|---|---|---|---|---|",
    ]
    for correlation in STUDY_CORRELATIONS:
        fourth, sixth = saving(EQUAL_SAVINGS, correlation, 4), saving(EQUAL_SAVINGS, correlation, 6)
        hedged = saving(LONG_SHORT_SAVINGS, correlation, LONG_SHORT_DEGREE)
        rows.append(
            f"| {czech_decimal(correlation)} | {percent(fourth.market_mode_share)} "
            f"| {saving_label(fourth.sample_saving)} | {saving_label(sixth.sample_saving)} "
            f"| {saving_label(hedged.sample_saving)} |"
        )
    return "\n".join(rows)


SAVINGS_TABLE_HINT = (
    "Kolikrát méně vzorků potřebuje GBS-P než klasické Monte Carlo pro stejnou relativní chybu. Hodnota pod 1 "
    "znamená, že GBS potřebuje vzorků víc."
)


def study_findings() -> str:
    independent = saving(EQUAL_SAVINGS, 0.0, 4)
    weak = saving(EQUAL_SAVINGS, 0.02, 4)
    strong = saving(EQUAL_SAVINGS, 0.9, 4)
    strong_sixth = saving(EQUAL_SAVINGS, 0.9, 6)
    hedged = saving(LONG_SHORT_SAVINGS, 0.25, LONG_SHORT_DEGREE)
    hedged_strong = saving(LONG_SHORT_SAVINGS, 0.5, LONG_SHORT_DEGREE)
    return (
        "**Co z tabulky plyne (náš výpočet).**\n\n"
        f"- *Rovnoměrné portfolio:* u přesně nezávislých aktiv ušetří GBS pro moment 4. stupně "
        f"{saving_label(independent.sample_saving)} vzorků, ale stačí korelace ρ = 0,02 a je horší než Monte Carlo "
        f"({saving_label(weak.sample_saving)}). S rostoucím tržním módem se úspora vrací a ustálí na "
        f"{saving_label(strong.sample_saving)}.\n"
        f"- *Portfolio long–short:* s rostoucí korelací se GBS rychle zhoršuje – při ρ = 0,25 potřebuje "
        f"{times_more_samples(hedged.sample_saving)}× víc vzorků než Monte Carlo, při ρ = 0,5 asi "
        f"{times_more_samples(hedged_strong.sample_saving)}× víc.\n\n"
        "**Proč (náš rozbor, ověřený výpočtem).** Konstanta chyby odhadu GBS-P se dá rozložit na dvě složky:\n\n"
        "$$\n"
        r"c_{\text{GBS}}^2 = \frac{1}{4}\left(\frac{m}{P_d} - 1\right) ."
        "\n$$\n\n"
        "$P_d$ je podíl výstřelů s přesně $d$ fotony (ostatní se zahodí) a $m \\ge 1$ je nesoulad: jak moc se "
        "poměr, v jakém přístroj vzory fotonů ukazuje, liší od poměru, v jakém vzory nesou moment. Při dokonalé "
        "shodě je $m = 1$.\n\n"
        f"1. *Nezávislá aktiva:* vzory s lichým počtem fotonů v některém detektoru jsou nemožné a zároveň k momentu "
        f"nic nepřispívají. Nesoulad je malý ($m$ = {czech_decimal(independent.pattern_mismatch, 1)}) a užitečných "
        f"výstřelů je {percent(independent.useful_shot_share)}.\n"
        "2. *Slabá korelace:* tyto vzory se objeví, ale vzácně. Jejich pravděpodobnost roste s druhou mocninou "
        "hafniánu, jejich příspěvek k momentu jen s první, takže vzácné vzory nesou nepoměrně velkou část momentu. "
        f"Nesoulad vyskočí (při ρ = 0,02 je $m$ = {czech_decimal(weak.pattern_mismatch, 0)}) a s klesající korelací "
        f"se nevrací: i při ρ = 0,0001 je kolem {czech_decimal(SINGULAR_MISMATCH, 0)}. Nezávislá aktiva jsou "
        "tedy výjimečný bod, ne nejlepší případ.\n"
        "3. *Silný tržní mód:* přístroj se chová skoro jako jeden stlačený mód a u rovnoměrného portfolia ukazuje "
        "vzory přesně v poměru jejich příspěvků ($m \\to 1$). Úsporu pak omezuje jen zahazování: přesně 4 fotony "
        f"má jen {percent(strong.useful_shot_share)} výstřelů, odtud strop {saving_label(strong.sample_saving)} "
        f"(u 6. stupně {percent(strong_sixth.useful_shot_share)} a {saving_label(strong_sixth.sample_saving)}).\n"
        "4. *Long–short:* jeho rozptyl tvoří jen slabě stlačené šumové módy, ale jednotlivé členy rozvoje momentu "
        "nesou hlavně tržní mód a se střídavými znaménky se skoro vyruší. Při ρ = 0,25 je součet jejich absolutních "
        f"hodnot {czech_decimal(hedged.cancellation, 0)}× větší než výsledek, při ρ = 0,5 už "
        f"{czech_decimal(hedged_strong.cancellation, 0)}×. GBS-P odhaduje každý člen s relativní chybou, takže "
        "chyba součtu je vůči malému výsledku obrovská. Znaménka členů přitom známe (dávají je váhy), nejde tedy "
        "o znaménkový problém z háčků, ale o jeho příbuzného: vzájemné rušení.\n\n"
        "**Co z toho plyne pro hypotézu (náš odhad).** O výhodě nerozhoduje jen spektrum, ale i poloha vah vůči "
        "hlavním vlastním vektorům – a obojí jde spočítat předem, bez spuštění přístroje. Skutečné akcie mají "
        "výrazný tržní mód, takže portfolia zajištěná proti trhu (long–short, tržně neutrální) by při tomto "
        "zakódování byla pro GBS-P nejhorší případ.\n"
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
**Co víme.** Andersen a Shan zavádějí dva odhady z výstřelů GBS, GBS-P a GBS-I. Pro GBS-I dokazují, že existují
úlohy, kde potřebuje exponenciálně méně vzorků než klasické Monte Carlo; výhoda ale neplatí pro všechny úlohy.
V navazujícím článku odhadují, pro jaký podíl náhodných úloh má GBS-I výhodu, a ten závisí na rozměru a stupni
úlohy. Na 2. stránce i zde počítáme s odhadem GBS-P. GBS přitom matici zpracovává přes její rozklad na vlastní
čísla (síly stlačení) a vlastní vektory (interferometr).

**Co víme o maticích akcií.** Spektrum skutečné korelační matice má jedno velké vlastní číslo (tržní mód,
u Laloux a kol. asi 25× nad horní mezí šumu), několik sektorových a široký pás šumu podle Marčenka
a Pastura.

**Hypotéza (náš odhad).** O úspoře vzorků nerozhoduje „náhodná matice“ z článků o GBS, ale tvar spektra
a poloha vah portfolia vůči tržnímu módu. Teorie náhodných matic dává realistické rodiny spekter, na kterých
by šlo výhodu GBS měřit systematicky – místo náhodně vybraných matic.
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_ADVANTAGE, "pro jaký podíl úloh má GBS-I výhodu"),
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "odhady GBS-P a GBS-I a jejich rozptyly"),
        Reading(LALOUX_1999, "jak vypadá spektrum korelační matice akcií"),
    ),
)

FIRST_STUDY = TheoryTopic(
    anchor="vs-prvni-vypocet",
    title="První výpočet: šest aktiv, tržní mód a dvě portfolia",
    in_short=(
        "Šest aktiv se společnou korelací ρ a dvě portfolia: rovnoměrné leží ve směru tržního módu, long–short "
        "je na něj kolmé. Pro každé ρ najdeme nejlepší sílu stlačení a spočítáme, kolikrát méně vzorků GBS "
        "potřebuje než Monte Carlo pro stejnou relativní chybu."
    ),
    explanation=r"""
**Model.** Korelační matice se stejnou korelací ρ mezi všemi dvojicemi má jedno vlastní číslo $1 + 5\rho$
(tržní mód, vlastní vektor $(1, \dots, 1)$) a pět stejných vlastních čísel $1 - \rho$. Je to nejjednodušší
spektrum „tržní mód plus šum“. Rovnoměrné portfolio leží pro každé $\rho > 0$ přesně ve směru tržního módu,
portfolio long–short s vahami $(1, -1, 1, -1, 1, -1)/6$ je na něj kolmé.

**Co měříme.** Konstanty relativní chyby $c$ z 2. stránky: chyba po $N$ vzorcích je $c/\sqrt{N}$. Úspora
vzorků je $(c_{\text{MC}}/c_{\text{GBS}})^2$, u GBS pro nejlepší sílu stlačení na mřížce posuvníku 2. stránky
(0,1 až 0,95). Je to teoretická hodnota pro velké $N$, ne simulace.

**Omezení.** Jen šest módů (víc simulátor v aplikaci nezvládne), dvě portfolia a jeden typ spektra. Přístroj
programujeme přímo kovarianční maticí aktiv, stejně jako na 2. stránce; jiné zakódování (otočení souřadnic,
jiné ladění stlačení) by mohlo dopadnout jinak. Sektory ani pás šumu podle Marčenka a Pastura tu nejsou.
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "odhad GBS-P, ze kterého vychází konstanta chyby"),
    ),
    related_caveats=(CLOSED_FORM, DISCARDED_SHOTS, SIGN_PROBLEM),
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
        "Šest otázek, které by z hypotézy udělaly výsledek – a háčky, kvůli kterým může vyjít negativně. "
        "I negativní výsledek by šel publikovat."
    ),
    explanation=r"""
1. **Úhel vah a hlavních vlastních vektorů.** Spočítali jsme dva krajní případy. Dá se úspora předpovědět
   z úhlu mezi vahami a hlavními vlastními vektory a ze spektra – bez výpočtu hafniánů? Taková diagnostika by
   šla spočítat ještě před spuštěním přístroje.
2. **Volba zakódování.** Přístroj tu programujeme přímo kovarianční maticí aktiv. Pomůže otočit souřadnice nebo
   ladit stlačení po módech (jako na 3. stránce), aby fotony šly tam, kde leží moment?
3. **Realistická spektra.** Spektrum „tržní mód + sektory + pás Marčenka a Pastura“ pro desítky aktiv. To je
   mimo dosah simulátoru v aplikaci (6 módů) a vyžaduje rychlejší klasickou simulaci GBS.
4. **Surová vs. vyčištěná matice.** Mění čištění spektrum tak, že se výhoda GBS zvětší, nebo zmenší?
5. **Úlohy bez vzorce.** Momenty portfolia mají uzavřený vzorec, takže GBS tu slouží jen jako test. Smysl
   mají úlohy bez vzorce, např. monomy z 3. stránky nebo nelineární payoffy – na spektrech z teorie
   náhodných matic.
6. **Hranice klasické simulace.** Kde je GBS s takovou maticí ještě klasicky simulovatelný? Bulmer a kol.
   a Quesada a kol. tuto hranici posunuli; výhoda ve vzorcích se musí porovnat s cenou simulace.

**Jak by vypadal výsledek.** Mapa „spektrum × váhy → úspora vzorků“, ze které je vidět, pro jaké portfolio
a trh má smysl GBS vůbec zkoušet. Pokud by mapa ukázala, že realistická spektra výhodu nemají, je to také
užitečný (negativní) výsledek.
""",
    further_reading=(
        Reading(BULMER_BOUNDARY, "hranice kvantové výhody GBS"),
        Reading(QUESADA_SPEEDUP, "rychlejší klasická simulace GBS"),
        Reading(ANDERSEN_SHAN_ADVANTAGE, "pro jaký podíl úloh má GBS-I výhodu"),
    ),
    related_caveats=(CLASSICAL_SIMULATION,),
)

TOPICS: Tuple[TheoryTopic, ...] = (HYPOTHESIS, FIRST_STUDY, NOISY_INPUT, OPEN_QUESTIONS)
