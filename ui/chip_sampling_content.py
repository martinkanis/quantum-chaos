"""Texts of the second lab of the chip simulator: boson sampling on the chip as a modified Monte Carlo."""

from __future__ import annotations

from typing import Dict, Tuple

from gbs.chip_boson_sampling import PhotonKind
from gbs.chip_programming import ChipTarget
from ui.advantage_content import ANGUITA_MONTE_CARLO_ACCELERATOR
from ui.theory_content import AARONSON_ARKHIPOV, ANDERSEN_SHAN_EXPECTATIONS, Reading, Source, TheoryTopic

SAMPLING_ANCHOR = "cip-boson-sampling-laborator"
SAMPLING_TITLE = "Laboratoř 2: boson sampling jako modifikované Monte Carlo"
SAMPLING_INTRO = r"""
Do prvních $n$ světlovodů vstoupí po jednom fotonu a detektory na konci spočítají, kolik fotonů dorazilo na který
výstup. To je jeden **výstřel** se vzorem $S = (s_1, s_2, \dots)$. Čip je naprogramovaný na zvolený interferometr $V$
Clementsovým rozkladem, větší čipy už ruční posuvníky nemají.

Z výstřelů odhadujeme modifikovaným Monte Carlem číslo

$$
\mu = \sum_S |\mathrm{Perm}(V_{S,T})|^2 = \mathrm{E}[S!],
$$

tedy průměr hodnot $Z(S) = S! = s_1!\,s_2!\cdots$. Výstřel, ve kterém žádné dva fotony nesdílejí detektor, má
$Z = 1$, dvojice v jednom detektoru dá $Z = 2$, trojice $Z = 6$. Číslo $\mu$ proto měří, jak moc se fotony shlukují.
Stejné $\mu$ umí klasický počítač odhadnout i bez fotonů, průměrem přes komplexní gaussovské vektory (výklad je
v poslední kapitole). Simulátor oba odhady porovná při stejném počtu vzorků.

1. Zvol počet světlovodů a fotonů. Se 16 světlovody a 6 fotony má čip 54 264 možných výstupních vzorů, se 7 fotony
   170 544.
2. **Spustit boson sampling** vystřelí zvolený počet výstřelů a spočítá oba odhady.
3. Přepni na **vyrobený čip** nebo na **rozlišitelné fotony**: odhad začne konvergovat jinam, než má. To je
   systematická chyba, kterou žádný počet výstřelů neodstraní.
"""

MODE_COUNT_OPTIONS = (4, 8, 12, 16)
DEFAULT_MODE_COUNT = 16
PHOTON_OPTIONS = (2, 3, 4, 5, 6, 7)
DEFAULT_PHOTONS = 6
SHOT_OPTIONS = (1_000, 10_000, 100_000)
DEFAULT_SHOTS = 10_000
SAMPLING_TARGET_LABELS: Dict[ChipTarget, str] = {
    ChipTarget.RANDOM: "Náhodný interferometr (Haar, podle seedu)",
    ChipTarget.SPREAD_EVENLY: "Fourierova matice",
}
PHOTON_KIND_LABELS: Dict[PhotonKind, str] = {
    PhotonKind.INDISTINGUISHABLE: "nerozlišitelné (ideální zdroj)",
    PhotonKind.DISTINGUISHABLE: "rozlišitelné (neinterferují)",
}
SAMPLING_CHIP_OPTIONS: Tuple[Tuple[str, float], ...] = (
    ("Ideální", 0.0),
    ("Vyrobený, děliče 50 ± 3 %", 0.03),
    ("Vyrobený, děliče 50 ± 8 %", 0.08),
)
SAMPLING_SEEDS = (1, 2, 3, 4, 5)
SAMPLING_SEED_HINT = "Určuje náhodný interferometr, výrobní chyby čipu i samotné výstřely."
TARGET_RELATIVE_ERROR = 0.01
"""The accuracy the readout converts the variance of one sample into a number of samples for."""

EXACT_HINT = (
    "Součet |Perm(V_ST)|² přes všechny vzory pro nerozlišitelné fotony a přesně naprogramovaný čip. Simulátor ho "
    "spočítá přímo, protože čip je malý; to je hodnota, kterou oba odhady mají trefit."
)
BOSON_HINT = "Průměr S! přes výstřely čipu ± jedna směrodatná chyba."
GAUSSIAN_HINT = (
    "Průměr přes stejný počet dvojic komplexních gaussovských vektorů ± jedna směrodatná chyba; žádný permanent "
    "se nepočítá."
)
BOSON_SHOTS_HINT = "Relativní rozptyl jednoho výstřelu (spočítaný přesně) děleno 0,01²."
GAUSSIAN_SHOTS_HINT = (
    "Relativní rozptyl odhadnutý z vylosovaných vzorků děleno 0,01². Chvosty jsou tak těžké, že i ten bývá podhodnocený."
)
LIMIT_HINT = (
    "Hodnota, ke které odhad z tohoto čipu konverguje: jeho skutečná matice a zvolené fotony. Rozdíl proti přesnému μ "
    "je systematická chyba."
)
CONVERGENCE_HINT = (
    "Průběžný odhad po prvních N vzorcích. Klasické Monte Carlo často vyskočí mimo graf: jeden vzorek s obří hodnotou "
    "posune celý průměr."
)
SHOT_VALUES_HINT = (
    "Jak často má výstřel hodnotu Z = S!: 1 znamená, že žádné dva fotony nedorazily do stejného detektoru, 2 jednu "
    "dvojici, 6 trojici. Rozlišitelné fotony se shlukují méně, a proto mají menší μ."
)
PHOTON_ANIMATION_HINT = (
    "Fotony vstoupí do prvních světlovodů a čipem projdou zpomaleně. Foton se na děliči nerozdělí na kousky: jas "
    "světlovodu a velikost tečky ukazují průměrný počet fotonů, tedy jak pravděpodobně by tam foton detektor našel. "
    "Kam fotony opravdu dorazí, rozhodne až detekce na konci, jeden výstřel."
)
FIRST_SHOTS_HINT = "Prvních pár výstřelů: výstupy, na kterých detektory zaznamenaly fotony (opakované číslo = víc fotonů)."

CLIFFORD_2018 = Source(
    "Clifford, P., Clifford, R.: *The classical complexity of boson sampling*. Proceedings of the 29th Annual "
    "ACM-SIAM Symposium on Discrete Algorithms (SODA 2018), 146–155, "
    "[doi:10.1137/1.9781611975031.10](https://doi.org/10.1137/1.9781611975031.10), "
    "[arXiv:1706.01260](https://arxiv.org/abs/1706.01260)"
)

SAMPLING_TOPIC = TheoryTopic(
    anchor="cip-boson-sampling",
    title="Boson sampling jako modifikované Monte Carlo",
    in_short=(
        r"Výstřel boson sampleru se vzorem $S$ má pravděpodobnost $|\mathrm{Perm}(U_{S,T})|^2/S!$. Průměr hodnot $S!$ "
        r"je proto nevychýlený odhad součtu $\mu = \sum_S |\mathrm{Perm}(U_{S,T})|^2$, který by klasicky vyžadoval "
        r"permanent pro každý vzor. Stejné $\mu$ jde zapsat jako střední hodnotu přes komplexní gaussovské vektory "
        r"a odhadnout obyčejným Monte Carlem, jen s mnohem větším rozptylem."
    ),
    explanation=r"""
**Odhad.** Boson sampler s jedním fotonem v každém ze vstupů $T = \{1, \dots, n\}$ vrací vzor $S$ s pravděpodobností

$$
P(S) = \frac{|\mathrm{Perm}(U_{S,T})|^2}{S!},
$$

kde $U_{S,T}$ má řádky výstupů (výstup $i$ zopakovaný $s_i$krát) a sloupce vstupů (viz vztah (1.57) ve
[skriptech, oddíl 1.5](/fotonika/zaklady#skripta-1-5)). Odhad typu GBS-I od Andersena a Shan, v aplikaci popsaný
u [Quandely](/reserse-gbs-financni-riziko/fotonicky-hardware#fotonika-nase-monte-carlo), přiřadí výstřelu hodnotu
$Z(S) = a_S\,S!$ a průměr odhaduje $\sum_S a_S |\mathrm{Perm}(U_{S,T})|^2$. Simulátor volí všechna $a_S = 1$:

$$
\mu = \sum_S |\mathrm{Perm}(U_{S,T})|^2 = \sum_S P(S)\, S! = \mathrm{E}[S!] .
$$

Relativní rozptyl jednoho výstřelu je $\mathrm{E}[S!^2]/\mu^2 - 1$. Pro relativní chybu $\varepsilon$ je potřeba
zhruba rozptyl děleno $\varepsilon^2$ výstřelů.

**Co $\mu$ znamená.** Kdyby žádné dva fotony nikdy neskončily ve stejném detektoru, bylo by $\mu = 1$. Bosony se ale
shlukují: že všech $n$ fotonů dorazí do jednoho výstupu, je u nerozlišitelných fotonů $n!$krát pravděpodobnější než
u rozlišitelných. Pro Fourierovu matici 4 × 4 a dva fotony vyjde $\mu = 1{,}5$, fotony tedy skončí spolu v polovině
výstřelů. Rozlišitelné fotony dají $\mu = 1{,}25$, spolu skončí jen ve čtvrtině. Proto $\mu$ citlivě reaguje na to,
jak dobře zdroj vyrábí nerozlišitelné fotony.

**Klasické Monte Carlo pro stejné $\mu$ (naše odvození).** Pro komplexní gaussovský vektor $z \sim \mathcal{CN}(0, I)$
a $w = U^\dagger z$ dává komplexní Wickova věta $\mathrm{E}[z^S \bar w^T] = \mathrm{Perm}(U_{S,T})$. Se dvěma
nezávislými kopiemi $z, z'$ je $|\mathrm{Perm}(U_{S,T})|^2$ střední hodnotou součinu a součet přes všechny vzory dá

$$
\mu = \mathrm{E}\Big[\, h_n(z \circ \bar z') \prod_{j \in T} \bar w_j\, w'_j \Big],
$$

kde $h_n$ je úplný homogenní symetrický polynom stupně $n$, tedy součet všech monomů stupně $n$. Obyčejné Monte Carlo
losuje gaussovské vektory a průměruje výraz v závorce, žádný permanent přitom nepočítá. Výraz je ale součinem mnoha
gaussovských veličin s velmi těžkými chvosty. V simulátoru vychází jeho relativní rozptyl o mnoho řádů větší než
u $S!$ a s počtem fotonů roste mnohem rychleji. Rovnost obou zápisů $\mu$ hlídají testy aplikace.

**Co to nedokazuje.** Pro pár fotonů je boson sampling klasicky snadný: algoritmus Clifforda a Clifforda vzorkuje
přesně stejné rozdělení za čas zhruba $n\,2^n$ na výstřel (plus polynom v počtu módů). Simulátor porovnává
s *naivním* klasickým Monte Carlem. Zda má modifikované Monte Carlo s permanenty výhodu i proti nejlepšímu
klasickému postupu, je otevřená otázka; Andersen a Shan obdobné výsledky pro boson sampling slibují v samostatné
práci. Boson sampling jako akcelerátor Monte Carla na čipu s 12 módy a třemi fotony předvedla skupina z Twente
([rešerše](/reserse-gbs-financni-riziko#reserse-twente)).

**Kdy odhad selže.** Výrobní chyby čipu změní matici $U$, výstřely pak mají jiné rozdělení a odhad konverguje
k jinému $\mu$. Rozlišitelné fotony neinterferují, $|\mathrm{Perm}(U_{S,T})|^2$ se nahradí
$\mathrm{Perm}(|U_{S,T}|^2)$ a $\mu$ se změní, v příkladech simulátoru klesne. V obou případech je chyba
systematická: víc výstřelů ji nezmenší, jen ji přesněji změří. Přesně taková selhání rozebírá stránka
[Kdy odhad rizika přes GBS selže](/vyzkumne-smery/kdy-gbs-selze).
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "obecný odhad GBS-I (Def. 3.3) a permanenty v příloze F"),
        Reading(ANGUITA_MONTE_CARLO_ACCELERATOR, "boson sampling jako akcelerátor Monte Carla na skutečném čipu"),
        Reading(CLIFFORD_2018, "přesné klasické vzorkování boson samplingu a jeho cena"),
        Reading(AARONSON_ARKHIPOV, "proč je boson sampling s mnoha fotony klasicky těžký"),
    ),
)
