"""Texts of the random matrix page: from quantum chaos to cleaning the correlation matrix of a portfolio."""

from __future__ import annotations

from typing import Tuple

from randommatrix.marchenko_pastur import NoiseBand
from randommatrix.min_variance import predicted_in_sample, predicted_out_of_sample
from ui.theory_content import Reading, Source, TheoryTopic

SOURCES_ANCHOR = "nahodne-matice-zdroje"
LAB_ANCHOR = "nahodne-matice-laborator"
SOURCES_CHECKED_DATE = "18. 10. 2026"

EXAMPLE_RATIO = 0.5
EXAMPLE_IN_SAMPLE = predicted_in_sample(EXAMPLE_RATIO)
EXAMPLE_OUT_OF_SAMPLE = predicted_out_of_sample(EXAMPLE_RATIO)
BAND_EXAMPLE_ASSETS = 400
BAND_EXAMPLE_OBSERVATIONS = 1000
BAND_EXAMPLE = NoiseBand(BAND_EXAMPLE_ASSETS / BAND_EXAMPLE_OBSERVATIONS)


def czech_decimal(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}".replace(".", ",")


def _band_example() -> str:
    observations = f"{BAND_EXAMPLE_OBSERVATIONS:,}".replace(",", " ")
    ratio = czech_decimal(BAND_EXAMPLE.ratio, 1).replace(",", "{,}")
    upper = czech_decimal(BAND_EXAMPLE.upper)
    return (
        f"**Příklad.** Pro {BAND_EXAMPLE_ASSETS} akcií a {observations} dní (asi čtyři roky) je $q = {ratio}$ "
        f"a pás sahá od {czech_decimal(BAND_EXAMPLE.lower)} do {upper}, přestože pravá vlastní čísla jsou všechna "
        f"rovna jedné. Největší „náhodný faktor“ tedy vysvětluje {upper}krát víc rozptylu, než by měl – a nic "
        "neznamená.\n"
    )


BOHIGAS_GIANNONI_SCHMIT = Source(
    "Bohigas, O., Giannoni, M. J., Schmit, C.: *Characterization of chaotic quantum spectra and universality of "
    "level fluctuation laws*. Physical Review Letters 52 (1984), 1–4, "
    "[doi:10.1103/PhysRevLett.52.1](https://doi.org/10.1103/PhysRevLett.52.1)"
)
GUHR_REVIEW = Source(
    "Guhr, T., Müller-Groeling, A., Weidenmüller, H. A.: *Random-matrix theories in quantum physics: common "
    "concepts*. Physics Reports 299 (1998), 189–425, "
    "[doi:10.1016/S0370-1573(97)00088-4](https://doi.org/10.1016/S0370-1573(97)00088-4), "
    "[arXiv:cond-mat/9707301](https://arxiv.org/abs/cond-mat/9707301)"
)
MARCHENKO_PASTUR = Source(
    "Marčenko, V. A., Pastur, L. A.: *Distribution of eigenvalues for some sets of random matrices*. "
    "Matematičeskij sbornik 72(114) (1967), 507–536; anglicky Mathematics of the USSR-Sbornik 1 (1967), 457–483, "
    "[doi:10.1070/SM1967v001n04ABEH001994](https://doi.org/10.1070/SM1967v001n04ABEH001994)"
)
LALOUX_1999 = Source(
    "Laloux, L., Cizeau, P., Bouchaud, J.-P., Potters, M.: *Noise dressing of financial correlation matrices*. "
    "Physical Review Letters 83 (1999), 1467–1470, "
    "[doi:10.1103/PhysRevLett.83.1467](https://doi.org/10.1103/PhysRevLett.83.1467), "
    "[arXiv:cond-mat/9810255](https://arxiv.org/abs/cond-mat/9810255)"
)
PLEROU_1999 = Source(
    "Plerou, V., Gopikrishnan, P., Rosenow, B., Amaral, L. A. N., Stanley, H. E.: *Universal and nonuniversal "
    "properties of cross correlations in financial time series*. Physical Review Letters 83 (1999), 1471–1474, "
    "[doi:10.1103/PhysRevLett.83.1471](https://doi.org/10.1103/PhysRevLett.83.1471), "
    "[arXiv:cond-mat/9902283](https://arxiv.org/abs/cond-mat/9902283)"
)
BOUCHAUD_POTTERS_REVIEW = Source(
    "Bouchaud, J.-P., Potters, M.: *Financial applications of random matrix theory: a short review*. "
    "In: Akemann, G., Baik, J., Di Francesco, P. (ed.): The Oxford Handbook of Random Matrix Theory, Oxford "
    "University Press 2011, [arXiv:0910.1205](https://arxiv.org/abs/0910.1205) – vzorce pro riziko v oddílu II C"
)
PAFKA_KONDOR = Source(
    "Pafka, S., Kondor, I.: *Noisy covariance matrices and portfolio optimization II*. Physica A 319 (2003), "
    "487–494, [doi:10.1016/S0378-4371(02)01499-1](https://doi.org/10.1016/S0378-4371(02)01499-1), "
    "[arXiv:cond-mat/0205119](https://arxiv.org/abs/cond-mat/0205119)"
)
LEDOIT_WOLF_2004 = Source(
    "Ledoit, O., Wolf, M.: *A well-conditioned estimator for large-dimensional covariance matrices*. Journal of "
    "Multivariate Analysis 88 (2004), 365–411, "
    "[doi:10.1016/S0047-259X(03)00096-4](https://doi.org/10.1016/S0047-259X(03)00096-4)"
)
LEDOIT_WOLF_2012 = Source(
    "Ledoit, O., Wolf, M.: *Nonlinear shrinkage estimation of large-dimensional covariance matrices*. Annals of "
    "Statistics 40 (2012), 1024–1060, [doi:10.1214/12-AOS989](https://doi.org/10.1214/12-AOS989)"
)
LEDOIT_WOLF_2020 = Source(
    "Ledoit, O., Wolf, M.: *Analytical nonlinear shrinkage of large-dimensional covariance matrices*. Annals of "
    "Statistics 48 (2020), 3043–3065, [doi:10.1214/19-AOS1921](https://doi.org/10.1214/19-AOS1921)"
)
BUN_BOUCHAUD_POTTERS = Source(
    "Bun, J., Bouchaud, J.-P., Potters, M.: *Cleaning large correlation matrices: tools from random matrix "
    "theory*. Physics Reports 666 (2017), 1–109, "
    "[doi:10.1016/j.physrep.2016.10.005](https://doi.org/10.1016/j.physrep.2016.10.005), "
    "[arXiv:1610.08104](https://arxiv.org/abs/1610.08104)"
)
MUNNIX_2012 = Source(
    "Münnix, M. C., Shimada, T., Schäfer, R., Leyvraz, F., Seligman, T. H., Guhr, T., Stanley, H. E.: "
    "*Identifying states of a financial market*. Scientific Reports 2 (2012), 644, "
    "[doi:10.1038/srep00644](https://doi.org/10.1038/srep00644), [arXiv:1202.1623](https://arxiv.org/abs/1202.1623)"
)
KRITZMAN_2011 = Source(
    "Kritzman, M., Li, Y., Page, S., Rigobon, R.: *Principal components as a measure of systemic risk*. Journal "
    "of Portfolio Management 37 (2011), č. 4, 112–126, "
    "[doi:10.3905/jpm.2011.37.4.112](https://doi.org/10.3905/jpm.2011.37.4.112)"
)
CILIBERTI_KONDOR_MEZARD = Source(
    "Ciliberti, S., Kondor, I., Mézard, M.: *On the feasibility of portfolio optimization under expected "
    "shortfall*. Quantitative Finance 7 (2007), 389–396, "
    "[doi:10.1080/14697680701422089](https://doi.org/10.1080/14697680701422089), "
    "[arXiv:physics/0606015](https://arxiv.org/abs/physics/0606015)"
)
KONDOR_PAFKA_NAGY = Source(
    "Kondor, I., Pafka, S., Nagy, G.: *Noise sensitivity of portfolio selection under various risk measures*. "
    "Journal of Banking & Finance 31 (2007), 1545–1573, "
    "[doi:10.1016/j.jbankfin.2006.12.003](https://doi.org/10.1016/j.jbankfin.2006.12.003), "
    "[arXiv:physics/0611027](https://arxiv.org/abs/physics/0611027)"
)
BASEL_FRTB = Source(
    "Basel Committee on Banking Supervision: *Minimum capital requirements for market risk* (leden 2019), "
    "[bis.org/bcbs/publ/d457](https://www.bis.org/bcbs/publ/d457.htm); hladina 97,5 % v odstavci "
    "[MAR33.3](https://www.bis.org/basel_framework/chapter/MAR/33.htm)"
)
HSIEH_1991 = Source(
    "Hsieh, D. A.: *Chaos and nonlinear dynamics: application to financial markets*. Journal of Finance 46 "
    "(1991), 1839–1877, [doi:10.1111/j.1540-6261.1991.tb04646.x](https://doi.org/10.1111/j.1540-6261.1991.tb04646.x)"
)
BDS_1996 = Source(
    "Brock, W. A., Dechert, W. D., Scheinkman, J. A., LeBaron, B.: *A test for independence based on the "
    "correlation dimension*. Econometric Reviews 15 (1996), 197–235, "
    "[doi:10.1080/07474939608800353](https://doi.org/10.1080/07474939608800353)"
)
BASS_PREDICTORS = Source(
    "Bass, T. A.: *The Predictors: How a Band of Maverick Physicists Used Chaos Theory to Trade Their Way to a "
    "Fortune on Wall Street*. Henry Holt, New York 1999"
)
WIKIPEDIA_PREDICTION_COMPANY = Source(
    "Wikipedia: [Prediction Company](https://en.wikipedia.org/wiki/Prediction_Company)"
)
WIKIPEDIA_RANDOM_MATRIX = Source(
    "Wikipedie: [Vlastní číslo](https://cs.wikipedia.org/wiki/Vlastn%C3%AD_%C4%8D%C3%ADslo), "
    "[Korelace](https://cs.wikipedia.org/wiki/Korelace)",
    czech=True,
)

LEAD = (
    "Teorie náhodných matic je nejlépe doložený most mezi kvantovým chaosem a řízením portfolií. Vznikla pro "
    "spektra těžkých jader a chaotických kvantových systémů. Od roku 1999 se s ní měří, kolik z korelační matice "
    "akcií je skutečná informace a kolik šum z krátké historie. Na stránce je laboratoř se syntetickým trhem, "
    "výklad krok za krokem a literatura; citace jsme ověřili "
    f"{SOURCES_CHECKED_DATE}. Vlastní odhady jsou tak označené."
)

IN_SHORT = (
    "Když odhadneš korelace N akcií z T dní, většina vlastních čísel matice vypadá přesně jako u čistého šumu. "
    "Markowitzova optimalizace se na ten šum „přisaje“: portfolio slibuje menší riziko, než skutečně nese. "
    "Při poměru q = N/T = 0,5 slibuje polovinu nejmenšího možného rozptylu a dodá dvojnásobek. Teorie "
    "náhodných matic řekne, která vlastní čísla jsou šum, a dovolí matici vyčistit."
)

LAB_INTRO = (
    "Simulujeme trh, u kterého pravdu známe: každá akcie má jednotkový rozptyl, korelaci 0,25 s celým trhem "
    "a dalších 0,16 se svým sektorem (sektorů je {sector_count}). Z T dní spočítáme výběrovou korelační matici, "
    "porovnáme její spektrum s čistým šumem a postavíme z ní portfolio s minimálním rozptylem. Protože pravou "
    "matici známe, vidíme, jaké riziko portfolio slibuje a jaké skutečně nese. Stejně to dopadne s dvěma "
    "vyčištěnými odhady matice."
)

SPECTRUM_HINT = (
    "Fialová křivka je Marčenkovo–Pasturovo rozdělení: tak by vypadala vlastní čísla, kdyby akcie byly "
    "nezávislé a veškerá korelace jen náhoda z konečné historie. Jeho rozptyl σ² odhadujeme jen z dat jako "
    "1 − λ_max/N, tedy bez znalosti pravdy. Sloupce nad čárkovanou mezí λ₊ nese informaci: sektory a daleko "
    "vpravo tržní mód. Všechno pod ní je od šumu nerozlišitelné."
)

RISK_TABLE_HINT = (
    "Rozptyly jsou vztažené k nejmenšímu možnému rozptylu, tedy k portfoliu postavenému z pravé matice. "
    "Slíbený rozptyl je to, co ukáže backtest na stejných datech; skutečný je to, co portfolio ponese dál. "
    "Poslední sloupec říká, kolikrát je riziko podhodnocené."
)

SWEEP_HINT = (
    "Pro {asset_count} akcií a různé délky historie, průměr z {repetitions} simulací v každém bodě. Fialové čáry "
    "jsou předpověď teorie náhodných matic pro surovou matici v limitě velkého N: slíbený rozptyl 1 − q "
    "a skutečný 1/(1 − q). Prázdná kolečka a modrá čára jsou simulace stejné surové matice."
)

ORIGINS = TheoryTopic(
    anchor="nm-kvantovy-chaos",
    title="Odkud náhodné matice pocházejí: kvantový chaos",
    in_short=(
        "Spektra složitých kvantových systémů mají univerzální statistiku, kterou popisují vlastní čísla "
        "náhodných matic. Pro chaotické systémy to v roce 1984 vyslovili Bohigas, Giannoni a Schmit."
    ),
    explanation=r"""
**Proč náhodná matice.** Hamiltonián těžkého jádra nikdo nezná přesně. Wigner v 50. letech navrhl nahradit ho
náhodnou symetrickou maticí a ptát se jen na statistické vlastnosti spektra – třeba jak daleko od sebe bývají
sousední hladiny. Ukázalo se, že tyto statistiky jsou *univerzální*: nezávisí na detailech, jen na symetrii
systému.

**Hypotéza BGS.** Bohigas, Giannoni a Schmit (1984) vyslovili domněnku, že stejnou statistiku mají kvantové
systémy, jejichž klasická obdoba je chaotická (jejich příklad byl Sinajův kulečník). Integrabilní systémy mají
naopak hladiny nezávislé jako Poissonův proces. Statistika spektra je tak „otisk“ chaosu v kvantové mechanice;
celý obor shrnuje přehled Guhra, Müllera-Groelinga a Weidenmüllera (1998).

**Co si odnést do financí.** Dvě myšlenky. Zaprvé: velká matice, o které nic nevíme, se chová jako náhodná
a její spektrum má známý tvar. Zadruhé: odchylky od toho tvaru jsou informace. Přesně tak se o patnáct let
později začalo číst spektrum korelační matice akcií.
""",
    further_reading=(
        Reading(BOHIGAS_GIANNONI_SCHMIT, "hypotéza, že chaotické kvantové systémy mají statistiku náhodných matic"),
        Reading(GUHR_REVIEW, "velký přehled teorie náhodných matic v kvantové fyzice"),
        Reading(WIKIPEDIA_RANDOM_MATRIX, "česky: vlastní čísla a korelace"),
    ),
)

MARCHENKO_PASTUR_TOPIC = TheoryTopic(
    anchor="nm-marcenko-pastur",
    title="Marčenkovo–Pasturovo rozdělení: jak vypadá čistý šum",
    in_short=(
        "I úplně nezávislé akcie ukážou v konečné historii náhodné korelace. Vlastní čísla takové matice "
        "vyplní pás, jehož šířku určuje jen poměr q = N/T."
    ),
    explanation=r"""
**Úloha.** Máme N akcií a T denních výnosů, z nich spočítáme výběrovou korelační matici $E$. Kdyby akcie byly
nezávislé, pravá matice je jednotková a všechna její vlastní čísla jsou 1. Výběrová matice ale z konečných dat
vyjde „rozmazaná“: vlastní čísla se rozprostřou kolem jedničky.

**Výsledek.** Marčenko a Pastur (1967) spočítali tvar toho rozmazání v limitě, kdy N i T rostou a poměr
$q = N/T$ je pevný. Vlastní čísla leží v pásu

$$
\lambda_\pm = \sigma^2 \left(1 \pm \sqrt{q}\right)^2 ,
$$

kde $\sigma^2$ je rozptyl šumu (u nezávislých akcií 1). Hustota uvnitř pásu je

$$
\rho(\lambda) = \frac{\sqrt{(\lambda_+ - \lambda)(\lambda - \lambda_-)}}{2 \pi q \sigma^2 \lambda} .
$$

""" + _band_example() + r"""
**Proč je to užitečné.** Vlastní číslo výrazně nad $\lambda_+$ šum vyrobit nedokáže, takže nese informaci. Vše
uvnitř pásu je od šumu nerozlišitelné. V laboratoři výše je to vidět na histogramu.
""",
    further_reading=(
        Reading(MARCHENKO_PASTUR, "původní odvození"),
        Reading(BUN_BOUCHAUD_POTTERS, "kapitola o Marčenkově–Pasturově zákonu s finančními příklady"),
    ),
)

EMPIRICAL = TheoryTopic(
    anchor="nm-empirie",
    title="Co ukázala skutečná data (1999)",
    in_short=(
        "Dva týmy fyziků nezávisle ukázaly, že většina vlastních čísel korelační matice amerických akcií leží "
        "v pásu šumu. Informaci nese jen tržní mód a několik dalších největších vlastních čísel."
    ),
    explanation=r"""
**Laloux, Cizeau, Bouchaud a Potters (1999)** vzali denní výnosy 406 akcií z indexu S&P 500 za roky 1991–1996
(1 309 dní, tedy $q \approx 0{,}31$) a porovnali spektrum jejich korelační matice s Marčenkovým–Pasturovým
rozdělením. S rozptylem šumu $\sigma^2 = 0{,}74$ (proložený) vysvětlí rozdělení 94 % spektra; jen 6 %
největších vlastních čísel leží nad pásem a nese 26 % celkové volatility. Největší vlastní číslo, tržní mód,
je asi 25krát větší než horní mez šumu.

**Plerou, Gopikrishnan, Rosenow, Amaral a Stanley (1999)** použili 30minutové výnosy 1 000 největších
amerických akcií z let 1994–1995. Statistika většiny vlastních čísel podle nich odpovídá náhodné matici
(gaussovskému ortogonálnímu souboru, stejnému jako u chaotických kvantových systémů); odchylky mají jen
některá z největších vlastních čísel.

**Proč to bylo překvapení.** Markowitzova teorie i rizikové modely bank berou korelační matici jako známou.
Tyto práce ukázaly, že při běžné délce historie je z ní většina šum – a že teorie náhodných matic umí říct,
která část.

**Náš syntetický trh** je postavený tak, aby se choval podobně: jeden tržní faktor a deset sektorů. Je to
zjednodušení s parametry podle naší volby; skutečné trhy mají těžké chvosty a korelace se v čase mění.
""",
    further_reading=(
        Reading(LALOUX_1999, "spektrum akcií S&P 500 proti čistému šumu"),
        Reading(PLEROU_1999, "nezávislé potvrzení na 30minutových výnosech"),
    ),
)

MARKOWITZ = TheoryTopic(
    anchor="nm-markowitz",
    title="Proč Markowitz šum zesiluje",
    in_short=(
        "Optimalizace hledá směry s nejmenším rozptylem – a ty jsou v odhadnuté matici uměle malé. Pro surovou "
        "matici vychází slíbený rozptyl 1 − q a skutečný 1/(1 − q) krát optimum; při "
        f"q = {czech_decimal(EXAMPLE_RATIO, 1)} tedy {czech_decimal(EXAMPLE_IN_SAMPLE, 1)}× "
        f"a {czech_decimal(EXAMPLE_OUT_OF_SAMPLE, 0)}×."
    ),
    explanation=r"""
**Portfolio s minimálním rozptylem.** Váhy, které při plné investici minimalizují rozptyl, jsou

$$
w = \frac{C^{-1} \mathbf{1}}{\mathbf{1}^\top C^{-1} \mathbf{1}} .
$$

Inverze matice dává největší váhu směrům s *nejmenšími* vlastními čísly. Právě ta jsou ve výběrové matici
podle Marčenka a Pastura uměle stlačená k $\lambda_-$. Optimalizace tak sází na „bezpečné“ kombinace akcií,
které jsou bezpečné jen v historických datech.

**Kolik to stojí.** Bouchaud a Potters ve svém přehledu (rovnice 29, s odkazem na Pafku a Kondora) uvádějí
pro nezávislé výnosy a velké N výsledek, který se dá zapsat přes rozptyl optimálního portfolia
$R^2_{\text{opt}}$ postaveného z pravé matice:

$$
R^2_{\text{slíbený}} \approx (1 - q)\, R^2_{\text{opt}}, \qquad
R^2_{\text{skutečný}} \approx \frac{R^2_{\text{opt}}}{1 - q} .
$$

Pozor na jednotky: faktory platí pro *rozptyl*. Pro směrodatnou odchylku (riziko v procentech) je třeba
vzít odmocninu, tedy $\sqrt{1-q}$ a $1/\sqrt{1-q}$.

**Příklad.** Při $q = 0{,}5$ (např. 500 akcií a 1 000 dní) backtest ukáže poloviční rozptyl, než je vůbec
možný, a portfolio ponese dvojnásobný. Slib a skutečnost se liší čtyřikrát v rozptylu, tedy dvakrát ve
směrodatné odchylce. Na skutečných akciích naměřili Bouchaud a Potters poměr skutečného a slíbeného rizika
asi 2,5 tam, kde vzorec dává 2.

**Odkud vzorce jsou.** Pafka a Kondor (2003) je odvodili pro modelový trh s nezávislými akciemi; Bouchaud
a Potters je uvádějí obecně pro Markowitzovu úlohu, ve které je vektor očekávaných výnosů náhodný a nezávislý
na korelacích. Že stejné faktory platí i pro portfolio s minimálním rozptylem na trhu s faktory, jsme ověřili
jen simulací: graf „Jak chyba roste s poměrem q“ v laboratoři sedí se vzorci při 200 akciích a více na pár
procent (vlastní ověření). Pafka a Kondor také uvádějí, že šum je při $q \approx 0{,}6$ výrazný a při
$q \le 0{,}2$ přijatelný.
""",
    further_reading=(
        Reading(BOUCHAUD_POTTERS_REVIEW, "vzorce pro slíbené a skutečné riziko"),
        Reading(PAFKA_KONDOR, "odvození na modelovém trhu, kdy je šum ještě přijatelný"),
    ),
)

CLEANING = TheoryTopic(
    anchor="nm-cisteni",
    title="Jak matici vyčistit",
    in_short=(
        "Vlastní čísla v pásu šumu se nahradí jedním společným číslem (ořezání), nebo se celá matice stáhne "
        "k jednoduchému cíli (shrinkage). Moderní metody upraví každé vlastní číslo zvlášť."
    ),
    explanation=r"""
**Ořezání vlastních čísel.** Vlastní čísla pod $\lambda_+$ nahradíme jejich průměrem (stopa matice, tedy
celkový rozptyl, se nezmění), vlastní čísla nad pásem i všechny vlastní vektory necháme. Informace zůstane,
šum se „uhladí“. Bun, Bouchaud a Potters to označují za nejspíš první estimátor založený na teorii náhodných
matic. Rozptyl šumu v laboratoři odhadujeme jednoduše z dat jako $\sigma^2 = 1 - \lambda_{\max}/N$, tedy
odečteme podíl tržního módu (naše volba; Laloux a kol. rozptyl proložili).

**Lineární shrinkage (Ledoit a Wolf 2004).** Výběrovou matici $E$ smícháme s násobkem jednotkové matice:

$$
\hat C = (1 - \delta)\, E + \delta\, m\, I ,
$$

kde $m$ je průměrný rozptyl a intenzitu $\delta \in [0, 1]$ odhadnou Ledoit a Wolf z dat tak, aby se
minimalizovala očekávaná kvadratická chyba. Metoda nepotřebuje předpoklad o rozdělení výnosů a vzorec pro
$\delta$ je jednoduchý, proto se snadno používá.

**Nelineární shrinkage a RIE.** Ledoit a Wolf (2012, 2020) a Bun, Bouchaud a Potters (2017) odvodili, jak
optimálně posunout *každé* vlastní číslo zvlášť, když vlastní vektory necháme (tzv. rotačně invariantní
estimátory, RIE). Ořezání i lineární shrinkage jsou hrubší pravidla stejného typu: mění jen vlastní čísla.
Podle Buna, Bouchauda a Potterse dává RIE na finančních datech lepší výsledky než dřívější metody.

**Co ukazuje laboratoř (náš pozorovaný výsledek, ne obecné pravidlo).** Na našem trhu s přesnou faktorovou
strukturou vychází ořezání lépe než lineární shrinkage: cíl $m I$ neumí vyjádřit, že všechny akcie korelují
s trhem. Na skutečných datech se pořadí metod může lišit; porovnání na reálných trzích je v přehledu Buna,
Bouchauda a Potterse.
""",
    further_reading=(
        Reading(BUN_BOUCHAUD_POTTERS, "ořezání, rotačně invariantní estimátory a srovnání na datech"),
        Reading(LEDOIT_WOLF_2004, "lineární shrinkage s odhadem optimální intenzity"),
        Reading(LEDOIT_WOLF_2012, "nelineární shrinkage"),
        Reading(LEDOIT_WOLF_2020, "analytická verze nelineárního shrinkage"),
    ),
)

MARKET_STATES = TheoryTopic(
    anchor="nm-stavy-trhu",
    title="Stavy trhu a systémové riziko ze spektra",
    in_short=(
        "Když se korelační matice počítá v klouzavém okně, její spektrum se v čase mění. Z toho se dají vyčíst "
        "stavy trhu i ukazatel systémového rizika."
    ),
    explanation=r"""
**Stavy trhu.** Münnix, Shimada, Schäfer, Leyvraz, Seligman, Guhr a Stanley (2012) – mezi autory je Thomas
Guhr, spoluautor přehledu o náhodných maticích v kvantové fyzice – spočítali korelační matice akcií z indexu
S&P 500 v dvouměsíčních oknech let 1992–2010 a rozdělili je metodou shlukování do osmi „stavů trhu“. Trh mezi
stavy přeskakuje a občas se vrací do dřívějších. Během krize se podle autorů struktura korelací úplně změní.

**Absorption ratio.** Kritzman, Li, Page a Rigobon (2011) definovali podíl celkového rozptylu, který vysvětlí
pevný počet největších vlastních vektorů (hlavních komponent), zhruba pětina počtu aktiv. Když roste, trh je
„těsněji svázaný“ a šok se snáz šíří; autoři ho navrhují jako ukazatel systémového rizika. Definici jsme
převzali ze sekundárních shrnutí, plný text článku je placený.

**Souvislost s laboratoří.** Obě metody čtou stejný objekt jako histogram výše – vlastní čísla korelační
matice – jen v čase. Teorie náhodných matic k tomu dodává měřítko, co je ještě šum.
""",
    further_reading=(
        Reading(MUNNIX_2012, "shlukování korelačních matic do stavů trhu"),
        Reading(KRITZMAN_2011, "absorption ratio jako ukazatel systémového rizika"),
    ),
)

EXPECTED_SHORTFALL = TheoryTopic(
    anchor="nm-expected-shortfall",
    title="Fázový přechod u Expected Shortfall",
    in_short=(
        "Při optimalizaci přes Expected Shortfall existuje kritický poměr N/T, nad kterým úloha z historických "
        "dat nemá smysluplné řešení. Spočítali to fyzici metodami teorie spinových skel."
    ),
    explanation=r"""
**Míra rizika.** Expected Shortfall je průměrná ztráta v nejhorších případech. Basilejský rámec pro tržní
riziko z roku 2019 (FRTB) ho počítá na hladině 97,5 %, tedy z 2,5 % nejhorších dní, a nahradil jím Value at
Risk.

**Výsledek.** Ciliberti, Kondor a Mézard (2007) spočítali replikovou metodou ze statistické fyziky
neuspořádaných systémů, že optimalizace portfolia přes historický Expected Shortfall má fázový přechod: nad
kritickým poměrem N/T se úloha stává neomezenou – optimální pozice utečou do nekonečna. Kritický poměr závisí
na hladině $\beta$: pro $\beta \to 1$ (největší ztráta) je 0,5, pro $\beta = 0{,}7$ asi 0,46. Kondor, Pafka
a Nagy (2007) ukázali, že u každé z porovnaných měr rizika závisí vliv šumu asymptoticky jen na N/T a v
kritickém bodě, který se pro jednotlivé míry liší, diverguje.

**Proč na tom záleží.** Je to stejný jev jako v laboratoři, jen ostřejší: se šumem roste chyba plynule
u rozptylu, ale u Expected Shortfall může optimalizace selhat úplně. Pro banky to znamená otázku „kolik dat
potřebujeme, aby čísla něco znamenala“ (náš výklad).
""",
    further_reading=(
        Reading(CILIBERTI_KONDOR_MEZARD, "fázový přechod, replikový výpočet"),
        Reading(KONDOR_PAFKA_NAGY, "citlivost různých měr rizika na šum"),
        Reading(BASEL_FRTB, "Expected Shortfall v regulaci tržního rizika"),
    ),
)

DETERMINISTIC_CHAOS = TheoryTopic(
    anchor="nm-chaos-v-cenach",
    title="Teorie chaosu a ceny: předpověď, nebo diagnostika?",
    in_short=(
        "Předpovídat ceny z nízkodimenzionálního chaosu se doložit nepodařilo. Nástroje teorie chaosu – testy "
        "nelinearity, entropie, rekurentní analýza – se ale dají použít jinak: jako diagnostika, jestli mají data "
        "strukturu, kterou gaussovský model nevystihne."
    ),
    explanation=r"""
**Myšlenka.** Pokud by ceny řídil deterministický chaotický systém s málo proměnnými, šlo by z historie
zrekonstruovat jeho atraktor (Takensova věta) a krátkodobě předpovídat.

**Testy.** Hsieh (1991) testoval výnosy amerických akcií mimo jiné testem BDS. Podle sekundárních shrnutí
našel nelineární závislost, ale žádný doklad nízkodimenzionálního chaosu, a nelinearitu lze vysvětlit
proměnlivou volatilitou. Plný text je placený, tento závěr jsme proti článku neověřili.

**Prediction Company.** Fyzici chaosu Doyne Farmer a Norman Packard založili v roce 1991 firmu na
předpovídání trhů. Od roku 1992 obchodovala pro O'Connor and Associates, z nichž se stala součást UBS; UBS firmu
v roce 2005 koupila. Začátky popisuje kniha Thomase Basse. Jakými modely přesně obchodovala, veřejně popsané
není, takže z jejího úspěchu nejde usuzovat, že ceny jsou chaotické (náš výklad).

**Dvě různé otázky (náš výklad).** „Řídí ceny chaotický systém, ze kterého jde předpovídat?“ – na to
literatura přesvědčivé ano nedala. „Mají výnosy nelineární strukturu, kterou gaussovský model nevystihne,
a kdy?“ – to je jiná otázka a nástroje teorie chaosu se na ni používají: test BDS, entropie nebo
kvantitativní rekurentní analýza měří, jak moc se data liší od nezávislého šumu a jak se to mění v čase.
Pro modely postavené na gaussovském předpokladu – Markowitze, gaussovské Monte Carlo i odhady na GBS – je to
užitečná diagnostika. Výjimkou je 0-1 test chaosu: na zašuměných datech zaměňuje šum za chaos.

**Závěr pro výzkum.** Z kvantového chaosu se do financí přenáší hlavně statistika spekter, tedy teorie
náhodných matic. Z klasické teorie chaosu spíš nástroje na měření nelineární struktury dat než předpovědní
modely.
""",
    further_reading=(
        Reading(HSIEH_1991, "testy chaosu na výnosech akcií"),
        Reading(BDS_1996, "test nezávislosti, který Hsieh použil"),
        Reading(BASS_PREDICTORS, "příběh Prediction Company"),
        Reading(WIKIPEDIA_PREDICTION_COMPANY, "data o smlouvě s O'Connor a koupi firmou UBS"),
    ),
)

TOPICS: Tuple[TheoryTopic, ...] = (
    ORIGINS,
    MARCHENKO_PASTUR_TOPIC,
    EMPIRICAL,
    MARKOWITZ,
    CLEANING,
    MARKET_STATES,
    EXPECTED_SHORTFALL,
    DETERMINISTIC_CHAOS,
)
