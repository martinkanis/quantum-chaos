"""Texts of the literature review page: GBS as a replacement of Monte Carlo for financial risk.

Only the public part of the review is published here; the internal notes on the direction of the thesis stay out.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from ui.advantage_content import (
    ANAND_POLYNOMIAL_SIMULATION,
    ANGUITA_MONTE_CARLO_ACCELERATOR,
    DANISH_QUANTUM_USE_CASES_PAGE,
    QPURPOSE_FINANCE,
    ZHANG_GBS_MCMC,
)
from ui.guide_practice import STRAWBERRY_FIELDS
from ui.theory_content import (
    ANDERSEN_SHAN_ADVANTAGE,
    ANDERSEN_SHAN_EXPECTATIONS,
    ARRAZOLA_BROMLEY,
    ARRAZOLA_REBENTROST_WEEDBROOK,
    DANISH_QUANTUM_USE_CASES,
    GLASSERMAN,
    HAMILTON,
    MADSEN,
    OH_CLASSICAL_SIMULATION,
    SDU_QUANTUM_FINANCE,
    WALRUS_HAFNIAN,
    ZHONG,
    Reading,
    Source,
    TheoryTopic,
)

TITLE = "Rešerše: Gaussian Boson Sampling pro odhad finančního rizika"
REVIEW_DATE = "23. 9. 2026"
SOURCES_CHECKED_DATE = "15. 10. 2026"
SOURCES_ANCHOR = "reserse-zdroje"

INTRO = (
    "Shrnutí rešerše literatury, patentů, projektů a hardwaru k jedné otázce: může fotonický Gaussian Boson "
    f"Sampler (GBS) nahradit Monte Carlo při odhadu finančního rizika? Rešerše je ze dne {REVIEW_DATE}, zdroje byly "
    f"znovu ověřeny {SOURCES_CHECKED_DATE}. Začni krátkým TL;DR, podrobnosti jsou v kapitolách a každé tvrzení má "
    "zdroj; kde jde o náš výklad, je to výslovně napsané."
)


@dataclass(frozen=True)
class KeyFinding:
    """One point of the TL;DR; the anchor leads to the chapter that explains it."""

    text: str
    anchor: str


@dataclass(frozen=True)
class ReviewQuestion:
    question: str
    answer: str
    anchor: str
    """Chapter where the answer is explained."""


SDU_QPURPOSE_SPINOUT = Source(
    "Centre for Quantum Mathematics, SDU: [Qpurpose: a Spin-off from QM]"
    "(https://www.sdu.dk/en/forskning/qm/research/quantum-computing/qpurpose) – spin-off založený v roce 2022"
)
SDU_QM_PROJECTS = Source(
    "Centre for Quantum Mathematics, SDU: [About QM](https://www.sdu.dk/en/forskning/qm/about-qm) – projekty "
    "centra včetně GBS2EXP"
)
REBENTROST_GUPT_BROMLEY = Source(
    "Rebentrost, P., Gupt, B., Bromley, T. R.: *Photonic quantum algorithm for Monte Carlo integration*, "
    "[arXiv:1809.02579](https://arxiv.org/abs/1809.02579) (2018)"
)
WOERNER_EGGER = Source(
    "Woerner, S., Egger, D. J.: *Quantum risk analysis*. npj Quantum Information 5, 15 (2019), "
    "[doi:10.1038/s41534-019-0130-6](https://doi.org/10.1038/s41534-019-0130-6)"
)
STAMATOPOULOS = Source(
    "Stamatopoulos, N. a kol.: *Option Pricing using Quantum Computers*. Quantum 4, 291 (2020), "
    "[doi:10.22331/q-2020-07-06-291](https://doi.org/10.22331/q-2020-07-06-291)"
)
EGGER_CREDIT_RISK = Source(
    "Egger, D. J., García Gutiérrez, R., Cahué Mestre, J., Woerner, S.: *Credit Risk Analysis Using Quantum "
    "Computers*. IEEE Transactions on Computers 70 (2021), 2136–2145, "
    "[doi:10.1109/TC.2020.3038063](https://doi.org/10.1109/TC.2020.3038063)"
)
CHAKRABARTI = Source(
    "Chakrabarti, S., Krishnakumar, R., Mazzola, G., Stamatopoulos, N., Woerner, S., Zeng, W. J.: *A Threshold "
    "for Quantum Advantage in Derivative Pricing*. Quantum 5, 463 (2021), "
    "[doi:10.22331/q-2021-06-01-463](https://doi.org/10.22331/q-2021-06-01-463)"
)
QI_NOISY_SIMULABILITY = Source(
    "Qi, H., Brod, D. J., Quesada, N., García-Patrón, R.: *Regimes of classical simulability for noisy Gaussian "
    "boson sampling*. Physical Review Letters 124, 100502 (2020), "
    "[doi:10.1103/PhysRevLett.124.100502](https://doi.org/10.1103/PhysRevLett.124.100502)"
)
BULMER_BOUNDARY = Source(
    "Bulmer, J. F. F. a kol.: *The boundary for quantum advantage in Gaussian boson sampling*. Science Advances 8, "
    "eabl9236 (2022), [doi:10.1126/sciadv.abl9236](https://doi.org/10.1126/sciadv.abl9236)"
)
OH_QUANTUM_INSPIRED = Source(
    "Oh, C., Fefferman, B., Jiang, L., Quesada, N.: *Quantum-inspired classical algorithm for graph problems by "
    "Gaussian boson sampling*. PRX Quantum 5, 020341 (2024), "
    "[doi:10.1103/PRXQuantum.5.020341](https://doi.org/10.1103/PRXQuantum.5.020341)"
)
JIUZHANG_4 = Source(
    "Liu, H.-L. a kol.: *Gaussian boson sampling with 1,024 squeezed states in 8,176 modes*. Nature 653, 687–692 "
    "(2026), [doi:10.1038/s41586-026-10523-6](https://doi.org/10.1038/s41586-026-10523-6)"
)
EUROHPC_LUCY = Source(
    "EuroHPC JU: [EuroHPC JU inaugurates quantum computer in France](https://www.eurohpc-ju.europa.eu/"
    "eurohpc-ju-inaugurates-quantum-computer-france-strengthening-europes-sovereignty-2026-04-14_en), 14. 4. 2026"
)
EUROHPC_QUANTUM_ACCESS = Source(
    "EuroHPC JU: [EuroHPC JU opens access to its quantum computers](https://www.eurohpc-ju.europa.eu/"
    "eurohpc-ju-opens-access-its-quantum-computers-2026-06-25_en), 25. 6. 2026"
)
ORCA_PT1 = Source(
    "ORCA Computing: [PT-1](https://orcacomputing.com/orca-pt-1/) – programovatelný boson sampler s časovými biny"
)
PERCEVAL = Source(
    "Quandela: [Perceval](https://perceval.quandela.net) – otevřený framework pro programování fotonických "
    "kvantových počítačů"
)
PIQUASSO = Source("[Piquasso](https://piquasso.com) – simulátor fotonických kvantových počítačů v Pythonu a C++")
TWENTE_PATENT = Source(
    "Renema, J. J., Roelink, T. I., Correa Anguita, M. (Universiteit Twente): *Monte Carlo integration using an "
    "optical quantum computer*, přihláška WO2024225891A1, zveřejněná 31. 10. 2024, "
    "[Google Patents](https://patents.google.com/patent/WO2024225891A1/en)"
)
XANADU_GBS_PATENT = Source(
    "Xanadu Quantum Technologies: *Apparatus and methods for Gaussian boson sampling*, patent US11593699B2, "
    "udělený 28. 2. 2023, [Google Patents](https://patents.google.com/patent/US11593699B2/en)"
)
HE_GRAPH_FINANCE = Source(
    "He, S. a kol.: *Time-domain-multiplexed Gaussian Boson sampling for graph problems in finance*. Chip 5, "
    "100181 (2026), [doi:10.1016/j.chip.2025.100181](https://doi.org/10.1016/j.chip.2025.100181)"
)
GRODZKI_PORTFOLIO = Source(
    "Grodzki, Ł., Słysz, M., Waligóra, G.: *Solving the Portfolio Optimization Problem on a Photonic Quantum "
    "Computer*. Entropy 28, 717 (2026), [doi:10.3390/e28070717](https://doi.org/10.3390/e28070717)"
)
CIMINI_RESERVOIR = Source(
    "Cimini, V. a kol.: *Large-scale quantum reservoir computing using a Gaussian Boson Sampler*. npj Quantum "
    "Information 12, 104 (2026), [doi:10.1038/s41534-026-01251-w](https://doi.org/10.1038/s41534-026-01251-w)"
)
CONT_STYLIZED_FACTS = Source(
    "Cont, R.: *Empirical properties of asset returns: stylized facts and statistical issues*. Quantitative "
    "Finance 1 (2001), 223–236"
)

CLAIMS_TOPIC = TheoryTopic(
    anchor="reserse-jyske-bank",
    title="Případ Jyske Bank a Qpurpose: co se skutečně nasadilo",
    in_short=(
        "Dánská firma Qpurpose dodává Jyske Bank software pro obchodování postavený na „kvantové matematice“. "
        "Podle veřejných zdrojů ale algoritmy zatím běží na klasických superpočítačích, které kvantový počítač "
        "emulují – dosavadní přínos tedy nevznikl na kvantovém hardwaru."
    ),
    explanation=r"""
**Odkud případ známe.** Přehled *16 Danish Quantum Use Cases* (prosinec 2024) popisuje na straně 44 případ 16,
*Quantum-Optimised Real-Time Trading*: poskytovatelem je Qpurpose, uživatelem Jyske Bank. Qpurpose je spin-off
Centra kvantové matematiky (QM) na University of Southern Denmark založený v roce 2022; teorii vyvíjí ředitel
centra J. E. Andersen se Shan Shan.

**Co se tvrdí.** Podle brožury dává GBS výrazné zrychlení oproti vzorkování Monte Carlem a „v určitých
případech“ exponenciální zrychlení oproti tradičním metodám – bez čísel, srovnání nebo odkazu na článek. Dále
uvádí krátkodobé předpovědi s přesností na několik bazických bodů, každodenní používání obchodníky a vyšší
výnosy z obchodování. Stránka SDU popisuje krátkodobé předpovědi pro vybrané třídy akcií a software podložený
simulacemi na HPC, který denně běží na obchodním stole banky. Žádné z těchto čísel nejde z veřejných zdrojů ověřit.

**Co se skutečně nasadilo.** Brožura říká, že algoritmy zatím běží na klasickém HPC, které kvantový počítač
emuluje, a na skutečné kvantové počítače se přesunou, až budou k dispozici. Nástroje podle ní kombinují
„skutečně kvantové“ a kvantově inspirované algoritmy.

**Proč na tom záleží (náš výklad).** Pro výzkum je to dobrá zpráva: metodu jde studovat, reprodukovat a porovnávat
s klasickým Monte Carlem hned, bez čekání na kvantový počítač. Zároveň z případu Jyske Bank zatím nejde nic
vyvozovat o výhodě skutečného kvantového hardwaru.
""",
    further_reading=(
        Reading(DANISH_QUANTUM_USE_CASES, "případ 16: Jyske Bank a Qpurpose"),
        Reading(DANISH_QUANTUM_USE_CASES_PAGE, "jen strana s případem"),
        Reading(SDU_QUANTUM_FINANCE, "spolupráce QM, Jyske Bank a Qpurpose"),
        Reading(SDU_QPURPOSE_SPINOUT, "vznik firmy"),
        Reading(QPURPOSE_FINANCE),
    ),
)

THEORY_TOPIC = TheoryTopic(
    anchor="reserse-teorie",
    title="Teorie: GBS jako odhad gaussovských integrálů",
    in_short=(
        "Výstupní pravděpodobnosti GBS jsou hafniány a gaussovské momenty jsou také hafniány. Andersen a Shan z toho "
        "postavili dva estimátory a dokázali, že na části úloh potřebují exponenciálně méně vzorků než obyčejné "
        "Monte Carlo – ne na všech úlohách a ne v čase. Obě jejich práce jsou zatím preprinty."
    ),
    explanation=r"""
**Myšlenka.** Hamilton a kol. (2017) ukázali, že pravděpodobnost naměřeného vzoru fotonů v GBS je dána hafniánem
matice, kterou přístroj „nese“. Gaussovské momenty – očekávané hodnoty součinů gaussovských veličin – jsou podle
Wickovy–Isserlisovy věty také hafniány. Arrazola, Rebentrost a Weedbrook (2017) proto navrhli používat vzorky
z GBS k výpočtu vysokorozměrných gaussovských integrálů. Rebentrost, Gupt a Bromley (2018) navrhli jiný,
spojitě-proměnný fotonický algoritmus pro Monte Carlo integraci s kvadratickým zrychlením.

**Co dokázali Andersen a Shan (2025).** Navrhli dva estimátory gaussovské očekávané hodnoty
$\mathbb{E}[f(X)]$, $X \sim \mathcal{N}(0, \Sigma)$, ze vzorků GBS a dokázali, že na *otevřené neprázdné
podmnožině* úloh potřebují exponenciálně méně vzorků než prosté Monte Carlo. Výhoda je definovaná přes
garantovanou velikost vzorku pro danou relativní přesnost $\varepsilon$ a pravděpodobnost úspěchu $\delta$.
Navazující práce ladí střední počet fotonů podle konkrétní úlohy a odhaduje, jak velká část prostoru úloh má
výhodu: podle autorů podstatná, v některých speciálních případech téměř celý prostor. K 15. 10. 2026 jsou obě
práce jen na arXivu, bez recenzního řízení v časopise.

**Na SDU pokračují.** Projekt GBS2EXP (DeiC Quantum Postdoc Fellowship, 2024–2027) chce s dnešními šumovými
a ztrátovými přístroji GBS odhadovat vysokorozměrné gaussovsky vážené integrály efektivněji než Monte Carlo
a míří na první průmyslové použití ve financích.

**Co z toho neplyne.** Výsledky se týkají počtu vzorků, ne času ani ceny výpočtu, a gaussovských úloh, ne
reálných finančních dat. Otázku, které konkrétní ukazatele rizika (VaR, CVaR, zajištění s reálnými výnosy) do
výhodné podmnožiny spadají, jsme v prošlé literatuře zodpovězenou nenašli – viz Otevřené otázky.
""",
    further_reading=(
        Reading(HAMILTON, "výstupní pravděpodobnosti GBS a hafnián"),
        Reading(ARRAZOLA_REBENTROST_WEEDBROOK, "první návrh GBS jako integrátoru"),
        Reading(REBENTROST_GUPT_BROMLEY, "spojitě-proměnný fotonický algoritmus pro Monte Carlo"),
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "dva estimátory a důkaz výhody na části úloh"),
        Reading(ANDERSEN_SHAN_ADVANTAGE, "jak velká část úloh má výhodu a ladění počtu fotonů"),
        Reading(SDU_QM_PROJECTS, "projekt GBS2EXP"),
    ),
)

TWENTE_TOPIC = TheoryTopic(
    anchor="reserse-twente",
    title="Konkurenční linie: Univerzita Twente",
    in_short=(
        "Skupina Jelmera Renemy z Univerzity Twente předvedla boson sampling jako hardwarový akcelerátor Monte Carla "
        "na fotonickém čipu. Používá jednotlivé fotony, ne GBS, metodu ukázala na fyzikálním integrálu a podala "
        "k ní patentovou přihlášku."
    ),
    explanation=r"""
**Co udělali.** Correa Anguita a kol. (2025) používají vážení vzorků (importance sampling): integrand rozloží na
rozdělení pravděpodobnosti, ze kterého vzorkuje fotonický přístroj, a funkci, kterou pro každý vzorek spočítá
klasický počítač. Popisují také, za jakých podmínek si úloha zachová výpočetní těžkost.

**Na čem.** Programovatelný dvanáctimódový interferometr na čipu z nitridu křemíku, tři fotony a supravodivé
detektory. Jde o boson sampling s jednotlivými fotony, ne o Gaussian Boson Sampling. Testovací úlohou je
fyzikální integrál – oprava energie tří bosonů v harmonické pasti –, ne finanční úloha. Kvantovou výhodu pro
určité třídy integrálů autoři zdůvodňují, ale neukazují; práce je zatím preprint.

**Čím se liší od SDU (náš výklad).** Andersen a Shan dokazují výhodu GBS teoreticky a publikují otevřeně; skupina
z Twente ukazuje experiment na skutečném hardwaru s jiným typem boson samplingu a metodu chrání patentovou
přihláškou (viz kapitola Patenty). Vlastní výzkum by měl obě linie citovat a jasně se od nich vymezit.
""",
    further_reading=(Reading(ANGUITA_MONTE_CARLO_ACCELERATOR, "experiment na fotonickém čipu"),),
)

GATE_BASED_TOPIC = TheoryTopic(
    anchor="reserse-amplitudova-estimace",
    title="Druhá cesta: kvantové Monte Carlo na hradlových počítačích",
    in_short=(
        "Kvantová amplitudová estimace slibuje až kvadratické zrychlení odhadu VaR, CVaR i cen opcí, potřebuje ale "
        "chybově korigované qubity – pro výhodu v oceňování derivátů asi 8 tisíc logických qubitů, které zatím "
        "nikdo nemá."
    ),
    explanation=r"""
**Princip.** Klasické Monte Carlo má chybu úměrnou $1/\sqrt{N}$, kde $N$ je počet vzorků. Kvantová amplitudová
estimace odhaduje tutéž střední hodnotu s chybou úměrnou až $1/N$ dotazů na kvantový obvod – k desetkrát vyšší
přesnosti tedy potřebuje desetkrát, ne stokrát víc práce. Woerner a Egger (2019) takto odhadovali VaR a CVaR:
s nejmělčími obvody klesá chyba jako $N^{-2/3}$, s hlubšími se blíží $N^{-1}$ – zrychlení je tedy „téměř
kvadratické“. Stejný princip použili Stamatopoulos a kol. (2020) pro opce a Egger a kol. (2021) pro kreditní
riziko.

**Háček.** Obvody jsou hluboké a bez opravy chyb je šum zničí. Chakrabarti a kol. (2021) spočítali, co by výhoda
v oceňování derivátů potřebovala: asi 8 tisíc logických (chybově korigovaných) qubitů, T-hloubku 54 milionů
a logická hradla s frekvencí 10 MHz, aby výpočet trval kolem sekundy. Současné odhady počítají s frekvencí
řádově 10 kHz.

**Srovnání s GBS (náš výklad).** Amplitudová estimace je obecná a její zrychlení je dokázané pro široké třídy úloh,
ale čeká na budoucí hardware. GBS cesta je bližší dnešku – fotonické přístroje existují a metodu jde simulovat –,
výhodu ale slibuje jen pro speciální gaussovské úlohy. Hotový příklad výpočtu VaR iterativní amplitudovou
estimací je v knihovně Classiq (odkaz v Quantum Academy).
""",
    further_reading=(
        Reading(WOERNER_EGGER, "VaR a CVaR pomocí amplitudové estimace"),
        Reading(STAMATOPOULOS, "oceňování opcí"),
        Reading(EGGER_CREDIT_RISK, "kreditní riziko"),
        Reading(CHAKRABARTI, "kolik prostředků by výhoda potřebovala"),
        Reading(GLASSERMAN, "klasické Monte Carlo ve financích jako měřítko"),
    ),
)

HARDWARE_TOPIC = TheoryTopic(
    anchor="reserse-hardware",
    title="Hardware a software: na čem to jde spustit",
    in_short=(
        "Největší GBS experimenty vznikly v čínských a kanadských laboratořích. V Evropě jsou přes EuroHPC "
        "dostupné menší fotonické počítače. Pro výzkum je ale nejlepší začít simulátorem."
    ),
    explanation=r"""
**Velké experimenty.** Jiuzhang (Zhong a kol., Science 2020) a Borealis od Xanadu (Madsen a kol., Nature 2022,
216 módů) tvrdily kvantovou výhodu ve vzorkování. Jiuzhang 4.0 (Liu a kol., Nature 2026) přivádí 1024 stlačených
stavů do obvodu s 8176 módy a zaznamenává až 3050 fotonů. Jde o vzorkování z rozdělení, ne o výpočet finančních
úloh – výhoda ve vzorkování ještě neznamená výhodu v Monte Carlu.

**Co je dostupné v Evropě.** Fotonický počítač Lucy od firmy Quandela s 12 qubity patří EuroHPC JU, stojí
v centru TGCC u Paříže a byl slavnostně spuštěn 14. 4. 2026. Od 25. 6. 2026 jsou kvantové počítače EuroHPC
v pilotní výzvě zdarma dostupné výzkumníkům, veřejným institucím i firmám z Evropy, s měsíčními uzávěrkami.
Lucy je obecný fotonický počítač, ne GBS. Polské superpočítačové centrum PSNC v Poznani provozuje od roku 2023
dva přístroje ORCA PT-1 – programovatelné boson samplery s časovými biny; na jednom z nich už vznikla práce
o optimalizaci portfolia (viz Další použití GBS ve financích).

**Software pro simulaci.** The Walrus počítá hafniány a pravděpodobnosti GBS, Strawberry Fields od Xanadu
simuluje fotonické obvody. Pozor: oba repozitáře jsou od roku 2026 archivované a dál se nevyvíjejí. Aktivně
vyvíjené jsou Perceval (Quandela) a Piquasso. Tato aplikace počítá vše vlastním kódem v Pythonu, pro malé úlohy
to stačí; platformy Classiq a CUDA-Q jsou popsané v Quantum Academy.

**Doporučený postup (náš výklad).** Nejdřív estimátor implementovat a otestovat v simulaci, kde známe přesný
výsledek; pak přidat realistický šum a ztráty fotonů (viz háček o reálném hardwaru); teprve potom zkoušet
skutečný fotonický procesor.
""",
    further_reading=(
        Reading(ZHONG, "Jiuzhang"),
        Reading(MADSEN, "Borealis"),
        Reading(JIUZHANG_4, "Jiuzhang 4.0: 1024 stlačených stavů, 8176 módů"),
        Reading(EUROHPC_LUCY, "Lucy"),
        Reading(EUROHPC_QUANTUM_ACCESS, "jak získat přístup"),
        Reading(ORCA_PT1, "boson sampler v PSNC"),
        Reading(WALRUS_HAFNIAN, "výpočet hafniánů"),
        Reading(STRAWBERRY_FIELDS, "simulace fotonických obvodů"),
        Reading(PERCEVAL),
        Reading(PIQUASSO),
    ),
)

CRITICISM_TOPIC = TheoryTopic(
    anchor="reserse-kritika",
    title="Kritická literatura: kdy GBS zvládne i klasický počítač",
    in_short=(
        "Ztráty fotonů a šum dovolují reálné GBS experimenty napodobit klasicky. Každou tvrzenou výhodu je proto "
        "nutné porovnat s nejlepším klasickým algoritmem, ne jen s obyčejným Monte Carlem."
    ),
    explanation=r"""
**Šum pomáhá klasice.** Qi a kol. (2020) popsali, při jaké míře šumu a ztrát je GBS klasicky simulovatelné.
Bulmer a kol. (2022) s novými algoritmy na superpočítači se zhruba 100 000 jádry napodobili GBS experimenty až
se 100 módy a 92 fotony; odhad pro tehdejší špičkové experimenty klesl z 600 milionů let na několik měsíců.
Oh a kol. (2024) využili ztráty fotonů v tensor-network algoritmu, napodobili tehdy největší experiment
s poměrně skromnými prostředky a podle autorů se ideálnímu rozdělení přiblížili lépe než experiment samotný.

**Klasika napodobuje i aplikace.** Oh a kol. (2024, PRX Quantum) ukázali kvantově inspirovaný klasický algoritmus
pro grafové úlohy, které měl GBS řešit. Novější práce vzorkují z GBS rozdělení na grafech efektivně klasicky
(Zhang a kol. 2025), dokonce v polynomiálním čase (Anand a kol. 2025).

**Závod pokračuje.** Jiuzhang 4.0 (2026) podle autorů obstál proti všem dnes známým klasickým metodám. Hranice
výhody se tedy posouvá oběma směry.

**Co z toho plyne pro výzkum (náš výklad).** Každé tvrzení o výhodě musí říct, v jakém režimu platí (počet
fotonů, ztráty, typ detektorů) a proti jakému klasickému algoritmu se měří. Na otázku „proč to nejde klasicky?“
je nutné mít připravenou odpověď.
""",
    further_reading=(
        Reading(QI_NOISY_SIMULABILITY, "kdy je šumové GBS klasicky simulovatelné"),
        Reading(BULMER_BOUNDARY, "hranice přesné klasické simulace"),
        Reading(OH_CLASSICAL_SIMULATION, "tensor-network simulace experimentů"),
        Reading(OH_QUANTUM_INSPIRED, "kvantově inspirovaný algoritmus pro grafové úlohy"),
        Reading(ZHANG_GBS_MCMC, "efektivní klasické vzorkování na grafech"),
        Reading(ANAND_POLYNOMIAL_SIMULATION, "polynomiální simulace na grafech"),
        Reading(JIUZHANG_4, "nejnovější tvrzení výhody"),
    ),
)

OTHER_USES_TOPIC = TheoryTopic(
    anchor="reserse-dalsi-pouziti",
    title="Další použití GBS ve financích",
    in_short=(
        "GBS se ve financích zkouší i mimo Monte Carlo: na hledání podvodů v grafech transakcí, optimalizaci "
        "portfolia a předpověď časových řad. Většina prací je zatím simulační nebo na malých přístrojích."
    ),
    explanation=r"""
- **Husté podgrafy.** Arrazola a Bromley (2018) ukázali, že GBS vzorkuje přednostně husté podgrafy. He a kol.
  (2026, UnionPay, TuringQ a Fudan University) na tom stavějí algoritmy pro podvody, koluzi, praní peněz
  a anomálie trhu a mapují je na fotonické obvody s časovým multiplexem.
- **Optimalizace portfolia.** Grodzki, Słysz a Waligóra (2026) řešili binární optimalizaci portfolia
  na simulátoru i na přístroji ORCA PT-1 v PSNC.
- **Časové řady.** Cimini a kol. (2026) použili GBS s více než 400 módy jako „rezervoár“ pro strojové učení.

Pro odhad rizika přes Monte Carlo jsou to spíš inspirace než přímé konkurence. Ukazují ale, kde je o GBS ve
financích zájem (náš výklad).
""",
    further_reading=(
        Reading(ARRAZOLA_BROMLEY, "GBS a husté podgrafy"),
        Reading(HE_GRAPH_FINANCE, "grafové úlohy ve financích"),
        Reading(GRODZKI_PORTFOLIO, "optimalizace portfolia na fotonickém přístroji"),
        Reading(CIMINI_RESERVOIR, "rezervoárové počítání s GBS"),
    ),
)

PATENTS_TOPIC = TheoryTopic(
    anchor="reserse-patenty",
    title="Patenty: kdo si co chrání",
    in_short=(
        "Univerzita Twente má patentovou přihlášku na Monte Carlo integraci s optickým kvantovým počítačem, Xanadu "
        "udělený patent na zařízení a metody GBS. Metodu Andersena a Shan rešerše v patentových databázích "
        "nenašla – je publikovaná otevřeně."
    ),
    explanation=r"""
**Twente.** Přihláška WO2024225891A1 *Monte Carlo integration using an optical quantum computer* (vynálezci Renema,
Roelink a Correa Anguita, priorita 25. 4. 2023, zveřejněná 31. 10. 2024) zatím udělená není. Pokračuje
v Evropě jako EP4702506A1 a v Austrálii; Google Patents u evropské přihlášky uvádí nového vlastníka, firmu
QuiX Quantum, s upozorněním, že údaje o vlastnících nemusí být přesné.

**Xanadu.** Patent US11593699B2 *Apparatus and methods for Gaussian boson sampling* (priorita 22. 5. 2019) byl
v USA udělen 28. 2. 2023; z téže rodiny je udělený i kanadský patent a evropská přihláška je otevřená.

**Co to znamená (náš výklad, ne právní rada).** Patenty omezují hlavně komerční využití. Před případným
nasazením v bance by bylo nutné patentové posouzení odborníkem, zejména vůči přihlášce z Twente a rodině
patentů Xanadu.
""",
    further_reading=(
        Reading(TWENTE_PATENT, "Monte Carlo integrace s optickým kvantovým počítačem"),
        Reading(XANADU_GBS_PATENT, "zařízení a metody GBS"),
    ),
)

OPEN_QUESTIONS_TOPIC = TheoryTopic(
    anchor="reserse-otevrene-otazky",
    title="Otevřené otázky",
    in_short=(
        "Které finanční úlohy spadají do oblasti s výhodou GBS, jak estimátory snášejí ztráty fotonů a co dělají "
        "negaussovská data s tlustými chvosty? V prošlé literatuře jsme odpovědi nenašli – je tu prostor pro "
        "vlastní výzkum."
    ),
    explanation=r"""
Následující seznam je náš přehled mezer, které z rešerše vyplynuly, ne citace jednoho zdroje.

1. **Které ukazatele rizika mají výhodu?** Důkaz Andersena a Shan platí pro část gaussovských úloh. Není jasné,
   jestli do ní spadají prakticky důležité ukazatele (VaR, CVaR, zajištění portfolia) a jak by se to dalo předem
   poznat.
2. **Reálná data nejsou gaussovská.** Výnosy aktiv mají tlusté chvosty a shlukování volatility (Cont 2001).
   Metoda integruje proti gaussovskému rozdělení, takže reálná data je nutné transformovat nebo aproximovat –
   a není jasné, co se tím stane s výhodou.
3. **Ztráty a šum.** Estimátory jsou odvozené pro ideální přístroj. Jak rychle se výhoda ztrácí se ztrátami
   fotonů a s prahovými detektory?
4. **Férové srovnání.** Měřítkem by nemělo být jen prosté Monte Carlo, ale i quasi-Monte Carlo a metody
   snižování rozptylu, a to v čase a ceně do dosažení přesnosti, ne jen v počtu vzorků.
5. **Recenze a reprodukovatelnost.** Práce Andersena a Shan zatím neprošly recenzním řízením a čísla, která
   Qpurpose uvádí pro Jyske Bank, nejsou podložená publikovanou metodou.
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_ADVANTAGE, "jak velká část úloh má výhodu"),
        Reading(CONT_STYLIZED_FACTS, "tlusté chvosty a další vlastnosti reálných výnosů"),
        Reading(GLASSERMAN, "quasi-Monte Carlo a snižování rozptylu"),
    ),
)

TOPICS: Tuple[TheoryTopic, ...] = (
    CLAIMS_TOPIC,
    THEORY_TOPIC,
    TWENTE_TOPIC,
    GATE_BASED_TOPIC,
    HARDWARE_TOPIC,
    CRITICISM_TOPIC,
    OTHER_USES_TOPIC,
    PATENTS_TOPIC,
    OPEN_QUESTIONS_TOPIC,
)

KEY_FINDINGS: Tuple[KeyFinding, ...] = (
    KeyFinding(
        "**Přínos u Jyske Bank zatím nevznikl na kvantovém hardwaru.** Algoritmy Qpurpose podle veřejných zdrojů "
        "běží na klasických superpočítačích, které kvantový počítač emulují.",
        CLAIMS_TOPIC.anchor,
    ),
    KeyFinding(
        "**Exponenciální výhoda je dokázaná jen pro část úloh a jen v počtu vzorků** – a zatím jen v preprintech. "
        "Které finanční ukazatele do této části spadají, nikdo neukázal.",
        THEORY_TOPIC.anchor,
    ),
    KeyFinding(
        "**Existuje konkurenční experimentální linie.** Univerzita Twente předvedla boson sampling s jednotlivými "
        "fotony jako akcelerátor Monte Carla na čipu a podala patentovou přihlášku.",
        TWENTE_TOPIC.anchor,
    ),
    KeyFinding(
        "**Hradlové kvantové Monte Carlo je obecnější, ale vzdálenější.** Výhoda v oceňování derivátů by potřebovala "
        "asi 8 tisíc chybově korigovaných qubitů.",
        GATE_BASED_TOPIC.anchor,
    ),
    KeyFinding(
        "**Klasické algoritmy dohánějí reálné GBS experimenty.** Každou výhodu je nutné měřit proti nejlepšímu "
        "klasickému algoritmu.",
        CRITICISM_TOPIC.anchor,
    ),
    KeyFinding(
        "**Začít jde hned a bez kvantového počítače** – simulací. Fotonický hardware je v Evropě dostupný přes "
        "EuroHPC a v PSNC.",
        HARDWARE_TOPIC.anchor,
    ),
    KeyFinding(
        "**Otevřené zůstávají hlavně otázky reálných dat:** tlusté chvosty, ztráty fotonů a férové srovnání v čase.",
        OPEN_QUESTIONS_TOPIC.anchor,
    ),
)

REVIEW_QUESTIONS: Tuple[ReviewQuestion, ...] = (
    ReviewQuestion(
        "Běží řešení Qpurpose pro Jyske Bank na kvantovém počítači?",
        "Podle veřejných zdrojů ne: algoritmy zatím běží na klasických superpočítačích, které kvantový počítač "
        "emulují, a na kvantový hardware se mají přesunout později. Čísla o přínosu pro banku nejde ověřit.",
        CLAIMS_TOPIC.anchor,
    ),
    ReviewQuestion(
        "Co přesně dokázali Andersen a Shan a co z jejich výsledku neplyne?",
        "Že na otevřené neprázdné podmnožině gaussovských úloh potřebují jejich GBS estimátory exponenciálně méně "
        "vzorků než prosté Monte Carlo pro danou relativní přesnost $\\varepsilon$ a spolehlivost $\\delta$. "
        "Neplyne z toho výhoda v čase, na všech úlohách ani pro konkrétní finanční ukazatele; práce jsou navíc "
        "zatím preprinty.",
        THEORY_TOPIC.anchor,
    ),
    ReviewQuestion(
        "Proč nestačí ukázat, že GBS potřebuje méně vzorků než obyčejné Monte Carlo?",
        "Protože konkurentem je nejlepší klasický postup – včetně klasické simulace samotného GBS, která díky "
        "ztrátám fotonů často jde – a protože v praxi rozhoduje čas a cena, ne počet vzorků.",
        CRITICISM_TOPIC.anchor,
    ),
    ReviewQuestion(
        "Proč je kvantová amplitudová estimace pro odhad rizika zatím mimo dosah?",
        "Její zrychlení vyžaduje hluboké obvody, které bez opravy chyb zničí šum. Pro výhodu v oceňování derivátů "
        "by bylo potřeba asi 8 tisíc logických qubitů a hradla s frekvencí 10 MHz – nic takového dnes neexistuje.",
        GATE_BASED_TOPIC.anchor,
    ),
    ReviewQuestion(
        "Čím se liší přístup Univerzity Twente od práce Andersena a Shan?",
        "Twente předvádí experiment na fotonickém čipu s jednotlivými fotony (ne GBS), integrand dělí mezi přístroj "
        "a klasický výpočet, ukazuje to na fyzikálním integrálu a metodu chrání patentovou přihláškou. Andersen "
        "a Shan dokazují výhodu GBS teoreticky a publikují otevřeně.",
        TWENTE_TOPIC.anchor,
    ),
    ReviewQuestion(
        "Proč nejsou reálné výnosy pro GBS estimátor „zadarmo“?",
        "Metoda integruje proti gaussovskému rozdělení, kdežto reálné výnosy mají tlusté chvosty a shlukování "
        "volatility. Data je nutné transformovat nebo aproximovat a není jasné, co se tím stane s výhodou.",
        OPEN_QUESTIONS_TOPIC.anchor,
    ),
)
