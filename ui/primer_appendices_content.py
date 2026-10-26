"""Czech translation of appendices A and B of the primer by Kolarovszki and Zimborás (ui/primer_content.py)."""

from __future__ import annotations

from ui.primer_content import PrimerChapter, PrimerSection

SECTION_A_1 = PrimerSection(
    anchor="skripta-a-1",
    number="A.1",
    title="Hilbertovy prostory",
    body=r"""
V kvantové mechanice je často potřeba pracovat ve vektorovém prostoru, jehož skaláry jsou komplexní čísla a jehož
dimenze může být nekonečná. Taková konstrukce vyžaduje zobecnit standardní eukleidovský vektorový prostor, což lze
udělat zavedením vektorových prostorů nad tělesem komplexních čísel. Tyto vektorové prostory jsou navíc přirozeně
vybaveny skalárním součinem (inner product), přímou obdobou standardního skalárního součinu (dot product)
eukleidovských prostorů, který nám umožňuje definovat úhly a vzdálenosti. Tím se dostáváme k pojmu Hilbertova prostoru
(Hilbert space), základního nástroje pro popis kvantově mechanických jevů.

**Definice A.1.1 (Komplexní prostor se skalárním součinem).** Komplexní prostor se skalárním součinem (complex inner
product space) $V$ je komplexní vektorový prostor se skalárním součinem $\langle \cdot | \cdot \rangle$, který má
následující vlastnosti:

- Symetrie vůči komplexnímu sdružení (conjugation symmetry):

$$
\langle x|y \rangle = \overline{\langle y|x \rangle}, \qquad x, y \in V.
\tag{A.1}
$$

- Linearita:

$$
\langle x|ay + bz \rangle = a \langle x|y \rangle + b \langle x|z \rangle, \qquad x, y, z \in V,\ a, b \in \mathbb{C},
\tag{A.2}
$$

- Pozitivní definitnost:

$$
\begin{aligned}
&\langle x|x \rangle \geq 0, \quad \forall\, x \in V, \\
&\langle x|x \rangle = 0 \Leftrightarrow x = 0.
\end{aligned}
\tag{A.3}
$$

V kvantové mechanice se předpokládá, že komplexní prostory se skalárním součinem jsou úplné v Cauchyově smyslu
(Cauchy-complete), tj. že cauchyovské posloupnosti v nich konvergují k prvku téhož prostoru. Komplexním prostorům se
skalárním součinem, které jsou v tomto smyslu úplné, říkáme *komplexní Hilbertovy prostory*:

**Definice A.1.2 (Komplexní Hilbertův prostor).** Komplexní Hilbertův prostor $\mathcal{H}$ je komplexní prostor se
skalárním součinem, který je úplný vzhledem k metrice indukované skalárním součinem,
$d(x, y) = \sqrt{\langle x - y | x - y \rangle}$. Úplnost znamená, že každá cauchyovská posloupnost v $\mathcal{H}$ má
limitu, která rovněž leží v $\mathcal{H}$.

Pomocí normy indukované skalárním součinem, kterou značíme $\lVert \cdot \rVert$, lze v Hilbertových prostorech
definovat konvergenci, a tedy i nekonečné součty (na rozdíl od obecných nekonečněrozměrných vektorových prostorů).

**Definice A.1.3.** Nechť $\mathcal{H}$ je Hilbertův prostor a $I$ množina indexů. Množina
$\{e_i \in \mathcal{H}\}_{i \in I}$ se nazývá *báze* (basis), jestliže

1. $\{e_i\}_{i \in I}$ je lineárně nezávislá množina,
2. pro každé $v \in \mathcal{H} \setminus \{0\}$ existuje $J \subseteq I$, kde $J$ má nejvýše spočetnou mohutnost, a k
   ní příslušná jednoznačně určená množina $\{c_j : c_j \in \mathbb{C}\}_{j \in J}$ taková, že

$$
v = \sum_{j \in J} c_j e_j .
\tag{A.4}
$$

Jestliže navíc $\langle e_i | e_j \rangle = \delta_{ij}$ pro všechna $i, j \in I$, nazývá se *ortonormální báze*
(orthonormal basis, ONB).

Počet prvků báze je podstatnou vlastností vektorových prostorů:

**Definice A.1.4 (Dimenze).** Dimenze Hilbertova prostoru je rovna mohutnosti jeho báze.

Konečněrozměrné komplexní Hilbertovy prostory jsou izomorfní s $\mathbb{C}^d$ pro nějaké $d \geq 1$. Proto se při
práci s kvantovými systémy popsanými konečněrozměrnými Hilbertovými prostory často používá následující příklad:

**Příklad.** Vektorový prostor $\mathbb{C}^d$, jehož skalárním součinem je standardní skalární součin (dot product)

$$
\begin{aligned}
\langle \cdot | \cdot \rangle &: \mathbb{C}^d \times \mathbb{C}^d \to \mathbb{C}, \\
(v, w) &\mapsto \sum_{j=1}^{d} \overline{v}_j w_j
\end{aligned}
\tag{A.5}
$$

je Hilbertův prostor.

Prostor kvadraticky integrovatelných funkcí s obvyklým skalárním součinem je důležitým příkladem nekonečněrozměrného
Hilbertova prostoru.

**Příklad (Kvadraticky integrovatelné funkce).** Definujme

$$
\langle f | g \rangle := \int_{-\infty}^{\infty} \overline{f(x)}\, g(x) \,\mathrm{d}x,
\tag{A.6}
$$

kde $f, g : \mathbb{R} \to \mathbb{C}$. Množina kvadraticky integrovatelných funkcí $L^2(\mathbb{R})$ tvoří Hilbertův
prostor se skalárním součinem definovaným vztahem (A.6).

Ačkoli některé Hilbertovy prostory, se kterými v této práci pracujeme, jsou konečněrozměrné, Hilbertův prostor
bosonového systému, který odpovídá fotonickému kvantovému počítači, má spočetně nekonečnou ortonormální bázi. Je třeba
poznamenat, že v kvantové mechanice se o všech Hilbertových prostorech předpokládá, že jsou separabilní (separable),
tj. že mají nejvýše spočetnou ortonormální bázi. Proto i v této práci předpokládáme, že všechny Hilbertovy prostory
jsou separabilní.

V kvantové mechanice se vektory často zapisují pomocí lomených závorek jako $|\psi\rangle \in \mathcal{H}$ a nazývají
se *ket* vektory. Abychom zavedli jejich protějšek, uvažujme množinu lineárních operátorů
$\mathcal{H} \to \mathbb{C}$, tj. *lineárních forem* (linear forms). Podle Rieszovy věty o reprezentaci (Riesz
representation theorem) existuje ke každé lineární formě $f_\phi : \mathcal{H} \to \mathbb{C}$ na Hilbertově prostoru
vektor $|\phi\rangle \in \mathcal{H}$ takový, že pro všechna $|\psi\rangle \in \mathcal{H}$ platí
$f_\phi(|\psi\rangle) = \langle \phi | \psi \rangle$. Pro stručnost značíme lineární formu
$f_\phi : \mathcal{H} \to \mathbb{C}$ symbolem $\langle \phi |$ a nazýváme ji *bra* vektorem příslušným ket vektoru
$|\phi\rangle$. Tento zápis je velmi praktický, protože výrazy $\langle \phi |$, $|\psi\rangle$,
$\langle \phi | \psi \rangle$ automaticky vyjadřují vztah mezi lineárními formami a vektory v Hilbertově prostoru.
Této konvenci se říká *bra-ket notace* (bra-ket notation) nebo *Diracova notace*.
""",
)

SECTION_A_2 = PrimerSection(
    anchor="skripta-a-2",
    number="A.2",
    title="Kvantové stavy",
    body=r"""
V kvantové mechanice je výhodné definovat množinu stavů nad separabilním Hilbertovým prostorem:

**Definice A.2.1 (Stavový prostor).** Stavový prostor (state space) na separabilním Hilbertově prostoru $\mathcal{H}$
je

$$
\mathcal{S}(\mathcal{H}) = \left\{ \rho \in \mathrm{B}(\mathcal{H}) : \operatorname{Tr} \rho = 1,\ \rho \geq 0 \right\},
\tag{A.7}
$$

kde $\mathrm{B}(\mathcal{H})$ označuje množinu omezených lineárních operátorů na $\mathcal{H}$ a $\rho \geq 0$
znamená, že $\rho$ je samosdružený lineární operátor s nezáporným spektrem. Prvky $\mathcal{S}(\mathcal{H})$ se
nazývají *operátory hustoty* (density operators).

Vlastní čísla operátoru hustoty $\rho \in \mathcal{S}(\mathcal{H})$ tvoří rozdělení pravděpodobnosti o
$\dim \mathcal{H}$ prvcích. Kvantové stavy odpovídají operátorům hustoty nad separabilním Hilbertovým prostorem, což
je jádro prvního postulátu kvantové mechaniky:

**Postulát 1.** Každému kvantovému systému přísluší separabilní Hilbertův prostor, nazývaný *stavový prostor*
kvantového systému, a *kvantové stavy* jsou úplně popsány operátory hustoty nad tímto Hilbertovým prostorem.

**Definice A.2.2 (Čistý stav).** Operátor hustoty popisuje *čistý stav* (pure state), jestliže je projektorem hodnosti
jedna. Ekvivalentně: operátor hustoty $\rho$ popisuje čistý stav právě tehdy, když $\rho = \rho^2$.

Je-li kvantový stav čistý, lze jeho operátor hustoty zapsat ve tvaru $\rho = |\psi\rangle\langle\psi|$. Čisté kvantové
stavy proto odpovídají jednotkovým vektorům $|\psi\rangle$ v Hilbertově prostoru $\mathcal{H}$ s relací ekvivalence
$|\psi\rangle \sim |\psi'\rangle$ pro libovolné $|\psi'\rangle = e^{i\alpha} |\psi\rangle$, kde
$\alpha \in [0, 2\pi)$.
""",
)

SECTION_A_3 = PrimerSection(
    anchor="skripta-a-3",
    number="A.3",
    title="Časový vývoj",
    body=r"""
Pro popis časového vývoje uzavřeného kvantového systému je zásadní unitární grupa nad Hilbertovým prostorem:

**Definice A.3.1 (Unitární grupa nad Hilbertovým prostorem).** Surjektivní omezené lineární operátory, které
zachovávají skalární součin v Hilbertově prostoru $\mathcal{H}$, se nazývají unitární operátory; přitom $U$ zachovává
skalární součin, jestliže $\langle U\psi, U\phi \rangle = \langle \psi, \phi \rangle$ pro všechna
$|\psi\rangle, |\phi\rangle \in \mathcal{H}$. Množina unitárních operátorů tvoří grupu, kterou značíme
$\mathrm{U}(\mathcal{H})$ a nazýváme *unitární grupa* (unitary group) nad $\mathcal{H}$.

S touto definicí lze zapsat druhý postulát kvantové mechaniky, který předepisuje, jak se uzavřené kvantové systémy
vyvíjejí:

**Postulát 2.** Časový vývoj uzavřeného kvantového systému modelovaného Hilbertovým prostorem $\mathcal{H}$ lze popsat
unitárními operátory nad $\mathcal{H}$.

Je důležité poznamenat, že nad konečněrozměrným Hilbertovým prostorem lze každý unitární operátor zapsat ve tvaru

$$
\hat{U} = \exp\big(i\hat{H}\big),
\tag{A.8}
$$

kde $\hat{H}$ je samosdružený operátor nad $\mathcal{H}$, nazývaný Hamiltonův operátor (hamiltonián).

*(Pozn. překl.: Ve vztahu (A.22) autoři používají obvyklejší znaménko, $\exp(-i\hat{H})$. Obě podoby jsou rovnocenné,
liší se jen znaménkem operátoru $\hat{H}$.)*
""",
)

SECTION_A_4 = PrimerSection(
    anchor="skripta-a-4",
    number="A.4",
    title="Měření",
    body=r"""
Zatím jsme postulovali, jak modelovat uzavřené kvantové systémy a jak popsat jejich vývoj. Potřebujeme však z těchto
systémů také získávat informace, a to pomocí měření. Při měření systém interaguje se svým okolím, a jeho vývoj proto
už není unitární.

Měření na kvantovém systému lze modelovat pomocí pozitivních operátorově hodnotových měr (positive operator-valued
measures, POVM):

**Definice A.4.1 (POVM pro spočetně mnoho výsledků).** Měření na kvantovém systému modelovaném konečněrozměrným
Hilbertovým prostorem $\mathcal{H}$ lze popsat pozitivními operátorově hodnotovými mírami (POVM), danými vztahem

$$
\begin{aligned}
\operatorname{POVM}(\mathcal{X}, \mathcal{H}) := \Bigg\{
& \{M_x\}_{x \in \mathcal{X}} \in \operatorname{Lin}(\mathcal{H}) : \\
& 0 \leq M_x \leq \mathbb{1}_{\mathcal{H}},\ \sum_{x \in \mathcal{X}} M_x = \mathbb{1}_{\mathcal{H}} \Bigg\},
\end{aligned}
\tag{A.9}
$$

kde $\mathcal{X}$ je spočetně nekonečná množina odpovídající možným výsledkům měření.

*(Pozn. překl.: Stačí, aby byla množina $\mathcal{X}$ nejvýše spočetná, tedy i konečná; konečně mnoho výsledků je v
praxi nejběžnější případ.)*

Všimněme si, že jsme uvedli definici POVM pro spočetně mnoho výsledků, ale v případě potřeby ji lze snadno zobecnit i
na nespočetné množiny. Poznamenejme, že pokud jsou všechny operátory, z nichž se POVM skládá, projektory, nazývá se
taková POVM projektorově hodnotová míra (projection-valued measure, PVM). Podstatné je, že pravděpodobnosti výsledků
měření udává Bornovo pravidlo (Born's rule), které je třetím postulátem:

**Postulát 3 (Bornovo pravidlo).** Měření jsou popsána pomocí POVM a indexována možnými výsledky měření. Je-li systém
ve stavu $\rho \in \mathcal{S}(\mathcal{H})$ a provede-li se na něm měření popsané POVM
$M = \{M_x\}_{x \in \mathcal{X}} \in \operatorname{POVM}(\mathcal{H})$, pak pravděpodobnost, že naměříme výsledek $x$,
je dána vztahem

$$
\operatorname{Prob}_{\rho, M}(\text{výsledek} = x) = \operatorname{Tr} \rho M_x .
\tag{A.10}
$$

Měření je způsob, jak z kvantového systému získat informaci. Zatímco operátor hustoty zachycuje veškerou naši znalost
o systému, měření lze chápat jako otázky kladené operátoru hustoty. Snadno se ověří, že Bornovo pravidlo spolu s
definicí POVM určuje rozdělení pravděpodobnosti na výsledcích měření, neboť

$$
\begin{aligned}
\operatorname{Prob}_{\rho, M}(\text{výsledek} = x) &= \operatorname{Tr} \rho M_x \geq 0, \\
\sum_{x \in \mathcal{X}} \operatorname{Prob}_{\rho, M}(\text{výsledek} = x)
&= \operatorname{Tr} \rho \sum_{x \in \mathcal{X}} M_x = 1.
\end{aligned}
\tag{A.11}
$$
""",
)

SECTION_A_5 = PrimerSection(
    anchor="skripta-a-5",
    number="A.5",
    title="Složené systémy",
    body=r"""
Pojem tenzorového součinu (tensor product) nám umožňuje studovat systémy s více částicemi, a je proto zásadní pro
konstrukci vektorového prostoru, ve kterém modelujeme fotonické kvantové stavy:

**Definice A.5.1 (Tenzorový součin Hilbertových prostorů).** Uvažujme Hilbertovy prostory $\mathcal{H}$ a
$\mathcal{K}$. Označme

$$
\mathcal{H} \otimes \mathcal{K} := F(\mathcal{H} \times \mathcal{K}) / R,
\tag{A.12}
$$

kde $F(\mathcal{H} \times \mathcal{K})$ označuje volný vektorový prostor (free vector space) generovaný množinou
$\mathcal{H} \times \mathcal{K}$ a $R$ je podprostor generovaný prvky

$$
R = \operatorname{span}_{\mathbb{C}} \left( \left\{
\begin{matrix}
(v_1 + v_2, w) - (v_1, w) - (v_2, w), \\
(v, w_1 + w_2) - (v, w_1) - (v, w_2), \\
(sv, w) - s(v, w), \\
(v, sw) - s(v, w)
\end{matrix}
\;\middle|\;
\begin{matrix}
\forall\, v_1, v_2, v \in \mathcal{H}, \\
w_1, w_2, w \in \mathcal{K}, \\
s \in \mathbb{C}
\end{matrix}
\right\} \right),
\tag{A.13}
$$

a faktorprostor $F(\mathcal{H} \times \mathcal{K}) / R$ je definován relací ekvivalence $\sim_R$ takto:

$$
a \sim_R b \iff a - b \in R.
\tag{A.14}
$$

Dále zavedeme zobrazení $\otimes : \mathcal{H} \times \mathcal{K} \to \mathcal{H} \otimes \mathcal{K}$, které prvkům
$\mathcal{H}$ a $\mathcal{K}$ přiřadí jejich *tenzorový součin* v $\mathcal{H} \otimes \mathcal{K}$:

$$
v \otimes w := (v, w) \in \mathcal{H} \otimes \mathcal{K}.
\tag{A.15}
$$

*(Pozn. překl.: Pro nekonečněrozměrné $\mathcal{H}$ nebo $\mathcal{K}$ dává tato konstrukce jen algebraický tenzorový
součin, který není úplný. Hilbertův prostor $\mathcal{H} \otimes \mathcal{K}$ je pak jeho zúplnění vzhledem ke
skalárnímu součinu, který je na součinových vektorech dán obdobou vztahu (A.18).)*

Univerzální vlastnost může posloužit i jako ekvivalentní definice tenzorového součinu:

**Definice A.5.2 (Tenzorový součin pomocí univerzální vlastnosti).** Nechť $\mathcal{H}$ a $\mathcal{K}$ jsou dva
konečněrozměrné Hilbertovy prostory. Tenzorový součin $\mathcal{H}$ a $\mathcal{K}$, značený
$\mathcal{H} \otimes \mathcal{K}$, je vektorový prostor s bilineárním zobrazením

$$
\otimes : \mathcal{H} \times \mathcal{K} \to \mathcal{H} \otimes \mathcal{K},
\tag{A.16}
$$

které má univerzální vlastnost (universal property), tj. je-li $f : \mathcal{H} \times \mathcal{K} \to \mathcal{H}'$,
pak existuje lineární zobrazení (až na izomorfismus) $\hat{f} : \mathcal{H} \otimes \mathcal{K} \to \mathcal{H}'$
takové, že $\otimes \circ \hat{f} := f$, kde $\mathcal{H}'$ je konečněrozměrný Hilbertův prostor.

*(Pozn. překl.: Přesněji: ke každému bilineárnímu zobrazení $f$ existuje právě jedno lineární zobrazení $\hat{f}$
takové, že $\hat{f} \circ \otimes = f$, tj. nejprve se použije $\otimes$ a potom $\hat{f}$; originál píše skládání v
obráceném pořadí. Až na izomorfismus je jednoznačně určen samotný tenzorový součin.)*

Ačkoli tato definice nezaručuje existenci, pro tenzorový součin Hilbertových prostorů dává konstrukci definice A.5.1.
Jednoznačnost se snadno ověří z univerzální vlastnosti pomocí diagramových argumentů.

Pojem tenzorového součinu nám umožňuje zapsat poslední, čtvrtý postulát kvantové mechaniky:

**Postulát 4.** Hilbertův prostor složeného kvantového systému (composite system) je modelován tenzorovým součinem
Hilbertových prostorů kvantových systémů, z nichž se skládá.

Bázi Hilbertova prostoru, který je tenzorovým součinem, lze zapsat pomocí tenzorových součinů všech bázových vektorů
dílčích Hilbertových prostorů:

**Tvrzení 12.** Nechť $\mathcal{H}$ a $\mathcal{K}$ jsou dva konečněrozměrné Hilbertovy prostory dimenzí $n$ a $m$ s
bázovými vektory $\{e_i\}_{i=1}^n \subseteq \mathcal{H}$ a $\{f_j\}_{j=1}^m \subseteq \mathcal{K}$. Tenzorový součin
$\mathcal{H}$ a $\mathcal{K}$, značený $\mathcal{H} \otimes \mathcal{K}$, je $(n \cdot m)$-rozměrný Hilbertův prostor
s bázovými vektory

$$
\{e_i \otimes f_j\}_{i,j=1}^{n,m},
\tag{A.17}
$$

se skalárním součinem zadaným na bázových vektorech jako

$$
\langle e_i \otimes f_j | e_k \otimes f_l \rangle_{\mathcal{H} \otimes \mathcal{K}}
= \langle e_i | e_k \rangle_{\mathcal{H}} \langle f_j | f_l \rangle_{\mathcal{K}} .
\tag{A.18}
$$

Poznamenejme, že tenzorový součin více Hilbertových prostorů lze definovat induktivně z tenzorového součinu dvou
Hilbertových prostorů, protože tenzorový součin Hilbertových prostorů je opět Hilbertův prostor. Dále se snadno ověří
asociativita tenzorového součinu. Pro tenzorový součin Hilbertových prostorů
$\mathcal{H}_1, \mathcal{H}_2, \dots, \mathcal{H}_n$ se navíc používá zápis

$$
\mathcal{H}_1 \otimes \mathcal{H}_2 \otimes \cdots \otimes \mathcal{H}_n = \bigotimes_{i=1}^{n} \mathcal{H}_i .
\tag{A.19}
$$

Ve speciálním případě, kdy

$$
\mathcal{H}_1 = \mathcal{H}_2 = \cdots = \mathcal{H}_n = \mathcal{H},
\tag{A.20}
$$

lze použít kratší zápis

$$
\mathcal{H}^{\otimes n} := \bigotimes_{i=1}^{n} \mathcal{H} .
\tag{A.21}
$$

Nyní můžeme definovat také tenzorový součin lineárních operátorů:

**Definice A.5.3.** Nechť $\mathcal{H}$ a $\mathcal{K}$ jsou dva konečněrozměrné Hilbertovy prostory dimenzí $n$ a $m$
s ortonormálními bázovými vektory $\{e_i\}_{i=1}^n \subseteq \mathcal{H}$ a $\{f_j\}_{j=1}^m \subseteq \mathcal{K}$.
Nechť $X : \mathcal{H} \to \mathcal{H}'$ a $Y : \mathcal{K} \to \mathcal{K}'$ jsou dva lineární operátory, kde
$\mathcal{H}'$ a $\mathcal{K}'$ jsou rovněž konečněrozměrné Hilbertovy prostory. Potom $X \otimes Y$ je lineární
operátor na $\mathcal{H} \otimes \mathcal{K}$, který na prvky ONB v $\mathcal{H} \otimes \mathcal{K}$ působí takto:

$$
(X \otimes Y)(e_i \otimes f_j) = (X e_i) \otimes (Y f_j).
$$

Uvažujme nyní složený systém, který lze modelovat prostorem $\mathcal{H} = \bigotimes_{i=1}^{n} \mathcal{H}_i$, kde
$\mathcal{H}_i$ odpovídají jednotlivým podsystémům. Pokud mezi podsystémy nedochází k žádné interakci, lze časový
vývoj složeného systému popsat jako

$$
\hat{U} = \bigotimes_{i=1}^{n} \hat{U}_i = \bigotimes_{i=1}^{n} \exp\big(-i\hat{H}_i\big),
\tag{A.22}
$$

kde $\hat{U}_i \in \mathrm{U}(\mathcal{H}_i)$ jsou operátory časového vývoje jednotlivých podsystémů s Hamiltonovými
operátory $\hat{H}_i$. S touto definicí lze celkový Hamiltonův operátor systému zapsat jako

$$
\hat{H} = \sum_{i}^{n} \hat{H}_i \otimes \bigotimes_{j,\, i \neq j}^{n} \mathbb{1}_j ,
\tag{A.23}
$$

kde $\mathbb{1}_j \in \operatorname{Lin}(\mathcal{H}_j)$ označuje identitu na $\mathcal{H}_j$.
""",
)

SECTION_A_6 = PrimerSection(
    anchor="skripta-a-6",
    number="A.6",
    title="Kvantová mechanika harmonického oscilátoru",
    body=r"""
Pro referenci uvádíme v této části stručný popis jednoduchého kvantového harmonického oscilátoru (harmonic
oscillator), který vychází ze Schrödingerovy rovnice. Schrödingerova rovnice je parciální diferenciální rovnice, která
určuje vlnovou funkci uzavřeného kvantového systému, v našem případě kvantového harmonického oscilátoru. Časový vývoj
určuje Hamiltonův operátor

$$
\hat{H} := \frac{1}{2} \left( -\frac{\partial^2}{\partial x^2} + x^2 \right).
\tag{A.24}
$$

Abychom získali stacionární vlnové funkce příslušné tomuto hamiltoniánu, musíme vyřešit časově nezávislou
Schrödingerovu rovnici kvantového harmonického oscilátoru, která zní

$$
\hat{H}\psi(x) := \frac{1}{2} \left( -\frac{\partial^2}{\partial x^2} + x^2 \right) \psi(x) = E_\psi \psi(x),
\tag{A.25}
$$

kde $E_\psi \in \mathbb{R}$ se nazývá vlastní číslo příslušné vlastní funkci (neboli vlastnímu stavu)
$\psi : \mathbb{R} \to \mathbb{C}$. Zavedeme-li operátory polohy a hybnosti

$$
\hat{x} := x\,\cdot,
\tag{A.26}
$$

$$
\hat{p} := -i \frac{\partial}{\partial x},
\tag{A.27}
$$

můžeme Hamiltonův operátor $\hat{H}$ přepsat jako

$$
\hat{H} = \frac{1}{2} \left( \hat{p}^2 + \hat{x}^2 \right).
\tag{A.28}
$$

Tento operátor lze rozložit na součin lineárních členů:

$$
\begin{aligned}
\hat{H} &= \frac{\hat{x} - i\hat{p}}{\sqrt{2}} \frac{\hat{x} + i\hat{p}}{\sqrt{2}} - \frac{i}{2} [\hat{x}, \hat{p}] \\
&= \frac{\hat{x} - i\hat{p}}{\sqrt{2}} \frac{\hat{x} + i\hat{p}}{\sqrt{2}} + \frac{1}{2} \mathbb{1},
\end{aligned}
\tag{A.29}
$$

kde lze využít identitu $[\hat{x}, \hat{p}] = i\mathbb{1}$, kterou snadno ověříme přímým výpočtem. Definujme
*posunovací (žebříkové) operátory* (ladder operators) jako

$$
a := \frac{\hat{x} + i\hat{p}}{\sqrt{2}},
\tag{A.30}
$$

$$
\hat{a}^\dagger := \frac{\hat{x} - i\hat{p}}{\sqrt{2}},
\tag{A.31}
$$

kde $a$ se nazývá *anihilační operátor* (annihilation operator) a $\hat{a}^\dagger$ *kreační operátor* (creation
operator). S tímto značením můžeme hamiltonián přepsat do následujícího jednoduššího tvaru:

$$
\hat{H} = \hat{a}^\dagger a + \frac{1}{2} \mathbb{1}.
\tag{A.32}
$$

**Tvrzení 13.** Každá funkce $\psi_0 : \mathbb{R} \to \mathbb{C}$, pro kterou

$$
a \psi_0 \equiv 0
\tag{A.33}
$$

je vlastní funkcí operátoru $\hat{H}$ s vlastním číslem $E_{\psi_0} = \frac{1}{2}$.

*Důkaz.* Přímým výpočtem dostaneme

$$
\hat{H}\psi_0(x) = \hat{a}^\dagger \underbrace{a\psi_0(x)}_{=0} + \frac{1}{2}\psi_0(x) = \frac{1}{2}\psi_0(x).
\tag{A.34}
$$

∎

Fyzikálně je $\psi_0$ vlastní stav odpovídající vakuu (vacuum) a anihilační operátor aplikovaný na něj dává 0.

**Tvrzení 14.** Funkce $\psi_n := \left(\hat{a}^\dagger\right)^n \psi_0$ jsou rovněž řešeními časově nezávislé
Schrödingerovy rovnice kvantového harmonického oscilátoru, a to s vlastními čísly

$$
E_{\psi_n} := n + \frac{1}{2}.
\tag{A.35}
$$

*Důkaz.* Přímým výpočtem dostaneme

$$
\left[a, \left(\hat{a}^\dagger\right)^n\right] = n \left(\hat{a}^\dagger\right)^{n-1},
\tag{A.36}
$$

a odtud

$$
\left[\hat{H}, \left(\hat{a}^\dagger\right)^n\right] = n \left(\hat{a}^\dagger\right)^n .
\tag{A.37}
$$

Dosazením do časově nezávislé Schrödingerovy rovnice dostaneme

$$
\begin{aligned}
\hat{H} \left(\hat{a}^\dagger\right)^n \psi_0(x)
&= \left[\hat{H}, \left(\hat{a}^\dagger\right)^n\right] \psi_0(x)
+ \left(\hat{a}^\dagger\right)^n \underbrace{\hat{H}\psi_0(x)}_{= \frac{1}{2}\psi_0(x)} \\
&= \left(n + \frac{1}{2}\right) \left(\hat{a}^\dagger\right)^n \psi_0(x).
\end{aligned}
\tag{A.38}
$$

∎

Řešení časově nezávislé Schrödingerovy rovnice tedy lze snadno generovat z $\psi_0$. Vyřešením diferenciální rovnice
$a\psi_0(x) = 0$ dostaneme

$$
\psi_0(x) = A_0 e^{-\frac{x^2}{2}}, \qquad (A_0 \in \mathbb{C}).
\tag{A.39}
$$

Aby byla splněna normovací podmínka, můžeme položit $A_0 = \pi^{-1/4}$. Navíc lze přímo spočítat, že výrazy

$$
\left(\hat{a}^\dagger\right)^n e^{-\frac{x^2}{2}}
= 2^{-n/2} \left( \hat{x} - \frac{\partial}{\partial x} \right)^n e^{-\frac{x^2}{2}}
\tag{A.40}
$$

dávají řešení příslušná vyšším vlastním číslům. Víme tedy, že

$$
\psi_n(x) = A_n H_n(x) e^{-\frac{x^2}{2}},
\tag{A.41}
$$

kde $A_n \in \mathbb{R}$ je nějaký normovací faktor, $H_n(x)$ je nějaký polynom v proměnné $x$ a už víme, že
$A_0 = \pi^{-1/4}$ a $H_0(x) = 1$. Dosazením do časově nezávislé Schrödingerovy rovnice dostaneme následující
diferenciální rovnici:

$$
\frac{\mathrm{d}^2 H_n(x)}{\mathrm{d}x^2} - 2x \frac{\mathrm{d}H_n(x)}{\mathrm{d}x} + 2n H_n(x) = 0,
\tag{A.42}
$$

což je přesně Hermitova diferenciální rovnice [48]. Řešeními těchto diferenciálních rovnic jsou Hermitovy polynomy
(Hermite polynomials) definované vztahem

$$
H_n(x) = (-1)^n e^{x^2} \frac{\mathrm{d}^n}{\mathrm{d}x^n} e^{-x^2}.
\tag{A.43}
$$

Hermitovy polynomy navíc splňují následující relace ortogonality

$$
\int_{\mathbb{R}} H_n(x) H_m(x) e^{-x^2} \,\mathrm{d}x = \sqrt{\pi}\, 2^n n!\, \delta_{nm},
\tag{A.44}
$$

a tedy

$$
\langle \psi_n | \psi_m \rangle = |A_n|^2 \sqrt{\pi}\, 2^n n!\, \delta_{nm},
\tag{A.45}
$$

což znamená, že $\{\psi_n\}_{n=0}^{\infty}$ tvoří ortogonální bázi v $L^2(\mathbb{R})$, takže $\psi_n$ lze normovat
volbou $A_n = 1/\sqrt{\sqrt{\pi}\, 2^n n!}$. Normované vlnové funkce tedy jsou

$$
\psi_n(x) = \frac{1}{\sqrt{\sqrt{\pi}\, 2^n n!}} H_n(x) e^{-\frac{x^2}{2}}.
\tag{A.46}
$$
""",
)

APPENDIX_B = PrimerSection(
    anchor="skripta-b",
    number="B",
    title="První kvantování",
    body=r"""
V tomto dodatku probereme formalismus, který je ve srovnání s formalismem použitým v kapitole 1 elementárnější a
nazývá se *první kvantování* (first quantization). V předchozím výkladu jsme používali *druhé kvantování* (second
quantization), označované také jako reprezentace obsazovacích čísel (occupation number representation).

V mnoha fyzikálních situacích uvažujeme systém složený z několika *nerozlišitelných částic* (indistinguishable
particles), které jsou buď bosony, nebo fermiony. Nerozlišitelnost se projevuje v symetrických vlastnostech složeného
stavu. U *bosonových* systémů jsou všechny možné stavy popisující $n$ částic úplně symetrické. Přesněji: nechť
$\mathcal{H}$ je Hilbertův prostor jedné částice, nechť $\pi \in S_n$, kde $S_n$ je grupa permutací (permutation
group) $n$ prvků, a uvažujme unitární působení $U_\pi : \mathcal{H}^{\otimes n} \to \mathcal{H}^{\otimes n}$ (kde
značíme $\mathcal{H}^{\otimes n} := \mathcal{H} \otimes \cdots \otimes \mathcal{H}$) definované vztahem

$$
U_\pi \psi = U_\pi\, \phi_1 \otimes \cdots \otimes \phi_n = \phi_{\pi(1)} \otimes \cdots \otimes \phi_{\pi(n)}.
\tag{B.1}
$$

Obecně je vektor $\psi \in \mathcal{H}^{\otimes n}$ *úplně symetrický* (totally symmetric), jestliže platí

$$
\forall\, \pi \in S_n : \ U_\pi \psi = \psi.
\tag{B.2}
$$

Pro bosony je $n$-částicový Hilbertův prostor podprostorem $\mathcal{H}^{\otimes n}$ definovaným jako

$$
\mathcal{H}^{\otimes n}\big|_{\mathrm{symm}}
:= \left\{ \psi \in \mathcal{H}^{\otimes n} : U_\pi \psi = \psi,\ \forall\, \pi \in S_n \right\}.
\tag{B.3}
$$

Pro *symetrizovaný tenzorový součin* (symmetrized tensor product) je užitečné zavést zápis
$\phi_1 \vee \cdots \vee \phi_n$:

$$
\phi_1 \vee \cdots \vee \phi_n
:= \frac{1}{\sqrt{n!}} \sum_{\pi \in S_n} \phi_{\pi(1)} \otimes \cdots \otimes \phi_{\pi(n)},
\tag{B.4}
$$

který dává úplně symetrické vektory, tj. $U_\pi\, \phi_1 \vee \cdots \vee \phi_n = \phi_1 \vee \cdots \vee \phi_n$ pro
libovolné $\pi \in S_n$ a $\phi_i \in \mathcal{H}$, a tedy
$\phi_1 \vee \cdots \vee \phi_n \in \mathcal{H}^{\otimes n}\big|_{\mathrm{symm}}$. Lze také ukázat, že vektory tohoto
tvaru generují prostor úplně symetrických vektorů, tj.

$$
\mathcal{H}^{\otimes n}\big|_{\mathrm{symm}} = \mathcal{H}^{\vee n}
:= \operatorname{span}\left\{ \phi_1 \vee \cdots \vee \phi_n \in \mathcal{H}^{\otimes n}\big|_{\mathrm{symm}} \right\}.
\tag{B.5}
$$

Proto se $\mathcal{H}^{\otimes n}\big|_{\mathrm{symm}}$ nazývá *$n$-částicový Hilbertův prostor* (n-particle Hilbert
space) bosonových systémů.

Pomocí vztahu (B.4) lze snadno ověřit, že

$$
\langle \phi_1 \vee \cdots \vee \phi_n | \psi_1 \vee \cdots \vee \psi_n \rangle
= \operatorname{per}\left( \left[ \langle \phi_i | \psi_j \rangle \right]_{i,j=1}^{n} \right),
\tag{B.6}
$$

kde $\operatorname{per}$ označuje permanent ze vztahu (1.52) a $[\langle \phi_i | \psi_j \rangle]_{i,j=1}^{n}$ je
matice sestavená ze skalárních součinů $\langle \phi_i | \psi_j \rangle$. Pomocí tohoto vzorce lze sestrojit ONB v
$\mathcal{H}^{\vee n}$:

**Tvrzení 15 (Fockova báze).** Nechť $B = \{e_1, \dots, e_d\}$ je ortonormální báze v $\mathcal{H}$. Potom

$$
B_n := \left\{ \frac{1}{\sqrt{n_1! \cdots n_d!}}\, e_{i_1} \vee \cdots \vee e_{i_n} : i_1 \leq \cdots \leq i_n \right\}
\tag{B.7}
$$

tvoří ortonormální bázi v $\mathcal{H}^{\vee n}$, kde $n_1, \dots, n_d$ udávají počty opakování indexů seřazených
vzestupně, tj. index $k$ se mezi $i_1, \dots, i_n$ vyskytuje $n_k$-krát.

*Poznámka.* Pro libovolný jednotkový vektor $\psi \in \mathcal{H}$ lze uvažovat symetrizovaný tenzorový součin
$\psi^{\vee n} \in \mathcal{H}^{\vee n}$,

$$
\psi^{\vee n} = \frac{n!}{\sqrt{n!}}\, \psi^{\otimes n} = \sqrt{n!}\, \psi^{\otimes n},
\tag{B.8}
$$

a pro jeho normu na $\mathcal{H}^{\otimes n}$ (indukovanou skalárním součinem na $\mathcal{H}$) dostaneme

$$
\lVert \psi^{\vee n} \rVert^2 = \langle \psi^{\vee n} | \psi^{\vee n} \rangle = n!\,.
\tag{B.9}
$$

Jednotkový vektor tak lze sestrojit jako $\frac{1}{\sqrt{n!}} \psi^{\vee n}$, neboť

$$
\frac{1}{n!} \lVert \psi^{\vee n} \rVert^2 = \frac{1}{n!}\, n! = 1.
\tag{B.10}
$$

Uvažujme nyní bosonový kvantový systém tvořený $\dim \mathcal{H}$ nezávislými optickými módy. Hilbertův prostor
složený ze všech $n$-částicových Hilbertových prostorů se nazývá *bosonový Fockův prostor* (bosonic Fock space), tj.
lze jej zapsat jako přímý součet (direct sum) symetrických $n$-částicových Hilbertových prostorů [49]:

$$
\mathcal{F}(\mathcal{H}) = \bigoplus_{n=0}^{\infty} \mathcal{H}^{\vee n}.
\tag{B.11}
$$

Uzávěr (closure) je potřeba proto, aby i bosonový Fockův prostor byl Hilbertovým prostorem. Prostor $\mathcal{H}$
obvykle nazýváme *jednočásticový Hilbertův prostor* (one-particle Hilbert space), zatímco $\mathcal{H}^{\vee n}$ je,
jak už bylo řečeno, $n$-částicový Hilbertův prostor. Podle konvence se přitom klade
$\mathcal{H}^{\vee 0} \cong \mathbb{C}$, což odpovídá vakuu.

*(Pozn. překl.: Uzávěr se obvykle vyznačuje pruhem,
$\mathcal{F}(\mathcal{H}) = \overline{\bigoplus_{n} \mathcal{H}^{\vee n}}$, který ve vztahu (B.11) v originálu chybí.
Jde o uzávěr algebraického přímého součtu, jehož prvky mají jen konečně mnoho nenulových složek.)*

Formalismus druhého kvantování poskytuje intuitivní jazyk pro popis bosonových systémů a používá se i při popisu
fotonického kvantového počítání. V tomto formalismu hrají zásadní roli bosonové anihilační a kreační operátory.

**Definice B.0.1 (Bosonový kreační a anihilační operátor).** Nechť $\mathcal{H}$ je jednočásticový Hilbertův prostor
bosonového systému. Kreační operátor příslušný jednočásticovému vektoru $\psi \in \mathcal{H}$ je neomezený operátor
$\hat{a}^\dagger(\psi)$ na $\mathcal{F}(\mathcal{H})$, který zobrazuje $n$-částicový vektor na $(n+1)$-částicový
vektor následujícím způsobem:

$$
\hat{a}^\dagger(\psi) : \phi_1 \vee \cdots \vee \phi_n \mapsto \psi \vee \phi_1 \vee \cdots \vee \phi_n .
\tag{B.12}
$$

Anihilační operátor $a(\psi)$ je neomezený operátor na $\mathcal{F}(\mathcal{H})$, který zobrazuje $n$-částicový
vektor na $(n-1)$-částicový vektor následujícím způsobem:

$$
a(\psi) : \phi_1 \vee \cdots \vee \phi_n \mapsto
\sum_{i=1}^{n} \langle \psi | \phi_i \rangle\,
\phi_1 \vee \cdots \vee \phi_{i-1} \vee \phi_{i+1} \vee \cdots \vee \phi_n .
\tag{B.13}
$$

Kreačním a anihilačním operátorům se často říká *posunovací (žebříkové) operátory*.

Uvažujme jednoduchý případ, kdy je jednočásticový Hilbertův prostor $\mathcal{H}_1$ jednorozměrný, což odpovídá
systému s jediným bosonovým módem. Při volbě jednotkového vektoru $\psi$ lze působení $\hat{a}^\dagger(\psi)$ vyjádřit
jako

$$
\hat{a}^\dagger(\psi) : \psi^{\vee n} \mapsto \psi^{\vee (n+1)},
\tag{B.14}
$$

a působení anihilačního operátoru jako

$$
a(\psi) : \psi^{\vee n} \mapsto n \psi^{\vee (n-1)},
\tag{B.15}
$$

kde $\psi^{\vee 0} := \psi^{\otimes 0} := 1$; s využitím $\psi^{\vee n} = \sqrt{n!}\, \psi^{\otimes n}$ dostaneme

$$
\begin{aligned}
\hat{a}^\dagger(\psi) &: \sqrt{n!}\, \psi^{\otimes n} \mapsto \sqrt{(n+1)!}\, \psi^{\otimes (n+1)}, \\
a(\psi) &: \sqrt{n!}\, \psi^{\otimes n} \mapsto \sqrt{n} \sqrt{n!}\, \psi^{\otimes (n-1)}.
\end{aligned}
\tag{B.16}
$$

Lze také použít zápis pomocí obsazovacích čísel (occupation number notation):

$$
\begin{aligned}
|n\rangle &:= \frac{1}{\sqrt{n!}}\, \psi^{\vee n}, \\
\hat{a}^\dagger &:= \hat{a}^\dagger(\psi), \\
a &:= a(\psi),
\end{aligned}
\tag{B.17}
$$

s nímž se vztah (B.14) zjednoduší na

$$
\begin{aligned}
\hat{a}^\dagger |n\rangle &= \sqrt{n+1}\, |n+1\rangle, \\
a |n\rangle &= \sqrt{n}\, |n-1\rangle.
\end{aligned}
\tag{B.18}
$$

Všimněme si, že $|n\rangle$ je z konstrukce normovaný, tj. $\langle n|n\rangle = 1$. Z definice je také zřejmé, že
$\langle n|m\rangle = \delta_{nm}$ pro $n, m \in \mathbb{N}$, kde $\delta_{nm}$ označuje Kroneckerovo delta. Množina
vektorů

$$
\left\{ |n\rangle \in \mathcal{F}(\mathcal{H}_1) : n \in \mathbb{N}_0 \right\}
\tag{B.19}
$$

tvoří ortonormální bázi v $\mathcal{F}(\mathcal{H}_1)$, kde $\mathcal{H}_1$ je jednorozměrný Hilbertův prostor
$\mathbb{C}$. Zobecněme předchozí úvahy a uvažujme nyní systém s $d$ bosonovými módy. Bosonovým Fockovým prostorem je
v tomto případě $\mathcal{F}(\mathcal{H})$, kde $\mathcal{H}$ je $d$-rozměrný Hilbertův prostor. Vezmeme-li ONB
jednočásticového Hilbertova prostoru $\{e_1, \dots, e_d\} \subset \mathcal{H}$, lze těchto $d$ bázových vektorů
přiřadit $d$ bosonovým módům systému. Podobně jako v jednomódovém případě tak lze stavy Fockovy báze definovat pomocí
báze v $\mathcal{F}(\mathcal{H})$, kterou podle tvrzení 15 sestrojíme z ONB jednočásticového Hilbertova prostoru:

$$
|n_1, \dots, n_d\rangle := \frac{1}{\sqrt{n_1! \dots n_d!}}\, e_{i_1} \vee \cdots \vee e_{i_n}.
\tag{B.20}
$$

Pro pevně zvolenou ONB v $\mathcal{H}$ lze používat kompaktní zápis $\hat{a}_i^\dagger := \hat{a}^\dagger(e_i)$,
$a_i := a(e_i)$. Snadno se ověří, že tyto operátory působí na sestrojenou ONB takto:

$$
\begin{aligned}
\hat{a}_j^\dagger |n_1, \dots, n_j, \dots, n_d\rangle &= \sqrt{n_j + 1}\, |n_1, \dots, n_j + 1, \dots, n_d\rangle, \\
\hat{a}_j |n_1, \dots, n_j, \dots, n_d\rangle &= \sqrt{n_j}\, |n_1, \dots, n_j - 1, \dots, n_d\rangle.
\end{aligned}
\tag{B.21}
$$

Pro kreační a anihilační operátory platí následující relace:

$$
\begin{aligned}
{[a_i, \hat{a}_j^\dagger]} &= \delta_{ij} \mathbb{1}, \\
{[a_i, \hat{a}_j]} &= [\hat{a}_i^\dagger, \hat{a}_j^\dagger] = 0,
\end{aligned}
\tag{B.22}
$$

pro všechna $i, j \in [d]$.
""",
)

CHAPTER = PrimerChapter(
    label="Dodatky A a B",
    title="Základy kvantové mechaniky a první kvantování",
    intro=r"""
**Dodatek A – Opakování: základy kvantové mechaniky.** Tento dodatek pro referenci připomíná minimální základy
kvantové mechaniky, které tato práce potřebuje, a činí tak formou několika postulátů. Podrobnější výklad kvantové
mechaniky a kvantového počítání najde čtenář v [2].
""",
    sections=(
        SECTION_A_1,
        SECTION_A_2,
        SECTION_A_3,
        SECTION_A_4,
        SECTION_A_5,
        SECTION_A_6,
        APPENDIX_B,
    ),
    original_pages="42–51",
)
