"""Texts of the photonic chip simulator: how a mesh of Mach–Zehnder interferometers is programmed and calibrated."""

from __future__ import annotations

from typing import Dict, Tuple

from gbs.chip_programming import ChipTarget
from ui.chip_sampling_content import SAMPLING_TOPIC
from ui.theory_content import AARONSON_ARKHIPOV, CLEMENTS, RECK, Reading, Source, TheoryTopic

SOURCES_ANCHOR = "cip-zdroje"
LAB_ANCHOR = "cip-laborator"

TITLE = "Simulátor fotonického čipu"
LEAD = (
    "Programovatelný fotonický čip se čtyřmi světlovody, šesti Machovými–Zehnderovými interferometry a laserem. "
    "Vyber, co má čip se světlem udělat, nech simulátor spočítat fáze a sleduj, kudy světlo teče. Na čipu "
    "s výrobními chybami uvidíš, proč se skutečné čipy musí kalibrovat. Ve druhé laboratoři pošleš jednotlivé "
    "fotony čipem až se 16 světlovody a z jejich výstřelů odhadneš modifikovaným Monte Carlem součet permanentů."
)
IN_SHORT = r"""
Lineární optický čip je unitární matice $U$: ze světla, které vstoupí do vstupu $j$, dorazí na výstup $i$ podíl
$|U_{ij}|^2$, a jediný foton tam dorazí se stejnou pravděpodobností. Síť $N(N-1)/2$ Machových–Zehnderových
interferometrů (MZI) v Clementsově uspořádání složí **libovolnou** unitární matici $N \times N$. „Naprogramovat čip“
znamená spočítat pro každý MZI dvě fáze $\theta$ a $\varphi$, a to simulátor dělá přesně Clementsovým rozkladem.
Na skutečném čipu ale děliče nedělí přesně 50:50, takže stejné fáze dají trochu jiné světlo a fáze se musí doladit
na každém kusu zvlášť.
"""

LAB_INTRO = r"""
Čip má 4 světlovody (vstupy vlevo, detektory vpravo) a 6 MZI ve čtyřech sloupcích. Každý MZI má dva fázové
posouvače: $\varphi$ (oranžový, na horním vstupu) a $\theta$ (fialový, mezi oběma děliči). Laser svítí do zvoleného
vstupu. Čím víc světla světlovodem teče, tím jasněji září, a čísla vpravo ukazují, kolik ho dopadne na každý
detektor. Po najetí myší na MZI se ukáže, kolik světla posílá do sousedního světlovodu.

1. Vyber **cíl**, tedy matici, kterou má čip provést: *průchod* (každý vstup na svůj výstup), *obrácení pořadí*
   (vstup 1 na výstup 4, 2 na 3, …), *dva děliče 50:50* (na světlovodech 1–2 a 3–4), *rovnoměrně rozdělit*
   (Fourierova matice) nebo *náhodnou unitární matici* podle seedu. Tabulka *Cíl* ukazuje $|V_{ij}|^2$: kolik
   světla ze vstupu (sloupec) má dojít na výstup (řádek).
2. Na začátku jsou všechny fáze nulové a čip obrací pořadí světlovodů (vstup 1 jde na výstup 4). S cílem
   *rovnoměrně rozdělit* je proto shoda jen 25 %.
3. **Naprogramovat podle návrhu** spočítá fáze Clementsovým rozkladem cíle. Na ideálním čipu je shoda 100 %.
4. Přepni na **vyrobený čip** a zkus totéž: návrhové fáze už nestačí. **Doladit na tomto čipu** je upraví podle
   chyb děličů tohoto kusu.
5. Fáze jde měnit i ručně posuvníky pod čipem a sledovat, jak se světlo přelévá.

Simulátor vznikl podle [Virtual Chip Simulator](https://sim.q-memory.tech/) firmy Q-Memory; tady je navíc výpočet
a pod čipem výklad, proč to funguje.
"""

TARGET_LABELS: Dict[ChipTarget, str] = {
    ChipTarget.PASS_THROUGH: "Průchod",
    ChipTarget.REVERSE: "Obrácení pořadí",
    ChipTarget.TWO_SPLITTERS: "Dva děliče 50:50",
    ChipTarget.SPREAD_EVENLY: "Rovnoměrně rozdělit",
    ChipTarget.RANDOM: "Náhodná unitární matice",
}
DEFAULT_TARGET = ChipTarget.SPREAD_EVENLY

CHIP_OPTIONS: Tuple[Tuple[str, float], ...] = (
    ("Ideální (děliče 50:50)", 0.0),
    ("Vyrobený, děliče 50 ± 3 %", 0.03),
    ("Vyrobený, děliče 50 ± 8 %", 0.08),
)
"""Label and the standard deviation of the share of light each coupler sends across."""
CHIP_SEEDS = (1, 2, 3, 4, 5)
SEED_HINT = "Určuje náhodnou cílovou matici i výrobní chyby čipu. Stejný seed dá vždy stejný kus i stejnou matici."
PHASES_HINT = (
    "θ určuje, jak MZI dělí světlo (0 = vše do sousedního světlovodu, π/2 = půl na půl, π = rovně), φ posouvá fázi "
    "horního vstupu. Obě jsou v radiánech."
)
MATCH_HINT = (
    "Podíl světla, které dopadne tam, kam podle cíle má, průměrovaný přes všechny čtyři vstupy (1 minus totální "
    "variační vzdálenost)."
)
DEVIATION_HINT = "Největší rozdíl jednoho prvku mapy přenosu |U_ij|² od cíle, v procentních bodech."
MATRIX_HINT = (
    "Sloupec = vstup, řádek = výstup. Číslo je podíl světla ze vstupu, který dojde na výstup; pro jediný foton je to "
    "pravděpodobnost. Sloupec vstupu, do kterého svítí laser, je zvýrazněný."
)

CAROLAN_2015 = Source(
    "Carolan, J. a kol.: *Universal linear optics*. Science 349, 711–716 (2015), "
    "[doi:10.1126/science.aab3642](https://doi.org/10.1126/science.aab3642)"
)
MILLER_2015 = Source(
    "Miller, D. A. B.: *Perfect optics with imperfect components*. Optica 2, 747 (2015), "
    "[doi:10.1364/OPTICA.2.000747](https://doi.org/10.1364/OPTICA.2.000747)"
)
MOWER_2015 = Source(
    "Mower, J., Harris, N. C., Steinbrecher, G. R., Lahini, Y., Englund, D.: *High-fidelity quantum state evolution "
    "in imperfect photonic integrated circuits*. Physical Review A 92, 032322 (2015), "
    "[doi:10.1103/PhysRevA.92.032322](https://doi.org/10.1103/PhysRevA.92.032322)"
)
HARRIS_2018 = Source(
    "Harris, N. C. a kol.: *Linear programmable nanophotonic processors*. Optica 5, 1623 (2018), "
    "[doi:10.1364/OPTICA.5.001623](https://doi.org/10.1364/OPTICA.5.001623)"
)
BOGAERTS_2020 = Source(
    "Bogaerts, W. a kol.: *Programmable photonic circuits*. Nature 586, 207–216 (2020), "
    "[doi:10.1038/s41586-020-2764-0](https://doi.org/10.1038/s41586-020-2764-0)"
)
PRIMER_TRANSLATION = Source(
    "Kolarovszki, Z., Zimborás, Z.: *Primer on photonic quantum computing, Gaussian Boson Sampling and its "
    "applications*. Skripta pro workshop v IT4Innovations, Ostrava 2025; český překlad je v této aplikaci, "
    "oddíly 1.2–1.5 v [1. části skript](/fotonika/zaklady)",
    czech=True,
)

MZI = TheoryTopic(
    anchor="cip-mzi",
    title="Světlovod, dělič a Machův–Zehnderův interferometr",
    in_short=(
        r"MZI tvoří dva děliče 50:50 a mezi nimi fázový posouvač $\theta$. Podle $\theta$ pošle světlo rovně "
        r"($\theta = \pi$), křížem do sousedního světlovodu ($\theta = 0$) nebo cokoli mezi tím. Druhý posouvač "
        r"$\varphi$ nastaví fázi mezi oběma vstupy."
    ),
    explanation=r"""
Na fotonickém čipu světlo vedou **světlovody** (waveguides): tenké proužky křemíku nebo nitridu křemíku, ve kterých
se světlo drží podobně jako v optickém vlákně. Jeden světlovod je jeden **mód** ve smyslu
[skript, oddíl 1.2](/fotonika/zaklady#skripta-1-2).

**Směrový vazební člen** (directional coupler) přiblíží dva světlovody těsně k sobě a světlo pak postupně přetéká
z jednoho do druhého. Délka a vzdálenost přiblížení určí, jaká část přeteče. Dělič 50:50 má matici

$$
B = \frac{1}{\sqrt 2}\begin{pmatrix} 1 & i \\ i & 1 \end{pmatrix},
$$

kde $i$ říká, že přeteklé světlo je o čtvrt vlny posunuté. **Fázový posouvač** je kus světlovodu, ve kterém se
změní index lomu, nejčastěji ohřátím malým topným tělískem. Světlo jím projde o trochu pomaleji a jeho fáze se
posune o úhel $x$: $P(x) = \operatorname{diag}(e^{ix}, 1)$.

MZI je za sebou posouvač $\varphi$, dělič, posouvač $\theta$ a druhý dělič:

$$
T(\theta, \varphi) = B\,P(\theta)\,B\,P(\varphi)
= i e^{i\theta/2}
\begin{pmatrix}
e^{i\varphi}\sin\frac{\theta}{2} & \cos\frac{\theta}{2} \\
e^{i\varphi}\cos\frac{\theta}{2} & -\sin\frac{\theta}{2}
\end{pmatrix}.
$$

Ze světla v horním vstupu tedy zůstane v horním světlovodu podíl $\sin^2(\theta/2)$ a do dolního přejde
$\cos^2(\theta/2)$:

- $\theta = 0$: **křížový stav**, všechno světlo přejde do sousedního světlovodu, protože se tam obě poloviny
  na druhém děliči sejdou ve fázi;
- $\theta = \pi/2$: MZI dělí 50:50;
- $\theta = \pi$: **rovný stav**, světlo jde rovně.

MZI je tedy dělič s *nastavitelným* dělicím poměrem: v zápisu skript (1.31) odpovídá děliči s úhlem
$(\pi - \theta)/2$, až na fáze. Fáze $\varphi$ dělicí poměr nemění. Rozhoduje o tom, jak se složí světlo
z obou vstupů, když svítí oba, a uvnitř sítě MZI svítí skoro vždy oba.
""",
    further_reading=(
        Reading(PRIMER_TRANSLATION, "děliče svazku a fázové posouvače jako kvantová hradla, oddíl 1.2"),
        Reading(BOGAERTS_2020, "přehled programovatelných fotonických obvodů: součástky, uspořádání, použití"),
        Reading(HARRIS_2018, "přehled křemíkových čipů z MZI pro klasické i kvantové úlohy"),
    ),
)

MESH = TheoryTopic(
    anchor="cip-sit",
    title="Síť interferometrů složí libovolnou matici",
    in_short=(
        r"Reck a kol. (1994) ukázali, že $N(N-1)/2$ děličů s fázemi v trojúhelníku složí libovolnou unitární matici "
        r"$N \times N$. Clements a kol. (2016) je přeskládali do obdélníku se stejným počtem MZI a poloviční optickou "
        r"hloubkou. Náš čip je Clementsova síť pro $N = 4$: 6 MZI ve 4 sloupcích."
    ),
    explanation=r"""
**Proč zrovna $N(N-1)/2$.** Unitární matice $N \times N$ má $N^2$ reálných parametrů. Každý MZI přidá dva
($\theta$ a $\varphi$), dohromady tedy $N(N-1)$. Zbylých $N$ parametrů jsou fáze na jednotlivých výstupech (jedna
z nich je jen celková fáze). Detektor, který počítá světlo nebo fotony, je nevidí, proto je náš čip vůbec nemá.
Pro $N = 4$ to dělá 6 MZI a 12 fází.

**Jak je síť poskládaná.** V prvním sloupci jsou MZI na dvojicích světlovodů 1–2 a 3–4, ve druhém na 2–3 a tak se to
střídá jako cihly ve zdi, celkem $N$ sloupců. Reck a kol. (1994) navrhli síť ve tvaru trojúhelníku se stejným počtem
děličů. Clements a kol. (2016) ukázali, že obdélník potřebuje poloviční optickou hloubku (počet MZI, kterými světlo
projde za sebou) a je výrazně odolnější vůči ztrátám světla. Obrázek 1.1 ve
[skriptech, oddíl 1.3.2](/fotonika/zaklady#skripta-1-3) ukazuje stejnou síť pro 6 módů.

**Skutečné čipy.** Programovatelné sítě MZI se dnes vyrábějí na křemíkových i nitridových čipech. Čip se šesti
světlovody a 15 MZI z Bristolu (Carolan a kol. 2015) šlo přeprogramovat na řadu dřívějších experimentů lineární
optiky, mimo jiné na Boson Sampling. Jak takové čipy zapadají do fotonického kvantového počítače, popisuje
[kapitola o hardwaru ve Waltherově přednášce](/fotonika/prednaska-walther-2022#walther-hardware).
""",
    further_reading=(
        Reading(RECK, "první důkaz, že děliče a fáze složí libovolnou unitární matici (trojúhelníková síť)"),
        Reading(CLEMENTS, "obdélníková síť, kterou používá simulátor, a algoritmus rozkladu"),
        Reading(CAROLAN_2015, "šestimódový čip, který jde přeprogramovat na libovolnou lineární optiku"),
    ),
)

PROGRAMMING = TheoryTopic(
    anchor="cip-programovani",
    title="Naprogramovat čip znamená rozložit matici",
    in_short=(
        r"Clementsův rozklad nuluje prvky cílové matice jeden po druhém. Každé vynulování je jeden MZI a jeho "
        r"$\theta$ a $\varphi$ jdou spočítat ze dvou čísel. Zbude diagonála fází, kterou detektor nevidí. Shoda "
        r"v simulátoru je podíl světla, které dopadne tam, kam má."
    ),
    explanation=r"""
**Rozklad.** Cílovou matici $V$ násobíme maticemi MZI střídavě zprava a zleva tak, aby každý MZI vynuloval jeden
prvek pod vedlejší diagonálou. MZI na sloupcích $m$ a $m + 1$ násobený zprava míchá jen tyto dva sloupce. Nula
v řádku $r$ vznikne, když

$$
e^{-i\varphi}\, V_{r,m} \sin\frac{\theta}{2} = -V_{r,m+1} \cos\frac{\theta}{2},
$$

tedy pro $\tan(\theta/2) = |V_{r,m+1}| / |V_{r,m}|$ a $\varphi$ z rozdílu fází obou prvků. Jde o Givensovu rotaci,
stejný trik, jakým numerická lineární algebra počítá QR rozklad. Násobení zleva funguje stejně s řádky. Po
$N(N-1)/2$ krocích zbude diagonální matice fází $D$. MZI násobené zleva se pak „protlačí“ přes $D$ doprava,
změní se jim přitom jen $\varphi$. Výsledek je

$$
V = D \cdot T_6 \cdots T_2 T_1 ,
$$

kde $T_1, \dots, T_6$ jsou MZI v pořadí, v jakém jimi světlo prochází. Matice $D$ jsou fáze na výstupech; detektor
měří jen $|{\cdot}|^2$, proto se na čipu nenastavují. Postup je podrobně v článku Clementse a kol. a stručně
ve [skriptech, oddíl 1.3.2](/fotonika/zaklady#skripta-1-3).

**Rozklad není jednoznačný.** U *průchodu* nedá všechny MZI rovně: MZI 1 a 4 nechá v křížovém stavu, takže světlo
mezi světlovody 1 a 2 přejde dvakrát křížem a vrátí se zpět. I to je průchod.

**Shoda.** Pro každý vstup $j$ simulátor spočte, kolik světla dopadne jinam, než říká cíl: polovinu součtu
$\sum_i \bigl| |U_{ij}|^2 - |V_{ij}|^2 \bigr|$, tzv. totální variační vzdálenost dvou rozdělení. Shoda je 1 minus
průměr přes vstupy:

$$
\text{shoda} = 1 - \frac{1}{N}\sum_{j=1}^{N} \frac{1}{2}\sum_{i=1}^{N} \Bigl| |U_{ij}|^2 - |V_{ij}|^2 \Bigr| .
$$

Shoda 25 % u nulových fází a cíle *rovnoměrně rozdělit* tedy znamená, že tři čtvrtiny světla dopadnou jinam, než
mají.
""",
    further_reading=(
        Reading(CLEMENTS, "algoritmus rozkladu krok za krokem, včetně přesunu MZI přes diagonálu fází"),
        Reading(PRIMER_TRANSLATION, "Clementsův rozklad, oddíl 1.3.2"),
    ),
)

PHOTONS = TheoryTopic(
    anchor="cip-fotony",
    title="Laser, jeden foton a více fotonů",
    in_short=(
        r"Pro laser i pro jediný foton platí totéž: na výstup $i$ dorazí podíl $|U_{ij}|^2$. Dva a více fotonů už "
        r"rozliší i matice se stejnými $|U_{ij}|^2$, protože o výsledku rozhoduje permanent a v něm fáze. Kvantový "
        r"experiment proto potřebuje trefit celou matici, ne jen mapu přenosu."
    ),
    explanation=r"""
Simulátor svítí laserem, tedy klasickým světlem. Intenzita na výstupu $i$ je $|U_{ij}|^2$ krát intenzita na vstupu
$j$. Jediný foton se chová stejně: podle vztahu (1.46) ve [skriptech](/fotonika/zaklady#skripta-1-3) se stav
$|e_j\rangle$ změní na $\sum_i U_{ij} |e_i\rangle$ a detektor $i$ foton zachytí s pravděpodobností $|U_{ij}|^2$.
Mapa přenosu v simulátoru je tedy zároveň tabulka pravděpodobností pro jeden foton.

Se dvěma fotony je to jinak. Fotony ve vstupech $j$ a $k$ dorazí na dva různé výstupy $i$ a $l$
s pravděpodobností

$$
\bigl| U_{ij} U_{lk} + U_{ik} U_{lj} \bigr|^2 ,
$$

což je druhá mocnina absolutní hodnoty permanentu podmatice 2 × 2 (viz
[skripta, oddíl 1.5](/fotonika/zaklady#skripta-1-5) a [hafnián a permanent](/gbs/hafnian)). Obě cesty fotonů se sčítají jako
amplitudy, takže na fázích záleží.

**Příklad.** Náš cíl *rovnoměrně rozdělit* je Fourierova matice $F_{jk} = \omega^{(j-1)(k-1)}/2$
s $\omega = e^{2\pi i/4}$. Hadamardova matice

$$
H = \frac{1}{2}\begin{pmatrix} 1 & 1 & 1 & 1 \\ 1 & -1 & 1 & -1 \\ 1 & 1 & -1 & -1 \\ 1 & -1 & -1 & 1 \end{pmatrix}
$$

má stejně jako $F$ všechna $|U_{ij}|^2 = 1/4$, takže ji laser od $F$ nerozliší a shoda je 100 %. Pošleme-li ale
jeden foton do vstupu 1 a druhý do vstupu 2, Fourierova matice je pošle na výstupy 1 a 2 s pravděpodobností
12,5 %, Hadamardova nikdy. Clementsův rozklad dává celou matici přesně (až na fáze na výstupech, které nevidí ani
fotony). Dolaďování v simulátoru ale hlídá jen $|U_{ij}|^2$, a proto u kvantového experimentu nestačí.
""",
    further_reading=(
        Reading(PRIMER_TRANSLATION, "permanent a Boson Sampling, oddíly 1.3.1 a 1.5"),
        Reading(AARONSON_ARKHIPOV, "proč je vzorkování z permanentů klasicky těžké"),
    ),
)

FABRICATION = TheoryTopic(
    anchor="cip-vyrobni-chyby",
    title="Skutečný čip: výrobní chyby a kalibrace",
    in_short=(
        "Vazební členy se nevyrobí přesně 50:50. MZI pak nedokáže světlo úplně přepnout, Clementsovy fáze přestanou "
        "sedět a shoda klesne. Fáze se proto ladí na každém kusu zvlášť, ale některé cíle nejdou spravit ani tak."
    ),
    explanation=r"""
Dělicí poměr vazebního členu závisí na délce a vzdálenosti přiblížených světlovodů a ty se při výrobě liší
o nanometry. Vyrobený čip v simulátoru má každý ze 12 děličů náhodně posunutý: posílá na druhou stranu
$50 \pm 3$ % nebo $50 \pm 8$ % světla (směrodatná odchylka). Seed určí konkrétní kus.

S nepřesnými děliči $B(\alpha_1)$ a $B(\alpha_2)$, které posílají na druhou stranu podíl $\sin^2\alpha$, už MZI
nemá plný rozsah. Podíl světla, který zůstane v horním světlovodu, jde měnit jen mezi $\cos^2(\alpha_1 + \alpha_2)$
a $\cos^2(\alpha_1 - \alpha_2)$. Dokonalý křížový stav existuje jen pro $\alpha_1 + \alpha_2 = \pi/2$. Když oba
děliče posílají na druhou stranu 53 % místo 50 %, zůstane v křížovém stavu
$(1 - 2 \cdot 0{,}53)^2 = 0{,}36$ % světla tam, kde být nemá.

**Kalibrace.** Na skutečném čipu se nejdřív změří, jak se chovají děliče a posouvače (charakterizace čipu), a fáze
se pak dopočítají pro konkrétní kus. Simulátor chyby zná, takže *Doladit na tomto čipu* rovnou upraví návrhové fáze.
Bere jednu fázi po druhé a posune ji tam, kde je součet čtverců odchylek $|U_{ij}|^2$ od cíle nejmenší. V každé
jednotlivé fázi je ta chyba trigonometrický polynom 2. stupně, takže pět vzorků určí celý její průběh a minimum jde
odečíst přesně. Takové ladění po souřadnicích je jednoduché a na malý čip stačí; v laboratořích se používají
i důmyslnější postupy.

**Ne všechno jde spravit.** *Obrácení* potřebuje všech šest MZI v dokonalém křížovém stavu, a ten s nepřesnými
děliči neexistuje, takže ladění skoro nic nezlepší. *Průchod* jde spravit líp: rovný stav propouští do sousedního
světlovodu jen $\sin^2(\alpha_1 - \alpha_2)$, takže se chyby obou děličů zčásti vyruší, a navíc vede k cíli víc
cest. Síť s nepřesnými děliči obecně přestává být univerzální: některé matice jsou mimo její dosah. Jak nepřesné
děliče zhoršují věrnost kvantových obvodů a jak to napravit volbou fází, rozebírají Mower a kol. (2015). Jak i
z nepřesných součástek složit obvod, který dělá přesně, co má, ukazuje Miller (2015).
""",
    further_reading=(
        Reading(MOWER_2015, "jak nepřesné děliče snižují věrnost sítě MZI a jak ji zlepšit"),
        Reading(MILLER_2015, "přesná optika z nepřesných součástek"),
    ),
)

TOPICS: Tuple[TheoryTopic, ...] = (MZI, MESH, PROGRAMMING, PHOTONS, FABRICATION, SAMPLING_TOPIC)
