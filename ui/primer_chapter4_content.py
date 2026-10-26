"""Czech translation of chapter 4 of the primer by Kolarovszki and Zimborás (ui/primer_content.py)."""

from __future__ import annotations

from ui.primer_content import PrimerChapter, PrimerSection

SECTION_4_1 = PrimerSection(
    anchor="skripta-4-1",
    number="4.1",
    title="Pravděpodobnosti detekce počtu částic u gaussovských stavů",
    body=r"""
Gaussian Boson Sampling (GBS), tedy detekci fotonů na obecném gaussovském stavu (Gaussian state), poprvé zavedly
práce [30, 42]. Podobně jako u standardního Boson Samplingu rostou klasické výpočetní prostředky potřebné k odebrání
vzorku (sample) ze složitého pravděpodobnostního rozdělení gaussovských fotonických stavů zpravidla exponenciálně
s počtem zúčastněných fotonů, takže úloha je pro klasické počítače nezvládnutelná (classically intractable). Jak
ukážeme v tomto oddílu, složitost odebrání vzorku z neposunutého (non-displaced) gaussovského stavu je dána výpočtem
maticové funkce zvané *hafnián* (hafnian) [43].

Uvažujme $d$-módový gaussovský stav s operátorem hustoty (density operator) $\rho$. Pravděpodobnost, že naměříme
počty částic $\mathbf{n} = (n_1, \dots, n_d)$, je dána Bornovým pravidlem:

$$
p(\mathbf{n}) := \operatorname{Tr}\left[\rho\, |\mathbf{n}\rangle\langle\mathbf{n}|\right].
\tag{4.1}
$$

V tomto odvození použijeme formulaci kvantové optiky ve fázovém prostoru (phase space), kterou jsme zavedli
v kapitole 3. Podle věty 3.4.2 můžeme psát

$$
|\mathbf{n}\rangle\langle\mathbf{n}|
= \int_{\mathbb{C}^d} P_{|\mathbf{n}\rangle\langle\mathbf{n}|}(\pmb{\alpha})\,
|\pmb{\alpha}\rangle\langle\pmb{\alpha}|\, \mathrm{d}\pmb{\alpha},
\tag{4.2}
$$

kde $\mathrm{d}\pmb{\alpha} = \prod_{i=1}^d \mathrm{d}^2\alpha_i$. Pravděpodobnost tedy můžeme přepsat jako

$$
p(\mathbf{n}) = \pi^d \int_{\mathbb{C}^d} Q_\rho(\pmb{\alpha})\,
P_{|\mathbf{n}\rangle\langle\mathbf{n}|}(\pmb{\alpha})\, \mathrm{d}\pmb{\alpha}.
\tag{4.3}
$$

Zobecněním vztahu (3.72) na více módů dostaneme

$$
P_{|\mathbf{n}\rangle\langle\mathbf{n}|}(\pmb{\alpha})
= \frac{e^{\lVert\pmb{\alpha}\rVert^2}}{\mathbf{n}!}
\left(\frac{\partial^2}{\partial\pmb{\alpha}\,\partial\overline{\pmb{\alpha}}}\right)^{\mathbf{n}}
\delta^{(2d)}(\pmb{\alpha}),
\tag{4.4}
$$

kde $\delta^{(2d)}(\pmb{\alpha}) := \delta^{(2)}(\alpha_1) \cdots \delta^{(2)}(\alpha_d)$. Pomocí tvrzení 11 můžeme
psát

$$
\begin{aligned}
p(\mathbf{n}) &= \frac{1}{\mathbf{n}!\sqrt{\det\Sigma}}
\left. \left(\frac{\partial^2}{\partial\pmb{\alpha}\,\partial\overline{\pmb{\alpha}}}\right)^{\mathbf{n}}
e^{\lVert\pmb{\alpha}\rVert^2}
\exp\!\left(-\frac{1}{2}\check{\pmb{\alpha}}^\dagger \Sigma^{-1} \check{\pmb{\alpha}}\right)
\right|_{\pmb{\alpha}=\mathbf{0}} \\
&= \frac{1}{\mathbf{n}!\sqrt{\det\Sigma}}
\left. \left(\frac{\partial^2}{\partial\pmb{\alpha}\,\partial\overline{\pmb{\alpha}}}\right)^{\mathbf{n}}
\exp\!\left(\frac{1}{2}\check{\pmb{\alpha}}^T A \check{\pmb{\alpha}}\right)
\right|_{\pmb{\alpha}=\mathbf{0}},
\end{aligned}
\tag{4.5}
$$

kde jsme označili

$$
A := X(\mathbb{1} - \Sigma^{-1}),
\tag{4.6}
$$

$$
X := \begin{bmatrix} 0 & \mathbb{1} \\ \mathbb{1} & 0 \end{bmatrix}.
\tag{4.7}
$$

Matice $X$ zde slouží k „překlopení“ $\check{\pmb{\alpha}}^\dagger$ na $\check{\pmb{\alpha}}^T$, tj.
$\check{\pmb{\alpha}}^\dagger X = \check{\pmb{\alpha}}^T$. Nakonec podle tvrzení 9 víme, že

$$
\left. \left(\frac{\partial^2}{\partial\pmb{\alpha}\,\partial\overline{\pmb{\alpha}}}\right)^{\mathbf{n}}
\exp\!\left(\frac{1}{2}\check{\pmb{\alpha}}^T A \check{\pmb{\alpha}}\right)
\right|_{\pmb{\alpha}=\mathbf{0}}
= \operatorname{haf}(\mathrm{br}_{\mathbf{n}} A),
\tag{4.8}
$$

kde $\mathrm{br}_{\mathbf{n}} := \mathrm{r}_{\mathbf{n}\oplus\mathbf{n}}$. Složením všech kroků dostaneme

$$
p(\mathbf{n}) = \frac{\operatorname{haf}(\mathrm{br}_{\mathbf{n}} A)}{\mathbf{n}!\sqrt{\det\Sigma}}.
\tag{4.9}
$$

Je-li gaussovský stav čistý, lze $A$ zapsat jako

$$
A = \begin{bmatrix} B & \\ & \overline{B} \end{bmatrix},
\tag{4.10}
$$

kde

$$
B = U \tanh(\mathbf{r})\, U^T
\tag{4.11}
$$

pro nějakou unitární matici $U$ řádu $d$, která odpovídá interferometru, a $\mathbf{r} \ge 0$, které odpovídá vrstvě
stlačovacích hradel (squeezing gates). V tomto případě – díky tomu, že se hafnián přímého součtu matic rozpadá na
součin hafniánů jednotlivých bloků – můžeme psát
$\operatorname{haf}(\mathrm{br}_{\mathbf{n}} A) = |\operatorname{haf}(\mathrm{r}_{\mathbf{n}} B)|^2$, z čehož plyne

$$
p(\mathbf{n}) = \frac{|\operatorname{haf}(\mathrm{r}_{\mathbf{n}} B)|^2}{\mathbf{n}!\sqrt{\det\Sigma}}.
\tag{4.12}
$$
""",
)

SECTION_4_2 = PrimerSection(
    anchor="skripta-4-2",
    number="4.2",
    title="Vlastnosti hafniánu a souvislost s teorií grafů",
    body=r"""
Abychom hafnián propojili s počtem perfektních párování (perfect matchings) v grafu, musíme si zopakovat několik
pojmů z teorie grafů.

### 4.2.1 Opakování: teorie grafů

Pro úplnost zde uvádíme definici grafu. Pro jednoduchost se v tomto kurzu nebudeme zabývat váženými (weighted),
znaménkovými (signed) ani orientovanými (directed) grafy.

**Definice 4.2.1 (Graf).** *Graf* (graph) je uspořádaná dvojice $G = (V, E)$, kde $V$ je konečná množina *vrcholů*
(vertices, též uzlů – nodes) a $E \subseteq \{\{u, v\} \mid u, v \in V,\ u \neq v\}$ je množina *hran* (edges),
které spojují dvojice různých vrcholů.

Grafy lze reprezentovat jejich maticí sousednosti:

**Definice 4.2.2 (Matice sousednosti).** Graf lze reprezentovat jeho *maticí sousednosti* (adjacency matrix) $A$, což
je čtvercová matice řádu $|V|$ s prvky $A_{ij} = 1$, pokud $(i, j) \in E$, tj. pokud mezi $i$-tým a $j$-tým vrcholem
vede hrana, a $A_{ij} = 0$ jinak.

Matice sousednosti (neorientovaného) grafu je symetrická, tj. $A^T = A$. Pojem grafů, v nichž je „každý spojen
s každým“ (all-to-all connected), vystihuje následující definice:

**Definice 4.2.3 (Úplný graf).** Graf se nazývá *úplný* (complete), jestliže každou dvojici jeho vrcholů spojuje
hrana.

**Definice 4.2.4 (Hustota podgrafu).** Mějme graf $G = (V, E)$ a jeho podgraf (subgraph) $S = (V_S, E_S)$. *Hustotou*
(density) podgrafu $S$ nazýváme poměr

$$
d(S) = \frac{|E_S|}{\binom{|V_S|}{2}}.
$$

**Definice 4.2.5 (Bipartitní graf).** *Bipartitní graf* (bipartite graph) je graf, jehož vrcholy lze rozdělit do dvou
disjunktních nezávislých množin (independent sets) tak, že každá hrana spojuje vrchol z jedné množiny s vrcholem
z druhé množiny.

Matici sousednosti takového grafu lze zapsat jako

$$
A = \begin{bmatrix} 0 & B \\ B^T & 0 \end{bmatrix}.
\tag{4.13}
$$

Matice $B$ se někdy nazývá *biadjacenční matice* (biadjacency matrix).

Párování (matchings) patří k základním strukturám teorie grafů – vystihují představu, že vrcholy spojujeme do
dvojic. Zvlášť důležitou roli mezi nimi hrají perfektní párování, protože odpovídají úplnému spárování celé množiny
vrcholů.

**Definice 4.2.6 (Perfektní párování).** Nechť $G = (V, E)$ je neorientovaný graf. *Perfektní párování* (perfect
matching) $M \subseteq E$ je množina hran taková, že každý vrchol $v \in V$ je incidentní právě s jednou hranou z $M$.
Ekvivalentně: $M$ je párování, které pokrývá všechny vrcholy grafu $G$. Množinu perfektních párování značíme
$\mathrm{PM}(G)$.

### 4.2.2 Perfektní párování a hafnián

Permanent matice vstupuje do hry, když chceme spočítat perfektní párování v bipartitním grafu. Pro
bipartitní graf je počet perfektních párování dán permanentem jeho biadjacenční matice $B$ rozměru $n \times n$.
Každý nenulový součin v definici permanentu odpovídá jednomu perfektnímu párování a permanent sečte všechna taková
párování. Pro bipartitní graf $G$ s maticí sousednosti tvaru

$$
A = \begin{bmatrix} 0 & B \\ B^T & 0 \end{bmatrix}
\tag{4.14}
$$

tedy můžeme psát

$$
\operatorname{per}(B) = |\mathrm{PM}(G)|.
\tag{4.15}
$$

Podobně platí klíčové pozorování, že hafnián matice $A$ je roven počtu perfektních párování grafu, tj. pro bipartitní
graf $G$ s maticí sousednosti $A$ můžeme psát

$$
\operatorname{haf}(A) = |\mathrm{PM}(G)|.
\tag{4.16}
$$

Je to logické: v definici hafniánu procházíme všechna perfektní párování z množiny $\mathrm{PM}([n])$, kde $n$ je počet
vrcholů, a člen součtu přispěje jedničkou jen tehdy, je-li dané perfektní párování z $\mathrm{PM}([n])$ zároveň
perfektním párováním grafu $G$.

*(Pozn. překl.: Jak ukazuje právě toto zdůvodnění, rovnost (4.16) platí pro každý neorientovaný graf bez vah
a smyček, nejen pro bipartitní. Pro bipartitní graf s maticí (4.14) navíc
$\operatorname{haf}(A) = \operatorname{per}(B)$, ve shodě s (4.15).)*
""",
)

SECTION_4_3 = PrimerSection(
    anchor="skripta-4-3",
    number="4.3",
    title="Hledání hustých podgrafů pomocí Gaussian Boson Samplingu",
    body=r"""
Vnořením (embedding) matice sousednosti $A$ do uspořádání GBS získáme vzorkovač (sampler), který přednostně
dává výsledky odpovídající podgrafům s velkým počtem perfektních párování. Této vlastnosti lze využít v aplikacích GBS
na grafové úlohy, například při hledání hustých podgrafů (dense subgraphs), protože grafy s mnoha perfektními
párováními bývají zpravidla husté. GBS tak může urychlit heuristické klasické algoritmy, které jako podprogram
využívají vzorkování (sampling) podgrafů. Patří mezi ně i stochastický algoritmus pro problém nejhustšího podgrafu
o $k$ vrcholech (densest $k$-subgraph problem) [31], který zní takto:

**Problém (nejhustší podgraf o $k$ vrcholech).** Pro daný graf $G$ a $k < |G|$ najděte podgraf o $k$ vrcholech
s největší hustotou.

Problém má přirozenou souvislost s úlohami shlukování (clustering), jejichž cílem je najít silně korelované
podmnožiny dat, a proto má široké spektrum aplikací. Tento problém je však NP-těžký (NP-hard) [44] a předpokládá se,
že neefektivní je i jeho aproximace [45]. Panuje však přesvědčení, že pro hledání hustých podgrafů o $k$ vrcholech
jsou užitečnější stochastické algoritmy.

Představíme hybridní stochastický algoritmus, který pomocí GBS získává kandidáty na husté podgrafy; původně byl
popsán v práci [31]. Podle předchozích úvah je pravděpodobnost pozorování dané konfigurace fotonů úměrná počtu
perfektních párování odpovídajícího podgrafu. Intuitivně lze navíc čekat, že graf s mnoha perfektními párováními
obsahuje mnoho hran. Rigorózně to bylo ukázáno v práci [46].

*(Pozn. překl.: Přesněji: pro čistý stav s $B$ úměrnou $A$ a bezkolizní vzorek s pevným počtem fotonů je podle
(4.12) tato pravděpodobnost úměrná čtverci počtu perfektních párování, $|\operatorname{haf}(\mathrm{r}_S A)|^2$,
s nímž pracuje i algoritmus 1 níže.)*

Předpokládejme zatím, že umíme matici sousednosti vnořit do obvodu GBS a získávat vzorky odpovídající podgrafům
s vysokým počtem perfektních párování; tomu budeme říkat průzkum (exploration). Získané vzorky však můžeme také
využít (exploitation), tj. navrhnout vylepšenou strategii, která vzorky z GBS dále upravuje (tweak), aby se případně
dosáhlo dalšího zlepšení. Takovou strategii úprav popisuje algoritmus 1. Tento algoritmus lze použít uvnitř
optimalizačního algoritmu, který hledá husté podgrafy, např. v simulovaném žíhání (simulated annealing). Je důležité
zmínit, že z výsledných vzorků musíme dodatečně vybrat (post-select) ty, které odpovídají podgrafům o $k$ vrcholech,
tj. vzorky obsahující pouze nuly a jedničky (tzv. *bezkolizní* vzorky, collision-free samples), v nichž je počet
jedniček přesně $k$. V takovém vzorku odpovídají indexy, na nichž stojí jedničky, indexům vrcholů vzorkovaného
podgrafu.

---

**Algoritmus 1: GBS-Tweak**

**Vstup:** graf $G$ s maticí sousednosti $A$ a podgraf $S$ s maticí sousednosti $\mathrm{r}_S A$, $d := |G|$,
$k := |S|$; $l$ je minimální počet vrcholů, které se ponechají.

**Výstup:** podgraf grafu $G$ o $k$ vrcholech.

**1.** Vygeneruj $R$ jako podgraf grafu $S$ o $l$ vrcholech s maticí sousednosti $\mathrm{r}_R \mathrm{r}_S A$ podle
rozdělení GBS

$$
p(R \mid S) \propto \left|\operatorname{haf}(\mathrm{r}_R \mathrm{r}_S A)\right|^2 .
$$

Rozšiř $R$ o $m$ zbývajících vrcholů z $S$ spolu s příslušnými hranami, kde $m \in \{0, 1, \dots, k - l - 1\}$ je
rovnoměrně náhodně zvolené číslo. Tím vznikne podgraf $G_{\text{keep}}$ o $l + m$ vrcholech.

**2.** Vygeneruj $T$ jako podgraf grafu $G$ o $k - l$ vrcholech s maticí sousednosti $\mathrm{r}_T A$ podle
rozdělení GBS

$$
p(T) \propto \left|\operatorname{haf}(\mathrm{r}_T A)\right|^2 .
$$

Zmenši $T$ tak, že náhodně vyřadíš $m$ jeho vrcholů (a příslušné hrany). Tím vznikne podgraf $G_{\text{replace}}$
o $k - l - m$ vrcholech. Pokud mají $G_{\text{keep}}$ a $G_{\text{replace}}$ nějaký společný vrchol, tento krok
opakuj.

**3.** Vrať podgraf o $k$ vrcholech

$$
G_{\text{keep}} \cup G_{\text{replace}} .
$$

---

K řešení grafových úloh pomocí GBS budeme potřebovat vnořit matice sousednosti grafů do fotonického kvantového
obvodu. To lze provést pomocí následujícího rozkladu:

**Věta 4.3.1 (Takagiho–Autonneho rozklad, Takagi–Autonne decomposition).** Nechť $A \in \mathbb{C}^{n \times n}$ je
komplexní symetrická matice, tj. $A^T = A$. Pak existují unitární matice $U \in \mathbb{C}^{n \times n}$ a diagonální
matice $D = \operatorname{diag}(\sigma_1, \dots, \sigma_n)$ s nezápornými reálnými prvky takové, že

$$
A = U D U^T.
$$

Diagonální prvky $\sigma_i$ jsou určeny jednoznačně až na pořadí a jsou to *singulární čísla* (singular values)
matice $A$.

*Důkaz.* Důkaz této věty vynecháme, najdete ho v práci [47]. ∎

Díky tomu můžeme libovolnou matici sousednosti zapsat ve tvaru matice $B$ z rovnice (4.11). Matice $D$ přitom
odpovídá vrstvě stlačovacích hradel a $U$ matici interferometru v obvodu. Všimněte si, že matici sousednosti lze
libovolně přeškálovat, což odpovídá nastavení středního počtu fotonů pomocí parametrů stlačení (squeezing).
""",
)

SECTION_4_4 = PrimerSection(
    anchor="skripta-4-4",
    number="4.4",
    title="Cvičení",
    body=r"""
**Cvičení 4.4.1.** Ukažte, že je-li gaussovský stav čistý, lze $A$ zapsat jako

$$
A = \begin{bmatrix} B & \\ & \overline{B} \end{bmatrix}.
\tag{4.17}
$$

*Řešení.* Víme, že kovarianční matici (covariance matrix) libovolného čistého $d$-módového gaussovského stavu lze
zapsat jako

$$
\sigma^{(\mathrm{c})} = S S^\dagger,
\tag{4.18}
$$

kde $S \in \mathrm{Sp}^{(\mathrm{c})}(2d, \mathbb{R})$. Podle Blochova–Messiahova rozkladu (Bloch–Messiah
decomposition) ji můžeme zapsat jako

$$
\sigma^{(\mathrm{c})} = V \sigma^{(\mathrm{c})}_{\text{squeezed}} V^\dagger,
\tag{4.19}
$$

kde $\sigma^{(\mathrm{c})}_{\text{squeezed}}$ odpovídá $d$ nezávislým stlačeným stavům (squeezed states) jako
počátečním stavům a je to kovarianční matice

$$
\sigma^{(\mathrm{c})}_{\text{squeezed}}
= \begin{bmatrix} \cosh\mathbf{r} & -\sinh\mathbf{r} \\ -\sinh\mathbf{r} & \cosh\mathbf{r} \end{bmatrix}.
\tag{4.20}
$$

Dále má $V$ tvar

$$
V = \begin{bmatrix} U & \\ & \overline{U} \end{bmatrix},
\tag{4.21}
$$

kde $U \in \mathrm{U}(d)$ je matice interferometru. Můžeme psát

$$
\begin{aligned}
\Sigma &= \frac{1}{2}\left(\mathbb{1} + \sigma^{(\mathrm{c})}\right)
= V \frac{1}{2}\left(\mathbb{1} + \sigma^{(\mathrm{c})}_{\text{squeezed}}\right) V^\dagger \\
&=: V \Sigma_{\text{squeezed}} V^\dagger,
\end{aligned}
\tag{4.22}
$$

kde $\Sigma_{\text{squeezed}}$ je Q-matice (Q-matrix) počátečních stlačených stavů, a tedy

$$
A = X(\mathbb{1} - \Sigma^{-1}) = X V (\mathbb{1} - \Sigma^{-1}_{\text{squeezed}}) V^\dagger.
\tag{4.23}
$$

Podle vztahu (3.93) víme, že inverze Q-matice jednomódového stlačeného stavu je

$$
\begin{bmatrix} 1 & e^{i\phi}\tanh(r) \\ e^{-i\phi}\tanh(r) & 1 \end{bmatrix},
\tag{4.24}
$$

a pro pohodlí můžeme pro všechna stlačovací hradla jednotně zvolit $\phi = \pi/2$. To smíme udělat volně, protože jde
jen o fázi, kterou lze přesunout do interferometru. Po této úpravě můžeme psát

$$
\Sigma^{-1}_{\text{squeezed}}
= \begin{bmatrix} \mathbb{1} & -\tanh(r) \\ -\tanh(r) & \mathbb{1} \end{bmatrix},
\tag{4.25}
$$

a tedy

$$
\begin{aligned}
A &= X V \begin{bmatrix} & \tanh(r) \\ \tanh(r) & \end{bmatrix} V^\dagger \\
&= X \begin{bmatrix} & U \tanh(r) U^T \\ \overline{U} \tanh(r) U^\dagger & \end{bmatrix}
\end{aligned}
\tag{4.26}
$$

$$
= \begin{bmatrix} \overline{U} \tanh(r) U^\dagger & \\ & U \tanh(r) U^T \end{bmatrix}
=: \begin{bmatrix} B & \\ & \overline{B} \end{bmatrix}.
\tag{4.27}
$$

*(Pozn. překl.: Řešení obsahuje tři nepřesnosti, které závěr cvičení nemění. (i) Kovarianční matice stlačeného
vakua má podle (2.73) prvky $\cosh(2\mathbf{r})$ a $-\sinh(2\mathbf{r})$; matice v (4.20) je symplektická matice
stlačení $D$ z (2.56) a kovarianční matice je teprve $D D^\dagger$. Právě s argumentem $2\mathbf{r}$ vyjde v (4.24)
$\tanh(r)$. (ii) Aby z (4.24) vyšlo (4.25), musí platit $e^{i\phi} = -1$, tedy $\phi = \pi$; volba $\phi = \pi/2$
by dala mimodiagonální prvky $i\tanh(r)$ a $-i\tanh(r)$. (iii) V (4.27) vychází
$B = \overline{U}\tanh(r)U^\dagger$, tedy matice komplexně sdružená k (4.11); protože $U$ je libovolná unitární
matice, stačí ji přeznačit, $U \to \overline{U}$.)*

**Cvičení 4.4.2.** Uvažujte graf s maticí sousednosti

```python
adjacency_matrix = np.array(
    [
        [0, 1, 0, 0, 0, 0, 0, 1, 1, 0],
        [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
        [0, 1, 1, 0, 1, 0, 1, 1, 1, 0],
    ]
)
```

a vnořte ho do obvodu v Piquassu pomocí instrukce `Graph`. Vzorkujte podgrafy pomocí `ParticleNumberMeasurement`.
Pomocí `Result.to_subgraph_nodes` převeďte vzorky na indexy vrcholů a vyfiltrujte bezkolizní vzorky odpovídající
podgrafům o $k$ vrcholech (tj. ponechte jen je). Aby bylo užitečných vzorků co nejvíce, upravte parametr
`mean_photon_number` instrukce `Graph`.

*Řešení.* Úlohu by měl vyřešit následující kód:

```python
import numpy as np
import networkx as nx
import piquasso as pq


adjacency_matrix = np.array(
    [
        [0, 1, 0, 0, 0, 0, 0, 1, 1, 0],
        [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
        [0, 1, 1, 0, 1, 0, 1, 1, 1, 0],
    ]
)


def postselect(subgraph_nodes, k):
    result = []

    for subgraph in subgraph_nodes:
        if len(subgraph) == len(np.unique(subgraph)) and len(subgraph) == k:
            result.append(subgraph)

    return result


shots = 1000
k = 6

with pq.Program() as program:
    pq.Q() | pq.Vacuum() | pq.Graph(
        adjacency_matrix, mean_photon_number=k / len(adjacency_matrix)
    ) | pq.ParticleNumberMeasurement()


simulator = pq.GaussianSimulator(d=len(adjacency_matrix))

result = simulator.execute(program, shots=shots)

dense_subgraph_nodes = result.to_subgraph_nodes()

filtered_dense_subgraph_nodes = postselect(dense_subgraph_nodes, k)

graph = nx.from_numpy_array(adjacency_matrix)

for i, x in enumerate(filtered_dense_subgraph_nodes):
    subgraph = graph.subgraph(x)
    print(f"Graph {i}: {subgraph} (density: {nx.density(subgraph)})")
```

**Cvičení 4.4.3.** Implementujte algoritmus GBS-Tweak (algoritmus 1) pomocí knihovny `networkx` a předchozího
cvičení.

*Řešení.* Viz přiložený notebook.

**Cvičení 4.4.4.** Pomocí algoritmu GBS-Tweak implementujte jednoduchý algoritmus simulovaného žíhání pro hledání
hustých podgrafů o $k$ vrcholech.

*Řešení.* Viz přiložený notebook.
""",
)

CHAPTER = PrimerChapter(
    label="Kapitola 4",
    title="Gaussian Boson Sampling",
    intro="",
    sections=(SECTION_4_1, SECTION_4_2, SECTION_4_3, SECTION_4_4),
    original_pages="36–41",
)
