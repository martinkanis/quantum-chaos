"""Commented reading of Andersen & Shan, arXiv:2502.19336: what each part of the paper says, explained from scratch."""

from __future__ import annotations

from typing import Tuple

from ui.theory_content import (
    ANDEL_STATISTICS,
    ANDERSEN_SHAN_ADVANTAGE,
    ANDERSEN_SHAN_EXPECTATIONS,
    ARRAZOLA_BROMLEY,
    BRADLER,
    GLASSERMAN,
    HAMILTON,
    ISSERLIS,
    MADSEN,
    OH_CLASSICAL_SIMULATION,
    WICK,
    WIKIPEDIA_COVARIANCE,
    WIKIPEDIA_HAFNIAN,
    ZHONG,
    KeyFinding,
    Reading,
    Source,
    TheoryTopic,
)

TITLE = "Článek Andersena a Shan krok za krokem"
SOURCES_ANCHOR = "clanek-zdroje"
INTRO = (
    "Čtení s komentářem k hlavnímu článku celé linie: Andersen, Shan, Using Gaussian Boson Samplers to Approximate "
    "Gaussian Expectation Problems (arXiv:2502.19336, verze 2). Zatím úvod na stranách 2–3: proč článek vznikl "
    "a jak přesně je zadaná úloha. Každý vzorec rozebíráme po částech a s příkladem; další oddíly přibudou postupně."
)

EXAMPLE_COVARIANCE = ((0.5, 0.25), (0.25, 0.5))
"""B of the worked examples: variances 0.5, covariance 0.25, eigenvalues 0.75 and 0.25 (below 1, as GBS needs)."""
EXAMPLE_WEIGHTS = (0.6, 0.4)
EXAMPLE_PORTFOLIO_SECOND_MOMENT = "0{,}38"
EXAMPLE_FOURTH_ORDER_MOMENT = "0{,}375"
COEFFICIENT_COUNT_EXAMPLE = "3 108 105"
"""Number of coefficients a_I of a polynomial in 20 variables of degree at most 8."""
COSH_EXPECTATION = "1{,}649"
"""E[cosh X] = e^{1/2} for X ~ N(0, 1)."""

ZHONG_2021 = Source(
    "Zhong, H.-S. a kol.: *Phase-programmable Gaussian boson sampling using stimulated squeezed light*. Physical "
    "Review Letters 127, 180502 (2021), [doi:10.1103/PhysRevLett.127.180502]"
    "(https://doi.org/10.1103/PhysRevLett.127.180502)"
)
MOTES_TIME_BIN = Source(
    "Motes, K. R., Gilchrist, A., Dowling, J. P., Rohde, P. P.: *Scalable boson sampling with time-bin encoding "
    "using a loop-based architecture*. Physical Review Letters 113, 120501 (2014), "
    "[doi:10.1103/PhysRevLett.113.120501](https://doi.org/10.1103/PhysRevLett.113.120501)"
)
HE_TIME_BIN = Source(
    "He, Y. a kol.: *Time-bin-encoded boson sampling with a single-photon device*. Physical Review Letters 118, "
    "190501 (2017), [doi:10.1103/PhysRevLett.118.190501](https://doi.org/10.1103/PhysRevLett.118.190501)"
)
HUH_VIBRONIC = Source(
    "Huh, J., Guerreschi, G. G., Peropadre, B., McClean, J. R., Aspuru-Guzik, A.: *Boson sampling for molecular "
    "vibronic spectra*. Nature Photonics 9, 615–620 (2015), "
    "[doi:10.1038/nphoton.2015.153](https://doi.org/10.1038/nphoton.2015.153)"
)
HUH_YUNG_VIBRONIC = Source(
    "Huh, J., Yung, M.-H.: *Vibronic boson sampling: generalized Gaussian boson sampling for molecular vibronic "
    "spectra at finite temperature*. Scientific Reports 7, 7462 (2017), "
    "[doi:10.1038/s41598-017-07770-z](https://doi.org/10.1038/s41598-017-07770-z)"
)
BANCHI_DOCKING = Source(
    "Banchi, L., Fingerhuth, M., Babej, T., Ing, C., Arrazola, J. M.: *Molecular docking with Gaussian boson "
    "sampling*. Science Advances 6, eaax1950 (2020), "
    "[doi:10.1126/sciadv.aax1950](https://doi.org/10.1126/sciadv.aax1950)"
)
ARRAZOLA_OPTIMIZATION = Source(
    "Arrazola, J. M., Bromley, T. R., Rebentrost, P.: *Quantum approximate optimization with Gaussian boson "
    "sampling*. Physical Review A 98, 012322 (2018), "
    "[doi:10.1103/PhysRevA.98.012322](https://doi.org/10.1103/PhysRevA.98.012322)"
)
BRADLER_ISOMORPHISM = Source(
    "Brádler, K., Friedland, S., Izaac, J., Killoran, N., Su, D.: *Graph isomorphism and Gaussian boson "
    "sampling*. Special Matrices 9, 166–196 (2021), "
    "[doi:10.1515/spma-2020-0132](https://doi.org/10.1515/spma-2020-0132)"
)
SCHULD_GRAPH_KERNEL = Source(
    "Schuld, M., Brádler, K., Israel, R., Su, D., Gupt, B.: *A quantum hardware-induced graph kernel based on "
    "Gaussian boson sampling*, [arXiv:1905.12646](https://arxiv.org/abs/1905.12646) (2019); časopisecky jako "
    "*Measuring the similarity of graphs with a Gaussian boson sampler*, Physical Review A 101, 032314 (2020)"
)
JAHANGIRI_POINT_PROCESSES = Source(
    "Jahangiri, S., Arrazola, J. M., Quesada, N., Killoran, N.: *Point processes with Gaussian boson sampling*. "
    "Physical Review E 101, 022134 (2020), "
    "[doi:10.1103/PhysRevE.101.022134](https://doi.org/10.1103/PhysRevE.101.022134)"
)
SPARROW_VIBRATIONS = Source(
    "Sparrow, C. a kol.: *Simulating the vibrational quantum dynamics of molecules using photonics*. Nature 557, "
    "660–667 (2018), [doi:10.1038/s41586-018-0152-9](https://doi.org/10.1038/s41586-018-0152-9)"
)
BROMLEY_APPLICATIONS = Source(
    "Bromley, T. R. a kol.: *Applications of near-term photonic quantum computers: software and algorithms*. "
    "Quantum Science and Technology 5, 034010 (2020), "
    "[doi:10.1088/2058-9565/ab8504](https://doi.org/10.1088/2058-9565/ab8504)"
)
OWEN_MONTE_CARLO = Source(
    "Owen, A. B.: *Monte Carlo theory, methods and examples*, [online kniha](https://artowen.su.domains/mc/) "
    "(2013) – učebnice, ze které článek vychází u Monte Carla"
)
WIKIPEDIA_MULTI_INDEX = Source(
    "Wikipedia: [Multi-index notation](https://en.wikipedia.org/wiki/Multi-index_notation) – multiindexový zápis "
    "s příklady"
)
WIKIPEDIA_FORMAL_POWER_SERIES = Source(
    "Wikipedia: [Formal power series](https://en.wikipedia.org/wiki/Formal_power_series) – co znamená „formální“ "
    "mocninná řada"
)
WIKIPEDIA_MULTIVARIATE_NORMAL = Source(
    "Wikipedia: [Multivariate normal distribution](https://en.wikipedia.org/wiki/Multivariate_normal_distribution) "
    "– hustota, kovarianční matice a elipsy stejné hustoty"
)
WIKIPEDIA_FUBINI = Source(
    "Wikipedie: [Fubiniova věta](https://cs.wikipedia.org/wiki/Fubiniova_v%C4%9Bta) – kdy smíme zaměnit pořadí "
    "integrálů (a integrálu se součtem)",
    czech=True,
)

STRUCTURE_TOPIC = TheoryTopic(
    anchor="clanek-struktura",
    title="Jak je článek postavený a co číst nejdřív",
    in_short=(
        "Devadesát stran, ale jádro je na prvních patnácti: úvod se všemi hlavními větami, zadání úlohy a dva odhady "
        "GBS-I a GBS-P. Zbytek tvoří hlavně důkazy (s. 16–64), numerické příklady (s. 65–76) a přílohy."
    ),
    explanation=r"""
**Kdo a co.** Jørgen Ellegaard Andersen a Shan Shan z Center for Quantum Mathematics na University of Southern
Denmark. Článek ukazuje, že vzorky z Gaussian Boson Sampleru umějí odhadnout jistý typ gaussovských integrálů
s exponenciálně menším zaručeným počtem vzorků než obyčejné Monte Carlo – ovšem jen na části prostoru úloh. Na
článek navazuje druhý, který odhaduje, jak velká ta část je (arXiv:2502.19362).

**Oddíly článku (čísla stran podle PDF verze 2).**

| Oddíl | Strany | O čem je |
|:---|:---|:---|
| 1 Úvod | 1–7 | motivace, zadání úlohy, oba odhady a všechny hlavní věty 1.1–1.8 |
| 2 Background | 8–9 | Wickova věta a rozdělení výstupů GBS |
| 3 Two estimators | 10–15 | odhady GBS-I a GBS-P a jejich vlastnosti |
| 4 Guaranteed sample size | 16–33 | kolik vzorků zaručeně stačí; důkazy vět 1.1 a 1.2 |
| 5 Efficiency comparison | 34–64 | srovnání s Monte Carlem; důkazy exponenciální výhody |
| 6 Numerical examples | 65–76 | simulace na malých úlohách |
| Přílohy A–G | 77–87 | kód, hardware, celková cena výpočtu, těžkost úlohy, volba Monte Carla jako srovnání, boson sampling, lemmata |

**Jak číst (náš návrh).** Napoprvé úvod, oddíly 2 a 3 a numerické příklady v oddílu 6; z příloh B (jak úlohu
nahrát do hardwaru), D (proč je úloha klasicky těžká) a E (proč srovnávají s obyčejným Monte Carlem). Důkazy
v oddílech 4 a 5 až ve chvíli, kdy budeš chtít výsledky zobecňovat nebo kontrolovat – jednu chybu ve vzorci
druhého článku jsme už našli (viz stránka o Qpurpose).
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "komentovaný článek"),
        Reading(ANDERSEN_SHAN_ADVANTAGE, "navazující článek"),
    ),
)

MOTIVATION_TOPIC = TheoryTopic(
    anchor="clanek-motivace",
    title="Strana 2 nahoře: kde je GBS dnes a proč autoři hledají užitečnou úlohu",
    in_short=(
        "GBS už v experimentech předvedl kvantovou výhodu – ale jen v samotném losování, ne v užitečném výpočtu. "
        "Navržených aplikací je spousta, žádná však nemá důkaz, že porazí klasické metody. Autoři proto volí úlohu, "
        "u které výhodu dokázat jde."
    ),
    explanation=r"""
Odstavec navazuje na stranu 1: tam stojí, že GBS je speciální kvantový počítač a že losovat z jeho rozdělení je
pro klasický počítač prokazatelně těžké (Aaronson a Arkhipov; Hamilton a kol.; Kruse a kol.). Na straně 2 pak
přicházejí tři kroky.

**1. Experimenty (odkazy [22, 34, 35]).** Malé GBS přístroje s až 216 optickými módy už existují: 216 módů má
Borealis od kanadské firmy Xanadu (Madsen a kol. 2022), před ním byly čínské přístroje Jiuzhang (Zhong a kol. 2020
a 2021). *Mód* je jeden světelný kanál. Tyto experimenty předvedly *kvantovou výhodu* v úzkém smyslu: přístroj
losuje vzory fotonů z rozdělení, které klasický počítač v rozumném čase napodobit nedokáže. Nic užitečného tím
ale nespočítaly – a pozdější klasické algoritmy se jim přiblížily (Oh a kol. 2024).

**2. Časové kódování (odkazy [16, 23]).** Místo mnoha samostatných světelných cest na čipu jsou módy po sobě
jdoucí světelné pulzy v jednom vlákně; pulzy se potkávají ve smyčkách se zpožděním a tam interferují. Jedna smyčka
tak nahradí velkou síť děličů svazku, proto autoři mluví o škálovatelných přístrojích v blízké budoucnosti. Návrh
je od Motese a kol. (2014), experiment s jednotlivými fotony od He a kol. (2017); takhle funguje i Borealis.

**3. Navržené aplikace (odkazy [3–5, 9, 10, 17–19, 31]).** Každá využívá toho, že pravděpodobnosti GBS jsou
hafniány a hafnián počítá perfektní párování v grafu:

- *vibronická spektra molekul* – jak molekula pohlcuje světlo a přitom kmitá (Huh a kol. 2015; Huh a Yung 2017);
- *molekulární docking* – jak se molekula léčiva usadí v bílkovině, převedeno na hledání kliky v grafu
  (Banchi a kol. 2020);
- *husté podgrafy* – GBS losuje přednostně podgrafy s mnoha hranami (Arrazola a Bromley 2018);
- *perfektní párování* – počet perfektních párování grafu je hafnián jeho matice sousednosti (Brádler a kol. 2018);
- *stochastická optimalizace* – vzorky GBS jako chytře losovaní kandidáti řešení (Arrazola, Bromley, Rebentrost
  2018);
- *podobnost grafů* – četnosti vzorů jako „otisk prstu“ grafu (Brádler a kol. 2021; Schuld a kol. 2019);
- *bodové procesy* – náhodná rozmístění bodů, která mají sklon se shlukovat (Jahangiri a kol. 2020).

Malé experimenty a simulace dopadly slibně (Banchi a kol. 2020; Bromley a kol. 2020; Sparrow a kol. 2018).

**Pointa odstavce.** Pro žádnou z aplikací ale není teoreticky ověřené, že ve velkém porazí nejlepší klasickou
metodu, ba ani tu, se kterou ji autoři sami srovnávali (*baseline*). Zda GBS přinese výhodu u prakticky
zajímavých úloh, je tedy otevřená otázka. Andersen a Shan proto volí opačný postup: začnou úlohou, ve které
hafniány přirozeně vystupují – gaussovskými středními hodnotami polynomů –, a výhodu pro ni *dokážou*. Cenou je,
že srovnávají s obyčejným Monte Carlem, ne s nejlepší klasickou metodou (vysvětlují to v příloze E).
""",
    further_reading=(
        Reading(MADSEN, "Borealis, 216 módů, časové kódování"),
        Reading(ZHONG, "Jiuzhang"),
        Reading(ZHONG_2021, "Jiuzhang 2.0"),
        Reading(OH_CLASSICAL_SIMULATION, "klasická simulace experimentů"),
        Reading(MOTES_TIME_BIN, "návrh smyčkové architektury"),
        Reading(HE_TIME_BIN),
        Reading(HUH_VIBRONIC),
        Reading(HUH_YUNG_VIBRONIC),
        Reading(BANCHI_DOCKING),
        Reading(ARRAZOLA_BROMLEY),
        Reading(BRADLER),
        Reading(ARRAZOLA_OPTIMIZATION),
        Reading(BRADLER_ISOMORPHISM),
        Reading(SCHULD_GRAPH_KERNEL),
        Reading(JAHANGIRI_POINT_PROCESSES),
        Reading(SPARROW_VIBRATIONS),
        Reading(BROMLEY_APPLICATIONS, "přehled aplikací a softwaru"),
    ),
)

INTEGRAL_TOPIC = TheoryTopic(
    anchor="clanek-rovnice-1",
    title="Rovnice (1): úloha jako integrál, tedy vážený průměr",
    in_short=(
        r"$\mu_{\mathrm{Haf}} = \int f(x)\,h(x)\,\mathrm{d}x$ je průměr hodnoty $f$ přes všechny možné scénáře $x$, "
        r"kde každý scénář váží svou pravděpodobností $h(x)$. Monte Carlo ho odhaduje průměrem $f$ přes vylosované "
        "scénáře."
    ),
    explanation=r"""
$$
\mu_{\mathrm{Haf}} = \int_{\mathbb{R}^N} f(x)\,h(x)\,\mathrm{d}x
$$

**Po částech.**

- $x = (x_1, \dots, x_N)$ je jeden *scénář*: $N$ reálných čísel, třeba odchylky výnosů $N$ aktiv od jejich
  očekávání. $\mathbb{R}^N$ je množina všech takových scénářů.
- $h(x)$ je *hustota pravděpodobnosti*: říká, jak pravděpodobné jsou scénáře v okolí $x$ (rozbor v kapitole 5).
- $f(x)$ je hodnota, která nás ve scénáři $x$ zajímá – výplata, ztráta, mocnina výnosu (kapitola 4).
- $\mathrm{d}x = \mathrm{d}x_1 \cdots \mathrm{d}x_N$: integruje se přes všech $N$ souřadnic najednou.

**Proč je to průměr.** U kostky se střední hodnota počítá jako $\sum_{s} f(s)\,P(s)$: každý výsledek $s$ přispěje
svou hodnotou krát svou pravděpodobností. U spojitých veličin se součet mění na integrál a pravděpodobnost na
hustotu. Rovnice (1) je tedy obyčejná střední hodnota $\mathbb{E}[f(X)]$, jen zapsaná jako integrál.

**Proč to není snadné.** Integrál přes $N$ rozměrů nejde počítat na mřížce: deset bodů na každou osu dává
$10^N$ bodů. Monte Carlo místo toho vylosuje $n$ scénářů $X_1, \dots, X_n$ s hustotou $h$ a spočítá průměr
$\frac{1}{n}\sum_j f(X_j)$. Jeho chyba klesá jako $\sigma/\sqrt{n}$ bez ohledu na dimenzi, kde $\sigma$ je
směrodatná odchylka $f(X)$. U polynomů vysokého stupně je ale $\sigma$ obrovská, protože výsledek určují vzácné
extrémní scénáře – a právě tam chce článek ukázat výhodu GBS.

**Proč „Haf“ v názvu.** Pro polynom $f$ se integrál rovná váženému součtu hafniánů matice $B$ (rovnice (3),
kapitola 7) – odtud index $\mathrm{Haf}$.
""",
    further_reading=(
        Reading(OWEN_MONTE_CARLO, "kapitoly 1–2: Monte Carlo jako odhad integrálu"),
        Reading(GLASSERMAN, "Monte Carlo ve financích"),
    ),
)

POLYNOMIAL_TOPIC = TheoryTopic(
    anchor="clanek-polynom",
    title="Rovnice (2) nahoře: polynom zapsaný multiindexy",
    in_short=(
        r"$f(x) = \sum_{k=0}^{K} \sum_{|I|=k} a_I\,x^I$ je obyčejný polynom stupně nejvýš $K$ v $N$ proměnných. "
        r"Multiindex $I = (i_1, \dots, i_N)$ říká, na kolikátou je která proměnná; každý monom $x^I$ má vlastní "
        r"koeficient $a_I$. Pro $K = \infty$ je to nekonečná mocninná řada."
    ),
    explanation=r"""
**Multiindex.** $I = (i_1, \dots, i_N)$ je $N$ nezáporných celých čísel – exponent pro každou proměnnou. Platí

$$
x^I = x_1^{i_1}\, x_2^{i_2} \cdots x_N^{i_N}
$$

a

$$
|I| = i_1 + i_2 + \dots + i_N ,
$$

kde $|I|$ je *stupeň* monomu. Například pro $N = 3$ a $I = (2, 0, 1)$ je $x^I = x_1^2 x_3$ a $|I| = 3$.

**Dvojitý součet.** Vnější součet jde přes stupeň $k = 0, 1, \dots, K$, vnitřní přes všechny multiindexy daného
stupně. Dohromady se sečtou všechny monomy stupně nejvýš $K$, každý se svým koeficientem $a_I \in \mathbb{R}$.
Pro $N = 2$ a $K = 2$:

$$
\begin{aligned}
f(x) = {} & a_{(0,0)} + a_{(1,0)}\,x_1 + a_{(0,1)}\,x_2 \\
& + a_{(2,0)}\,x_1^2 + a_{(1,1)}\,x_1 x_2 \\
& + a_{(0,2)}\,x_2^2 .
\end{aligned}
$$

**Příklad z financí.** Portfolio s vahami 0,6 a 0,4 má výnos $L = 0{,}6\,x_1 + 0{,}4\,x_2$. Jeho druhá mocnina

$$
L^2 = 0{,}36\,x_1^2 + 0{,}48\,x_1 x_2 + 0{,}16\,x_2^2
$$

je polynom s $a_{(2,0)} = 0{,}36$, $a_{(1,1)} = 0{,}48$, $a_{(0,2)} = 0{,}16$ a ostatními koeficienty nulovými;
$\mathbb{E}[L^2]$ je rozptyl výnosu portfolia. Vyšší mocniny $L^d$ (šikmost, špičatost, chvosty) dávají polynomy
vyššího stupně – to je úloha stránky „Monte Carlo na GBS“.

**Kolik je koeficientů.** Monomů stupně nejvýš $K$ v $N$ proměnných je $\binom{N+K}{K}$; pro $N = 2$, $K = 2$
právě šest. Počet roste rychle – pro 20 proměnných a stupeň 8 je to už 3 108 105 koeficientů (tabulka níže).
Úloha je tedy dána čtveřicí $N$, $K$, matice $B$ a všech koeficientů $a_I$.

**$K < \infty$ nebo $K = \infty$.** Konečné $K$ znamená polynom. Pro $K = \infty$ je $f$ *formální mocninná
řada*: nekonečný součet monomů, například $e^{x_1} = \sum_{k} x_1^k / k!$. Slovo *formální* znamená, že řadu
zatím bereme jen jako zápis a neříkáme nic o tom, jestli konverguje. Hladké funkce (třeba výplaty) se do takové
řady rozvíjejí Taylorovým rozvojem. Kdy pak má integrál (1) smysl, řeší podmínka (A1) v kapitole 7.
""",
    further_reading=(
        Reading(WIKIPEDIA_MULTI_INDEX),
        Reading(WIKIPEDIA_FORMAL_POWER_SERIES),
    ),
)

DENSITY_TOPIC = TheoryTopic(
    anchor="clanek-hustota",
    title="Rovnice (2) dole: hustota normálního rozdělení h(x)",
    in_short=(
        r"$h(x) = (2\pi)^{-N/2}(\det B)^{-1/2}\exp\!\big(-\tfrac{1}{2}x^\top B^{-1}x\big)$ je zvonová křivka "
        r"v $N$ rozměrech. Exponenciála určuje tvar (čím dál od nuly, tím méně pravděpodobné), konstanta před ní "
        r"zajistí, že celková pravděpodobnost je 1. Matice $B$ je kovarianční matice."
    ),
    explanation=r"""
$$
\begin{aligned}
h(x) = {} & (2\pi)^{-N/2}\,(\det B)^{-1/2} \\
& \cdot \exp\!\Big(-\frac{1}{2}\,x^\top B^{-1} x\Big)
\end{aligned}
$$

**Zprava doleva.**

- $x^\top B^{-1} x = \sum_{i,j} x_i\,(B^{-1})_{ij}\,x_j$ je jedno číslo, *kvadratická forma*. Měří, jak daleko je
  scénář $x$ od nuly, když vezmeme v úvahu rozptyly a korelace (druhá mocnina tzv. Mahalanobisovy vzdálenosti).
- $\exp(-\tfrac{1}{2}\cdot)$ dělá ze vzdálenosti hustotu: v nule je největší a se vzdáleností klesá. Body se
  stejnou hustotou leží na elipsách (v $N$ rozměrech na elipsoidech), jejichž osy jsou vlastní vektory $B$.
- $(2\pi)^{-N/2}(\det B)^{-1/2}$ je *normovací konstanta*: vybere výšku zvonu tak, aby $\int h(x)\,\mathrm{d}x = 1$.
  Determinant $\det B$ měří „objem“ rozptylu: čím větší rozptyl, tím širší a nižší zvon.

**Kontrola pro $N = 1$.** Je-li $B = \sigma^2$, dostaneme známou hustotu

$$
h(x) = \frac{1}{\sqrt{2\pi\sigma^2}}\;e^{-x^2/(2\sigma^2)} .
$$

**Proč je $B$ reálná, symetrická a pozitivně definitní.**

- *Reálná*, protože proměnné $x_i$ jsou reálné.
- *Symetrická*, protože $B_{ij} = \mathrm{cov}(X_i, X_j) = \mathrm{cov}(X_j, X_i) = B_{ji}$.
- *Pozitivně definitní*, tedy $w^\top B w > 0$ pro každé nenulové $w$: každá kombinace $w^\top X$ (třeba výnos
  portfolia s vahami $w$) má kladný rozptyl. Jinak by neexistovaly $B^{-1}$ ani $(\det B)^{-1/2}$ – například
  dvě dokonale korelovaná aktiva dávají singulární matici.

**Proč nulová střední hodnota.** Neubírá na obecnosti: má-li $X$ střední hodnotu $m$, je $X = m + Y$ s $Y$
s nulovou střední hodnotou a $f(m + Y)$ je zase polynom stejného stupně v $Y$. Ve financích to znamená počítat
s odchylkami výnosů od očekávání.

**Co přijde na straně 3.** Aby šla matice nahrát do GBS, musí mít vlastní čísla menší než 1; v praxi se $B$
vhodně přeškáluje. Proto mají příklady na této stránce $B$ s rozptyly 0,5 a kovariancí 0,25 (vlastní čísla 0,75
a 0,25).
""",
    further_reading=(
        Reading(WIKIPEDIA_MULTIVARIATE_NORMAL),
        Reading(ANDEL_STATISTICS, "vícerozměrné normální rozdělení"),
        Reading(WIKIPEDIA_COVARIANCE),
    ),
)

EXPECTATION_TOPIC = TheoryTopic(
    anchor="clanek-stredni-hodnota",
    title="Komplexní f, střední hodnota E[f(X)] a značení",
    in_short=(
        r"Komplexní $f$ se rozdělí na reálnou a imaginární část, takže stačí řešit reálné úlohy. Z pohledu "
        r"pravděpodobnosti je $\mu_{\mathrm{Haf}} = \mathbb{E}[f(X)]$ pro $X$ s hustotou $h$, pokud je výsledek "
        r"konečný. $I_{\mathrm{Haf}}$ je jméno úlohy, $\mu_{\mathrm{Haf}}$ její řešení."
    ),
    explanation=r"""
**Komplexní $f$.** Je-li $f = u + \mathrm{i}\,v$ s reálnými funkcemi $u$ a $v$, je
$\int f h = \int u h + \mathrm{i}\int v h$. Jedna komplexní úloha jsou tedy dvě reálné, a článek proto dál počítá
jen s reálnými koeficienty $a_I$. Nezaměňovat s přílohou F: tam jsou komplexní samotné proměnné $z$, místo
hafniánů vycházejí permanenty a úloha souvisí s boson samplingem z jednotlivých fotonů (viz stránka o Quandele).

**Pravděpodobnostní pohled.** Má-li náhodný vektor $X$ hustotu $h$, je $\mu_{\mathrm{Haf}} = \mathbb{E}[f(X)]$.
Dvě technické podmínky z textu:

- *$f$ je měřitelná* – zaručuje, že $f(X)$ je náhodná veličina. Všechny spojité funkce, tedy i polynomy, měřitelné
  jsou; v praxi to není omezení.
- *$|\mu_{\mathrm{Haf}}| < \infty$* – střední hodnota musí být konečná, jinak úloha nemá řešení. Například pro
  $N = 1$, $B = 1$ a $f(x) = e^{x^2}$ je $\int e^{x^2} e^{-x^2/2}\,\mathrm{d}x / \sqrt{2\pi} = \infty$, protože
  integrand roste do nekonečna.

**Značení.** $I_{\mathrm{Haf}}$ je *jméno úlohy* („pro dané $N$, $K$, $a_I$ a $B$ spočítej integrál (1)“),
$\mu_{\mathrm{Haf}}$ je *její řešení*, jedno číslo. Na straně 3 přibudou varianty: $I^\times_{\mathrm{Haf}}(\epsilon,
\delta)$ je stejná úloha s požadovanou přesností a $I_{\mathrm{Haf}^2}$ rodina úloh s hafniány na druhou
(kapitola 8).
""",
    further_reading=(
        Reading(ANDEL_STATISTICS, "střední hodnota a měřitelnost"),
    ),
)

CONDITION_TOPIC = TheoryTopic(
    anchor="clanek-podminka-a1",
    title="Podmínka (A1): kdy smíme integrovat člen po členu",
    in_short=(
        r"(A1) chce, aby byl konečný integrál ze součtu *absolutních hodnot* všech členů. Pak $\mu_{\mathrm{Haf}}$ "
        r"existuje a integrál se smí počítat člen po členu (Fubiniova věta). Z Wickovy věty pak vyjde "
        r"$\mu_{\mathrm{Haf}} = \sum a_I\,\mathrm{Haf}(B_I)$. U polynomů platí vždy, u nekonečných řad ne."
    ),
    explanation=r"""
**Podmínka (A1):**

$$
\int_{\mathbb{R}^N} \sum_{k=0}^{K} \sum_{|I|=k} \big|a_I\,x^I\big|\, h(x)\,\mathrm{d}x < \infty
$$

**Rozdíl oproti (1).** Uvnitř jsou absolutní hodnoty: sčítají se velikosti všech členů a nic se navzájem
nevyruší. (A1) tedy říká, že ani „celková hmota“ všech členů dohromady není nekonečná.

**Co z ní plyne (věta pokračuje na straně 3).**

1. *Trojúhelníková nerovnost:* $|\mu_{\mathrm{Haf}}| \le \int \sum |a_I x^I|\,h < \infty$, takže řešení existuje.
2. *Fubiniova věta* (pro součet a integrál): smíme prohodit pořadí, tedy integrovat člen po členu,

$$
\mu_{\mathrm{Haf}} = \sum_{k=0}^{K} \sum_{|I|=k} a_I \int x^I h(x)\,\mathrm{d}x ,
$$

tedy

$$
\mu_{\mathrm{Haf}} = \sum_{k=0}^{K} \sum_{|I|=k} a_I\,\mathbb{E}\big[X^I\big] .
$$

U nekonečné řady to bez (A1) obecně neplatí: součet integrálů nemusí konvergovat, nebo může vyjít jinak než
integrál součtu.

**U polynomů je (A1) zadarmo.** Součet je konečný a normální rozdělení má všechny momenty konečné, takže každý
člen $\mathbb{E}|a_I X^I|$ je konečný.

**Dvě nekonečné řady pro $N = 1$, $B = 1$** (tabulka níže sčítá prvních deset členů):

- $\cosh x = \sum_k x^{2k}/(2k)!$ – všechny členy jsou nezáporné a $\mathbb{E}[\cosh X] = e^{1/2} \approx 1{,}649$,
  takže (A1) platí. Člen po členu: $\mathbb{E}[X^{2k}] = (2k-1)!!$, tedy
  $\sum_k (2k-1)!!/(2k)! = \sum_k 1/(2^k k!) = e^{1/2}$ – stejný výsledek.
- $e^{x^2} = \sum_k x^{2k}/k!$ – integrál je nekonečný, (A1) neplatí a částečné součty člen po členu rostou nade
  všechny meze.

**Odtud rovnice (3) a název.** Podle Wickovy (Isserlisovy) věty je $\mathbb{E}[X^I] = \mathrm{Haf}(B_I)$ pro sudé
$|I|$ a nula pro liché, kde $B_I$ vznikne z $B$ zopakováním $j$-tého řádku a sloupce $i_j$-krát. Proto

$$
\mu_{\mathrm{Haf}} = \sum_{k=0}^{K} \sum_{|I|=2k} a_I\,\mathrm{Haf}(B_I) .
$$

Liché členy autoři vynechali, protože střední hodnota liché funkce normálního rozdělení s nulovou střední hodnotou
je nula ($X$ a $-X$ jsou stejně pravděpodobné).

**Příklad.** Pro $B$ s rozptyly 0,5 a kovariancí 0,25 a $I = (2, 2)$ je $B_I$ matice $4 \times 4$ a

$$
\begin{aligned}
\mathbb{E}[X_1^2 X_2^2] &= \mathrm{Haf}(B_I) \\
&= B_{11}B_{22} + 2B_{12}^2 = 0{,}375 .
\end{aligned}
$$

Pro portfolio z kapitoly 4 je $\mathbb{E}[L^2] = 0{,}36\,B_{11} + 0{,}48\,B_{12} + 0{,}16\,B_{22} = 0{,}38$,
protože hafnián matice $2 \times 2$ je její mimodiagonální prvek.
""",
    further_reading=(
        Reading(WIKIPEDIA_FUBINI),
        Reading(ISSERLIS),
        Reading(WICK),
        Reading(WIKIPEDIA_HAFNIAN, "hafnián a Wickova věta s příklady"),
    ),
)

NEXT_STEPS_TOPIC = TheoryTopic(
    anchor="clanek-co-dal",
    title="Kam to vede: strana 3 a dál",
    in_short=(
        r"Na straně 3 autoři chtějí vlastní čísla $B$ menší než 1, zavedou přesnost jako $(\epsilon, \delta)$ "
        r"a rodinu $I_{\mathrm{Haf}^2}$ s hafniány na druhou, kterou řeší odhad GBS-I. Druhý odhad, GBS-P, řeší "
        "přímo původní úlohu."
    ),
    explanation=r"""
**Vlastní čísla $B$ pod 1.** Přístroj umí nahrát jen takové matice; vysvětlení je v teorii ke stránce „Monte Carlo na
GBS“ (Nahrání $\Sigma$ do zařízení).

**Přesnost $(\epsilon, \delta)$, rovnice (4).** Hledá se odhad $e$, pro který
$P\big(|\mu_{\mathrm{Haf}} - e| > \epsilon\,|\mu_{\mathrm{Haf}}|\big) < \delta$. Pro $\epsilon = 0{,}01$
a $\delta = 0{,}05$: s pravděpodobností aspoň 95 % je relativní chyba nejvýš 1 %. *Zaručený počet vzorků* je
počet, od kterého to platí; přesně v něm se GBS a Monte Carlo v článku srovnávají.

**Rodina $I_{\mathrm{Haf}^2}$, rovnice (5)–(7).** Proměnné se zdvojí na $(p, q)$ s kovarianční maticí
$B \oplus B$ a polynom má tvar $\sum a_I\,p^I q^I$. Wickova věta pak dá
$\mu_{\mathrm{Haf}^2} = \sum a_I\,\mathrm{Haf}(B_I)^2$ – a protože GBS losuje vzor $I$ s pravděpodobností úměrnou
$\mathrm{Haf}(B_I)^2$, řeší tuto rodinu vážený výběr GBS-I přímo. Druhý odhad, GBS-P, odmocňuje četnosti a míří na
původní $\mu_{\mathrm{Haf}}$.

**Příloha F a boson sampling.** Pro komplexní proměnné vycházejí místo hafniánů permanenty a autoři píší, že
obdobné výsledky pro boson sampling s jednotlivými fotony ukážou v samostatné práci. To je cesta, kterou by šlo
použít na hardwaru Quandely.
""",
    further_reading=(
        Reading(HAMILTON, "proč jsou pravděpodobnosti GBS hafniány na druhou"),
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "strany 3–7 a příloha F"),
    ),
)

TOPICS: Tuple[TheoryTopic, ...] = (
    STRUCTURE_TOPIC,
    MOTIVATION_TOPIC,
    INTEGRAL_TOPIC,
    POLYNOMIAL_TOPIC,
    DENSITY_TOPIC,
    EXPECTATION_TOPIC,
    CONDITION_TOPIC,
    NEXT_STEPS_TOPIC,
)

KEY_FINDINGS: Tuple[KeyFinding, ...] = (
    KeyFinding(
        "**Motivace:** GBS umí kvantovou výhodu v samotném losování, ale u žádné navržené aplikace není dokázané, "
        "že porazí klasické metody. Autoři proto volí úlohu, kde výhodu dokázat jde.",
        MOTIVATION_TOPIC.anchor,
    ),
    KeyFinding(
        r"**Rovnice (1) je střední hodnota** $\mathbb{E}[f(X)]$: průměr $f$ přes všechny scénáře vážený jejich "
        "pravděpodobností. Monte Carlo ji odhaduje průměrem přes vylosované scénáře.",
        INTEGRAL_TOPIC.anchor,
    ),
    KeyFinding(
        r"**$f$ je polynom v multiindexovém zápisu**, $x^I = x_1^{i_1} \cdots x_N^{i_N}$. Koeficientů je "
        f"$\\binom{{N+K}}{{K}}$ – pro 20 proměnných a stupeň 8 už {COEFFICIENT_COUNT_EXAMPLE}.",
        POLYNOMIAL_TOPIC.anchor,
    ),
    KeyFinding(
        r"**$h$ je hustota normálního rozdělení** s nulovou střední hodnotou a kovarianční maticí $B$; konstanta "
        "před exponenciálou jen zajistí, že celková pravděpodobnost je 1.",
        DENSITY_TOPIC.anchor,
    ),
    KeyFinding(
        r"**Podmínka (A1)** dovolí integrovat člen po členu; z Wickovy věty pak vyjde "
        r"$\mu_{\mathrm{Haf}} = \sum a_I\,\mathrm{Haf}(B_I)$ – odtud „Haf“. U polynomů platí vždy.",
        CONDITION_TOPIC.anchor,
    ),
)
