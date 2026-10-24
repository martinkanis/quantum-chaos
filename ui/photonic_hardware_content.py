"""Texts of the page on Quandela and on which European photonic hardware could run GBS or boson sampling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from ui.advantage_content import ANGUITA_MONTE_CARLO_ACCELERATOR
from ui.literature_review_content import EUROHPC_LUCY, EUROHPC_QUANTUM_ACCESS, ORCA_PT1, PERCEVAL, PIQUASSO
from ui.navigation import PHOTONICS_TERMS_HREF
from ui.theory_content import (
    AARONSON_ARKHIPOV,
    ANDERSEN_SHAN_EXPECTATIONS,
    HAMILTON,
    KRUSE,
    MADSEN,
    KeyFinding,
    Reading,
    Source,
    TheoryTopic,
)

TITLE = "Quandela a fotonický hardware v Evropě"
SOURCES_ANCHOR = "fotonika-zdroje"
SOURCES_CHECKED_DATE = "19. 10. 2026"

INTRO = (
    "Co dělá francouzská firma Quandela, jak funguje její hardware a software Perceval, co z toho jde použít na "
    "modifikované Monte Carlo z této aplikace a kdo v Evropě umí spustit Gaussian Boson Sampling se stlačeným "
    f"světlem. Zdroje ověřeny {SOURCES_CHECKED_DATE}; výsledky z Percevalu jsou z našeho vlastního experimentu."
)


@dataclass(frozen=True)
class NoiseScenario:
    label: str
    relative_bias: float
    """(E[odhad] − μ) / μ spočítané v Percevalu 1.3.1 z přesného rozdělení výstupů při daném šumu zdroje."""


@dataclass(frozen=True)
class PhotonicMachine:
    operator: str
    machine: str
    input_light: str
    runs_gbs: str
    access: str


PHOTONIC_MACHINES: Tuple[PhotonicMachine, ...] = (
    PhotonicMachine("Univerzita Paderborn", "PaQS, 12 módů", "stlačené vakuum", "ano", "výzkumná spolupráce"),
    PhotonicMachine("Fraunhofer IOF Jena", "sampler z projektu PhoQuant", "stlačené světlo", "ohlášeno", "plán: cloud"),
    PhotonicMachine("DTU Kodaň", "PhotoQ", "stlačené světlo", "ve výstavbě", "plán: cloud"),
    PhotonicMachine(
        "Quandela", "Belenos, Lucy (12 qubitů, 24 módů)", "jednotlivé fotony", "ne", "cloud; Lucy přes EuroHPC"
    ),
    PhotonicMachine("QuiX Quantum", "Bia", "2–4 jednotlivé fotony", "ne", "cloud"),
    PhotonicMachine("ORCA Computing", "PT-1 (PSNC Poznaň), PT-2", "jednotlivé fotony; u PT-2 sporné", "ne", "partneři"),
    PhotonicMachine("Xanadu (Kanada, pro srovnání)", "Borealis, 216 módů", "stlačené vakuum", "ano", "od 2023 mimo cloud"),
)
"""Who could run GBS or single-photon boson sampling for us; the chapter on Europe gives the sources."""

GBS_EMULATION_AGREEMENT = "4 · 10⁻⁸"
"""Largest deviation from the hafnian formula in scripts/perceval_gbs_emulation.py (3 modes, ≤ 6 photons per mode)."""
GBS_EMULATION_INPUT_COMPONENTS = 64
"""(6/2 + 1)³ Fock states in the truncated squeezed-vacuum input of the same script."""

PERCEVAL_AGREEMENT = (
    "Pravděpodobnosti z Percevalu 1.3.1 se od vzorce s permanenty liší nejvýš o 9,7 · 10⁻¹⁷ (přes všech 56 vzorů), "
    "tedy jen zaokrouhlením."
)
NOISE_SCENARIOS: Tuple[NoiseScenario, ...] = (
    NoiseScenario("nerozlišitelnost fotonů 0,95", -0.0146),
    NoiseScenario("nerozlišitelnost fotonů 0,90", -0.0292),
    NoiseScenario("vícefotonová emise g² = 0,02", -0.0302),
    NoiseScenario("propustnost 0,5 (rovnoměrné ztráty)", 0.0),
    NoiseScenario("vše dohromady (0,90; 0,5; 0,02)", -0.0456),
)
"""Output of scripts/perceval_boson_sampling.py; Perceval is not a dependency of the app, so the numbers are stored."""

QUANDELA_CATALOGUE = Source(
    "Quandela: [Product catalogue 2026]"
    "(https://www.quandela.com/wp-content/uploads/2026/02/Product-catalogue-Quandela-Q12026.pdf) – zdroj Prometheus, "
    "procesory MosaiQ, parametry fotonů"
)
QUANDELA_BELENOS = Source("Quandela: [Belenos](https://www.quandela.com/qpus/belenos/) – 12 qubitů, 24 módů, v cloudu")
MARING_PLATFORM = Source(
    "Maring, N. a kol.: *A general-purpose single-photon-based quantum computing platform*, "
    "[arXiv:2306.00874](https://arxiv.org/abs/2306.00874) (2023) – první šestifotonový boson sampling na univerzálním "
    "programovatelném čipu"
)
PERCEVAL_LICENCE = Source(
    "GitHub: [licence Percevalu](https://github.com/Quandela/Perceval/blob/main/LICENSE) – MIT s výjimkou pro jádro "
    "exqalibur"
)
EXQALIBUR_LICENCE = Source(
    "PyPI: [exqalibur](https://pypi.org/project/exqalibur/) – výpočetní jádro Percevalu, licence CC BY-NC-ND 4.0"
)
EUROHPC_QUANTUM_CALL = Source(
    "EuroHPC JU: [Call for proposals – quantum access pilot mode]"
    "(https://www.eurohpc-ju.europa.eu/eurohpc-ju-call-proposals-quantum-access-pilot-mode_en) – měsíční uzávěrky, "
    "přístup na 3 nebo 6 měsíců, [přihláška](https://access.eurohpc-ju.europa.eu/calls/61)"
)
EUROHPC_QUANTUM_COMPUTERS = Source(
    "EuroHPC JU: [Our quantum computers](https://www.eurohpc-ju.europa.eu/supercomputers/our-quantum-computers_en) – "
    "přehled strojů, technologií a dodavatelů"
)
QUANDELA_CREDIT_AGRICOLE = Source(
    "Quandela: [Crédit Agricole and Quandela optimise default risk prediction models]"
    "(https://www.quandela.com/newsroom-posts/credit-agricole-and-quandela-optimise-default-risk-prediction-models) – "
    "bez zveřejněných metrik"
)
QPURPOSE_PARTNERSHIPS = Source(
    "Qpurpose: [Partnerships](https://qpurpose.dk/partnerships) – spolupráce s ORCA na gaussovsky vážených integrálech "
    "a očekávání podobné výhody u boson samplingu (Sparrow Quantum)"
)
PAQS_PAPER = Source(
    "Stefszky, M. a kol. (Silberhorn): *Benchmarking Gaussian and non-Gaussian input states with a hybrid sampling "
    "platform*, [arXiv:2512.08433](https://arxiv.org/abs/2512.08433) (2025, v3 2026) – stroj PaQS"
)
PADERBORN_PAQS = Source(
    "Universität Paderborn: [Europe's largest sampling-based quantum computer]"
    "(https://www.uni-paderborn.de/en/news-item/141998), 7. 10. 2024 – PaQS, projekt PhoQuant, plán cloudového "
    "sampleru ve Fraunhofer IOF Jena"
)
DTU_PHOTOQ = Source(
    "DTU: [PhotoQ](https://photoq.dtu.dk/) – stavba plně konfigurovatelného, cloudově dostupného GBS se stlačeným "
    "světlem (Innovation Fund Denmark)"
)
QUIX_BIA = Source(
    "QuiX Quantum: [Bia](https://www.quixquantum.com/news/bia-launch) – cloudová služba, 2–4 jednotlivé fotony, "
    "12–20 kanálů, mezi cílovými úlohami Quantum Monte Carlo"
)
PARK_PT2 = Source(
    "Park, Stepney, D'Amico: *Benchmarking the ORCA PT-2 Boson Sampler using Minimum Dominating Set Problems*, "
    "[arXiv:2605.30935](https://arxiv.org/abs/2605.30935) (2026)"
)
BACARREZA_PT2 = Source(
    "Bacarreza a kol. (ORCA Computing): *Quantum latent distributions in deep generative models*, "
    "[arXiv:2508.19857](https://arxiv.org/abs/2508.19857) (2025)"
)
PAESANI_CHIP = Source(
    "Paesani, S. a kol.: *Generation and sampling of quantum states of light in a silicon chip*. Nature Physics 15 "
    "(2019), 925–929, [arXiv:1812.03158](https://arxiv.org/abs/1812.03158)"
)
PHOQUSING = Source(
    "CORDIS: [PHOQUSING – Photonic Quantum Sampling Machine](https://cordis.europa.eu/project/id/899544) – projekt EU "
    "2020–2024 (Sapienza, CNRS, QuiX a další), kvantové tečky a jednotlivé fotony"
)
HAMILTON_JEX_NON_GAUSSIAN = Source(
    "Hamilton, C. S., Jex, I.: *Boson sampling from non-Gaussian states*, "
    "[arXiv:2403.17183](https://arxiv.org/abs/2403.17183) (2024) – ČVUT FJFI"
)
LUND_SCATTERSHOT = Source(
    "Lund, A. P., Laing, A., Rahimi-Keshari, S. a kol.: *Boson sampling from a Gaussian state*. Physical Review "
    "Letters 113, 100502 (2014), [doi:10.1103/PhysRevLett.113.100502](https://doi.org/10.1103/PhysRevLett.113.100502) "
    "– scattershot boson sampling ze stlačeného světla"
)
WANG_TWENTY_PHOTONS = Source(
    "Wang, H. a kol.: *Boson sampling with 20 input photons and a 60-mode interferometer in a 10^14-dimensional "
    "Hilbert space*. Physical Review Letters 123, 250503 (2019), "
    "[doi:10.1103/PhysRevLett.123.250503](https://doi.org/10.1103/PhysRevLett.123.250503)"
)
BOREALIS_RETIRED = Source(
    "PennyLane fórum: [Access to Borealis device](https://discuss.pennylane.ai/t/access-to-borealis-device/3322), "
    "15. 8. 2023 – Borealis stažen z cloudu Xanadu"
)

COMPANY_TOPIC = TheoryTopic(
    anchor="fotonika-quandela",
    title="Quandela: kdo to je a co dělá",
    in_short=(
        "Francouzský výrobce fotonických kvantových počítačů postavených na jednotlivých fotonech z kvantových teček. "
        "Prodává procesory do cloudu i do datových center, zdroje fotonů a software Perceval; v Evropě provozuje "
        "stroj Lucy pro EuroHPC."
    ),
    explanation=r"""
**Firma.** Quandela vznikla v roce 2017 a sídlí v Massy u Paříže. Prodává kvantové procesory (přes cloud
i k instalaci u zákazníka), samostatné zdroje jednotlivých fotonů, software a cloudové služby.

**Stroje.** Procesor Belenos (12 qubitů, 24 módů) je dostupný v cloudu Quandela. Stroj Lucy stejné řady patří
EuroHPC JU, stojí v centru TGCC u Paříže a byl slavnostně spuštěn 14. 4. 2026. Je to jediný fotonický stroj mezi
kvantovými počítači EuroHPC – ostatní jsou neutrální atomy, iontové pasti a supravodivé qubity, včetně VLQ v IT4I
v Ostravě (IQM, 24 qubitů).

**Čím se zabývá.** Firma propaguje hlavně kvantové strojové učení, variační algoritmy a grafové úlohy. Ve financích
hlásí spolupráci s Crédit Agricole CIB na předpovědi selhání úvěrů, bez zveřejněných metrik. Práci na Monte Carlu
nebo numerické integraci jsme u Quandely nenašli.
""",
    further_reading=(
        Reading(QUANDELA_CATALOGUE),
        Reading(QUANDELA_BELENOS),
        Reading(EUROHPC_LUCY, "stroj Lucy"),
        Reading(EUROHPC_QUANTUM_COMPUTERS),
        Reading(QUANDELA_CREDIT_AGRICOLE, "jediný nalezený finanční případ"),
    ),
)

HARDWARE_TOPIC = TheoryTopic(
    anchor="fotonika-hardware-quandely",
    title="Hardware: jednotlivé fotony, ne stlačené světlo",
    in_short=(
        "Zdrojem je kvantová tečka, která na každý puls laseru vyšle nejvýš jeden foton. Stlačené světlo, které GBS "
        "potřebuje, žádný stroj Quandely nevyrábí – umí ale boson sampling s jednotlivými fotony a libovolným "
        "interferometrem."
    ),
    explanation=r"""
**Zdroj.** Kvantová tečka v polovodičové mikrodutině vyzařuje jednotlivé fotony. Katalog uvádí pro zdroj
Prometheus vícefotonovou složku $g^{(2)}(0)$ kolem 2 % a nerozlišitelnost fotonů kolem 94 %. Právě tyto dvě veličiny
v našem experimentu níže vychylují odhad.

**Výpočet.** Fotony se rozdělí do prostorových módů, projdou programovatelným interferometrem (síť děličů svazku
a fázových posuvů) a dopadnou na detektory. Qubit je jeden foton ve dvou módech (dual-rail); pro hradlové výpočty se
dvouqubitová hradla dělají s pomocnými fotony a výběrem výsledků.

**Co z toho plyne pro GBS.** GBS potřebuje na vstupu stlačené vakuum – stav, ve kterém vznikají páry fotonů – a jeho
pravděpodobnosti jsou hafniány. Jednotlivé fotony dávají pravděpodobnosti $|\mathrm{Perm}(U_{S,T})|^2/S!$, tedy
permanenty. Na čipu Quandely už proběhl boson sampling se šesti fotony (Maring a kol.); GBS v pravém smyslu na
jejich hardwaru spustit nejde.
""",
    further_reading=(
        Reading(QUANDELA_CATALOGUE),
        Reading(MARING_PLATFORM),
        Reading(HAMILTON, "proč GBS potřebuje stlačené světlo"),
    ),
)

SAMPLING_KINDS_TOPIC = TheoryTopic(
    anchor="fotonika-bs-a-gbs",
    title="Boson sampling, nebo Gaussian boson sampling: v čem je rozdíl",
    in_short=(
        "Přístroj je v obou případech stejný – interferometr a detektory fotonů –, liší se jen to, co do něj svítí. "
        "Boson sampling posílá jednotlivé fotony a pravděpodobnosti výstupů jsou permanenty; GBS posílá stlačené "
        "vakuum, fotony v něm vznikají po párech a pravděpodobnosti jsou hafniány. Quandela umí první: má zdroj "
        "jednotlivých fotonů, ne stlačeného světla."
    ),
    explanation=r"""
**Co mají společné.** Světlo vstoupí do $m$ módů, projde interferometrem $U$ (síť děličů svazku a fázových
posuvů) a detektory spočítají fotony v každém výstupu. Výsledek jednoho výstřelu je vzor $S = (s_1, \dots, s_m)$.
V obou případech je losování z rozdělení vzorů pro klasický počítač prokazatelně těžké (za rozumných předpokladů).

| | boson sampling | Gaussian boson sampling |
|:---|:---|:---|
| navrhli | Aaronson a Arkhipov (2011) | Hamilton a kol. (2017) |
| vstup | $n$ jednotlivých fotonů | stlačené vakuum v každém módu |
| počet fotonů ve výstřelu | vždy přesně $n$ | náhodný, sudý (fotony vznikají po párech) |
| pravděpodobnost vzoru | $\lvert\mathrm{Perm}(U_{S,T})\rvert^2 / S!$ | $\lvert\mathrm{Haf}(B_S)\rvert^2 / (S!\,\prod_j \cosh r_j)$ |
| maticová funkce | permanent | hafnián |
| zdroj světla | kvantová tečka, ohlašovaný foton | nelineární krystal nebo vlnovod |
| příklady strojů | Quandela, QuiX, USTC (20 fotonů) | Jiuzhang, Borealis, PaQS |
| odhad typu GBS-I | permanentní varianta (příloha F) | GBS-I a GBS-P (Andersen a Shan) |

**Proč permanent a proč hafnián.** Při boson samplingu má každý foton svůj vstup a hledá se, který foton skončil
v kterém detektoru – to je *přiřazení* dvou různých seznamů, a součet přes všechna přiřazení je permanent. Ve
stlačeném vakuu vznikají fotony po dvojicích a hledá se, které zachycené fotony tvořily pár – to je *rozdělení
jednoho seznamu do dvojic*, a součet přes všechna taková rozdělení je hafnián. Rozdíl polopatě a v datových
strukturách vysvětluje stránka o hafniánu.

**Proč GBS na Quandele nejde.**

- *Zdroj:* kvantová tečka vyšle na puls nejvýš jeden foton. Stlačené vakuum je superpozice 0, 2, 4, … fotonů a
  vzniká v nelineárním materiálu (parametrická down-konverze, """ + f"[co to je]({PHOTONICS_TERMS_HREF})" + r""");
  takový zdroj procesory Quandely nemají.
- *Optika to nedožene:* interferometr je lineární a zachovává počet fotonů, takže ze vstupu s pevným počtem fotonů
  superpozici různých počtů nevyrobí.
- *Software:* Perceval 1.3.1 ani jeho jádro nemají stlačené stavy, hafniány ani torontiány (jejich obdobu pro
  detektory, které jen rozliší „foton ano/ne“); jádro počítá permanenty.

**V simulátoru to ale oklikou jde (náš experiment).** Stlačené vakuum jde zapsat jako superpozici Fockových stavů se
sudým počtem fotonů a simulátor Percevalu umí takovou superpozici poslat interferometrem. Pro 3 módy a nejvýš
6 fotonů na mód (64 složek vstupu) se pravděpodobnosti shodují s hafniánovým vzorcem
z této aplikace na 4 · 10⁻⁸. Je to ovšem obyčejná klasická simulace: počet složek roste jako
$(K/2+1)^m$ pro $K$ fotonů na mód, takže jde jen o malé případy, a na skutečný procesor takový vstup nahrát nejde.

**Obráceně to funguje.** Stroj se stlačeným světlem umí i boson sampling: dvoumódové stlačené vakuum vytvoří pár
fotonů, detekce jednoho z nich „ohlásí“ druhý a z mnoha takových zdrojů se náhodně vybere vstup (scattershot boson
sampling, Lund a kol. 2014). Permanent je zvláštní případ hafniánu, GBS je tedy obecnější úloha.

**Co tedy znamená „Quandela umí boson sampling“.** Variantu Aaronsona a Arkhipova s jednotlivými fotony – tu
předvedli na svém čipu se šesti fotony (Maring a kol.) a jejich dokumentace k ní má příklady. GBS se stlačeným
světlem to není.
""",
    further_reading=(
        Reading(AARONSON_ARKHIPOV, "boson sampling s jednotlivými fotony"),
        Reading(HAMILTON, "Gaussian boson sampling"),
        Reading(LUND_SCATTERSHOT),
        Reading(WANG_TWENTY_PHOTONS, "boson sampling s 20 fotony z kvantové tečky"),
        Reading(MARING_PLATFORM, "boson sampling na čipu Quandely"),
    ),
)

SOFTWARE_TOPIC = TheoryTopic(
    anchor="fotonika-perceval",
    title="Software: Perceval",
    in_short=(
        "Perceval je otevřená knihovna v Pythonu pro lineární optiku s jednotlivými fotony: obvody, realistický šum "
        "zdroje, přesné i vzorkovací simulátory a odesílání úloh na skutečné procesory. Stlačené stavy ani hafniány "
        "nezná."
    ),
    explanation=r"""
**Co umí.** Libovolný interferometr (komponenta `Unitary`), Fockovy stavy, model šumu zdroje (pravděpodobnost emise,
$g^{(2)}$, nerozlišitelnost, ztráty, nepřesnost fází) a detektory s rozlišením počtu fotonů i bez něj. Simulátory:
SLOS (přesné rozdělení), Naive a NaiveApprox (permanent přesně, nebo Gurvitsovým odhadem), MPS a CliffordClifford2017
(vzorkování). Úlohy jde poslat na procesory Quandela přes jejich cloud nebo přes Scaleway.

**Co jsme ověřili v kódu.** Ve zdrojácích Percevalu 1.3.1 ani jeho výpočetního jádra exqalibur není nic se stlačením,
gaussovskými stavy, hafniány ani torontiány; jádro počítá permanenty (Glynn, Ryser) a jejich Gurvitsův odhad.

**Praktické podmínky.** Perceval potřebuje Python ≥ 3.10, takže v této aplikaci (lokálně Python 3.9) běží zvlášť –
skript `scripts/perceval_boson_sampling.py` přes Podman. Perceval je pod licencí MIT. Jeho výpočetní jádro exqalibur
má samo o sobě licenci **CC BY-NC-ND 4.0** (jen nekomerční použití), licence Percevalu ale obsahuje výjimku: exqalibur
se smí v rámci Percevalu, tedy přes jeho pythonovské vazby, používat a šířit za podmínek MIT. Pro výzkum to
neznamená žádné omezení; před komerčním nasazením bychom tento výklad (náš) ověřili s Quandelou.
""",
    further_reading=(
        Reading(PERCEVAL, "dokumentace a kód"),
        Reading(PERCEVAL_LICENCE),
        Reading(EXQALIBUR_LICENCE),
    ),
)

USE_CASE_TOPIC = TheoryTopic(
    anchor="fotonika-nase-monte-carlo",
    title="Jak Quandelu použít na naše modifikované Monte Carlo",
    in_short=(
        "Odhad GBS-I od Andersena a Shan funguje pro jakýkoli sampler s pravděpodobnostmi tvaru váha × funkce matice. "
        "Pro jednotlivé fotony z něj vznikne odhad součtů $\\sum a_S |\\mathrm{Perm}(U_{S,T})|^2$ – ten na Quandele "
        "běží a v Percevalu jsme ho ověřili."
    ),
    explanation=r"""
**Převod z GBS na boson sampling (náš výklad).** V obecné části prvního článku (Def. 3.3) je odhad GBS-I vážený výběr
pro libovolný sampler s $P(S) = w_S\,\varphi(S)$. U jednotlivých fotonů je $P(S) = |\mathrm{Perm}(U_{S,T})|^2/S!$,
takže výstřel se vzorem $S$ přispěje hodnotou $Z(S) = a_S\,S!$ a průměr odhaduje
$$\mu = \sum_S a_S\,|\mathrm{Perm}(U_{S,T})|^2.$$
Místo hafniánů reálné gaussovské míry tak vystupují permanenty – obdoba rodiny $\mathrm{Haf}^2$ pro komplexní
gaussovská rozdělení. Sami autoři v příloze F prvního článku popisují komplexní obdobu gaussovské úlohy, ve které
místo hafniánů vystupují permanenty, a obdobné výsledky pro boson sampling slibují v samostatné práci. Qpurpose na
své stránce partnerů píše, že podobné exponenciální zrychlení očekává i pro boson sampling; experimentálně tuto
cestu předvedla skupina z Twente.

**Náš experiment v Percevalu.** Haarovsky náhodný interferometr se 6 módy, 3 fotony na vstupu, koeficienty $a_S$
náhodně z $(0{,}5;\,1{,}5)$. Pravděpodobnosti z Percevalu se shodují se vzorcem s permanenty, odhad je nevychýlený
a vzorky z Percevalu k přesné hodnotě konvergují. Pak jsme zapnuli šum zdroje – tabulka níže.

**Co z tabulky plyne.** Rovnoměrné ztráty odhad nevychylují: když se počítají jen výstřely se všemi fotony, ztráta
zahodí výstřely, ale nezmění jejich rozdělení. Rozlišitelné fotony a vícefotonová emise ale dávají systematickou
chybu v řádu procent, kterou žádný počet výstřelů neodstraní – při parametrech zdroje Quandela je to podstatné
a přesně to je námět pro diagnostiku, kdy odhad selže.

**Které prostředí použít.** Vývoj a ladění lokálně v Percevalu (SLOS, model šumu), pak jejich simulátor skutečného
stroje v cloudu a nakonec procesor Belenos v cloudu Quandela nebo Lucy přes výzvu EuroHPC. Pro GBS se stlačeným
světlem Quandela použít nejde – viz další kapitola.
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "obecný odhad GBS-I (Def. 3.3) a permanenty v příloze F"),
        Reading(ANGUITA_MONTE_CARLO_ACCELERATOR, "boson sampling jako akcelerátor Monte Carla"),
        Reading(QPURPOSE_PARTNERSHIPS),
        Reading(EUROHPC_QUANTUM_CALL, "přístup k Lucy"),
    ),
)

EUROPE_TOPIC = TheoryTopic(
    anchor="fotonika-gbs-v-evrope",
    title="Kdo v Evropě umí GBS se stlačeným světlem",
    in_short=(
        "Jako službu v Evropě GBS nenabízí nikdo. Programovatelný GBS stroj provozuje Univerzita Paderborn (PaQS) – "
        "dostupný přes výzkumnou spolupráci; DTU v Kodani staví GBS dostupný přes cloud. Ostatní evropské fotonické "
        "stroje pracují s jednotlivými fotony."
    ),
    explanation=r"""
**GBS se stlačeným světlem.**

- **Univerzita Paderborn, stroj PaQS (skupina C. Silberhorn).** Integrovaný zdroj stlačeného vakua, plně
  programovatelný dvanáctimódový interferometr QuiX a supravodivé detektory rozlišující až tři fotony; vznikl
  v německém projektu PhoQuant. Přístup jen přes spolupráci.
- **Fraunhofer IOF Jena.** Univerzita Paderborn ohlásila druhý, cloudově dostupný sampler v Jeně; jestli už běží,
  jsme neověřili.
- **DTU Kodaň, projekt PhotoQ.** Staví plně konfigurovatelný GBS se stlačeným světlem, který má být dostupný přes
  cloud. Je ve výstavbě.
- **Historicky:** GBS na křemíkovém čipu předvedl Bristol (Paesani a kol., 2019). Kanadský Borealis od Xanadu byl
  v roce 2023 stažen z cloudu.

**Jednotlivé fotony (boson sampling, ne GBS).** Quandela (Belenos, Lucy), QuiX Quantum (cloudová služba Bia,
2–4 fotony, mezi cílovými úlohami uvádí Quantum Monte Carlo), Sapienza a projekt PHOQUSING. ORCA Computing má stroje
PT-1 v polském PSNC a PT-2 ve Velké Británii: PT-1 pracuje s jednotlivými fotony, u PT-2 popisuje nezávislý benchmark
fotonově odčítané stlačené stavy, kdežto článek ORCA mluví o jednotlivých fotonech. Qpurpose podle své stránky s ORCA
spolupracuje na gaussovsky vážených integrálech.

**Česká stopa.** Původní článek o GBS spoluautorsky napsali Craig S. Hamilton a Igor Jex z FJFI ČVUT spolu
s paderbornskou skupinou; Hamilton a Jex se dál věnují boson samplingu s negaussovskými stavy. Pro spolupráci
s Paderbornem je to přirozený most (náš návrh).
""",
    further_reading=(
        Reading(PAQS_PAPER),
        Reading(PADERBORN_PAQS),
        Reading(DTU_PHOTOQ),
        Reading(PAESANI_CHIP),
        Reading(MADSEN, "Borealis"),
        Reading(BOREALIS_RETIRED),
        Reading(QUIX_BIA),
        Reading(PHOQUSING),
        Reading(ORCA_PT1),
        Reading(PARK_PT2),
        Reading(BACARREZA_PT2, "PT-2 podle ORCA"),
        Reading(HAMILTON, "původní GBS, ČVUT a Paderborn"),
        Reading(KRUSE),
        Reading(HAMILTON_JEX_NON_GAUSSIAN),
    ),
)

RECOMMENDATION_TOPIC = TheoryTopic(
    anchor="fotonika-doporuceni",
    title="Co z toho plyne pro výzkum (náš návrh)",
    in_short=(
        "GBS počítat klasicky na vlastním kódu, o GBS hardware žádat přes spolupráci s Paderbornem nebo DTU a na "
        "Quandele mezitím testovat obdobu s jednotlivými fotony – Lucy jde zdarma přes výzvu EuroHPC."
    ),
    explanation=r"""
1. **Teď:** estimátory GBS dál simulovat klasicky – kód této aplikace, případně Piquasso – a na superpočítači
   Karolina v IT4I.
2. **Hardware pro GBS:** požádat o spolupráci Paderborn (stroj PaQS); vstupní bod je ČVUT (Hamilton, Jex). Sledovat
   DTU PhotoQ, až zpřístupní cloud.
3. **Quandela pro obdobu s jednotlivými fotony:** v Percevalu zkoumat, jak šum zdroje vychyluje odhad; pak žádost
   do pilotní výzvy EuroHPC o čas na stroji Lucy – nejbližší uzávěrka je 1. 11. 2026, přístup na 3 nebo 6 měsíců.
4. **Na co dát pozor:** licence jádra exqalibur mimo Perceval (nekomerční), patentová přihláška Twente na Monte Carlo s optickým
   kvantovým počítačem a to, že sama obdoba GBS-I pro permanenty zatím nemá důkaz výhody – jde o otevřenou otázku.
""",
    further_reading=(
        Reading(PIQUASSO, "klasická simulace GBS"),
        Reading(EUROHPC_QUANTUM_ACCESS, "pilotní přístup EuroHPC"),
        Reading(EUROHPC_QUANTUM_CALL),
    ),
)

TOPICS: Tuple[TheoryTopic, ...] = (
    COMPANY_TOPIC,
    HARDWARE_TOPIC,
    SAMPLING_KINDS_TOPIC,
    SOFTWARE_TOPIC,
    USE_CASE_TOPIC,
    EUROPE_TOPIC,
    RECOMMENDATION_TOPIC,
)

KEY_FINDINGS: Tuple[KeyFinding, ...] = (
    KeyFinding(
        "**Quandela GBS neumí.** Její stroje pracují s jednotlivými fotony z kvantových teček, ne se stlačeným "
        "světlem; Perceval nezná hafniány ani stlačené stavy.",
        HARDWARE_TOPIC.anchor,
    ),
    KeyFinding(
        "**Boson sampling ≠ GBS.** Jednotlivé fotony dávají permanenty, stlačené světlo hafniány. Malé GBS jde "
        "v simulátoru Percevalu napodobit oklikou, na hardwaru ne.",
        SAMPLING_KINDS_TOPIC.anchor,
    ),
    KeyFinding(
        "**Umí ale obdobu s jednotlivými fotony.** Odhad GBS-I přeložený na permanenty jsme v Percevalu ověřili: "
        "sedí se vzorcem a je nevychýlený.",
        USE_CASE_TOPIC.anchor,
    ),
    KeyFinding(
        "**Šum zdroje dělá systematickou chybu**, rovnoměrné ztráty ne: rozlišitelné fotony a vícefotonová emise "
        "posunou odhad o jednotky procent.",
        USE_CASE_TOPIC.anchor,
    ),
    KeyFinding(
        "**GBS se stlačeným světlem v Evropě jako službu nikdo nenabízí.** Programovatelný stroj má Paderborn "
        "(spolupráce), DTU staví cloudový.",
        EUROPE_TOPIC.anchor,
    ),
    KeyFinding(
        "**Česká stopa:** spoluautoři původního GBS (Hamilton, Jex) jsou na ČVUT – přirozený most k Paderbornu.",
        EUROPE_TOPIC.anchor,
    ),
    KeyFinding(
        "**Lucy od Quandely jde zdarma přes výzvu EuroHPC**, nejbližší uzávěrka 1. 11. 2026.",
        RECOMMENDATION_TOPIC.anchor,
    ),
)
