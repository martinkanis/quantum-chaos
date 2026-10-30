"""Notes from Philip Walther's Schrödinger Lecture on photonic quantum computing (ESI Vienna, 12 December 2022).

The text follows the talk chapter by chapter; what Walther says and shows on his slides is kept apart from our own
remarks and calculations, which are marked as such. The slides come from the recording and are served behind the
login (web/lecture_slides.py); the transcript and all frames are on the branch podklady-video.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from ui.piquasso_content import KLM
from ui.theory_content import AARONSON_ARKHIPOV, MADSEN, RECK, ZHONG, KeyFinding, Reading, Source, TheoryTopic

LECTURE = "walther-2022"
"""Folder of the slides in content/lectures and part of their URL."""
VIDEO_URL = "https://youtu.be/DswQ0FTYa18"
VIDEO_SECONDS = 3857
"""Length of the recording, 1:04:17."""
TITLE = "Přednáška: Philip Walther o fotonickém kvantovém počítání (2022)"
SOURCES_ANCHOR = "walther-zdroje"

INTRO = (
    "Zápisky ze Schrödingerovy přednášky Philipa Walthera z Vídeňské univerzity „Photonic quantum computing – "
    "a bright future for many applications“ (Institut Erwina Schrödingera, Vídeň, 12. prosince 2022, 64 minut, "
    "anglicky). Walther vede vídeňskou skupinu kvantové fotoniky a je jedním z autorů prvních experimentů "
    "s klastrovými stavy, slepým počítáním i boson samplingem. Přednáška je přehledová: co fotonický kvantový "
    "počítač potřebuje, proč se dvouqubitová hradla s fotony dělají tak těžko, jak to obchází měřením řízené "
    "počítání a fúze a co dalšího fotony umějí. Kapitoly sledují přednášku, u každé jsou slajdy a odkaz na místo "
    "ve videu. Co říká přednášející, je odlišené od našich poznámek a výpočtů, které jsou označené."
)

HOW_MADE = (
    "Jak stránka vznikla: zvuk jsme přepsali modelem Whisper large-v3, slajdy jsou snímky ze záznamu na YouTube "
    "(z animovaných slajdů je vždy jen poslední krok, opakované snímky jsou vynechané). Slajdy patří autorovi, "
    "proto jsou jen za přihlášením. Citace ze slajdů jsme dohledali a kde se slajd mýlí, je to u citace uvedeno."
)

KEY_FINDINGS = (
    KeyFinding(
        "**Fotonický kvantový počítač = zdroj fotonů + čip + detektory.** Čipy a supravodivé detektory (účinnost "
        "kolem 95 %) jsou podle Walthera v podstatě vyřešené, nejtěžší jsou dobré jednotlivé fotony na povel.",
        "walther-hardware",
    ),
    KeyFinding(
        "**Fotony spolu neinteragují,** takže dvouqubitové hradlo jde jen pravděpodobnostně a s měřením. Schéma KLM "
        "je sice škálovatelné, ale potřebuje $10^3$ až $10^5$ pomocných fotonů na qubit.",
        "walther-hradla",
    ),
    KeyFinding(
        "**Měřením řízené počítání** obrací úlohu: nejdřív se připraví velký provázaný klastrový stav a výpočet "
        "jsou už jen měření jednotlivých qubitů. Těžká část se přesune do přípravy stavu.",
        "walther-klastry",
    ),
    KeyFinding(
        "**Plán, na kterém staví PsiQuantum:** třífotonové GHZ stavy, fúze s úspěšností 75 % a teorie perkolace, "
        "která zaručí, že se z náhodně slepených kousků dá počítat.",
        "walther-fuze",
    ),
    KeyFinding(
        "**Fotony umějí víc než rychlost:** slepé kvantové počítání v cloudu, kde server nepozná vstup, program ani "
        "výsledek, a superpozice pořadí hradel, která jedním průchodem fotonu pozná, zda dvě hradla komutují.",
        "walther-slepe",
    ),
    KeyFinding(
        "**Boson sampling:** fotony na děliči svazku „počítají“ permanent, který je pro klasický počítač #P-těžký. "
        "Klasická mez je podle slajdu kolem 70 fotonů; čínský Jiuzhang (2020) měl až 76 detekovaných fotonů.",
        "walther-boson-sampling",
    ),
)


@dataclass(frozen=True)
class LectureSlide:
    file_name: str
    """slajd_SSSS.jpg, where SSSS is the second of the recording the frame comes from."""
    caption: str

    @property
    def seconds(self) -> int:
        return int(self.file_name[len("slajd_"):len("slajd_") + 4])


@dataclass(frozen=True)
class ChapterTime:
    anchor: str
    start: int
    """Second of the recording where the chapter starts; it ends where the next one starts."""


WALTHER_VIDEO = Source(
    "Walther, P.: *Photonic quantum computing – a bright future for many applications*. Schrödingerova přednáška, "
    "Institut Erwina Schrödingera, Vídeň, 12. 12. 2022, [záznam na YouTube](https://youtu.be/DswQ0FTYa18)"
)
WALTHER_GROUP = Source(
    "Quantum Photonics, Vídeňská univerzita: [quantumphotonics.at](https://www.quantumphotonics.at) a online "
    "kvantová laboratoř [photonq.at](https://www.photonq.at)"
)
SCHRODINGER_1952 = Source(
    "Schrödinger, E.: *Are there quantum jumps? Part II*. The British Journal for the Philosophy of Science 3, "
    "233–242 (1952)"
)
O_BRIEN_2007 = Source(
    "O'Brien, J. L.: *Optical quantum computing*. Science 318, 1567–1570 (2007), "
    "[doi:10.1126/science.1142892](https://doi.org/10.1126/science.1142892)"
)
KWIAT_1995 = Source(
    "Kwiat, P. G., Mattle, K., Weinfurter, H., Zeilinger, A., Sergienko, A. V., Shih, Y.: *New high-intensity "
    "source of polarization-entangled photon pairs*. Physical Review Letters 75, 4337 (1995), "
    "[doi:10.1103/PhysRevLett.75.4337](https://doi.org/10.1103/PhysRevLett.75.4337)"
)
NOBEL_2022 = Source(
    "Nobelova cena za fyziku 2022 (Aspect, Clauser, Zeilinger): "
    "[tisková zpráva](https://www.nobelprize.org/prizes/physics/2022/press-release/)"
)
SHOR_1994 = Source(
    "Shor, P. W.: *Algorithms for quantum computation: discrete logarithms and factoring*. Proceedings 35th Annual "
    "Symposium on Foundations of Computer Science, 124–134 (1994), "
    "[doi:10.1109/SFCS.1994.365700](https://doi.org/10.1109/SFCS.1994.365700)"
)
GROVER_1996 = Source(
    "Grover, L. K.: *A fast quantum mechanical algorithm for database search*. Proceedings of the 28th Annual ACM "
    "Symposium on Theory of Computing, 212–219 (1996), "
    "[arXiv:quant-ph/9605043](https://arxiv.org/abs/quant-ph/9605043)"
)
FEYNMAN_1982 = Source(
    "Feynman, R. P.: *Simulating physics with computers*. International Journal of Theoretical Physics 21, "
    "467–488 (1982), [doi:10.1007/BF02650179](https://doi.org/10.1007/BF02650179)"
)
LLOYD_1996 = Source(
    "Lloyd, S.: *Universal quantum simulators*. Science 273, 1073–1078 (1996), "
    "[doi:10.1126/science.273.5278.1073](https://doi.org/10.1126/science.273.5278.1073)"
)
ALGORITHM_ZOO = Source("[Quantum Algorithm Zoo](https://quantumalgorithmzoo.org) – katalog kvantových algoritmů")
YOLE_ROADMAP = Source(
    "Yole Développement: *Quantum Technologies 2021*, červen 2021 – graf počtu fyzikálních qubitů 1998–2026 "
    "na slajdu ve 22:29"
)
UPPU_2021 = Source(
    "Uppu, R., Midolo, L., Zhou, X., Carolan, J., Lodahl, P.: *Quantum-dot-based deterministic photon–emitter "
    "interfaces for scalable photonic quantum technology*. Nature Nanotechnology 16, 1308–1317 (2021), "
    "[doi:10.1038/s41565-021-00965-6](https://doi.org/10.1038/s41565-021-00965-6)"
)
HARRIS_2017 = Source(
    "Harris, N. C. a kol.: *Quantum transport simulations in a programmable nanophotonic processor*. Nature "
    "Photonics 11, 447–452 (2017)"
)
CALAFELL_COUNTERFACTUAL = Source(
    "Alonso Calafell, I. a kol.: *Trace-free counterfactual communication with a nanophotonic processor*. npj "
    "Quantum Information 5, 61 (2019), [arXiv:1808.04856](https://arxiv.org/abs/1808.04856) – na slajdu pod "
    "názvem preprintu „Genuine counterfactual communication…“"
)
GREGANTI_DETECTORS = Source(
    "Greganti, C., Schiansky, P., Alonso Calafell, I., Procopio, L. M., Rozema, L. A., Walther, P.: Optics "
    "Express 26, 3286 (2018) – detektory SNSPD rozlišující počet fotonů (citace podle slajdu)"
)
O_BRIEN_CNOT_2003 = Source(
    "O'Brien, J. L., Pryde, G. J., White, A. G., Ralph, T. C., Branning, D.: *Demonstration of an all-optical "
    "quantum controlled-NOT gate*. Nature 426, 264–267 (2003), "
    "[doi:10.1038/nature02054](https://doi.org/10.1038/nature02054)"
)
ZEUNER_2018 = Source(
    "Zeuner, J. a kol.: *Integrated-optics heralded controlled-NOT gate for polarization-encoded qubits*. npj "
    "Quantum Information 4, 13 (2018), [doi:10.1038/s41534-018-0068-0](https://doi.org/10.1038/s41534-018-0068-0)"
)
RAUSSENDORF_BRIEGEL = Source(
    "Raussendorf, R., Briegel, H. J.: *A one-way quantum computer*. Physical Review Letters 86, 5188 (2001), "
    "[doi:10.1103/PhysRevLett.86.5188](https://doi.org/10.1103/PhysRevLett.86.5188) – na jednom slajdu chybně "
    "„PRL 86, 910“"
)
WALTHER_ONE_WAY_2005 = Source(
    "Walther, P. a kol.: *Experimental one-way quantum computing*. Nature 434, 169–176 (2005), "
    "[doi:10.1038/nature03347](https://doi.org/10.1038/nature03347)"
)
PANT_PERCOLATION = Source(
    "Pant, M., Towsley, D., Englund, D., Guha, S.: *Percolation thresholds for photonic quantum computing*. Nature "
    "Communications 10, 1070 (2019)"
)
GIMENO_SEGOVIA_2015 = Source(
    "Gimeno-Segovia, M., Shadbolt, P., Browne, D. E., Rudolph, T.: *From three-photon Greenberger-Horne-Zeilinger "
    "states to ballistic universal quantum computation*. Physical Review Letters 115, 020502 (2015), "
    "[doi:10.1103/PhysRevLett.115.020502](https://doi.org/10.1103/PhysRevLett.115.020502)"
)
RUDOLPH_2017 = Source(
    "Rudolph, T.: *Why I am optimistic about the silicon-photonic route to quantum computing*. APL Photonics 2, "
    "030901 (2017)"
)
BARTOLUCCI_FBQC = Source(
    "Bartolucci, S. a kol.: *Fusion-based quantum computation*. Nature Communications 14, 912 (2023), "
    "[doi:10.1038/s41467-023-36493-1](https://doi.org/10.1038/s41467-023-36493-1)"
)
PSIQUANTUM_2021 = Source(
    "Business Wire: *PsiQuantum Closes $450 Million Funding Round to Build the World's First Commercially Viable "
    "Quantum Computer*, 27. 7. 2021 (snímek na slajdu ve 44:55)"
)
CALAFELL_GRAPHENE = Source(
    "Alonso Calafell, I. a kol.: *Quantum computing with graphene plasmons*. npj Quantum Information 5, 37 (2019), "
    "[doi:10.1038/s41534-019-0150-2](https://doi.org/10.1038/s41534-019-0150-2)"
)
RIVEST_1978 = Source(
    "Rivest, R. L., Adleman, L., Dertouzos, M. L.: *On data banks and privacy homomorphisms*. In: Foundations of "
    "Secure Computation, Academic Press 1978, 169–180"
)
BFK_2009 = Source(
    "Broadbent, A., Fitzsimons, J., Kashefi, E.: *Universal blind quantum computation*. 50th Annual IEEE Symposium "
    "on Foundations of Computer Science, 517–526 (2009), [arXiv:0807.4154](https://arxiv.org/abs/0807.4154)"
)
BARZ_2012 = Source(
    "Barz, S., Kashefi, E., Broadbent, A., Fitzsimons, J. F., Zeilinger, A., Walther, P.: *Demonstration of blind "
    "quantum computing*. Science 335, 303–308 (2012), "
    "[doi:10.1126/science.1214707](https://doi.org/10.1126/science.1214707)"
)
GREGANTI_2016 = Source(
    "Greganti, C., Röhsner, M.-C., Barz, S., Morimae, T., Walther, P.: *Demonstration of measurement-only blind "
    "quantum computing*. New Journal of Physics 18, 013020 (2016), "
    "[doi:10.1088/1367-2630/18/1/013020](https://doi.org/10.1088/1367-2630/18/1/013020)"
)
OCB_2012 = Source(
    "Oreshkov, O., Costa, F., Brukner, Č.: *Quantum correlations with no causal order*. Nature Communications 3, "
    "1092 (2012), [doi:10.1038/ncomms2076](https://doi.org/10.1038/ncomms2076)"
)
CHIRIBELLA_2012 = Source(
    "Chiribella, G.: *Perfect discrimination of no-signalling channels via quantum superposition of causal "
    "structures*. Physical Review A 86, 040301 (2012), "
    "[doi:10.1103/PhysRevA.86.040301](https://doi.org/10.1103/PhysRevA.86.040301)"
)
CHIRIBELLA_SWITCH = Source(
    "Chiribella, G., D'Ariano, G. M., Perinotti, P., Valiron, B.: *Quantum computations without definite causal "
    "structure*. Physical Review A 88, 022318 (2013), "
    "[doi:10.1103/PhysRevA.88.022318](https://doi.org/10.1103/PhysRevA.88.022318)"
)
PROCOPIO_2015 = Source(
    "Procopio, L. M. a kol.: *Experimental superposition of orders of quantum gates*. Nature Communications 6, "
    "7913 (2015), [doi:10.1038/ncomms8913](https://doi.org/10.1038/ncomms8913) – slajdy uvádějí jednou 7913, "
    "jednou 8913 (to je konec DOI)"
)
RUBINO_2017 = Source(
    "Rubino, G. a kol.: *Experimental verification of an indefinite causal order*. Science Advances 3, e1602589 "
    "(2017), [doi:10.1126/sciadv.1602589](https://doi.org/10.1126/sciadv.1602589)"
)
HONG_OU_MANDEL = Source(
    "Hong, C. K., Ou, Z. Y., Mandel, L.: *Measurement of subpicosecond time intervals between two photons by "
    "interference*. Physical Review Letters 59, 2044 (1987), "
    "[doi:10.1103/PhysRevLett.59.2044](https://doi.org/10.1103/PhysRevLett.59.2044)"
)
FIRST_BOSON_SAMPLING = Source(
    "Broome, M. A. a kol., Science 339, 794 (2013); Spring, J. B. a kol., Science 339, 798 (2013); Tillmann, M. "
    "a kol., Nature Photonics 7, 540 (2013); Crespi, A. a kol., Nature Photonics 7, 545 (2013) – první čtyři "
    "experimenty s boson samplingem (3–4 fotony)"
)
LUND_BREMNER_RALPH = Source(
    "Lund, A. P., Bremner, M. J., Ralph, T. C.: *Quantum sampling problems, BosonSampling and quantum supremacy*. "
    "npj Quantum Information 3, 15 (2017)"
)
ARUTE_2019 = Source(
    "Arute, F. a kol.: *Quantum supremacy using a programmable superconducting processor*. Nature 574, 505–510 "
    "(2019), [doi:10.1038/s41586-019-1666-5](https://doi.org/10.1038/s41586-019-1666-5)"
)
SAGGIO_2021 = Source(
    "Saggio, V. a kol.: *Experimental quantum speed-up in reinforcement learning agents*. Nature 591, 229–233 (2021)"
)
SPAGNOLO_2022 = Source(
    "Spagnolo, M. a kol.: *Experimental photonic quantum memristor*. Nature Photonics 16, 318–323 (2022), "
    "[doi:10.1038/s41566-022-00973-5](https://doi.org/10.1038/s41566-022-00973-5)"
)
MAZUMDER_2012 = Source(
    "Mazumder, P., Kang, S. M., Waser, R.: *Memristors: devices, models, and applications*. Proceedings of the "
    "IEEE 100 (2012)"
)


INTRODUCTION_TOPIC = TheoryTopic(
    anchor="walther-uvod",
    title="Úvod: od Schrödingerových „ichtyosaurů“ k druhé kvantové revoluci",
    in_short=(
        "Schrödinger v roce 1952 tvrdil, že s jednotlivými částicemi experimentovat neumíme. Dnes to laboratoře dělají "
        "běžně – s ionty, atomy, supravodivými obvody i fotony – a na tom stojí kvantové technologie."
    ),
    explanation=r"""
Prvních šest minut záznamu je uvítání: přednášku uvádí Christoph Dellago, ředitel Institutu Erwina Schrödingera
(v přepisu zkomolený na „Delage“). Připomene, že o pár dní dřív převzali Nobelovu cenu za fyziku Alain Aspect,
John Clauser a vídeňský Anton Zeilinger, a představí Walthera: začínal jako kvantový chemik na TU Wien, doktorát
dělal u Zeilingera, postdoktorát na Harvardu a od roku 2015 je ve Vídni řádným profesorem.

Walther začíná citátem, který ukazuje na slajdu:

> „Nikdy neexperimentujeme s jediným elektronem nebo atomem. V myšlenkových experimentech někdy předpokládáme, že
> ano; to vždy vede k směšným důsledkům… s jednotlivými částicemi neexperimentujeme o nic víc, než můžeme v zoo
> chovat ichtyosaury.“ (E. Schrödinger, 1952)

Pointa: o necelých sedmdesát let později je práce s jednotlivými kvantovými objekty v laboratořích rutina. Walther
tomu říká **druhá kvantová revoluce** – první revoluce byla samotná kvantová teorie, druhá je řízení jednotlivých
kvantových částic tak, aby se jejich superpozice a provázání dalo využít v technice. Na slajdu jsou čtyři platformy:

- **ionty** v elektromagnetické pasti, ovládané lasery,
- **neutrální atomy** v optické mřížce,
- **supravodivé obvody** řízené mikrovlnami (to, co staví IBM a Google),
- **fotony** ve vlnovodech na čipu – téma celé přednášky.

Přednáška je určená smíšenému publiku (informatici, matematici, fyzici), takže Walther slibuje přehled: co
fotonický počítač potřebuje, jaké má problémy, jaké jsou „plány“ velkých strojů a na konci vídeňské speciality.
""",
    further_reading=(
        Reading(WALTHER_VIDEO, "celý záznam; čas každé kapitoly je u jejích slajdů"),
        Reading(SCHRODINGER_1952, "článek s citátem o ichtyosaurech"),
        Reading(NOBEL_2022, "Nobelova cena za experimenty s provázanými fotony"),
    ),
)

SUPERPOSITION_TOPIC = TheoryTopic(
    anchor="walther-superpozice",
    title="Superpozice, qubit a jak se zapíše do fotonu",
    in_short=(
        "Foton na děliči svazku je ve superpozici „prošel“ a „odrazil se“. Qubit nese obě hodnoty 0 a 1 zároveň a $N$ "
        "qubitů má $2^N$ amplitud. Do fotonu se qubit zapíše dráhou nebo polarizací a jedno jde převést na druhé."
    ),
    explanation=r"""
**Superpozice na děliči svazku.** Foton nejde rozdělit na menší kusy. Když dopadne na polopropustné zrcadlo
(dělič svazku 50 : 50), s pravděpodobností 50 % projde do dráhy $A$ a s pravděpodobností 50 % se odrazí do
dráhy $B$. Dokud ho neměříme, je v obou drahách současně – přesněji existují obě amplitudy zároveň:

$$
|1\rangle_{\text{před}} \;\to\; \frac{1}{\sqrt{2}}\bigl(|1\rangle_A + |1\rangle_B\bigr).
$$

(Slajd vynechává fázi: u souměrného děliče dostane odražená složka navíc faktor $i$. Na pravděpodobnostech jedné
cesty to nic nemění, na interferenci ano – uvidíme ji v kapitole o boson samplingu.) Měření dá náhodnou odpověď,
foton najdeme buď v $A$, nebo v $B$.

**Totéž na čipu.** Místo skleněné kostky se dnes používá *integrovaná fotonika*: vlnovody (něco jako optická
vlákna) vepsané do čipu velikosti nehtu. Když se dva vlnovody na krátkém úseku přiblíží, světlo mezi nimi
„přetéká“ evanescentním polem – vznikne *směrová spojka*. Délkou a vzdáleností úseku se nastaví poměr, třeba
50 : 50. Walther pouští animaci: foton vstoupí jedním vlnovodem a ze spojky odchází v superpozici obou.

**Bit a qubit.** Klasický bit je vypínač: 0, nebo 1. Qubit může být v superpozici

$$
|Q\rangle = \alpha|0\rangle + \beta|1\rangle, \qquad |\alpha|^2 + |\beta|^2 = 1,
$$

na slajdu konkrétně $\tfrac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$ – „0 *a* 1“ místo „0 *nebo* 1“. Se třemi qubity
je stav popsaný osmi amplitudami $a_0|000\rangle + a_1|001\rangle + \dots + a_7|111\rangle$, obecně $N$ qubitů
nese $2^N$ čísel. Odtud Waltherovo „kvantové zrychlení na první pohled“.

*Vlastní poznámka:* $2^N$ amplitud neznamená $2^N$ výsledků najednou – měření vrátí jen jeden řetězec bitů.
Užitek přichází z interference (další kapitola). Exponenciální počet amplitud ale vysvětluje, proč se kvantové
počítače špatně simulují: 50 qubitů má $2^{50} \approx 1{,}1 \cdot 10^{15}$ komplexních amplitud, což při
16 bajtech na amplitudu (dvě čísla s dvojitou přesností) dělá asi 18 petabajtů paměti.

**Polarizace jako qubit.** Kromě dráhy jde qubit zapsat do polarizace: vodorovně polarizovaný foton
$|H\rangle = |0\rangle$, svisle $|V\rangle = |1\rangle$. Stavy na Blochově (pro světlo Poincarého) sféře mají
jména: diagonální $D$ a antidiagonální $A$ na rovníku, kruhové $R$ a $L$ vpředu a vzadu. Hradla na jednom qubitu
jsou obyčejné **vlnové destičky**:

- půlvlnná destička ($\lambda/2$) natočená o $22{,}5^\circ$ udělá z $|H\rangle$ stav
  $(|H\rangle + |V\rangle)/\sqrt{2}$ – to je Hadamardovo hradlo,
- trojice $\lambda/4$, $\lambda/2$, $\lambda/4$ připraví libovolný stav $\alpha|H\rangle + \beta|V\rangle$.

**Převod polarizace na dráhu.** Polarizační dělič svazku (PBS) pustí $H$ rovně a $V$ odrazí. Z
$\alpha|H\rangle + \beta|V\rangle$ tak vznikne $\alpha|0\rangle + \beta|1\rangle$ zapsané do dvou drah (druhou
dráhu ještě destička $\lambda/2$ otočí zpět na $H$). Fotony tak mohou „přeskakovat“ mezi stupni volnosti – podle
Walthera jeden z důvodů, proč jsou tak vděčný kvantový systém. Formálně totéž vykládají
[skripta v kapitole o fotonických hradlech](/fotonika/zaklady#skripta-1-2).
""",
    further_reading=(
        Reading(O_BRIEN_2007, "přehled optického kvantového počítání, z něj je obrázek polarizačních qubitů"),
        Reading(WALTHER_VIDEO, "animace směrové spojky v 9:02"),
    ),
)

ENTANGLEMENT_TOPIC = TheoryTopic(
    anchor="walther-provazani",
    title="Provázání a zdroj, za který byla Nobelova cena",
    in_short=(
        "U provázaných částic je informace jen v celku, jednotlivá částice dává náhodné výsledky. Provázané páry "
        "fotonů dává sestupná parametrická konverze v nelineárním krystalu (Kwiat, Zeilinger a kol., 1995)."
    ),
    explanation=r"""
**Provázání.** Walther ho vysvětluje na dvou kostkách: víme, že obě padnou stejně, ale ne jak. Podíváme-li se na
jednu, dostaneme náhodné číslo – a tím okamžitě známe i druhou. Na slajdu: *informace je společná vlastnost;
korelace nese jen celý systém, jednotlivá částice dává náhodné výsledky.* (Pojem pochází od Schrödingera z roku
1935.) Provázání je pro kvantový počítač zdroj: bez něj by šel výpočet efektivně simulovat klasicky.

**Sestupná parametrická konverze (SPDC).** Průlom podle Walthera přišel v polovině 90. let. Laserový „pumpovací“
foton projde nelineárním krystalem (na slajdu BBO, krystal s nelinearitou $\chi^{(2)}$) a občas se rozpadne na dva
fotony s nižší energií. Platí zákony zachování energie a hybnosti (fázové sladění):

$$
\omega_{\text{pumpa}} = \omega_1 + \omega_2, \qquad \mathbf{k}_{\text{pumpa}} = \mathbf{k}_1 + \mathbf{k}_2 .
$$

V uspořádání „typu II“ má jeden foton polarizaci $H$, druhý $V$, a vylétají po dvou kuželích (na fotografii
barevné kruhy). Trik: vezmeme světlo z **průsečíků** kuželů. Tam nejde poznat, který foton přišel z kterého kužele,
a proto je pár v superpozici

$$
\frac{1}{\sqrt{2}}\bigl(|H\rangle_A|V\rangle_B - |V\rangle_A|H\rangle_B\bigr).
$$

„Tak jednoduché to je,“ říká Walther – a hned dodává, že to chce přesné seřízení a „citlivé konečky prstů“.

**Nobelova cena 2022.** Aspect a Clauser používali v 70. a 80. letech atomové kaskády, Zeilinger právě tenhle
krystalový zdroj. Na něm stojí teleportace, „entanglement swapping“ a řada dalších průkopnických experimentů.

**K čemu jsou fotony dobré.** Fotony letí rychlostí světla, takže se hodí na čtyři oblasti: kvantovou komunikaci,
základy kvantové mechaniky, metrologii (měření se světlem, kvantově vylepšené mikroskopy) a – asi posledních 20 let –
také na počítání. Kde se z provázaných párů stávají jednotlivé fotony pro počítač, vysvětluje kapitola
o [zdrojích fotonů ve Fotonice ve světě](/fotonika-ve-svete#svet-jednotlive-fotony).
""",
    further_reading=(
        Reading(KWIAT_1995, "zdroj provázaných párů z průsečíku kuželů"),
        Reading(NOBEL_2022),
    ),
)

ALGORITHMS_TOPIC = TheoryTopic(
    anchor="walther-algoritmy",
    title="Co je kvantový počítač a co umějí kvantové algoritmy",
    in_short=(
        "Kvantový algoritmus zpracuje všechny vstupy v superpozici a interferencí potlačí špatné odpovědi. "
        "K univerzálnosti stačí jednoqubitová hradla a jedno dvouqubitové. Zrychlení je exponenciální (Shor), "
        "kvadratické (Grover), polynomiální (Monte Carlo) – nebo zatím neprokázané (VQE, strojové učení)."
    ),
    explanation=r"""
**Interference je jádro.** Walther kreslí strom cest: k výsledku se dá dojít cestou s amplitudami $A_1A_2$ nebo
cestou $A_3A_4$. Kvantově se nesčítají pravděpodobnosti, ale amplitudy:

$$
P = |A_1A_2 + A_3A_4|^2 = |A_1A_2|^2 + |A_3A_4|^2 + 2\,\mathrm{Re}\bigl(A_1A_2A_3^*A_4^*\bigr).
$$

Poslední, interferenční člen může být záporný a cesty se pak vyruší. Dobrý kvantový algoritmus je podle něj
navržený tak, aby se špatné odpovědi vyrušily a správná s vysokou pravděpodobností „přežila“. Proto fungují
algoritmy, které mají interferenci v sobě – třeba Fourierova transformace.

**Obvodový model.** Dnes se algoritmy kreslí jako obvody: vodorovné čáry jsou qubity, krabičky hradla. Hadamardovo
hradlo $H$ vyrobí superpozici, dvouqubitová hradla (CNOT, řízená fáze) vyrobí provázání. Pro **univerzální**
kvantový počítač stačí libovolná jednoqubitová hradla plus jedno provazující dvouqubitové hradlo – z nich se
složí jakákoli operace. (U fotonů je jednoqubitová část snadná, dvouqubitová velmi těžká – viz kapitola
o hradlech.)

**Přehled algoritmů ze slajdů:**

- **Shor (1994, na slajdu 1993):** rozklad čísla $c = a \cdot b$ na prvočinitele s exponenciálním zrychlením.
  Prolomil by šifrování RSA – „zabijácká aplikace pro tajné služby“.
- **Grover (1996):** hledání v neseřazené databázi, kvadratické zrychlení – místo $N$ dotazů zhruba $\sqrt{N}$.
  Stejný princip jde použít na úlohy splnitelnosti (SAT) nebo barvení grafů.
- **Kvantová simulace (Feynman 1982, Lloyd 1996):** kvantové systémy simulovat kvantovým počítačem, s polynomiální
  místo exponenciální náročnosti.
- **Kvantová Fourierova transformace** také pro soustavy lineárních rovnic.
- **Kvantové Monte Carlo:** polynomiální (kvadratické) zrychlení.
- **Kvantové eigensolvery (VQE) a kvantové strojové učení** (QSVM, kvantové $k$ nejbližších sousedů, kvantové
  neuronové sítě): zrychlení zatím není jasné. Ve Vídni se věnují právě strojovému učení.

*Pozor na citát:* Walther říká, že Feynman v roce 1982 napsal „There's plenty of room at the bottom“. To je
Feynmanova přednáška o nanotechnologiích z roku 1959; o simulaci kvantových systémů je jeho článek *Simulating
physics with computers* z roku 1982 (v literatuře níže). Aktuální přehled algoritmů a jejich zrychlení vede
Quantum Algorithm Zoo; s otázkou, co je dokázané a co jen domněnka, posílá Walther na teoretika Norberta Schucha.

*Vlastní poznámka:* kvadratické zrychlení Monte Carla je to, o co jde
v [rešerši k finančnímu riziku](/reserse-gbs-financni-riziko); fotonický GBS se o zrychlení Monte Carla pokouší jinou cestou.
""",
    further_reading=(
        Reading(SHOR_1994),
        Reading(GROVER_1996),
        Reading(FEYNMAN_1982, "článek o simulaci, na který Walther naráží"),
        Reading(LLOYD_1996),
        Reading(ALGORITHM_ZOO, "odkaz ze slajdu"),
    ),
)

RACE_TOPIC = TheoryTopic(
    anchor="walther-zavod",
    title="Závod hardwaru: počet qubitů není všechno",
    in_short=(
        "Supravodiče, ionty, atomy i fotony – podle Walthera je závod otevřený. Počty qubitů rostou exponenciálně, "
        "ale provázat všechny qubity zatím nikdo neumí; rekordem bylo 24 provázaných iontů."
    ),
    explanation=r"""
Walther ukazuje obálku *The Economist* z roku 2015 („Quantum computing race“) a říká, že situace je pořád stejná:
**závod je otevřený** a není jasné, která platforma vyhraje.

**Graf počtu qubitů** (zdroj Yole Développement, 2021) má logaritmickou osu a dvě části. *Historie:* od dvou
qubitů v roce 1998 přes D-Wave (28 qubitů v roce 2007, 5 000 v roce 2020), Google (72 qubitů Bristlecone v roce
2018, 53 qubitů Sycamore v roce 2019) a IBM (50 qubitů v roce 2017). *Sliby:* IBM 433 a 1 121 qubitů, Intel 1 000
a **PsiQuantum milion fotonických qubitů v roce 2026**. Walther zmiňuje i čerstvou zprávu o čipu IBM se zhruba
400 qubity.

**Ale počet qubitů nevypovídá o všem.** Zajímavé je, kolik qubitů jde opravdu provázat a s jakou chybou. Na slajdu
stojí: *aktuální světový rekord v provázání: 24 qubitů (ionty)*. Velké čipy jsou úžasné, ale ne každý qubit se dá
spojit s každým a ne všechny fungují, jak by měly. Výzkumné laboratoře se proto často soustředí na menší systémy
s lepší kontrolou.

*Vlastní poznámka:* graf je „stav 2021“ a sliby byly obchodní plány. Kam se fotonické firmy, včetně PsiQuantum,
dostaly do roku 2026, shrnuje stránka [Fotonika ve světě](/fotonika-ve-svete#svet-jednotlive-fotony). Pro porovnání
platforem jsou lepší metriky než počet qubitů – chybovost dvouqubitových hradel, kvantový objem, počet logických
qubitů s opravou chyb.
""",
    further_reading=(
        Reading(YOLE_ROADMAP, "zdroj grafu na slajdu"),
        Reading(ARUTE_2019, "Sycamore, 53 qubitů"),
    ),
)

HARDWARE_TOPIC = TheoryTopic(
    anchor="walther-hardware",
    title="Fotonický počítač: zdroje, čipy a detektory",
    in_short=(
        "Potřeba jsou tři věci: zdroj jednotlivých fotonů, čip, na kterém interferují, a detektory. Čipy a supravodivé "
        "detektory jsou téměř vyřešené. Nejtěžší je zdroj: SPDC je náhodný, kvantové tečky jsou deterministické, "
        "ale fotony se z nich špatně dostávají ven."
    ),
    explanation=r"""
„V karikatuře“ je fotonický kvantový počítač jednoduchý: **zdroj** jednotlivých fotonů, **čip**, na kterém se
fotony potkají a interferují, a **detektory** na konci. Problémy začnou, když se přiblížíme.

### Zdroje: příroda se brání

Fotonů je kolem plno (žárovky, lasery), ale jsou to ty „špatné“. Seznam přání na slajdu:

- **spektrálně čisté** – každý foton stejný jako ostatní (nerozlišitelnost je podmínka interference),
- **opravdu jeden foton** – ne dva ani tři,
- **na povel** – jeden foton na každý puls.

**Spontánní zdroje (SPDC, SFWM)** jsou *pravděpodobnostní*: laser jen občas vyrobí pár a někdy místo jednoho páru
dva či tři, což je šum. Jeden foton z páru se dá detekovat jako „ohlašovací“ (signal/idler), ale náhodnosti se
tím nezbavíme. Walther počítá: když každý zdroj vystřelí s pravděpodobností 1 %, dva zdroje současně s
pravděpodobností $1\,\% \cdot 1\,\% = 10^{-4}$ – pravděpodobnost klesá exponenciálně. (*Vlastní výpočet:* pro
deset zdrojů je to $10^{-20}$.)

**Deterministické zdroje** jsou jednotlivé emitory – „umělé atomy“. Skutečné atomy se musí chytat a chladit,
proto se používají **kvantové tečky**: kousek polovodiče, který se chová jako jeden atom. Laser ho vybudí, při
návratu vyzáří jeden foton. Kolem tečky je rezonátor (na slajdu mikropilíř firmy Quandela). „Žádný oběd není
zadarmo“: foton vznikne pokaždé, ale je těžké ho dostat do vlákna – každý krok (vyzáření do rezonátoru, polarizátor,
sběrná optika, navázání do vlákna) má svou účinnost a ty se násobí. Walther: je lepší bojovat s technologickým
problémem (sběr) než s přírodním (náhodnost).

**Kolik fotonů zvládneme.** Slajd porovnává dvě cesty:

| Cesta | Pasivní optika | Aktivní optika |
|---|---|---|
| víc zdrojů SPDC (multiplexování) | 10–12 fotonů | kolem 40 fotonů |
| jedna kvantová tečka + demultiplexování | 20 fotonů | 80–100 fotonů |

Demultiplexování: tečka střílí fotony jeden za druhým a rychlé elektrooptické modulátory je rozdělují do různých
drah (na slajdu 32 fotonů do osmi výstupů). Proti milionu qubitů ze slibů to vypadá málo – Walther ale slibuje,
že sto fotonů na plán libovolně velkého počítače stačí (kapitola o fúzích). Na dotaz z publika dodává, že víc
nezávislých teček zatím nejde vyrobit tak, aby dávaly *stejné* fotony – výroba je trochu náhodná.

### Čip: interferometry s topením

Základní stavební kámen je **Machův–Zehnderův interferometr (MZI)**: dělič, fázový posun $\varphi$, dělič. Fázový
posun dělá malé topení – teplo materiál roztáhne a změní optickou délku. Fázi jde nastavit velmi přesně (slajd:
kontrast až $1 : 10^{-8}$) a šum je statický, z okolí se nepřidává. *Vlastní výpočet:* foton, který vstoupí jedním
vstupem, odejde z jednoho výstupu s pravděpodobností $\sin^2(\varphi/2)$ a z druhého $\cos^2(\varphi/2)$ – fází
se tedy nastaví libovolný poměr, tj. libovolné hradlo na jednom qubitu (spolu s fází na vstupu).

Ve Vídni mají čip z MIT: **26 módů, 88 laditelných MZI, 176 termooptických fázových posunů**, průměrná viditelnost
interference 99,94 %, délka asi 5 mm. *Vlastní výpočet:* univerzální interferometr pro $N$ módů potřebuje
$N(N-1)/2$ děličů (Reck a kol., 1994; slajd v kapitole o boson samplingu). Pro 26 módů je to 325; 88 MZI by
počtem stačilo na univerzální interferometr nejvýš pro 13 módů. Takový čip tedy neumí libovolnou transformaci
všech 26 módů, ale bohatou podmnožinu. Jak interferometry rozkládat, vykládají
[skripta v oddílu 1.3](/fotonika/zaklady#skripta-1-3).

### Detektory: supravodivé nanodrátky

Detektory jsou podle Walthera „téměř hotová technologie“. Nejlepší jsou **supravodivé nanodrátkové detektory
(SNSPD)**: proužek NbN široký do 200 nm a tenký do 10 nm, chlazený na 1–4 K, kterým teče proud 10–20 µA těsně
pod kritickou hodnotou. Dopadne-li foton, lokálně ohřeje drát (*hotspot*), proud musí obtékat kolem, překročí
kritickou hustotu a kousek drátu přestane být supravodivý. Skok odporu je signál. Tenký drát se rychle ochladí
a je připravený na další foton. Parametry ze slajdů: účinnost 95–97 % (na dotaz z publika: včetně pouzdra
a navázání z vlákna), mrtvá doba pod 50 ns, časový rozptyl (jitter) pod 100 ps. Víceprvkové detektory umějí i **rozlišit
počet fotonů** (účinnost kolem 93 %).

*Vlastní výpočet, proč na účinnosti tolik záleží:* pravděpodobnost, že se detekují všechny fotony, je součin
účinností. Při 95 % a 70 fotonech je to $0{,}95^{70} \approx 2{,}8\,\%$. Ztráty fotonů jsou proto hlavní nepřítel
fotonických experimentů – viz [skripta o ztrátách](/fotonika/zaklady#skripta-1-6).
""",
    further_reading=(
        Reading(UPPU_2021, "kvantové tečky jako zdroje a demultiplexování (slajd 29:00)"),
        Reading(HARRIS_2017, "čip 26 × 26 z MIT"),
        Reading(CALAFELL_COUNTERFACTUAL, "vídeňský experiment na čipu z MIT"),
        Reading(GREGANTI_DETECTORS),
    ),
)

GATES_TOPIC = TheoryTopic(
    anchor="walther-hradla",
    title="Univerzální počítač z fotonů: hradla s měřením a schéma KLM",
    in_short=(
        "Fotony spolu neinteragují, takže dvouqubitové hradlo CNOT jde postavit jen z interference a měření – "
        "s úspěšností 1/9 (fotony se zničí) nebo 1/4 (se dvěma pomocnými fotony). Schéma KLM dovede úspěšnost "
        "k jedné, ale za cenu $10^3$ až $10^5$ pomocných fotonů na qubit."
    ),
    explanation=r"""
**Proč je to těžké.** Hradla na jednom fotonu jsou snadná (destičky, MZI). Dvouqubitové hradlo ale potřebuje,
aby jeden foton ovlivnil druhý – a fotony spolu prakticky neinteragují. Typický příklad je **CNOT** (řízená
negace) v polarizaci:

$$
|H\rangle_C|H\rangle_T \to |H\rangle_C|H\rangle_T, \quad
|H\rangle_C|V\rangle_T \to |H\rangle_C|V\rangle_T, \quad
|V\rangle_C|H\rangle_T \to |V\rangle_C|V\rangle_T, \quad
|V\rangle_C|V\rangle_T \to |V\rangle_C|H\rangle_T .
$$

Je-li řídicí foton $C$ vodorovný, cílový $T$ se nezmění; je-li svislý, cílový se překlopí. Na slajdu je i obvod,
který z $|000\rangle$ pomocí $H$ a dvou CNOT vyrobí provázaný stav $(|000\rangle + |111\rangle)/\sqrt{2}$.

**Tři generace fotonického CNOT:**

1. **Destruktivní CNOT (2003):** chytrý interferometr, na jehož výstupu se fotony chovají, *jako by* prošly
   CNOT – ale jen s pravděpodobností $p = 1/9 \approx 11\,\%$ a fotony se musí detekovat, takže se zničí. „Splní
   misi, ale jsou mrtví.“
2. **Nedestruktivní, ohlašované CNOT se dvěma pomocnými fotony** (ancillami): větší interferometr, ve kterém se
   změří jen pomocné fotony a ohlásí, že hradlo proběhlo; řídicí a cílový foton letí dál. Úspěšnost
   $p = 1/4$. Vídeňská skupina ho postavila na čipu (Zeuner a kol., 2018).
3. **Schéma KLM** (Knill, Laflamme, Milburn, 2001): s rostoucím počtem pomocných fotonů jde úspěšnost dohnat
   libovolně blízko jedné. Je to škálovatelné – ne exponenciálně drahé – ale podle slajdu je potřeba
   **$10^3$ až $10^5$ pomocných fotonů na qubit**. A jednotlivé fotony jsou přesně to, co se dělá nejhůř:
   „hlava 22“.

Walther shrnuje: přístup, kdy se pro každé hradlo „obětují“ pomocné fotony, se nakonec neukázal jako nejlepší
architektura – lepší je úplně jiné schéma, výpočet měřením na velkém provázaném stavu (další kapitola). Srovnávací slajd
to říká jednou větou: *u měřením řízeného počítání se problém přesouvá do přípravy stavu.*

*Vlastní poznámka:* destruktivní CNOT z roku 2003 stojí na děličích s propustností 1/3; amplituda správného
výsledku je 1/3, pravděpodobnost tedy $(1/3)^2 = 1/9$. Elementární fotonická hradla formálně vykládají
[skripta v oddílu 1.2](/fotonika/zaklady#skripta-1-2). Ohlašované hradlo s úspěšností
$2/27$, které počítá i [stránka o Piquassu](/fotonika-ve-svete/piquasso#piquasso-qubity), je Knillova varianta bez
provázaných pomocných fotonů.
""",
    further_reading=(
        Reading(O_BRIEN_CNOT_2003, "destruktivní CNOT, $p = 1/9$"),
        Reading(ZEUNER_2018, "ohlašované CNOT na čipu, $p = 1/4$"),
        Reading(KLM, "schéma KLM"),
    ),
)

CLUSTER_TOPIC = TheoryTopic(
    anchor="walther-klastry",
    title="Měřením řízené počítání a klastrové stavy",
    in_short=(
        "Raussendorf a Briegel (2001): připrav velký provázaný klastrový stav a počítej jen měřeními jednotlivých "
        "qubitů. Úhel měření určuje rotaci, výsledky předchozích měření upravují další (feed-forward). Vodorovné "
        "řetízky jsou logické qubity, svislé spoje dvouqubitová hradla."
    ),
    explanation=r"""
**Myšlenka.** Abstrakt článku Raussendorfa a Briegela (Briegel je profesor v Innsbrucku – „rakouský příspěvek“)
Walther čte nahlas: *výpočet sestává výhradně z měření jednotlivých qubitů na zvláštní třídě provázaných stavů,
klastrových stavech. Měření do stavu „vtisknou“ logický obvod a zároveň zničí jeho provázání. Klastrové stavy jsou
tedy jednosměrné kvantové počítače a měření tvoří program.* Na rozdíl od obvodu se nedá jít zpět – změřený stav je
pryč – ale to nevadí, chceme jen výsledek.

**Jak klastrový stav vypadá.** Qubity v mřížce, každý ve stavu $|+\rangle = (|0\rangle + |1\rangle)/\sqrt{2}$,
a mezi každými dvěma sousedy se provede hradlo řízené fáze (CZ):

$$
\mathrm{CZ}\,|i\rangle|j\rangle = (-1)^{ij}\,|i\rangle|j\rangle, \qquad i, j \in \{0, 1\}.
$$

Slajd zapisuje totéž pomocí isingovské interakce $\exp\bigl[-i\tfrac{\pi}{4}\sum_{\langle j,k\rangle}
\sigma_z^{(j)}\sigma_z^{(k)}\bigr]$ aplikované na $|+\rangle^{\otimes n}$; od součinu hradel CZ se liší jen
rotacemi jednotlivých qubitů kolem osy $z$. Ekvivalentní popis: klastrový stav je společný vlastní stav
s vlastním číslem $+1$ operátorů $K_a = X_a \prod_{b \in N(a)} Z_b$ – na qubitu $a$ Pauliho $X$, na jeho sousedech
$Z$ (na slajdu křížek ze $Z$ kolem $X$).

**Jak se počítá.** Z mřížky se nejdřív odstraní qubity, které nepotřebujeme (měřením v bázi $Z$). Zbudou
vodorovné řetízky – **logické qubity** – a svislé spoje mezi nimi – **dvouqubitová hradla**. Čas plyne zleva
doprava. Každý qubit se změří v bázi z rovníku Blochovy sféry,

$$
|\pm_\delta\rangle = \frac{1}{\sqrt{2}}\bigl(|0\rangle \pm e^{i\delta}|1\rangle\bigr),
$$

a měření posune stav o krok dál po řetízku s rotací: po změření prvního qubitu je logický qubit ve stavu
$H\,R_z(-\delta)\,|+\rangle$, kde $R_z(\phi) = e^{-i\phi\sigma_z/2}$. **Úhel měření určuje rotaci.** Protože
výsledek měření je náhodný (±), přidá se k rotaci známá Pauliho chyba; opraví se tak, že se úhly dalších měření
upraví podle předchozích výsledků – tomu se říká *feed-forward*. Slajd ukazuje malé klastry (lineární, „podkova“,
čtverec) a obvody, které na nich jde spustit.

**Architektura.** Počítač je pak: *dej mi qubity, provaž je, měř podle pravidel, přečti výsledek*. Vídeňská
skupina to v roce 2005 jako první předvedla s fotony (Walther a kol., Nature 2005) – čtyřfotonový klastrový stav
z SPDC a jednoduché algoritmy na něm.

**Proč to s fotony není zadarmo.** Provázat fotony do klastru je opět to těžké dvouqubitové hradlo. Jak se to dá
obejít, je další kapitola.
""",
    further_reading=(
        Reading(RAUSSENDORF_BRIEGEL, "původní článek"),
        Reading(WALTHER_ONE_WAY_2005, "první fotonický experiment"),
    ),
)

FUSION_TOPIC = TheoryTopic(
    anchor="walther-fuze",
    title="Fúze, perkolace a plán fotonického počítače",
    in_short=(
        "Malé klastry se slepují „fúzemi“ – měřením na děliči svazku, které uspěje s pravděpodobností 50 %, vylepšené "
        "75 %. Teorie perkolace říká, že při dost vysoké úspěšnosti vždy existuje cesta přes celý stav. Stačí pak "
        "třífotonové GHZ stavy na povel a pasivní optika – to je plán PsiQuantum."
    ),
    explanation=r"""
**Fúzní hradlo.** Dva malé klastry (na slajdu dva třífotonové GHZ stavy) se pošlou po jednom fotonu na dělič
svazku a změří se. Když detektory ukážou správnou kombinaci, zbylé fotony se spojí do většího klastru (ze dvou
třífotonových vznikne čtyřfotonový: šest fotonů, dva se změřily, čtyři zbyly). Úspěšnost je ale jen **50 %**.
S pomocnými fotony jde úspěšnost zvýšit na **75 %** – buď se čtyřmi nezávislými pomocnými fotony, nebo se dvěma
provázanými. Fúze je tedy tři ze čtyř pokusů.

**Perkolace.** Proč stačí, aby fúze občas selhaly? Představ si kávu protékající mletou kávou (Walther: „Turtschi
aus Kaffee“): voda si najde cestu, i když spousta průchodů je ucpaných. Matematicky – teorie perkolace – má mřížka
s náhodně chybějícími spoji **práh**: je-li pravděpodobnost spoje nad prahem, existuje souvislá cesta přes celou
mřížku. Víme-li (z výsledků detektorů), které fúze uspěly, změříme výpočet podél té cesty – nemusí být rovná,
stačí že vede od začátku do konce.

Slajdy uvádějí dvě varianty:

- **5qubitové „hvězdy“** a fúze s úspěšností **50 %** – vznikne univerzální klastrový stav, pokud je úspěšnost
  nad prahem (Pant a kol., 2019);
- **třífotonové stavy** a fúze s úspěšností **75 %** – práh je podle grafu na slajdu $\lambda_c = 74{,}6\,\%$ (2D,
  Gimeno-Segovia a kol., 2015), pro 3D klastry 59 % (u ztrát zatím není jasné, jak to dopadne).

Je to kompromis mezi velikostí výchozího stavu a kvalitou fúzí.

**Plán (blueprint) podle Rudolpha (2017):**

1. deterministická výroba třífotonových GHZ stavů (Greenberger–Horne–Zeilinger),
2. fúze s úspěšností kolem 75 %,
3. průběžné „pěstování“ klastru **jen pasivní optikou**,
4. obyčejné měřením řízené počítání.

Jediná aktivní (přepínaná) vrstva je výroba GHZ stavů; klasické řízení sbírá výsledky fúzí a podle nich volí báze
měření. Walther zdůrazňuje rozdíl proti iontům a supravodičům: ty mají potíž s tím, jak systém **zvětšit**
(propojit další a další qubity). U fotonů je to naopak – nejtěžší je **první krok**, kvalitní třífotonový zdroj na
povel; „dej mi tři fotony a zbytek je základní optika“. Přesně tuhle architekturu staví **PsiQuantum** (Jeremy
O'Brien, dříve Bristol). Na slajdu je zpráva z roku 2021 o kole 450 milionů dolarů; Walther dodává, že celkem
firma získala „skoro miliardu“ (stav 2022).

**Jiné cesty k interakci fotonů** (vědecky zajímavé, slajd ve 45:30):

- **dutinová kvantová elektrodynamika** – atom v rezonátoru zprostředkuje interakci dvou fotonů (Caltech, MPQ,
  ICFO a další),
- **provázané stavy přímo z pevných látek** – kvantová tečka, která sama vyzařuje řetězec provázaných fotonů,
- **nelinearity grafenu** – vídeňský návrh hradla $\sqrt{\mathrm{SWAP}}$ s grafenovými plazmony.

Proč jsou potřeba zrovna třífotonové GHZ stavy, jak na ně přišli Greenberger, Horne a Zeilinger a jak je
vídeňská skupina poprvé vyrobila, rozvádí stránka [GHZ stavy](/fotonika/prednaska-walther-2022/ghz-stavy).

*Vlastní poznámka:* dnešní podoba plánu PsiQuantum se jmenuje fúzní kvantové počítání (FBQC, Bartolucci a kol.,
2023). Jak se firmě daří do roku 2026, popisuje stránka [PsiQuantum](/fotonika-ve-svete/psiquantum).
""",
    further_reading=(
        Reading(PANT_PERCOLATION, "perkolace s 5qubitovými hvězdami"),
        Reading(GIMENO_SEGOVIA_2015, "z třífotonových GHZ stavů k univerzálnímu počítání, práh 74,6 %"),
        Reading(RUDOLPH_2017, "plán na slajdu ve 44:06"),
        Reading(BARTOLUCCI_FBQC, "dnešní podoba plánu"),
        Reading(PSIQUANTUM_2021),
        Reading(CALAFELL_GRAPHENE, "vídeňský návrh hradla s grafenovými plazmony"),
    ),
)

BLIND_TOPIC = TheoryTopic(
    anchor="walther-slepe",
    title="Slepé kvantové počítání: bezpečný kvantový cloud",
    in_short=(
        "Klient připraví qubity s tajnými náhodnými fázemi, server je provází a měří v bázích, které mu klient řekne. "
        "Úhel měření, který server vidí, je posunutý o tajnou fázi, takže server nepozná vstup, program ani výsledek."
    ),
    explanation=r"""
Walther tohle považuje osobně za důležitější než rychlost: kvantové počítače mohou **chránit data**, což je pro
cloud a internet zásadní.

**Otázka z roku 1978.** Rivest (spoluautor RSA) se s kolegy ptal: *můžeme zpracovávat zašifrovaná data, aniž je
nejdřív rozšifrujeme?* Klasické řešení – plně homomorfní šifrování – přišlo až o 30 let později a má obrovskou
režii. Kvantové řešení je **slepé kvantové počítání (BQC)**: server dá klientovi plný výkon, ale nezná vstup,
program ani výstup.

**Princip** je průnik kvantové kryptografie (měření stav změní) a kvantového počítání. A protože se mluví o měření,
hodí se k tomu měřením řízené počítání. Protokol Broadbentové, Fitzsimonse a Kashefiové (BFK, 2009):

1. **Klient připraví qubity** $|\theta_j\rangle = \tfrac{1}{\sqrt{2}}\bigl(|0\rangle + e^{i\theta_j}|1\rangle\bigr)$
   s náhodným úhlem $\theta_j \in \{0, \pi/4, \dots, 7\pi/4\}$ – osm možností – a pošle je serveru. Klient tedy
   nepotřebuje kvantový počítač, jen umí posílat jednotlivé qubity.
2. **Server je provází** hradly CZ do klastrového stavu.
3. **Server měří** v rovině $X$–$Y$ v bázi s úhlem $\delta_j$, který mu klient sdělí.
4. **Výpočet:** logický qubit se otočí o $-\delta_j + \theta_j$; klient chce rotaci o svůj tajný úhel $\phi_j$,
   proto pošle $\delta_j = \phi_j + \theta_j + r_j\pi$ s náhodným bitem $r_j$ (ten skryje i výsledek měření).

Server zná $\delta_j$, ale ne $\theta_j$ – a k pochopení, co měření s qubitem udělá, potřebuje obojí. Na slajdu:
*skutečný úhel měření je skrytý.* „Tak jednoduché to je.“

*Vlastní výpočet, proč server nic nepozná:* pro libovolný tajný úhel $\phi_j$ z osmi možností dává náhodné
$\theta_j$ (osm možností) a $r_j$ (dvě) úhel $\delta_j$ rozložený rovnoměrně přes všech osm hodnot. Rozložení
toho, co server vidí, tedy na programu vůbec nezávisí.

**Experiment.** Ve Vídni to v roce 2012 předvedli s fotony (Barz a kol., Science): univerzální sadu jednoqubitových
hradel, netriviální dvouqubitová hradla a Deutschův a Groverův algoritmus naslepo. Navazující práce (Greganti
a kol., 2016) ukázala variantu, kde klient jen měří. Walther: fotony jsou ideální nosič pro kvantové cloudy
a skupina na tom pracuje dál.
""",
    further_reading=(
        Reading(RIVEST_1978, "původní otázka"),
        Reading(BFK_2009, "protokol BFK"),
        Reading(BARZ_2012, "fotonický experiment"),
        Reading(GREGANTI_2016, "varianta, kde klient jen měří"),
    ),
)

SWITCH_TOPIC = TheoryTopic(
    anchor="walther-prepinac",
    title="Superpozice pořadí hradel: kvantový přepínač",
    in_short=(
        "Kvantová mechanika dovoluje superponovat i pořadí operací: „$U_1$ před $U_2$“ a „$U_2$ před $U_1$“ zároveň. "
        "Jeden foton, který projde oběma pořadími naráz, jediným průchodem rozliší, zda hradla komutují, nebo "
        "antikomutují. Vídeňský experiment měl úspěšnost 0,976."
    ),
    explanation=r"""
**Superponovat jde všechno.** Superpozici stavů (spin nahoru a dolů, kruhová polarizace $R$ a $L$) už známe.
Teoretici kolem Časlava Bruknera ve Vídni (Oreshkov, Costa, Brukner, 2012) a Giulia Chiribelly ukázali, že
kvantová mechanika dovoluje superponovat i **kauzální vztahy**: „$A$ je před $B$“ plus „$B$ je před $A$“. Pro
základy fyziky a obecnou relativitu je to zajímavé samo o sobě; Walther to bere pragmaticky jako **superpozici
pořadí hradel** – nový druh „softwarové“ architektury.

**Kvantový přepínač** (*quantum switch*). V běžném obvodu mají hradla pevné pořadí. V přepínači řídicí qubit
rozhodne: je-li $|0\rangle$, projde cílový stav $|\psi\rangle$ nejdřív $U_1$, pak $U_2$; je-li $|1\rangle$, opačně.
Je-li řídicí qubit v superpozici, dostaneme

$$
\frac{1}{\sqrt{2}}\bigl(|0\rangle + |1\rangle\bigr)|\psi\rangle \;\to\;
\frac{1}{\sqrt{2}}|0\rangle\,U_2U_1|\psi\rangle + \frac{1}{\sqrt{2}}|1\rangle\,U_1U_2|\psi\rangle .
$$

(Dva slajdy přiřazují pořadí k $|0\rangle$ a $|1\rangle$ navzájem obráceně; na výsledku níže to nic nemění.)

**K čemu to je.** Úloha (Chiribella, 2012): máme dvě hradla, o kterých víme, že buď **komutují**
($U_1U_2 = U_2U_1$), nebo **antikomutují** ($U_1U_2 = -U_2U_1$). Které z toho platí? Změří-li se řídicí qubit
v bázi $|\pm\rangle$ (u fotonu: dráhy se na konci sejdou na děliči svazku), vyjde

$$
\frac{1}{2}|+\rangle\,\{U_1, U_2\}|\psi\rangle + \frac{1}{2}|-\rangle\,[U_1, U_2]|\psi\rangle ,
$$

kde $\{U_1, U_2\} = U_1U_2 + U_2U_1$ je antikomutátor a $[U_1, U_2] = U_1U_2 - U_2U_1$ komutátor. Komutují-li
hradla, komutátor je nulový a foton vyjde **vždy jedním výstupem**; antikomutují-li, vždy druhým. Stačí **jedno
použití každého hradla**. Běžný kvantový obvod s pevným pořadím by podle Walthera potřeboval jedno z hradel
použít dvakrát. Na konci se dráhy musí spojit na děliči, aby „příroda nevěděla“, které pořadí nastalo – jinak by
se interference ztratila.

**Experiment** (Procopio a kol., 2015): ohlašovaný foton z SPDC, řídicí qubit je dráha, cílový polarizace,
hradla $U_1$, $U_2$ jsou sady vlnových destiček. Pro všech 16 dvojic z $\{I, X, Y, Z\}$ (Pauliho matice) foton
vyšel správným výstupem: $X$ s $X$ komutuje, $X$ s $Y$ antikomutuje – „co se učí v prvním semestru“. Průměrná
úspěšnost $0{,}976 \pm 0{,}015$ (na slajdu chybí desetinná čárka u chyby). Navazující experiment (Rubino a kol.,
2017) ověřil neurčité kauzální pořadí přímo.

*Vlastní výpočet:* pravděpodobnost výstupu „komutují“ je $\|\{U_1, U_2\}\psi\|^2/4$ a „antikomutují“
$\|[U_1, U_2]\psi\|^2/4$. Pro $X, X$ vychází 1 a 0, pro $X, Y$ 0 a 1 – pro libovolný vstupní stav $\psi$.
""",
    further_reading=(
        Reading(OCB_2012, "procesy bez pevného kauzálního pořadí"),
        Reading(CHIRIBELLA_2012, "úloha komutují × antikomutují"),
        Reading(CHIRIBELLA_SWITCH, "kvantový přepínač"),
        Reading(PROCOPIO_2015, "vídeňský experiment"),
        Reading(RUBINO_2017),
    ),
)

BOSON_SAMPLING_TOPIC = TheoryTopic(
    anchor="walther-boson-sampling",
    title="Boson sampling a kvantová nadřazenost",
    in_short=(
        "Dva fotony na děliči svazku odejdou vždy spolu, protože se vyruší amplitudy „oba projdou“ a „oba se "
        "odrazí“ – to je permanent matice. Permanent je #P-těžký, a proto je těžké i vzorkovat výstupy velkého "
        "interferometru. Klasická mez kolem 70 fotonů; po Googlu (2019) ji překonal čínský Jiuzhang (2020)."
    ),
    explanation=r"""
**Nadřazenost** (*supremacy*, dnes spíš *kvantová výhoda*) znamená experiment, jehož výsledek klasický počítač
v rozumném čase nespočítá. Walther upozorňuje, že to není v rozporu s rekordem 24 provázaných qubitů: k těmto
úlohám nepotřebujeme ovladatelné provázání, jen složité zpracování. Fotony byly mezi prvními kandidáty.

**Dva fotony a permanent.** Dělič svazku popisuje matice $U = \begin{pmatrix} a & b \\ c & d \end{pmatrix}$,
pro souměrný dělič $\tfrac{1}{\sqrt{2}}\begin{pmatrix} 1 & i \\ i & 1 \end{pmatrix}$ (odraz přidá fázi $i$). Přijdou-li
dva fotony každý jedním vstupem, mohou odejít každý jiným výstupem dvěma způsoby: oba projdou, nebo se oba odrazí.
Amplituda je součet obou cest, $ad + cb$ – a to je **permanent** matice $U$, „determinant se všemi znaménky plus“.
Pro dělič s amplitudami propustnosti $T$ a odrazu $iR$:

$$
P_{\text{koincidence}} = \left|\mathrm{Perm}\begin{pmatrix} T & iR \\ iR & T \end{pmatrix}\right|^2 = |T^2 - R^2|^2 .
$$

Pro dělič 50 : 50 je $T = R = 1/\sqrt{2}$, permanent je nula a fotony **odejdou vždy stejným výstupem**
(Hongův–Ouův–Mandelův jev, 1987). Walther: dává to smysl, fotony jsou bosony, „rády se shlukují“.

**Proč je to těžké.** Determinant se počítá rychle, permanent ne – patří do třídy **#P** (počítání řešení, ještě
těžší než úlohy typu obchodního cestujícího). Aaronson a Arkhipov (2010) ukázali, že těžké je dokonce jen
**vzorkovat** výstupy: pošleme $n$ fotonů do $m$ módů interferometru $U$, vstup $|1, \dots, 1, 0, \dots, 0\rangle$,
a pravděpodobnost výstupu s obsazeními $s_1, \dots, s_m$ je

$$
p_S = \frac{|\mathrm{Per}(A_S)|^2}{s_1!\, s_2! \cdots s_m!},
$$

kde $A_S$ je podmatice $U$ vybraná podle vstupních a výstupních módů. Fotony „spočítají permanent zadarmo“.
Interferometr libovolné unitární matice jde poskládat z děličů a fázových posunů (Reck a kol., 1994; nejvýš
$N(N-1)/2$ děličů pro $N$ módů). Je to *neuniverzální* kvantové počítání – podmnožina toho, co umí univerzální
počítač.

**Klasická mez kolem 70 fotonů** (slajd), Walther říká „70 fotonů ve zhruba 200 módech“. *Vlastní výpočet:*
70 nerozlišitelných fotonů ve 200 módech může skončit v $\binom{269}{70} \approx 10^{66}$ různých výstupech. Walther
to přirovnává k autu ThrustSSC, které jako první překonalo rychlost zvuku na zemi: neumělo zatočit ani brzdit,
ale ukázalo, že žádná základní mez neexistuje. Boson sampling taky není užitečný výpočet – aplikace se teprve
hledají.

**Historie.** Po článku Aaronsona a Arkhipova se do závodu pustily skupiny z Itálie, Oxfordu, Austrálie
i Vídně – se 3 až 4 fotony, aby ověřily, že to funguje (čtyři experimenty z roku 2013). První nadřazenost ale
ohlásil **Google (2019)** se supravodivým čipem Sycamore (53 qubitů) a náhodnými obvody. Fotony se vrátily
o rok později: **Jiuzhang** z USTC (Čína, 2020) – Gaussian Boson Sampling s 50 stlačenými stavy ve 100módovém
interferometru a až 76 detekovanými fotony. Slajd porovnává velikost stavového prostoru: Google $10^{16}$, Čína
$10^{30}$ – o 14 řádů víc. *Vlastní výpočet:* $2^{53} \approx 9 \cdot 10^{15}$ (53 qubitů) a
$2^{100} \approx 1{,}3 \cdot 10^{30}$ (100 detektorů, každý rozliší jen „klik“ nebo „nic“). Slajd uvádí u Googlu
rok 2018; článek vyšel v Nature v říjnu 2019.

Walther končí tím, že nadřazenost je „hotová věc“ a strach, že škálování kvantových počítačů brání nějaká
základní mez, je pryč.

*Vlastní poznámka:* klasické algoritmy od té doby část nároků oslabily (u Sycamoru i u Jiuzhangu), závod
pokračuje – shrnuto na [Fotonice ve světě](/fotonika-ve-svete#svet-kdo-postavil-gbs). Jiuzhang i Borealis jsou
*Gaussian* Boson Sampling se stlačeným světlem, kde místo permanentu vystupuje hafnián; rozdíl vykládá
[stránka o hafniánu a permanentu](/gbs/hafnian#hafnian-permanent)
a [skripta, kapitola 4](/fotonika/gaussian-boson-sampling).
Matematiku boson samplingu podrobně: [skripta, oddíl 1.5](/fotonika/zaklady#skripta-1-5).
""",
    further_reading=(
        Reading(HONG_OU_MANDEL, "shlukování dvou fotonů"),
        Reading(AARONSON_ARKHIPOV, "původně arXiv:1011.3245 (2010), citovaný na slajdu"),
        Reading(RECK, "rozklad interferometru na děliče"),
        Reading(FIRST_BOSON_SAMPLING, "mezi nimi vídeňský experiment Tillmanna a kol."),
        Reading(LUND_BREMNER_RALPH, "přehled ze slajdu"),
        Reading(ARUTE_2019, "Google, 2019"),
        Reading(ZHONG, "Jiuzhang, 2020"),
        Reading(MADSEN, "Borealis od Xanadu, 2022 – „ještě větší výsledky“, o kterých Walther mluví"),
    ),
)

OUTLOOK_TOPIC = TheoryTopic(
    anchor="walther-zaver",
    title="Závěr: jasná budoucnost pro mnoho aplikací",
    in_short=(
        "Budoucnost je jasná ne kvůli humbuku a inženýrství, ale protože ještě nevíme, co všechno jde udělat: "
        "bezpečný cloud, boson sampling, superpozice hradel, posilované učení a kvantový memristor."
    ),
    explanation=r"""
Na kapitolu o strojovém učení už nezbyl čas – Walther jen ukáže úvodní slajd (*fotonické kvantové počítání pro
posilované učení*) a přehled aplikací memristorů, „rezistorů s pamětí“, které napodobují synapse v neuronových
sítích. Závěrečný slajd shrnuje vídeňské výsledky:

- **bezpečný kvantový cloud** – Science 335, 303 (2012),
- **úsporné kvantové počítání (boson sampling)** – Nature Photonics 7, 540 (2013),
- **kvantové počítání se superponovaným pořadím hradel** – Nature Communications 6, 7913 (2015), Science Advances 3,
  e1602589 (2017),
- **posilované učení (kvantové strojové učení)** – Nature 591, 229 (2021): kvantový agent se učí rychleji,
- **kvantový memristor (kvantové neuronové sítě)** – Nature Photonics 16, 318 (2022).

Poselství: *jasná budoucnost – ne kvůli humbuku a inženýrským výzvám, ale protože je pořád otevřené, co všechno
se dá udělat.* Strojové učení a napodobování neuronových sítí v mozku jsou další směry. Přednáška končí poděkováním
týmu Quantum Photonics („já jen předvádím jejich peří“) a nabídkou doktorských a postdoktorských míst.

*Vlastní poznámka pro disertaci:* z přednášky plyne, proč je pro modifikované Monte Carlo zajímavý právě
(Gaussian) Boson Sampling – je to fotonická úloha, která nepotřebuje dvouqubitová hradla ani klastrové stavy,
jen zdroj, interferometr a detektory. Zároveň je vidět jeho hlavní slabina: ztráty a nedokonalé zdroje. To jsou
přesně otázky stránek [Fotonika ve světě](/fotonika-ve-svete) a [Piquasso](/fotonika-ve-svete/piquasso).
""",
    further_reading=(
        Reading(SAGGIO_2021, "posilované učení"),
        Reading(SPAGNOLO_2022, "kvantový memristor"),
        Reading(MAZUMDER_2012, "přehled aplikací memristorů ze slajdu"),
        Reading(WALTHER_GROUP),
    ),
)

TOPICS: Tuple[TheoryTopic, ...] = (
    INTRODUCTION_TOPIC,
    SUPERPOSITION_TOPIC,
    ENTANGLEMENT_TOPIC,
    ALGORITHMS_TOPIC,
    RACE_TOPIC,
    HARDWARE_TOPIC,
    GATES_TOPIC,
    CLUSTER_TOPIC,
    FUSION_TOPIC,
    BLIND_TOPIC,
    SWITCH_TOPIC,
    BOSON_SAMPLING_TOPIC,
    OUTLOOK_TOPIC,
)

CHAPTER_TIMES: Tuple[ChapterTime, ...] = (
    ChapterTime(INTRODUCTION_TOPIC.anchor, 0),
    ChapterTime(SUPERPOSITION_TOPIC.anchor, 494),
    ChapterTime(ENTANGLEMENT_TOPIC.anchor, 711),
    ChapterTime(ALGORITHMS_TOPIC.anchor, 933),
    ChapterTime(RACE_TOPIC.anchor, 1321),
    ChapterTime(HARDWARE_TOPIC.anchor, 1545),
    ChapterTime(GATES_TOPIC.anchor, 2054),
    ChapterTime(CLUSTER_TOPIC.anchor, 2275),
    ChapterTime(FUSION_TOPIC.anchor, 2470),
    ChapterTime(BLIND_TOPIC.anchor, 2760),
    ChapterTime(SWITCH_TOPIC.anchor, 3050),
    ChapterTime(BOSON_SAMPLING_TOPIC.anchor, 3300),
    ChapterTime(OUTLOOK_TOPIC.anchor, 3760),
)
"""Where each chapter starts in the recording; the slides between two starts belong to the earlier chapter."""

SLIDES: Tuple[LectureSlide, ...] = (
    LectureSlide("slajd_0005.jpg", "Titulní slajd přednášky"),
    LectureSlide("slajd_0433.jpg", "Schrödingerův citát o ichtyosaurech (1952)"),
    LectureSlide("slajd_0459.jpg", "Druhá kvantová revoluce: ionty, atomy, mikrovlny, fotony"),
    LectureSlide("slajd_0494.jpg", "Superpozice jednoho fotonu na děliči svazku"),
    LectureSlide("slajd_0542.jpg", "Superpozice ve vlnovodech na čipu (animace směrové spojky)"),
    LectureSlide("slajd_0611.jpg", "Bit a qubit: N qubitů nese 2^N čísel"),
    LectureSlide("slajd_0660.jpg", "Polarizační qubity: vlnové destičky, Blochova sféra, převod na dráhu"),
    LectureSlide("slajd_0711.jpg", "Kvantové provázání"),
    LectureSlide("slajd_0766.jpg", "Provázané fotony ze sestupné parametrické konverze"),
    LectureSlide("slajd_0856.jpg", "Nobelova cena za fyziku 2022"),
    LectureSlide("slajd_0896.jpg", "Kde se fotonické kvantové systémy uplatní"),
    LectureSlide("slajd_0933.jpg", "Kvantový počítač: vstup, zpracování, výstup"),
    LectureSlide("slajd_1060.jpg", "Koncept kvantového počítání: interference, obvod, algoritmy"),
    LectureSlide("slajd_1169.jpg", "Kvantové algoritmy a jejich zrychlení"),
    LectureSlide("slajd_1321.jpg", "Závod architektur (The Economist, 2015)"),
    LectureSlide("slajd_1349.jpg", "Vývoj počtu fyzikálních qubitů 1998–2026 (Yole, 2021)"),
    LectureSlide("slajd_1547.jpg", "Fotonický počítač: zdroje, manipulace, detekce"),
    LectureSlide("slajd_1637.jpg", "Zdroje jednotlivých fotonů: spontánní a deterministické"),
    LectureSlide("slajd_1740.jpg", "Mnoho fotonů: multiplexování SPDC a demultiplexování kvantové tečky"),
    LectureSlide("slajd_1839.jpg", "Integrovaná fotonika: Machův–Zehnderův interferometr"),
    LectureSlide("slajd_1865.jpg", "Laditelný čip 26 × 26 z MIT"),
    LectureSlide("slajd_1921.jpg", "Detekce fotonů supravodivými nanodrátky"),
    LectureSlide("slajd_1964.jpg", "Detektory rozlišující počet fotonů"),
    LectureSlide("slajd_2054.jpg", "Oddíl: univerzální fotonické počítání"),
    LectureSlide("slajd_2187.jpg", "Lineárně optická hradla CNOT: destruktivní a ohlašované"),
    LectureSlide("slajd_2278.jpg", "Dvě architektury: obvodový model (KLM) a klastrové stavy"),
    LectureSlide("slajd_2306.jpg", "Raussendorf a Briegel: jednosměrný kvantový počítač (2001)"),
    LectureSlide("slajd_2365.jpg", "Klastrový stav"),
    LectureSlide("slajd_2421.jpg", "Výpočet měřením: logické qubity a hradla na klastru"),
    LectureSlide("slajd_2456.jpg", "Výpočet na klastrovém stavu krok za krokem"),
    LectureSlide("slajd_2532.jpg", "Fúzní hradla: úspěšnost 50 % a 75 %"),
    LectureSlide("slajd_2552.jpg", "Perkolace a fúze ve 3D"),
    LectureSlide("slajd_2601.jpg", "Perkolace a fúze ve 2D: práh 74,6 %"),
    LectureSlide("slajd_2676.jpg", "Plán fotonického kvantového počítače (Rudolph, 2017)"),
    LectureSlide("slajd_2695.jpg", "PsiQuantum získává 450 milionů dolarů (2021)"),
    LectureSlide("slajd_2730.jpg", "Nelineární optická hradla: dutinová QED, pevné látky, grafen"),
    LectureSlide("slajd_2763.jpg", "Oddíl: fotonické počítání pro bezpečné kvantové cloudy"),
    LectureSlide("slajd_2823.jpg", "Cloud a Rivestova otázka (1978)"),
    LectureSlide("slajd_2920.jpg", "Slepé kvantové počítání: klient a server"),
    LectureSlide("slajd_2990.jpg", "Protokol BFK krok za krokem"),
    LectureSlide("slajd_3028.jpg", "Bezpečný fotonický kvantový cloud v laboratoři"),
    LectureSlide("slajd_3054.jpg", "Oddíl: superpozice kvantového softwaru"),
    LectureSlide("slajd_3103.jpg", "Superpozice stavů a kauzálních vztahů"),
    LectureSlide("slajd_3134.jpg", "Pevné pořadí hradel v běžném algoritmu"),
    LectureSlide("slajd_3157.jpg", "Kvantový přepínač: dvě pořadí hradel"),
    LectureSlide("slajd_3174.jpg", "Kvantový přepínač: obě pořadí v superpozici"),
    LectureSlide("slajd_3189.jpg", "K čemu to je: komutují, nebo antikomutují?"),
    LectureSlide("slajd_3214.jpg", "Vídeňská aparatura a výsledky pro 16 dvojic hradel"),
    LectureSlide("slajd_3307.jpg", "Oddíl: fotonické počítání pro kvantovou nadřazenost"),
    LectureSlide("slajd_3364.jpg", "Dva fotony na děliči: permanent a Hongův–Ouův–Mandelův jev"),
    LectureSlide("slajd_3484.jpg", "Libovolná unitární transformace z děličů (Reck a kol., 1994)"),
    LectureSlide("slajd_3494.jpg", "Boson sampling: pravděpodobnost výstupu přes permanent"),
    LectureSlide("slajd_3536.jpg", "Klasická mez kolem 70 fotonů (auto ThrustSSC)"),
    LectureSlide("slajd_3606.jpg", "Animace boson samplingu"),
    LectureSlide("slajd_3611.jpg", "První experimenty se 3–4 fotony (2013)"),
    LectureSlide("slajd_3653.jpg", "Google: nadřazenost s 53 supravodivými qubity (2019)"),
    LectureSlide("slajd_3681.jpg", "Čína: Jiuzhang, 76 fotonů (2020)"),
    LectureSlide("slajd_3765.jpg", "Oddíl: fotonické počítání pro posilované učení"),
    LectureSlide("slajd_3775.jpg", "Aplikace memristorů"),
    LectureSlide("slajd_3777.jpg", "Shrnutí: jasná budoucnost pro mnoho aplikací"),
    LectureSlide("slajd_3817.jpg", "Tým Quantum Photonics a poděkování"),
)
"""Every distinct slide of the talk; of an animated slide only its last step, frames repeating a slide are left out."""


def chapter_start(anchor: str) -> int:
    return next(chapter.start for chapter in CHAPTER_TIMES if chapter.anchor == anchor)


def chapter_end(anchor: str) -> int:
    starts = [chapter.start for chapter in CHAPTER_TIMES]
    index = [chapter.anchor for chapter in CHAPTER_TIMES].index(anchor)
    return starts[index + 1] if index + 1 < len(starts) else VIDEO_SECONDS


def chapter_slides(anchor: str) -> Tuple[LectureSlide, ...]:
    start, end = chapter_start(anchor), chapter_end(anchor)
    return tuple(slide for slide in SLIDES if start <= slide.seconds < end)


def video_at(seconds: int) -> str:
    return f"{VIDEO_URL}?t={seconds}"


def timestamp(seconds: int) -> str:
    """„25:47“, or „1:02:45“ past the first hour, as YouTube writes it."""
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours}:{minutes:02d}:{secs:02d}" if hours else f"{minutes}:{secs:02d}"
