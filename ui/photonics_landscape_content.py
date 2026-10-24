"""Texts of the page on photonic quantum computing worldwide: companies, research groups, suppliers and who can do GBS."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from ui.advantage_content import ANGUITA_MONTE_CARLO_ACCELERATOR
from ui.andersen_shan_paper_content import ZHONG_2021
from ui.literature_review_content import (
    CIMINI_RESERVOIR,
    EUROHPC_LUCY,
    EUROHPC_QUANTUM_ACCESS,
    HE_GRAPH_FINANCE,
    JIUZHANG_4,
    PERCEVAL,
    TWENTE_PATENT,
)
from ui.photonic_hardware_content import (
    BACARREZA_PT2,
    BOREALIS_RETIRED,
    DTU_PHOTOQ,
    EUROHPC_QUANTUM_CALL,
    PADERBORN_PAQS,
    PAESANI_CHIP,
    PAQS_PAPER,
    PARK_PT2,
    PHOQUSING,
    QPURPOSE_PARTNERSHIPS,
    QUANDELA_CREDIT_AGRICOLE,
    QUIX_BIA,
    WANG_TWENTY_PHOTONS,
)
from ui.theory_content import (
    HAMILTON,
    MADSEN,
    OH_CLASSICAL_SIMULATION,
    SDU_QUANTUM_FINANCE,
    ZHONG,
    KeyFinding,
    Reading,
    Source,
    TheoryTopic,
)

TITLE = "Fotonika ve světě: konkurence a partneři"
SOURCES_ANCHOR = "svet-zdroje"
RESEARCH_DATE = "24. 10. 2026"
INTRO = (
    "Kdo ve světě staví fotonické kvantové počítače, co přesně dělá a prodává, kdo dodává součástky, kdo umí – nebo "
    "by teoreticky uměl – Gaussian Boson Sampling a kdo je pro disertaci konkurence a kdo partner. Rešerše je ze dne "
    f"{RESEARCH_DATE}; tvrzení firem a nerecenzované preprinty jsou tak označené a ke každé položce je zdroj."
)


class GbsVerdict(str, Enum):
    BUILT = "postavil GBS"
    THEORETICALLY = "teoreticky"
    COMPONENTS = "jen komponenty"
    NO = "ne"


class PlayerKind(str, Enum):
    COMPANY = "firma"
    RESEARCH = "výzkum"


@dataclass(frozen=True)
class PhotonicsPlayer:
    name: str
    country: str
    kind: PlayerKind
    what: str
    verdict: GbsVerdict
    reason: str


PLAYERS: Tuple[PhotonicsPlayer, ...] = (
    PhotonicsPlayer("USTC Hefei (Pan, Lu) – Jiuzhang", "Čína", PlayerKind.RESEARCH, "stlačené světlo, tisíce módů",
                    GbsVerdict.BUILT, "Jiuzhang 1.0–4.0, naposledy 1 024 stlačených stavů v 8 176 módech (Nature 2026)"),
    PhotonicsPlayer("Xanadu", "Kanada", PlayerKind.COMPANY, "stlačené světlo, GKP qubity",
                    GbsVerdict.BUILT, "X8 a Borealis byly skutečné GBS; dnes vyřazené, cloud zrušen"),
    PhotonicsPlayer("Univerzita Paderborn (Silberhorn) – PaQS", "Německo", PlayerKind.RESEARCH, "stlačené světlo, 12 módů",
                    GbsVerdict.BUILT, "PaQS: stlačené vakuum, čip QuiX, detektory do 3 fotonů; přístup spoluprací"),
    PhotonicsPlayer("TuringQ (Jin, SJTU)", "Čína", PlayerKind.COMPANY, "čipy z niobičnanu lithného",
                    GbsVerdict.BUILT, "GBS na čipu s více než 10 000 fotony, zatím jen preprint (září 2026)"),
    PhotonicsPlayer("Imperial / Oxford (Walmsley)", "Velká Británie", PlayerKind.RESEARCH, "stlačené světlo, časové biny",
                    GbsVerdict.BUILT, "GBS s posunutím (15 módů) a GBS pro husté podgrafy"),
    PhotonicsPlayer("Bristol → NBI (Paesani)", "Velká Británie / Dánsko", PlayerKind.RESEARCH, "křemíkový čip",
                    GbsVerdict.BUILT, "GBS na čipu se zdroji stlačeného světla (2019); dnes jiné téma"),
    PhotonicsPlayer("DTU Kodaň (Andersen) – PhotoQ", "Dánsko", PlayerKind.RESEARCH, "stlačené světlo, klastrové stavy",
                    GbsVerdict.THEORETICALLY, "staví GBS dostupný přes cloud, patent na GBS; experiment zatím nenalezen"),
    PhotonicsPlayer("PhoQuant (Fraunhofer IOF Jena, Paderborn, Q.ANT a další)", "Německo", PlayerKind.RESEARCH,
                    "národní projekt fotonického počítače", GbsVerdict.THEORETICALLY,
                    "cílí na GBS se 100 kanály a cloudem do poloviny 2027; PaQS je mezikrok"),
    PhotonicsPlayer("Q.ANT", "Německo", PlayerKind.COMPANY, "klasický fotonický procesor pro AI",
                    GbsVerdict.COMPONENTS, "čipy z niobičnanu lithného; partner projektu PhoQuant"),
    PhotonicsPlayer("NTT", "Japonsko", PlayerKind.COMPANY, "špičkové zdroje stlačeného světla",
                    GbsVerdict.THEORETICALLY, "10 dB stlačení, ale počítač měří homodynně, fotony nepočítá"),
    PhotonicsPlayer("OptQC (Furusawa) / RIKEN", "Japonsko", PlayerKind.COMPANY, "analogový optický počítač",
                    GbsVerdict.THEORETICALLY, "stlačené světlo a gaussovské operace, ale bez počítání fotonů"),
    PhotonicsPlayer("ORCA Computing", "Velká Británie", PlayerKind.COMPANY, "boson sampling v časových binech",
                    GbsVerdict.THEORETICALLY, "zdroj na sestupné konverzi a detektory počtu fotonů; oficiálně jednotlivé fotony"),
    PhotonicsPlayer("PsiQuantum", "USA", PlayerKind.COMPANY, "fúzní výpočty s jednotlivými fotony",
                    GbsVerdict.THEORETICALLY, "zdroje jsou ohlašované (fyzikálně dvoumódové stlačení), GBS nepublikovali"),
    PhotonicsPlayer("Quandela", "Francie", PlayerKind.COMPANY, "jednotlivé fotony z kvantových teček",
                    GbsVerdict.NO, "boson sampling ano, stlačené světlo ne (viz stránka o Quandele)"),
    PhotonicsPlayer("QuiX Quantum", "Nizozemsko", PlayerKind.COMPANY, "programovatelné interferometry SiN",
                    GbsVerdict.COMPONENTS, "jejich čip je srdcem PaQS; vlastní cloud a počítač s jednotlivými fotony"),
    PhotonicsPlayer("Sparrow Quantum", "Dánsko", PlayerKind.COMPANY, "zdroje jednotlivých fotonů",
                    GbsVerdict.COMPONENTS, "partner Qpurpose; vede k boson samplingu, ne ke GBS"),
    PhotonicsPlayer("Ligentec", "Švýcarsko", PlayerKind.COMPANY, "slévárna čipů SiN",
                    GbsVerdict.COMPONENTS, "vyrobila Xanaduův čip X8 se zdroji stlačeného světla"),
    PhotonicsPlayer("Ephos", "Itálie", PlayerKind.COMPANY, "laserem psané skleněné čipy",
                    GbsVerdict.COMPONENTS, "interferometry až 200 módů; v roce 2026 se přeorientovává"),
    PhotonicsPlayer("Thorlabs", "USA", PlayerKind.COMPANY, "katalog optiky",
                    GbsVerdict.COMPONENTS, "krystaly PPKTP a optika ano, programovatelné interferometry a detektory počtu fotonů ne"),
    PhotonicsPlayer("Quantum Computing Inc. (QCi)", "USA", PlayerKind.COMPANY, "slévárna TFLN, „entropy computing“",
                    GbsVerdict.COMPONENTS, "materiál vhodný pro GBS, tvrzení o výkonu sporná"),
    PhotonicsPlayer("Univerzita Twente (Renema)", "Nizozemsko", PlayerKind.RESEARCH, "boson sampling pro Monte Carlo",
                    GbsVerdict.NO, "Monte Carlo s jednotlivými fotony, ne GBS; patentová přihláška"),
    PhotonicsPlayer("Sapienza Řím (Sciarrino)", "Itálie", PlayerKind.RESEARCH, "boson sampling s kvantovými tečkami",
                    GbsVerdict.NO, "vlastní GBS nemá; ověřovala Borealis přes cloud"),
    PhotonicsPlayer("Aegiq", "Velká Británie", PlayerKind.COMPANY, "kvantové tečky a křemíková fotonika",
                    GbsVerdict.NO, "jednotlivé fotony, stroj v NQCC"),
    PhotonicsPlayer("Quantum Source", "Izrael", PlayerKind.COMPANY, "deterministická hradla foton–atom",
                    GbsVerdict.NO, "klastrové stavy pro odolné výpočty"),
    PhotonicsPlayer("Nu Quantum", "Velká Británie", PlayerKind.COMPANY, "fotonické propojení kvantových počítačů",
                    GbsVerdict.NO, "sítě, ne výpočet"),
    PhotonicsPlayer("Photonic Inc.", "Kanada", PlayerKind.COMPANY, "spinové qubity v křemíku s optickým rozhraním",
                    GbsVerdict.NO, "fotony jen propojují qubity"),
    PhotonicsPlayer("Infleqtion (dříve ColdQuanta)", "USA", PlayerKind.COMPANY, "neutrální atomy",
                    GbsVerdict.NO, "není fotonický počítač, světlo jen ovládá atomy"),
    PhotonicsPlayer("Pasqal", "Francie", PlayerKind.COMPANY, "neutrální atomy v optických pinzetách",
                    GbsVerdict.NO, "není fotonický počítač; analogie GBS jen u grafových úloh"),
    PhotonicsPlayer("ČVUT FJFI (Jex, Hamilton)", "Česko", PlayerKind.RESEARCH, "teorie boson samplingu",
                    GbsVerdict.NO, "spoluautoři původního GBS, ale bez experimentu; most do Paderbornu"),
    PhotonicsPlayer("Univerzita Palackého Olomouc, katedra optiky", "Česko", PlayerKind.RESEARCH,
                    "kvantová optika, detekce počtu fotonů", GbsVerdict.NO,
                    "měření fotonové statistiky; vlastní zdroj stlačeného světla pro GBS neověřen"),
    PhotonicsPlayer("IT4Innovations, VŠB-TU Ostrava", "Česko", PlayerKind.RESEARCH, "supravodivý počítač VLQ, HPC",
                    GbsVerdict.NO, "GBS jen převedené na hradlový program (projekt ESA GBS4EO, neověřeno)"),
)
"""Verdict per player; the chapters give the sources."""

JIUZHANG_3 = Source(
    "Deng, Y.-H. a kol.: *Gaussian boson sampling with pseudo-photon-number-resolving detectors and quantum "
    "computational advantage*. Physical Review Letters 131, 150601 (2023), "
    "[arXiv:2304.12240](https://arxiv.org/abs/2304.12240)"
)
XANADU_X8 = Source(
    "Arrazola, J. M. a kol.: *Quantum circuits with many photons on a programmable nanophotonic chip*. Nature 591, 54 "
    "(2021), [doi:10.1038/s41586-021-03202-1](https://doi.org/10.1038/s41586-021-03202-1) – čip vyrobený u Ligentec"
)
XANADU_AURORA = Source(
    "*Scaling and networking a modular photonic quantum computer*. Nature 638, 912 (2025), "
    "[doi:10.1038/s41586-024-08406-9](https://doi.org/10.1038/s41586-024-08406-9) – Aurora"
)
XANADU_ROADMAP = Source(
    "Quantum Computing Report: [Xanadu unveils technical roadmap targeting 1,000 logical qubits by 2031]"
    "(https://quantumcomputingreport.com/xanadu-unveils-technical-roadmap-targeting-1000-logical-qubits-by-2031/), 2026"
)
XANADU_RESULTS = Source(
    "Xanadu: [výsledky za rok 2025](https://stocktitan.net/news/XNDU/xanadu-announces-fourth-quarter-and-full-year-2025-"
    "12l2bdb3wznh.html), duben 2026 – firma kótovaná jako XNDU"
)
STRAWBERRY_FIELDS_ARCHIVED = Source(
    "GitHub: [XanaduAI/strawberryfields](https://github.com/XanaduAI/strawberryfields) a "
    "[XanaduAI/thewalrus](https://github.com/XanaduAI/thewalrus) – v roce 2026 archivované"
)
PSIQUANTUM_OMEGA = Source(
    "*A manufacturable platform for photonic quantum computing*. Nature 641, 876 (2025), "
    "[doi:10.1038/s41586-025-08820-7](https://doi.org/10.1038/s41586-025-08820-7) – čipy Omega od PsiQuantum"
)
PSIQUANTUM_AUSTRALIA = Source(
    "PsiQuantum: [stavba počítače v Austrálii](https://www.psiquantum.com/news-import/psiquantum-to-build-worlds-first-"
    "utility-scale-fault-tolerant-quantum-computer-in-australia), 2024"
)
ORCA_PT3 = Source(
    "ORCA Computing: [PT-3](https://orcacomputing.com/orca-computing-launches-pt-3-the-first-quantum-computer-built-for-"
    "commercial-quantum-advantage/), říjen 2026 – 64 fotonů ve 128 módech"
)
CUDAQ_PHOTONIC = Source(
    "NVIDIA: [CUDA-Q – fotonický hardware](https://nvidia.github.io/cuda-quantum/latest/using/backends/hardware/"
    "photonic.html) – rozhraní pro ORCA PT"
)
TURINGQ_PREPRINT = Source(
    "*A chip-scale space-time multiplexed Gaussian boson sampling processor beyond 10,000 photons*, "
    "[arXiv:2609.11922](https://arxiv.org/abs/2609.11922) (2026) – TuringQ a SJTU, nerecenzováno"
)
IMPERIAL_DISPLACEMENT = Source(
    "Thekkadath, G. S. a kol.: *Experimental demonstration of Gaussian boson sampling with displacement*. PRX Quantum 3, "
    "020336 (2022), [doi:10.1103/PRXQuantum.3.020336](https://doi.org/10.1103/PRXQuantum.3.020336)"
)
SAPIENZA_BOREALIS = Source(
    "*Validation of a noisy Gaussian boson sampler via graph theory*, [arXiv:2306.12120](https://arxiv.org/abs/2306.12120)"
    " (2023) – Sapienza ověřuje Borealis přes cloud"
)
SQUASHED_STATES = Source(
    "*Classical models may be a better explanation of the Jiuzhang 1.0 Gaussian boson sampler than its targeted "
    "squeezed light model*. Quantum 7, 1076 (2023), [arXiv:2207.10058](https://arxiv.org/abs/2207.10058)"
)
GBS_BENCHMARK_2026 = Source(
    "*Gaussian boson sampling: benchmarking quantum advantage*, [arXiv:2604.12330](https://arxiv.org/abs/2604.12330) "
    "(2026) – klasický algoritmus proti experimentům"
)
NTT_SQUEEZING = Source(
    "Hirota, K. a kol.: *Generation of 10-dB squeezed light from a broadband waveguide optical parametric amplifier*, "
    "[arXiv:2511.15082](https://arxiv.org/abs/2511.15082) (2025) – NTT a Tokijská univerzita"
)
OPTQC_PLATFORM = Source(
    "Yokoyama, S. a kol.: *A full-stack analog optical quantum computing platform with one hundred inputs*, "
    "[arXiv:2506.16147](https://arxiv.org/abs/2506.16147) (2025) – RIKEN, OptQC, NTT"
)
OPTQC_MOQUREN = Source(
    "AIST: [spuštění stroje MoQuren od OptQC](https://www.aist.go.jp/aist_e/news/au20260722.html), červenec 2026"
)
DTU_CLUSTER = Source(
    "Larsen, M. V. a kol.: *Deterministic generation of a two-dimensional cluster state*. Science 366, 369 (2019), "
    "[arXiv:1906.08709](https://arxiv.org/abs/1906.08709)"
)
DTU_GBS_PATENT = Source(
    "DTU: [System and method for Gaussian boson sampling](https://orbit.dtu.dk/en/publications/system-and-method-for-"
    "gaussian-boson-sampling) – patentová přihláška WO2024038212"
)
PHOQUANT_PROJECT = Source(
    "Universität Paderborn: [projekt PhoQuant](https://www.uni-paderborn.de/en/project/191) – fotonický počítač "
    "založený na GBS, aspoň 100 kanálů, algoritmy přes cloud"
)
PHOQUANT_ATLAS = Source(
    "Quantensysteme Projektatlas: [PhoQuant](https://www.quantensysteme.info/projektatlas/projekte/q/phoquant) – "
    "koordinátor Fraunhofer IOF Jena, 1/2022–6/2027, 84,8 % hradí BMFTR"
)
QANT_FUNDING = Source(
    "Q.ANT: [financování a procesor NPU](https://qant.com/?p=9101) – analogové fotonické počítání pro AI"
)
QUIX_20_MODES = Source(
    "Taballione, C. a kol.: *20-mode universal quantum photonic processor*. Quantum 7, 1071 (2023), "
    "[arXiv:2203.01801](https://arxiv.org/abs/2203.01801)"
)
QUIX_CARINA = Source(
    "PostQuantum: [QuiX Carina](https://postquantum.com/industry-news/quix-carina-universal-photonic/) – univerzální "
    "fotonický počítač pro DLR, 2026"
)
SPARROW_SOURCE = Source(
    "Zahalka, P. a kol.: *A photonic source with half-a-GHz single-photon flux*, "
    "[arXiv:2609.05387](https://arxiv.org/abs/2609.05387) (2026) – Sparrow Quantum"
)
AEGIQ_NQCC = Source(
    "Quantum Computing Report: [Aegiq v NQCC](https://quantumcomputingreport.com/aegiq-commissions-photonic-quantum-"
    "computer-with-integrated-chip-technology-at-uks-nqcc/), 2025"
)
QUANTUM_SOURCE_ORIGIN = Source(
    "Quantum Computing Report: [Quantum Source ORIGIN](https://quantumcomputingreport.com/quantum-source-addresses-"
    "photonic-scaling-with-origin-a-deterministic-resource-state-generator/), 2025"
)
EPHOS_FUNDING = Source(
    "The Quantum Insider: [Ephos – skleněné fotonické čipy](https://thequantuminsider.com/2024/09/24/glass-based-photonic"
    "-chip-startup-ephos-secures-8-5m-to-innovate-quantum-computing-and-ai-infrastructure/), 2024"
)
NU_QUANTUM = Source(
    "Tech.eu: [Nu Quantum, série A](https://tech.eu/2025/12/10/university-of-cambridge-quantum-spinout-nets-record-60m-"
    "series-a/), 2025"
)
PHOTONIC_INC = Source(
    "Bergeron, L. a kol. (Photonic Inc.): *Optical observation of single spins in silicon*. Nature 607, 266 (2022), "
    "[doi:10.1038/s41586-022-04821-y](https://doi.org/10.1038/s41586-022-04821-y)"
)
QCI_CRITIQUE = Source(
    "*A critical comment on „Entropy computing“*, [arXiv:2605.03612](https://arxiv.org/abs/2605.03612) (2026) – "
    "kritika tvrzení QCi"
)
INFLEQTION_TECHNOLOGY = Source(
    "Infleqtion: [technologie](https://infleqtion.com/technology) – neutrální atomy, hodiny a senzory"
)
PASQAL_CREDIT_AGRICOLE = Source(
    "Pasqal: [partnerství s Crédit Agricole CIB](https://www.pasqal.com/newsroom/credit-agricole-cib-and-pasqal-advance-"
    "their-strategic-partnership-to-deploy-quantum-computing-applied-to-finance/), 2026"
)
PASQAL_RISK = Source(
    "Leclerc, L. a kol.: *Financial risk management on a neutral atom quantum processor*, "
    "[arXiv:2212.03223](https://arxiv.org/abs/2212.03223) (2022)"
)
PASQAL_KERNEL = Source(
    "Henry, L.-P. a kol.: *Quantum evolution kernel: machine learning on graphs with programmable arrays of qubits*, "
    "[arXiv:2107.03247](https://arxiv.org/abs/2107.03247) (2021)"
)
THORLABS_DETECTORS = Source(
    "Thorlabs: [detektory jednotlivých fotonů](https://www.thorlabs.com/single-photon-detectors) a "
    "[krystaly PPKTP](https://www.thorlabs.com/ppktp-crystals-for-spontaneous-parametric-down-conversion-spdc)"
)
IDQ_SNSPD = Source(
    "ID Quantique: [ID281 SNSPD](https://www.idquantique.com/quantum-detection-systems/products/id281-snspd-system/) – "
    "vícepixelové detektory rozlišující až 8 fotonů"
)
SINGLE_QUANTUM = Source("Single Quantum: [technologie](https://singlequantum.com/technology) – detektory SNSPD, Delft")
PIXEL_PHOTONICS = Source(
    "Pixel Photonics: [detektory integrované do vlnovodu](https://www.pixelphotonics.com/en/single-photon-detector-products/)"
)
PHOTON_SPOT = Source("Photon Spot: [detektory SNSPD](https://www.photonspot.com/detectors)")
QUANTUM_OPUS = Source("Quantum Opus: [Opus One](https://www.quantumopus.com/) – detektory „PNR ready“")
SIMIT_SNSPD = Source(
    "Ding, C. a kol.: *Photon-number-resolving single-photon detector with a system detection efficiency of 98%*, "
    "[arXiv:2504.02202](https://arxiv.org/abs/2504.02202) (2025)"
)
XANADU_TES = Source(
    "The Quantum Insider: [Xanadu a Applied Materials – detektory TES na 300mm deskách]"
    "(https://thequantuminsider.com/2025/05/05/xanadu-applied-materials-collaborate-on-transition-edge-sensors-for-"
    "scalable-photonic-quantum-systems/), 2025"
)
RAICOL = Source("Raicol Crystals: [krystaly a vlnovody PPKTP](https://raicol.com/)")
COVESION = Source("Covesion: [krystaly a vlnovody PPLN](https://covesion.com/) – spolu s AdvR v Hawthorn Photonics")
HC_PHOTONICS = Source("HC Photonics: [čipy a vlnovody PPLN](https://www.hcphotonics.com/)")
NOISY_LABS = Source(
    "Universität Hamburg: [stlačené světlo a firma Noisy Labs]"
    "(https://www.physik.uni-hamburg.de/en/iqp/ag-schnabel/forschung/gequetschtes-licht.html) – spojité zdroje"
)
LIGENTEC = Source("Ligentec: [slévárna nitridu křemíku](https://www.ligentec.com/), Švýcarsko")
LIONIX = Source("LioniX International: [platforma TriPleX](https://www.lionix-international.com/), Nizozemsko")
CCRAFT = Source(
    "optics.org: [CSEM zakládá slévárnu niobičnanu lithného CCRAFT]"
    "(https://optics.org/news/csem-spins-off-lithium-niobate-photonic-integrated-circuit-foundry), 2025"
)
BLUEFORS = Source(
    "The Quantum Insider: [Bluefors PT205 pro detektory SNSPD](https://thequantuminsider.com/2025/03/18/bluefors-"
    "announces-compact-high-performance-pt205-pulse-tube-cryocooler-designed-for-quantum-sensing-and-communication-"
    "applications/), 2025"
)
PIQUASSO_PAPER = Source(
    "Kolarovszki, Z. a kol.: *Piquasso: a photonic quantum computer simulation software platform*. Quantum 9, 1708 "
    "(2025), [quantum-journal.org](https://quantum-journal.org/papers/q-2025-04-15-1708/)"
)
BOSONIC_QISKIT = Source("C2QA: [Bosonic Qiskit](https://github.com/C2QA/bosonic-qiskit) – bosonické módy vedle qubitů")
OLOMOUC_PNR = Source(
    "Hloušek, J. a kol.: *Accurate detection of arbitrary photon statistics*. Physical Review Letters 123, 153604 "
    "(2019), [arXiv:1812.02262](https://arxiv.org/abs/1812.02262) – Univerzita Palackého Olomouc"
)
XANADU_BANKS = Source(
    "BetaKit: [Xanadu, BMO and Scotiabank joint project uses quantum for trading products]"
    "(https://betakit.com/xanadu-bmo-scotiabank-joint-project-uses-quantum-for-trading-products/), 21. 8. 2019"
)
HSBC_IBM = Source(
    "Ciceri, A. a kol.: *Enhanced fill probability estimates in institutional algorithmic bond trading using "
    "statistical learning algorithms with quantum computers*, [arXiv:2509.17715](https://arxiv.org/abs/2509.17715) "
    "(2025) – HSBC a IBM"
)
CLASSIQ_MIZUHO = Source(
    "The Quantum Insider: [Classiq se Sumitomo a Mizuho-DL Financial Technology]"
    "(https://thequantuminsider.com/2025/03/25/classiq-powers-quantum-advance-with-sumitomo-corporation-and-mizuho-dl-"
    "financial-technology/), 2025 – kvantové Monte Carlo pro úvěrová portfolia"
)
QC_WARE_GOLDMAN = Source(
    "The Quantum Insider: [Goldman Sachs a QC Ware – mělké Monte Carlo]"
    "(https://thequantuminsider.com/2021/04/30/goldman-sachs-and-qc-ware-collaboration-brings-new-way-to-price-risky-"
    "assets-within-reach-of-quantum-computers/), 2021"
)
MULTIVERSE_BBVA = Source(
    "BBVA: [BBVA and Multiverse showcase how quantum computing could help optimize investment portfolio management]"
    "(https://www.bbva.com/en/bbva-and-multiverse-showcase-how-quantum-computing-could-help-optimize-investment-"
    "portfolio-management)"
)
MCKINSEY_MONITOR = Source(
    "PostQuantum: [shrnutí McKinsey Quantum Technology Monitor 2026]"
    "(https://postquantum.com/industry-news/mckinsey-quantum-monitor-2026/) – investice do kvantových start-upů"
)
PSIQUANTUM_SERIES_E = Source(
    "Pulse 2.0: [PsiQuantum získal 1 mld. USD při ocenění 7 mld. USD]"
    "(https://pulse2.com/psiquantum-1-billion-at-7-billion-valuation-raised-for-building-fault-tolerant-quantum-"
    "computers), září 2025"
)
VLQ_INAUGURATION = Source(
    "e-INFRA CZ: [LUMI-Q consortium unveils the VLQ quantum computer]"
    "(https://www.e-infra.cz/en/news/lumi-q-consortium-unveils-the-vlq-quantum-computer-for-the-czech-and-european-"
    "science-community), září 2025"
)
CNB_FX_RESERVES = Source(
    "Veselý, M.: *Finding the Optimal Currency Composition of Foreign Exchange Reserves with a Quantum Computer*. "
    "CNB Working Paper 1/2023, [cnb.cz](https://www.cnb.cz/en/economic-research/research-publications/cnb-working-"
    "paper-series/Finding-the-Optimal-Currency-Composition-of-Foreign-Exchange-Reserves-with-anbspQuantum-Computer-"
    "00001)"
)
QUANTERA = Source("QuantERA: [členové konsorcia](https://quantera.eu/consortium/) – za Česko MŠMT a TA ČR")
CTU_GROUP = Source(
    "ČVUT FJFI: [kvantová dynamika, optika a informatika](https://kf.fjfi.cvut.cz/cz/vyzkum/smery-vyzkumu/kvantova-"
    "dynamika-optika-informatika) – skupina I. Jexe",
    czech=True,
)

CHAIN_TOPIC = TheoryTopic(
    anchor="svet-co-je-potreba",
    title="Co je potřeba pro GBS a jak číst verdikty",
    in_short=(
        "GBS potřebuje tři věci: pulzní zdroj stlačeného vakua, programovatelný interferometr a detektory, které umějí "
        "spočítat fotony. Kdo má všechny tři a GBS předvedl, „postavil GBS“; kdo má stlačené světlo, ale ne celý "
        "řetězec, ho „teoreticky“ umí; kdo dodává jen část, dodává „komponenty“."
    ),
    explanation=r"""
**Řetězec GBS.**

1. **Zdroj stlačeného vakua** – nelineární krystal nebo vlnovod (PPKTP, PPLN, niobičnan lithný na izolátoru) čerpaný
   pulzním laserem. Pro GBS musí být pulzní a jednomódový; spojité zdroje pro gravitační detektory nestačí.
2. **Programovatelný interferometr** – síť děličů svazku a fázových posuvů na čipu (nitrid křemíku, sklo, niobičnan
   lithný) nebo ve vláknových smyčkách s časovými biny.
3. **Detektory počtu fotonů** – supravodivé TES (skutečné rozlišení počtu) nebo vícepixelové SNSPD (rozliší nejvýš
   tolik fotonů, kolik mají pixelů). S prahovými detektory („cvakne / necvakne“) vycházejí místo hafniánů torontiány.
4. **Chlazení** detektorů na 1–4 K a **software** pro řízení a simulaci.

**Verdikty v tabulce na konci.**

- *postavil GBS* – skupina nebo firma GBS experimentálně předvedla (recenzovaně, případně preprint – je uvedeno);
- *teoreticky* – má zdroje stlačeného světla nebo podobný stroj, ale GBS nenabízí ani nepředvedla;
- *jen komponenty* – vyrábí část řetězce (čipy, zdroje, detektory);
- *ne* – jiná technologie (jednotlivé fotony, atomy, sítě) bez stlačeného světla.

**Proč to rozlišujeme.** Odhady Andersena a Shan potřebují rozdělení s hafniány, tedy skutečné GBS. Stroj
s jednotlivými fotony (permanenty) umí jen obdobu, kterou rozebírá stránka o Quandele.
""",
    further_reading=(
        Reading(HAMILTON, "původní návrh GBS"),
        Reading(MADSEN, "Borealis jako vzor celého řetězce"),
    ),
)

BUILT_TOPIC = TheoryTopic(
    anchor="svet-kdo-postavil-gbs",
    title="Kdo GBS skutečně postavil",
    in_short=(
        "Velké GBS stroje postavily jen čínská USTC (Jiuzhang, naposledy přes 8 000 módů) a kanadský Xanadu (Borealis, "
        "dnes vyřazený). V Evropě běží PaQS v Paderbornu. Menší GBS předvedly Imperial, Bristol a nově čínský TuringQ "
        "– ten zatím jen v preprintu."
    ),
    explanation=r"""
**USTC Hefei (Jian-Wei Pan, Chao-Yang Lu), Čína.** Jiuzhang 1.0 (2020, 100 módů, 76 kliků), 2.0 (2021, 144 módů,
programovatelné fáze), 3.0 (2023, až 255 kliků s pseudo-rozlišením počtu fotonů) a 4.0 (Nature, květen 2026:
1 024 stlačených stavů v 8 176 módech, až 3 050 detekcí). Přístup zvenčí ani cloud nenabízí.

**Xanadu, Toronto.** Čip X8 (2021, 8 módů stlačeného světla, vyrobený ve slévárně Ligentec) a Borealis (2022,
216 módů v časových binech, detektory TES s účinností 95 %). Borealis byl v roce 2023 dostupný v cloudu – skupina
ze Sapienzy ho tak ověřovala –, pak ho Xanadu stáhl. Dnes se firma soustředí na qubity GKP (stroj Aurora 2025,
plán 1 000 logických qubitů do 2031) a je kótovaná na burze; veřejný cloud ani GBS už nenabízí.

**Univerzita Paderborn (Christine Silberhorn), Německo.** Stroj PaQS (2024, článek 2025–2026): stlačené vakuum
z vlnovodu PPKTP, dvanáctimódový čip QuiX a detektory rozlišující až tři fotony; porovnává gaussovské
a negaussovské vstupy. Postaven v projektu PhoQuant. Přístup přes výzkumnou spolupráci.

**Menší GBS.** Imperial College (Walmsley): GBS s posunutím na 15 módech a GBS pro husté podgrafy. Bristol
(Paesani a kol. 2019): GBS na křemíkovém čipu se zdroji stlačeného světla. McMahonova skupina (Cornell) využila GBS
s více než 400 módy pro rezervoárové počítání.

**TuringQ, Šanghaj.** Preprint ze září 2026: GBS na čipu z niobičnanu lithného s multiplexem v prostoru i čase,
přes 10 000 detekovaných fotonů za milisekundu. Recenze zatím chybí a firma tvrdí kvantovou výhodu.

**Pozor na „kvantovou výhodu“.** Klasické modely („squashed states“) vysvětlují Jiuzhang 1.0 lépe než ideální GBS
a klasické algoritmy z roku 2026 napodobí experimenty až do zhruba 1 000 módů. Pro výzkum odhadů rizika to
znamená: výhodu je potřeba dokazovat na úloze, ne na rekordu ve vzorkování.
""",
    further_reading=(
        Reading(ZHONG, "Jiuzhang 1.0"),
        Reading(ZHONG_2021, "Jiuzhang 2.0"),
        Reading(JIUZHANG_3),
        Reading(JIUZHANG_4),
        Reading(XANADU_X8),
        Reading(MADSEN, "Borealis"),
        Reading(BOREALIS_RETIRED),
        Reading(SAPIENZA_BOREALIS),
        Reading(PAQS_PAPER),
        Reading(PADERBORN_PAQS),
        Reading(IMPERIAL_DISPLACEMENT),
        Reading(PAESANI_CHIP),
        Reading(CIMINI_RESERVOIR, "McMahonova skupina, Cornell"),
        Reading(TURINGQ_PREPRINT),
        Reading(SQUASHED_STATES),
        Reading(GBS_BENCHMARK_2026),
        Reading(OH_CLASSICAL_SIMULATION),
    ),
)

SQUEEZED_TOPIC = TheoryTopic(
    anchor="svet-stlacene-svetlo",
    title="Stlačené světlo bez GBS: kdo by to teoreticky uměl",
    in_short=(
        "Stlačené světlo umějí japonské NTT a OptQC, dánská DTU a Xanadu, ale nikdo z nich dnes GBS nenabízí. "
        "Nejblíž veřejnému GBS jsou DTU (projekt PhotoQ) a německý projekt PhoQuant (Jena, Paderborn); u obou je spuštění "
        "zatím neověřené."
    ),
    explanation=r"""
**NTT a OptQC, Japonsko.** NTT má jedny z nejlepších zdrojů stlačeného světla (vlnovodový zesilovač, 10 dB). Spolu
s Furusawovou skupinou a RIKEN postavili analogový optický počítač se stovkou vstupů a cloudem; OptQC (spin-off
z roku 2024) spustil v červenci 2026 stroj MoQuren. Všechny ale **měří homodynně** – amplitudy pole, ne počty
fotonů – a takové gaussovské obvody jdou efektivně simulovat klasicky. Pro GBS by potřebovaly detektory počtu
fotonů.

**DTU Kodaň (Ulrik Andersen).** Stlačené světlo a klastrové stavy s desítkami tisíc módů, patentová přihláška na
GBS s časovým multiplexem a projekt PhotoQ, který staví GBS dostupný přes cloud. Experiment GBS jsme zatím
nenašli; dostupnost cloudu je neověřená.

**PhoQuant, Německo.** Národní projekt (asi 49 mil. €, leden 2022 – červen 2027) vedený Fraunhofer IOF Jena,
s Paderbornem, Q.ANT, HQS, Menlo Systems a dalšími. Paderborn ho popisuje jako fotonický počítač založený na GBS
s aspoň 100 kanály a algoritmy přes cloud; stroj PaQS je jeho mezikrok. Spuštění cloudu jsme k datu rešerše
neověřili. Q.ANT (Stuttgart, spin-off firmy TRUMPF) je v projektu partner; sám prodává analogové fotonické procesory
pro AI – klasickou optiku, ne kvantový počítač.

**Xanadu Aurora.** Stále obsahuje desítky zdrojů stlačeného světla a detektory počtu fotonů, ale slouží ke
klastrovým stavům a opravě chyb, ne ke GBS.

**PsiQuantum a ORCA.** Jejich zdroje fotonových párů (čtyřvlnné směšování, sestupná konverze) jsou fyzikálně slabé
dvoumódové stlačení, ze kterého ohlašováním vznikají jednotlivé fotony. PsiQuantum GBS nepublikoval a hardware
nezpřístupňuje. U ORCA PT-2 se zdroje rozcházejí – nezávislý benchmark mluví o fotonově odčítaných stlačených
stavech, ORCA o jednotlivých fotonech; před případným využitím je třeba se zeptat přímo ORCA.
""",
    further_reading=(
        Reading(NTT_SQUEEZING),
        Reading(OPTQC_PLATFORM),
        Reading(OPTQC_MOQUREN),
        Reading(DTU_CLUSTER),
        Reading(DTU_GBS_PATENT),
        Reading(DTU_PHOTOQ),
        Reading(PHOQUANT_PROJECT),
        Reading(PHOQUANT_ATLAS),
        Reading(QANT_FUNDING),
        Reading(XANADU_AURORA),
        Reading(XANADU_ROADMAP),
        Reading(XANADU_RESULTS),
        Reading(PSIQUANTUM_OMEGA),
        Reading(PSIQUANTUM_AUSTRALIA),
        Reading(PARK_PT2),
        Reading(BACARREZA_PT2),
    ),
)

SINGLE_PHOTON_TOPIC = TheoryTopic(
    anchor="svet-jednotlive-fotony",
    title="Jednotlivé fotony: boson sampling a cesta k univerzálnímu počítači",
    in_short=(
        "Většina evropských fotonických firem pracuje s jednotlivými fotony: Quandela, QuiX, ORCA, Sparrow, Aegiq. "
        "Umějí boson sampling (permanenty), ne GBS. Twente ukázala boson sampling jako urychlovač Monte Carla – "
        "nejbližší konkurenční linie k disertaci."
    ),
    explanation=r"""
**QuiX Quantum (Enschede, Nizozemsko).** Spin-off Univerzity Twente (2019): programovatelné interferometry
z nitridu křemíku (20 módů s průměrnou ztrátou 2,9 dB), cloudová služba Bia (2–4 fotony, 12–20 kanálů), série A
15 mil. € (2025) a univerzální počítač Carina pro německé DLR (2026). Jejich čip je interferometrem stroje PaQS –
pro GBS jsou tedy dodavatelem klíčové součásti.

**ORCA Computing (Londýn).** Spin-off Oxfordu (2019): boson sampling v časových binech se smyčkami ve vlákně.
PT-1 v polském PSNC, PT-2 (2024) a PT-3 (říjen 2026, 64 fotonů ve 128 módech) v londýnském datacentru; přístup
přes vlastní SDK a NVIDIA CUDA-Q. Qpurpose s ORCA podle své stránky řeší gaussovsky vážené integrály.

**Sparrow Quantum (Kodaň).** Zdroje jednotlivých fotonů z kvantových teček (spin-off Institutu Nielse Bohra,
2015); v září 2026 rekordní tok přes 500 milionů fotonů za sekundu. Partner Qpurpose – ta pro boson sampling
„očekává“ podobné zrychlení jako u GBS, výsledek zatím nepublikovala.

**Další.** Aegiq (Sheffield) – stroj s kvantovými tečkami v britském NQCC; Quantum Source (Izrael) – deterministická
hradla foton–atom pro klastrové stavy; Ephos (Milán) – laserem psané skleněné čipy s až 200 módy, v roce 2026 se ale
přeorientovává na pouzdření čipů.

**Univerzita Twente (Jelmer Renema).** Boson sampling jako urychlovač Monte Carla (2025): tři fotony ze sestupné
konverze na dvanáctimódovém čipu, aplikace z fyziky, ne z financí. K metodě patentová přihláška – pro komerční
využití to je důležité.

**Sapienza Řím (Fabio Sciarrino).** Boson sampling s kvantovými tečkami na 128módových skleněných čipech,
koordinátor projektu PHOQUSING.
""",
    further_reading=(
        Reading(QUIX_20_MODES),
        Reading(QUIX_BIA),
        Reading(QUIX_CARINA),
        Reading(ORCA_PT3),
        Reading(CUDAQ_PHOTONIC),
        Reading(QPURPOSE_PARTNERSHIPS),
        Reading(SPARROW_SOURCE),
        Reading(AEGIQ_NQCC),
        Reading(QUANTUM_SOURCE_ORIGIN),
        Reading(EPHOS_FUNDING),
        Reading(ANGUITA_MONTE_CARLO_ACCELERATOR),
        Reading(TWENTE_PATENT),
        Reading(PHOQUSING),
        Reading(WANG_TWENTY_PHOTONS, "boson sampling s 20 fotony z USTC"),
    ),
)

OTHER_TOPIC = TheoryTopic(
    anchor="svet-jine-technologie",
    title="Není to fotonický počítač: atomy, sítě a klasická optika",
    in_short=(
        "ColdQuanta (dnes Infleqtion) a Pasqal jsou počítače s neutrálními atomy – světlo v nich jen ovládá atomy. "
        "Photonic Inc. a Nu Quantum používají fotony k propojení qubitů, iPronics a procesor Q.ANT jsou klasická "
        "optika. Pro GBS nic z toho nepoužijeme."
    ),
    explanation=r"""
**Infleqtion (dříve ColdQuanta), Boulder.** Neutrální atomy (stroj Sqale, 100 fyzikálních qubitů v britském NQCC),
optické hodiny a senzory. Lasery atomy chladí a drží, ale výpočet probíhá v atomech. Od února 2026 kótovaná
na NYSE.

**Pasqal, Palaiseau (ze seznamu „Pascal“).** Atomy rubidia v optických pinzetách, stroje pro HPCQS ve Francii
a v Jülichu, od srpna 2026 na Nasdaqu. Ve financích dlouhodobě spolupracuje s Crédit Agricole CIB (předpověď
zhoršení ratingu, 2022; strategické partnerství 2026). Nejbližší obdobou GBS je jejich „quantum evolution kernel“
pro grafy – pravděpodobnosti ale nejsou hafniány, takže odhad typu GBS-P z něj nevznikne.

**Photonic Inc.** (Kanada) – spinové qubity v křemíku s optickým rozhraním; **Nu Quantum** (Cambridge) – fotonické
propojení iontových a atomových počítačů; **Quantum Computing Inc.** (USA) – slévárna niobičnanu lithného a stroj
Dirac-3, jehož tvrzení o výkonu zpochybňuje kritický preprint i žaloby akcionářů; **iPronics** (Valencie) – klasické
optické přepínače pro datacentra.
""",
    further_reading=(
        Reading(INFLEQTION_TECHNOLOGY),
        Reading(PASQAL_CREDIT_AGRICOLE),
        Reading(PASQAL_RISK),
        Reading(PASQAL_KERNEL),
        Reading(PHOTONIC_INC),
        Reading(NU_QUANTUM),
        Reading(QCI_CRITIQUE),
    ),
)

SUPPLY_TOPIC = TheoryTopic(
    anchor="svet-dodavatele",
    title="Dodavatelé: zdroje, čipy, detektory a chlazení",
    in_short=(
        "Interferometry a detektory se dají koupit; pulzní zdroj stlačeného světla pro GBS v katalogu nikdo nenabízí "
        "– staví se z krystalů PPKTP nebo PPLN, případně na čipu. Thorlabs dodá optiku a krystaly, ale ne "
        "programovatelný interferometr ani detektory počtu fotonů."
    ),
    explanation=r"""
**Zdroje stlačeného světla a nelineární krystaly.** Krystaly a vlnovody PPKTP (Raicol, Izrael; AdvR a Covesion,
dnes Hawthorn Photonics) a PPLN (HC Photonics, Tchaj-wan; NTT). Komerční „stlačený laser“ nabízí hamburská Noisy
Labs, ale spojitý – pro GBS je potřeba pulzní jednomódový zdroj, který zatím staví každá skupina sama.

**Čipy a slévárny.** Nitrid křemíku: Ligentec (Švýcarsko – vyrobila Xanaduův čip X8), LioniX a QuiX (Nizozemsko),
imec (Belgie), GlobalFoundries (čipy PsiQuantum). Niobičnan lithný na izolátoru, vhodný pro zdroje i rychlé
přepínání: CCRAFT (Švýcarsko, bývalý CSEM), HyperLight (USA), Lightium (Švýcarsko), interní linka Q.ANT, QCi.

**Detektory počtu fotonů.** Vícepixelové SNSPD: ID Quantique (Ženeva, až 8 fotonů), Single Quantum (Delft), Photon
Spot a Quantum Opus (USA), Pixel Photonics (Münster, detektory přímo ve vlnovodu). Skutečné TES vyrábí jen NIST
a AIST pro výzkum; Xanadu s Applied Materials je zavádí do výroby. Křemíkové SPAD (Thorlabs, Hamamatsu, Excelitas)
počet fotonů nerozliší.

**Chlazení.** Detektory běží při 1–4 K: Bluefors (Finsko), ICEoxford (Spojené království), Montana Instruments
(Atlas Copco), attocube (Německo – chlazení pro Quandelin stroj Lucy). Výrobci SNSPD dodávají kryostat v sadě.

**Thorlabs (USA).** Zdroj fotonových párů SPDC810, krystaly PPKTP (výslovně i pro stlačené světlo), balancované
detektory pro homodynní měření a výukové sady. Pro malý laboratorní experiment dobrý dodavatel optiky; jádro GBS
(programovatelný interferometr, detektory počtu fotonů, pulzní squeezer) ale nepokryje.
""",
    further_reading=(
        Reading(RAICOL),
        Reading(COVESION),
        Reading(HC_PHOTONICS),
        Reading(NOISY_LABS),
        Reading(LIGENTEC),
        Reading(LIONIX),
        Reading(CCRAFT),
        Reading(IDQ_SNSPD),
        Reading(SINGLE_QUANTUM),
        Reading(PIXEL_PHOTONICS),
        Reading(PHOTON_SPOT),
        Reading(QUANTUM_OPUS),
        Reading(SIMIT_SNSPD),
        Reading(XANADU_TES),
        Reading(BLUEFORS),
        Reading(EUROHPC_LUCY, "Lucy s chlazením od attocube"),
        Reading(THORLABS_DETECTORS),
    ),
)

SOFTWARE_TOPIC = TheoryTopic(
    anchor="svet-software",
    title="Software: co se dá dál používat",
    in_short=(
        "Xanaduův software pro GBS (Strawberry Fields, The Walrus, MrMustard) je od roku 2026 archivovaný. Aktivně "
        "vyvíjený simulátor s GBS je Piquasso z Budapešti; Perceval je pro jednotlivé fotony, CUDA-Q obsluhuje ORCA."
    ),
    explanation=r"""
- **Strawberry Fields, The Walrus, MrMustard** (Xanadu) – archivované v roce 2026; The Walrus zůstává referenční
  knihovnou pro hafniány a torontiány a dá se dál nainstalovat, verzi je ale dobré zafixovat.
- **PennyLane** (Xanadu) – aktivní, ale zaměřený na qubity; fotonický plugin je zastaralý.
- **Piquasso** (Budapest Quantum Computing Group, licence Apache) – aktivní, umí boson sampling i GBS, rozhraní
  v Pythonu s jádrem v C++. Nejlepší kandidát pro simulace v disertaci vedle vlastního kódu této aplikace.
- **Perceval** (Quandela) – jednotlivé fotony; GBS jen oklikou (viz stránka o Quandele).
- **Bosonic Qiskit** – bosonické módy vedle qubitů v oříznutém Fockově prostoru; **NVIDIA CUDA-Q** – rozhraní pro
  ORCA PT.
""",
    further_reading=(
        Reading(STRAWBERRY_FIELDS_ARCHIVED),
        Reading(PIQUASSO_PAPER),
        Reading(PERCEVAL),
        Reading(BOSONIC_QISKIT),
        Reading(CUDAQ_PHOTONIC),
    ),
)

FINANCE_TOPIC = TheoryTopic(
    anchor="svet-finance",
    title="Kdo nabízí fotoniku a kvantové Monte Carlo bankám",
    in_short=(
        "Recenzovaný doklad výhody na skutečné bankovní úloze se skutečným kvantovým hardwarem zatím nezveřejnil "
        "nikdo. Jediná metoda GBS v denním provozu – Qpurpose u Jyske Bank – běží podle SDU jako simulace na "
        "klasických počítačích."
    ),
    explanation=r"""
**Qpurpose (Odense, Dánsko).** Spin-off SDU z roku 2022, metoda z článků Andersena a Shan (GBS pro gaussovsky
vážené integrály). Software pro krátkodobou předpověď akcií běží podle SDU denně na obchodním stole Jyske Bank,
„podporovaný simulacemi na HPC“ – tedy na klasických počítačích. Metriky zveřejněné nejsou; podrobný rozbor je na
stránce o Qpurpose. Mezi partnery uvádí ORCA, Sparrow, Quandelu, IBM a Pasqal.

**Quandela a Crédit Agricole CIB (2025).** Hybridní algoritmus pro předpověď selhání úvěru. Tisková zpráva nemá
metriky ani článek a neříká, jestli úloha běžela na hardwaru.

**Xanadu s BMO a Scotiabank (2019).** Software, který *simuloval* kvantové Monte Carlo pro obchodní produkty;
zrychlení „stokrát až tisíckrát“ bylo projekcí pro budoucí hardware. Správci aktiv BMO a CIBC dnes v Xanadu
investují.

**ORCA, QuiX.** Finance mají v marketingu („risk modeling“), konkrétního zákazníka z financí neuvádějí. ORCA se
k financím dostává přes Qpurpose.

**Hradlová a kvantově inspirovaná konkurence.** S tímhle banka nabídku GBS srovná:

- *kvantové Monte Carlo s amplitudovou estimací* – Classiq se Sumitomo a Mizuho-DL FT (zkrácení obvodů pro
  úvěrová portfolia, studie proveditelnosti), QC Ware s Goldman Sachs („mělké“ Monte Carlo pro hardware za 5–10 let);
- *HSBC s IBM* (2025) – až o 34 % lepší odhad, zda se obchod s dluhopisem vyplní, na procesoru Heron. Nejsilnější
  veřejný bankovní výsledek, ale hradlový, ne fotonický, a „až“ znamená nejlepší případ;
- *kvantově inspirované metody* – Multiverse (Španělsko) s BBVA a Crédit Agricole; firma se dnes přeorientovala na
  kompresi jazykových modelů.

**Čínská linie.** He a kol. (2026) ukázali GBS s časovým multiplexem pro grafové úlohy z financí.

**Peníze v oboru.** McKinsey napočítal za rok 2025 asi 12,6 mld. USD do kvantových start-upů, QED-C 4,9 mld. USD
soukromého rizikového kapitálu – liší se definicí. PsiQuantum získal 1 mld. USD (září 2025, ocenění 7 mld.),
Xanadu přes vstup na burzu asi 302 mil. USD, QuiX 15 mil. €, Quandela naposledy 50 mil. € (2023). Kolik šlo do
fotoniky celkem, nikdo nezveřejnil.
""",
    further_reading=(
        Reading(SDU_QUANTUM_FINANCE, "Jyske Bank a simulace na HPC"),
        Reading(QPURPOSE_PARTNERSHIPS),
        Reading(QUANDELA_CREDIT_AGRICOLE),
        Reading(XANADU_BANKS),
        Reading(CLASSIQ_MIZUHO),
        Reading(QC_WARE_GOLDMAN),
        Reading(HSBC_IBM),
        Reading(MULTIVERSE_BBVA),
        Reading(HE_GRAPH_FINANCE),
        Reading(MCKINSEY_MONITOR),
        Reading(PSIQUANTUM_SERIES_E),
    ),
)

CZECH_TOPIC = TheoryTopic(
    anchor="svet-cesko",
    title="Česko a nejbližší partneři",
    in_short=(
        "Nejbližší tým je doma: IT4I v Ostravě má kvantový počítač VLQ a podle abstraktu semináře převádí GBS na "
        "hradlový program v projektu ESA. Teorii GBS spoluzaložili Hamilton a Jex z ČVUT, měření počtu fotonů umí "
        "Olomouc. Stroj Lucy od Quandely jde zdarma přes EuroHPC, nejbližší uzávěrky 1. 11. a 1. 12. 2026."
    ),
    explanation=r"""
**IT4Innovations, VŠB-TU Ostrava.** VLQ je supravodivý počítač IQM s 24 qubity (od září 2025), napojený na
superpočítač Karolina; provozuje ho konsorcium LUMI-Q a přístup je přes EuroHPC i pro firmy. Podle abstraktu
semináře z 25. 5. 2026 běží projekt ESA **GBS4EO** (KP Labs, Jagellonská univerzita, IT4I): GBS hledá husté
podgrafy v hyperspektrálních datech z dálkového průzkumu Země a úloha se převádí na hradlový program pro VLQ.
Stránka semináře už není dostupná, proto bez odkazu – *ověřit přímo v IT4I*. Pokud sedí, je to nejbližší tým
se zkušeností s GBS na místním hardwaru.

**ČVUT FJFI (Igor Jex, Craig S. Hamilton).** Spoluautoři původního článku o GBS (2017, s Paderbornem). Teorie, ne
experiment; přirozená cesta ke stroji PaQS a projektu PhoQuant.

**Univerzita Palackého Olomouc, katedra optiky.** Experimentální kvantová optika; skupina M. Ježka publikovala
metodu přesného měření fotonové statistiky (PRL 2019), tedy přesně to, co detekce v GBS potřebuje. Vlastní pulzní
zdroj stlačeného světla pro GBS jsme neověřili.

**Česká národní banka.** Pracovní studie 1/2023 (Martin Veselý): složení devizových rezerv na počítačích IBM
a D-Wave (QAOA, VQE, Groverovo adaptivní hledání) proti klasickým metodám. Jediná doložená kvantová studie české
finanční instituce, a proto nejpravděpodobnější první finanční protějšek.

**Programy.** Pilotní přístup EuroHPC (výzva 61): zdarma, projekty na 3 nebo 6 měsíců, uzávěrky každý měsíc –
nejbližší 1. 11. a 1. 12. 2026; mezi stroji je fotonická Lucy (Quandela) i VLQ. V QuantERA jsou za Česko MŠMT
a TA ČR. Výzva Horizon Europe na velké fotonické platformy (10 mil. €) je pro hardwarová konsorcia, ne pro
doktoranda.

**Kde jsme nic nenašli.** ÚFE AV ČR, ELI Beamlines, Crytur ani Meopta podle svých stránek kvantové počítání nedělají;
české kvantové start-upy ani aktivitu komerčních bank jsme nenašli.

**Pozor na jména.** Ulrik L. Andersen (DTU, experimenty se stlačeným světlem) a Jørgen E. Andersen (SDU, Qpurpose,
článek Andersena a Shan) jsou dva různí lidé.
""",
    further_reading=(
        Reading(VLQ_INAUGURATION),
        Reading(CTU_GROUP),
        Reading(HAMILTON, "Hamilton a Jex mezi autory"),
        Reading(OLOMOUC_PNR),
        Reading(CNB_FX_RESERVES),
        Reading(EUROHPC_QUANTUM_ACCESS),
        Reading(EUROHPC_QUANTUM_CALL),
        Reading(QUANTERA),
    ),
)

VERDICT_TOPIC = TheoryTopic(
    anchor="svet-souhrn",
    title="Souhrn: kdo umí GBS, kdo je konkurence a kdo partner",
    in_short=(
        "Skutečné GBS umí jen hrstka laboratoří a jako službu ho dnes nenabízí nikdo. Konkurencí disertace jsou "
        "Qpurpose, Twente a hradlové kvantové Monte Carlo; partnery IT4I, ČVUT s Paderbornem, DTU a Olomouc."
    ),
    explanation=r"""
Tabulka níže shrnuje verdikty z předchozích kapitol. Rozdělení na konkurenci a partnery je **náš odhad**
z hlediska disertace, ne doložený fakt.

**Partneři.**

- *IT4I* – domácí hardware (VLQ, Karolina) a případně tým GBS4EO;
- *ČVUT (Hamilton, Jex) → Paderborn a PhoQuant* – jediný programovatelný GBS v Evropě, přístupný spoluprací;
- *DTU (U. L. Andersen)* – až zpřístupní cloud PhotoQ;
- *Olomouc* – měření fotonové statistiky a experimentální zázemí;
- *Quandela (Lucy přes EuroHPC) a QuiX* – hardware pro obdobu s jednotlivými fotony;
- *Piquasso* – aktivní simulátor GBS po archivaci Xanaduova softwaru.

**Konkurence.**

- *Qpurpose a SDU* – stejná věda i trh; akademicky spíš spolupracovníci, komerčně konkurent. Diagnostika selhání
  z této aplikace může nezávisle prověřit, kde jejich výhoda platí;
- *Twente (Renema)* – Monte Carlo s jednotlivými fotony a patentová přihláška;
- *hradlové kvantové Monte Carlo* (IBM s HSBC, Classiq, QC Ware) – s tím banka GBS srovná;
- *klasické a kvantově inspirované algoritmy* – největší reálná konkurence: co jde spočítat klasicky, banka koupí
  klasicky.

**Co z toho plyne pro disertaci (náš odhad).** Veřejný doklad výhody na bankovní úloze se skutečným hardwarem
chybí. Nejvěrohodnější česká nabídka proto není slib kvantové výhody, ale nezávislé srovnání a diagnostika selhání
GBS a kvantového Monte Carla, doplněné kvantově inspirovanými odhady na Karolině.
""",
    further_reading=(
        Reading(PIQUASSO_PAPER),
        Reading(TWENTE_PATENT),
        Reading(OH_CLASSICAL_SIMULATION, "klasická simulace jako konkurence"),
    ),
)

TOPICS: Tuple[TheoryTopic, ...] = (
    CHAIN_TOPIC,
    BUILT_TOPIC,
    SQUEEZED_TOPIC,
    SINGLE_PHOTON_TOPIC,
    OTHER_TOPIC,
    SUPPLY_TOPIC,
    SOFTWARE_TOPIC,
    FINANCE_TOPIC,
    CZECH_TOPIC,
    VERDICT_TOPIC,
)

KEY_FINDINGS: Tuple[KeyFinding, ...] = (
    KeyFinding(
        "**Konkurence a partneři (náš odhad):** konkurencí jsou Qpurpose, Twente a hradlové kvantové Monte Carlo; "
        "partnery IT4I, ČVUT s Paderbornem, DTU a Olomouc.",
        VERDICT_TOPIC.anchor,
    ),
    KeyFinding(
        "**Velké GBS postavily jen USTC (Jiuzhang) a Xanadu (Borealis).** Borealis je od roku 2023 mimo cloud; "
        "v Evropě běží menší PaQS v Paderbornu.",
        BUILT_TOPIC.anchor,
    ),
    KeyFinding(
        "**GBS jako službu dnes nenabízí nikdo.** Nejblíž jsou DTU (PhotoQ) a německý PhoQuant; spuštění obou je "
        "neověřené.",
        SQUEEZED_TOPIC.anchor,
    ),
    KeyFinding(
        "**Většina evropských firem pracuje s jednotlivými fotony** (Quandela, QuiX, ORCA, Sparrow) – boson "
        "sampling s permanenty, ne GBS s hafniány.",
        SINGLE_PHOTON_TOPIC.anchor,
    ),
    KeyFinding(
        "**Z tvého seznamu:** Xanadu GBS postavil; Q.ANT ho jen podporuje v PhoQuantu; „chipX“ je nejspíš QuiX "
        "(interferometry); Thorlabs dodá krystaly a optiku; ColdQuanta (Infleqtion) a Pasqal jsou atomy.",
        VERDICT_TOPIC.anchor,
    ),
    KeyFinding(
        "**Software od Xanadu je archivovaný** (Strawberry Fields, The Walrus); aktivní simulátor GBS je Piquasso.",
        SOFTWARE_TOPIC.anchor,
    ),
    KeyFinding(
        "**Ve financích chybí doklad výhody na hardwaru.** Qpurpose u Jyske Bank běží jako simulace na HPC, "
        "nejsilnější bankovní výsledek (HSBC s IBM) je hradlový.",
        FINANCE_TOPIC.anchor,
    ),
    KeyFinding(
        "**Nejbližší partneři jsou doma:** IT4I (VLQ, Karolina), ČVUT (spoluautoři GBS) a Olomouc (měření fotonů); "
        "Lucy přes EuroHPC s uzávěrkou 1. 11. 2026.",
        CZECH_TOPIC.anchor,
    ),
)
