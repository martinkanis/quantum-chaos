"""Texts of the page on three-photon GHZ states: what they are, how Greenberger, Horne and Zeilinger came to them,
how the Vienna group made them in 1999 and why they are the building block of the photonic blueprint.

Expands the fusion chapter of Walther's lecture (ui/walther_lecture_content.py); numbers in the text are checked
by tests/test_ghz_states_page.py.
"""

from __future__ import annotations

from ui.theory_content import KeyFinding, Reading, Source, TheoryTopic
from ui.walther_lecture_content import (
    BARTOLUCCI_FBQC,
    GIMENO_SEGOVIA_2015,
    KWIAT_1995,
    NOBEL_2022,
    PANT_PERCOLATION,
    RUDOLPH_2017,
    WALTHER_VIDEO,
)

TITLE = "GHZ stavy: od Greenbergera, Horna a Zeilingera k fotonickému počítači"
SOURCES_ANCHOR = "ghz-zdroje"
BLUEPRINT_SLIDES = ("slajd_2532.jpg", "slajd_2601.jpg", "slajd_2676.jpg")
"""Walther's slides on fusion, percolation and the blueprint, shown in the chapter on why three photons."""

INTRO = (
    "V přednášce Philipa Walthera stojí celý plán fotonického kvantového počítače na jediné věci: na zdroji "
    "třífotonových GHZ stavů na povel. Tahle stránka to rozvádí. Co GHZ stav je, jak na něj Greenberger, Horne "
    "a Zeilinger přišli při hledání silnější verze Bellovy věty, jak ho vídeňská skupina v roce 1999 poprvé "
    "vyrobila z fotonů, proč jsou pro počítač potřeba právě tři fotony a kde se dnes takové zdroje berou. "
    "Výpočty v textu jsou naše a hlídá je test; ostatní je doložené citacemi."
)

KEY_FINDINGS = (
    KeyFinding(
        "**GHZ stav** tří qubitů je $(|000\\rangle + |111\\rangle)/\\sqrt{2}$: buď jsou všechny tři 0, nebo všechny 1. "
        "Pro fotony v polarizaci $(|HHH\\rangle + |VVV\\rangle)/\\sqrt{2}$.",
        "ghz-co-to-je",
    ),
    KeyFinding(
        "**Bellova věta bez nerovností:** Greenberger, Horne a Zeilinger (1989) ukázali, že u tří a více částic "
        "lokální realismus nepředpoví kvantovou mechaniku ani v jediném měření – nejen statisticky jako u Bella.",
        "ghz-historie",
    ),
    KeyFinding(
        "**První GHZ z fotonů (Vídeň, 1999)** vznikl ze dvou provázaných párů: jeden foton z každého páru se potkal "
        "na polarizačním děliči a čtvrtý foton „smazal“, ze kterého páru který foton je. GHZ ale existoval jen "
        "při detekci všech čtyř fotonů – pro počítač nepoužitelný.",
        "ghz-experiment",
    ),
    KeyFinding(
        "**Proč právě tři:** fúze spotřebuje dva fotony. Ze dvou párů tak zase vznikne pár ($2 + 2 - 2 = 2$), "
        "ze dvou GHZ stavů ale čtyřfotonový stav ($3 + 3 - 2 = 4$). Tři fotony jsou nejmenší jednotka, ze které "
        "klastr roste.",
        "ghz-proc-tri",
    ),
    KeyFinding(
        "**Dnes:** ohlašovaný GHZ ze šesti jednotlivých fotonů uspěje s pravděpodobností 1/32 (Vídeň i Hefei, "
        "2024); deterministicky vyzařují řetězce provázaných fotonů kvantové tečky a atomy v rezonátoru "
        "(GHZ až ze 14 fotonů, 2022).",
        "ghz-dnes",
    ),
)

GHZ_1989 = Source(
    "Greenberger, D. M., Horne, M. A., Zeilinger, A.: *Going beyond Bell's theorem*. In: Kafatos, M. (ed.), Bell's "
    "Theorem, Quantum Theory and Conceptions of the Universe, Kluwer, Dordrecht 1989, s. 69, "
    "[arXiv:0712.0921](https://arxiv.org/abs/0712.0921)"
)
GHSZ_1990 = Source(
    "Greenberger, D. M., Horne, M. A., Shimony, A., Zeilinger, A.: *Bell's theorem without inequalities*. American "
    "Journal of Physics 58, 1131–1143 (1990)"
)
MERMIN_1990 = Source(
    "Mermin, N. D.: *What's wrong with these elements of reality?* Physics Today 43 (6), 9–11 (1990)"
)
MERMIN_PRL_1990 = Source(
    "Mermin, N. D.: *Extreme quantum entanglement in a superposition of macroscopically distinct states*. Physical "
    "Review Letters 65, 1838 (1990), [doi:10.1103/PhysRevLett.65.1838](https://doi.org/10.1103/PhysRevLett.65.1838)"
)
ZHWZ_1997 = Source(
    "Zeilinger, A., Horne, M. A., Weinfurter, H., Żukowski, M.: *Three-particle entanglements from two entangled "
    "pairs*. Physical Review Letters 78, 3031 (1997), "
    "[doi:10.1103/PhysRevLett.78.3031](https://doi.org/10.1103/PhysRevLett.78.3031)"
)
TELEPORTATION_1997 = Source(
    "Bouwmeester, D., Pan, J.-W., Mattle, K., Eibl, M., Weinfurter, H., Zeilinger, A.: *Experimental quantum "
    "teleportation*. Nature 390, 575–579 (1997)"
)
BOUWMEESTER_1999 = Source(
    "Bouwmeester, D., Pan, J.-W., Daniell, M., Weinfurter, H., Zeilinger, A.: *Observation of three-photon "
    "Greenberger-Horne-Zeilinger entanglement*. Physical Review Letters 82, 1345 (1999), "
    "[doi:10.1103/PhysRevLett.82.1345](https://doi.org/10.1103/PhysRevLett.82.1345)"
)
PAN_2000 = Source(
    "Pan, J.-W., Bouwmeester, D., Daniell, M., Weinfurter, H., Zeilinger, A.: *Experimental test of quantum "
    "nonlocality in three-photon Greenberger–Horne–Zeilinger entanglement*. Nature 403, 515–519 (2000), "
    "[doi:10.1038/35000514](https://doi.org/10.1038/35000514)"
)
PAN_REVIEW_2012 = Source(
    "Pan, J.-W., Chen, Z.-B., Lu, C.-Y., Weinfurter, H., Zeilinger, A., Żukowski, M.: *Multiphoton entanglement "
    "and interferometry*. Reviews of Modern Physics 84, 777 (2012), [arXiv:0805.2853](https://arxiv.org/abs/0805.2853)"
)
BROWNE_RUDOLPH_2005 = Source(
    "Browne, D. E., Rudolph, T.: *Resource-efficient linear optical quantum computation*. Physical Review Letters "
    "95, 010501 (2005), [doi:10.1103/PhysRevLett.95.010501](https://doi.org/10.1103/PhysRevLett.95.010501)"
)
EWERT_VAN_LOOCK_2014 = Source(
    "Ewert, F., van Loock, P.: *3/4-efficient Bell measurement with passive linear optics and unentangled "
    "ancillae*. Physical Review Letters 113, 140403 (2014), "
    "[doi:10.1103/PhysRevLett.113.140403](https://doi.org/10.1103/PhysRevLett.113.140403)"
)
CAO_2024 = Source(
    "Cao, H., Hansen, L. M., Giorgino, F., Carosini, L., Zahálka, P., Zilk, F., Loredo, J. C., Walther, P.: "
    "*Photonic source of heralded Greenberger-Horne-Zeilinger states*. Physical Review Letters 132, 130604 (2024), "
    "[doi:10.1103/PhysRevLett.132.130604](https://doi.org/10.1103/PhysRevLett.132.130604)"
)
CHEN_2024 = Source(
    "Chen, S. a kol. (Pan, J.-W.): *Heralded three-photon entanglement from a single-photon source on a photonic "
    "chip*. Physical Review Letters 132, 130603 (2024), "
    "[doi:10.1103/PhysRevLett.132.130603](https://doi.org/10.1103/PhysRevLett.132.130603)"
)
LINDNER_RUDOLPH_2009 = Source(
    "Lindner, N. H., Rudolph, T.: *Proposal for pulsed on-demand sources of photonic cluster state strings*. "
    "Physical Review Letters 103, 113602 (2009), "
    "[doi:10.1103/PhysRevLett.103.113602](https://doi.org/10.1103/PhysRevLett.103.113602)"
)
SCHWARTZ_2016 = Source(
    "Schwartz, I. a kol.: *Deterministic generation of a cluster state of entangled photons*. Science 354, 434–437 "
    "(2016)"
)
THOMAS_2022 = Source(
    "Thomas, P., Ruscio, L., Morin, O., Rempe, G.: *Efficient generation of entangled multiphoton graph states from "
    "a single atom*. Nature 608, 677–681 (2022), "
    "[doi:10.1038/s41586-022-04987-5](https://doi.org/10.1038/s41586-022-04987-5)"
)
COGAN_2023 = Source(
    "Cogan, D. a kol.: *Deterministic generation of indistinguishable photons in a cluster state*. Nature Photonics "
    "(2023), [doi:10.1038/s41566-022-01152-2](https://doi.org/10.1038/s41566-022-01152-2)"
)


WHAT_TOPIC = TheoryTopic(
    anchor="ghz-co-to-je",
    title="Co je GHZ stav",
    in_short=(
        "Tři qubity, které jsou buď všechny 0, nebo všechny 1, v superpozici. Každý sám o sobě je úplně náhodný, "
        "dohromady jsou dokonale korelované. Je to nejjednodušší „opravdu trojčásticové“ provázání."
    ),
    explanation=r"""
**Definice.** Stav Greenbergera, Horna a Zeilingera (GHZ) tří qubitů je

$$
|\mathrm{GHZ}_3\rangle = \frac{1}{\sqrt{2}}\bigl(|000\rangle + |111\rangle\bigr),
$$

u fotonů s polarizací jako qubitem $\tfrac{1}{\sqrt{2}}(|HHH\rangle + |VVV\rangle)$: buď jsou všechny tři fotony
vodorovně polarizované, nebo všechny svisle, a dokud je neměříme, platí obojí současně. Obecně pro $n$ qubitů
$(|0\dots0\rangle + |1\dots1\rangle)/\sqrt{2}$. Je to přímé zobecnění Bellova stavu
$(|00\rangle + |11\rangle)/\sqrt{2}$ ze dvou qubitů na víc.

**Co je na něm zvláštního.** Změříme-li jediný foton v bázi $H/V$, dostaneme náhodně $H$ nebo $V$ – a tím známe
i oba ostatní. Provázání se tím ale úplně zničí: zbylé dva fotony jsou pak obyčejný stav $|HH\rangle$ nebo
$|VV\rangle$. Změříme-li jeden foton „šikmo“ (v bázi $\pm 45^\circ$, tedy Pauliho $X$), zbylé dva zůstanou
provázané v Bellově stavu. GHZ stav tak nese korelace, které nejsou vidět na žádné dvojici zvlášť – každá dvojice
má sama o sobě jen klasické korelace.

**Proč se mu říká „kočičí“ stav.** $|000\rangle$ a $|111\rangle$ se liší na všech qubitech současně; pro velké $n$ je
to superpozice dvou „makroskopicky odlišných“ stavů, odtud přirovnání ke Schrödingerově kočce. Mermin v roce 1990
ukázal, že nesoulad s lokálním realismem, měřený jeho nerovností, roste u GHZ stavu s počtem částic
exponenciálně.

**Graf a klastr.** V jazyce grafových stavů (klastrových stavů z
[přednášky](/fotonika/prednaska-walther-2022#walther-klastry)) je třífotonový GHZ stav až na lokální operace totéž
co lineární klastr ze tří qubitů: stačí na krajní dva qubity použít Hadamardovo hradlo. *Vlastní výpočet:*

$$
(H \otimes I \otimes H)\,\mathrm{CZ}_{12}\,\mathrm{CZ}_{23}\,|{+}{+}{+}\rangle = |\mathrm{GHZ}_3\rangle .
$$

Proto
se v plánech fotonického počítače mluví o GHZ stavech a o malých klastrech jako o tomtéž stavebním kameni.
""",
    further_reading=(
        Reading(MERMIN_1990, "krátký a čtivý výklad GHZ argumentu"),
        Reading(MERMIN_PRL_1990, "Merminova nerovnost pro $n$ částic"),
        Reading(PAN_REVIEW_2012, "přehled mnohofotonového provázání od vídeňské a čínské skupiny"),
    ),
)

HISTORY_TOPIC = TheoryTopic(
    anchor="ghz-historie",
    title="Jak na to přišli: Bellova věta bez nerovností",
    in_short=(
        "Bellova věta ukazuje rozpor s lokálním realismem jen statisticky. Greenberger, Horne a Zeilinger hledali "
        "silnější verzi – a u tří nebo čtyř částic ji našli: čtyři měření, u kterých lokální realismus "
        "předpovídá opak kvantové mechaniky s jistotou."
    ),
    explanation=r"""
**Výchozí otázka.** Bellova věta (1964) říká, že žádná lokální realistická teorie nereprodukuje všechny
předpovědi kvantové mechaniky pro dva provázané qubity. Rozpor je ale *statistický*: lokální realismus omezuje
korelace nerovností (třeba CHSH $|S| \le 2$) a kvantová mechanika ji porušuje (až $2\sqrt{2}$). K důkazu je potřeba
mnoho měření a průměrování. Daniel Greenberger, Michael Horne a Anton Zeilinger se ptali, co se stane, když
provázaných částic bude víc než dvě.

**Odpověď (1989–1990).** Ve sborníku z roku 1989 ukázali na čtyřech částicích, že rozpor jde dostat bez
nerovností – z dokonalých korelací, tedy z výsledků, které kvantová mechanika předpovídá *s jistotou*. Úplné
zpracování vyšlo v roce 1990 s Abnerem Shimonym v American Journal of Physics pod názvem *Bellova věta bez
nerovností*. Ve stejném roce David Mermin argument zjednodušil na tři částice a podal ho tak, jak se dnes učí.

**Merminova verze krok za krokem.** Každý ze tří fotonů můžeme měřit buď v bázi $X$ (lineární polarizace
$\pm 45^\circ$), nebo $Y$ (kruhová polarizace $R/L$); výsledek je vždy $+1$ nebo $-1$. Pro stav
$|\mathrm{GHZ}_3\rangle$ kvantová mechanika předpovídá s jistotou součiny výsledků:

| Nastavení | Součin výsledků |
|---|---|
| $X$, $Y$, $Y$ | $-1$ |
| $Y$, $X$, $Y$ | $-1$ |
| $Y$, $Y$, $X$ | $-1$ |
| $X$, $X$, $X$ | $+1$ |

*Vlastní výpočet:* stav je vlastním vektorem všech čtyř operátorů $X \otimes Y \otimes Y$, $Y \otimes X \otimes Y$,
$Y \otimes Y \otimes X$ a $X \otimes X \otimes X$ s vlastními čísly $-1, -1, -1, +1$.

**Kde se lokální realismus zasekne.** Lokální realista řekne: každý foton nese předem dané hodnoty $x_i$ a $y_i$
($\pm 1$) pro obě možná měření, nezávisle na tom, co se měří u ostatních. Pak

$$
(x_1 y_2 y_3)(y_1 x_2 y_3)(y_1 y_2 x_3) = x_1 x_2 x_3 \, (y_1 y_2 y_3)^2 = x_1 x_2 x_3 ,
$$

protože každé $y_i$ se objeví dvakrát a $y_i^2 = 1$. Z prvních tří řádků tabulky je levá strana
$(-1)^3 = -1$, takže lokální realismus předpovídá **$x_1 x_2 x_3 = -1$**. Kvantová mechanika předpovídá **$+1$**.
Žádná statistika – stačí (v ideálním případě) jediné měření $XXX$.

**Proč to tehdy nikdo neměřil.** Vyrobit tři provázané částice bylo koncem 80. let mimo dosah: zdroje SPDC dávaly
jen páry. Trvalo skoro deset let, než vídeňská skupina zvládla techniku, která dva páry „sešije“ – stejnou, jakou
v roce 1997 použila pro kvantovou teleportaci. Za experimenty s provázanými fotony dostal Zeilinger v roce 2022
Nobelovu cenu spolu s Aspectem a Clauserem.
""",
    further_reading=(
        Reading(GHZ_1989, "původní čtyřčásticová verze"),
        Reading(GHSZ_1990, "úplné zpracování, název „Bellova věta bez nerovností“"),
        Reading(MERMIN_1990, "zjednodušení na tři částice"),
        Reading(NOBEL_2022),
    ),
)

EXPERIMENT_TOPIC = TheoryTopic(
    anchor="ghz-experiment",
    title="Jak vídeňská skupina vyrobila první fotonový GHZ stav (1999)",
    in_short=(
        "Dva provázané páry z jednoho laserového pulzu, jeden foton z každého na polarizační dělič a čtvrtý foton "
        "změřený tak, aby nešlo poznat, ze kterého páru je. Pokud cvaknou všechny čtyři detektory, zbylé tři "
        "fotony vykazují GHZ korelace. O rok později s nimi změřili Merminův test."
    ),
    explanation=r"""
**Návrh (1997).** Zeilinger, Horne, Weinfurter a Żukowski ukázali, jak dostat tři provázané částice ze dvou
nezávislých párů: z každého páru se vezme jedna částice a obě se změří tak, aby nešlo zjistit, ze kterého páru
která pochází. Zbylé tři částice pak skončí v GHZ stavu. Klíčová ingredience je **nerozlišitelnost**: fotony
z různých párů se musí potkat ve stejný okamžik a se stejným spektrem.

**Aparatura (Bouwmeester, Pan, Daniell, Weinfurter, Zeilinger, 1999).** Krátký ultrafialový pulz prošel krystalem
BBO, kde občas vytvořil provázaný pár, odrazil se zpět a krystalem prošel podruhé – tak mohly z jednoho pulzu
vzniknout dva páry. Krátké pulzy a úzké spektrální filtry zajistily, že fotony z obou párů jsou v čase
nerozlišitelné. Jeden foton z každého páru se potkal na **polarizačním děliči (PBS)**, který $H$ propouští
a $V$ odráží. Čtyři fotony šly na detektory: spouštěcí $T$ a tři detektory $D_1$, $D_2$, $D_3$ s analyzátory
polarizace, které měřily GHZ korelace. Část detekce byla nastavená tak, aby z ní nešlo poznat, ze kterého páru
foton pochází (polarizace měřená „šikmo“, ve směru $45^\circ$).

**Proč to funguje (zjednodušeně).** *Vlastní výpočet na ideálním modelu:* vezměme dva páry ve stavu
$(|HH\rangle + |VV\rangle)/\sqrt{2}$, fotony $a, b$ a $c, d$. Fotony $b$ a $c$ jdou na PBS. Vyjde-li z každého
výstupu děliče právě jeden foton, musely mít $b$ i $c$ stejnou polarizaci – buď oba $H$, nebo oba $V$ (jinak by
skončily ve stejném výstupu). Nastane to s pravděpodobností $1/2$ a stav čtyř fotonů je pak
$(|HHHH\rangle + |VVVV\rangle)/\sqrt{2}$ – čtyřfotonový GHZ stav. Pak se foton na detektoru $T$ změří
v bázi $\pm 45^\circ$; výsledek $+45^\circ$ (pravděpodobnost $1/2$) smaže informaci o jeho polarizaci a zbylé tři
fotony jsou přesně v $(|HHH\rangle + |VVV\rangle)/\sqrt{2}$. Skutečný experiment měl páry v jiném Bellově stavu,
takže výsledný stav vycházel jako $(|HHV\rangle + |VVH\rangle)/\sqrt{2}$ – až na otočení polarizace jednoho
fotonu totéž.

Mimochodem: krok s polarizačním děličem je přesně **fúze typu I**, kterou o šest let později Browne a Rudolph
navrhli pro stavbu klastrů (další kapitola). Vídeňský experiment tak byl první fúzí, jen se tomu tak ještě neříkalo.

**Háček: postselekce.** GHZ korelace se ukážou jen v případech, kdy cvaknou **všechny čtyři** detektory současně.
Jenže při detekci se fotony zničí. Stav tedy „existuje“ jen zpětně, v datech vybraných podle detekce
(*postselekce*). Navíc SPDC občas vytvoří dva páry v jednom místě a žádný v druhém, což dává falešné čtveřice; na
to experiment musel dávat pozor. Pro fyziku (test lokálního realismu) to stačí, pro počítač ne: tam potřebujeme
GHZ stav, který nám někdo *ohlásí* a necháme ho žít dál.

**Test lokálního realismu (Pan a kol., Nature 2000).** Se stejným zdrojem změřili tři nastavení typu $XYY$,
ze kterých lokální realismus předpovídá výsledek čtvrtého měření $XXX$, a pak změřili i $XXX$. Výsledky souhlasily
s kvantovou mechanikou a byly v ostrém rozporu s lokálním realismem. Průměrná viditelnost korelací byla podle
přehledových prací $(71 \pm 4)\,\%$, nad hranicí 50 %, kterou je pro porušení lokálního realismu u tří částic potřeba
překročit. (Kvůli postselekci se dodnes diskutuje, jak „čistý“ ten test byl – stejné výhrady jako u raných
Bellových experimentů.)
""",
    further_reading=(
        Reading(ZHWZ_1997, "návrh: tři provázané částice ze dvou párů"),
        Reading(TELEPORTATION_1997, "stejná dvoupárová technika o dva roky dřív"),
        Reading(BOUWMEESTER_1999, "první pozorování třífotonového GHZ"),
        Reading(PAN_2000, "Merminův test s fotony"),
        Reading(PAN_REVIEW_2012, "přehled mnohofotonových experimentů"),
        Reading(KWIAT_1995, "zdroj provázaných párů"),
    ),
)

WHY_THREE_TOPIC = TheoryTopic(
    anchor="ghz-proc-tri",
    title="Proč právě tři fotony: fúze a růst klastru",
    in_short=(
        "Fúze spojí dva kusy klastru tak, že dva fotony změří. Z párů tak nic neroste ($2 + 2 - 2 = 2$), z GHZ "
        "stavů ano ($3 + 3 - 2 = 4$). Fúze z lineární optiky uspěje jen napůl, s pomocnými fotony na 75 %, a to "
        "s třífotonovými stavy právě stačí na perkolaci."
    ),
    explanation=r"""
**Fúze.** Browne a Rudolph (2005) navrhli spojovat malé klastry měřením: z každého kusu se vezme jeden foton
a oba se změří na děliči svazku. *Fúze typu II* je vlastně Bellovo měření dvou fotonů – a z lineární optiky
jde rozlišit jen dva ze čtyř Bellových stavů, takže uspěje s pravděpodobností $1/2$. (*Fúze typu I* je ještě
jednodušší: polarizační dělič a měření jednoho výstupu – přesně krok z experimentu 1999.) Když uspěje, změřené
fotony zmizí a zbytky obou kusů se spojí; když selže, spoj vypadne (a protože víme, že selhala, počítá se s tím).

**Počítání fotonů.** Fúze typu II spotřebuje dva fotony. Spojíme-li dva Bellovy páry, zbudou
$2 + 2 - 2 = 2$ fotony – zase jen pár, nic nevyrostlo. Spojíme-li dva třífotonové GHZ stavy, zbudou
$3 + 3 - 2 = 4$ fotony ve čtyřfotonovém GHZ stavu. **Tři fotony jsou nejmenší kus, ze kterého klastr roste.**
*Vlastní výpočet:* pro každý ze čtyř Bellových výsledků měření fotonů 3 a 4 ve stavu
$|\mathrm{GHZ}_3\rangle \otimes |\mathrm{GHZ}_3\rangle$ (každý s pravděpodobností $1/4$) zbude čtyřfotonový GHZ
stav až na lokální Pauliho opravu; lineární optika rozliší dva z nich, odtud úspěšnost $1/2$.

**Zvýšení úspěšnosti.** S pomocnými fotony jde Bellovo měření z lineární optiky „posílit“: Ewert a van Loock (2014)
ukázali úspěšnost $3/4$ s pomocnými fotony, které nemusí být ani provázané; Walther na slajdu uvádí dvě varianty
(čtyři pomocné fotony, nebo dva provázané), obě s úspěšností 75 %.

**Perkolace.** Proč stačí 75 %? Gimeno-Segovia, Shadbolt, Browne a Rudolph (2015) spočítali, že ze třífotonových
GHZ stavů a fúzí s úspěšností nad prahem zhruba $74{,}6\,\%$ (2D mřížka, podle grafu na Waltherově slajdu) vznikne
s vysokou pravděpodobností souvislý klastr přes celou mřížku – a to „balisticky“, bez opakování a bez paměti na
fotony. Kompromis je mezi velikostí výchozího stavu a kvalitou fúzí: s pětiqubitovými hvězdami stačí fúze
s úspěšností 50 % (Pant a kol., 2019), se třemi fotony je potřeba 75 %.

**Rudolphův plán (2017)**, který Walther ukazuje, z toho skládá stroj: (1) deterministický zdroj třífotonových GHZ
stavů, (2) fúze s úspěšností kolem 75 %, (3) růst klastru jen pasivní optikou, (4) obyčejné měřením řízené
počítání. Jedinou aktivní vrstvou je zdroj GHZ stavů – a právě ten je nejtěžší. Pozor na slovo „deterministický“:
Rudolphův článek nepředpokládá zázračný zdroj, ale *téměř* deterministický, poskládaný z mnoha pravděpodobnostních
– ohlašované jednotlivé fotony z křemíkových vlnovodů se multiplexují, z nich se pravděpodobnostně skládají malé
provázané stavy a ty se multiplexují znovu (podobně jako výpočet s 1/32 v další kapitole). Na Rudolphův plán navazuje
fúzní kvantové počítání (FBQC, Bartolucci a kol., 2023), architektura firmy PsiQuantum, kde se z malých
„zdrojových stavů“ a fúzí rovnou staví kód opravující chyby.
""",
    further_reading=(
        Reading(BROWNE_RUDOLPH_2005, "fúze typu I a II"),
        Reading(EWERT_VAN_LOOCK_2014, "Bellovo měření s úspěšností 3/4"),
        Reading(GIMENO_SEGOVIA_2015, "ze třífotonových GHZ stavů k balistickému počítání"),
        Reading(PANT_PERCOLATION),
        Reading(RUDOLPH_2017, "plán na Waltherově slajdu"),
        Reading(BARTOLUCCI_FBQC, "fúzní kvantové počítání"),
    ),
)

TODAY_TOPIC = TheoryTopic(
    anchor="ghz-dnes",
    title="Kde vzít tři fotony na povel: ohlašované a deterministické GHZ",
    in_short=(
        "Dvě cesty. Ohlašovaná: šest jednotlivých fotonů z kvantové tečky interferuje na čipu a tři detekce ohlásí, "
        "že zbylé tři jsou v GHZ stavu – uspěje s pravděpodobností 1/32. Deterministická: jeden emitor (kvantová "
        "tečka, atom v rezonátoru) vyzáří provázané fotony jeden po druhém."
    ),
    explanation=r"""
**Ohlašované GHZ ze šesti jednotlivých fotonů (2024).** Místo SPDC se vezme deterministický zdroj jednotlivých
fotonů (kvantová tečka v mikrorezonátoru, viz [přednáška](/fotonika/prednaska-walther-2022#walther-hardware)) a šest
fotonů se pošle do lineárně optického obvodu. Když tři pomocné detektory ukážou správnou kombinaci, zbylé tři
fotony jsou v GHZ stavu a **přežijí** – na rozdíl od roku 1999 jde stav dál použít. Protokol uspěje
s pravděpodobností $1/32$. Ve stejném čísle Physical Review Letters vyšly dvě práce:

- **Vídeň (Cao a kol., Walther):** šestifotonový zdroj z kvantové tečky (šestice s frekvencí kolem 547 Hz,
  průměrná nerozlišitelnost dvojic 0,923), věrnost ohlášeného GHZ stavu až $0{,}7278 \pm 0{,}0106$;
- **Hefei (Chen a kol., Pan):** totéž na programovatelném 12módovém čipu, věrnost $0{,}573 \pm 0{,}024$.

*Vlastní výpočet, co znamená 1/32:* jeden generátor uspěje v průměru jednou za 32 pokusů. Má-li být GHZ stav
k dispozici „skoro na povel“, musí běžet víc generátorů vedle sebe a vybrat ten, který uspěl (multiplexování):
aby aspoň jeden z $N$ uspěl s pravděpodobností 99 %, je potřeba $N = 146$ generátorů, tedy 876 jednotlivých fotonů
na jeden GHZ stav. Proto je pro plán tak důležité, aby zdroje byly rychlé, levné a vyrobitelné ve velkém – a proto
PsiQuantum sází na křemíkovou fotoniku z polovodičové továrny.

**Deterministické zdroje: emitor, který „plete“ řetězec fotonů.** Lindner a Rudolph (2009) navrhli, jak jeden
spin (elektron v kvantové tečce) může vyzařovat fotony jeden po druhém tak, že každý je provázaný se spinem
a přes něj s předchozími – vzniká lineární klastr. Mezi emisemi se spin pootočí; na konci se změří. Realizace:

- **kvantová tečka (Schwartz a kol., 2016)** – první deterministicky vytvořený řetězec provázaných fotonů,
- **atom rubidia v rezonátoru (Thomas a kol., 2022)** – GHZ stavy až ze **14 fotonů** a lineární klastry až
  z **12 fotonů**, s vysokou účinností,
- **kvantová tečka s nerozlišitelnými fotony (Cogan a kol., 2023)** – klastr z fotonů, které spolu umějí
  interferovat, což je pro fúze nutné.

Deterministický zdroj je přesně krok (1) Rudolphova plánu. Zbývá zvládnout ztráty (každý ztracený foton je
chyba), nerozlišitelnost fotonů z různých zdrojů a výrobu ve velkém.

*Vlastní poznámka pro disertaci:* GBS, na kterém stojí modifikované Monte Carlo v této aplikaci, GHZ stavy ani
fúze nepotřebuje – stačí stlačené světlo, interferometr a detektory. Univerzální fotonický počítač je jiná a mnohem
delší cesta; přehled firem, které ji jdou, je ve [Fotonice ve světě](/fotonika-ve-svete#svet-jednotlive-fotony).
""",
    further_reading=(
        Reading(CAO_2024, "vídeňské ohlašované GHZ"),
        Reading(CHEN_2024, "ohlašované GHZ na čipu z Hefei"),
        Reading(LINDNER_RUDOLPH_2009, "návrh deterministického zdroje klastrů"),
        Reading(SCHWARTZ_2016),
        Reading(THOMAS_2022, "GHZ ze 14 fotonů z jednoho atomu"),
        Reading(COGAN_2023),
        Reading(WALTHER_VIDEO, "kapitola o fúzích od 41:13"),
    ),
)

TOPICS = (WHAT_TOPIC, HISTORY_TOPIC, EXPERIMENT_TOPIC, WHY_THREE_TOPIC, TODAY_TOPIC)
