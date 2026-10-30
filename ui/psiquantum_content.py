"""Texts of the page on PsiQuantum: from Rudolph's 2017 blueprint (shown in Walther's lecture) to October 2026.

Sources were checked on 30 October 2026 through search results; company claims are marked as such and figures that
only one aggregator reports (for example a rumoured 2026 round) are left out. Numbers we compute ourselves are
checked by tests/test_psiquantum_page.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from ui.ghz_states_content import BROWNE_RUDOLPH_2005
from ui.photonics_landscape_content import PSIQUANTUM_OMEGA
from ui.theory_content import KeyFinding, Reading, Source, TheoryTopic
from ui.walther_lecture_content import BARTOLUCCI_FBQC, GIMENO_SEGOVIA_2015, PSIQUANTUM_2021, RUDOLPH_2017

TITLE = "PsiQuantum: cesta od Rudolphova plánu k milionu fotonických qubitů"
SOURCES_ANCHOR = "psiq-zdroje"
SOURCES_CHECKED_DATE = "30. 10. 2026"
LECTURE_SLIDES = ("slajd_2676.jpg", "slajd_2695.jpg")
"""Walther's slides with Rudolph's blueprint and the 2021 funding round."""

INTRO = (
    "Na Waltherově slajdu „Blueprint for photonic quantum computer“ je plán Terryho Rudolpha z roku 2017 – a Walther "
    "dodává, že přesně podle něj staví svůj počítač firma PsiQuantum. Tahle stránka sleduje, co se s plánem stalo: "
    "kdo firmu založil, jak se plán změnil ve fúzní kvantové počítání, co PsiQuantum skutečně ukázal (čipy Omega "
    "z továrny GlobalFoundries), kolik peněz dostal, kde a kdy staví a co na to kritici. Na konci jsou videa, "
    f"podcasty a články. Stav k {SOURCES_CHECKED_DATE}; co je jen tvrzení firmy, je tak označené."
)


@dataclass(frozen=True)
class FundingRound:
    date: str
    name: str
    amount_musd: int
    """Millions of US dollars."""
    investors: str
    valuation: str


FUNDING_ROUNDS: Tuple[FundingRound, ...] = (
    FundingRound(
        "duben 2020", "Series C", 215, "Playground, Atomico, Founders Fund, Redpoint, BlackRock", "nezveřejněno",
    ),
    FundingRound("červenec 2021", "Series D", 450, "vedla BlackRock; Baillie Gifford, M12 (Microsoft), Temasek",
                 "asi 3,15 mld. USD (podle tisku)"),
    FundingRound("září 2025", "Series E", 1000, "BlackRock, Temasek, Baillie Gifford; NVentures (NVIDIA), Macquarie",
                 "7 mld. USD"),
)
"""Rounds confirmed by two or more sources; the 2016 and 2017 rounds are only in aggregators and differ."""

SERIES_D_VALUATION_BUSD = 3.15
SERIES_E_VALUATION_BUSD = 7.0

KEY_FINDINGS = (
    KeyFinding(
        "**Plán z roku 2017** (Rudolph): z ohlašovaných fotonů multiplexováním skoro na povel vyrobit malé provázané "
        "stavy, spojovat je fúzemi a počítat měřením. Firma ho od té doby přetavila ve **fúzní kvantové počítání** "
        "(FBQC, 2023), kde se z malých stavů rovnou staví kód opravující chyby.",
        "psiq-plan",
    ),
    KeyFinding(
        "**Co je ukázané:** čipy Omega z běžné polovodičové továrny GlobalFoundries s věrností fúze 99,22 % "
        "a propojení čipů 99,72 % (Nature 2025) – ale jen u fotonů, které se nevytratily. Integrovaný generátor "
        "zdrojových stavů ani logický qubit zatím veřejně ukázaný není.",
        "psiq-omega",
    ),
    KeyFinding(
        "**Peníze:** soukromá kola od roku 2020 za 1,665 mld. USD (poslední 1 mld. USD při ocenění 7 mld.), k tomu "
        "940 mil. AUD od Austrálie a Queenslandu, pobídky Illinois a smlouvy s DARPA, kde je PsiQuantum v závěrečné "
        "fázi programu QBI.",
        "psiq-penize",
    ),
    KeyFinding(
        "**Termíny se posouvají:** počítač v Brisbane měl běžet koncem roku 2027; stavba se přestěhovala do Moreton "
        "Bay, základní kámen až v červnu 2026 a tisk píše o roce 2029. Chicago má testovací systém pro DARPA "
        "kolem roku 2028.",
        "psiq-kde-a-kdy",
    ),
    KeyFinding(
        "**Kritika:** největší slabinou jsou podle odborníků **ztráty fotonů**, hlavně v optických přepínačích; "
        "australská dotace prošla bez běžného výběrového řízení a vyvolala vyšetřování v Senátu.",
        "psiq-kritika",
    ),
)

ABOUT_PSIQUANTUM = Source(
    "PsiQuantum: [O firmě](https://psiquantum.com/about) a [technologie](https://psiquantum.com/technology)"
)
FOUNDER_BIOS = Source(
    "PsiQuantum: [životopisy zakladatelů a vedení](https://www.psiquantum.com/s/PsiQuantum-FounderExecBios.pdf)"
)
RUDOLPH_SUMMARY = Source(
    "PsiQuantum: [Why I am optimistic about the silicon-photonic route to quantum computing]"
    "(https://psiquantum.com/news-import/why-i-am-optimistic-about-the-silicon-photonic-route-to-quantum-computing) "
    "– shrnutí Rudolphova plánu, preprint [arXiv:1607.08535](https://arxiv.org/abs/1607.08535)"
)
INTERLEAVING = Source(
    "Bombín, H. a kol.: *Interleaving: modular architectures for fault-tolerant photonic quantum computing*. 2021, "
    "[arXiv:2103.08612](https://arxiv.org/abs/2103.08612)"
)
LINEAR_OPTICS_STATES = Source(
    "Bartolucci, S. a kol.: *Creation of entangled photonic states using linear optics*. 2021, "
    "[arXiv:2106.13825](https://arxiv.org/abs/2106.13825)"
)
ACTIVE_VOLUME = Source(
    "Litinski, D., Nickerson, N.: *Active volume: an architecture for efficient fault-tolerant quantum computers "
    "with limited non-local connections*. 2022, [arXiv:2211.15465](https://arxiv.org/abs/2211.15465)"
)
LOSS_TOLERANCE_2025 = Source(
    "PsiQuantum: *Comparison of schemes for highly loss tolerant photonic fusion based quantum computing*. 2025, "
    "[arXiv:2506.11975](https://arxiv.org/abs/2506.11975); shrnutí "
    "[The Quantum Insider](https://thequantuminsider.com/2025/06/17/psiquantum-study-maps-path-to-loss-tolerant-"
    "photonic-quantum-computing/), 17. 6. 2025"
)
GLOBALFOUNDRIES_2021 = Source(
    "Business Wire: [PsiQuantum a GlobalFoundries vyrábějí čipy pro kvantový počítač]"
    "(https://www.businesswire.com/news/home/20210505005355/en), 5. 5. 2021"
)
OMEGA_ANNOUNCEMENT = Source(
    "Business Wire: [PsiQuantum oznamuje čipovou sadu Omega]"
    "(https://www.businesswire.com/news/home/20250226714082/en/), 26. 2. 2025"
)
OMEGA_COMMENTARY = Source(
    "PostQuantum: [rozbor článku o platformě Omega](https://postquantum.com/quantum-research/psiquantum-photonic-"
    "platform-nature/) – věrnosti jsou podmíněné detekcí fotonů"
)
LINDE_CRYOPLANT = Source(
    "Linde Engineering: [velký kryogenní systém pro PsiQuantum v Austrálii](https://www.linde-engineering.com/news-and-"
    "events/press-releases/2025/linde-engineering-to-deliver-large-cryogenic-plant-to-psiquantum-in-australia), "
    "8. 5. 2025"
)
SERIES_C = Source(
    "Global Venturing: [PsiQuantum získal 215 mil. USD](https://globalventuring.com/university/psiquantum-processes-"
    "215m-round), 7. 4. 2020"
)
SERIES_D = Source(
    "The Quantum Insider: [BlackRock vede kolo 450 mil. USD](https://thequantuminsider.com/2021/07/27/investors-see-"
    "the-light-as-blackrock-leads-450-million-series-d-investment-into-psiquantum/), 27. 7. 2021"
)
SERIES_E = Source(
    "Business Wire: [PsiQuantum získal 1 mld. USD](https://www.businesswire.com/news/home/20250910135739/en/), "
    "10. 9. 2025; Bloomberg: [NVIDIA podporuje PsiQuantum, ocenění 7 mld. USD](https://www.bloomberg.com/news/"
    "articles/2025-09-10/nvidia-backs-psiquantum-in-1-billion-round-at-7-billion-value)"
)
AUSTRALIA_DEAL = Source(
    "Business Wire: [Austrálie a Queensland investují do PsiQuantum](https://www.businesswire.com/news/home/"
    "20240429080449/en), 29. 4. 2024 – 940 mil. AUD v kapitálu, grantech a půjčkách"
)
ILLINOIS_PARK = Source(
    "Capitol News Illinois: [začala stavba Illinois Quantum and Microelectronics Park](https://capitolnewsillinois.com/"
    "news/state-private-developers-break-ground-on-quantum-research-park/), 30. 9. 2025"
)
DARPA_FINAL_PHASE = Source(
    "The Quantum Insider: [DARPA vybrala Microsoft a PsiQuantum do závěrečné fáze](https://thequantuminsider.com/2025/"
    "02/07/darpa-selects-microsoft-psiquantum-for-final-phase-of-its-useful-quantum-computer-program/), 7. 2. 2025"
)
DARPA_125M = Source(
    "Business Wire: [smlouva s DARPA za 125 mil. USD](https://www.businesswire.com/news/home/20260722358075/en/), "
    "22. 7. 2026"
)
DARPA_STAGE_C_2026 = Source(
    "DARPA: [čtyři další týmy v závěrečné fázi QBI](https://www.darpa.mil/news/2026/four-more-teams-enter-quantum-"
    "benchmarking-initiative-final-stage), 7. 10. 2026"
)
CHIPS_AWARD = Source(
    "NIST: [dokončení grantu CHIPS R&D pro PsiQuantum](https://www.nist.gov/news-events/news/2026/09/department-"
    "commerce-announces-finalization-chips-rd-award-psiquantum), září 2026 – 100 mil. USD"
)
AFRL_BTO = Source(
    "Breaking Defense: [AFRL dává PsiQuantum 10,8 mil. USD na experimentální čipy](https://breakingdefense.com/2025/04/"
    "air-force-research-lab-awards-psiquantum-10-8m-for-experimental-quantum-chips), duben 2025"
)
OSC_LOAN = Source(
    "The Quantum Insider: [podmíněná půjčka až 150 mil. USD na kalifornský závod](https://thequantuminsider.com/2026/"
    "10/08/psiquantum-conditional-150m-loan-california-quantum-facility/), 8. 10. 2026"
)
MORETON_BAY = Source(
    "Business News Australia: [PsiQuantum stěhuje stavbu z letiště v Brisbane do Moreton Bay]"
    "(https://www.businessnewsaustralia.com/articles/psiquantum-shifts-940-million-quantum-computer-site-from-brisbane-"
    "airport-to-moreton-bay.html), květen 2026"
)
BRISBANE_LATE = Source(
    "Startup Daily: [stavba v Brisbane má velké zpoždění](https://www.startupdaily.net/topic/global-tech/psiquantums-"
    "brisbane-build-is-already-running-very-late/), leden 2026"
)
GROUNDBREAKING_2026 = Source(
    "Business Wire: [základní kámen v Moreton Bay](https://www.businesswire.com/news/home/20260617018403/en/), "
    "17. 6. 2026"
)
CHICAGO_2028 = Source(
    "Investing.com (Bloomberg): [počítač v Chicagu má běžet v roce 2028](https://in.investing.com/news/company-news/"
    "psiquantums-chicago-quantum-computer-to-begin-operations-in-2028--bloomberg-93CH-4920596), červenec 2025"
)
DARESBURY = Source(
    "UKRI: [PsiQuantum otevírá vývojové pracoviště v Daresbury](https://ukri.org/news/psiquantum-opens-rd-facility-at-"
    "daresbury-laboratory), březen 2023"
)
FERRIE_2024 = Source(
    "Ferrie, C.: [Austrálie vsadila miliardu na první užitečný kvantový počítač. Vyplatí se to?]"
    "(https://theconversation.com/australia-just-made-a-billion-dollar-bet-on-building-the-worlds-first-useful-"
    "quantum-computer-in-brisbane-will-it-pay-off-228992), The Conversation, 30. 4. 2024"
)
ADVISORY_BYPASSED = Source(
    "The Quantum Insider: [investice obešla národní poradní výbor pro kvantové technologie]"
    "(https://thequantuminsider.com/2024/05/07/australian-governments-big-investment-on-psiquantum-bypassed-national-"
    "quantum-advisory-committee/), 7. 5. 2024"
)
INTERNAL_REVIEW = Source(
    "ACS Information Age: [interní audit dohody s PsiQuantum](https://ia.acs.org.au/article/2025/govt-s-psiquantum-"
    "deal-given-all-clear-by-internal-audit.html), 2025 – postup „přiměřený“, finanční riziko „vysoké“"
)
IEEE_SPECTRUM = Source(
    "IEEE Spectrum: [PsiQuantum Supercomputer: Aiming for a Million Qubits](https://spectrum.ieee.org/psiquantum-"
    "supercomputer), 2025 – s komentářem Simona Devitta ke ztrátám v přepínačích"
)
DARPA_PARADOX = Source(
    "PostQuantum: [paradox DARPA QBI: náskok bez ukázky](https://postquantum.com/quantum-computing/darpa-qbi-paradox-"
    "undemonstrated-lead/) – komentář"
)
MIT_TR_2026 = Source(
    "O'Donnell, J.: [PsiQuantum has a plan to make a massive quantum computer out of light]"
    "(https://www.technologyreview.com/2026/07/14/1140356/psiquantum-plan-massive-quantum-computer-out-of-light/), "
    "MIT Technology Review, 14. 7. 2026"
)
NATURE_FEATURE_2024 = Source(
    "Gibney, E.: *This billion-dollar firm plans to build giant quantum computers from light. Can it succeed?* Nature "
    "(news feature), 28. 11. 2024, [doi:10.1038/d41586-024-03827-y](https://doi.org/10.1038/d41586-024-03827-y)"
)
CEO_CHANGE = Source(
    "Business Wire: [Victor Peng prozatímním CEO, Jeremy O'Brien předsedou představenstva]"
    "(https://www.businesswire.com/news/home/20260210565444/en/), 10. 2. 2026"
)
LIP_BU_TAN = Source(
    "Semafor: [šéf Intelu Lip-Bu Tan v představenstvu PsiQuantum](https://www.semafor.com/article/04/30/2026/quantum-"
    "computing-company-psiquantum-adds-intels-lip-bu-tan-to-board), 30. 4. 2026"
)
LOCKHEED = Source(
    "Business Wire: [memorandum s Lockheed Martin o algoritmech](https://www.businesswire.com/news/home/20251103085089/"
    "en/), 3. 11. 2025"
)
BOEHRINGER = Source(
    "The Quantum Insider: [Boehringer Ingelheim a PsiQuantum: odhad zrychlení simulací molekul]"
    "(https://thequantuminsider.com/2025/01/15/psiquantum-boehringer-ingelheim-researchers-report-speedup-for-complex-"
    "molecular-simulations/), 15. 1. 2025"
)
OPTICAL_SWITCH = Source(
    "The Quantum Insider: [optický přepínač 8 × 8 pro datová centra AI](https://thequantuminsider.com/2026/10/28/"
    "psiquantum-optical-circuit-switch-ai-data-centers/), 28. 10. 2026"
)
CONSTRUCT_NVIDIA = Source(
    "The Quantum Insider: [Construct s NVIDIA CUDA-Q](https://thequantuminsider.com/2026/03/17/psiquantum-construct-"
    "450x-speedup-nvidia-cuda-q-integration/), 17. 3. 2026"
)
RUDOLPH_TALK_2018 = Source(
    "Rudolph, T.: [Why I am optimistic about the silicon-photonic route to quantum computing]"
    "(https://www.youtube.com/watch?v=u2hKabVtols), přednáška BQIT 2018 (YouTube)"
)
RUDOLPH_CALTECH = Source(
    "Rudolph, T.: [Quantum Computing at the Speed of Light](https://www.youtube.com/watch?v=ifodWb0Tguo), Caltech, "
    "4. 11. 2021 (YouTube)"
)
RUDOLPH_PHOTONS = Source(
    "Rudolph, T.: [How to stop worrying and love the photons](https://www.youtube.com/watch?v=-NOSx9tHO2Y) (YouTube)"
)
SHADBOLT_Q2B = Source(
    "Shadbolt, P.: [přednáška na Q2B 2021](https://www.youtube.com/watch?v=MKHWj_zD8Yc) (YouTube)"
)
SHADBOLT_GTC = Source(
    "Shadbolt, P.: [NVIDIA GTC 2025, Quantum Day](https://www.youtube.com/watch?v=s_gMIuxZg54) (YouTube)"
)
OBRIEN_UNSW = Source(
    "O'Brien, J.: [Westheimerova přednáška, UNSW 2023](https://www.youtube.com/watch?v=kVfbVgsIbkE) (YouTube)"
)
NICKERSON_PIRSA = Source(
    "Nickerson, N.: [Fault tolerance with the ZX-calculus and fusion complexes](https://pirsa.org/node/22866), "
    "Perimeter Institute, 31. 5. 2024"
)
PROTIVITI_PODCAST = Source(
    "Podcast The Post-Quantum World: [A Million Photonic Qubits](https://www.protiviti.com/us-en/podcast/million-"
    "photonic-qubits) – rozhovor s Terrym Rudolphem"
)
PSIQUANTUM_RESEARCH = Source(
    "PsiQuantum: [seznam publikací](https://www.psiquantum.com/research) a [vysvětlení FBQC]"
    "(https://www.psiquantum.com/news-import/fusion-based-quantum-computation-fbqc)"
)
PHOTONIC_SURVEY = Source(
    "*Photonic quantum computers*. Přehledový článek, 2024, [arXiv:2409.08229](https://arxiv.org/abs/2409.08229)"
)


WHO_TOPIC = TheoryTopic(
    anchor="psiq-kdo",
    title="Kdo jsou a odkud přišli",
    in_short=(
        "Firmu založili v roce 2016 v Palo Altu čtyři fyzici z Bristolu a Imperial College: Jeremy O'Brien, Terry "
        "Rudolph, Pete Shadbolt a Mark Thompson. Od začátku chtěli rovnou celý počítač s opravou chyb, ne malé "
        "přechodné stroje."
    ),
    explanation=r"""
**Zakladatelé.** Jeremy O'Brien vedl v Bristolu skupinu integrované kvantové fotoniky (je mimo jiné autorem
přehledu *Optical quantum computing* z roku 2007, ze kterého je jeden z Waltherových slajdů). Terry Rudolph je
teoretik z Imperial College – spoluautor fúzních hradel (Browne a Rudolph, 2005), deterministického zdroje klastrů
(Lindner a Rudolph, 2009) i balistického počítání ze třífotonových GHZ stavů (2015). Pete Shadbolt a Mark Thompson
přišli z bristolských laboratoří křemíkové fotoniky. V roce 2026 má firma podle odhadů zhruba 500–650 lidí; sama
počty nezveřejňuje.

**Role dnes.** Rudolph je hlavní architekt, Shadbolt vědecký ředitel, Thompson hlavní technolog. O'Brien vedl firmu
deset let; v únoru 2026 ho ve funkci generálního ředitele vystřídal **Victor Peng** (dříve prezident AMD a šéf
Xilinxu), od července 2026 natrvalo, a O'Brien je předsedou představenstva. Firma to vysvětluje přechodem „od
výzkumu k nasazení“. V dubnu 2026 přibyl do představenstva šéf Intelu Lip-Bu Tan.

**Sázka od prvního dne.** PsiQuantum se od začátku neúčastnil závodu o „NISQ“ stroje s desítkami šumných qubitů.
Cílem je rovnou počítač s opravou chyb, a protože na to je potřeba řádově milion fyzikálních qubitů, musí se dát
**vyrobit v polovodičové továrně**. Odtud spolupráce s GlobalFoundries. *Náš výklad:* proto firma léta skoro
nepublikovala výsledky z laboratoře – malý stroj by podle její logiky nic nedokazoval, rozhoduje vyrobitelnost
součástek.

**Pracoviště:** sídlo v Palo Altu, výroba a testování prototypů v Milpitas (Kalifornie, asi 13 000 m²), vývojové
pracoviště v britském Daresbury (od roku 2023, kryogenika), stavba v Chicagu a v Austrálii (kapitola o termínech).
""",
    further_reading=(
        Reading(ABOUT_PSIQUANTUM),
        Reading(FOUNDER_BIOS),
        Reading(CEO_CHANGE),
        Reading(LIP_BU_TAN),
        Reading(NATURE_FEATURE_2024, "nejlepší úvodní reportáž o firmě"),
    ),
)

PLAN_TOPIC = TheoryTopic(
    anchor="psiq-plan",
    title="Od plánu z roku 2017 k fúznímu kvantovému počítání",
    in_short=(
        "Rudolphův plán: multiplexované ohlašované fotony, z nich malé provázané stavy, fúze a perkolace. Dnešní "
        "architektura FBQC místo jednoho obřího klastru opakuje malé „zdrojové stavy“ a fúze rovnou jako součást "
        "opravy chyb; fotony čekají v optických vláknech."
    ),
    explanation=r"""
**Plán z roku 2017.** Rudolph v článku *Why I am optimistic about the silicon-photonic route to quantum computing*
(preprint 2016, APL Photonics 2017) – to je „blueprint“ na Waltherově slajdu – tvrdí, že úzkým hrdlem je výroba
malých třífotonových provázaných stavů na čipu. Nepočítá ale se zázračným deterministickým zdrojem: ohlašované
jednotlivé fotony z křemíkových vlnovodů (spontánní čtyřvlnné směšování) se **multiplexují** rychlými přepínači
skoro na povel, z nich se pravděpodobnostně skládají malé provázané stavy a ty se multiplexují znovu. Pak už jen
pasivní optika „balisticky“ rozptýlí stavy fúzemi do velkého klastru. Podle článku to stojí řádově 100 fyzikálních
fotonů na jeden výpočetní, s dobrými třífotonovými zdroji pod 20. Proč zrovna tři fotony, vykládá stránka
[GHZ stavy](/fotonika/prednaska-walther-2022/ghz-stavy#ghz-proc-tri).

**Fúzní kvantové počítání (FBQC, 2021/2023).** Hlavní změna oproti plánu: místo jednoho obřího klastru, který roste
perkolací, se opakují **zdrojové stavy pevné velikosti** (třeba „6-kruh“ ze šesti fotonů, v zakódované verzi
z 24) z generátorů, které pracují
pořád dokola. Fúze mezi nimi nejsou jen lepidlo – jejich výsledky jsou rovnou měřeními kódu, který opravuje chyby
(topologický povrchový kód). Článek uvádí prahy: kód vydrží 10,4 % ztrát na jednu fúzi (asi 2,7 % na foton)
a 43,2 % neúspěšných fúzí.

**Prokládání (interleaving, 2021).** Jeden generátor zdrojových stavů obslouží mnoho míst kódu, protože fotony mohou
chvíli „čekat“ v optickém vlákně – vlákno slouží jako paměť. Počítač je tak modulární: moduly s generátory a fúzemi
spojené vlákny.

**Aktivní objem (2022).** Litinski a Nickerson ukázali, že s levnými nelokálními spoji (vlákna) cena výpočtu roste
s počtem logických operací, ne s celým objemem obvodu – pro rozklad 2048bitového čísla vychází „aktivní objem“
44× menší.

**Ztráty jako hlavní nepřítel (2025).** Studie firmy srovnává schémata, jak zdrojové stavy zakódovat a fúze
přizpůsobovat, aby kód snesl víc ztrát. Bez kódování snese posílená fúze méně než 1 % ztrát na foton; se
zakódovaným 6-kruhem 2,7 %; nejlepší schémata víc.

*Naše shrnutí, ne citace:* „deterministický třífotonový GHZ“ z roku 2017 se v praxi proměnil v řetězec
ohlašované fotony → multiplexování → lineárně optická výroba malých provázaných stavů → fúze do zakódovaných
zdrojových stavů → fúze mezi nimi, s fotony čekajícími ve vláknech. Integrovaný generátor zdrojových stavů ale
zatím firma veřejně neukázala.
""",
    further_reading=(
        Reading(RUDOLPH_2017, "plán na Waltherově slajdu"),
        Reading(RUDOLPH_SUMMARY),
        Reading(GIMENO_SEGOVIA_2015, "předchůdce: balistické počítání ze třífotonových GHZ"),
        Reading(BROWNE_RUDOLPH_2005, "fúzní hradla"),
        Reading(BARTOLUCCI_FBQC, "fúzní kvantové počítání"),
        Reading(INTERLEAVING),
        Reading(LINEAR_OPTICS_STATES, "jak se zdrojové stavy skládají z jednotlivých fotonů"),
        Reading(ACTIVE_VOLUME),
        Reading(LOSS_TOLERANCE_2025),
    ),
)

OMEGA_TOPIC = TheoryTopic(
    anchor="psiq-omega",
    title="Továrna a čipy Omega: co je skutečně ukázané",
    in_short=(
        "Čipy se vyrábějí v běžné továrně GlobalFoundries. Sada Omega (Nature 2025) má zdroje, přepínače "
        "z titaničitanu "
        "barnatého, vlnovody z nitridu křemíku a supravodivé detektory; věrnosti přes 99 %, ale jen pro fotony, které "
        "se neztratily. Chlazení na asi 4 K v „kryokabinetech“."
    ),
    explanation=r"""
**GlobalFoundries (od roku 2021).** PsiQuantum má vlastní nástroje ve dvou 300mm továrnách GlobalFoundries: fotonické
čipy v Malta (stát New York, Fab 8), řídicí elektroniku v Drážďanech. Firma tvrdí, že čipů vyrobila už „miliony“ –
to je tvrzení firmy, ne nezávislé měření. Smysl je jasný: kvantový počítač z čipů, které umí vyrobit běžná továrna,
se dá škálovat jako polovodičový průmysl.

**Omega (únor 2025, Nature).** Sada čipů pro dvoukolejné (dual-rail) fotonické qubity. Součástky:

- zdroje jednotlivých fotonů (spontánní, ohlašované),
- elektrooptické přepínače z **titaničitanu barnatého (BTO)** – rychlé a s malými ztrátami, nutné pro multiplexování,
- vlnovody z **nitridu křemíku** s malými ztrátami,
- **supravodivé detektory** jednotlivých fotonů (stejný princip jako
  ve [Waltherově přednášce](/fotonika/prednaska-walther-2022#walther-hardware)).

**Změřená čísla** (článek v Nature):

| Veličina | Hodnota |
|---|---|
| příprava a měření stavu qubitu (SPAM) | 99,98 % ± 0,01 % |
| Hongova–Ouova–Mandelova viditelnost fotonů z nezávislých zdrojů | 99,50 % ± 0,25 % |
| věrnost dvouqubitové fúze | 99,22 % ± 0,12 % |
| věrnost propojení dvou čipů vláknem | 99,72 % ± 0,04 % |

**Háček:** všechny věrnosti jsou **podmíněné detekcí** – počítají se jen případy, kdy foton dorazil. Ztráty, které
jsou pro fotonický počítač největší problém, v nich nejsou (článek to u propojení výslovně píše). Firma tvrdí, že
ztráty snížila „z asi 50 % na asi 1 %“ – to je opět její údaj.

**Chlazení.** Na rozdíl od supravodivých qubitů (milikelviny) stačí fotonickým čipům a detektorům kolem **4 K**
(kapalné helium). Čipy sedí v „kryokabinetech“ velikosti serverové skříně, propojených vlákny; pro užitečný stroj
jich má být kolem stovky (MIT Technology Review). Pro australský stroj dodává Linde velký heliový kryosystém.

**Co ukázané není.** Veřejně zatím nebyl ukázán integrovaný generátor zdrojových stavů, síť fúzí ani logický qubit
(stav říjen 2026). MIT Technology Review v červenci 2026 shrnul: „tenhle počítač, jak je popsaný, neexistuje“ –
existují jeho součástky.
""",
    further_reading=(
        Reading(PSIQUANTUM_OMEGA, "článek v Nature 2025"),
        Reading(OMEGA_ANNOUNCEMENT),
        Reading(OMEGA_COMMENTARY),
        Reading(GLOBALFOUNDRIES_2021),
        Reading(LINDE_CRYOPLANT),
        Reading(MIT_TR_2026),
    ),
)

MONEY_TOPIC = TheoryTopic(
    anchor="psiq-penize",
    title="Peníze: soukromá kola a veřejné zakázky",
    in_short=(
        "Tři potvrzená velká kola (2020–2025) dohromady 1,665 mld. USD, ocenění 7 mld. USD. K tomu Austrálie "
        "a Queensland 940 mil. AUD, Illinois, americké armádní a vládní zakázky a závěrečná fáze programu DARPA."
    ),
    explanation=r"""
**Soukromá kola** (tabulka níže, jen kola potvrzená víc zdroji). První kola z let 2016 a 2017 uvádějí jen
agregátory a navzájem se liší. V roce 2026 kolovaly zprávy o kole 1,5 mld. USD při ocenění 10,5 mld. USD –
nenašli jsme k nim tiskovou zprávu a čísla přesně odpovídají kolu ze září 2025 přepočtenému na australské
dolary, proto je neuvádíme. *Vlastní výpočet:* tři potvrzená kola dávají dohromady 1,665 mld. USD; ocenění mezi
lety 2021 a 2025 vzrostlo z asi 3,15 na 7 mld. USD, tedy 2,2krát.

**Veřejné peníze:**

- **Austrálie a Queensland (2024):** 940 mil. AUD (asi 620 mil. USD) v kapitálu, grantech a půjčkách, napůl federace
  a napůl Queensland, za počítač postavený v Brisbane.
- **Illinois (2024):** PsiQuantum je hlavním nájemcem Illinois Quantum and Microelectronics Park v Chicagu; stát dává
  pobídky kolem 200 mil. USD výměnou za investici aspoň 1,1 mld. USD.
- **DARPA:** v roce 2023 program US2QC, v únoru 2025 spolu s Microsoftem vybraný do závěrečné fáze; v červenci 2026
  smlouva za 125 mil. USD v rámci programu Quantum Benchmarking Initiative (QBI). V říjnu 2026 přibyli do závěrečné
  fáze Atom Computing, Diraq, IBM a IonQ – PsiQuantum je teď jedním ze šesti. Cílem QBI je ověřit, zda jde užitečný
  kvantový počítač postavit do roku 2033.
- **Ministerstvo obchodu USA (CHIPS):** 100 mil. USD na optické přepínače, detektory a pouzdření (2026).
- **Letectvo USA (AFRL):** 22,5 mil. USD (2022) na návrh čipů a 10,8 mil. USD (2025) na přepínače z BTO.
- **Úřad pro strategický kapitál ministerstva obrany:** podmíněná půjčka až 150 mil. USD na závod v Milpitas
  (říjen 2026, zatím nedokončená).
- **Velká Británie:** 9 mil. GBP na pracoviště v Daresbury (2023).
""",
    further_reading=(
        Reading(SERIES_C),
        Reading(SERIES_D),
        Reading(PSIQUANTUM_2021, "zpráva o kole 2021 na Waltherově slajdu"),
        Reading(SERIES_E),
        Reading(AUSTRALIA_DEAL),
        Reading(ILLINOIS_PARK),
        Reading(DARPA_FINAL_PHASE),
        Reading(DARPA_125M),
        Reading(DARPA_STAGE_C_2026),
        Reading(CHIPS_AWARD),
        Reading(AFRL_BTO),
        Reading(OSC_LOAN),
    ),
)

SITES_TOPIC = TheoryTopic(
    anchor="psiq-kde-a-kdy",
    title="Kde a kdy: Brisbane, Chicago a posouvání termínů",
    in_short=(
        "Australský stroj měl běžet koncem roku 2027; stavba se po zpoždění přestěhovala do Moreton Bay a začala "
        "v červnu 2026, tisk píše o roce 2029. V Chicagu vzniká testovací systém pro DARPA s cílem kolem roku 2028."
    ),
    explanation=r"""
| Kdy | Co |
|---|---|
| 2016 | založení firmy v Palo Altu |
| 2017 | Rudolphův plán v APL Photonics |
| 2021 | výroba v GlobalFoundries; kolo 450 mil. USD a slib celého stroje „do poloviny dekády“ |
| 2023 | článek o FBQC; pracoviště v Daresbury; program DARPA US2QC |
| duben 2024 | dohoda s Austrálií: stroj v Brisbane do konce roku 2027 |
| červenec 2024 | Chicago: hlavní nájemce kvantového parku |
| únor 2025 | čipy Omega v Nature; závěrečná fáze DARPA |
| září 2025 | kolo 1 mld. USD; základní kámen v Chicagu |
| leden 2026 | Senát: stavba na letišti v Brisbane má až rok zpoždění |
| květen 2026 | přesun stavby do Moreton Bay (bývalá papírna v Petrie) |
| červen 2026 | základní kámen v Moreton Bay, nejdřív kryosystém (2. pololetí 2027) |
| říjen 2026 | závěrečná fáze DARPA rozšířena na šest firem |

**Brisbane / Moreton Bay.** Původní cíl – užitečný stroj v provozu koncem roku 2027 – se posouvá. Stavba měla začít
v polovině roku 2025, v lednu 2026 senátní slyšení ukázalo, že plán zástavby letiště ani nešel do připomínek.
V květnu 2026 firma místo změnila, v červnu položila základní kámen. Někteří novináři píšou o provozu v roce 2029,
jiní stále citují rok 2027 a firma nový termín výslovně neuvedla.

**Chicago.** Na místě bývalých oceláren U.S. Steel South Works; první fáze má budovu kanceláří a laboratoří
a „největší přechodný testovací systém“, který má ověřit DARPA. Podle Bloombergu má běžet v roce 2028, což
O'Brien sám nazval „velmi agresivním“ termínem.

*Vlastní poznámka:* posouvání termínů není u velkých staveb nic neobvyklého, ale u PsiQuantum je to zásadní –
firma veřejně neukázala integrovaný stroj, takže termíny jsou jediné, podle čeho se dá postup měřit zvenčí.
""",
    further_reading=(
        Reading(BRISBANE_LATE),
        Reading(MORETON_BAY),
        Reading(GROUNDBREAKING_2026),
        Reading(ILLINOIS_PARK),
        Reading(CHICAGO_2028),
        Reading(DARESBURY),
    ),
)

CRITICISM_TOPIC = TheoryTopic(
    anchor="psiq-kritika",
    title="Kritika a otevřené otázky",
    in_short=(
        "Technicky: ztráty fotonů, hlavně v rychlých přepínačích, a chybějící ukázka logického qubitu. Politicky: "
        "australská dotace bez běžného výběrového řízení. Konkurence (Xanadu, Quandela) mezitím ukázala malé "
        "fungující stroje."
    ),
    explanation=r"""
**Ztráty.** Simon Devitt (IEEE Spectrum) považuje optické ztráty za největší zdroj chyb hned po chybách hradel:
vlnovody a detektory podle něj vypadají připravené, ale **ztráty v přepínačích jsou zatím příliš vysoké**. To je
přesně místo, kde Rudolphův plán potřebuje nejvíc: multiplexování stojí na mnoha rychlých přepínačích za sebou
a ztráty se násobí. Proto firma investuje do přepínačů z titaničitanu barnatého a dostala na ně peníze od AFRL
i z programu CHIPS.

**Žádný logický qubit.** Na rozdíl od supravodivých a iontových týmů, které ukázaly logické qubity s opravou chyb,
PsiQuantum zatím ukázal jen součástky. Kritici (třeba PostQuantum) upozorňují, že DARPA posunula do závěrečné
fáze firmu bez ukázaného qubitu. *Náš výklad obhajoby:* u fotonů je logika opačná – malý stroj nic nedokazuje,
rozhoduje vyrobitelnost a ztráty součástek ve velkém.

**Australská dotace.** Nabídka PsiQuantum přišla mimo běžné výběrové řízení a národní poradní výbor pro kvantové
technologie se o dohodě dozvěděl z médií. Opozice žádala dokumenty v Senátu, nová vláda Queenslandu svůj podíl
přezkoumala a ponechala s dalšími podmínkami. Interní audit (2025) označil postup za přiměřený, finanční riziko za
„vysoké“. Christopher Ferrie (UTS) psal už v roce 2024 o sázce na neprověřený stroj, která „zdaleka není jistá“.

**Konkurence mezi fotonikou.** Xanadu postavil modulární stroj Aurora (Nature 2025) a v březnu 2026 vstoupil na
burzu; Quandela dodala 12qubitový stroj Lucy do CEA a cílí na opravu chyb kolem roku 2030 (podle své roadmapy).
Přehled je ve [Fotonice ve světě](/fotonika-ve-svete#svet-jednotlive-fotony) a o Quandele na
[samostatné stránce](/reserse-gbs-financni-riziko/fotonicky-hardware).
""",
    further_reading=(
        Reading(IEEE_SPECTRUM),
        Reading(DARPA_PARADOX),
        Reading(MIT_TR_2026, "nejnovější dlouhý článek, kritický"),
        Reading(FERRIE_2024),
        Reading(ADVISORY_BYPASSED),
        Reading(INTERNAL_REVIEW),
    ),
)

RECENT_TOPIC = TheoryTopic(
    anchor="psiq-novinky",
    title="Co se děje v letech 2025–2026",
    in_short=(
        "Software Construct pro algoritmy s opravou chyb (s NVIDIA CUDA-Q), spolupráce s Lockheed Martin "
        "a Boehringer Ingelheim, nový generální ředitel a první komerční produkt mimo kvantové počítání: optický "
        "přepínač pro datová centra AI."
    ),
    explanation=r"""
- **Leden 2025 – chemie:** s Boehringer Ingelheim odhad zrychlení simulací enzymu P450 a kofaktoru FeMoco na
  architektuře aktivního objemu (234× a 278×) – jde o teoretický odhad, ne o výpočet na stroji.
- **Září 2025 – Construct:** software pro návrh algoritmů s opravou chyb; v březnu 2026 propojený s NVIDIA CUDA-Q,
  v květnu 2026 zdarma pro všechny vývojáře.
- **Listopad 2025 – Lockheed Martin:** memorandum o algoritmech pro letectví a obranu.
- **Únor a červenec 2026 – vedení:** Victor Peng generálním ředitelem, O'Brien předsedou představenstva.
- **Říjen 2026 – optický přepínač 8 × 8 pro datová centra AI:** první produkt mimo kvantové počítání, vzorky jdou
  zákazníkům. Firma uvádí vložný útlum 1,2 dB a přepnutí pod 3 ms; verze 64 × 64 je ve výrobě. Využívá stejnou
  nízkoztrátovou fotoniku jako kvantové čipy.

*Vlastní poznámka:* přepínač pro AI dává smysl obchodně (tržby dřív než kvantový počítač) i technicky – nutí firmu
vyrábět nízkoztrátové přepínače ve velkém, což kvantový plán potřebuje.
""",
    further_reading=(
        Reading(BOEHRINGER),
        Reading(CONSTRUCT_NVIDIA),
        Reading(LOCKHEED),
        Reading(CEO_CHANGE),
        Reading(OPTICAL_SWITCH),
    ),
)

LEARN_TOPIC = TheoryTopic(
    anchor="psiq-materialy",
    title="Videa, podcasty a články",
    in_short=(
        "Nejlepší začátek: Rudolphova přednáška o plánu z roku 2018 a reportáž v Nature z roku 2024. Do hloubky: "
        "článek o FBQC a přednáška Naomi Nickerson o odolnosti vůči chybám."
    ),
    explanation=r"""
**Doporučené pořadí pro doktoranda:**

1. Rudolphova přednáška *Why I am optimistic about the silicon-photonic route* (2018) – plán z Waltherova slajdu
   vlastními slovy autora.
2. Reportáž Elizabeth Gibney v Nature (2024) – kdo firma je, co slibuje a kde jsou pochybnosti.
3. Článek o fúzním kvantovém počítání (Nature Communications 2023) a vysvětlení na webu firmy.
4. Rudolph na Caltechu (2021) nebo *How to stop worrying and love the photons* – proč fotony.
5. Shadbolt na Q2B (2021) a NVIDIA GTC (2025) – inženýrský a obchodní pohled.
6. Nickerson na Perimeter Institute (2024) – oprava chyb s fúzemi v ZX-kalkulu, pro pokročilé.
7. Článek MIT Technology Review (2026) – nejnovější kritický pohled.

Všechny odkazy jsou v literatuře níže; videa jsou na YouTube, PIRSA má vlastní přehrávač.
""",
    further_reading=(
        Reading(RUDOLPH_TALK_2018),
        Reading(NATURE_FEATURE_2024),
        Reading(PSIQUANTUM_RESEARCH),
        Reading(RUDOLPH_CALTECH),
        Reading(RUDOLPH_PHOTONS),
        Reading(SHADBOLT_Q2B),
        Reading(SHADBOLT_GTC),
        Reading(OBRIEN_UNSW),
        Reading(NICKERSON_PIRSA),
        Reading(PROTIVITI_PODCAST),
        Reading(MIT_TR_2026),
        Reading(PHOTONIC_SURVEY, "přehled fotonických kvantových počítačů"),
    ),
)

THESIS_TOPIC = TheoryTopic(
    anchor="psiq-pro-disertaci",
    title="Co z toho plyne pro disertaci",
    in_short=(
        "PsiQuantum je sázka na univerzální počítač s opravou chyb kolem roku 2030 a později. Pro modifikované Monte "
        "Carlo přes GBS z něj přímo nic není – nepublikoval GBS a hardware nezpřístupňuje –, ale jeho výsledky "
        "o zdrojích, přepínačích a ztrátách se týkají každého fotonického stroje."
    ),
    explanation=r"""
*Celá kapitola je náš odhad, ne citace.*

- **Přímé využití: žádné.** PsiQuantum nenabízí přístup k hardwaru a GBS nepublikoval (viz
  [Fotonika ve světě](/fotonika-ve-svete#svet-jednotlive-fotony)). Pro výpočty v disertaci zůstávají GBS stroje
  a simulátory, třeba [Piquasso](/fotonika-ve-svete/piquasso).
- **Nepřímé využití:** kvantové Monte Carlo s kvadratickým zrychlením (amplitude estimation) je jedna z aplikací,
  na kterou firmy s univerzálními počítači míří; dobrý argument v úvodu disertace je srovnání „GBS dnes, s omezeními“
  proti „univerzální počítač s opravou chyb, nejdřív koncem dekády“.
- **Co sledovat:** ukázku generátoru zdrojových stavů a první logický qubit, výsledky závěrečné fáze DARPA QBI
  a termín spuštění v Moreton Bay.
""",
    further_reading=(
        Reading(DARPA_STAGE_C_2026),
        Reading(MIT_TR_2026),
    ),
)

TOPICS: Tuple[TheoryTopic, ...] = (
    WHO_TOPIC, PLAN_TOPIC, OMEGA_TOPIC, MONEY_TOPIC, SITES_TOPIC, CRITICISM_TOPIC, RECENT_TOPIC, LEARN_TOPIC,
    THESIS_TOPIC,
)
