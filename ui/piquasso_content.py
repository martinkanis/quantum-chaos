"""Texts of the page on Piquasso, the photonic quantum computer simulator, and on translating between qubits and photons.

Piquasso and Qiskit are not dependencies of the app (Piquasso 8 needs Python 3.10 or newer), so the numbers they
produced are stored here; scripts/piquasso_gbs_check.py and scripts/qiskit_native_gate_counts.py create them.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from ui.advantage_content import QISKIT_DOCUMENTATION
from ui.literature_review_content import PERCEVAL
from ui.navigation import ADVANTAGE_PATH, CAVEATS_PATH, GUIDE_PATH, PHOTONICS_LANDSCAPE_PATH
from ui.photonics_landscape_content import STRAWBERRY_FIELDS_ARCHIVED, VLQ_INAUGURATION
from ui.theory_content import KRUSE, PIQUASSO_PAPER, KeyFinding, Reading, Source, TheoryTopic

TITLE = "Piquasso: simulátor fotonického kvantového počítače"
SOURCES_ANCHOR = "piquasso-zdroje"
SOURCES_CHECKED_DATE = "26. 10. 2026"
PIQUASSO_VERSION = "8.0.2"

INTRO = (
    "Co je Piquasso, jak se v něm píše fotonický obvod, který ze čtyř simulátorů zvolit a jak s ním ověřit výpočty "
    "této aplikace. Na konci překlad mezi qubity a fotony oběma směry, včetně otázky, jestli jde GBS spustit na "
    f"qubitovém počítači VLQ v Ostravě. Čísla z Piquassa {PIQUASSO_VERSION} a z Qiskitu jsou z našich vlastních "
    f"výpočtů; zdroje ověřeny {SOURCES_CHECKED_DATE}."
)


@dataclass(frozen=True)
class PiquassoProbability:
    problem_key: str
    probability: float
    """p(n) of the target pattern from GaussianSimulator.get_particle_detection_probability."""


@dataclass(frozen=True)
class PiquassoSampling:
    measurement_cutoff: int
    shots: int
    hits: int
    """Shots that gave exactly the target pattern."""
    max_photons_per_mode: int
    mean_photons: float
    """Mean number of detected photons per shot."""
    mean_photons_error: float
    """Standard error of that mean."""
    estimate: float
    """GBS-P estimate of the moment from the frequency hits / shots."""


@dataclass(frozen=True)
class NativeGateCount:
    problem_key: str
    qubits: int
    cz: int
    """CZ gates after transpiling the exported circuit to the IQM native gates PRX and CZ (all-to-all coupling)."""
    qasm_lines: int
    """Lines of the same circuit written as OpenQASM 3."""
    state_preparation_cz: int
    """CZ gates of preparing one mode by Qiskit's StatePreparation instead of a full unitary."""


PIQUASSO_PROBABILITIES: Tuple[PiquassoProbability, ...] = (
    PiquassoProbability("extremni-moment", 0.023604564912671416),
    PiquassoProbability("spolecny-extrem", 0.0040227146916575005),
    PiquassoProbability("nesoumerny-monom", 0.004837752697504781),
    PiquassoProbability("historie-usa", 0.00034657916068379447),
    PiquassoProbability("trzni-faktor", 0.00024849307072256373),
)
"""Output of scripts/piquasso_gbs_check.py with Piquasso 8.0.2; the page puts the app's own values next to them."""

SAMPLED_PROBLEM = "spolecny-extrem"
SAMPLING_SEED = 42
PIQUASSO_SAMPLING: Tuple[PiquassoSampling, ...] = (
    PiquassoSampling(5, 20000, 0, 4, 2.86, 0.02, 0.0),
    PiquassoSampling(40, 20000, 70, 39, 14.20, 0.12, 162631.0),
    PiquassoSampling(80, 20000, 70, 79, 15.16, 0.14, 162631.0),
)
"""Output of scripts/piquasso_gbs_check.py: 20 000 shots of problem 2 („Společný extrém dvou aktiv“), seed 42."""
FAILING_MEASUREMENT_CUTOFF = 160
"""With this cutoff the sampler of Piquasso 8.0.2 stops with „ValueError: Probabilities contain NaN“."""

DUAL_RAIL_CNOT_SUCCESS = 0.07406872654316693
"""Norm of the post-selected state of H + CNOT encoded by dual_rail_encode_from_qiskit (cutoff 7)."""
TWO_QUBIT_GATES_EXAMPLE = 10

QISKIT_NATIVE_GATE_COUNTS: Tuple[NativeGateCount, ...] = (
    NativeGateCount("extremni-moment", qubits=8, cz=16812, qasm_lines=70240, state_preparation_cz=120),
    NativeGateCount("spolecny-extrem", qubits=10, cz=479535, qasm_lines=2007190, state_preparation_cz=11),
)
"""Output of scripts/qiskit_native_gate_counts.py (Qiskit 2.6.1)."""
ASSUMED_GATE_FIDELITY = 0.99
"""Our assumption for one qubit–resonator operation, not a measured value of VLQ."""
OPERATIONS_PER_CZ_ON_STAR = 3
"""MOVE, CZ, MOVE: a CZ between two qubits of the star topology goes through the central resonator."""

PIQUASSO_REPOSITORY = Source(
    "Budapest Quantum Computing Group: [Piquasso na GitHubu](https://github.com/Budapest-Quantum-Computing-Group/"
    "piquasso) – zdrojový kód, licence Apache 2.0, změny verzí v CHANGELOG.md"
)
PIQUASSO_PYPI = Source(
    "PyPI: [piquasso 8.0.2](https://pypi.org/project/piquasso/8.0.2/) – vydáno 20. 10. 2026, Python 3.10 až 3.14"
)
PIQUASSO_DOCUMENTATION = Source(
    "[Dokumentace Piquassa](https://piquasso.readthedocs.io) – návody včetně Gaussian Boson Samplingu a popis "
    "simulátorů"
)
PIQUASSO_BOOST = Source(
    "Budapest Quantum Computing Group: [Piquasso Boost](https://github.com/Budapest-Quantum-Computing-Group/"
    "piquassoboost) – rychlé výpočty permanentu, hafniánu a torontiánu v C/C++"
)
MORSE_DATA_FLOW = Source(
    "Morse, G. a kol.: *High performance Boson sampling simulation via data-flow engines*. New Journal of Physics "
    "26, 033033 (2024), [arXiv:2309.07027](https://arxiv.org/abs/2309.07027)"
)
KAPOSI_TORONTONIAN = Source(
    "Kaposi, Á., Kolarovszki, Z., Kozsik, T., Zimborás, Z., Rakyta, P.: *Polynomial speedup in Torontonian "
    "calculation by a scalable recursive algorithm*. [arXiv:2109.04528](https://arxiv.org/abs/2109.04528) (2021)"
)
BLACKBIRD = Source(
    "Xanadu: [Blackbird](https://github.com/XanaduAI/blackbird) – jazyk pro zápis fotonických obvodů, obdoba "
    "OpenQASM pro fotoniku"
)
PIQUASSO_DUAL_RAIL = Source(
    "Piquasso: [dual_rail_encoding.py](https://github.com/Budapest-Quantum-Computing-Group/piquasso/blob/main/"
    "piquasso/dual_rail_encoding.py) – převod obvodu z Qiskitu na fotonický program"
)
KNILL_POSTSELECTION = Source(
    "Knill, E.: *Quantum gates using linear optics and postselection*. Physical Review A 66, 052306 (2002), "
    "[doi:10.1103/PhysRevA.66.052306](https://doi.org/10.1103/PhysRevA.66.052306)"
)
KLM = Source(
    "Knill, E., Laflamme, R., Milburn, G. J.: *A scheme for efficient quantum computation with linear optics*. "
    "Nature 409, 46–52 (2001), [doi:10.1038/35051009](https://doi.org/10.1038/35051009)"
)
SHENDE_SYNTHESIS = Source(
    "Shende, V. V., Bullock, S. S., Markov, I. L.: *Synthesis of quantum-logic circuits*. IEEE Transactions on "
    "Computer-Aided Design 25, 1000–1010 (2006), [arXiv:quant-ph/0406176](https://arxiv.org/abs/quant-ph/0406176)"
)
IQM_STAR_TRANSPILE = Source(
    "IQM: [iqm-client, modul transpile](https://github.com/iqm-finland/iqm-client/blob/main/src/iqm/iqm_client/"
    "transpile.py) – hvězdicová architektura, brána mezi dvěma qubity jako MOVE, CZ, MOVE přes rezonátor"
)
VLQ_STAR_TOPOLOGY = Source(
    "Business Wire: [IQM Quantum Computers to deliver Czech Republic’s first quantum computer with unique star "
    "topology](https://www.businesswire.com/news/home/20240926088435/en), září 2024"
)

ABOUT_TOPIC = TheoryTopic(
    anchor="piquasso-co-to-je",
    title="Co je Piquasso a kdo ho vyvíjí",
    in_short=(
        "Open-source simulátor fotonických kvantových počítačů z Budapešti: rozhraní v Pythonu, náročné výpočty "
        "(permanent, hafnián, torontián) v C++. Umí spojité proměnné (gaussovské stavy, GBS) i jednotlivé fotony "
        "(boson sampling). Licence Apache 2.0, článek v časopise Quantum z roku 2025."
    ),
    explanation=r"""
**Kdo.** Piquasso vyvíjí Budapest Quantum Computing Group, vývojáři a fyzici z Eötvösovy univerzity (ELTE)
a z Wignerova výzkumného centra pro fyziku v Budapešti. Hlavní článek *Piquasso: A Photonic Quantum Computer
Simulation Software Platform* vyšel v časopise *Quantum* 9, 1708 (2025); má třináct autorů, prvním je Zoltán
Kolarovszki, posledním Zoltán Zimborás. Vývoj podpořila maďarská Národní laboratoř kvantové informace.

**Co to je.** Knihovna, ve které se fotonický obvod napíše jako program – příprava stavu, brány, měření a ztráty –
a pak spustí na *simulátoru*, který stav drží v reprezentaci vhodné pro danou úlohu (další kapitoly). Výpočetní
jádra, tedy permanent, hafnián, torontián a pfaffián, jsou v C++ a balíček je obsahuje už předkompilovaná.
Rychlejší verze pro desítky fotonů, s paralelizací na více jader a variantou pro programovatelná hradlová pole
(FPGA), jsou v samostatném projektu Piquasso Boost. Programy jde derivovat podle parametrů přes TensorFlow nebo JAX
(*diferencovatelné programování*: parametry obvodu se ladí gradientním sestupem) a od verze 8.0 počítá permanent
i grafická karta přes JAX.

**Verze a instalace.** Na PyPI je Piquasso od listopadu 2021; aktuální verze 8.0.2 vyšla 20. 10. 2026 a potřebuje
Python 3.10 až 3.14. Instalace je `pip install piquasso`, volitelné části přes `piquasso[jax]`,
`piquasso[tensorflow]` nebo `piquasso[qiskit]`.

**Proč právě Piquasso.** Software firmy Xanadu pro GBS (Strawberry Fields, The Walrus) je od roku 2026
archivovaný. Perceval od Quandely je stavěný na jednotlivé fotony; podle autorů Piquassa se nezaměřuje na spojité
proměnné, tedy ani na GBS se stlačeným světlem. Piquasso je tak aktivně vyvíjený nástroj, který umí přesně tu
fyziku, na které stojí tato aplikace – a jak ukazuje kapitola o ověření, počítá stejně.
""",
    further_reading=(
        Reading(PIQUASSO_PAPER, "architektura, simulátory a srovnání s ostatními knihovnami"),
        Reading(PIQUASSO_REPOSITORY),
        Reading(PIQUASSO_PYPI),
        Reading(PIQUASSO_BOOST),
        Reading(MORSE_DATA_FLOW, "boson sampling na FPGA ze stejné skupiny"),
        Reading(KAPOSI_TORONTONIAN, "rekurzivní výpočet torontiánu pro prahové detektory"),
        Reading(STRAWBERRY_FIELDS_ARCHIVED),
        Reading(PERCEVAL),
    ),
)

PROGRAM_TOPIC = TheoryTopic(
    anchor="piquasso-program",
    title="Fotonický obvod jako program",
    in_short=(
        "Program je posloupnost instrukcí přiřazených módům zápisem `pq.Q(módy) | instrukce`. Simulátor dostane počet "
        "módů a konfiguraci, program provede a vrátí výsledný stav, případně vzorky z měření."
    ),
    explanation=r"""
Takhle vypadá v Piquassu úloha 2 ze stránky Výhoda GBS, „Společný extrém dvou aktiv“: dva módy, dva stlačovače
a interferometr. Hodnoty $r_j$ a matici $O$ spočítá aplikace z rozkladu

$$
B = D \Sigma D = O \operatorname{diag}(\tanh r) \, O^\top.
$$

```python
import numpy as np
import piquasso as pq

squeezing = [0.3353, 2.0912]   # r_j: stlačení obou módů
O = np.array(...)              # ortogonální matice interferometru z aplikace

with pq.Program() as program:
    for mode, r in enumerate(squeezing):
        pq.Q(mode) | pq.Squeezing(r)          # stlačovač: stlačené vakuum v módu
    pq.Q(0, 1) | pq.Interferometer(O)         # síť děličů svazku a fázových posunů
    pq.Q(0, 1) | pq.ParticleNumberMeasurement()  # detektory počtu fotonů

config = pq.Config(measurement_cutoff=40, seed_sequence=42)
simulator = pq.GaussianSimulator(d=2, config=config)
result = simulator.execute(program, shots=20000)
print(result.samples[:5])    # vzory, například (0, 2), (3, 1), …
```

Řádek po řádku: `pq.Q(0, 1)` vybere módy, na které instrukce působí, a svislítko ji na ně „pošle“.
`Squeezing(r)` je stlačovač, zdroj párů fotonů; `Interferometer(O)` je lineární optická síť, která fotony
přerozdělí mezi módy (jakoukoli unitární matici jde složit z děličů svazku a fázových posunů); a
`ParticleNumberMeasurement` jsou detektory, které rozliší počet fotonů. Simulátor dostane počet módů `d`
a konfiguraci – semínko náhody a ořezy (o nich kapitola o pastech).

Instrukce jsou ve čtyřech skupinách:

- **přípravy** stavu: `Vacuum`, `NumberState` (Fockův stav, třeba jeden foton v každém módu), `Thermal`, …;
- **brány**: gaussovské (`Squeezing`, `Displacement`, `Beamsplitter`, `Phaseshifter`, `Interferometer`)
  i negaussovské (`Kerr`, `CubicPhase`), které umí jen Fockovy simulátory;
- **měření**: počet fotonů, prahové detektory (`ThresholdMeasurement`, jen „klikl / neklikl“) a homodynní
  měření kvadratury;
- **kanály** se ztrátami: `Loss`, `Attenuator`, `LossyInterferometer`.

Pravděpodobnost jednoho vzoru jde spočítat i přímo, bez vzorkování: z programu bez měření vezme simulátor stav
a `state.get_particle_detection_probability(occupation_number=(8, 8))` vrátí $p(n)$. Přesně to používá kapitola
o ověření. Program jde načíst i z jazyka Blackbird, ve kterém Xanadu psala obvody pro své fotonické čipy
(`program.load_blackbird("obvod.xbb")`) – Blackbird je pro fotoniku zhruba tím, čím je OpenQASM pro qubity.
""",
    further_reading=(
        Reading(PIQUASSO_DOCUMENTATION, "seznam všech instrukcí s parametry"),
        Reading(KRUSE, "proč jsou pravděpodobnosti GBS hafniány"),
        Reading(BLACKBIRD),
    ),
)

SIMULATORS_TOPIC = TheoryTopic(
    anchor="piquasso-simulatory",
    title="Čtyři simulátory: kdy který",
    in_short=(
        "GaussianSimulator drží jen střední hodnoty a kovarianční matici, a proto zvládne GBS s mnoha fotony. Fockovy "
        "simulátory drží amplitudu každého rozložení fotonů do zvoleného ořezu a umí i negaussovské brány; "
        "PassiveSimulator počítá boson sampling s jednotlivými fotony."
    ),
    explanation=r"""
Přehled je v tabulce na konci kapitoly.

**Proč pro GBS gaussovský simulátor.** Stlačené světlo po průchodu interferometrem zůstává *gaussovský stav*:
celý ho popíše $2d$ středních hodnot a kovarianční matice $2d \times 2d$, ať v módech letí kolik chce fotonů.
Fockův simulátor naopak potřebuje amplitudu pro každé rozložení fotonů. Piquasso používá *globální* ořez $c$
(celkem nejvýš $c - 1$ fotonů), takže amplitud je

$$
\binom{c - 1 + d}{d}.
$$

Pro úlohu aplikace s nejvíc módy, úlohu 5 se vzorem $(4, 4, 4, 4)$, tedy 16 fotony ve 4 módech, je to při
$c = 17$ celkem 4 845 amplitud; matice hustoty má 4 845² ≈ 23,5 milionu čísel. Gaussovský simulátor si vystačí
s maticí 8 × 8. Exponenciální cena se mu ale nevyhne – jen se přesune do výpočtu hafniánu, jehož velikost roste
s počtem fotonů ve vzoru.

**Kdy Fockův simulátor.** Když obvod obsahuje negaussovskou bránu (Kerrův jev, kubická fáze), když se fotony
přidávají nebo odečítají, nebo když chceme derivace celé amplitudy podle parametrů – například u fotonických
neuronových sítí se spojitými proměnnými, na kterých článek o Piquassu porovnává rychlost se Strawberry Fields.

**PassiveSimulator** (do verze 7 `SamplingSimulator`) je určený pro boson sampling: vstupem jsou jednotlivé
fotony, obvod tvoří jen děliče svazku, fázové posuny a ztráty a pravděpodobnosti jsou permanenty. To je úloha
hardwaru Quandely; pro GBS se stlačeným světlem se nehodí.
""",
    further_reading=(
        Reading(PIQUASSO_DOCUMENTATION),
        Reading(PIQUASSO_PAPER, "srovnání globálního a lokálního ořezu se Strawberry Fields"),
    ),
)

VERIFICATION_TOPIC = TheoryTopic(
    anchor="piquasso-overeni",
    title="Ověření: Piquasso počítá stejně jako tato aplikace",
    in_short=(
        "Na všech pěti úlohách stránky Výhoda GBS dává Piquasso stejnou pravděpodobnost cílového vzoru jako náš "
        "vzorec s hafniánem: relativní rozdíl je nejvýš 6 · 10⁻¹¹, tedy jen zaokrouhlení. Ze vzorků Piquassa jde "
        "moment odhadnout i metodou GBS-P."
    ),
    explanation=r"""
**Co jsme porovnali.** Aplikace pro každou úlohu naladí přístroj: z kovarianční matice $\Sigma$ a vah $D$ spočítá
stlačení $r_j$ a interferometr $O$ (rozklad z předchozí kapitoly). Pravděpodobnost cílového vzoru $n$ pak počítá
vzorcem

$$
p(n) = \frac{\operatorname{Haf}(B_n)^2}{n! \, \prod_j \cosh r_j},
$$

kde hafnián dodá Steinova rekurze (viz Teorie). Do Piquassa jsme vložili stejné $r_j$ a $O$ a pravděpodobnost
téhož vzoru vzali z `GaussianSimulator`. Piquasso ji počítá z kovarianční matice stavu vlastním kódem (hafnián
v C++), ne naší rekurzí. Shoda tedy nezávisle potvrzuje celý řetězec – naladění přístroje, vzorec i rekurzi.
Tabulka níže ukazuje, že se obě čísla liší jen v posledních platných číslicích.

**Vzorkování.** Úlohu 2 (vzor $(8, 8)$, $p(n) \approx 0{,}004$) jsme v Piquassu spustili
na 20 000 výstřelů. Očekávaně by vzor měl padnout asi 80,5krát; padl 70krát a odhad GBS-P z této četnosti dal
moment 162 631 proti přesným 174 352,5, tedy o 6,7 % méně. Statistická chyba takového odhadu je asi 5,6 %
(odhad je úměrný odmocnině četnosti, viz Teorie), takže odchylka je v mezích náhody. Druhá tabulka ukazuje, co
se stane, když se měřicí ořez nechá na výchozí hodnotě – o tom další kapitola.
""",
    further_reading=(
        Reading(PIQUASSO_REPOSITORY, "kde přesně GaussianSimulator počítá pravděpodobnost vzoru"),
    ),
)

PITFALLS_TOPIC = TheoryTopic(
    anchor="piquasso-pasti",
    title="Pasti, na které jsme narazili",
    in_short=(
        "Výchozí měřicí ořez pustí do vzorku nejvýš 4 fotony v módu a nijak nevaruje: náš cílový vzor (8, 8) za "
        "20 000 výstřelů nepadl ani jednou. Ořez je potřeba nastavit nad počet fotonů v cílovém vzoru, ale ne "
        "libovolně vysoko – se 160 Piquasso 8.0.2 skončí chybou."
    ),
    explanation=r"""
**Měřicí ořez.** `pq.Config(measurement_cutoff=…)` omezuje, kolik fotonů smí mít *jeden mód* ve vzorku
z `GaussianSimulator`; výchozí hodnota 5 znamená nejvýš 4. Piquasso přitom nevaruje – vzorky prostě nikdy
nepřekročí 4 fotony v módu. Pro GBS se silným stlačením je to zásadní: v úloze 2 je jeden mód
stlačený na $r \approx 2{,}09$ a střední počet fotonů na výstřel je $\sum_j \sinh^2 r_j = 16$. S výchozím ořezem
cílový vzor $(8, 8)$ nepadl ani jednou a odhad momentu vyšel nulový.

Pro odhad GBS-P stačí ořez nad počtem fotonů v cílovém vzoru: s ořezem 40 i 80 padl vzor stejně 70krát (stejné
semínko náhody). Jiné statistiky ale ořez zkresluje i výš: průměrný počet fotonů na výstřel vyšel 2,86, 14,20
a 15,16 proti teoretickým 16 – silně stlačený mód má dlouhý chvost a ořez ho usekne. Zvyšovat ořez ale nejde
donekonečna: s hodnotou 160 skončí Piquasso 8.0.2 chybou `ValueError: Probabilities contain NaN`. Příčinu jsme
nezkoumali; náš odhad je přetečení čísel v plovoucí čárce u velkých počtů fotonů.

**Ořez Fockových simulátorů.** `pq.Config(cutoff=…)` je globální, platí pro celkový počet fotonů. Když ho
Piquasso z programu neodvodí, použije 4, a to je pro GBS skoro vždy málo.

**Python 3.9.** Piquasso 8 potřebuje Python 3.10 až 3.14. Tato aplikace lokálně běží na Pythonu 3.9, proto
Piquasso není její závislost a skripty s ním běží ve zvláštním prostředí; čísla na této stránce jsou uložená.

**Přejmenování ve verzi 8.0.** `SamplingSimulator` je jen zastaralý alias pro `PassiveSimulator` a při použití
varuje; článek i starší návody používají staré jméno.

**Konvence $\hbar = 2$.** Piquasso má ve výchozím nastavení $\hbar = 2$, kovarianční matice v článcích
s $\hbar = 1$ nebo $\hbar = 1/2$ se proto liší násobkem. Pravděpodobnosti vzorů na volbě $\hbar$ nezávisí.

**Znaménka a cena.** Simulátor vrací pravděpodobnosti, tedy $|\operatorname{Haf}|^2$ – znaménkový problém ze
stránky Háčky platí i tady. A Piquasso je klasická simulace: cena roste exponenciálně s počtem fotonů, takže je
to nástroj na ověření a ladění, ne náhrada fotonického čipu.
""",
    further_reading=(
        Reading(PIQUASSO_DOCUMENTATION, "popis třídy Config: cutoff, measurement_cutoff, hbar"),
        Reading(PIQUASSO_REPOSITORY, "CHANGELOG.md: přejmenování ve verzi 8.0.0"),
    ),
)

QUBITS_TOPIC = TheoryTopic(
    anchor="piquasso-qubity",
    title="Qubity a fotony: překlad oběma směry a VLQ",
    in_short=(
        "Z qubitů na fotony: Piquasso převede obvod z Qiskitu na fotonický, každá dvouqubitová brána ale v lineární "
        "optice uspěje jen s pravděpodobností 2/27. Z fotonů na qubity: GBS jde emulovat na qubitech a zapsat "
        "v OpenQASM, po překladu do nativních bran IQM ale vyjdou desítky tisíc až statisíce bran CZ – na "
        "počítači VLQ by z toho byl šum."
    ),
    explanation=r"""
**Z qubitů na fotony.** Funkce `dual_rail_encode_from_qiskit` vezme obvod `QuantumCircuit` z Qiskitu a každý
qubit zakóduje do jednoho fotonu ve dvou módech: $|0\rangle = |1, 0\rangle$ a $|1\rangle = |0, 1\rangle$
(*dual-rail*). Jednoqubitové brány jsou pak děliče svazku a fázové posuny, tedy deterministické. Dvouqubitovou
bránu CZ (a z ní CNOT) ale lineární optika bez měření neumí: Piquasso použije Knillovu bránu se dvěma pomocnými
fotony a *postselekcí* – výsledek platí, jen když v pomocných módech změříme po jednom fotonu. Změřili jsme to na
Bellově obvodu (Hadamard a CNOT): uspěje s pravděpodobností 0,0741, tedy 2/27. Obvod s deseti dvouqubitovými
branami tak uspěje asi s pravděpodobností 5 · 10⁻¹². Proto fotonické qubitové počítače potřebují složitější
schémata s pomocnými stavy a měřením, jak je navrhli Knill, Laflamme a Milburn.

**Z fotonů na qubity: GBS na VLQ.** Opačný směr dělá export do Qiskitu na stránce Výhoda GBS. Každý mód
zakóduje do $q$ qubitů (počet fotonů jako binární číslo, ořez $2^q$ hladin), stlačené vakuum připraví jako stav
a každý dělič svazku jako unitární matici na $2q$ qubitech. Qiskit takový obvod umí zapsat v OpenQASM 3,
a protože VLQ – supravodivý počítač IQM s 24 qubity v IT4Innovations v Ostravě – přijímá obvody z Qiskitu,
technicky ho tam poslat jde: našich pět úloh potřebuje 8 až 20 qubitů. Úskalí jsme změřili překladem obvodu do
nativních bran IQM (tabulka):

1. **Počet bran.** Obecná unitární matice na $n$ qubitech potřebuje řádově $4^n$ dvouqubitových bran; dolní
   mez je $(4^n - 3n - 1)/4$ (Shende, Bullock, Markov). U úlohy 1 je to 16 812 bran CZ, u úlohy 2 s jedním
   děličem svazku na 10 qubitech 479 535. Chytřejší kompilace pomůže jen zčásti: připravit stav módu přes
   `StatePreparation` stojí u úlohy 1 jen 120 bran CZ, dělič svazku jsme jinak nerozkládali.
2. **Hvězdicová topologie.** Qubity VLQ jsou propojené přes centrální rezonátor. Brána mezi dvěma qubity je
   proto ve skutečnosti trojice MOVE, CZ, MOVE: stav jednoho qubitu se přesune do rezonátoru a zpět. Stav jde
   přesunout jen do prázdného rezonátoru, takže dvouqubitové brány nejspíš běží po jedné – to je náš závěr
   z dokumentace IQM.
3. **Šum.** Náš hrubý odhad: při věrnosti 99 % na operaci projde úloha 1 se třemi operacemi na každou bránu CZ
   bez jediné chyby s pravděpodobností asi 10⁻²²⁰. Výsledek by byl čistý šum.
4. **Žádná výhoda.** Emulace bosonů na qubitech je dražší než klasická simulace: Piquasso spočítá
   pravděpodobnost vzoru kterékoli z našich úloh za 1–2 ms (první volání trvá asi 2 s, kód se teprve překládá).

**IT4I a projekt GBS4EO.** Stránka Fotonika ve světě cituje abstrakt semináře, podle kterého IT4I převádí GBS
na hradlový program pro VLQ (hledání hustých podgrafů). Jak přesně, nevíme. Pro hledání podgrafů stačí vědět,
jestli detektor klikl; s ořezem na 0 nebo 1 foton by stačil jeden qubit na mód a obvod by byl o řády menší.
To je ale přibližná úloha jiného druhu než náš odhad momentu, který potřebuje přesný počet fotonů – náš odhad,
ověřit přímo v IT4I.
""",
    further_reading=(
        Reading(PIQUASSO_DUAL_RAIL),
        Reading(KNILL_POSTSELECTION, "brána CZ s pravděpodobností úspěchu 2/27"),
        Reading(KLM),
        Reading(SHENDE_SYNTHESIS, "rozklad obecné unitární matice a dolní mez počtu bran"),
        Reading(IQM_STAR_TRANSPILE),
        Reading(VLQ_STAR_TOPOLOGY),
        Reading(VLQ_INAUGURATION),
        Reading(QISKIT_DOCUMENTATION, "transpilace a zápis do OpenQASM 3"),
    ),
)

@dataclass(frozen=True)
class SimulatorRow:
    name: str
    memory: str
    extras: str
    use: str


SIMULATOR_ROWS: Tuple[SimulatorRow, ...] = (
    SimulatorRow(
        "GaussianSimulator", "střední hodnoty a kovarianční matici 2d × 2d",
        "ztráty, měření počtu fotonů, prahové i homodynní", "GBS: pravděpodobnost vzoru přes hafnián, vzorkování",
    ),
    SimulatorRow(
        "PureFockSimulator", "stavový vektor ve Fockově bázi do ořezu",
        "negaussovské brány, derivace přes TensorFlow a JAX", "malé obvody s několika fotony",
    ),
    SimulatorRow(
        "FockSimulator", "matici hustoty, tedy druhou mocninu stavového vektoru", "smíšené stavy a šum",
        "malé obvody se ztrátami",
    ),
    SimulatorRow(
        "PassiveSimulator", "obsazení vstupních módů a matici interferometru", "jen pasivní lineární optika a ztráty",
        "boson sampling s jednotlivými fotony (permanenty)",
    ),
)
"""The table of the chapter on simulators; words wrap in it, so it is not part of the Markdown."""

TOPICS: Tuple[TheoryTopic, ...] = (
    ABOUT_TOPIC, PROGRAM_TOPIC, SIMULATORS_TOPIC, VERIFICATION_TOPIC, PITFALLS_TOPIC, QUBITS_TOPIC,
)

KEY_FINDINGS: Tuple[KeyFinding, ...] = (
    KeyFinding(
        "**Piquasso** je aktivně vyvíjený open-source simulátor fotonických kvantových počítačů z Budapešti "
        "(Python a C++, licence Apache 2.0, článek v Quantum 2025); umí GBS i boson sampling.",
        ABOUT_TOPIC.anchor,
    ),
    KeyFinding(
        "Pro GBS je správná volba **GaussianSimulator**: drží jen kovarianční matici, Fockovy simulátory by pro "
        "16 fotonů ve 4 módech potřebovaly 4 845 amplitud.",
        SIMULATORS_TOPIC.anchor,
    ),
    KeyFinding(
        "**Ověření:** pravděpodobnosti vzorů z Piquassa se s naším vzorcem přes hafnián shodují na všech pěti "
        "úlohách aplikace až na zaokrouhlení.",
        VERIFICATION_TOPIC.anchor,
    ),
    KeyFinding(
        "**Pozor na `measurement_cutoff`:** výchozí hodnota 5 tiše uřízne každý mód na 4 fotony a cílový vzor "
        "(8, 8) pak nepadne nikdy.",
        PITFALLS_TOPIC.anchor,
    ),
    KeyFinding(
        "**GBS na qubitovém VLQ** technicky jde (emulace a OpenQASM), ale po překladu jsou to desítky tisíc až "
        "statisíce bran CZ a výsledek by byl šum.",
        QUBITS_TOPIC.anchor,
    ),
)

RELATED_LINKS = (
    ("Výhoda GBS: pět úloh a export do Qiskitu", ADVANTAGE_PATH),
    ("Průvodce: kapitola o skriptu pro Qiskit", GUIDE_PATH),
    ("Háčky: znaménkový problém", f"{CAVEATS_PATH}#znamenko"),
    ("Fotonika ve světě: kdo staví hardware", PHOTONICS_LANDSCAPE_PATH),
)
