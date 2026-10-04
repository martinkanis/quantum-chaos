"""Texts of the theory page; each step of the GBS page links to the matching topic here."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Tuple

from ui.caveats_content import (
    CLASSICAL_SIMULATION,
    CLOSED_FORM,
    DISCARDED_SHOTS,
    SAMPLES_NOT_TIME,
    SIGN_PROBLEM,
    Caveat,
)


SOURCES_ANCHOR = "zdroje"


@dataclass(frozen=True)
class Source:
    citation: str
    """Markdown without the final full stop: authors, *title*, where and when published, optional link."""
    czech: bool = False


@dataclass(frozen=True)
class Reading:
    source: Source
    note: str = ""
    """What the source adds to the topic that cites it."""


@dataclass(frozen=True)
class TheoryTopic:
    anchor: str
    title: str
    in_short: str
    explanation: str
    further_reading: Tuple[Reading, ...]
    related_caveats: Tuple[Caveat, ...] = ()


DRIMAL_MONTE_CARLO = Source(
    "Dřímal, J., Trunec, D., Brablec, A.: *Úvod do metody Monte Carlo*. Přírodovědecká fakulta MU, Brno 2006, "
    "[PDF](https://www.physics.muni.cz/~trunec/mc.pdf)",
    czech=True,
)
DVORAKOVA_MONTE_CARLO = Source(
    "Dvořáková, Ľ.: *Vyzkoušejte metodu Monte Carlo*. Rozhledy matematicko-fyzikální 94 (2019), č. 2, s. 1–11, "
    "[DML-CZ](https://dml.cz/dmlcz/147998)",
    czech=True,
)
FABIAN_KLUIBER = Source(
    "Fabian, F., Kluiber, Z.: *Metoda Monte Carlo a možnosti jejího uplatnění*. Prospektrum, Praha 1998, "
    "[WorldCat](https://search.worldcat.org/cs/title/metoda-monte-carlo-a-moznosti-jejiho-uplatneni/oclc/40790269)",
    czech=True,
)
ANDEL_STATISTICS = Source(
    "Anděl, J.: *Základy matematické statistiky*. Matfyzpress, Praha 2005 (3. vyd. 2011), "
    "[nakladatel](https://matfyzpress.cz/cz/e-shop/vsechny-tituly/zaklady-matematicke-statistiky-9788073781620)",
    czech=True,
)
WIKIPEDIA_MONTE_CARLO = Source(
    "Wikipedie: [Metoda Monte Carlo](https://cs.wikipedia.org/wiki/Metoda_Monte_Carlo), "
    "[Zákon velkých čísel](https://cs.wikipedia.org/wiki/Z%C3%A1kon_velk%C3%BDch_%C4%8D%C3%ADsel), "
    "[Centrální limitní věta](https://cs.wikipedia.org/wiki/Centr%C3%A1ln%C3%AD_limitn%C3%AD_v%C4%9Bta)",
    czech=True,
)
WIKIPEDIA_COVARIANCE = Source(
    "Wikipedie: [Kovarianční matice](https://cs.wikipedia.org/wiki/Kovarian%C4%8Dn%C3%AD_matice)",
    czech=True,
)
WIKIPEDIA_PRINCIPAL_COMPONENTS = Source(
    "Wikipedie: [Analýza hlavních komponent](https://cs.wikipedia.org/wiki/Anal%C3%BDza_hlavn%C3%ADch_komponent)",
    czech=True,
)
SALEH_TEICH = Source(
    "Saleh, B. E. A., Teich, M. C.: *Základy fotoniky* (4 svazky). Matfyzpress, Praha 1994–1996 – český překlad "
    "učebnice *Fundamentals of Photonics*",
    czech=True,
)
METROPOLIS_ULAM = Source(
    "Metropolis, N., Ulam, S.: *The Monte Carlo Method*. Journal of the American Statistical Association 44 "
    "(1949), 335–341"
)
GLASSERMAN = Source("Glasserman, P.: *Monte Carlo Methods in Financial Engineering*. Springer, New York 2004")
MARKOWITZ = Source("Markowitz, H.: *Portfolio Selection*. The Journal of Finance 7 (1952), 77–91")
ISSERLIS = Source(
    "Isserlis, L.: *On a formula for the product-moment coefficient of any order of a normal frequency "
    "distribution in any number of variables*. Biometrika 12 (1918), 134–139, "
    "[doi:10.1093/biomet/12.1-2.134](https://doi.org/10.1093/biomet/12.1-2.134)"
)
WICK = Source(
    "Wick, G. C.: *The Evaluation of the Collision Matrix*. Physical Review 80 (1950), 268–272, "
    "[doi:10.1103/PhysRev.80.268](https://doi.org/10.1103/PhysRev.80.268)"
)
WIKIPEDIA_HAFNIAN = Source(
    "Wikipedia (anglicky): [Isserlis' theorem](https://en.wikipedia.org/wiki/Isserlis%27s_theorem), "
    "[Hafnian](https://en.wikipedia.org/wiki/Hafnian)"
)
WALRUS_HAFNIAN = Source(
    "[The hafnian](https://the-walrus.readthedocs.io/en/latest/hafnian.html) – dokumentace knihovny The Walrus"
)
BARVINOK = Source("Barvinok, A.: *Combinatorics and Complexity of Partition Functions*. Springer 2016")
VALIANT = Source(
    "Valiant, L. G.: *The complexity of computing the permanent*. Theoretical Computer Science 8 (1979), 189–201"
)
BJORKLUND_GUPT_QUESADA = Source(
    "Björklund, A., Gupt, B., Quesada, N.: *A faster hafnian formula for complex matrices and its benchmarking on "
    "a supercomputer*. ACM Journal of Experimental Algorithmics (2019)"
)
HAMILTON = Source(
    "Hamilton, C. S., Kruse, R., Sansoni, L., Barkhofen, S., Silberhorn, C., Jex, I.: *Gaussian Boson Sampling*. "
    "Physical Review Letters 119, 170501 (2017), "
    "[doi:10.1103/PhysRevLett.119.170501](https://doi.org/10.1103/PhysRevLett.119.170501)"
)
KRUSE = Source(
    "Kruse, R., Hamilton, C. S., Sansoni, L., Barkhofen, S., Silberhorn, C., Jex, I.: *Detailed study of "
    "Gaussian boson sampling*. Physical Review A 100, 032326 (2019), "
    "[doi:10.1103/PhysRevA.100.032326](https://doi.org/10.1103/PhysRevA.100.032326)"
)
AARONSON_ARKHIPOV = Source(
    "Aaronson, S., Arkhipov, A.: *The computational complexity of linear optics*. Theory of Computing 9 (2013), "
    "143–252"
)
GERRY_KNIGHT = Source("Gerry, C. C., Knight, P. L.: *Introductory Quantum Optics*. Cambridge University Press 2005")
RECK = Source(
    "Reck, M., Zeilinger, A., Bernstein, H. J., Bertani, P.: *Experimental realization of any discrete unitary "
    "operator*. Physical Review Letters 73, 58 (1994)"
)
CLEMENTS = Source(
    "Clements, W. R. a kol.: *Optimal design for universal multiport interferometers*. Optica 3, 1460 (2016)"
)
ZHONG = Source("Zhong, H.-S. a kol.: *Quantum computational advantage using photons*. Science 370, 1460 (2020)")
MADSEN = Source(
    "Madsen, L. S. a kol.: *Quantum computational advantage with a programmable photonic processor*. "
    "Nature 606, 75 (2022)"
)
BRADLER = Source(
    "Brádler, K., Dallaire-Demers, P.-L., Rebentrost, P., Su, D., Weedbrook, C.: *Gaussian boson sampling for "
    "perfect matchings of arbitrary graphs*. Physical Review A 98, 032310 (2018)"
)
ARRAZOLA_BROMLEY = Source(
    "Arrazola, J. M., Bromley, T. R.: *Using Gaussian Boson Sampling to Find Dense Subgraphs*. Physical Review "
    "Letters 121, 030503 (2018)"
)
QUESADA_THRESHOLD_DETECTORS = Source(
    "Quesada, N., Arrazola, J. M., Killoran, N.: *Gaussian boson sampling using threshold detectors*. Physical "
    "Review A 98, 062322 (2018)"
)
ANDERSEN_SHAN_EXPECTATIONS = Source(
    "Andersen, Shan: *Using Gaussian Boson Samplers to Approximate Gaussian Expectation Problems*, "
    "[arXiv:2502.19336](https://arxiv.org/abs/2502.19336) (2025)"
)
ANDERSEN_SHAN_ADVANTAGE = Source(
    "Andersen, Shan: *Estimating the Percentage of GBS Advantage in Gaussian Expectation Problems*, "
    "[arXiv:2502.19362](https://arxiv.org/abs/2502.19362) (2025)"
)
ARRAZOLA_REBENTROST_WEEDBROOK = Source(
    "Arrazola, Rebentrost, Weedbrook: *Quantum supremacy and high-dimensional integration*, arXiv (2017)"
)


DAMODARAN_RETURNS = Source(
    "Damodaran, A.: *Historical Returns on Stocks, Bonds and Bills: 1928–2023*. NYU Stern, leden 2024, "
    "[data](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histret.html)"
)
WIKIPEDIA_CORRELATION = Source("Wikipedie: [Korelace](https://cs.wikipedia.org/wiki/Korelace)", czech=True)
DANISH_QUANTUM_USE_CASES = Source(
    "*16 Danish Quantum Use Cases*, prosinec 2024, případ 16 Quantum-Optimised Real-Time Trading (Jyske Bank, "
    "Qpurpose), [PDF](https://dqc.dk/wp-content/uploads/2024/12/16-Danish-Quantum-Use-Cases-December-2024.pdf)"
)
SDU_QUANTUM_FINANCE = Source(
    "Centre for Quantum Mathematics, SDU: [Quantum Mathematics for Finance: QM, Jyske Bank and Qpurpose]"
    "(https://www.sdu.dk/en/forskning/qm/quantum-computing/quantum-in-finance)"
)
OH_CLASSICAL_SIMULATION = Source(
    "Oh, C., Liu, M., Alexeev, Y., Fefferman, B., Jiang, L.: *Classical algorithm for simulating experimental "
    "Gaussian boson sampling*. Nature Physics 20, 1461 (2024), "
    "[článek](https://www.nature.com/articles/s41567-024-02535-8)"
)


MONTE_CARLO = TheoryTopic(
    anchor="monte-carlo",
    title="Klasické Monte Carlo: střední hodnota jako průměr přes náhodné scénáře",
    in_short=(
        "Střední hodnotu náhodné veličiny odhadneme tak, že náhodu nasimulujeme: vylosujeme mnoho nezávislých "
        "scénářů, pro každý spočítáme výsledek a výsledky zprůměrujeme. Podle zákona velkých čísel se průměr "
        r"blíží skutečné hodnotě a jeho chyba klesá jako $1/\sqrt{N}$."
    ),
    explanation=r"""
**Střední hodnota.** Česká statistická literatura mluví o *střední hodnotě* (značí se $\mathrm{E}X$),
ekonomické texty často o *očekávané hodnotě* – jde o totéž. Je to průměr všech možných výsledků vážený jejich
pravděpodobnostmi. Pro náhodný vektor $X$ s hustotou $\varphi$ a funkci $f$ je to integrál

$$
\mathbb{E}[f(X)] = \int f(x)\,\varphi(x)\,\mathrm{d}x .
$$

U portfolia s $k$ aktivy je $x$ vektor $k$ ročních výnosů a integrál je $k$-rozměrný. Pro jednoduchá $f$
vede na vzorec, obecně ho ale přesně spočítat neumíme.

**Metoda Monte Carlo.** Skripta Masarykovy univerzity ji definují jako numerickou metodu, která úlohu řeší
modelováním náhodných veličin a statistickým odhadem jejich charakteristik. Hledané číslo se vyjádří jako
střední hodnota vhodné náhodné veličiny a ta se odhadne aritmetickým průměrem jejích nezávislých realizací:

1. vygenerujeme $N$ nezávislých scénářů $X^{(1)}, \dots, X^{(N)}$ se stejným rozdělením jako $X$
   (tzv. náhodný výběr),
2. pro každý spočítáme $f\big(X^{(i)}\big)$,
3. výsledky zprůměrujeme:

$$
\hat\mu_N = \frac{1}{N}\sum_{i=1}^{N} f\big(X^{(i)}\big) \approx \mathbb{E}[f(X)] .
$$

**Co je scénář.** Scénář je jedna vylosovaná realizace $X^{(i)}$ – u nás jeden smyšlený, ale věrohodný rok:
odchylky ročních výnosů všech aktiv od očekávání najednou. Třeba akcie o 12 % líp, než se čekalo, dluhopisy
o 1 % hůř a zlato o 20 % líp. Z něj vyjde odchylka portfolia

$$
L = 0{,}6\cdot 12\,\% + 0{,}3\cdot(-1\,\%) + 0{,}1\cdot 20\,\% = 8{,}9\,\%
$$

a hodnota, která se průměruje, $f(X) = L^4 \approx 0{,}000063$. Počítač scénáře losuje tak, aby každé
aktivum kolísalo se svou volatilitou a aktiva se hýbala spolu podle korelací – většinou tedy vyjde obyčejný
rok, jen občas extrémní. Na 1. stránce je scénářem celá jedna možná budoucnost portfolia měsíc po měsíci
přes celý horizont; u GBS hraje roli scénáře výstřel.

**Proč to funguje.**

- *Nestrannost:* $\mathbb{E}[\hat\mu_N] = \mathbb{E}[f(X)]$ – odhad se v průměru nemýlí.
- *Zákon velkých čísel:* s rostoucím $N$ se výběrový průměr blíží střední hodnotě (podle silného zákona
  velkých čísel skoro jistě).
- *Centrální limitní věta:* pro velké $N$ má $\hat\mu_N$ přibližně normální rozdělení se směrodatnou
  odchylkou $\sigma_f/\sqrt{N}$, kde $\sigma_f^2 = \operatorname{var} f(X)$ je rozptyl výsledku jednoho
  scénáře (starší česká literatura říká *disperze* a značí ji $D(X)$). Z toho plyne 95% interval
  spolehlivosti $\hat\mu_N \pm 1{,}96\,\hat\sigma_f/\sqrt{N}$.
- I bez předpokladu normality dává odhad chyby Čebyševova nerovnost: s pravděpodobností aspoň $1-\alpha$ se
  průměr od střední hodnoty neliší o víc než $\sqrt{D(X)/(N\alpha)}$. Chyba tedy vždy klesá jako $1/\sqrt{N}$.

**Rozptyl scénáře polopatě.** Jeden konkrétní scénář je jedno číslo a sám rozptyl nemá. Než ho ale
vylosujeme, je jeho výsledek náhodný – a rozptyl říká, jak moc se výsledky jednotlivých scénářů mezi sebou
liší; $\sigma_f$ je typická odchylka jednoho scénáře od průměru. Příklad mimo finance: průměrnou výšku lidí
odhadneš z pár stovek náhodně změřených lidí, protože výšky se liší jen o desítky centimetrů. Průměrný příjem
ne – jeden miliardář ve vzorku průměr rozhodí, rozptyl jednoho „scénáře“ je obrovský a vzorků je potřeba
mnohem víc. U $L^4$ je to podobné: obyčejný rok s odchylkou 5 % dá $0{,}05^4 \approx 0{,}000006$, vzácný rok
s odchylkou 30 % dá $0{,}3^4 \approx 0{,}008$, asi 1 300× víc. Typická odchylka jednoho scénáře od průměru je
proto zhruba 3,3× větší než průměr sám; jeden scénář skoro nic neřekne a teprve 100 000 scénářů stáhne chybu
průměru asi na 1 %. Nejde přitom o rozptyl výnosu portfolia ($\sigma_p^2$, čtverec volatility), ale
o kolísání toho, co se v Monte Carlu průměruje.

**Pravidlo odmocniny.** Desetkrát přesnější výsledek stojí stokrát víc scénářů. Výhodou je, že rychlost
$1/\sqrt{N}$ nezávisí na počtu proměnných: mřížka s 10 body na osu by pro 6 aktiv potřebovala milion bodů
a pro 20 aktiv $10^{20}$, kdežto Monte Carlu stačí pořád zhruba stejný počet scénářů. Proto se tolik
používá ve financích – pro ceny derivátů, pro VaR i pro simulaci portfolia na 1. stránce. Zmenšit se dá
konstanta $\sigma_f$: k tomu slouží *metody snižování rozptylu (disperze)*, třeba *metoda váženého výběru*
(importance sampling). Vrátíme se k ní u srovnání s GBS, protože GBS estimátor se chová velmi podobně.

**Na naší úloze.** Pro $\mathbb{E}[L^d]$ klasické Monte Carlo v každém scénáři

1. vylosuje nezávislé normované normální veličiny $Z \sim \mathcal{N}(0, I)$ a převede je na korelované
   výnosy $X = AZ$, kde $AA^\top = \Sigma$ (třeba Choleského rozklad),
2. spočítá odchylku výnosu portfolia $L = w^\top X$ a umocní ji na $d$,

a nakonec výsledky zprůměruje. Hodnota $L^d$ má ale *těžký chvost*: vzácné scénáře s velkým $|L|$ přispívají
do průměru nepoměrně hodně, takže $\sigma_f$ je velké – a pro $d = 6$ mnohem větší než pro $d = 2$
(viz srovnání s GBS).

**Náhoda z počítače: seed, referenční a kontrolní běhy.** Počítač losuje *pseudonáhodná čísla*:
deterministickou posloupnost, která vypadá náhodně. Její počáteční stav určuje *seed*: stejný seed a stejné
vstupy dají vždy přesně stejné scénáře, a tedy stejné výsledky. Volba „Náhodný“ bere pokaždé nový seed, takže
se výsledky mezi spuštěními mírně liší. *Referenční běh* (seed 42) je jeden pevně daný běh, na jehož čísla se
dá odkazovat a porovnávat je. *Kontrolní běhy* (seed 1, 2, 3) jsou tentýž výpočet s jinými, ale pevnými
seedy, tedy s jinými náhodnými scénáři. Když vyjdou skoro stejně, má simulace vzorků dost; když se výrazně
liší, je náhodná chyba velká a je potřeba zvýšit počet vzorků. Je to nejjednodušší způsob, jak chybu Monte
Carla uvidět bez teorie.

**Historie a název.** Myšlenka je stará: Buffonova úloha o jehle z 18. století odhaduje číslo $\pi$
z četnosti, s jakou náhodně hozená jehla protne rovnoběžku. Soustavně metodu rozvinuli S. Ulam,
J. von Neumann a N. Metropolis v Los Alamos ve 40. letech 20. století; název podle kasina v Monaku se
v odborném tisku poprvé objevil v článku Metropolise a Ulama z roku 1949.
""",
    further_reading=(
        Reading(
            DRIMAL_MONTE_CARLO,
            "kap. 1.4 princip a odhad chyby, kap. 5 výpočet integrálů a metody snižování disperze včetně metody "
            "váženého výběru",
        ),
        Reading(DVORAKOVA_MONTE_CARLO, "přístupný úvod se středoškolskou matematikou"),
        Reading(FABIAN_KLUIBER),
        Reading(ANDEL_STATISTICS, "zákon velkých čísel, centrální limitní věta, odhady"),
        Reading(WIKIPEDIA_MONTE_CARLO),
        Reading(METROPOLIS_ULAM),
        Reading(GLASSERMAN),
    ),
)

PORTFOLIO_MOMENT = TheoryTopic(
    anchor="moment-portfolia",
    title="Úloha: moment výnosu portfolia",
    in_short=(
        r"Počítáme průměr $d$-té mocniny odchylky výnosu portfolia od očekávání. Pro $d = 2$ je to rozptyl "
        "(čtverec volatility), vyšší sudé momenty zdůrazňují extrémní roky."
    ),
    explanation=r"""
**Výnosy očištěné o střední hodnotu.** Roční výnos aktiva $i$ označme $R_i$ a jeho očekávaný výnos
$\mu_i = \mathbb{E}R_i$. Úloha pracuje s odchylkou

$$
X_i = R_i - \mu_i ,
$$

tedy s „překvapením“, o kolik se konkrétní rok liší od očekávání. Odchylky mají střední hodnotu nula
a očekávané výnosy na ně nemají vliv – proto je na 2. stránce nezadáváš.

**Model: vícerozměrné normální rozdělení.** Vektor odchylek $X = (X_1, \dots, X_k)$ má rozdělení
$\mathcal{N}(0, \Sigma)$ s kovarianční maticí

$$
\Sigma_{ij} = \rho_{ij}\,\sigma_i\,\sigma_j ,
$$

kde $\sigma_i$ je volatilita aktiva $i$ (směrodatná odchylka ročního výnosu) a $\rho_{ij}$ korelace aktiv $i$
a $j$. Na diagonále jsou rozptyly $\Sigma_{ii} = \sigma_i^2$. Výchozí portfolio (akcie 16 %, dluhopisy 5 %,
zlato 15 %, všechny korelace 0,2) má

$$
\Sigma = \begin{pmatrix} 0{,}0256 & 0{,}0016 & 0{,}0048 \\ 0{,}0016 & 0{,}0025 & 0{,}0015 \\
0{,}0048 & 0{,}0015 & 0{,}0225 \end{pmatrix}.
$$

**Výnos portfolia.** S vahami $w = (w_1, \dots, w_k)$ – podíly, jejichž součet je 1 – se výnos portfolia
odchýlí od očekávání o

$$
L = w^\top X = w_1X_1 + w_2X_2 + \dots + w_kX_k .
$$

Pro výchozí váhy $w = (0{,}6;\ 0{,}3;\ 0{,}1)$ je $L = 0{,}6\,X_1 + 0{,}3\,X_2 + 0{,}1\,X_3$.

**Moment stupně $d$.** Hledáme $\mathbb{E}[L^d]$ – průměrnou $d$-tou mocninu odchylky:

- $d = 2$: $\mathbb{E}[L^2] = w^\top\Sigma w = \sigma_p^2$ je *rozptyl* portfolia a jeho odmocnina
  $\sigma_p$ volatilita. Pro výchozí portfolio je $\sigma_p^2 = 0{,}010908$, tedy $\sigma_p \approx 10{,}4\,\%$
  – méně než u samotných akcií, protože diverzifikace část výkyvů vyruší.
- $d = 4$: *čtvrtý moment*. Mocnina $L^4$ roste s velikostí odchylky tak rychle, že v průměru dominují vzácné
  velké výkyvy. Poměr $\mathbb{E}[L^4]/\sigma_p^4$ je *špičatost* (kurtosis), míra „tlustých chvostů“:
  normální rozdělení ji má rovnou 3, výnosy akcií (zvlášť denní) mívají vyšší.
- $d = 6$: šestý moment je na extrémní roky citlivý ještě víc.

**Proč jen sudé $d$.** Normální rozdělení s nulovou střední hodnotou je symetrické: odchylka $+x$ je stejně
pravděpodobná jako $-x$. Liché mocniny se proto v průměru vyruší a $\mathbb{E}[L^3] = \mathbb{E}[L^5] = 0$.
Ve Wickově větě to odpovídá tomu, že lichý počet činitelů nejde rozdělit do dvojic.

**Kontrolní vzorec.** Lineární kombinace normálních veličin je opět normální, takže
$L \sim \mathcal{N}(0, \sigma_p^2)$ a

$$
\mathbb{E}[L^d] = (d-1)!!\;\sigma_p^{d}, \qquad (d-1)!! = 1\cdot 3\cdot 5 \cdots (d-1),
$$

tedy $\mathbb{E}[L^2] = \sigma_p^2$, $\mathbb{E}[L^4] = 3\sigma_p^4$ a $\mathbb{E}[L^6] = 15\sigma_p^6$. Pro výchozí
portfolio je $\mathbb{E}[L^4] = 3\cdot 0{,}010908^2 \approx 3{,}57\cdot 10^{-4}$.

**Jak číslu rozumět.** Moment má jednotku „výnos na $d$-tou“, proto je názornější jeho $d$-tá odmocnina:
$(\mathbb{E}[L^4])^{1/4} \approx 13{,}7\,\%$ proti volatilitě 10,4 %. Čtvrtý moment tedy „vidí“ velké výkyvy
silněji než rozptyl.

**Proč zrovna tahle úloha.** $L^d$ je *polynom* v gaussovských proměnných – přesně ten typ funkce, pro který
platí Wickova věta a se kterým GBS umí pracovat. Kontrolní vzorec navíc umožní ověřit, že všechny další kroky
počítají správně.
""",
    further_reading=(
        Reading(ANDEL_STATISTICS, "vícerozměrné normální rozdělení a jeho momenty"),
        Reading(WIKIPEDIA_COVARIANCE),
        Reading(MARKOWITZ, r"rozptyl portfolia $w^\top\Sigma w$ jako míra rizika"),
    ),
    related_caveats=(CLOSED_FORM,),
)

CORRELATION = TheoryTopic(
    anchor="korelace",
    title="Korelace mezi aktivy: proč a jak funguje",
    in_short=(
        "Korelace (od −1 do +1) říká, jak moc se dvě aktiva hýbou spolu. Čím je nižší, tím víc se jejich výkyvy "
        "v portfoliu navzájem vyruší – to je podstata diverzifikace."
    ),
    explanation=r"""
**Co korelace je.** Číslo od −1 do +1, které říká, jak moc se výnosy dvou aktiv hýbou společně:

- **+1:** když má jedno aktivum dobrý rok, má ho i druhé,
- **0:** z pohybu jednoho nejde nic poznat o druhém,
- **−1:** když jedno roste, druhé klesá.

Počítá se jako společné kolísání (kovariance) vydělené kolísáním obou aktiv zvlášť; zpětně z ní a z volatilit
vzniká kovarianční matice:

$$
\rho_{ij} = \frac{\operatorname{cov}(R_i, R_j)}{\sigma_i\,\sigma_j}, \qquad
\Sigma_{ij} = \rho_{ij}\,\sigma_i\,\sigma_j .
$$

**Proč na ní záleží: diverzifikace.** Rozptyl portfolia je

$$
\sigma_p^2 = \sum_{i}\sum_{j} w_i\,w_j\,\rho_{ij}\,\sigma_i\,\sigma_j .
$$

Když se aktiva nehýbou úplně spolu, jejich výkyvy se částečně vyruší. Výchozí portfolio (akcie 60 %
s volatilitou 16 %, dluhopisy 30 % s 5 %, zlato 10 % s 15 %) má při stejných aktivech a jiné korelaci všech
párů volatilitu 12,6 % při korelaci 1, 10,4 % při výchozí 0,2, 9,8 % při 0 a 8,1 % při −0,5. Jen při
korelaci 1 je volatilita portfolia prostým váženým průměrem volatilit:

$$
0{,}6\cdot 16\,\% + 0{,}3\cdot 5\,\% + 0{,}1\cdot 15\,\% = 12{,}6\,\% .
$$

Čím nižší korelace, tím víc rizika se vyruší.

**Jak s korelací pracuje aplikace.**

- Posuvník nastaví stejnou korelaci všem párům, v matici jde upravit každý pár zvlášť (počítají se hodnoty
  nad diagonálou). Po změně aktiv nebo posuvníku se matice znovu vyplní jednotně.
- Simulace na 1. stránce: z volatilit a korelací vznikne kovarianční matice $\Sigma$. Každý měsíc generátor
  vylosuje nezávislá náhodná čísla a smíchá je přes rozklad $\Sigma$ na hlavní komponenty – jeden společný
  „tržní“ šok tak zasáhne víc aktiv najednou a ta se pohnou spolu. Pak se spočítá výnos portfolia a portfolio
  se vrátí na cílové váhy.
- Stránka GBS: korelace vstupují do $\Sigma$, která se nahraje do zařízení – rozklad na hlavní komponenty je
  tu přímo nastavení stlačení a interferometru. Povolené jsou jen nezáporné korelace.
- Stresové scénáře korelaci nepoužívají: scénář je konkrétní rok, ve kterém se aktiva pohnula tak, jak se
  skutečně pohnula.
- Předvolby trhu nastaví průměrnou korelaci za zvolené období, spočítanou přes páry tříd, které portfolio
  obsahuje.

**Proč nejde zadat libovolná čísla.** Korelace si nesmí odporovat: když se A hýbe hodně s B (0,9) a B hodně
s C (0,9), nemůže se A hýbat proti C (−0,9). Matematicky musí být korelační matice pozitivně semidefinitní,
jinak by některá kombinace aktiv měla záporný rozptyl – aplikace takovou matici odmítne. Proto posuvník začíná
na −0,5: stejná korelace všech párů $n$ aktiv nesmí klesnout pod $-1/(n-1)$, pro 3 aktiva tedy −0,5 a pro
4 aktiva už −0,33.

**Korelace není stálá.** Stejná dvojice akcie–státní dluhopisy se v různých krizích chovala opačně: v roce 2008
akcie klesly o 36,6 % a dluhopisy vzrostly o 20,1 % (útěk do bezpečí), v roce 2022 klesly akcie o 18,0 %
a dluhopisy o 17,8 % (obojí srazila inflace a rostoucí sazby). Za období 1972–2023 vychází korelace
akcie–dluhopisy +0,07, akcie–zlato −0,20 a dluhopisy–zlato −0,09. Model ale používá jedno pevné číslo na celý
horizont a korelace navíc měří jen lineární souvislost – extrémní roky se mohou chovat jinak, než napoví průměr.
""",
    further_reading=(
        Reading(MARKOWITZ, "proč diverzifikace snižuje riziko portfolia"),
        Reading(ANDEL_STATISTICS, "korelace a vícerozměrné normální rozdělení"),
        Reading(WIKIPEDIA_CORRELATION),
        Reading(DAMODARAN_RETURNS, "roční výnosy, ze kterých jsou spočítané historické korelace"),
    ),
    related_caveats=(SIGN_PROBLEM,),
)

WICK_THEOREM = TheoryTopic(
    anchor="wickova-veta",
    title="Wickova–Isserlisova věta a hafnián",
    in_short=(
        "Střední hodnota součinu gaussovských veličin se spočítá rozdělením činitelů do dvojic: každou dvojici "
        "nahradíme kovariancí a součiny přes všechna možná rozdělení sečteme. Tomuto součtu se říká hafnián – "
        "a proto je každý moment portfolia vážený součet hafniánů."
    ),
    explanation=r"""
**Věta polopatě.** Máme několik gaussovských veličin s nulovou střední hodnotou a chceme střední hodnotu
jejich součinu. Postup:

1. činitele rozdělíme **do dvojic** – každý činitel právě do jedné dvojice,
2. každou dvojici $(X_i, X_j)$ nahradíme kovariancí $\Sigma_{ij} = \mathbb{E}[X_iX_j]$,
3. součiny přes všechna možná rozdělení do dvojic sečteme.

Nejmenší zajímavý případ jsou čtyři činitele. Rozdělit $a, b, c, d$ do dvojic jde třemi způsoby –
$\{ab, cd\}$, $\{ac, bd\}$ a $\{ad, bc\}$ – takže

$$
\mathbb{E}[X_aX_bX_cX_d] = \Sigma_{ab}\Sigma_{cd} + \Sigma_{ac}\Sigma_{bd} + \Sigma_{ad}\Sigma_{bc}.
$$

**Opakované činitele.** Věta platí i tehdy, když se některá veličina opakuje – činitele jen rozlišujeme podle
pozice:

- $\mathbb{E}[X_1^4] = \mathbb{E}[X_1X_1X_1X_1]$: všechna tři rozdělení dají $\Sigma_{11}\Sigma_{11}$,
  celkem $3\sigma_1^4$ – známý čtvrtý moment normálního rozdělení.
- $\mathbb{E}[X_1^2X_2^2]$: rozdělení $\{11, 22\}$ dá $\Sigma_{11}\Sigma_{22}$ a dvě rozdělení $\{12, 12\}$ dají
  $\Sigma_{12}^2$, celkem $\sigma_1^2\sigma_2^2 + 2\Sigma_{12}^2$. Pro nekorelovaná aktiva zbude jen
  $\sigma_1^2\sigma_2^2$, kladná korelace moment zvětší.
- $\mathbb{E}[X_1^3X_2]$: $X_2$ se musí spárovat s jednou ze tří kopií $X_1$ a zbylé dvě spolu, takže
  $3\,\Sigma_{11}\Sigma_{12}$.
- $\mathbb{E}[X_1^2X_2X_3] = \Sigma_{11}\Sigma_{23} + 2\,\Sigma_{12}\Sigma_{13}$.
- Lichý počet činitelů do dvojic rozdělit nejde, proto $\mathbb{E}[X_1^3] = \mathbb{E}[X_1X_2X_3] = 0$.

**Kolik je rozdělení.** První činitel si vybírá partnera z $2m-1$ zbývajících, další volný z $2m-3$ atd.,
takže $2m$ činitelů jde do dvojic rozdělit $(2m-1)!! = 1\cdot3\cdot5\cdots(2m-1)$ způsoby: 1 pro dva
činitele, 3 pro čtyři, 15 pro šest, 105 pro osm, 945 pro deset a přes 650 milionů pro dvacet.

**Hafnián.** Součtu přes všechna rozdělení do dvojic se říká hafnián. Pro symetrickou matici $A$ rozměru
$2m \times 2m$ je

$$
\mathrm{Haf}(A) = \sum_{M}\ \prod_{\{i,j\} \in M} A_{ij},
$$

kde se sčítá přes všechna rozdělení indexů $1, \dots, 2m$ do dvojic $M$. V řeči grafů jde o součet přes
**perfektní párování** úplného grafu, jehož hrany mají váhy $A_{ij}$. Název zavedl E. R. Caianiello podle
Hafnie, latinského jména Kodaně, kde pracoval. Hafnián je příbuzný **permanentu** (determinantu bez znamének):
permanent matice $A$ je hafnián blokové matice $\begin{pmatrix} 0 & A \\ A^\top & 0 \end{pmatrix}$. Hafnián je
proto nejméně tak těžké spočítat jako permanent – a výpočet permanentu je #P-úplný (Valiant 1979).

**Věta formálně.** Je-li $(X_1, \dots, X_{2m})$ gaussovský vektor s nulovou střední hodnotou, pak

$$
\mathbb{E}[X_1X_2\cdots X_{2m}] = \sum_{M}\ \prod_{\{i,j\} \in M}\mathbb{E}[X_iX_j]
= \mathrm{Haf}\big(\operatorname{cov}(X)\big)
$$

a součin lichého počtu činitelů má střední hodnotu 0. Statistik L. Isserlis větu publikoval v roce 1918;
fyzik G. C. Wick ji v roce 1950 odvodil pro operátory v kvantové teorii pole, kde se jí dodnes říká Wickova
věta.

**Proč platí (náznak důkazu).** Všechny momenty gaussovského vektoru jsou uložené v jeho momentové
vytvořující funkci

$$
\mathbb{E}\big[e^{t^\top X}\big] = e^{\frac12 t^\top\Sigma t}
= \sum_{m=0}^{\infty}\frac{1}{m!}\Big(\tfrac12\,t^\top\Sigma t\Big)^m .
$$

Moment řádu $2m$ je $2m$-násobná derivace podle $t$ v bodě $0$ a tu „přežije“ jen člen
$\frac{1}{m!}\big(\tfrac12 t^\top\Sigma t\big)^m$. Ten je součinem $m$ kopií
$\tfrac12\sum_{i,j} t_i\Sigma_{ij}t_j$, takže si derivace rozeberou jednotlivá $t$ po dvojicích – každá
kopie dostane jednu dvojici. Každé rozdělení do dvojic přitom vznikne $2^m\,m!$ způsoby (pořadí dvojic
a pořadí uvnitř dvojice), což přesně vykrátí faktor $\frac{1}{2^m\,m!}$. Zbude součet přes rozdělení do
dvojic – hafnián.

**Od momentu portfolia k hafniánům.** Multinomická věta rozepíše mocninu součtu:

$$
L^d = (w_1X_1 + \dots + w_kX_k)^d = \sum_{|n| = d} c_n\,X_1^{n_1}\cdots X_k^{n_k},
\qquad c_n = \frac{d!}{n_1!\cdots n_k!}\,w_1^{n_1}\cdots w_k^{n_k}.
$$

Vzor $n = (n_1, \dots, n_k)$ říká, kolikrát se v monomu opakuje které aktivum; sčítá se přes všechny vzory se
součtem $|n| = n_1 + \dots + n_k = d$. Na každý monom použijeme Wickovu větu: jeho $d$ činitelů tvoří vektor,
ve kterém se $X_i$ opakuje $n_i$-krát, a kovarianční matice tohoto vektoru $\Sigma_n$ vznikne z $\Sigma$
zopakováním řádku i sloupce $i$ celkem $n_i$-krát. Tedy $\mathbb{E}[X_1^{n_1}\cdots X_k^{n_k}] =
\mathrm{Haf}(\Sigma_n)$ a

$$
\mathbb{E}[L^d] = \sum_{|n| = d} c_n\,\mathrm{Haf}(\Sigma_n).
$$

**Kolik je vzorů.** Vzorů se součtem $d$ pro $k$ aktiv je $\binom{d+k-1}{k-1}$ (kolika způsoby jde rozdělit
$d$ stejných kuliček do $k$ přihrádek): pro 3 aktiva a $d = 4$ je to 15 – tabulka níže je vypisuje všechny –
pro 6 aktiv a $d = 6$ už 462.

**Jeden řádek podrobně.** Vzor $n = (2, 0, 2)$ je monom $X_1^2X_3^2$ (akcie² · zlato²). Jeho koeficient je

$$
c_n = \frac{4!}{2!\,0!\,2!}\cdot 0{,}6^2\cdot 0{,}1^2 = 6\cdot 0{,}36\cdot 0{,}01 = 0{,}0216 .
$$

Matice $\Sigma_n$ opakuje řádky a sloupce 1, 1, 3, 3:

$$
\Sigma_{(2,0,2)} = \begin{pmatrix}
\Sigma_{11} & \Sigma_{11} & \Sigma_{13} & \Sigma_{13} \\ \Sigma_{11} & \Sigma_{11} & \Sigma_{13} & \Sigma_{13} \\
\Sigma_{13} & \Sigma_{13} & \Sigma_{33} & \Sigma_{33} \\ \Sigma_{13} & \Sigma_{13} & \Sigma_{33} & \Sigma_{33}
\end{pmatrix},
$$

a její hafnián (tři rozdělení do dvojic) je

$$
\Sigma_{11}\Sigma_{33} + 2\,\Sigma_{13}^2 = 0{,}0256\cdot 0{,}0225 + 2\cdot 0{,}0048^2 = 0{,}00062208 .
$$

Příspěvek k momentu je $0{,}0216\cdot 0{,}00062208 \approx 1{,}34\cdot 10^{-5}$, asi 3,8 % z
$\mathbb{E}[L^4] \approx 3{,}57\cdot 10^{-4}$.

**Proč je to pro GBS důležité.** Klasický výpočet hafniánu je exponenciálně drahý: nejlepší známé algoritmy
potřebují řádově $n^3\,2^{n/2}$ operací pro matici $n \times n$. GBS je fyzikální zařízení, jehož
pravděpodobnosti jsou hafniány – umí tedy vzorkovat z rozdělení daného hafniány, aniž by je kdokoli počítal.
Na tom stojí celá myšlenka 2. stránky.
""",
    further_reading=(
        Reading(ISSERLIS),
        Reading(WICK),
        Reading(WIKIPEDIA_HAFNIAN),
        Reading(WALRUS_HAFNIAN, "definice, vlastnosti a algoritmy pro výpočet hafniánu"),
        Reading(BARVINOK, "permanenty a hafniány podrobně"),
        Reading(VALIANT),
        Reading(BJORKLUND_GUPT_QUESADA),
    ),
    related_caveats=(CLOSED_FORM, CLASSICAL_SIMULATION),
)

GBS_DEVICE = TheoryTopic(
    anchor="gbs-zarizeni",
    title="Gaussian Boson Sampler: co je to za zařízení",
    in_short=(
        "Optický obvod: zdroje stlačeného světla vyrábějí fotony v párech, interferometr je promíchá mezi kanály "
        "a detektory spočítají fotony v každém kanálu. Pravděpodobnost každého výsledku je druhá mocnina "
        "hafniánu – proto se GBS hodí právě na úlohy s hafniány."
    ),
    explanation=r"""
**Kanály (módy).** Světlo v zařízení běží v $k$ oddělených kanálech – optických vláknech, vlnovodech na čipu
nebo časových oknech jednoho svazku. Fyzika jim říká **módy**. V každém módu může být libovolný počet fotonů.

**Tři části obvodu** (schéma je v kroku 3 na 2. stránce):

1. **Zdroje stlačeného světla.** Silný laserový puls prochází nelineárním krystalem nebo vlnovodem. Při
   takzvané spontánní parametrické konverzi se foton čerpacího svazku občas rozpadne na **dva** fotony.
   Výsledný stav se jmenuje **stlačené vakuum** a obsahuje jen 0, 2, 4, … fotonů. Parametr stlačení $r_j$
   určuje, jak ochotně páry vznikají; střední počet fotonů v módu $j$ je $\sinh^2 r_j$. Název „stlačené“
   pochází z toho, že kvantový šum jedné složky elektromagnetického pole je menší než u vakua – za cenu
   většího šumu složky druhé.
2. **Interferometr.** Síť děličů svazku (polopropustných zrcadel) a fázových posunů. Matematicky provádí
   unitární transformaci $U$: každý výstupní mód je „směsí“ všech vstupních. Libovolnou matici $U$ rozměru
   $k \times k$ jde poskládat z $k(k-1)/2$ děličů svazku (Reck a kol. 1994, Clements a kol. 2016).
   Interferometr je **pasivní** – fotony jen přerozděluje, žádné nepřidává ani neubírá.
3. **Detektory rozlišující počet fotonů.** Na konci každého módu detektor spočítá, kolik fotonů do něj
   dorazilo.

**Výstřel.** Jedno spuštění obvodu dá vzor $n = (n_1, \dots, n_k)$ – počty fotonů v jednotlivých
detektorech. Výsledek je náhodný a opakováním dostaneme vzorky z rozdělení $p(n)$. Odtud název *boson
sampling*, vzorkování bosonů – fotony jsou bosony.

**Pravděpodobnost vzoru.** Pro ideální (bezztrátové) zařízení platí (Hamilton a kol. 2017)

$$
p(n) = \frac{\mathrm{Haf}(B_n)^2}{n_1!\cdots n_k!\;\prod_{j=1}^{k}\cosh r_j},
\qquad B = U\,\mathrm{diag}(\tanh r_1, \dots, \tanh r_k)\,U^\top ,
$$

kde $B_n$ vznikne z $B$ opakováním řádku a sloupce $i$ celkem $n_i$-krát – stejná konstrukce jako $\Sigma_n$
ve Wickově větě. Pro obecné komplexní $U$ stojí v čitateli $|\mathrm{Haf}(B_n)|^2$; tady je $U$ reálné. Číslo
$1/\prod_j \cosh r_j$ je pravděpodobnost, že nevznikne žádný foton, a faktoriály $n_i!$ opravují počítání
stavů, kdy do jednoho detektoru dorazí víc nerozlišitelných fotonů.

**Proč zrovna hafnián.** Výstupní stav zařízení se dá (až na nepodstatnou fázi) zapsat jako

$$
|\psi\rangle = \frac{1}{\sqrt{\prod_j\cosh r_j}}\,
\exp\Big(\tfrac12\sum_{i,j} B_{ij}\,a_i^\dagger a_j^\dagger\Big)|0\rangle ,
$$

kde $a_i^\dagger$ přidá foton do módu $i$. Člen $B_{ij}\,a_i^\dagger a_j^\dagger$ vytvoří **pár** s jedním fotonem
v detektoru $i$ a druhým v detektoru $j$; $B_{ij} = \sum_l U_{il}\tanh(r_l)\,U_{jl}$ sčítá všechny zdroje $l$,
které ho mohly vyrobit. Rozepsáním exponenciály vzniknou součiny $m$ takových párů a amplituda vzoru se $2m$
fotony je součet přes všechny způsoby, jak detekované fotony rozdělit do párů – tedy $\mathrm{Haf}(B_n)$
vydělený $\sqrt{n!}$ a normalizací. Je to stejná kombinatorika jako v důkazu Wickovy věty (exponenciála
kvadratické formy). Pravděpodobnost je kvadrát absolutní hodnoty amplitudy (Bornovo pravidlo), odtud druhá
mocnina hafniánu.

**Proč je to „těžké“.** Aaronson a Arkhipov (2011) ukázali, že přesně vzorkovat z obdobného rozdělení
s permanenty (jednotlivé fotony místo stlačeného světla) klasický počítač za rozumných předpokladů teorie
složitosti efektivně nezvládne. GBS je varianta se stlačeným světlem a hafniány, kterou navrhli Hamilton,
Kruse, Sansoni, Barkhofen, Silberhorn a **Igor Jex z FJFI ČVUT v Praze** (2017). Na ní stojí experimenty
kvantové výhody Jiuzhang (Čína, 2020) a Borealis (Kanada, 2022). Jak ale upozorňuje první háček, klasické
algoritmy reálná (ztrátová) zařízení dohánějí.

**Proč se hodí pro Wickovu větu.** Pravděpodobnosti GBS obsahují hafniány matice $B$, momenty portfolia
hafniány matice $\Sigma$. Když zařízení nastavíme tak, aby $B$ byla úměrná $\Sigma$, ponesou četnosti
výstřelů informaci o momentech (další dva oddíly).
""",
    further_reading=(
        Reading(HAMILTON),
        Reading(KRUSE, "odvození vzorce pro $p(n)$ krok za krokem"),
        Reading(AARONSON_ARKHIPOV),
        Reading(SALEH_TEICH, "fotony a kvantové stavy světla"),
        Reading(GERRY_KNIGHT, "stlačené stavy světla"),
        Reading(RECK),
        Reading(CLEMENTS),
        Reading(ZHONG),
        Reading(MADSEN),
    ),
    related_caveats=(CLASSICAL_SIMULATION,),
)

ENCODING = TheoryTopic(
    anchor="nahrani-matice",
    title="Nahrání Σ do zařízení: proč stlačení a interferometr",
    in_short=(
        r"Zařízení nastavíme tak, aby jeho matice $B$ byla úměrná kovarianční matici: $B = \gamma\Sigma$. "
        r"Rozklad $\Sigma$ na vlastní čísla a vlastní vektory přímo říká jak: vlastní čísla (rozptyly hlavních "
        "komponent) určí stlačení, vlastní vektory nastavení interferometru."
    ),
    explanation=r"""
**Cíl.** Pravděpodobnosti GBS obsahují $\mathrm{Haf}(B_n)$, moment potřebuje $\mathrm{Haf}(\Sigma_n)$. Když bude
$B = \gamma\Sigma$ pro nějaké kladné číslo $\gamma$, je v každém členu hafniánu matice $d \times d$ součin $d/2$
prvků a každý nese jedno $\gamma$, takže

$$
\mathrm{Haf}(B_n) = \gamma^{d/2}\,\mathrm{Haf}(\Sigma_n).
$$

Škálování $\gamma$ známe, na konci ho vydělíme.

**Spektrální rozklad.** Kovarianční matice je symetrická a pozitivně semidefinitní, proto má rozklad

$$
\Sigma = V\,\mathrm{diag}(\lambda_1, \dots, \lambda_k)\,V^\top, \qquad \lambda_j \ge 0,
$$

kde sloupce ortogonální matice $V$ jsou vlastní vektory a $\lambda_j$ vlastní čísla. Porovnání
s $B = U\,\mathrm{diag}(\tanh r)\,U^\top$ dává přímo návod:

$$
U = V, \qquad \tanh r_j = \gamma\,\lambda_j .
$$

(Pro obecnou komplexní symetrickou matici se používá Takagiho rozklad; pro reálnou pozitivně semidefinitní
matici splývá s rozkladem na vlastní čísla.)

**Proč „eigen-portfolia“.** Vlastní vektory kovarianční matice jsou **hlavní komponenty** (analýza hlavních
komponent, PCA): vzájemně nekorelované kombinace aktiv. Komponenta $j$ je portfolio s vahami ve sloupci $j$
matice $V$ a její rozptyl je přesně $\lambda_j$. Rozklad tedy říká, že riziko se dá zapsat jako $k$
nezávislých zdrojů náhody. Pro výchozí portfolio:

- $\lambda \approx 0{,}0293$ – akcie a zlato společně, jakýsi „trh“, největší zdroj rizika,
- $\lambda \approx 0{,}0190$ – zlato proti akciím (rozdíl jejich výnosů),
- $\lambda \approx 0{,}0023$ – téměř čisté dluhopisy, nejmenší riziko.

**Proč silnější stlačení pro větší rozptyl.** Ve vzorci $\tanh r_j = \gamma\lambda_j$ roste stlačení
s rozptylem komponenty, takže zdroj $j$ vyrábí fotonové páry tím ochotněji, čím víc komponenta $j$ přispívá
k riziku. Střední počet fotonů $\sinh^2 r_j$ je u výchozího portfolia 0,96 pro „trh“, 0,26 pro „zlato proti
akciím“ a jen 0,003 pro „dluhopisy“. Fotony tak nesou informaci úměrně tomu, jak moc daná komponenta hýbe
výnosem.

**Proč interferometr skládá komponenty zpět na aktiva.** Rozklad $\Sigma = V\,\mathrm{diag}(\lambda)\,V^\top$
čteme zprava doleva: nezávislé komponenty ($\mathrm{diag}(\lambda)$) se maticí $V$ promítnou na jednotlivá
aktiva. Interferometr $U = V$ dělá fyzicky totéž se světlem: vstupní mód $j$ nese komponentu $j$ a po průchodu
interferometrem obsahuje výstupní mód $i$ přesně takovou směs komponent, jakou má aktivum $i$. Proto
**detektor $i$ odpovídá aktivu $i$** a počet fotonů $n_i$ v něm hraje roli mocniny $X_i$ v monomu. Heatmapa
$|U|$ v kroku 3 ukazuje, jak silně míří který vstup do kterého aktiva.

**Proč škálování $\gamma$ a „síla stlačení“.** Nekonečné stlačení neexistuje: musí platit $\tanh r_j < 1$,
tedy $\gamma\lambda_{\max} < 1$. Aplikace volí $\gamma = s/\lambda_{\max}$, kde $s = \tanh r_{\max} \in (0, 1)$
je posuvník „síla stlačení“. Největší komponenta dostane $\tanh r = s$, ostatní úměrně méně. Pro výchozí
portfolio a $s = 0{,}7$ je $\gamma \approx 23{,}9$ a $r \approx (0{,}06;\ 0{,}49;\ 0{,}87)$. Na výsledném
momentu $\gamma$ nezáleží (vydělí se), ovlivní ale, kolik fotonů vzniká – a tedy kolik výstřelů bude
užitečných.

**Proč jen nezáporné korelace.** Samotné nahrání by fungovalo pro libovolnou pozitivně semidefinitní
$\Sigma$. Problém nastane až při zpětném výpočtu: z pravděpodobnosti úměrné $\mathrm{Haf}^2$ se dá získat jen
$|\mathrm{Haf}|$ a znaménko se ztratí.
""",
    further_reading=(
        Reading(KRUSE, "jak gaussovský stav určí matici $B$"),
        Reading(BRADLER, "nahrání libovolné symetrické matice přes Takagiho rozklad"),
        Reading(ARRAZOLA_BROMLEY),
        Reading(WIKIPEDIA_PRINCIPAL_COMPONENTS),
        Reading(CLEMENTS, "jak z děličů svazku poskládat libovolné $U$"),
    ),
    related_caveats=(SIGN_PROBLEM,),
)

SHOTS = TheoryTopic(
    anchor="vystrely",
    title="Výstřely: proč sudé počty fotonů a proč jen d fotonů",
    in_short=(
        "Zdroje vyrábějí fotony jen v párech a interferometr je jen přerozděluje, proto má každý výstřel "
        r"sudý počet fotonů. Pro moment stupně $d$ jsou užitečné jen výstřely s přesně $d$ fotony – jen ty "
        "odpovídají hafniánům, které v momentu vystupují."
    ),
    explanation=r"""
**Co je výstřel.** Jeden výstřel je jedno spuštění obvodu: zdroje vyšlou pulz stlačeného světla, ten projde
interferometrem a detektory zaznamenají počty fotonů $n = (n_1, \dots, n_k)$. Reálná zařízení opakují výstřely
rychle za sebou s každým pulzem laseru.

**Proč sudé počty.** Stlačené vakuum v jednom módu má v bázi počtu fotonů tvar

$$
|\psi_r\rangle = \frac{1}{\sqrt{\cosh r}}\sum_{m=0}^{\infty}(-\tanh r)^m\,
\frac{\sqrt{(2m)!}}{2^m\,m!}\;|2m\rangle ,
$$

obsahuje tedy jen stavy se **sudým** počtem fotonů $2m$ – fotony vznikají v párech. Pravděpodobnost, že zdroj
vyzáří $2m$ fotonů, je druhá mocnina amplitudy:

$$
P(2m) = \frac{(2m)!}{(2^m\,m!)^2}\,\frac{\tanh^{2m} r}{\cosh r}, \qquad P(\text{lichý počet}) = 0 .
$$

Interferometr je pasivní (energii nedodává ani neodebírá), takže **zachovává celkový počet fotonů** a jen ho
přerozdělí mezi výstupní módy. Celkový počet ve výstřelu je proto součet sudých čísel – sudý. Jednotlivé
detektory přitom liché počty vidět mohou: pár se může rozdělit do dvou detektorů, třeba vzor $(1, 0, 1)$.

**Rozdělení celkového počtu fotonů.** Interferometr na součtu nic nemění, takže celkový počet je součet
nezávislých příspěvků jednotlivých zdrojů a jeho rozdělení je konvoluce rozdělení $P(2m)$ všech módů – bez
jediného hafniánu. Pro výchozí portfolio a sílu stlačení 0,7 má výstřel 0 fotonů s pravděpodobností 63,5 %,
2 fotony s 22,2 %, 4 fotony s 8,4 %, 6 fotonů s 3,4 %, 8 fotonů s 1,4 % a víc fotonů s 1,1 %.

**Proč jen výstřely s přesně $d$ fotony.** Vzor $n$ se součtem $|n|$ souvisí jen s hafniánem
$\mathrm{Haf}(B_n)$ matice rozměru $|n| \times |n|$. Moment $\mathbb{E}[L^d]$ je součet hafniánů rozměru
$d \times d$ (monomy stupně $d$). Výstřely s jiným počtem fotonů – prázdné, se 2 fotony nebo se 6 fotony při
$d = 4$ – nesou informaci o jiných hafniánech (dvoufotonové vzory třeba o jednotlivých kovariancích), které
v součtu pro $\mathbb{E}[L^d]$ přímo nevystupují, a estimátor je proto zahodí (tzv. post-selekce). Podíl
užitečných výstřelů je $P_d = P(\text{celkem} = d)$: pro výchozí nastavení a $d = 4$ asi 8,4 %, zhruba každý
dvanáctý výstřel.

**Proč nejde vyrábět přesně $d$ fotonů.** Počet párů je náhodný – řídí ho kvantová statistika stlačeného
světla, ne experimentátor. Síla stlačení jen posouvá rozdělení: slabé stlačení znamená převahu prázdných
výstřelů, silné převahu výstřelů s mnoha fotony. Užitečný podíl má proto maximum někde uprostřed. Střední
počet fotonů $\bar n = \sum_j \sinh^2 r_j$ je při výchozím nastavení asi 1,22.

**Kde se skrývá hafnián.** Rozdělení celkového počtu fotonů hafniány nepotřebuje. Hafniány rozhodují až
o tom, **jak se** daný počet fotonů **rozdělí mezi detektory** – tedy o pravděpodobnostech jednotlivých vzorů
se stejným součtem. Právě tyto podíly nesou informaci o $\Sigma$.
""",
    further_reading=(
        Reading(KRUSE),
        Reading(GERRY_KNIGHT, "stlačené vakuum v bázi počtu fotonů"),
        Reading(QUESADA_THRESHOLD_DETECTORS, "co se změní, když detektor pozná jen „foton ano/ne“"),
    ),
    related_caveats=(DISCARDED_SHOTS,),
)

ESTIMATOR = TheoryTopic(
    anchor="odhad-z-cetnosti",
    title="Od četností fotonů zpět k momentu",
    in_short=(
        "Ze vzorce pro pravděpodobnost vzoru se dá vyjádřit hafnián. Neznámou pravděpodobnost nahradí relativní "
        "četnost z výstřelů a dosazením do Wickova součtu vznikne odhad momentu."
    ),
    explanation=r"""
**Krok 1: vyjádřit hafnián z pravděpodobnosti.** Pro vzor $n$ se součtem $|n| = d$ platí

$$
p(n) = \frac{\mathrm{Haf}(B_n)^2}{n!\,Z}, \qquad n! = n_1!\cdots n_k!, \qquad Z = \prod_j\cosh r_j .
$$

Protože $B = \gamma\Sigma$, je $\mathrm{Haf}(B_n) = \gamma^{d/2}\,\mathrm{Haf}(\Sigma_n)$. Po dosazení
a odmocnění:

$$
\mathrm{Haf}(\Sigma_n) = \gamma^{-d/2}\,\sqrt{p(n)\;n!\;Z}.
$$

Odmocnina dává nezápornou hodnotu – správné znaménko to je jen tehdy, když $\mathrm{Haf}(\Sigma_n) \ge 0$,
což zaručí nezáporné korelace.

**Krok 2: odhadnout pravděpodobnost četností.** Ze všech $N$ výstřelů (i zahozených) spočítáme, kolikrát
padl vzor $n$: $N_n$. Relativní četnost $\hat p(n) = N_n/N$ je nestranný odhad $p(n)$ – stejný princip jako
u Buffonovy jehly, kde se pravděpodobnost odhaduje podílem „úspěšných“ pokusů. Počty $N_n$ mají dohromady
multinomické rozdělení.

**Krok 3: složit moment.** Dosazením do Wickova součtu vznikne odhad

$$
\widehat{\mathbb{E}[L^d]} = \sum_{|n| = d} c_n\,\gamma^{-d/2}\sqrt{\hat p(n)\;n!\;Z}.
$$

Všechno kromě $\hat p(n)$ je známé předem: koeficienty $c_n$ z vah, $\gamma$ a $Z$ z nastavení zařízení
a faktoriály ze vzoru. **Zařízení dodá jen četnosti** – žádný hafnián se klasicky nepočítá.

**Příklad s čísly** (výchozí portfolio, $d = 4$, síla stlačení 0,7, $\gamma \approx 23{,}914$,
$Z \approx 1{,}5746$). Vzor $(4, 0, 0)$ – čtyři fotony v detektoru akcií – má pravděpodobnost
$p \approx 3{,}346\,\%$ na výstřel. Pak

$$
\gamma^{-2}\sqrt{p\cdot 4!\cdot Z} = \frac{\sqrt{0{,}03346\cdot 24\cdot 1{,}5746}}{23{,}914^2}
\approx \frac{1{,}1244}{571{,}9} \approx 0{,}0019661 ,
$$

což je přesně

$$
\mathrm{Haf}(\Sigma_{(4,0,0)}) = 3\sigma_1^4 = 3\cdot 0{,}16^4 = 0{,}0019661 .
$$

Ze 100 000 výstřelů padne tento vzor v průměru asi 3 346×; skutečný počet kolísá zhruba o $\sqrt{N p (1-p)} \approx 57$, tedy
o 1,7 %, a odhad hafniánu díky odmocnině jen o 0,85 %. Obecně kolísá počet výskytů vzoru relativně zhruba
o $1/\sqrt{N_n}$ a odhad hafniánu o polovinu toho – vzory, které padají zřídka, jsou proto odhadnuté nejhůř.

**Vlastnosti odhadu.**

- *Konzistentní:* s rostoucím $N$ jdou četnosti k pravděpodobnostem (zákon velkých čísel) a odmocnina je
  spojitá, takže odhad jde k přesné hodnotě.
- *Pro konečné $N$ mírně vychýlený:* průměr odmocnin je menší než odmocnina průměru (Jensenova nerovnost)
  a vzory, které zatím nepadly, se počítají jako nula. Vychýlení ale mizí jako $1/N$, rychleji než náhodná
  chyba $1/\sqrt{N}$.
- *Chyba úměrná $1/\sqrt{N}$:* podrobně v dalším oddílu.

**Co estimátor potřebuje a co ne.** Potřebuje znát $\gamma$, $Z$ a $c_n$ – to jsou vstupy nastavení, ne
výsledek. Hafniány matice $\Sigma$ nikde nepočítá, jen je „čte“ z fyzikálního experimentu. V této aplikaci
je ovšem i ten experiment simulovaný klasicky.
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_EXPECTATIONS),
        Reading(ANDERSEN_SHAN_ADVANTAGE),
        Reading(ARRAZOLA_REBENTROST_WEEDBROOK),
    ),
    related_caveats=(SIGN_PROBLEM, CLASSICAL_SIMULATION),
)

COMPARISON = TheoryTopic(
    anchor="srovnani",
    title="Srovnání s klasickým Monte Carlem polopatě",
    in_short=(
        r"Chyba obou metod klesá jako $c/\sqrt{N}$. Rozhoduje jen konstanta $c$: u klasického MC závisí jen na "
        "stupni momentu, u GBS na tom, jak dobře četnosti vzorů odpovídají jejich podílům na momentu – a kolik "
        "výstřelů se zahodí."
    ),
    explanation=r"""
**Jak se v aplikaci srovnává.** Obě metody dostanou stejný „rozpočet“ $N$: klasické MC $N$ náhodných scénářů,
GBS $N$ výstřelů (i těch, které zahodí). Celý odhad se zopakuje 20× s jinými náhodnými čísly a spočítá se
**relativní RMSE**

$$
\mathrm{RMSE}_{\mathrm{rel}} = \frac{1}{\mu}\sqrt{\frac{1}{20}\sum_{r=1}^{20}\big(\hat\mu^{(r)} - \mu\big)^2},
$$

tedy typická odchylka odhadu od přesné hodnoty $\mu$ v procentech. Relativní chyba 1 % znamená, že se odhad
obvykle trefí do ±1 % přesné hodnoty. Pozor, i RMSE z 20 opakování je jen odhad s relativní nejistotou zhruba
$1/\sqrt{2\cdot 20} \approx 16\,\%$. Naměřené chyby se proto mezi běhy liší a spolehlivější je srovnat
teoretické konstanty níže (na 2. stránce jsou v grafu konvergence čárkovaně).

**Obě chyby klesají jako $1/\sqrt{N}$.** U MC to říká centrální limitní věta; u GBS totéž platí pro četnosti
a odmocnina na tom nic nemění. V logaritmickém grafu jsou to rovnoběžné přímky se sklonem $-\tfrac12$:
**4× víc vzorků znamená poloviční chybu, 100× víc desetinovou**. O vítězi rozhoduje jen konstanta $c$
v $\mathrm{RMSE}_{\mathrm{rel}} \approx c/\sqrt{N}$ a k přesnosti $\varepsilon$ je potřeba zhruba
$N \approx (c/\varepsilon)^2$ vzorků.

**Konstanta klasického MC.** Jeden scénář přispěje hodnotou $L^d$ a chyba průměru je daná poměrem jejího
rozptylu a čtverce střední hodnoty. Protože $L$ je normální, spočítá se přesně z momentů
$\mathbb{E}[L^{2d}] = (2d-1)!!\,\sigma_p^{2d}$:

$$
c_{\mathrm{MC}} = \sqrt{\frac{\operatorname{var}(L^d)}{\mu^2}} = \sqrt{\frac{(2d-1)!!}{\big((d-1)!!\big)^2} - 1}
\;\approx\; 1{,}41\ (d = 2),\quad 3{,}27\ (d = 4),\quad 6{,}72\ (d = 6).
$$

Volatilita i váhy se vykrátí – **pro každé gaussovské portfolio vyjde stejně**. Vyšší moment znamená větší
chybu, protože $L^d$ čím dál víc ovládají vzácné extrémní scénáře. Pro přesnost 1 % a $d = 4$ potřebuje MC
asi $(3{,}27/0{,}01)^2 \approx 107\,000$ scénářů.

**Konstanta GBS: vážený výběr, který volí fyzika.** Česká skripta o Monte Carlu popisují **metodu váženého
výběru** (importance sampling): body se losují s hustotou $p$, průměruje se $f/p$ a rozptyl odhadu je
$\int f^2/p - I^2$ – nejmenší, když je $p$ úměrné $|f|$. GBS estimátor se chová velmi podobně. Delta metoda
(rozvoj odmocniny do prvního řádu) dává pro velké $N$

$$
c_{\mathrm{GBS}} = \frac12\sqrt{\sum_{|n| = d}\frac{\pi_n^2}{p(n)} - 1},
\qquad \pi_n = \frac{c_n\,\mathrm{Haf}(\Sigma_n)}{\mu}\ \text{(podíl vzoru na momentu)}.
$$

Čte se to takhle:

- **Faktor ½** přináší odmocnina: relativní chyba četnosti 2 % znamená relativní chybu hafniánu 1 %.
- **Člen $\pi_n^2/p(n)$** trestá vzory, které nesou velký podíl momentu, ale padají zřídka. Zařízení „losuje“
  vzory s pravděpodobnostmi $p(n)$, které nevolíme my, ale fyzika. Ideální by bylo $p(n)$ úměrné $\pi_n$.
- **Zahazování výstřelů** je ve vzorci schované: užitečné vzory mají dohromady pravděpodobnost jen $P_d$.
  I kdyby se pravděpodobnosti trefily do podílů dokonale, platí podle Cauchyovy–Schwarzovy nerovnosti

$$
c_{\mathrm{GBS}} \;\ge\; \frac12\sqrt{\frac{1}{P_d} - 1}.
$$

Pro $P_d = 8{,}4\,\%$ je to 1,65 – nejlepší možný případ je tedy asi dvakrát lepší než MC.

**Výchozí portfolio v číslech** ($d = 4$, síla stlačení 0,7). Vzor $(4, 0, 0)$ nese 71 % momentu a tvoří 40 %
užitečných výstřelů – to je v pořádku. Vzor $(3, 1, 0)$ ale nese 8,9 % momentu a přitom tvoří jen 0,6 %
užitečných výstřelů: dluhopisy mají malou volatilitu, takže fotonů v jejich detektoru je málo, jenže váha
30 % dělá z jejich kombinací s akciemi nezanedbatelnou část momentu. Takové vzory konstantu zvětšují.
Výsledek $c_{\mathrm{GBS}} \approx 3{,}15$ proti $c_{\mathrm{MC}} \approx 3{,}27$ – proto na 2. stránce
vychází chyba obou metod **srovnatelná**.

**Kdy vyhraje která metoda** (graf níže, výchozí portfolio):

- *Slabé stlačení:* většina výstřelů je prázdná, $P_d$ je malé a GBS prohrává. Pro $d = 4$ a sílu 0,3 je
  $c_{\mathrm{GBS}} \approx 14$, tedy potřeba zhruba 19× víc výstřelů než scénářů.
- *Silnější stlačení a vyšší momenty:* MC trpí těžkým chvostem $L^d$, kdežto GBS „vidí“ velké podíly
  momentu přímo. Pro $d = 6$ a sílu 0,9 je $c_{\mathrm{GBS}} \approx 3{,}9$ proti $6{,}7$ u MC – k téže
  přesnosti stačí asi třikrát méně výstřelů než scénářů.

**Co srovnání neříká.** Počet vzorků není čas ani cena: jeden výstřel reálného GBS, jeho kalibrace a přenos
dat stojí jinak než jeden gaussovský scénář na procesoru. Srovnává se navíc s nejjednodušším MC – metody
snižování rozptylu (vážený výběr, nalezení hlavní části) by zmenšily i $c_{\mathrm{MC}}$. A pro tento
konkrétní moment existuje vzorec, takže tu jde o testovací úlohu.
""",
    further_reading=(
        Reading(DRIMAL_MONTE_CARLO, "kap. 5.4 odhad účinnosti metody, kap. 5.7 metoda váženého výběru"),
        Reading(ANDERSEN_SHAN_EXPECTATIONS),
        Reading(ANDERSEN_SHAN_ADVANTAGE),
        Reading(GLASSERMAN, "snižování rozptylu ve financích"),
    ),
    related_caveats=(SAMPLES_NOT_TIME, DISCARDED_SHOTS, CLOSED_FORM),
)

GBS_ADVANTAGE = TheoryTopic(
    anchor="exponencialni-vyhoda",
    title="Exponenciální výhoda: co přesně dokázali Andersen a Shan",
    in_short=(
        "Andersen a Shan (2025) dokázali, že existují gaussovské úlohy, pro které GBS stačí polynomiálně mnoho "
        "vzorků, zatímco klasickému Monte Carlu exponenciálně mnoho. Jde hlavně o polynomy velmi vysokého stupně; "
        "o tento výsledek se opírá i tvrzení firmy Qpurpose o exponenciálním zrychlení."
    ),
    explanation=r"""
**Kdo a kde.** Jørgen Ellegaard Andersen a Shan Shan z Center for Quantum Mathematics na University of Southern
Denmark zveřejnili v únoru 2025 dva preprinty na arXivu; recenzovanou verzi se zatím dohledat nepodařilo. Na
centrum navazuje firma Qpurpose (spin-off z roku 2022). V přehledu *16 Danish Quantum Use Cases* (prosinec 2024)
popisuje projekt pro Jyske Bank, kde GBS má „v určitých případech“ nabízet exponenciální zrychlení oproti
Monte Carlu.

**Prostor úloh.** Úloha je spočítat $\mathbb{E}[f(X)]$ pro gaussovský vektor $X$ v $N$ dimenzích
s kovarianční maticí $B$ (vlastní čísla mezi 0 a 1, aby šla nahrát do zařízení) a polynom
$f(x) = \sum_{|I| \le K} a_I\,x^I$ stupně nejvýš $K$. Jedna úloha je tedy volba $N$, $K$, $B$ a koeficientů
$a_I$ – naše $\mathbb{E}[L^d]$ je speciální případ.

**Dva odhady.**

- *GBS-I* se chová jako vážený výběr: průměruje přeškálované koeficienty $a_I$ přes vylosované vzory. Je
  nestranný, ale řeší upravenou úlohu, ve které místo hafniánů vystupují jejich druhé mocniny,
  $\sum_I a_I\,\mathrm{Haf}(B_I)^2$ – střední hodnotu přes „zdvojený“ gaussovský vektor s kovariancí
  $B \oplus B$.
- *GBS-P* odmocňuje relativní četnosti vzorů – přesně odhad z 2. stránky. Je mírně vychýlený, ale řeší
  původní úlohu.

**Co tvrdí.** Srovnávají zaručený počet vzorků, se kterým má odhad s pravděpodobností aspoň $1-\delta$ relativní
chybu nejvýš $\varepsilon$ (odvozený z rozptylu přes Čebyševovu nerovnost). Hlavní věty říkají, že pro dost velký
stupeň $K$ existuje neprázdná otevřená podmnožina úloh, kde klasické Monte Carlo potřebuje exponenciálně víc
vzorků než GBS – pro GBS-I na upravené úloze i pro GBS-P na původní. Zpřesněná verze: pro
$K \ge \zeta N^2$ stačí GBS řádově $N^{3+p}$ vzorků, zatímco Monte Carlo potřebuje aspoň $e^{c N^2}$.

**Jaká je to množina, polopatě.** „Otevřená neprázdná podmnožina“ znamená, že takové úlohy existují a malá změna
matice nebo koeficientů výhodu nezničí; věta ale neříká, jak velká ta oblast je. Tvoří ji hlavně polynomy velmi
vysokého stupně (stupeň roste aspoň s druhou mocninou počtu proměnných) s koeficienty sladěnými s rozdělením GBS.
Důvod je stejný jako ve srovnání na 2. stránce: rozptyl klasického Monte Carla roste se stupněm polynomu
exponenciálně – u nás konstanta $c_{\mathrm{MC}}$ roste z 1,41 přes 3,27 na 6,72 pro $d = 2, 4, 6$ – kdežto GBS
se chová jako vážený výběr, který sám losuje vzory úměrně hafniánům na druhou. Druhý článek odhaduje, jak velký
podíl úloh je výhodný: po vyladění středního počtu fotonů „podstatný“, ve speciálních případech téměř 100 %.

**Na co si dát pozor.**

- Jde o počet vzorků ideálního bezeztrátového GBS, ne o čas ani o reálný hardware; klasické algoritmy dnes
  reálná ztrátová zařízení umějí napodobit (Oh a kol. 2024).
- Srovnává se s obyčejným Monte Carlem, ne s nejlepší klasickou metodou (vážený výběr, řídicí proměnné).
- Je to věta o existenci: užitek pro konkrétní finanční úlohy (VaR, opce) v článcích doložený není. Tvrzení
  o přínosu pro obchodování v Jyske Bank pocházejí z přehledu případových studií, ne z recenzované práce,
  a podle něj i stránek SDU algoritmy zatím běží na klasických počítačích.
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "definice úloh, odhady GBS-I a GBS-P a věty o exponenciální výhodě"),
        Reading(ANDERSEN_SHAN_ADVANTAGE, "jak velký podíl úloh je výhodný"),
        Reading(DANISH_QUANTUM_USE_CASES, "případ 16: Jyske Bank a Qpurpose"),
        Reading(SDU_QUANTUM_FINANCE, "spolupráce centra QM, Jyske Bank a Qpurpose"),
        Reading(OH_CLASSICAL_SIMULATION, "proč výhoda reálných zařízení není samozřejmá"),
    ),
    related_caveats=(SAMPLES_NOT_TIME, CLASSICAL_SIMULATION, CLOSED_FORM),
)

TOPICS: Tuple[TheoryTopic, ...] = (
    MONTE_CARLO,
    PORTFOLIO_MOMENT,
    CORRELATION,
    WICK_THEOREM,
    GBS_DEVICE,
    ENCODING,
    SHOTS,
    ESTIMATOR,
    COMPARISON,
    GBS_ADVANTAGE,
)


def all_sources(topics: Sequence[TheoryTopic]) -> List[Source]:
    """Every cited source once, in the order in which the topics first cite it."""
    sources: List[Source] = []
    for topic in topics:
        for reading in topic.further_reading:
            if reading.source not in sources:
                sources.append(reading.source)
    return sources
