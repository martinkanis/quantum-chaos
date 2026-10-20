"""Hafnian and permanent explained for a beginner: pairings versus assignments, with data structures and finance."""

from __future__ import annotations

from typing import Tuple

from montecarlo.historical_returns import AssetClass
from ui.theory_content import (
    AARONSON_ARKHIPOV,
    BJORKLUND_GUPT_QUESADA,
    DAMODARAN_RETURNS,
    HAMILTON,
    ISSERLIS,
    VALIANT,
    WICK,
    WIKIPEDIA_HAFNIAN,
    KeyFinding,
    Reading,
    Source,
    TheoryTopic,
)

TITLE = "Hafnián a permanent polopatě"
SOURCES_ANCHOR = "hafnian-zdroje"
INTRO = (
    "Dvě maticové funkce, na kterých stojí celé Monte Carlo na GBS: hafnián sčítá přes všechna rozdělení jedné "
    "skupiny do dvojic, permanent přes všechna přiřazení jedné skupiny druhé. Vysvětlení na spolubydlících a bytech, "
    "v datových strukturách a v kódu, na trzích s byty a nakonec na skutečných datech."
)

ROOMMATES = ("Adam", "Bára", "Cyril", "Dana")
COMPATIBILITY = ((0, 3, 1, 2), (3, 0, 1, 4), (1, 1, 0, 2), (2, 4, 2, 0))
"""How well two roommates get on; symmetric, the diagonal is never used."""
ROOMMATES_HAFNIAN = 12

BUYERS = ("Anna", "Petr")
FLATS = ("byt 1", "byt 2")
FIT = ((3, 1), (2, 4))
"""FIT[buyer][flat]: how well a flat suits a buyer."""
BUYERS_PERMANENT = 14
BUYERS_DETERMINANT = 10

REGIONS = ("Praha", "Brno", "Ostrava", "Plzeň")
REGION_CORRELATIONS = (
    (1.0, 0.8, 0.5, 0.7),
    (0.8, 1.0, 0.6, 0.6),
    (0.5, 0.6, 1.0, 0.5),
    (0.7, 0.6, 0.5, 1.0),
)
"""Illustrative correlations of yearly flat price changes, not measured data."""
FOUR_REGIONS_MOMENT = "1{,}12"
PRAGUE_BRNO_MOMENT = "2{,}28"

DATA_ASSETS = (AssetClass.STOCKS, AssetClass.BONDS, AssetClass.REAL_ESTATE, AssetClass.GOLD)
DATA_ASSET_LABELS = {
    AssetClass.STOCKS: "akcie",
    AssetClass.BONDS: "státní dluhopisy",
    AssetClass.REAL_ESTATE: "nemovitosti",
    AssetClass.GOLD: "zlato",
}

PERMANENT_CODE = '''from itertools import permutations
from math import prod


def permanent(fit):
    # fit[kupec][byt]; přiřazení = permutace: přiřazení[i] je byt i-tého kupce
    kupci = range(len(fit))
    return sum(
        prod(fit[kupec][byt] for kupec, byt in zip(kupci, prirazeni))
        for prirazeni in permutations(kupci)
    )
'''

HAFNIAN_CODE = '''from math import prod


def dvojice(lide):
    # všechna rozdělení seznamu sudé délky do dvojic
    if not lide:
        yield []
        return
    prvni, zbytek = lide[0], lide[1:]
    for i, partner in enumerate(zbytek):
        ostatni = zbytek[:i] + zbytek[i + 1:]
        for rozdeleni in dvojice(ostatni):
            yield [(prvni, partner)] + rozdeleni


def hafnian(sedi):
    # sedi[a][b] == sedi[b][a]: jak spolu sedí dvojice a, b
    lide = list(range(len(sedi)))
    return sum(prod(sedi[a][b] for a, b in rozdeleni) for rozdeleni in dvojice(lide))
'''

WIKIPEDIA_PERMANENT = Source(
    "Wikipedia: [Permanent (mathematics)](https://en.wikipedia.org/wiki/Permanent_(mathematics)) – definice, "
    "vlastnosti a vztah k párování v bipartitních grafech"
)
WIKIPEDIA_PERFECT_MATCHING = Source(
    "Wikipedia: [Perfect matching](https://en.wikipedia.org/wiki/Perfect_matching) – perfektní párování v grafu"
)
WIKIPEDIA_BIPARTITE = Source(
    "Wikipedie: [Bipartitní graf](https://cs.wikipedia.org/wiki/Bipartitn%C3%AD_graf)", czech=True
)
WIKIPEDIA_DETERMINANT = Source("Wikipedie: [Determinant](https://cs.wikipedia.org/wiki/Determinant)", czech=True)

PAIRING_TOPIC = TheoryTopic(
    anchor="hafnian-dvojice",
    title="Hafnián: všechna rozdělení do dvojic",
    in_short=(
        "Máme sudý počet lidí a pro každou dvojici číslo, jak spolu sedí. Hafnián projde všechny způsoby, jak "
        "všechny rozdělit do dvojic, u každého vynásobí čísla zvolených dvojic a výsledky sečte."
    ),
    explanation=r"""
**Spolubydlící.** Adam, Bára, Cyril a Dana mají bydlet po dvou. Tabulka říká, jak spolu sedí každá dvojice
(čím víc, tím líp); je symetrická, protože „Adam s Bárou“ je totéž co „Bára s Adamem“, a diagonálu nepotřebujeme.

| | Adam | Bára | Cyril | Dana |
|:---|:---|:---|:---|:---|
| Adam | – | 3 | 1 | 2 |
| Bára | 3 | – | 1 | 4 |
| Cyril | 1 | 1 | – | 2 |
| Dana | 2 | 4 | 2 | – |

Rozdělit čtyři lidi do dvojic jde třemi způsoby:

- Adam–Bára a Cyril–Dana: $3 \cdot 2 = 6$,
- Adam–Cyril a Bára–Dana: $1 \cdot 4 = 4$,
- Adam–Dana a Bára–Cyril: $2 \cdot 1 = 2$.

Hafnián tabulky je součet: $6 + 4 + 2 = 12$. Násobí se proto, že rozdělení „funguje“, jen když fungují všechny
jeho dvojice najednou; sčítá se přes všechna rozdělení, protože nás zajímají všechny možnosti dohromady.

**Obecně.** Pro symetrickou matici $A$ velikosti $2n \times 2n$

$$
\mathrm{Haf}(A) = \sum_{\text{rozdělení do dvojic}}\ \prod_{(i,j)} a_{ij} ,
$$

pro $4 \times 4$ tedy $\mathrm{Haf}(A) = a_{12}a_{34} + a_{13}a_{24} + a_{14}a_{23}$. Rozdělení $2n$ lidí do dvojic
je $(2n-1)!! = 1 \cdot 3 \cdot 5 \cdots (2n-1)$: první si vybírá ze $2n - 1$ partnerů, další volný ze $2n - 3$
atd. Pro lichý počet žádné úplné rozdělení není a hafnián se bere jako nula.
""",
    further_reading=(
        Reading(WIKIPEDIA_HAFNIAN),
        Reading(WIKIPEDIA_PERFECT_MATCHING),
    ),
)

ASSIGNMENT_TOPIC = TheoryTopic(
    anchor="hafnian-permanent",
    title="Permanent: všechna přiřazení kupců k bytům",
    in_short=(
        "Teď máme dvě různé skupiny – kupce a byty – a každý kupec dostane jeden byt. Permanent projde všechna "
        "taková přiřazení, u každého vynásobí, jak byty kupcům sedí, a výsledky sečte. Je to determinant bez "
        "střídání znamének."
    ),
    explanation=r"""
**Kupci a byty.** Anna a Petr si rozdělí dva byty. Tabulka říká, jak který byt kterému kupci sedí; řádky jsou
kupci, sloupce byty – dvě různé skupiny, takže tabulka symetrická být nemusí.

| | byt 1 | byt 2 |
|:---|:---|:---|
| Anna | 3 | 1 |
| Petr | 2 | 4 |

Přiřazení jsou dvě: Anna → byt 1 a Petr → byt 2 dává $3 \cdot 4 = 12$, Anna → byt 2 a Petr → byt 1 dává
$1 \cdot 2 = 2$. Permanent je $12 + 2 = 14$.

**Obecně.** Pro matici $M$ velikosti $n \times n$

$$
\mathrm{Perm}(M) = \sum_{\sigma}\ \prod_{i=1}^{n} m_{i,\sigma(i)} ,
$$

kde $\sigma$ probíhá všech $n!$ permutací – $\sigma(i)$ je byt $i$-tého kupce.

**Příbuzný determinantu.** Determinant má stejné členy, jen polovinu z nich odečítá: $\det M = 12 - 2 = 10$.
Díky znaménkům se determinant spočítá Gaussovou eliminací zhruba za $n^3$ kroků; permanent žádnou takovou zkratku
nemá a jeho výpočet je #P-těžký (Valiant 1979) – stejně jako u hafniánu.
""",
    further_reading=(
        Reading(WIKIPEDIA_PERMANENT),
        Reading(WIKIPEDIA_DETERMINANT),
        Reading(VALIANT, "proč je permanent výpočetně těžký"),
    ),
)

DATA_STRUCTURES_TOPIC = TheoryTopic(
    anchor="hafnian-datove-struktury",
    title="Rozdíl v datových strukturách a v kódu",
    in_short=(
        "Permanent pracuje se dvěma seznamy a tabulkou řádky × sloupce, jedno řešení je permutace. Hafnián pracuje "
        "s jedním seznamem a symetrickou tabulkou každý s každým, jedno řešení je seznam dvojic. Permanent je "
        "zvláštní případ hafniánu, kde jsou dvojice uvnitř stejné skupiny zakázané."
    ),
    explanation=r"""
| | permanent | hafnián |
|:---|:---|:---|
| vstupní seznamy | dva: kupci a byty | jeden: lidé |
| tabulka | řádky × sloupce, nemusí být symetrická | každý s každým, symetrická |
| jako graf | bipartitní: hrany jen mezi skupinami | obecný: hrana mezi kýmkoli |
| jedno řešení | permutace, např. `[1, 0, 2]` | seznam dvojic, např. `[(0, 3), (1, 2)]` |
| počet řešení | $n!$ pro $n$ kupců | $(2n-1)!!$ pro $2n$ lidí |

**V Pythonu.** Permanent prochází permutace, hafnián rekurzivně tvoří dvojice (oba kódy níže jsou přímočaré a pro
velké matice beznadějně pomalé – k tomu kapitola 6).

**Permanent jako hafnián.** Dejte kupce i byty do jednoho seznamu a do tabulky „každý s každým“ napište nulu všude,
kde by se párovali kupec s kupcem nebo byt s bytem:

$$
\mathrm{Perm}(M) = \mathrm{Haf}\begin{pmatrix} 0 & M \\ M^\top & 0 \end{pmatrix} .
$$

Rozdělení, ve kterém je zakázaná dvojice, má součin nula, a zbydou přesně přiřazení kupců k bytům. Pro Annu, Petra
a dva byty vzniknou tři rozdělení čtyř „lidí“: Anna–Petr a byt 1–byt 2 dá nulu, zbylá dvě dají 12 a 2 – tedy
permanent 14. Pro čtyři kupce a čtyři byty má hafnián 105 rozdělení, z nichž nenulových je právě $4! = 24$.
Hafnián je tedy obecnější funkce.
""",
    further_reading=(
        Reading(WIKIPEDIA_BIPARTITE),
        Reading(WIKIPEDIA_PERMANENT),
    ),
)

MARKETS_TOPIC = TheoryTopic(
    anchor="hafnian-trhy-s-byty",
    title="Hafnián ve financích: společné výkyvy čtyř trhů s byty",
    in_short=(
        r"Pro normálně rozdělené veličiny je průměr součinu rovný hafniánu jejich kovarianční matice (Wickova "
        r"věta). Pro čtyři trhy s byty se společný pohyb všech čtyř rozloží na všechny způsoby, jak trhy spárovat; "
        r"v našem ilustračním příkladu vyjde 1,12."
    ),
    explanation=r"""
**Úloha.** Sledujeme roční změny cen bytů v Praze, Brně, Ostravě a Plzni, převedené na normované odchylky
$Z_i$ (průměr 0, rozptyl 1). Kovarianční matice normovaných veličin je jejich korelační matice. Čísla jsou
**ilustrační**, ne naměřená:

| | Praha | Brno | Ostrava | Plzeň |
|:---|:---|:---|:---|:---|
| Praha | 1 | 0,8 | 0,5 | 0,7 |
| Brno | 0,8 | 1 | 0,6 | 0,6 |
| Ostrava | 0,5 | 0,6 | 1 | 0,5 |
| Plzeň | 0,7 | 0,6 | 0,5 | 1 |

**Všechny čtyři trhy najednou.** $\mathbb{E}[Z_1 Z_2 Z_3 Z_4]$ je velké, když se všechny čtyři trhy často hýbou
stejným směrem. Podle Wickovy věty je to hafnián korelační matice – trhy se „spárují“ všemi třemi způsoby a korelace
dvojic se vynásobí:

$$
\begin{aligned}
& \mathbb{E}[Z_1 Z_2 Z_3 Z_4] \\
& = \rho_{12}\rho_{34} + \rho_{13}\rho_{24} + \rho_{14}\rho_{23} \\
& = 0{,}8 \cdot 0{,}5 + 0{,}5 \cdot 0{,}6 + 0{,}7 \cdot 0{,}6 \\
& = 1{,}12 .
\end{aligned}
$$

Kdyby trhy byly nezávislé, vyšla by nula. Proč dvojice: u normálního rozdělení je veškerá závislost dána
kovariancemi dvojic, takže i společný pohyb čtyř trhů se musí poskládat z párových vazeb.

**Současně velké výkyvy dvou trhů.** Opakované proměnné se v tabulce zopakují, takže
$\mathbb{E}[Z_1^2 Z_2^2]$ je hafnián matice $4 \times 4$ se dvěma řádky Prahy a dvěma Brna:

$$
\begin{aligned}
\mathbb{E}[Z_1^2 Z_2^2] &= 1 \cdot 1 + 2\,\rho_{12}^2 \\
&= 1 + 2 \cdot 0{,}64 = 2{,}28 .
\end{aligned}
$$

Pro nezávislé trhy by to bylo 1. Silná korelace tedy víc než zdvojnásobí průměr součinu čtverců – měřítko toho,
jak často jsou oba trhy daleko od průměru zároveň. A $\mathbb{E}[Z_1^4] = 3$: čtyři stejné činitele jde spárovat
třemi způsoby.

**Proč to potřebujeme.** Momenty výnosu portfolia $L = \sum_i w_i Z_i$, třeba $\mathbb{E}[L^4]$, se roznásobí na
součet přesně takových hafniánů. Pro čtyři trhy je to hračka; pro desítky aktiv a vysoké mocniny je hafniánů
astronomicky mnoho a jsou obrovské – proto se sahá po Monte Carlu, nebo po GBS.
""",
    further_reading=(
        Reading(ISSERLIS),
        Reading(WICK),
        Reading(WIKIPEDIA_HAFNIAN, "Isserlisova věta s příklady"),
    ),
)

PHOTONS_TOPIC = TheoryTopic(
    anchor="hafnian-fotony",
    title="Proč GBS dává hafnián a boson sampling permanent",
    in_short=(
        "Ve stlačeném světle vznikají fotony po dvojicích, a hledá se, které zachycené fotony tvořily pár – to je "
        "rozdělení do dvojic, tedy hafnián. Jednotlivé fotony mají každý svůj vstup a hledá se, který skončil kde – "
        "to je přiřazení, tedy permanent."
    ),
    explanation=r"""
**GBS.** Zdroje stlačeného světla vyrábějí fotony po párech, interferometr je promíchá a detektory spočítají, kolik
jich kam dopadlo. Kterýkoli dva zachycené fotony mohly být jedním párem – jako spolubydlící, kteří se mohou
spárovat každý s každým. Pravděpodobnost vzoru $S$ proto obsahuje hafnián matice $B$ se zopakovanými řádky:

$$
P(S) = \frac{\lvert\mathrm{Haf}(B_S)\rvert^2}{S!\,\prod_j \cosh r_j} .
$$

**Boson sampling.** Každý z $n$ fotonů má svůj vstupní kanál a skončí v některém detektoru – jako kupci, z nichž
každý dostane jeden byt. Sčítá se přes všechna přiřazení vstupů k detektorům, tedy permanent:
$P(S) = \lvert\mathrm{Perm}(U_{S,T})\rvert^2 / S!$.

**Co z toho plyne.** GBS hafnián nespočítá, ale losuje vzory přesně s pravděpodobností úměrnou jeho druhé mocnině.
Z jednoho vzoru se hafnián zjistit nedá; z četností mnoha výstřelů jde odhadnout *součet* hafniánů, tedy
střední hodnotu z předchozí kapitoly – na tom stojí Monte Carlo na GBS. Rozdíl obou variant hardwaru je rozebraný
na stránce o Quandele.
""",
    further_reading=(
        Reading(HAMILTON, "pravděpodobnosti GBS jsou hafniány"),
        Reading(AARONSON_ARKHIPOV, "pravděpodobnosti boson samplingu jsou permanenty"),
    ),
)

HARDNESS_TOPIC = TheoryTopic(
    anchor="hafnian-tezkost",
    title="Proč se hafnián nedá prostě spočítat",
    in_short=(
        "Počet rozdělení do dvojic roste jako (2n − 1)!!, rychleji než exponenciála. Chytré algoritmy to srazí na "
        "zhruba n³ · 2^(n/2) kroků pro matici n × n, pořád ale exponenciálně – a lepší postup se nečeká."
    ),
    explanation=r"""
**Hrubou silou.** Kód z kapitoly 3 projde všechna rozdělení. Tabulka níže ukazuje, kolik jich je – pro 40 lidí
(matice $40 \times 40$) by to při miliardě rozdělení za sekundu trvalo zhruba deset milionů let.

**Chytřeji, ale pořád exponenciálně.** Nejlepší známé algoritmy pro hafnián matice $n \times n$ potřebují řádově
$n^3\,2^{n/2}$ kroků (Björklund, Gupt a Quesada 2019), Ryserův vzorec pro permanent zhruba $n\,2^n$. To je obrovské
zlepšení oproti $(2n-1)!!$, ale pořád exponenciála. Valiant (1979) ukázal, že výpočet permanentu je #P-těžký,
a protože permanent je zvláštní případ hafniánu, platí totéž pro hafnián; polynomiální algoritmus se nečeká.

**Proč to nevadí v aplikaci.** Pro málo proměnných s vysokými mocninami počítá aplikace momenty Steinovou rekurzí,
která se rozdělením do dvojic vyhne. Těžké jsou matice s mnoha různými řádky – mnoho aktiv s malými mocninami.
""",
    further_reading=(
        Reading(BJORKLUND_GUPT_QUESADA, "nejrychlejší známý algoritmus pro hafnián"),
        Reading(VALIANT),
    ),
)

DATA_TOPIC = TheoryTopic(
    anchor="hafnian-data",
    title="Kontrola na datech: americké nemovitosti, akcie a zlato",
    in_short=(
        "Hafniánový vzorec platí přesně jen pro normálně rozdělená data. Roční výnosy z let 1928–2023 mají tlustší "
        "chvosty: zlato má čtvrtý moment skoro pětkrát větší, než normální rozdělení předpovídá, a společné "
        "výkyvy akcií a nemovitostí jsou výrazně silnější."
    ),
    explanation=r"""
**Co porovnáváme.** Normované roční výnosy akcií, státních dluhopisů, nemovitostí (ceny domů) a zlata v USA za
96 let (Damodaran). Pro každý moment je v tabulce níže hodnota, kterou dává hafnián korelační matice spočítané
z týchž dat – tedy co by platilo, kdyby výnosy byly normálně rozdělené –, a průměr přímo z dat.

**Co z toho plyne.** U akcií sedí čtvrtý moment s normálním rozdělením dobře, u dluhopisů a nemovitostí je vyšší
a u zlata mnohonásobně vyšší (prudké skoky ceny v 70. letech). Společné velké výkyvy akcií a nemovitostí jsou
v datech výrazně silnější, než předpovídá hafnián. Hafniánový vzorec – a s ním odhad z GBS, který na něm stojí –
by tedy u takových dat riziko společných propadů podcenil. Přesně to je téma stránky *Kdy odhad rizika přes GBS
selže*.

**Opatrně.** 96 ročních pozorování je na čtvrté momenty málo: jeden extrémní rok je výrazně posune. Čísla berte
jako ilustraci, ne jako přesný odhad.
""",
    further_reading=(
        Reading(DAMODARAN_RETURNS),
    ),
)

TOPICS: Tuple[TheoryTopic, ...] = (
    PAIRING_TOPIC,
    ASSIGNMENT_TOPIC,
    DATA_STRUCTURES_TOPIC,
    MARKETS_TOPIC,
    PHOTONS_TOPIC,
    HARDNESS_TOPIC,
    DATA_TOPIC,
)

KEY_FINDINGS: Tuple[KeyFinding, ...] = (
    KeyFinding(
        "**Hafnián = součet přes všechna rozdělení jedné skupiny do dvojic** (spolubydlící), u každého se násobí "
        "„jak spolu sedí“ zvolené dvojice.",
        PAIRING_TOPIC.anchor,
    ),
    KeyFinding(
        "**Permanent = součet přes všechna přiřazení jedné skupiny druhé** (kupci a byty); je to determinant bez "
        "znamének a zvláštní případ hafniánu.",
        ASSIGNMENT_TOPIC.anchor,
    ),
    KeyFinding(
        "**V datech:** permanent = dva seznamy a tabulka řádky × sloupce, hafnián = jeden seznam a symetrická "
        "tabulka každý s každým.",
        DATA_STRUCTURES_TOPIC.anchor,
    ),
    KeyFinding(
        "**Ve financích:** průměr součinu normálně rozdělených výnosů je hafnián jejich kovarianční matice "
        "(Wickova věta) – společný pohyb trhů se skládá z párových vazeb.",
        MARKETS_TOPIC.anchor,
    ),
    KeyFinding(
        "**V GBS** vznikají fotony po párech, proto hafnián; jednotlivé fotony v boson samplingu dávají permanent.",
        PHOTONS_TOPIC.anchor,
    ),
    KeyFinding(
        "**Na skutečných datech** mají výnosy tlustší chvosty, než hafnián gaussovského modelu předpovídá.",
        DATA_TOPIC.anchor,
    ),
)
