"""Texts of the page on what Qpurpose actually sells to Jyske Bank and how its method behaves on classical hardware."""

from __future__ import annotations

from typing import Tuple

from gbs.advantage_share import AdvantageShare
from ui.advantage_content import DANISH_QUANTUM_USE_CASES_PAGE, QPURPOSE_FINANCE
from ui.literature_review_content import SDU_QPURPOSE_SPINOUT
from ui.theory_content import (
    ANDERSEN_SHAN_ADVANTAGE,
    ANDERSEN_SHAN_EXPECTATIONS,
    DANISH_QUANTUM_USE_CASES,
    SDU_QUANTUM_FINANCE,
    KeyFinding,
    Reading,
    Source,
    TheoryTopic,
)

TITLE = "Qpurpose: co skutečně prodávají a jak to funguje"
SOURCES_ANCHOR = "qpurpose-zdroje"
SOURCES_CHECKED_DATE = "17. 10. 2026"

REPLICATION_MATRICES = 30
REPLICATION_COEFFICIENT_VECTORS = 100
REPLICATION_SEED = 2025
REPLICATION_SHARES: Tuple[AdvantageShare, ...] = (
    AdvantageShare(3, 2, derived_percent=95.59, printed_percent=94.94, median_scale=1.068, median_variance_ratio=5.149),
    AdvantageShare(3, 3, derived_percent=99.50, printed_percent=98.83, median_scale=1.155, median_variance_ratio=33.87),
    AdvantageShare(3, 4, derived_percent=99.93, printed_percent=100.0, median_scale=1.180, median_variance_ratio=293.6),
    AdvantageShare(4, 2, derived_percent=96.83, printed_percent=94.66, median_scale=1.045, median_variance_ratio=3.314),
    AdvantageShare(4, 3, derived_percent=100.0, printed_percent=100.0, median_scale=1.085, median_variance_ratio=16.92),
    AdvantageShare(4, 4, derived_percent=100.0, printed_percent=100.0, median_scale=1.170, median_variance_ratio=185.1),
)
"""Our recomputation of Fig. 2 in arXiv:2502.19362 (gbs.advantage_share.advantage_share, cells in this order, one
shared generator seeded with REPLICATION_SEED). Stored because it takes seconds; a test recomputes it."""

INTRO = (
    "Odpověď na otázku, co má firma Qpurpose skutečně v provozu u Jyske Bank a jak to funguje – z veřejných "
    f"zdrojů ověřených {SOURCES_CHECKED_DATE} a z vlastních výpočtů nad články Andersena a Shan. U každého tvrzení "
    "je vidět, jestli je doložené, jen tvrzené, nebo jde o náš odhad."
)

QPURPOSE_JYSKE_BLOG = Source(
    "Qpurpose: [How Jyske Bank Adopted Quantum-Optimised Trading]"
    "(https://qpurpose.dk/blog/how-jyske-bank-adopted-quantum-optimised-trading) – blog bez data"
)
QPURPOSE_GPU_JOB = Source(
    "Qpurpose: [Algorithmic Software Engineer – GPU-accelerated computing]"
    "(https://qpurpose.dk/blog/algorithmic-software-engineer-gpu-accelerated-computing) – pracovní inzerát"
)
FINANSFORBUNDET_JYSKE = Source(
    "Finansforbundet: [Gå-hjem-møde i Jyske Bank endte med et kvante-spring]"
    "(https://finansforbundet.dk/dk/nyheder/2025/gaa-hjem-moede-i-jyske-bank-endte-med-et-kvante-spring/), "
    "29. 4. 2025 – rozhovor s Mortenem Byrdalem, šéfem obchodování Jyske Markets"
)
AUTHORS_CODE = Source(
    "Shan, S.: [GBSPE](https://github.com/sshanshans/GBSPE) – kód k arXiv:2502.19362; rozptyl GBS-I počítá "
    "metoda `compute_qgbs` v souboru `src/utils/NData.py`"
)

PRODUCT_TOPIC = TheoryTopic(
    anchor="qpurpose-co-maji",
    title="Co prodávají: Price Predator pro Jyske Bank",
    in_short=(
        "Hotový software v provozu, ne kvantový počítač. Qpurpose Price Predator dává obchodníkům Jyske Bank "
        "krátkodobé předpovědi cen a směru trhu pro zhruba 300 akcií, je zabudovaný do IT banky a běží na klasických "
        "počítačích, které kvantový algoritmus emulují."
    ),
    explanation=r"""
**Produkt (doloženo z webu firmy).** Stránka Finance jmenuje produkt *Qpurpose Price Predator*: předpovídá ceny
tříd akcií v blízké budoucnosti a směr trhu, pokrývá přes 300 akcií z živých dat a běží na vysoce výkonných
počítačích, které emulují kvantové systémy. Vyvinutý a ověřený byl za tři roky spolupráce s Jyske Bank.

**Jak ho banka používá (doloženo z více zdrojů).** Blog Qpurpose popisuje řešení jako kvantově inspirované
a plně zabudované do IT systémů banky; obchodníci ho používají zhruba pro 300 tříd akcií a dostávají předpovědi
cen a podporu rozhodování pro živé obchody. Brožura *16 Danish Quantum Use Cases* (prosinec 2024, s. 44) uvádí,
že obchodníci software používají denně, a vedle předpovědí zmiňuje nástroje pro hodnocení rizik a plánování
zajištění. Šéf obchodování Jyske Markets Morten Byrdal v rozhovoru z dubna 2025 říká, že projekt běží asi rok
a půl, výstup slouží obchodníkovi jako podklad – rozhoduje vždy člověk – a nejkritičtější je kvalita dat.

**Obchodní model.** Qpurpose o sobě píše, že dodává služby „end-to-end“, a stránka SDU ji označuje za firmu
poskytující řešení a služby. V inzerátu na programátora GPU firma otevřeně uvádí, že projekty zatím zahrnují
klasické algoritmy a vývoj softwaru (CUDA, HIP, OpenCL, Python, C++). Forma smlouvy ani cena veřejné nejsou.

**Rozpor ve zdrojích.** Byrdal v rozhovoru mluví o tom, že banka „staví vlastní kvantový počítač“. Všechny
ostatní zdroje popisují emulaci na klasickém HPC; nejspíš jde o zjednodušení pro novináře (náš výklad).
""",
    further_reading=(
        Reading(QPURPOSE_FINANCE, "produkt Price Predator"),
        Reading(QPURPOSE_JYSKE_BLOG, "jak ho banka používá"),
        Reading(DANISH_QUANTUM_USE_CASES_PAGE, "případ 16"),
        Reading(FINANSFORBUNDET_JYSKE, "pohled banky"),
        Reading(SDU_QPURPOSE_SPINOUT, "firma jako spin-off SDU"),
        Reading(QPURPOSE_GPU_JOB, "projekty zatím na klasických algoritmech"),
    ),
)

METHOD_TOPIC = TheoryTopic(
    anchor="qpurpose-jak-funguje",
    title="Jak to podle všeho funguje",
    in_short=(
        "Doložené je, že počítají gaussovsky vážené integrály metodou Andersena a Shan a že vše běží klasicky. Jak "
        "z integrálů vzniká předpověď ceny, veřejně popsané není – níže je oddělené, co je doložené a co náš odhad."
    ),
    explanation=r"""
**Doloženo.** Stránka SDU uvádí rámec „Gaussian Boson Sampling applied to Gaussian Weighted Integrals“ od
J. E. Andersena a Shan Shan, denní provoz na obchodním stole a simulace na HPC. Brožura dodává, že GBS je
relevantní, protože počítá gaussovsky vážené integrály, a že algoritmy zatím běží na klasickém HPC.

**Co ty integrály jsou.** $\mu = \int f(x)\,\mathcal{N}(0, B)(x)\,dx$ pro polynom nebo mocninnou řadu $f$; podle
Wickovy věty $\mu = \sum_I a_I\,\mathrm{Haf}(B_I)$. Odhad GBS-P z výstřelů přístroje odmocňuje četnosti vzorů
fotonů. Odhad GBS-I je vážený výběr pro speciální rodinu $\mu = \sum_I a_I\,\mathrm{Haf}(B_I)^2$: každý výstřel se
vzorem $I$ přispěje hodnotou $a_I\,I!\,t^{-2K}/d_t$. Ani jeden z nich hafniány za běhu nepočítá – ty „počítá“
fotonický přístroj tím, že vzorkuje.

**Náš odhad, jak z toho vzniká předpověď.** (1) Výnosy akcií z živých dat se popíšou vícerozměrným normálním
rozdělením. (2) Hledaná veličina – očekávaný pohyb ceny nebo výplata zajištění – se aproximuje polynomem
v těchto výnosech. (3) Její střední hodnota je gaussovský integrál. Na klasickém HPC jde takový integrál buď
spočítat přesně přes hafniány, nebo odhadnout vážením vzorků z emulovaného rozdělení GBS. Která varianta běží
u Jyske Bank, veřejně známé není.
""",
    further_reading=(
        Reading(SDU_QUANTUM_FINANCE, "rámec gaussovsky vážených integrálů"),
        Reading(DANISH_QUANTUM_USE_CASES, "běh na klasickém HPC"),
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "odhady GBS-I a GBS-P"),
    ),
)

CLASSICAL_TOPIC = TheoryTopic(
    anchor="qpurpose-klasicky",
    title="Co z metody zbude na klasickém počítači",
    in_short=(
        "Exponenciální výhoda z článku platí pro ideální kvantový přístroj proti obyčejnému Monte Carlu a měří se "
        "počtem vzorků. Na klasickém počítači se rozdělení GBS musí emulovat ze stejných hafniánů, ze kterých jde "
        "výsledek spočítat přesně."
    ),
    explanation=r"""
**Jak autoři měří cenu.** V příloze C prvního článku počítají, že jeden vzorek z GBS stojí konstantní čas – to
platí pro skutečný fotonický přístroj. Při emulaci na klasickém počítači je potřeba znát pravděpodobnosti
$P_{tB}(I) = \frac{d_t}{I!}\,t^{2K}\,\mathrm{Haf}(B_I)^2$, tedy hafniány všech vzorů, které se dají vylosovat.

**Proč je to problém.** Kdo zná $\mathrm{Haf}(B_I)$ pro všechny vzory, zná i přesnou hodnotu
$\mu = \sum_I a_I\,\mathrm{Haf}(B_I)^2$ a nemusí vzorkovat vůbec. Tabulka níže to ukazuje na matici $B$
z příkladu 6.1 prvního článku s $a_I = 1$: GBS-I potřebuje řádově méně vzorků než Monte Carlo a rozdíl s rostoucím
$K$ roste, jenže přesný výpočet potřebuje jen hafniány ze druhého sloupce – v aplikaci je spočítá Steinova
rekurze za zlomek sekundy.

**Co z toho plyne (náš výklad).** Klasická „kvantově inspirovaná“ verze může porazit *obyčejné* Monte Carlo,
protože je to chytřejší numerika: přesný výpočet přes hafniány nebo vážený výběr. Proti nejlepší klasické
metodě ale exponenciální výhoda na klasickém hardwaru nevzniká. Autoři sami v příloze D uvádějí jako otevřenou
otázku, jestli v oblasti, kde jejich odhady vyhrávají, leží nějaká úloha prokazatelně těžká pro klasický
počítač. Přesný výpočet přestane stačit u mnoha proměnných a vysokých stupňů – počet vzorů roste jako
$\binom{2K + N - 1}{N - 1}$ – a právě tam by měl smysl skutečný fotonický přístroj.
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "příloha C (cena vzorku) a příloha D (otevřená otázka těžkosti)"),
    ),
)

PAPER_CHECK_TOPIC = TheoryTopic(
    anchor="qpurpose-kontrola-clanku",
    title="Kontrola článku: chyba ve větě 3.5",
    in_short=(
        "Ve větě 3.5 druhého článku je v rozptylu GBS-I faktor t⁻⁴ᴷ, ze samotného odhadu ale vychází t⁻²ᴷ – a stejně "
        "chybně počítá i kód autorů. Náš přepočet obrázku 2 ukazuje, že závěr se tím nemění."
    ),
    explanation=r"""
**Odvození.** Výstřel se vzorem $I$ (s $|I| = 2K$ fotony) padne s pravděpodobností
$P_{tB}(I) = \frac{d_t}{I!}\,\mathrm{Haf}((tB)_I)^2 = \frac{d_t}{I!}\,t^{2K}\,\mathrm{Haf}(B_I)^2$, protože hafnián
matice $2K \times 2K$ je homogenní stupně $K$. Odhad přičte $Z = \frac{I!}{d_t}\,a_I\,t^{-2K}$, takže

$$\mathbb{E}[Z^2] = \sum_I P_{tB}(I)\,Z^2 = \frac{t^{-2K}}{d_t}\sum_{|I|=2K} a_I^2\,I!\,\mathrm{Haf}(B_I)^2.$$

Věta 3.5 i řádek `return qgbs_sum * (self.t_factor ** (-4 * self.K)) / self.dt` v kódu autorů mají $t^{-4K}$.
Že správně je $t^{-2K}$, potvrzuje i důsledek 3.6 téhož článku: minimum $t^{-2K}/d_t$ leží přesně v bodě
$m_{tB} = 2K$, s $t^{-4K}$ by leželo v $4K$. V aplikaci to hlídá test, který rozptyl spočítá přímým součtem přes
všechny vzory.

**Mění to závěr?** Ne. Optimální $t$ vychází blízko 1, takže faktor $t^{2K}$ je malý proti poměru rozptylů Monte
Carla a GBS-I. Tabulka níže opakuje výpočet obrázku 2 (náhodné matice a koeficienty podle §4.2) s oběma vzorci.
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_ADVANTAGE, "věta 3.5, důsledek 3.6 a obrázek 2"),
        Reading(AUTHORS_CODE, "výpočet rozptylu GBS-I"),
    ),
)

QUESTIONS_TOPIC = TheoryTopic(
    anchor="qpurpose-otazky",
    title="Na co se zeptat Qpurpose nebo Jyske Bank",
    in_short="Otázky, které by z tvrzení Qpurpose udělaly ověřitelná fakta.",
    explanation=r"""
1. **Co přesně počítáte?** Jakou funkci $f$, jaký stupeň $K$ a kolik proměnných $N$ – a jak se z integrálu stane
   předpověď ceny?
2. **Přesný výpočet, nebo vzorkování?** Počítáte integrál na HPC přes hafniány, nebo vzorkujete z emulovaného GBS?
   Jak dlouho trvá jeden přepočet a kolik stojí výpočetní čas?
3. **Proti čemu je „2 bazické body proti 10“?** Co je konvenční přístup, jaký horizont předpovědi a jaká metrika?
4. **Negaussovská data.** Výnosy mají tlusté chvosty – jak to model řeší?
5. **Znaménko hafniánu.** Druhý článek u GBS-P předpokládá efektivní metodu pro znaménko hafniánu a slibuje ji
   v další práci. Máte ji?
6. **Klasická těžkost.** Leží úlohy banky v oblasti, kde odhady vyhrávají, a je tam nějaká úloha prokazatelně
   těžká pro klasický počítač?
7. **Hardware.** Plánujete běh na skutečném fotonickém přístroji a kdy?
8. **Věta 3.5.** Víte o faktoru $t^{-4K}$ místo $t^{-2K}$? Upozornit autory je i dobrý způsob, jak navázat
   odborný kontakt (náš návrh).
""",
    further_reading=(Reading(QPURPOSE_JYSKE_BLOG, "tvrzení o 2 a 10 bazických bodech"),),
)

TOPICS: Tuple[TheoryTopic, ...] = (
    PRODUCT_TOPIC,
    METHOD_TOPIC,
    CLASSICAL_TOPIC,
    PAPER_CHECK_TOPIC,
    QUESTIONS_TOPIC,
)

KEY_FINDINGS: Tuple[KeyFinding, ...] = (
    KeyFinding(
        "**Mají software v provozu, ne kvantový počítač.** Qpurpose Price Predator dává obchodníkům Jyske Bank "
        "krátkodobé předpovědi pro zhruba 300 akcií a běží na klasickém HPC zabudovaném do IT banky.",
        PRODUCT_TOPIC.anchor,
    ),
    KeyFinding(
        "**Prodávají vývoj a provoz na zakázku.** Software vznikl za tři roky spolupráce s bankou a podle inzerátů "
        "firmy stojí projekty zatím na klasických algoritmech.",
        PRODUCT_TOPIC.anchor,
    ),
    KeyFinding(
        "**Metodou jsou gaussovsky vážené integrály Andersena a Shan.** Jak z nich vzniká předpověď ceny, veřejně "
        "popsané není.",
        METHOD_TOPIC.anchor,
    ),
    KeyFinding(
        "**Na klasickém počítači exponenciální výhoda mizí.** Emulace GBS potřebuje stejné hafniány jako přesný "
        "výpočet; porazit jde jen obyčejné Monte Carlo.",
        CLASSICAL_TOPIC.anchor,
    ),
    KeyFinding(
        "**Ve druhém článku je chyba ve vzorci pro rozptyl GBS-I** (t⁻⁴ᴷ místo t⁻²ᴷ, i v kódu autorů), závěr se tím "
        "ale nemění.",
        PAPER_CHECK_TOPIC.anchor,
    ),
    KeyFinding(
        "**Čísla o přínosu (2 bazické body proti 10, pětkrát přesnější, vyšší výnosy) nejde ověřit** – chybí "
        "definice i srovnání.",
        QUESTIONS_TOPIC.anchor,
    ),
)
