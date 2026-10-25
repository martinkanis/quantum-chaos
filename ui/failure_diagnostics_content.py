"""Texts of the page on when a GBS-based risk estimate fails: three sources of error and how to detect each one."""

from __future__ import annotations

from typing import Tuple

from ui.caveats_content import CLASSICAL_SIMULATION, TAIL_RISK
from ui.literature_review_content import BULMER_BOUNDARY
from ui.random_matrix_content import (
    BDS_1996,
    BOUCHAUD_POTTERS_REVIEW,
    BUN_BOUCHAUD_POTTERS,
    LALOUX_1999,
    czech_decimal,
)
from ui.random_matrix_gbs_content import (
    EQUAL_SAVINGS,
    LONG_SHORT_DEGREE,
    LONG_SHORT_SAVINGS,
    NOISE_EXAMPLE_DEGREE,
    NOISE_EXAMPLE_MOMENT_RATIO,
    NOISE_EXAMPLE_RATIO,
    saving,
    saving_label,
    times_more_samples,
)
from ui.theory_content import (
    ANDERSEN_SHAN_ADVANTAGE,
    ANDERSEN_SHAN_EXPECTATIONS,
    OH_CLASSICAL_SIMULATION,
    Reading,
    Source,
    TheoryTopic,
)

SOURCES_ANCHOR = "ds-zdroje"

CONT_2001 = Source(
    "Cont, R.: *Empirical properties of asset returns: stylized facts and statistical issues*. Quantitative "
    "Finance 1 (2001), 223–236, [doi:10.1080/713665670](https://doi.org/10.1080/713665670)"
)
PINCUS_1991 = Source(
    "Pincus, S. M.: *Approximate entropy as a measure of system complexity*. Proceedings of the National Academy "
    "of Sciences 88 (1991), 2297–2301, [doi:10.1073/pnas.88.6.2297](https://doi.org/10.1073/pnas.88.6.2297)"
)
RICHMAN_MOORMAN_2000 = Source(
    "Richman, J. S., Moorman, J. R.: *Physiological time-series analysis using approximate entropy and sample "
    "entropy*. American Journal of Physiology – Heart and Circulatory Physiology 278 (2000), H2039–H2049, "
    "[doi:10.1152/ajpheart.2000.278.6.H2039](https://doi.org/10.1152/ajpheart.2000.278.6.H2039)"
)
BANDT_POMPE_2002 = Source(
    "Bandt, C., Pompe, B.: *Permutation entropy: a natural complexity measure for time series*. Physical Review "
    "Letters 88 (2002), 174102, [doi:10.1103/PhysRevLett.88.174102](https://doi.org/10.1103/PhysRevLett.88.174102)"
)
ZUNINO_2009 = Source(
    "Zunino, L., Zanin, M., Tabak, B. M., Pérez, D. G., Rosso, O. A.: *Forbidden patterns, permutation entropy and "
    "stock market inefficiency*. Physica A 388 (2009), 2854–2864, "
    "[doi:10.1016/j.physa.2009.03.042](https://doi.org/10.1016/j.physa.2009.03.042)"
)
ECKMANN_KAMPHORST_RUELLE = Source(
    "Eckmann, J.-P., Oliffson Kamphorst, S., Ruelle, D.: *Recurrence plots of dynamical systems*. Europhysics "
    "Letters 4 (1987), 973–977, [doi:10.1209/0295-5075/4/9/004](https://doi.org/10.1209/0295-5075/4/9/004)"
)
MARWAN_2007 = Source(
    "Marwan, N., Romano, M. C., Thiel, M., Kurths, J.: *Recurrence plots for the analysis of complex systems*. "
    "Physics Reports 438 (2007), 237–329, "
    "[doi:10.1016/j.physrep.2006.11.001](https://doi.org/10.1016/j.physrep.2006.11.001)"
)
BASTOS_CAIADO_2011 = Source(
    "Bastos, J. A., Caiado, J.: *Recurrence quantification analysis of global stock markets*. Physica A 390 "
    "(2011), 1315–1325, [doi:10.1016/j.physa.2010.12.008](https://doi.org/10.1016/j.physa.2010.12.008)"
)
GOTTWALD_MELBOURNE_2004 = Source(
    "Gottwald, G. A., Melbourne, I.: *A new test for chaos in deterministic systems*. Proceedings of the Royal "
    "Society A 460 (2004), 603–611, [doi:10.1098/rspa.2003.1183](https://doi.org/10.1098/rspa.2003.1183), "
    "[arXiv:nlin/0208033](https://arxiv.org/abs/nlin/0208033)"
)
GOTTWALD_MELBOURNE_COMMENT_2008 = Source(
    "Gottwald, G. A., Melbourne, I.: *Comment on „Reliability of the 0-1 test for chaos“*. Physical Review E 77 "
    "(2008), 028201, [doi:10.1103/PhysRevE.77.028201](https://doi.org/10.1103/PhysRevE.77.028201)"
)
GOTTWALD_MELBOURNE_REVIEW_2016 = Source(
    "Gottwald, G. A., Melbourne, I.: *The 0-1 test for chaos: a review*. In: Skokos, Ch., Gottwald, G. A., "
    "Laskar, J. (ed.): Chaos Detection and Predictability, Lecture Notes in Physics 915, Springer 2016, 221–247, "
    "[doi:10.1007/978-3-662-48410-4_7](https://doi.org/10.1007/978-3-662-48410-4_7)"
)
HU_2005 = Source(
    "Hu, J., Tung, W.-W., Gao, J., Cao, Y.: *Reliability of the 0-1 test for chaos*. Physical Review E 72 (2005), "
    "056207, [doi:10.1103/PhysRevE.72.056207](https://doi.org/10.1103/PhysRevE.72.056207)"
)
DE_LIMA_1996 = Source(
    "de Lima, P. J. F.: *Nuisance parameter free properties of correlation integral based statistics*. "
    "Econometric Reviews 15 (1996), 237–259, "
    "[doi:10.1080/07474939608800354](https://doi.org/10.1080/07474939608800354)"
)
MARTINOVIC_2018 = Source(
    "Martinovič, T.: *Tools for time series analysis of nonlinear dynamical systems*. Disertační práce, VŠB – "
    "Technická univerzita Ostrava 2018, anglicky s českým abstraktem, "
    "[DSpace VŠB-TUO](http://hdl.handle.net/10084/133997)"
)
TOMCALA_2021 = Source(
    "Tomčala, J.: *Real time series analysis in terms of predictability, entropy and chaos*. Disertační práce, "
    "VŠB – Technická univerzita Ostrava 2021, anglicky s českým abstraktem, "
    "[DSpace VŠB-TUO](http://hdl.handle.net/10084/145410)"
)
KODERA_TRAN_2009 = Source(
    "Kodera, J., Tran Van Quang: *Vizuální nelineární rekurentní analýza a její aplikace na český akciový trh*. "
    "Politická ekonomie 57 (2009), č. 3, 305–322, [doi:10.18267/j.polek.686](https://doi.org/10.18267/j.polek.686), "
    "[PDF](https://polek.vse.cz/pdfs/pol/2009/03/02.pdf)",
    czech=True,
)
ORLANDO_LAMPART_2023 = Source(
    "Orlando, G., Lampart, M.: *Expecting the unexpected: entropy and multifractal systems in finance*. Entropy 25 "
    "(2023), 1527, [doi:10.3390/e25111527](https://doi.org/10.3390/e25111527)"
)

LEAD = (
    "Vlastní výzkumný námět, ne doložený výsledek: místo otázky „je GBS rychlejší než Monte Carlo?“ se ptát, kdy "
    "odhad finančního rizika přes Gaussian Boson Sampler selže a jestli se to dá poznat z dat předem. U každého "
    "tvrzení je vidět, jestli je doložené literaturou, spočítané v aplikaci, nebo je to náš návrh."
)

IN_SHORT = (
    "Odhad rizika přes GBS může selhat třemi různými způsoby: data nejsou gaussovská, takže je chybné samo "
    "zadání; zadání sedí, ale pro danou matici a portfolio GBS nemá výhodu; nebo je matice odhadnutá z krátké "
    "historie a nese šum. Každý zdroj chyby se jinak pozná z dat – testy nelinearity a entropie, spektrem "
    "matice spolu s vahami portfolia a poměrem q = N/T – a jinak se opravuje."
)


def failure_sources_table() -> str:
    return "\n".join([
        "| zdroj chyby | co je špatně | diagnostika z dat, předem | kde je rozbor |",
        "|---|---|---|---|",
        "| 1. data nejsou gaussovská | zadání: gaussovský integrál neodpovídá datům, stejně pro GBS i Monte Carlo "
        "| test BDS, entropie, rekurentní analýza, 0-1 test chaosu | kapitoly 2 a 3 |",
        "| 2. GBS nemá výhodu | odhad: pro danou matici a portfolio potřebuje GBS víc vzorků | spektrum matice "
        "a poloha vah vůči hlavním vlastním vektorům | kapitola 4 |",
        "| 3. šum ve vstupu | vstup: matice odhadnutá z krátké historie | poměr q = N/T, spektrum proti "
        "Marčenkovu–Pasturovu rozdělení | kapitola 5 |",
    ])


WHY_ASK = TheoryTopic(
    anchor="ds-proc",
    title="Proč se ptát, kdy GBS selže",
    in_short=(
        "Otázka „je GBS rychlejší?“ má kladnou odpověď jen pro část úloh. Otázka „kdy odhad selže a jak to poznat "
        "předem?“ dává smysl i tehdy, když výhoda nevyjde (náš výklad)."
    ),
    explanation=r"""
**Co je doložené.** Andersen a Shan dokazují, že jejich odhady z výstřelů GBS potřebují exponenciálně méně
vzorků než Monte Carlo na otevřené neprázdné podmnožině gaussovských úloh – ne na všech; srovnávají přitom
zaručené počty vzorků, ne čas. V navazujícím článku odhadují, pro jaký podíl úloh to platí. Oh a kol. (2024) navíc ukázali, že experimenty GBS se ztrátami
fotonů jde simulovat klasicky. Výhoda tedy není samozřejmá ani v teorii, ani na hardwaru.

**Náš návrh.** Místo jediného čísla „o kolik je GBS rychlejší“ rozlišit, *proč* odhad rizika přes GBS selže,
a pro každou příčinu najít ukazatel, který jde spočítat z dat dřív, než se přístroj spustí. Navrhujeme tři
zdroje chyby z tabulky nahoře. Každý se jinak pozná a jinak opravuje. Kdo je nerozliší, snadno připíše GBS
chybu gaussovského modelu nebo šumu v datech – a oponent se na to zeptá.

**Proč má otázka smysl i při neúspěchu.** Mapa „kde GBS nepomůže a proč“ je pro uživatele stejně užitečná jako
mapa, kde pomůže. Výsledek tedy nestojí na tom, že kvantová výhoda vyjde.
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "odhady GBS-P a GBS-I a pro jaké úlohy je výhoda dokázaná"),
        Reading(ANDERSEN_SHAN_ADVANTAGE, "pro jaký podíl úloh mají GBS-P a GBS-I výhodu"),
        Reading(OH_CLASSICAL_SIMULATION, "klasická simulace skutečných experimentů GBS"),
    ),
)

MODEL_SOURCE = TheoryTopic(
    anchor="ds-data",
    title="Zdroj 1: data nejsou gaussovská",
    in_short=(
        "Odhady Andersena a Shan počítají integrály proti gaussovskému rozdělení. Skutečné výnosy mají těžké "
        "chvosty a shlukování volatility. Na takových datech je chybné samo zadání – pro GBS stejně jako pro "
        "gaussovské Monte Carlo."
    ),
    explanation=r"""
**Co počítá GBS.** Andersen a Shan řeší gaussovské úlohy: střední hodnotu funkce náhodného vektoru s normálním
rozdělením. Klasické Monte Carlo, se kterým GBS srovnává stránka „Monte Carlo na GBS“, dělá totéž losováním. Obě metody
tedy odhadují číslo, které platí, *pokud* jsou výnosy gaussovské.

**Co ukazují data.** Cont (2001) shrnuje tzv. stylizovaná fakta – vlastnosti výnosů, které se opakují napříč
trhy a obdobími – Cont jich uvádí jedenáct. Patří mezi ně nevýznamná (lineární) autokorelace výnosů, těžké
chvosty, shlukování volatility (po velkých pohybech přicházejí velké pohyby), pomalé slábnutí autokorelace
absolutních výnosů a podmíněně těžké chvosty: chvosty zůstanou těžké, i když se výnosy očistí od shlukování
volatility například modelem GARCH. Gaussovský model s pevnou maticí nevystihne ani jedno z posledních čtyř.

**Důsledek (náš výklad).** Když se odhad rizika přes GBS na reálných datech netrefí, nemusí jít o chybu GBS:
stejně by se netrefil gaussovský model spočítaný přesně. Výzkum proto musí nejdřív změřit chybu modelu
(přesný gaussovský výsledek proti tomu, co se skutečně stalo) a teprve zbytek přičítat odhadu.

**Co s tím (náš návrh).** Gaussovský model jde používat tam a tehdy, kdy data od gaussovského chování výrazně
neodbíhají – a to je potřeba umět poznat předem. To je úkol diagnostiky v další kapitole.
""",
    further_reading=(
        Reading(CONT_2001, "stylizovaná fakta výnosů: proč nejsou gaussovské"),
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "gaussovské úlohy, které GBS řeší"),
    ),
    related_caveats=(TAIL_RISK,),
)

DIAGNOSTIC_TOOLS = TheoryTopic(
    anchor="ds-nastroje",
    title="Diagnostika zdroje 1: nelinearita, entropie, rekurence a 0-1 test",
    in_short=(
        "Nástroje z nelineární dynamiky a teorie chaosu měří, jak moc se řada liší od nezávislého šumu a jak se to "
        "mění v čase. Jako předpovědní modely cen doložené nejsou, jako diagnostika struktury dat se používají – "
        "s výjimkou 0-1 testu, který na zašuměných datech zaměňuje šum za chaos."
    ),
    explanation=r"""
**Test BDS** (Brock, Dechert, Scheinkman a LeBaron 1996) testuje, jestli jsou data nezávislá a stejně
rozdělená. Dá se použít i na rezidua odhadnutého modelu: co v nich zbude, je závislost, kterou model nevystihl.
U modelů s proměnlivou volatilitou (typu GARCH) to ale platí jen za dalších podmínek, které rozebírá de Lima
(1996).

**Entropie** měří, jak pravidelná a předvídatelná řada je: nízká hodnota znamená opakující se vzory, vysoká
blízkost náhodě. Aproximativní (přibližnou) entropii zavedl Pincus (1991), vzorkovou entropii Richman a Moorman
(2000) a permutační entropii, která porovnává jen pořadí hodnot, Bandt a Pompe (2002). Zunino a kol. (2009)
ukázali, že méně efektivní akciové trhy mají nižší permutační entropii a víc chybějících („zakázaných“) vzorů
pořadí. Orlando a Lampart (2023) na indexu NYSE zjistili, že poklesy cen entropii *zvyšují*: medvědí trhy tak
nesou větší šanci na nečekané extrémní události.

**Kvantitativní rekurentní analýza (RQA)** vychází z rekurentního diagramu (Eckmann, Oliffson Kamphorst a Ruelle
1987), který zaznamená, kdy se stav systému vrací do blízkosti dřívějšího stavu. Z diagramu se počítají míry jako
podíl rekurencí, determinismus (podíl rekurencí v diagonálních úsečkách) nebo laminarita (ve svislých
úsečkách); přehled je v článku Marwana a kol. (2007). Bastos a Caiado (2011) ji počítali v klouzavém okně na
akciových indexech: během krizí (technologická bublina, asijská krize, hypoteční krize) podíl rekurencí
v diagonálních a svislých strukturách dočasně klesl. Česky ji na index PX aplikovali Kodera a Tran Van Quang
(2009).

**0-1 test chaosu** (Gottwald a Melbourne 2004) dá z jedné časové řady číslo $K$ blízko 0 pro pravidelnou a blízko
1 pro chaotickou dynamiku. Je ale navržený pro deterministické systémy. Hu a kol. (2005) ukázali, že šum typu
$1/f^\alpha$ vyhodnotí jako chaos; autoři testu odpověděli, že použít ho na náhodná data je chyba, protože je
určený pro deterministické, nanejvýš mírně zašuměné systémy (Gottwald a Melbourne 2008). Ve svém přehledu (2016)
dodávají, že u dostatečně dlouhých zašuměných dat vyjde $K = 1$ bez ohledu na skutečnou dynamiku. Výnosy akcií mají velkou náhodnou
složku, takže $K$ blízko 1 u nich o chaosu nic neříká – 0-1 test je tu nanejvýš pomocný ukazatel (náš závěr).

**Implementace.** Paralelní RQA a 0-1 test zpracoval ve své disertaci Martinovič (2018), rychlé varianty
přibližné a vzorkové entropie Tomčala (2021, balík TSEntropies; jeho rychlé varianty nedávají přesně stejné
hodnoty jako původní metody). Obě práce vznikly na VŠB-TUO.

**Jak z toho udělat diagnostiku (náš návrh).** Ukazatele počítat v klouzavém okně, ze kterého se odhaduje
i matice, a testovat, jestli jejich hodnota předem signalizuje, že gaussovský odhad rizika v dalším období
selže. Háček (náš odhad): entropie i RQA potřebují dost dlouhá okna, kdežto proměnlivost trhu žene
k oknům krátkým.
""",
    further_reading=(
        Reading(BDS_1996, "test nezávislosti a stejného rozdělení, i pro rezidua modelů"),
        Reading(DE_LIMA_1996, "kdy jde test BDS použít na rezidua"),
        Reading(PINCUS_1991, "aproximativní entropie"),
        Reading(RICHMAN_MOORMAN_2000, "vzorková entropie"),
        Reading(BANDT_POMPE_2002, "permutační entropie"),
        Reading(ZUNINO_2009, "permutační entropie a efektivita akciových trhů"),
        Reading(ORLANDO_LAMPART_2023, "entropie a multifraktály ve financích"),
        Reading(ECKMANN_KAMPHORST_RUELLE, "rekurentní diagram"),
        Reading(MARWAN_2007, "přehled rekurentní analýzy a jejích měr"),
        Reading(BASTOS_CAIADO_2011, "rekurentní analýza akciových indexů v krizích"),
        Reading(KODERA_TRAN_2009, "česky: rekurentní analýza indexu PX"),
        Reading(GOTTWALD_MELBOURNE_2004, "0-1 test chaosu"),
        Reading(HU_2005, "0-1 test vyhodnotí šum 1/f jako chaos"),
        Reading(GOTTWALD_MELBOURNE_COMMENT_2008, "odpověď autorů: test není pro náhodná data"),
        Reading(GOTTWALD_MELBOURNE_REVIEW_2016, "přehled 0-1 testu včetně vlivu šumu"),
        Reading(MARTINOVIC_2018, "paralelní RQA a 0-1 test"),
        Reading(TOMCALA_2021, "rychlý výpočet entropií"),
    ),
)


def _estimator_findings() -> str:
    aligned = saving(EQUAL_SAVINGS, 0.9, 4).sample_saving
    weak = saving(EQUAL_SAVINGS, 0.02, 4).sample_saving
    hedged = saving(LONG_SHORT_SAVINGS, 0.25, LONG_SHORT_DEGREE).sample_saving
    return (
        "**Co jsme spočítali (6 aktiv, moment 4. stupně).** Pro portfolio ve směru tržního módu GBS při silné "
        f"korelaci ušetří {saving_label(aligned)} vzorků, při slabé korelaci ρ = 0,02 je ale horší než Monte Carlo "
        f"({saving_label(weak)}). Portfolio long–short, kolmé na tržní mód, potřebuje při ρ = 0,25 "
        f"{times_more_samples(hedged)}× víc vzorků než Monte Carlo.\n"
    )


ESTIMATOR_SOURCE = TheoryTopic(
    anchor="ds-vyhoda",
    title="Zdroj 2: zadání sedí, ale GBS nepomůže",
    in_short=(
        "I pro gaussovská data záleží úspora vzorků na matici a na úloze. Náš výpočet ukazuje, že rozhoduje spektrum "
        "spolu s polohou vah portfolia – a obojí jde spočítat předem."
    ),
    explanation=r"""
**Co je doložené.** Výhoda platí jen pro část úloh; u odhadu GBS-P její podíl podle Andersena a Shan klesá
s rozměrem úlohy a roste se stupněm. Hranici, za kterou už GBS nejde
klasicky simulovat, posunuli Bulmer a kol. (2022) i Oh a kol. (2024); úsporu vzorků je proto potřeba porovnat
i s cenou klasické simulace.

""" + _estimator_findings() + r"""
**Diagnostika (náš návrh).** Spektrum matice a podíl rozptylu portfolia, který leží v silně stlačených módech –
tedy v hlavních vlastních vektorech. Obojí jde spočítat bez spuštění přístroje i bez výpočtu hafniánů. Jestli
to stačí jako obecný ukazatel, je otevřená otázka na podstránce.
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_ADVANTAGE, "pro jaký podíl úloh mají GBS-P a GBS-I výhodu"),
        Reading(BULMER_BOUNDARY, "hranice klasické simulace GBS"),
    ),
    related_caveats=(CLASSICAL_SIMULATION,),
)


def _input_example() -> str:
    return (
        f"**Příklad (náš dopočet).** Při q = {czech_decimal(NOISE_EXAMPLE_RATIO, 1)} slibuje portfolio "
        "optimalizované na odhadnuté matici poloviční rozptyl, než je vůbec možný, a nese dvojnásobný. Moment "
        f"{NOISE_EXAMPLE_DEGREE}. stupně pak vyjde {czech_decimal(1 / NOISE_EXAMPLE_MOMENT_RATIO, 0)}× menší "
        "než skutečný – a GBS by to chybné číslo spočítal velmi přesně.\n"
    )


INPUT_SOURCE = TheoryTopic(
    anchor="ds-vstup",
    title="Zdroj 3: matice je odhadnutá z krátké historie",
    in_short=(
        "Korelační matice N akcií z T dní nese šum a teorie náhodných matic ho umí změřit. Diagnostikou je poměr "
        "q = N/T a spektrum proti Marčenkovu–Pasturovu rozdělení; lékem je matici před zakódováním vyčistit."
    ),
    explanation=r"""
**Co je doložené.** Laloux a kol. (1999) ukázali, že většina vlastních čísel korelační matice akcií leží
v pásu čistého šumu. Pro portfolio optimalizované na takové matici uvádějí Bouchaud a Potters slíbený rozptyl
$(1-q)$ a skutečný $1/(1-q)$ krát optimum.

""" + _input_example() + r"""
**Diagnostika.** Poměr $q = N/T$ a počet vlastních čísel nad horní mezí Marčenkova–Pasturova rozdělení –
oboje jde spočítat přímo z dat. Lékem je čištění matice (ořezání, shrinkage, rotačně invariantní estimátory),
klasický krok, který GBS nenahradí.
""",
    further_reading=(
        Reading(LALOUX_1999, "většina spektra korelační matice je šum"),
        Reading(BOUCHAUD_POTTERS_REVIEW, "slíbené a skutečné riziko"),
        Reading(BUN_BOUCHAUD_POTTERS, "jak matici vyčistit"),
    ),
)

VERIFICATION_PLAN = TheoryTopic(
    anchor="ds-navrh",
    title="Jak by se to dalo ověřit",
    in_short=(
        "V klouzavých oknech spočítat diagnostiky všech tří zdrojů, odhadnout riziko gaussovským modelem přesně "
        "i přes GBS a otestovat, jestli diagnostiky předem ukážou, kdy odhad selže (náš návrh)."
    ),
    explanation=r"""
1. **Data.** Denní výnosy $N$ akcií; klouzavá okna délky $T$ a za každým oknem následující období.
2. **Diagnostiky z okna.** Zdroj 1: test BDS na reziduích, entropie, RQA. Zdroj 2: spektrum
   a poloha vah vůči hlavním vlastním vektorům. Zdroj 3: $q$ a počet vlastních čísel nad pásem šumu.
3. **Chyby v následujícím období, každá zvlášť.** Chyba modelu: přesný gaussovský výsledek proti tomu, co se
   stalo. Chyba odhadu: rozptyl GBS proti Monte Carlu při stejném počtu vzorků (v emulaci). Chyba vstupu:
   surová proti vyčištěné matici.
4. **Test.** Předpovídají diagnostiky z okna velikost chyby lépe než jednoduchá srovnávací pravidla, třeba
   samotná volatilita okna?
5. **Výsledek i při neúspěchu.** Když diagnostiky chybu nepředpovídají, je to také zjištění: selhání odhadu pak
   nejde poznat předem a je potřeba jiný přístup.

**Háčky.** VaR a CVaR nejsou polynomy, takže odhad ze stránky „Monte Carlo na GBS“ na ně přímo nestačí. Emulace GBS
zvládne jen malý počet módů a hranice klasické simulace se posouvá. A diagnostiky zdroje 1 potřebují delší okna než
odhad matice (náš odhad).
""",
    further_reading=(
        Reading(BUN_BOUCHAUD_POTTERS, "jak porovnávat estimátory na skutečných datech mimo vzorek"),
        Reading(CONT_2001, "co musí model výnosů vystihnout"),
    ),
    related_caveats=(TAIL_RISK, CLASSICAL_SIMULATION),
)

TOPICS: Tuple[TheoryTopic, ...] = (
    WHY_ASK,
    MODEL_SOURCE,
    DIAGNOSTIC_TOOLS,
    ESTIMATOR_SOURCE,
    INPUT_SOURCE,
    VERIFICATION_PLAN,
)
