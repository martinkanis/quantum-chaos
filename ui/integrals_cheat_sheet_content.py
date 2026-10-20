"""Cheat sheet on integrals: from the basic table to the Gaussian integrals behind GBS and Monte Carlo."""

from __future__ import annotations

from typing import Tuple

from ui.andersen_shan_paper_content import OWEN_MONTE_CARLO, WIKIPEDIA_FUBINI
from ui.theory_content import WIKIPEDIA_HAFNIAN, WIKIPEDIA_MONTE_CARLO, Reading, Source, TheoryTopic

TITLE = "Tahák: integrály"
SOURCES_ANCHOR = "tahak-zdroje"
INTRO = (
    "Vzorce a pravidla na jedno místo: základní „kuchařka“, per partes, substituce, určitý a nevlastní integrál, "
    "vícerozměrné integrály a nakonec gaussovské integrály a Monte Carlo, na kterých stojí zbytek aplikace. Každé "
    "pravidlo má krátký příklad; výsledek neurčitého integrálu si vždy ověříš derivací."
)

MONTE_CARLO_STANDARD_ERROR = "0{,}298"
"""√Var(U²) for U uniform on [0, 1]: √(1/5 − 1/9) = √(4/45)."""

OHNISKO_BASICS = Source(
    "Ohnisko: [Neurčitý integrál – základy](https://www.youtube.com/watch?v=ZH3mYXP8RME) – video s integrační "
    "„kuchařkou“ a linearitou",
    czech=True,
)
OHNISKO_BY_PARTS = Source(
    "Ohnisko: [Integrace metodou per partes](https://www.youtube.com/watch?v=HoPTNCYEB7E)", czech=True
)
OHNISKO_SUBSTITUTION = Source("Ohnisko: [Integrály – substituce](https://www.youtube.com/watch?v=5Vvscu3C5lo)", czech=True)
OHNISKO_CIRCLE = Source(
    "Ohnisko: [Obsah kruhu jako určitý integrál](https://www.youtube.com/watch?v=0Ea57VCLc2E)", czech=True
)
WIKIPEDIA_ANTIDERIVATIVE = Source(
    "Wikipedie: [Primitivní funkce](https://cs.wikipedia.org/wiki/Primitivn%C3%AD_funkce)", czech=True
)
WIKIPEDIA_NEWTON_INTEGRAL = Source(
    "Wikipedie: [Newtonův integrál](https://cs.wikipedia.org/wiki/Newton%C5%AFv_integr%C3%A1l)", czech=True
)
WIKIPEDIA_RIEMANN_INTEGRAL = Source(
    "Wikipedie: [Riemannův integrál](https://cs.wikipedia.org/wiki/Riemann%C5%AFv_integr%C3%A1l) – integrál jako "
    "plocha a limita součtů",
    czech=True,
)
WIKIPEDIA_BY_PARTS = Source(
    "Wikipedie: [Integrace per partes](https://cs.wikipedia.org/wiki/Integrace_per_partes)", czech=True
)
WIKIPEDIA_IMPROPER_INTEGRAL = Source(
    "Wikipedie: [Nevlastní integrál](https://cs.wikipedia.org/wiki/Nevlastn%C3%AD_integr%C3%A1l)", czech=True
)
WIKIPEDIA_GAUSS_INTEGRAL = Source(
    "Wikipedie: [Gaussův integrál](https://cs.wikipedia.org/wiki/Gauss%C5%AFv_integr%C3%A1l)", czech=True
)
WIKIPEDIA_GAUSSIAN_INTEGRAL = Source(
    "Wikipedia: [Gaussian integral](https://en.wikipedia.org/wiki/Gaussian_integral) – včetně vícerozměrné verze"
)
WIKIPEDIA_LISTS_OF_INTEGRALS = Source(
    "Wikipedia: [Lists of integrals](https://en.wikipedia.org/wiki/Lists_of_integrals) – rozsáhlé tabulky"
)
PAUL_INTEGRALS = Source(
    "Dawkins, P.: Paul's Online Math Notes – [Integrals](https://tutorial.math.lamar.edu/Classes/CalcI/IntegralsIntro.aspx) "
    "– výklad s řešenými příklady"
)
PAUL_SUBSTITUTION = Source(
    "Dawkins, P.: Paul's Online Math Notes – [Substitution Rule]"
    "(https://tutorial.math.lamar.edu/Classes/CalcI/SubstitutionRuleIndefinite.aspx)"
)
PAUL_BY_PARTS = Source(
    "Dawkins, P.: Paul's Online Math Notes – [Integration by Parts]"
    "(https://tutorial.math.lamar.edu/Classes/CalcII/IntegrationByParts.aspx)"
)

BASICS_TOPIC = TheoryTopic(
    anchor="tahak-zaklady",
    title="Co je integrál: neurčitý a určitý",
    in_short=(
        r"Neurčitý integrál je opak derivace: hledáme $F$ s $F' = f$ a přidáme konstantu $C$. Určitý integrál "
        r"$\int_a^b f$ je číslo – plocha pod grafem – a spočítá se jako $F(b) - F(a)$."
    ),
    explanation=r"""
**Neurčitý integrál (primitivní funkce).**

$$
\int f(x)\,\mathrm{d}x = F(x) + C
$$

právě když $F'(x) = f(x)$. Konstanta $C$ je tam proto, že derivace konstanty je nula: $(x^2)' = (x^2 + 5)' = 2x$.

**Zkouška vždy funguje.** Výsledek zderivuj; musí vyjít původní funkce.

**Co znamená $\mathrm{d}x$.** Říká, podle které proměnné integrujeme: $\int a x\,\mathrm{d}x = a x^2/2 + C$,
ale $\int a x\,\mathrm{d}a = a^2 x/2 + C$.

**Určitý integrál a Newtonova–Leibnizova formule.** $\int_a^b f(x)\,\mathrm{d}x$ je plocha mezi grafem a osou
$x$ na intervalu $[a, b]$; části pod osou se počítají záporně. Spočítá se z libovolné primitivní funkce:

$$
\begin{aligned}
\int_a^b f(x)\,\mathrm{d}x &= \big[F(x)\big]_a^b \\
&= F(b) - F(a) .
\end{aligned}
$$

Konstanta $C$ se přitom odečte. Příklad: $\int_0^1 x^2\,\mathrm{d}x = \big[x^3/3\big]_0^1 = 1/3$.
""",
    further_reading=(
        Reading(OHNISKO_BASICS),
        Reading(WIKIPEDIA_ANTIDERIVATIVE),
        Reading(WIKIPEDIA_NEWTON_INTEGRAL),
        Reading(WIKIPEDIA_RIEMANN_INTEGRAL),
        Reading(PAUL_INTEGRALS),
    ),
)

TABLE_TOPIC = TheoryTopic(
    anchor="tahak-kucharka",
    title="Kuchařka: základní integrály a linearita",
    in_short=(
        "Tabulka integrálů, které stačí znát nazpaměť, a „užitečná věta“: integrál součtu je součet integrálů "
        "a konstanta se vytkne. Součin ani složenou funkci takhle integrovat nejde – na ty jsou per partes "
        "a substituce."
    ),
    explanation=r"""
| funkce $f(x)$ | $\int f(x)\,\mathrm{d}x$ | podmínka |
|:---|:---|:---|
| $0$ | $C$ | |
| $a$ (konstanta) | $a x + C$ | |
| $x^n$ | $\dfrac{x^{n+1}}{n+1} + C$ | $n \ne -1$ |
| $\dfrac{1}{x}$ | $\ln\lvert x\rvert + C$ | $x \ne 0$ |
| $e^x$ | $e^x + C$ | |
| $e^{kx}$ | $\dfrac{e^{kx}}{k} + C$ | $k \ne 0$ |
| $a^x$ | $\dfrac{a^x}{\ln a} + C$ | $a > 0,\ a \ne 1$ |
| $\sin x$ | $-\cos x + C$ | |
| $\cos x$ | $\sin x + C$ | |
| $\dfrac{1}{\cos^2 x}$ | $\mathrm{tg}\,x + C$ | $\cos x \ne 0$ |
| $\dfrac{1}{\sin^2 x}$ | $-\mathrm{cotg}\,x + C$ | $\sin x \ne 0$ |
| $\dfrac{1}{1+x^2}$ | $\mathrm{arctg}\,x + C$ | |
| $\dfrac{1}{\sqrt{1-x^2}}$ | $\arcsin x + C$ | $-1 < x < 1$ |

**Odmocniny a zlomky jsou mocniny.** $\sqrt{x} = x^{1/2}$, takže $\int \sqrt{x}\,\mathrm{d}x = \tfrac{2}{3}x^{3/2} + C$;
$1/x^2 = x^{-2}$, takže $\int x^{-2}\,\mathrm{d}x = -1/x + C$.

**Linearita („užitečná věta“).**

$$
\begin{aligned}
& \int \big[c_1 f_1(x) + c_2 f_2(x)\big]\,\mathrm{d}x \\
& = c_1 \int f_1(x)\,\mathrm{d}x + c_2 \int f_2(x)\,\mathrm{d}x
\end{aligned}
$$

Příklad: $\int \big(3x^2 - \tfrac{4}{x} + 2e^x\big)\,\mathrm{d}x = x^3 - 4\ln\lvert x\rvert + 2e^x + C$.

**Pozor.** $\int f g \ne \int f \cdot \int g$ a $\int f(g(x))\,\mathrm{d}x$ obecně není $F(g(x))$. Na součin je per
partes, na složenou funkci substituce (další dvě kapitoly).
""",
    further_reading=(
        Reading(OHNISKO_BASICS, "integrační kuchařka od 10. minuty"),
        Reading(WIKIPEDIA_LISTS_OF_INTEGRALS),
    ),
)

BY_PARTS_TOPIC = TheoryTopic(
    anchor="tahak-per-partes",
    title="Per partes: integrál součinu",
    in_short=(
        r"$\int u\,v'\,\mathrm{d}x = u\,v - \int u'\,v\,\mathrm{d}x$. Za $u$ se volí to, co se derivováním "
        r"zjednoduší (polynom, $\ln x$), za $v'$ to, co umíme integrovat ($e^x$, $\sin x$, $\cos x$)."
    ),
    explanation=r"""
**Vzorec** plyne z derivace součinu $(uv)' = u'v + uv'$:

$$
\int u\,v'\,\mathrm{d}x = u\,v - \int u'\,v\,\mathrm{d}x
$$

a pro určitý integrál

$$
\int_a^b u\,v'\,\mathrm{d}x = \big[u\,v\big]_a^b - \int_a^b u'\,v\,\mathrm{d}x .
$$

**Jak volit.** Anglická pomůcka LIATE říká, co brát za $u$ přednostně: logaritmus, inverzní goniometrické,
algebraické (polynomy), trigonometrické, exponenciála.

**Příklady.**

- $\int x\,e^x\,\mathrm{d}x$: $u = x$, $v' = e^x$, takže $x e^x - \int e^x\,\mathrm{d}x = (x - 1)\,e^x + C$.
  Určitě: $\int_0^1 x\,e^x\,\mathrm{d}x = \big[(x-1)e^x\big]_0^1 = 0 - (-1) = 1$.
- $\int \ln x\,\mathrm{d}x$: $u = \ln x$, $v' = 1$, takže $x\ln x - \int x \cdot \tfrac{1}{x}\,\mathrm{d}x
  = x\ln x - x + C$.
- $\int x^2 \cos x\,\mathrm{d}x$: per partes dvakrát; vyjde $x^2 \sin x + 2x\cos x - 2\sin x + C$.

**Kde to potkáš v GBS.** Momenty normálního rozdělení se počítají právě per partes: s $u = x^{n-1}$ a
$v' = x\,e^{-x^2/2}$ (tedy $v = -e^{-x^2/2}$) vyjde $\mathbb{E}[X^n] = (n-1)\,\mathbb{E}[X^{n-2}]$. To je
jednorozměrné Steinovo lemma, na kterém stojí výpočet momentů v aplikaci.
""",
    further_reading=(
        Reading(OHNISKO_BY_PARTS),
        Reading(WIKIPEDIA_BY_PARTS),
        Reading(PAUL_BY_PARTS),
    ),
)

SUBSTITUTION_TOPIC = TheoryTopic(
    anchor="tahak-substituce",
    title="Substituce: integrál složené funkce",
    in_short=(
        r"$\int f(g(x))\,g'(x)\,\mathrm{d}x = \int f(t)\,\mathrm{d}t$ pro $t = g(x)$. Zvol za $t$ vnitřní funkci, "
        r"přepiš $\mathrm{d}x$ přes $\mathrm{d}t = g'(x)\,\mathrm{d}x$, zintegruj a vrať se k $x$."
    ),
    explanation=r"""
**Postup.** (1) $t = g(x)$, (2) $\mathrm{d}t = g'(x)\,\mathrm{d}x$, (3) přepiš celý integrál na $t$ – žádné $x$
nesmí zůstat, (4) zintegruj, (5) dosaď zpět $t = g(x)$.

**Příklady.**

- $\int 2x\cos(x^2)\,\mathrm{d}x$: $t = x^2$, $\mathrm{d}t = 2x\,\mathrm{d}x$, tedy
  $\int \cos t\,\mathrm{d}t = \sin(x^2) + C$.
- $\int x\,e^{-x^2/2}\,\mathrm{d}x$: $t = -x^2/2$, $\mathrm{d}t = -x\,\mathrm{d}x$, tedy
  $-\int e^t\,\mathrm{d}t = -e^{-x^2/2} + C$.
- $\int \mathrm{tg}\,x\,\mathrm{d}x = \int \frac{\sin x}{\cos x}\,\mathrm{d}x$: $t = \cos x$, vyjde
  $-\ln\lvert\cos x\rvert + C$. Obecně $\int \frac{g'(x)}{g(x)}\,\mathrm{d}x = \ln\lvert g(x)\rvert + C$.

**Lineární substituce, nejčastější případ.** $\int f(ax + b)\,\mathrm{d}x = \frac{1}{a}F(ax + b) + C$, třeba
$\int \cos 3x\,\mathrm{d}x = \tfrac{1}{3}\sin 3x + C$ nebo $\int e^{2x+1}\,\mathrm{d}x = \tfrac{1}{2}e^{2x+1} + C$.

**U určitého integrálu se mění meze.**

$$
\int_a^b f(g(x))\,g'(x)\,\mathrm{d}x = \int_{g(a)}^{g(b)} f(t)\,\mathrm{d}t .
$$
""",
    further_reading=(
        Reading(OHNISKO_SUBSTITUTION),
        Reading(PAUL_SUBSTITUTION),
    ),
)

DEFINITE_TOPIC = TheoryTopic(
    anchor="tahak-urcity",
    title="Vlastnosti určitého integrálu a plochy",
    in_short=(
        "Meze se dají sčítat a prohazovat (se změnou znaménka), lichá funkce na symetrickém intervalu dá nulu "
        r"a sudá dvojnásobek poloviny. Plocha mezi křivkami je integrál z rozdílu; obsah kruhu vyjde $\pi r^2$."
    ),
    explanation=r"""
**Pravidla pro meze.**

- $\int_a^a f = 0$, $\int_b^a f = -\int_a^b f$, $\int_a^c f = \int_a^b f + \int_b^c f$.
- *Lichá funkce* ($f(-x) = -f(x)$) na $[-a, a]$: $\int_{-a}^{a} f = 0$. Proto mají normálně rozdělené veličiny
  liché momenty nulové.
- *Sudá funkce* ($f(-x) = f(x)$): $\int_{-a}^{a} f = 2\int_0^a f$.

**Plocha mezi křivkami** $g \le f$ na $[a, b]$ je $\int_a^b \big(f(x) - g(x)\big)\,\mathrm{d}x$.

**Obsah kruhu.** Kruh $x^2 + y^2 \le r^2$ má v bodě $x$ výšku $2\sqrt{r^2 - x^2}$, takže

$$
S = \int_{-r}^{r} 2\sqrt{r^2 - x^2}\,\mathrm{d}x = \pi r^2
$$

(substituce $x = r\sin t$).

**Průměrná hodnota funkce** na intervalu je $\frac{1}{b-a}\int_a^b f(x)\,\mathrm{d}x$ – tady začíná Monte Carlo
(poslední kapitola).
""",
    further_reading=(
        Reading(OHNISKO_CIRCLE),
        Reading(WIKIPEDIA_RIEMANN_INTEGRAL),
    ),
)

IMPROPER_TOPIC = TheoryTopic(
    anchor="tahak-nevlastni",
    title="Nevlastní integrály: nekonečné meze",
    in_short=(
        r"Integrál do nekonečna je limita: $\int_a^\infty f = \lim_{R\to\infty}\int_a^R f$. Může vyjít konečný "
        r"($\int_1^\infty x^{-2} = 1$) i nekonečný ($\int_1^\infty x^{-1} = \infty$). Když je konečný integrál "
        r"z $\lvert f\rvert$, je všechno v pořádku."
    ),
    explanation=r"""
**Definice.** $\int_a^\infty f(x)\,\mathrm{d}x = \lim_{R\to\infty}\int_a^R f(x)\,\mathrm{d}x$, podobně pro
$-\infty$ a pro funkce, které u meze rostou nade všechny meze.

**Mocniny – vzor pro srovnání.**

| integrál | konverguje, když | příklad |
|:---|:---|:---|
| $\int_1^\infty x^{-p}\,\mathrm{d}x$ | $p > 1$ | $\int_1^\infty x^{-2}\,\mathrm{d}x = 1$, ale $\int_1^\infty x^{-1}\,\mathrm{d}x = \infty$ |
| $\int_0^1 x^{-p}\,\mathrm{d}x$ | $p < 1$ | $\int_0^1 x^{-1/2}\,\mathrm{d}x = 2$, ale $\int_0^1 x^{-1}\,\mathrm{d}x = \infty$ |

**Srovnávací kritérium.** Platí-li $\lvert f\rvert \le g$ a $\int g < \infty$, konverguje i $\int f$. Proto
jsou konečné všechny momenty normálního rozdělení: $x^n e^{-x^2/2}$ klesá rychleji než $x^{-2}$.

**Absolutní konvergence.** Je-li $\int \lvert f\rvert < \infty$, integrál konverguje a smí se s ním zacházet
„jako s konečným“ – přesně to hlídá podmínka (A1) v článku Andersena a Shan.
""",
    further_reading=(
        Reading(WIKIPEDIA_IMPROPER_INTEGRAL),
    ),
)

MULTIPLE_TOPIC = TheoryTopic(
    anchor="tahak-vicerozmerne",
    title="Vícenásobné integrály a Fubiniova věta",
    in_short=(
        "Vícenásobný integrál se počítá postupně, jedna proměnná po druhé, a pořadí lze prohodit, je-li integrál "
        r"z $\lvert f\rvert$ konečný. Při změně proměnných se násobí absolutní hodnotou determinantu (Jakobiánem)."
    ),
    explanation=r"""
**Postupná integrace (Fubini).** Je-li $\iint \lvert f\rvert < \infty$, pak

$$
\begin{aligned}
& \iint_{[a,b]\times[c,d]} f(x, y)\,\mathrm{d}x\,\mathrm{d}y \\
& = \int_a^b \Big(\int_c^d f(x, y)\,\mathrm{d}y\Big)\mathrm{d}x \\
& = \int_c^d \Big(\int_a^b f(x, y)\,\mathrm{d}x\Big)\mathrm{d}y .
\end{aligned}
$$

Stejně se smí prohodit součet a integrál, $\int \sum_k f_k = \sum_k \int f_k$, když $\sum_k \int \lvert f_k\rvert
< \infty$.

**Součin se rozpadne.** $\iint g(x)\,h(y)\,\mathrm{d}x\,\mathrm{d}y = \int g \cdot \int h$. V pravděpodobnosti:
pro nezávislé $X$, $Y$ je $\mathbb{E}[g(X)\,h(Y)] = \mathbb{E}[g(X)]\,\mathbb{E}[h(Y)]$.

**Změna proměnných.**

- Polární souřadnice: $x = r\cos\varphi$, $y = r\sin\varphi$, $\mathrm{d}x\,\mathrm{d}y = r\,\mathrm{d}r\,\mathrm{d}\varphi$.
- Lineární substituce v $N$ rozměrech: $x = A z$ dává $\mathrm{d}x = \lvert\det A\rvert\,\mathrm{d}z$. Odtud
  pochází $\det B$ v hustotě normálního rozdělení.
""",
    further_reading=(
        Reading(WIKIPEDIA_FUBINI),
    ),
)

GAUSSIAN_TOPIC = TheoryTopic(
    anchor="tahak-gauss",
    title="Gaussovské integrály: všechno, co potřebuje GBS",
    in_short=(
        r"$\int_{-\infty}^{\infty} e^{-x^2/2}\,\mathrm{d}x = \sqrt{2\pi}$; sudé momenty normálního rozdělení jsou "
        r"$(2k-1)!!$, liché nulové; v $N$ rozměrech $\int e^{-\frac12 x^\top A x}\,\mathrm{d}x = (2\pi)^{N/2}"
        r"(\det A)^{-1/2}$. Společné momenty dává Wickova věta jako hafniány."
    ),
    explanation=r"""
**Základní gaussovský integrál.**

$$
\int_{-\infty}^{\infty} e^{-x^2/2}\,\mathrm{d}x = \sqrt{2\pi} \approx 2{,}507
$$

a po substituci obecněji pro $a > 0$

$$
\int_{-\infty}^{\infty} e^{-a x^2}\,\mathrm{d}x = \sqrt{\pi/a} .
$$

Trik: druhá mocnina je dvojný integrál
$\iint e^{-(x^2+y^2)/2}\,\mathrm{d}x\,\mathrm{d}y$ a v polárních souřadnicích
$\int_0^{2\pi}\!\int_0^\infty e^{-r^2/2}\,r\,\mathrm{d}r\,\mathrm{d}\varphi = 2\pi$.

**Hustota a momenty.** Hustota normovaného normálního rozdělení je $\varphi(x) = e^{-x^2/2}/\sqrt{2\pi}$ a

$$
\int x^{2k}\,\varphi(x)\,\mathrm{d}x = (2k - 1)!! ,
$$

kde $(2k-1)!! = 1 \cdot 3 \cdot 5 \cdots (2k-1)$, a liché momenty jsou nulové, $\int x^{2k+1}\,\varphi(x)\,\mathrm{d}x = 0$.

Tedy $\mathbb{E}[X^2] = 1$, $\mathbb{E}[X^4] = 3$, $\mathbb{E}[X^6] = 15$. S rozptylem $\sigma^2$ se násobí
$\sigma^{2k}$.

**Doplnění na čtverec.** $tx - x^2/2 = -(x - t)^2/2 + t^2/2$, a proto
$\int e^{tx}\,\varphi(x)\,\mathrm{d}x = e^{t^2/2}$. Například $\mathbb{E}[\cosh X] = e^{1/2}$.

**$N$ rozměrů.** Pro pozitivně definitní $A$

$$
\begin{aligned}
& \int_{\mathbb{R}^N} e^{-\frac{1}{2}x^\top A x}\,\mathrm{d}x \\
& = (2\pi)^{N/2}\,(\det A)^{-1/2} .
\end{aligned}
$$

S $A = B^{-1}$ odtud plyne normovací konstanta hustoty $h(x)$ v článku Andersena a Shan. Pro vektor $X$
s kovarianční maticí $B$ je $\mathbb{E}[X_i X_j] = B_{ij}$ a $\mathbb{E}[e^{w^\top X}] = e^{\frac12 w^\top B w}$.

**Wickova věta.** Společné momenty jsou součty přes rozdělení do dvojic:
$\mathbb{E}[X_1X_2X_3X_4] = B_{12}B_{34} + B_{13}B_{24} + B_{14}B_{23}$. Obecně je to hafnián – a hafniány
na druhou jsou pravděpodobnosti výstupů GBS.
""",
    further_reading=(
        Reading(WIKIPEDIA_GAUSS_INTEGRAL),
        Reading(WIKIPEDIA_GAUSSIAN_INTEGRAL),
        Reading(WIKIPEDIA_HAFNIAN, "Wickova věta a hafnián"),
    ),
)

MONTE_CARLO_TOPIC = TheoryTopic(
    anchor="tahak-monte-carlo",
    title="Integrál jako střední hodnota: Monte Carlo",
    in_short=(
        r"Každý integrál jde zapsat jako střední hodnotu, $\int_a^b f = (b-a)\,\mathbb{E}[f(U)]$, a odhadnout "
        r"průměrem přes náhodné vzorky. Chyba klesá jako $1/\sqrt{n}$ bez ohledu na dimenzi."
    ),
    explanation=r"""
**Střední hodnota je integrál.** Pro $X$ s hustotou $p$ je $\mathbb{E}[f(X)] = \int f(x)\,p(x)\,\mathrm{d}x$.
Obráceně: je-li $U$ rovnoměrně rozdělené na $[a, b]$, platí $\int_a^b f(x)\,\mathrm{d}x = (b-a)\,\mathbb{E}[f(U)]$.

**Monte Carlo.** Vylosuj $U_1, \dots, U_n$ a spočítej

$$
\int_a^b f(x)\,\mathrm{d}x \approx \frac{b-a}{n}\sum_{j=1}^{n} f(U_j) .
$$

Směrodatná chyba je $(b-a)\,\sigma/\sqrt{n}$, kde $\sigma^2 = \mathrm{Var}\,f(U)$.

**Příklad.** $\int_0^1 x^2\,\mathrm{d}x = 1/3$. Pro $U$ rovnoměrné na $[0, 1]$ je
$\mathrm{Var}(U^2) = \tfrac{1}{5} - \tfrac{1}{9} = \tfrac{4}{45}$, tedy $\sigma \approx 0{,}298$; s 10 000 vzorky
je chyba asi 0,003.

**Vážený výběr (importance sampling).** Losuje-li se z jiné hustoty $q$, platí
$\int f(x)\,\mathrm{d}x = \mathbb{E}_q\big[f(X)/q(X)\big]$. Dobře zvolené $q$ (podobné $\lvert f\rvert$) rozptyl
výrazně zmenší. Odhad GBS-I je přesně tohle: $q$ je rozdělení výstupů Gaussian Boson Sampleru.
""",
    further_reading=(
        Reading(WIKIPEDIA_MONTE_CARLO),
        Reading(OWEN_MONTE_CARLO, "kapitola 9: vážený výběr"),
    ),
)

TOPICS: Tuple[TheoryTopic, ...] = (
    BASICS_TOPIC,
    TABLE_TOPIC,
    BY_PARTS_TOPIC,
    SUBSTITUTION_TOPIC,
    DEFINITE_TOPIC,
    IMPROPER_TOPIC,
    MULTIPLE_TOPIC,
    GAUSSIAN_TOPIC,
    MONTE_CARLO_TOPIC,
)
