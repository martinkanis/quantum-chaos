"""Czech translation of chapter 2 of the primer by Kolarovszki and Zimborás (ui/primer_content.py)."""

from __future__ import annotations

from ui.primer_content import PrimerChapter, PrimerSection

INTRO = r"""
V této kapitole zavedeme pojem gaussovských stavů (Gaussian states)¹. Množina gaussovských stavů má mnoho
zajímavých vlastností a obecně se považuje za dobře zvládnutelnou (tractable) podmnožinu všech fotonických kvantových
stavů. Tato kapitola se však už dobře prošlapané oblasti gaussovských stavů věnuje jen povrchně. Více informací
o gaussovských stavech najde čtenář v pracích [38, 33].

Kapitolu zahájíme představením několika elementárních fotonických stavů, které jsou zároveň elementárními příklady
gaussovských stavů.

¹ V těchto skriptech označuje termín gaussovské stavy *bosonové gaussovské stavy* (bosonic Gaussian states).
"""

SECTION_2_1 = PrimerSection(
    anchor="skripta-2-1",
    number="2.1",
    title="Elementární fotonické kvantové stavy",
    body=r"""
Vakuový stav (vacuum state) a stavy Fockovy báze (Fock basis states) jsme už zavedli v oddílu 1.1 v souvislosti
s kreačními a anihilačními operátory (creation and annihilation operators), podrobné definice jsme však vynechali:

**Definice 2.1.1 (Vakuový stav).** *Vakuový stav* (vakuum) je definován vztahem

$$
\hat a_i |0\rangle = 0, \qquad \forall\, i \in [d],
\tag{2.1}
$$

kde index $i$ označuje módy systému.

Stavy, které vzniknou působením stlačovacího hradla (squeezing gate) na vakuum jako počáteční stav, se nazývají
stlačené stavy (squeezed states):

**Definice 2.1.2 (Stlačený stav).** Jednomódový *stlačený stav* je definován jako

$$
|z\rangle := S(z)\, |0\rangle,
\tag{2.2}
$$

kde $z \in \mathbb{C}$.

Podobně stavy, které vzniknou z vakua jako počátečního stavu působením hradla posunutí (displacement gate), se
nazývají koherentní stavy (coherent states):

**Definice 2.1.3 (Koherentní stav).** Jednomódový (kanonický) *koherentní stav* je definován jako

$$
|\alpha\rangle := D(\alpha)\, |0\rangle,
\tag{2.3}
$$

kde $\alpha \in \mathbb{C}$.

*Poznámka.* Stlačené a koherentní stavy se značí velmi podobně. Rozdíl je v tom, že koherentní stavy označujeme
řeckými písmeny (obvykle $\alpha$) a stlačené stavy latinskými písmeny (obvykle $z$).

Vakuum, stlačené a koherentní stavy jsou čisté stavy (pure states). Běžným smíšeným stavem (mixed state) je tepelný
stav (thermal state), který se místo stavovým vektorem modeluje *operátorem hustoty* (density operator):

**Definice 2.1.4 (Tepelný stav).** Operátor hustoty jednomódového tepelného stavu je definován jako

$$
\rho = \sum_{n=0}^{\infty} \frac{\overline{n}^{\,n}}{(1 + \overline{n})^{n+1}}\, |n\rangle\langle n|,
\tag{2.4}
$$

kde $\overline{n} = \operatorname{Tr}[\rho\, \hat n]$ je střední počet fotonů.

Vakuum, koherentní, stlačené a tepelné stavy patří do třídy fotonických kvantových stavů, které se nazývají
*gaussovské stavy*. Stavy Fockovy báze však s výjimkou vakua gaussovské *nejsou*.
""",
)

SECTION_2_2 = PrimerSection(
    anchor="skripta-2-2",
    number="2.2",
    title="Lineární hradla a symplektická grupa",
    body=r"""
Než zavedeme pojem gaussovských stavů, je užitečné probrat souvislost mezi lineárními hradly (linear gates)
a symplektickou grupou (symplectic group), protože ta poskytuje užitečný nástroj k analýze gaussovských stavů pomocí
jejich statistických momentů (statistical moments).

Jak jsme už probrali v oddílu 1.2, působení lineárních optických hradel na posunovací (žebříkové) operátory (ladder
operators) může pomoci popsat časový vývoj fotonických kvantových stavů. Konkrétněji: lineární optická hradla jsou
zvláštní hradla, která na posunovací operátory působí lineárně. Tuto lineární transformaci lze popsat pomocí reálné
symplektické grupy [39]:

**Definice 2.2.1 (Symplektická grupa).** *Reálná symplektická grupa* (real symplectic group) je definována jako

$$
\operatorname{Sp}(2d, \mathbb{R}) := \left\{ S \in \mathbb{R}^{2d \times 2d} \mid S J S^T = J \right\},
\tag{2.5}
$$

kde $J$ je regulární antisymetrická matice, obvykle volená jako

$$
J = \begin{bmatrix} & \mathbb{1} \\ -\mathbb{1} & \end{bmatrix}.
\tag{2.6}
$$

Symplektická grupa popisuje pouze lineární optická hradla, jejichž hamiltoniány (Hamiltonians) jsou v posunovacích
operátorech ryze kvadratické. Pro obecná lineární optická hradla s hamiltoniány, které obsahují lineární
i kvadratické členy, musíme zavést reálnou afinní symplektickou grupu.

**Definice 2.2.2 (Afinní symplektická grupa).** *Reálná afinní symplektická grupa* (real affine symplectic group) je
definována přímým součinem²

$$
\operatorname{ASp}(2d, \mathbb{R}) := \mathbb{R}^{2d} \times \operatorname{Sp}(2d, \mathbb{R}),
\tag{2.7}
$$

kde grupové násobení v $\operatorname{ASp}(2d, \mathbb{R})$ je definováno vztahem

$$
(\pmb{\zeta}_1, S_1) \cdot (\pmb{\zeta}_2, S_2) := (\pmb{\zeta}_1 + S_1 \pmb{\zeta}_2,\, S_1 S_2)
\tag{2.8}
$$

pro $S_i \in \operatorname{Sp}(2d, \mathbb{R})$ a $\pmb{\zeta}_i \in \mathbb{R}^{2d}$.

*Poznámka.* Reálná symplektická grupa se nejčastěji používá v jiné, výhodnější bázi, kterou budeme někdy nazývat
*komplexní báze* (complex basis). Definujeme proto *komplexní tvar* (complex form) reálné symplektické grupy [40, 33]

$$
\begin{aligned}
\operatorname{Sp}^{(c)}(2d, \mathbb{R}) &:= W \operatorname{Sp}(2d, \mathbb{R}) W^\dagger \\
&= \left\{ S \in \mathbb{C}^{2d \times 2d} : S K S^\dagger = K,\ W^\dagger S W \in \mathbb{R}^{2d \times 2d} \right\},
\end{aligned}
\tag{2.9}
$$

kde $W$ je definováno v rovnici (1.18) a

$$
K = i W J W^\dagger = \begin{bmatrix} \mathbb{1} & \\ & -\mathbb{1} \end{bmatrix}.
\tag{2.10}
$$

Podobně komplexní tvar afinní symplektické grupy je prostě

$$
\operatorname{ASp}^{(c)}(2d, \mathbb{R}) := \operatorname{Sp}^{(c)}(2d, \mathbb{R}) \times W \mathbb{R}^{2d},
\tag{2.11}
$$

kde grupové násobení je definováno analogicky jako v definici 2.2.2.

Následující tvrzení dává do souvislosti kanonické komutační relace (CCR) a reálnou symplektickou grupu: transformace,
které zachovávají CCR, tvoří právě symplektickou grupu z definice 2.2.1.

**Tvrzení 1 (Transformace zachovávající CCR).** Uvažujme lineární transformaci posunovacích operátorů tvaru

$$
\pmb{\omega} := S \pmb{\xi},
\tag{2.12}
$$

kde $S \in \mathbb{C}^{2d \times 2d}$ splňuje $W^\dagger S W \in \mathbb{R}^{2d \times 2d}$, a označme

$$
\pmb{\omega} = [\hat b_1, \dots, \hat b_d, \hat b_1^\dagger, \dots, \hat b_d^\dagger]^T.
$$

Pokud i transformované operátory splňují kanonické komutační relace, tj. platí-li

$$
[\hat b_i, \hat b_j^\dagger] = \delta_{ij}, \qquad [\hat b_i, \hat b_j] = [\hat b_i^\dagger, \hat b_j^\dagger] = 0,
\tag{2.13}
$$

pak $S$ musí být symplektická matice (symplectic matrix) v komplexní bázi, tj.

$$
S \in \operatorname{Sp}^{(c)}(2d, \mathbb{R}).
\tag{2.14}
$$

*Důkaz.* Můžeme psát $[\xi_i, \xi_j^\dagger] = [\omega_i, \omega_j^\dagger] = K_{ij}$, kde $K$ je definováno v rovnici
(2.10). Díky tomu platí

$$
[\omega_i, \omega_j^\dagger] = \sum_{k,l=1}^{2d} S_{ik} \overline{S_{jl}}\, [\xi_k, \xi_l^\dagger]
= \sum_{k,l=1}^{2d} S_{ik} \overline{S_{jl}}\, K_{kl} \stackrel{!}{=} K_{ij},
\tag{2.15}
$$

z čehož plyne $S K S^\dagger = K$, a tedy $S \in \operatorname{Sp}^{(c)}(2d, \mathbb{R})$. ∎

Klíčové pozorování je, že vývoj posunovacích operátorů pod lineárními optickými kvantovými hradly lze snadno popsat
a že součin lineárních optických kvantových hradel je opět lineární optické kvantové hradlo, pokud ho lze zapsat jako
exponenciálu jediného hamiltoniánu. Dále chceme ukázat, že lineární optická kvantová hradla lze charakterizovat
afinní symplektickou grupou. Z praktických důvodů popíšeme zvlášť hradla s ryze lineárními a s ryze kvadratickými
hamiltoniány. Lineární hradla s ryze lineárními hamiltoniány lze popsat takto:

**Tvrzení 2 (Časový vývoj posunovacích operátorů pod lineárními hamiltoniány).** Uvažujme lineární optické hradlo
popsané unitárním operátorem

$$
U = e^{i \hat H},
\tag{2.16}
$$

kde hamiltonián $\hat H = \breve{\pmb{\alpha}} \cdot \pmb{\xi}$ je ryze lineární (ve značení definice 1.2.2). Vývoj
posunovacích operátorů lze zapsat jako

$$
U^\dagger \pmb{\xi} U = \pmb{\xi} + i J \breve{\pmb{\alpha}} \mathbb{1},
\tag{2.17}
$$

kde poslední člen chápeme jako

$$
i J \breve{\pmb{\alpha}} \mathbb{1}
:= [(i J \breve{\pmb{\alpha}})_1 \mathbb{1}, \dots, (i J \breve{\pmb{\alpha}})_{2d} \mathbb{1}]^T.
$$

*Důkaz.* Použijeme Hadamardovo lemma (Hadamard lemma) z rovnice (1.26) s volbou $X = -i \hat H$ a $Y = \hat a_k$.
Komutátor lze vyjádřit jako

$$
\begin{aligned}
{}[\hat H, \hat a_k] &= [\breve{\pmb{\alpha}} \cdot \pmb{\xi}, \hat a_k]
= \sum_{j=1}^{d} \overline{\beta_j}\, [\hat a_j^\dagger, \hat a_k] = -\overline{\beta_k}\, \mathbb{1}, \\
[\hat H, \hat a_k^\dagger] &= -[\hat H, \hat a_k]^\dagger = \beta_k \mathbb{1}.
\end{aligned}
\tag{2.18}
$$

Protože je komutátor úměrný $\mathbb{1}$, komutátory vyšších řádů můžeme vynechat a psát jednoduše

$$
\begin{aligned}
U^\dagger \hat a_k U &= \hat a_k - \overline{\beta_k}\, \mathbb{1}, \\
U^\dagger \hat a_k^\dagger U &= \hat a_k^\dagger + \beta_k \mathbb{1},
\end{aligned}
\tag{2.19}
$$

neboli stručněji

$$
U^\dagger \pmb{\xi} U = \pmb{\xi} + i J \breve{\pmb{\alpha}} \mathbb{1}.
\tag{2.20}
$$

∎

*(Pozn. překl.: V důkazu značí $\beta_j$ složky vektoru $\alpha \in \mathbb{C}^d$ z definice 1.2.2. Z lemmatu plyne
$U^\dagger \hat a_k U = \hat a_k - i[\hat H, \hat a_k] = \hat a_k + i\overline{\beta_k}\, \mathbb{1}$
a $U^\dagger \hat a_k^\dagger U = \hat a_k^\dagger - i\beta_k \mathbb{1}$, ve vztahu (2.19) tedy u členů s $\beta_k$
chybí faktor $-i$. Teprve s ním (2.19) odpovídá rovnicím (2.17) a (2.20).)*

U lineárních hradel s ryze kvadratickými hamiltoniány lze adjungované působení (adjoint action) popsat komplexním
tvarem symplektické grupy [33]:

**Tvrzení 3 (Časový vývoj posunovacích operátorů pod kvadratickými hamiltoniány).** Uvažujme lineární optické hradlo
s unitárním operátorem $U = e^{i \hat H}$, kde $\hat H = \pmb{\xi}^\dagger H \pmb{\xi}$ je ryze kvadratický
hamiltonián (quadratic Hamiltonian) ve značení definice 1.2.2. Vývoj posunovacích operátorů lze zapsat jako

$$
U^\dagger \pmb{\xi} U = S^{(c)} \pmb{\xi},
\tag{2.21}
$$

kde $S^{(c)} \in \operatorname{Sp}^{(c)}(2d, \mathbb{R})$ je dáno vztahem

$$
S^{(c)} = e^{i 2 K H}.
\tag{2.22}
$$

*Důkaz.* Použijeme Hadamardovo lemma z rovnice (1.26) a napíšeme

$$
U^\dagger \pmb{\xi} U = e^{-i \hat H} \pmb{\xi} e^{i \hat H} = e^{\operatorname{ad}_{(-i \hat H)}} \pmb{\xi}.
\tag{2.23}
$$

Abychom určili $e^{\operatorname{ad}_{(-i \hat H)}}$, musíme vyčíslit působení $\operatorname{ad}_{(-i \hat H)}$
na posunovací operátory:

$$
\operatorname{ad}_{(-i \hat H)} \pmb{\xi} = -i [\hat H, \pmb{\xi}] = -i [\pmb{\xi}^\dagger H \pmb{\xi}, \pmb{\xi}].
\tag{2.24}
$$

Podle definice 1.2.2 má $H$ tvar

$$
H = \begin{bmatrix} A & B \\ \overline{B} & \overline{A} \end{bmatrix},
\tag{2.25}
$$

kde $A^\dagger = A$ a $B^T = B$. Zaměříme-li se na jednu složku, lze $[\pmb{\xi}^\dagger H \pmb{\xi}, \hat a_k]$
a $[\pmb{\xi}^\dagger H \pmb{\xi}, \hat a_k^\dagger]$ vyjádřit jako

$$
\begin{aligned}
{}[\hat H, \hat a_k] &= \sum_{i,j=1}^{d} A_{ij} [\hat a_i^\dagger \hat a_j, \hat a_k] +
\overline{A_{ij}} [\hat a_i \hat a_j^\dagger, \hat a_k] +
B_{ij} [\hat a_i^\dagger \hat a_j^\dagger, \hat a_k] \\
&= -\sum_{i,j=1}^{d} A_{ij} \delta_{ik} \hat a_j + \overline{A_{ij}} \hat a_i \delta_{jk} +
B_{ij} (\delta_{ik} \hat a_j^\dagger + \hat a_i^\dagger \delta_{jk}) \\
&= -\left[ \sum_{j=1}^{d} A_{kj} \hat a_j + B_{kj} \hat a_j^\dagger +
\sum_{j=1}^{d} \underbrace{\overline{A_{jk}}}_{=A_{kj}} \hat a_j +
\underbrace{B_{jk}}_{=B_{kj}} \hat a_j^\dagger \right] \\
&= -2 \sum_{j=1}^{d} A_{kj} \hat a_j + B_{kj} \hat a_j^\dagger, \\
[\hat H, \hat a_k^\dagger] &= -[\hat H, \hat a_k]^\dagger
= 2 \sum_{j=1}^{d} \overline{A_{kj}} \hat a_j^\dagger + \overline{B_{kj}} \hat a_j.
\end{aligned}
\tag{2.26}
$$

Složíme-li všechny složky dohromady, lze komutátory zapsat jako

$$
[\pmb{\xi}^\dagger H \pmb{\xi}, \pmb{\xi}] = -2 K H \pmb{\xi}.
\tag{2.27}
$$

Transformaci odpovídající unitárnímu vývoji posunovacích operátorů lze tedy zapsat jako

$$
U^\dagger \pmb{\xi} U = e^{i 2 K H} \pmb{\xi}.
\tag{2.28}
$$

Pomocí tvrzení 1 lze také ukázat, že $S^{(c)} \in \operatorname{Sp}^{(c)}(2d, \mathbb{R})$, neboť

$$
[U^\dagger \pmb{\xi} U, U^\dagger \pmb{\xi}^\dagger U] = [\pmb{\xi}, \pmb{\xi}^\dagger],
\tag{2.29}
$$

a že $W^\dagger S^{(c)} W \in \mathbb{R}^{2d \times 2d}$, neboť $U^\dagger \hat x_i U$ i $U^\dagger \hat p_i U$ jsou pro
$i \in [d]$ samosdružené (self-adjoint). ∎

Definujeme-li tedy působení afinní symplektické grupy $\operatorname{ASp}^{(c)}(2d, \mathbb{R})$ na posunovací
operátory $\pmb{\xi}$ jako

$$
(\pmb{\gamma}, S^{(c)}) \cdot \pmb{\xi} := S^{(c)} \pmb{\xi} + \pmb{\gamma} \mathbb{1},
\tag{2.30}
$$

můžeme uzavřít, že vývoj posunovacích operátorů lineárním optickým obvodem je plně popsán grupou
$\operatorname{ASp}^{(c)}(2d, \mathbb{R})$.

² Pro úplnost: takový součin grup se nazývá polopřímý součin (semidirect product).
""",
)

SECTION_2_3 = PrimerSection(
    anchor="skripta-2-3",
    number="2.3",
    title="Gaussovské stavy",
    body=r"""
Jak jsme už avizovali, gaussovské stavy tvoří podmnožinu fotonických kvantových stavů s mnoha mimořádně příjemnými
vlastnostmi. Hlavním důvodem je, že gaussovské stavy lze zapsat pomocí jediného lineárního optického hamiltoniánu
(linear optical Hamiltonian), a to takto:

**Definice 2.3.1 (Gaussovský stav).** Uvažujme lineární optické hamiltoniány $\hat H$ (nazývané *rodičovský
hamiltonián*, parent Hamiltonian), jejichž hamiltonovská matice (Hamiltonian matrix) $H$ ve smyslu definice 1.2.1 je
pozitivně definitní (positive definite). Množinu takových operátorů označme $\mathcal{A}$. Množina smíšených
gaussovských stavů je definována jako

$$
\mathcal{S}_{G,\text{mixed}} := \left\{ \frac{e^{-\beta \hat H}}{\operatorname{Tr} e^{-\beta \hat H}} :
\hat H \in \mathcal{A}, \beta > 0 \right\},
\tag{2.31}
$$

kdežto množina čistých gaussovských stavů je definována jako

$$
\mathcal{S}_{G,\text{pure}} := \left\{
\lim_{\beta \to \infty} \frac{e^{-\beta \hat H}}{\operatorname{Tr} e^{-\beta \hat H}} : \hat H \in \mathcal{A}
\right\}.
\tag{2.32}
$$

Množina gaussovských stavů je tedy prostě

$$
\mathcal{S}_G := \mathcal{S}_{G,\text{mixed}} \cup \mathcal{S}_{G,\text{pure}}.
$$

Gaussovské stavy, jejichž rodičovský hamiltonián nemá lineární člen, nazýváme *centrované* gaussovské stavy
(centralized Gaussian states). V tomto workshopu se pro stručnost soustředíme na čisté centrované gaussovské stavy.

Nejdůležitějším gaussovským stavem je vakuum:

**Příklad (Vakuový stav).** Nechť
$\hat H = \hat a^\dagger \hat a = \hat n = \sum_{n=0}^{\infty} n\, |n\rangle\langle n|$, což je lineární optický
hamiltonián s pozitivně definitní hamiltonovskou maticí. Pak můžeme psát

$$
e^{-\beta \hat H} = \sum_{n=0}^{\infty} e^{-\beta n}\, |n\rangle\langle n|,
\tag{2.33}
$$

$$
\operatorname{Tr} e^{-\beta \hat H} = \sum_{n=0}^{\infty} e^{-\beta n} = \frac{1}{1 - e^{-\beta}}.
\tag{2.34}
$$

Potom

$$
\rho(\beta) = \frac{e^{-\beta \hat H}}{\operatorname{Tr} e^{-\beta \hat H}}
= \sum_{n=0}^{\infty} (1 - e^{-\beta}) e^{-\beta n}\, |n\rangle\langle n|,
\tag{2.35}
$$

a tedy pro $\beta \to \infty$ dostaneme

$$
\lim_{\beta \to \infty} \rho(\beta) = |0\rangle\langle 0|,
\tag{2.36}
$$

takže vakuum je čistý gaussovský stav.

Poznamenejme, že rovnice (2.35) definuje tepelný stav se středním počtem fotonů $\overline{n} = (1 + e^{\beta})^{-1}$
a že pro konečné $\beta > 0$ jde o smíšené gaussovské stavy. *(Pozn. překl.: Pro rozdělení
$p_n = (1 - e^{-\beta}) e^{-\beta n}$ z (2.35) vychází $\overline{n} = \sum_n n\, p_n = (e^{\beta} - 1)^{-1}$, ve shodě
s (2.4); v originálu je ve vzorci chybné znaménko.)*

Gaussovské stavy a lineární optická hradla spolu úzce souvisejí: působením lineárních optických hradel na gaussovské
stavy vznikají opět gaussovské stavy. Snadno se o tom přesvědčíme pomocí faktu, že unitární operátory lineárních
optických hradel zobrazují lineární optické hamiltoniány opět na lineární optické hamiltoniány. Konkrétně pro
smíšený gaussovský stav $\rho$ lze časový vývoj zapsat jako

$$
U \rho U^\dagger = \frac{U e^{-\beta \hat H} U^\dagger}{\operatorname{Tr}\left[ U e^{-\beta \hat H} U^\dagger \right]}
= \frac{e^{-\beta U \hat H U^\dagger}}{\operatorname{Tr} e^{-\beta U \hat H U^\dagger}},
\tag{2.37}
$$

a pokud $U$ odpovídá lineárnímu optickému hradlu, je $U \hat H U^\dagger$ také lineární optický hamiltonián
s pozitivně definitní hamiltonovskou maticí. Následuje typický příklad jednomódových čistých gaussovských stavů:

**Příklad (Stlačený stav).** Jednomódový stlačený stav definovaný vztahem

$$
|z\rangle := S(z)\, |0\rangle
\tag{2.38}
$$

je gaussovský stav, protože vakuum je gaussovské a lineární hradla zobrazují gaussovské stavy na gaussovské stavy.
""",
)

SECTION_2_4 = PrimerSection(
    anchor="skripta-2-4",
    number="2.4",
    title="Rozklad gaussovských stavů na normální módy",
    body=r"""
Abychom mohli zkoumat strukturu gaussovských stavů, musíme se nejprve seznámit s pojmem rozkladu na normální módy
(normal mode decomposition)³:

**Tvrzení 4 (Rozklad na normální módy).** Pro každou pozitivně definitní reálnou matici $H$ typu $2d \times 2d$
existuje diagonální matice $D$ a symplektická matice $S \in \operatorname{Sp}(2d, \mathbb{R})$ takové, že

$$
H = S D S^T,
\tag{2.39}
$$

kde

$$
D = \operatorname{diag}(\pmb{\nu}, \pmb{\nu}),
\tag{2.40}
$$

a $\nu_i > 0$ jsou vlastní čísla matice $|iJH|$; $\operatorname{diag}$ označuje sestavení diagonální matice se
zadanými vektory na diagonále.

*Důkaz.* Důkaz tohoto faktu pro stručnost vynecháme. Zvídavý čtenář ho najde v oddílu 3.2.3 práce [38]. ∎

To lze využít k rozkladu libovolného kvadratického hamiltoniánu $\hat H$ z rovnice (1.21) s pozitivně definitní
hamiltonovskou maticí:

$$
\hat H = \pmb{\chi}^T H^{(\mathrm{xp})} \pmb{\chi} = (S \pmb{\chi})^T D S \pmb{\chi}
\tag{2.41}
$$

pro nějakou reálnou symplektickou matici $S \in \operatorname{Sp}(2d, \mathbb{R})$, kde $D$ má tvar (2.40). Vezměme
nyní lineární hradlo s unitárním operátorem $U$ takovým, že

$$
U^\dagger \pmb{\chi} U = S \pmb{\chi},
\tag{2.42}
$$

a tedy

$$
U \hat H U^\dagger = \pmb{\chi}^T D \pmb{\chi} = \sum_{i=1}^{d} \nu_i (\hat x_i^2 + \hat p_i^2)
= \sum_{i=1}^{d} 2 \nu_i \left(\hat n_i + \frac{1}{2} \mathbb{1}\right).
\tag{2.43}
$$

Každý kvadratický hamiltonián s pozitivně definitní hamiltonovskou maticí je tedy unitárně ekvivalentní hamiltoniánu
volných, neinteragujících harmonických oscilátorů s frekvencemi úměrnými $\nu_i$.

³ Známý také jako Williamsonův rozklad (Williamson decomposition).
""",
)

SECTION_2_5 = PrimerSection(
    anchor="skripta-2-5",
    number="2.5",
    title="Statistické momenty gaussovských stavů",
    body=r"""
Přímým důsledkem rozkladu kvadratických hamiltoniánů na normální módy je, že (čisté) gaussovské stavy lze vytvořit
jedině tak, že vakuum necháme vyvíjet výhradně pod lineárními optickými hamiltoniány. Gaussovské stavy jsou proto
plně popsány svým vektorem posunutí (displacement vector) $\mu$ a kovarianční maticí (covariance matrix) $\sigma$,
definovanými po prvcích jako

$$
\begin{aligned}
\mu_i &:= \operatorname{Tr}\left[ \rho\, \pmb{\chi}_i \right], \\
\sigma_{ij} &:= \operatorname{Tr}\left[ \rho \left\{ \pmb{\chi}_i - \mu_i \mathbb{1}, \pmb{\chi}_j - \mu_j \mathbb{1}
\right\} \right],
\end{aligned}
\tag{2.44}
$$

kde $\{A, B\} := AB + BA$ je antikomutátor a $\pmb{\chi}$ je vektor kvadraturních operátorů (quadrature operators)
z rovnice (1.18) v oddílu 1.1. Někdy je však praktičtější používat obdobné veličiny v bázi posunovacích operátorů:

$$
\mu_i^{(\mathrm{c})} := \operatorname{Tr}\left[ \rho\, \pmb{\xi}_i \right],
\tag{2.45}
$$

$$
\sigma_{ij}^{(\mathrm{c})} := \operatorname{Tr}\left[ \rho \left\{
(\pmb{\xi}_i - \mu_i^{(\mathrm{c})} \mathbb{1})^\dagger, \pmb{\xi}_j - \mu_j^{(\mathrm{c})} \mathbb{1} \right\} \right].
\tag{2.46}
$$

Mezi oběma definicemi lze přecházet pomocí vztahů

$$
\pmb{\mu}^{(\mathrm{c})} := W \pmb{\mu},
\tag{2.47}
$$

$$
\sigma^{(\mathrm{c})} := W \sigma W^\dagger,
\tag{2.48}
$$

kde $W$ je definováno v rovnici (1.18).

Pro lepší představu uvažujme následující příklad:

**Příklad (Kovarianční matice vakua).** Víme, že je-li $\rho = |0\rangle\langle 0|$, pak

$$
\mu_0^{(\mathrm{c})} = \operatorname{Tr}\left[ |0\rangle\langle 0|\, a \right]
= \langle 0| \underbrace{a\, |0\rangle}_{=0} = 0,
\tag{2.49}
$$

$$
\mu_1^{(\mathrm{c})} = \operatorname{Tr}\left[ |0\rangle\langle 0|\, \hat a^\dagger \right]
= \langle 0| \underbrace{\hat a^\dagger |0\rangle}_{=|1\rangle} = \langle 0|1\rangle = 0.
\tag{2.50}
$$

Prvky kovarianční matice pak lze zapsat jako

$$
\sigma_{ij}^{(\mathrm{c})} = \operatorname{Tr}\left[ \rho \{ \pmb{\xi}_i^\dagger, \pmb{\xi}_j \} \right]
= \langle 0| \{ \pmb{\xi}_i^\dagger, \pmb{\xi}_j \} |0\rangle.
\tag{2.51}
$$

Analogicky k předchozí úvaze víme, že
$\langle 0| \hat a^\dagger \hat a^\dagger |0\rangle = \langle 0| a a |0\rangle = 0$ a že
$\{\hat a^\dagger, a\} = 2 \hat a^\dagger a + \mathbb{1}$, takže statistické momenty vakua jsou jednoduše

$$
\pmb{\mu}^{(\mathrm{c})} = [0,\, 0]^T,
\tag{2.52}
$$

$$
\sigma^{(\mathrm{c})} = \mathbb{1}_{2 \times 2},
\tag{2.53}
$$

což mimochodem má stejný tvar i v kvadraturní bázi.

Vývoj pod lineárním hradlem s ryze kvadratickým hamiltoniánem je plně popsán následující transformací vektoru
posunutí a kovarianční matice:

$$
\begin{aligned}
\pmb{\mu} &\mapsto S \pmb{\mu}, \\
\sigma &\mapsto S \sigma S^T,
\end{aligned}
\tag{2.54}
$$

kde $S \in \operatorname{Sp}(2d, \mathbb{R})$ je reálná symplektická matice příslušná danému lineárnímu hradlu, jak
jsme probrali v oddílu 2.2.
""",
)

SECTION_2_6 = PrimerSection(
    anchor="skripta-2-6",
    number="2.6",
    title="Blochův–Messiahův rozklad",
    body=r"""
Podobně jako u Clementsova rozkladu (Clements decomposition) z oddílu 1.3.2 se přirozeně nabízí otázka, jak rozložit
obecné lineární optické prvky. Odpověď se v podstatě redukuje na jistý rozklad reálných symplektických matic, který
je nepostradatelným nástrojem pro studium lineárního optického kvantového počítání.

Ukazuje se, že k realizaci libovolné lineární operace ve fotonickém kvantovém počítání stačí jen hradla posunutí,
stlačovací hradla, fázové posouvače (phaseshifters) a děliče svazku (beamsplitters). Nástroj, kterým rozklad na
elementární lineární optická hradla získáme, se nazývá *Blochův–Messiahův rozklad* (Bloch–Messiah
decomposition)⁴:

**Věta 2.6.1 (Blochův–Messiahův rozklad).** Uvažujme symplektickou matici
$S^{(c)} \in \operatorname{Sp}^{(c)}(2d, \mathbb{R})$. Matici $S^{(c)}$ lze rozložit jako

$$
\begin{aligned}
S^{(c)} &= V_1 D V_2, \\
V_1 &= \begin{bmatrix} U_1 & \\ & \overline{U_1} \end{bmatrix}, \qquad
V_2 = \begin{bmatrix} U_2 & \\ & \overline{U_2} \end{bmatrix},
\end{aligned}
\tag{2.55}
$$

kde $U_1, U_2 \in \operatorname{U}(d)$ a $D$ je

$$
D = \begin{bmatrix} \cosh \mathbf{r} & -\sinh \mathbf{r} \\ -\sinh \mathbf{r} & \cosh \mathbf{r} \end{bmatrix},
\tag{2.56}
$$

a $\mathbf{r} \in \mathbb{R}^d_{\geq 0}$. Funkce cosh a sinh se přitom chápou po prvcích, např.
$\cosh \mathbf{r} = \bigoplus_{i=1}^{d} \cosh r_i$.

*Důkaz.* Důkaz tohoto lineárně algebraického faktu pro stručnost vynecháme, lze ho však najít v práci [41]. ∎

Pomocí tohoto rozkladu lze každý unitární operátor příslušný kvadratickému hamiltoniánu rozložit na dvě pasivní
lineární transformace (které lze dále rozložit Clementsovým rozkladem z oddílu 1.3.2) a řadu jednomódových
stlačovacích hradel (s využitím rovnice (1.35)). Lineární optická hradla mají v hamiltoniánu i lineární členy, z nichž
vzniká vrstva (column) jednomódových hradel posunutí. Tyto úvahy nyní shrneme do věty:

**Věta 2.6.2.** Unitární operátor $U$ libovolného lineárního optického hradla lze rozložit jako

$$
\begin{aligned}
U &= \left( \prod_{i=1}^{d} D_i(\alpha_i) \right) I(U_1) \left( \prod_{i=1}^{d} S_i(r_i) \right) I(U_2), \\
&\qquad \alpha_i \in \mathbb{C},\ r_i \in \mathbb{R},
\end{aligned}
\tag{2.57}
$$

kde $I(U_1)$ a $I(U_2)$ jsou interferometry (interferometers) parametrizované unitárními maticemi $U_1$ a $U_2$
a $D_i(\alpha_i)$ a $S_i(r_i)$ jsou hradlo posunutí a stlačovací hradlo působící na $i$-tý mód.

*Důkaz.* Jak jsme probrali v oddílu 2.2, každé lineární optické hradlo určuje prvek afinní symplektické grupy
$\operatorname{ASp}^{(c)}(2d, \mathbb{R})$. Podle rovnice (2.8) lze libovolný prvek
$(\pmb{\gamma}, S^{(c)}) \in \operatorname{ASp}^{(c)}(2d, \mathbb{R})$ rozložit jednoduše jako

$$
(\pmb{\gamma}, S^{(c)}) = (\pmb{\gamma}, \mathbb{1}) \cdot (\mathbf{0}, S^{(c)}),
\tag{2.58}
$$

kde činitelé odpovídají po řadě lineárním a kvadratickým členům hamiltoniánu. Aplikujeme-li dále Blochův–Messiahův
rozklad z věty 2.6.1 na symplektickou matici $S^{(c)}$, dostaneme

$$
S^{(c)} = V_1 D V_2,
\tag{2.59}
$$

kde $V_1, V_2$ jsou unitární symplektické matice odpovídající interferometrům $I(U_1)$ a $I(U_2)$ a $D$ odpovídá
vrstvě stlačovacích hradel

$$
S(\mathbf{r}) := \prod_{i=1}^{d} S(r_i).
\tag{2.60}
$$

Lineární část $\pmb{\gamma}$ je nakonec na bosonovém Fockově prostoru (Fock space) reprezentována vrstvou
jednomódových hradel posunutí. ∎

⁴ V literatuře se nazývá také *Eulerův* rozklad (Euler decomposition).
""",
)

SECTION_2_7 = PrimerSection(
    anchor="skripta-2-7",
    number="2.7",
    title="Cvičení",
    body=r"""
**Cvičení 2.7.1.** Spočtěte pravděpodobnost, že v koherentním stavu detekujeme 0 fotonů, tj. spočtěte

$$
|\langle 0|\alpha\rangle|^2 = \, ?
\tag{2.61}
$$

Použijte vzorec

$$
D(\alpha) = e^{\alpha \hat a^\dagger - \overline{\alpha} a}
= e^{\alpha \hat a^\dagger} e^{-\overline{\alpha} a} e^{\frac{1}{2} [\alpha \hat a^\dagger, \overline{\alpha} a]}.
\tag{2.62}
$$

*Řešení.* Spočteme $[\alpha \hat a^\dagger, \overline{\alpha} a] = -|\alpha|^2$ a napíšeme

$$
\begin{aligned}
\langle 0|\alpha\rangle &= \langle 0| D(\alpha) |0\rangle
= e^{-\frac{|\alpha|^2}{2}} \langle 0| e^{\alpha \hat a^\dagger} e^{-\overline{\alpha} a} |0\rangle \\
&\stackrel{a|0\rangle = 0}{=} e^{-\frac{|\alpha|^2}{2}} \underbrace{\langle 0|0\rangle}_{=1}
= e^{-\frac{|\alpha|^2}{2}}.
\end{aligned}
\tag{2.63}
$$

Odtud $|\langle 0|\alpha\rangle|^2 = e^{-|\alpha|^2}$. Můžeme to ověřit i v Piquassu:

```python
import piquasso as pq
import numpy as np


alpha = 0.1

with pq.Program() as program:
    pq.Q() | pq.Vacuum()

    pq.Q() | pq.Displacement(alpha)

simulator = pq.PureFockSimulator(d=1)

state = simulator.execute(program).state

print("Expected: ", np.exp(-np.abs(alpha)**2))
print("Actual: ", state.get_particle_detection_probability((0,)))
```

**Cvičení 2.7.2.** Pomocí simulátoru `PureFockSimulator` z Piquassa připravte koherentní stavy instrukcí
`Displacement`. Proč je norma simulovaného stavu menší než 1? Ověřte, že se norma s rostoucím parametrem `cutoff`
v `Config` zvětšuje.

*Řešení.* Kód v Piquassu:

```python
import piquasso as pq
import numpy as np


with pq.Program() as program:
    pq.Q() | pq.Vacuum()

    pq.Q() | pq.Displacement(r=0.1)

simulator = pq.PureFockSimulator(d=1, config=pq.Config(cutoff=4)) # <- Zvyšte cutoff!

state = simulator.execute(program).state

print("Norm: ", state.norm)
```

**Cvičení 2.7.3.** Jaký je střední počet částic v koherentním stavu, tj. čemu se rovná

$$
\langle \hat n \rangle_{D(\alpha)|0\rangle} = \langle 0| D^\dagger(\alpha) \hat n D(\alpha) |0\rangle \, ?
\tag{2.64}
$$

Výsledky porovnejte s výsledky z `PureFockSimulator` a `GaussianSimulator`.

*Řešení.* Kód v Piquassu:

```python
import piquasso as pq
import numpy as np


with pq.Program() as program:
    pq.Q() | pq.Vacuum()

    pq.Q() | pq.Displacement(r=0.1)

simulator = pq.PureFockSimulator(d=1) # Změňte PureFockSimulator -> GaussianSimulator!

state = simulator.execute(program).state

print("Mean photon number: ", state.mean_photon_number())
```

**Cvičení 2.7.4.** Spočtěte kovarianční matici jednomódového koherentního stavu. K porovnání výsledků použijte
`GaussianSimulator`.

*Řešení.* Spočtěme $\sigma^{(\mathrm{c})}$. Nejdříve ale musíme začít s $\pmb{\mu}^{(\mathrm{c})}$, který snadno
spočteme z rovnice (1.38):

$$
\pmb{\mu}^{(\mathrm{c})} = \breve{\alpha},
\tag{2.65}
$$

kde $\breve{\alpha} := [\alpha, \overline{\alpha}]^T$. Využili jsme přitom, že $|\alpha\rangle = D(\alpha)|0\rangle$,
a cykličnost stopy, díky níž jsme výraz přepsali do Heisenbergova obrazu (Heisenberg picture). Pro kovarianční
matici můžeme také zapsat vývoj antikomutátoru:

$$
\begin{aligned}
&D^\dagger(\alpha) \{ \xi_i^\dagger - \overline{\breve{\alpha}_i} \mathbb{1}, \xi_j - \breve{\alpha}_j \mathbb{1} \}
D(\alpha) \\
&\quad = \{ D^\dagger(\alpha) \xi_i^\dagger D(\alpha) - \overline{\breve{\alpha}_i} \mathbb{1},
D^\dagger(\alpha) \xi_j D(\alpha) - \breve{\alpha}_j \mathbb{1} \} \\
&\quad = \{ \xi_i^\dagger + \overline{\breve{\alpha}_i} \mathbb{1} - \overline{\breve{\alpha}_i} \mathbb{1},
\xi_j + \breve{\alpha}_j \mathbb{1} - \breve{\alpha}_j \mathbb{1} \} \\
&\quad = \{ \xi_i^\dagger, \xi_j \},
\end{aligned}
\tag{2.66}
$$

což dává kovarianční matici vakua, tedy $\mathbb{1}_{2 \times 2}$. Proto
$\sigma^{(\mathrm{c})} = \mathbb{1}_{2 \times 2}$. Můžeme to ověřit v Piquassu:

```python
import piquasso as pq
import numpy as np


with pq.Program() as program:
    pq.Q() | pq.Vacuum()

    pq.Q() | pq.Displacement(r=0.1)

simulator = pq.GaussianSimulator(d=1)

state = simulator.execute(program).state

print("Covariance matrix: ", state.complex_covariance_matrix)
```

*(Pozn. překl.: V Piquassu 8.0.2 se tento atribut jmenuje `complex_covariance`; s `complex_covariance_matrix` skončí
kód chybou `AttributeError`.)*

**Cvičení 2.7.5.** Jaký je střední počet částic ve stlačeném stavu, tj. čemu se rovná

$$
\langle \hat n \rangle_{S(z)|0\rangle} = \langle 0| S^\dagger(z) \hat n S(z) |0\rangle \, ?
\tag{2.67}
$$

Výsledky porovnejte s výsledky z `PureFockSimulator` a `GaussianSimulator`.

*Řešení.* Víme, že

$$
S^\dagger(z) \hat n S(z) = S^\dagger(z) \hat a^\dagger \hat a S(z)
= S^\dagger(z) \hat a^\dagger S(z) S^\dagger(z) \hat a S(z),
\tag{2.68}
$$

a můžeme psát

$$
\begin{aligned}
S^\dagger(z) \hat a^\dagger S(z) &= \cosh(r) \hat a^\dagger - e^{-i\phi} \sinh(r) \hat a, \\
S^\dagger(z) \hat a S(z) &= \cosh(r) \hat a - e^{i\phi} \sinh(r) \hat a^\dagger,
\end{aligned}
\tag{2.69}
$$

kde $z = r e^{i\phi}$. Můžeme tedy psát

$$
\begin{aligned}
S^\dagger(z) \hat n S(z) &= \cosh^2(r) \hat a^\dagger \hat a -
\cosh(r) \sinh(r) \left( e^{i\phi} (\hat a^\dagger)^2 + e^{-i\phi} \hat a \hat a \right) \\
&\quad + \sinh^2(r) \hat a \hat a^\dagger.
\end{aligned}
\tag{2.70}
$$

Odtud

$$
\langle z| \hat n |z\rangle = \langle 0| S^\dagger(z) \hat n S(z) |0\rangle = \sinh^2(r).
\tag{2.71}
$$

**Cvičení 2.7.6.** Ukažte, že kovarianční matice jednomódového stlačeného stavu má tvar

$$
\sigma = \begin{bmatrix} e^{-2r} & 0 \\ 0 & e^{2r} \end{bmatrix},
\tag{2.72}
$$

neboli v bázi posunovacích operátorů

$$
\sigma^{(c)} = \begin{bmatrix} \cosh(2r) & -e^{i\phi} \sinh(2r) \\ -e^{-i\phi} \sinh(2r) & \cosh(2r) \end{bmatrix}.
\tag{2.73}
$$

K porovnání výsledků použijte `GaussianSimulator`.

*Řešení.* Protože kovarianční matice vakua je $\mathbb{1}_{2 \times 2}$, můžeme podle rovnice (2.54) psát
$\sigma = S S^T$, kde $S$ je (reálná) symplektická matice stlačovacího hradla z rovnice (1.36).

*(Pozn. překl.: Tvar (2.72) platí pro reálné $z = r$, tj. $\phi = 0$; pro obecné $\phi$ je $\sigma$ pootočená a má
nenulové mimodiagonální prvky. Mimodiagonální prvky v (2.73) odpovídají převodu (2.48),
$\sigma^{(c)} = W \sigma W^\dagger$, a stejnou konvenci používá i Piquasso. Přímo z definice (2.46) by vyšla matice
komplexně sdružená, tj. vpravo nahoře $-e^{-i\phi} \sinh(2r)$.)*
""",
)

CHAPTER = PrimerChapter(
    label="Kapitola 2",
    title="Gaussovské stavy",
    intro=INTRO,
    sections=(SECTION_2_1, SECTION_2_2, SECTION_2_3, SECTION_2_4, SECTION_2_5, SECTION_2_6, SECTION_2_7),
    original_pages="17–26",
)
