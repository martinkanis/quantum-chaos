"""Czech translation of the introduction and chapter 1 of the primer (ui/primer_content.py)."""

from __future__ import annotations

from ui.primer_content import PrimerChapter, PrimerSection

INTRODUCTION = PrimerSection(anchor="skripta-uvod", number="", title="Úvod", body=r"""
Kvantové počítače slibují, že zvládnou některé úlohy, které leží mimo možnosti klasických počítačů [1, 2],
a nabízejí množství potenciálních aplikací – od fyziky mnoha částic [3, 4] přes úlohy kvantové chemie [5, 6, 7]
až po strojové učení [8, 9]. Tento příslib v poslední době podnítil výrazný pokrok ve vývoji prototypů kvantových
počítačů, jímž vstupujeme do druhé kvantové revoluce. Pokrok v kvantovém počítání nakonec pohání velké množství
koncových uživatelů v průmyslu. Není proto divu, že významného pokroku dosáhl soukromý sektor, a to jak velké
zavedené firmy (např. Google [10], IBM [11], Microsoft [12], AWS [13]), tak menší startupy (např. Rigetti [14],
Xanadu [15], PsiQuantum [16], Pasqal [17], Quix [18], Quantinuum [19], QuEra [20]).

Vývoj kvantového počítače však přináší i vlastní specifické výzvy. Největší překážkou je potlačení dekoherence,
tj. zachování kvantové koherence systému, který interaguje se svým okolím [21]. Konečným cílem je sestrojit
kvantové počítače odolné vůči chybám (fault-tolerant). Dnešní technologie však škálovatelný kvantový počítač odolný
vůči chybám zatím nepřinesla a současná zařízení jsou stále zatížená šumem a ještě ne plně škálovatelná [22]. Přesto
lze tyto zašuměné kvantové počítače středního rozsahu (noisy intermediate-scale quantum, NISQ) chápat jako významný
krok k chybově odolnému kvantovému počítání i jako počítače s potenciálně užitečnými aplikacemi. Velikost obvodů,
kterou dnešní hardware dovoluje, už stačí na netriviální výpočty, jak dokládají experimenty prokazující kvantovou
výhodu, které nelze simulovat na běžných počítačích [23, 20].

Mezi mnoha návrhy kvantových výpočtů získaly na významu fotonické kvantové počítače díky nedávným demonstracím
schémat, která mohou vést k fotonické kvantové výhodě [24, 25, 15], a díky vývoji proveditelných metod kvantového
počítání odolného vůči chybám [16, 26, 27]. Fotonické kvantové počítače jsou kvantové počítače, které jako nosiče
kvantové informace používají fotony. Mezi různými paradigmaty kvantového počítání vyniká fotonické kvantové počítání
svými jedinečnými přednostmi [28]: (i) kvantové jevy (např. superpozici či provázání, angl. entanglement) lze
u fotonů pozorovat i za pokojové teploty, zatímco qubity realizované v hmotných systémech vyžadují nízké teploty;
(ii) lze využít poměrně vyspělé technologie – například hradla dělič svazku a fázový posouvač jsou už dnes
klíčovou součástí mnoha optických experimentů; (iii) fotony lze provázat i na větší vzdálenosti, což umožňuje
komunikaci v síti fotonických kvantových počítačů.

Teorie grafů už dlouho poskytuje jednotící matematický rámec pro tak rozmanité obory, jako jsou informatika, fyzika
a chemie. Zvláště fotonické kvantové počítání má k teorii grafů hluboký vztah: mnoho výpočetních úloh lze
přeformulovat v jazyce teorie grafů a fotonický hardware přirozeně realizuje lineárně optické sítě, které odpovídají
maticím sousednosti grafů. Klíčovým příkladem této souhry je *Boson Sampling*, který zavedli Aaronson a Arkhipov [29]
a který lze chápat jako vzorkování z rozdělení pravděpodobnosti určeného permanentem podmatice unitární matice
popisující optický interferometr. Permanent přitom počítá perfektní párování bipartitních grafů. Obdobně tento obraz
rozšiřuje *Gaussian Boson Sampling* (GBS) [30], který spojuje statistiku detekce fotonů s hafniánem a smyčkovým
hafniánem (loop hafnian), tedy funkcemi, které počítají perfektní párování grafů. Tyto souvislosti nejen přirozeně
propojují fotonické kvantové počítání s teorií grafů, ale také otevírají cestu k využití fotonických zařízení při
řešení grafových úloh, jako je hledání hustých podgrafů [31] nebo maximálních klik [32].

Skripta jsou uspořádána takto. V kapitole 1 shrnujeme teoretické základy fotonického kvantového počítání. Kapitola 2
uvádí do problematiky (bosonových) gaussovských stavů, tedy kvantových stavů, které hrají klíčovou roli v Gaussian
Boson Sampling. Abychom osvětlili souvislost gaussovských stavů s teorií grafů, zavádíme v kapitole 3 formalismus
fázového prostoru kvantové optiky. Nakonec v kapitole 4 probíráme Gaussian Boson Sampling a jeho aplikace v úlohách
teorie grafů.
""")

SECTION_1_1 = PrimerSection(
    anchor="skripta-1-1", number="1.1", title="Fockův prostor a kanonické komutační relace", body=r"""
Základním objektem fotonických kvantových systémů, kterými se zabýváme, je fotonický *kvantový mód* (qumode),
zkráceně jen *mód*. Zhruba řečeno, v jednom kvantovém módu může být určitý počet částic (fotonů) $n \ge 0$, který
reprezentujeme vektorem $|n\rangle$; ten odpovídá kvantovému stavu kvantového módu s $n$ fotony. Těmto vektorům
říkáme *Fockovy stavy* (Fock states), číslu $n$ *obsazovací číslo* (occupation number) a vektorovému prostoru,
který generují, (bosonový) *Fockův prostor* (Fock space). Fockovy stavy tvoří ortogonální bázi Fockova prostoru, tj.

$$
\langle n|m\rangle = \delta_{nm},
\tag{1.1}
$$

kde $\delta_{nm}$ je Kroneckerovo delta, které je rovno 1 pro $n = m$ a 0 jinak. Fockův stav $|0\rangle$ se nazývá
*vakuový stav* (vacuum state), krátce vakuum. *Kreační a anihilační operátory* (creation and annihilation
operators), souhrnně nazývané *posunovací (žebříkové) operátory* (ladder operators), definujeme jejich působením
na Fockovy stavy:

$$
\begin{aligned}
\hat a^\dagger |n\rangle &= \sqrt{n+1}\, |n+1\rangle, \\
\hat a |n\rangle &= \sqrt{n}\, |n-1\rangle \qquad (n \ge 1), \\
\hat a |0\rangle &= 0.
\end{aligned}
\tag{1.2}
$$

Fockův stav $|n\rangle$ lze z vakua sestrojit pomocí kreačního operátoru jako

$$
|n\rangle = \frac{(\hat a^\dagger)^n}{\sqrt{n!}} |0\rangle .
\tag{1.3}
$$

Libovolný jednomódový čistý stav $|\psi\rangle$ lze rozložit do Fockových stavů jako

$$
|\psi\rangle = \sum_{n=0}^{\infty} c_n |n\rangle, \quad c_n \in \mathbb{C},
\tag{1.4}
$$

kde z normalizace $\lVert \psi \rVert = 1$ plyne

$$
\sum_{n=0}^{\infty} |c_n|^2 = 1.
\tag{1.5}
$$

Kreační a anihilační operátor splňují následující relaci, kterou lze snadno ověřit pomocí vztahu (1.2):

$$
[\hat a, \hat a^\dagger] = \mathbb{1},
\tag{1.6}
$$

kde $\mathbb{1}$ je jednotkový (identický) operátor a $[A, B] := AB - BA$ je *komutátor*. Z posunovacích operátorů
lze sestrojit *operátor počtu částic* (number operator) $\hat n := \hat a^\dagger \hat a$, který splňuje rovnici

$$
\hat n |n\rangle = \hat a^\dagger \hat a |n\rangle = n |n\rangle .
\tag{1.7}
$$

Ve fyzikálním kontextu interpretujeme vakuový stav jako kvantový stav bez fotonů. To snadno nahlédneme ze vztahu

$$
\hat n |0\rangle = \sum_{i=1}^{d} \hat a_i^\dagger \hat a_i |0\rangle = 0,
\tag{1.8}
$$

neboť podle definice platí $\hat a_i |0\rangle = 0$.

*(Pozn. překl.: Vztah (1.8) už předbíhá k systému s $d$ módy, který zavádí následující odstavec; $\hat n$ je v něm
celkový operátor počtu částic, viz (1.24). Pro jeden mód stačí $\hat a^\dagger \hat a |0\rangle = 0$.)*

Zobecněme nyní předchozí úvahy a uvažujme systém s $d$ módy. V tom případě máme $d$ fotonických kvantových módů
a obecný Fockův stav zapisujeme jako

$$
|n_1, \dots, n_d\rangle .
\tag{1.9}
$$

Ten odpovídá kvantovému stavu, v němž je $n_1$ fotonů v prvním kvantovém módu, $n_2$ fotonů ve druhém kvantovém
módu a tak dále. Kreační a anihilační operátory se upraví takto:

$$
\begin{aligned}
\hat a_j^\dagger |n_1, \dots, n_j, \dots, n_d\rangle &= \sqrt{n_j + 1}\, |n_1, \dots, n_j + 1, \dots, n_d\rangle, \\
\hat a_j |n_1, \dots, n_j, \dots, n_d\rangle &= \sqrt{n_j}\, |n_1, \dots, n_j - 1, \dots, n_d\rangle .
\end{aligned}
\tag{1.10}
$$

Pro kreační a anihilační operátory platí relace

$$
\begin{aligned}
{}[\hat a_i, \hat a_j^\dagger] &= \delta_{ij} \mathbb{1}, \\
[\hat a_i, \hat a_j] = [\hat a_i^\dagger, \hat a_j^\dagger] &= 0,
\end{aligned}
\tag{1.11}
$$

pro všechna $i, j \in [d]$. Tyto relace se nazývají *kanonické komutační relace* (canonical commutation relations,
CCR) a (asociativní) algebra generovaná posunovacími operátory se nazývá *algebra CCR*. Prvky této algebry, pro které
platí $t^\dagger = t$, se nazývají samosdružené (self-adjoint).

Podobně jako dříve nazýváme vektorový prostor generovaný (vícemódovými) Fockovými stavy Fockovým prostorem. Fockovy
bázové stavy lze také získat působením kreačních operátorů na vakuový stav, tj.

$$
|l_1, \dots, l_d\rangle = \prod_{i=1}^{d} \frac{(\hat a_i^\dagger)^{l_i}}{\sqrt{l_i!}} |0\rangle .
\tag{1.12}
$$

Tyto stavy jsou užitečné, protože tvoří spočetnou bázi Fockova prostoru. Obecně lze libovolný vektor $|\psi\rangle$,
který odpovídá (čistému) stavu ve Fockově prostoru, rozložit jako

$$
|\psi\rangle = \sum_{n_1=0}^{\infty} \cdots \sum_{n_d=0}^{\infty} c_{n_1, \dots, n_d} |n_1, \dots, n_d\rangle,
\tag{1.13}
$$

kde $c_{n_1, \dots, n_d} \in \mathbb{C}$ a

$$
\sum_{n_1=0}^{\infty} \cdots \sum_{n_d=0}^{\infty} |c_{n_1, \dots, n_d}|^2 = 1.
\tag{1.14}
$$

Místo posunovacích operátorů lze ekvivalentně používat tzv. *kvadraturní operátory* (quadrature operators), což jsou
pozorovatelné odpovídající poloze a hybnosti ve fázovém prostoru.

**Definice 1.1.1 (Kvadraturní operátory).** Operátor polohy $\hat x_i$ a operátor hybnosti $\hat p_i$ jsou
definovány jako

$$
\begin{aligned}
\hat x_i &= \frac{\hat a_i + \hat a_i^\dagger}{\sqrt{2}}, \\
\hat p_i &= \frac{\hat a_i - \hat a_i^\dagger}{i\sqrt{2}},
\end{aligned}
\tag{1.15}
$$

kde $i \in [d]$. Tyto operátory se souhrnně nazývají *kvadraturní operátory*.

Všimněme si, že kvadraturní operátory jsou samosdružené a že CCR lze vyjádřit i pomocí kvadraturních operátorů:

$$
[\hat x_i, \hat p_j] = \delta_{ij} \mathbb{1}, \quad [\hat x_i, \hat x_j] = [\hat p_i, \hat p_j] = 0,
\tag{1.16}
$$

pro všechna $i, j \in [d]$.

*(Pozn. překl.: Z definice (1.15) a relací (1.11) vychází $[\hat x_i, \hat p_j] = i\, \delta_{ij} \mathbb{1}$,
kde $i$ je imaginární jednotka; v první relaci (1.16) originálu tento faktor chybí.)*

Přechod mezi posunovacími a kvadraturními operátory lze maticově zapsat jako

$$
\pmb{\xi} = W \pmb{\chi},
\tag{1.17}
$$

kde jsme operátory seskupili do vektorů

$$
\begin{aligned}
\pmb{\xi} &= [\hat a_1, \dots, \hat a_d, \hat a_1^\dagger, \dots, \hat a_d^\dagger]^T, \\
\pmb{\chi} &= [\hat x_1, \dots, \hat x_d, \hat p_1, \dots, \hat p_d]^T, \\
W &= \frac{1}{\sqrt{2}} \begin{bmatrix} \mathbb{1} & i\mathbb{1} \\ \mathbb{1} & -i\mathbb{1} \end{bmatrix}.
\end{aligned}
\tag{1.18}
$$
""")

SECTION_1_2 = PrimerSection(
    anchor="skripta-1-2", number="1.2", title="Elementární fotonická kvantová hradla", body=r"""
Ve fotonickém kvantovém počítání lze kvantový obvod popsat unitárním operátorem na Fockově prostoru. Elementární
stavební bloky fotonických kvantových obvodů se nazývají elementární *fotonická kvantová hradla* (photonic quantum
gates); lze z nich sestavit širokou škálu unitárních operátorů na bosonovém Fockově prostoru. Elementární fotonická
kvantová hradla lze charakterizovat jejich fotonickými hamiltoniány, což jsou samosdružené operátory; samotná
fotonická hradla se pak zapíší jako exponenciála těchto hamiltoniánů, viz vztah (A.8).

V této části uvedeme užitečné roztřídění fotonických kvantových hradel. Jedním důležitým hlediskem je stupeň
hamiltoniánu jakožto polynomu v posunovacích operátorech, který určuje jejich dynamiku. Později zejména uvidíme, že
fotonická hradla s hamiltoniány stupně 2 mají obzvlášť pěkný popis. Dalším užitečným rozlišovacím znakem fotonických
kvantových hradel je zachování počtu částic: fotonická kvantová hradla zachovávající počet částic mají tu vlastnost,
že jejich unitární operátory na bosonovém Fockově prostoru lze rozložit na přímé součty podle počtu částic.

V kontextu lineární optiky odpovídají fotonická hradla hamiltoniánům, které jsou v posunovacích operátorech nejvýše
kvadratické. Zavedeme proto následující terminologii.

**Definice 1.2.1 (Kvadratický hamiltonián).** *Kvadratický hamiltonián* (quadratic Hamiltonian) $\hat H$ na $d$
módech je samosdružený operátor tvaru

$$
\hat H = \pmb{\xi}^\dagger H \pmb{\xi} = \sum_{i,j=1}^{2d} H_{ij} \xi_i^\dagger \xi_j,
\tag{1.19}
$$

kde $\pmb{\xi}$ je definováno vztahem (1.18), $\pmb{\xi}^\dagger$ chápeme jako sdružení po složkách,

$$
H = \begin{bmatrix} A & B \\ \overline{B} & \overline{A} \end{bmatrix},
\tag{1.20}
$$

a $A, B \in \mathbb{C}^{d \times d}$ splňují $A^\dagger = A$ a $B^T = B$. Matici $H$ budeme nazývat *hamiltonovská
matice* (Hamiltonian matrix).

V kvadraturní bázi lze kvadratické hamiltoniány zapsat také jako

$$
\hat H = \pmb{\chi}^T H^{(\mathrm{xp})} \pmb{\chi},
\tag{1.21}
$$

kde $H^{(\mathrm{xp})} \in \mathbb{R}^{2d \times 2d}$ je hamiltonovská matice v kvadraturní bázi, která má tvar

$$
H^{(\mathrm{xp})} = W^\dagger H W
= \begin{bmatrix}
\operatorname{Re}(A + B) & -\operatorname{Im}(A - B) \\
\operatorname{Im}(A + B) & \operatorname{Re}(A - B)
\end{bmatrix}.
\tag{1.22}
$$

**Definice 1.2.2 (Lineárně optický hamiltonián).** *Lineárně optický hamiltonián* (linear optical Hamiltonian) lze
zapsat jako

$$
\hat H = \pmb{\xi}^\dagger H \pmb{\xi} + \check{\pmb{\alpha}} \cdot \pmb{\xi},
\tag{1.23}
$$

kde $\pmb{\xi}^\dagger H \pmb{\xi}$ je kvadratický hamiltonián podle definice 1.2.1,
$\check{\pmb{\alpha}} := [\pmb{\alpha}, \overline{\pmb{\alpha}}]$ a $\pmb{\alpha} \in \mathbb{C}^d$.

Ústředním pojmem lineární optiky jsou *lineárně optická hradla* (linear optical gates), tedy fotonická kvantová
hradla s lineárně optickými hamiltoniány. Lineárními se nazývají proto, že na posunovací operátory působí (afinně)
lineárně. Fotonická kvantová hradla, která lineární nejsou, se nazývají *nelineární*; na tomto workshopu je však
používat nebudeme. Další důležité roztřídění fotonických kvantových hradel vychází z toho, jak mění počet částic
v systému. Hradla, která počet částic nemění, se nazývají *pasivní hradla* (passive gates), a hradla, která ho mění,
*aktivní hradla* (active gates) [33]. Konkrétněji uvažujme *celkový operátor počtu částic* (global particle number
operator)

$$
\hat n := \sum_{j=1}^{d} \hat n_j = \sum_{j=1}^{d} \hat a_j^\dagger \hat a_j .
\tag{1.24}
$$

Pasivní hradla jsou definována tím, že zachovávají celkový operátor počtu částic:

**Definice 1.2.3 (Pasivní hradlo).** *Pasivní hradlo* je fotonické kvantové hradlo, jehož unitární operátor $U$
komutuje s celkovým operátorem počtu částic, tj.

$$
[U, \hat n] = 0.
\tag{1.25}
$$

### 1.2.1 Běžná fotonická kvantová hradla

V této části uvádíme nejdůležitější příklady fotonických hradel pro tento text. Ukážeme nejen jejich unitární
operátor na Fockově prostoru, ale také vývoj kreačních a anihilačních operátorů pod působením těchto hradel.
To je důležité, protože – jak uvidíme – v teorii lineární optiky pomáhá unitární vývoj kreačních
a anihilačních operátorů charakterizovat vývoj fotonických kvantových stavů. K jeho výpočtu je potřeba Hadamardovo
lemma¹ [34]. Pro fotonický hamiltonián $\hat H$ a operátor $X$ lze Hadamardovo lemma zapsat jako

$$
\begin{aligned}
e^{i\hat H} X e^{-i\hat H} &= e^{\mathrm{ad}_{i\hat H}} X \\
&= X + [i\hat H, X] + \frac{1}{2!} [i\hat H, [i\hat H, X]] \\
&\quad + \frac{1}{3!} [i\hat H, [i\hat H, [i\hat H, X]]] + \cdots .
\end{aligned}
\tag{1.26}
$$

*¹ Hadamardovo lemma se nazývá také Campbellova identita.*

*Hradlo fázového posuvu* (phaseshift gate), neboli rotační hradlo, modeluje skutečný optický prvek, fázový
posouvač (phase shifter), který otáčí fázi postupující elektromagnetické vlny. Jako kvantové hradlo působí hradlo
fázového posuvu na stav tak, že jej otáčí v kanonickém fázovém prostoru.

**Definice 1.2.4 (Hradlo fázového posuvu).** *Hradlo fázového posuvu* je definováno na jednom módu a jeho operátor je

$$
R_j(\phi) = \exp\left( i\phi \hat n_j \right),
\tag{1.27}
$$

kde $\phi \in [0, 2\pi)$ a $\hat n_j := \hat a_j^\dagger \hat a_j$.

Důležité je, že hradlo fázového posuvu je jediné jednomódové pasivní lineárně optické hradlo, a proto se považuje
za elementární stavební blok fotonických kvantových obvodů. V Heisenbergově obrazu transformuje posunovací operátory
takto:

$$
\begin{aligned}
R_j(\phi)^\dagger \hat a_j R_j(\phi) &= \hat a_j e^{i\phi}, \\
R_j(\phi)^\dagger \hat a_j^\dagger R_j(\phi) &= \hat a_j^\dagger e^{-i\phi},
\end{aligned}
\tag{1.28}
$$

což lze odvodit pomocí vztahu (1.26). Předchozí vyjádření lze stručněji zapsat jako

$$
R_j^\dagger(\phi) \begin{bmatrix} \hat a_j \\ \hat a_j^\dagger \end{bmatrix} R_j(\phi)
= \begin{bmatrix} e^{i\phi} & 0 \\ 0 & e^{-i\phi} \end{bmatrix}
\begin{bmatrix} \hat a_j \\ \hat a_j^\dagger \end{bmatrix}.
\tag{1.29}
$$

Hradla fázového posuvu spolu s *hradly děliče svazku* (beamsplitter gates) generují všechny pasivní lineárně optické
transformace, jak vyjde najevo později v oddílu 1.3.2. Dělič svazku je optické zařízení, které rozděluje světlo
na dvě části, a je nezbytnou součástí mnoha optických experimentů. Děliče svazku navíc hrají zásadní roli
i v kvantové teleportaci, v kvantovém počítání a v základním výzkumu fotonů.

**Definice 1.2.5 (Hradlo děliče svazku).** Uvažujme bosonový systém s $d$ módy. Unitární operátor *hradla děliče
svazku* mezi módy s indexy $j, k \in [d] := \{1, \dots, d\}$ má v posunovacích operátorech tvar

$$
B_{jk}(\theta, \phi)
= \exp\left( \theta \left( e^{i\phi} \hat a_j \hat a_k^\dagger - e^{-i\phi} \hat a_j^\dagger \hat a_k \right) \right),
\tag{1.30}
$$

kde $\theta, \phi \in [0, 2\pi)$ jsou úhlové parametry děliče svazku. Pro $\theta = \pi/4$ a $\phi = 0$ se nazývá
dělič svazku 50/50.

Posunovací operátory se tímto hradlem transformují takto:

$$
B_{jk}^\dagger(\theta, \phi)
\begin{bmatrix} \hat a_j \\ \hat a_k \\ \hat a_j^\dagger \\ \hat a_k^\dagger \end{bmatrix}
B_{jk}(\theta, \phi)
= \begin{bmatrix} t & -\overline{r} & & \\ r & t & & \\ & & t & -r \\ & & \overline{r} & t \end{bmatrix}
\begin{bmatrix} \hat a_j \\ \hat a_k \\ \hat a_j^\dagger \\ \hat a_k^\dagger \end{bmatrix},
\tag{1.31}
$$

kde $t = \cos(\theta)$ a $r = e^{i\phi} \sin(\theta)$.

*Poznámka.* Označme dvě vstupní pole $\hat a_0, \hat a_1$ a dvě výstupní pole $\hat b_0, \hat b_1$. Vstupní a výstupní
pole spolu lineárně souvisejí vztahem

$$
\begin{bmatrix} \hat b_0 \\ \hat b_1 \end{bmatrix}
= \begin{bmatrix} t' & r \\ r' & t \end{bmatrix}
\begin{bmatrix} \hat a_0 \\ \hat a_1 \end{bmatrix}.
\tag{1.32}
$$

Z kanonických komutačních relací (1.11) plyne

$$
|t'| = |t|, \quad |r'| = |r|, \quad |t|^2 + |r|^2 = 1,
\tag{1.33}
$$

kde se $t$ nazývá (amplitudová) propustnost (transmittance) a $r$ (amplitudová) odrazivost (reflectance).

*Stlačovací hradlo* (squeezing gate) je typickým příkladem aktivního lineárně optického hradla.

**Definice 1.2.6 (Stlačovací hradlo).** Unitární operátor *stlačovacího hradla* je

$$
S_j(z) = \exp\left( \frac{1}{2} \left( \overline{z} \hat a_j^2 - z \hat a_j^{\dagger 2} \right) \right),
\tag{1.34}
$$

kde $z \in \mathbb{C}$.

Název stlačovacího hradla vychází z jeho operační interpretace ve fázovém prostoru. Vyjdeme-li z vakuového stavu,
stlačovací hradlo vytvoří stav, který je ve fázovém prostoru v určitém směru „stlačený“². Tento kvantový stav se
nazývá stlačené vakuum (squeezed vacuum state), případně prostě stlačený stav (squeezed state). Stlačovací hradlo
navíc transformuje posunovací operátory takto:

$$
S_j^\dagger(z) \begin{bmatrix} \hat a_j \\ \hat a_j^\dagger \end{bmatrix} S_j(z)
= \begin{bmatrix} \cosh r & -e^{i\phi} \sinh r \\ -e^{-i\phi} \sinh r & \cosh r \end{bmatrix}
\begin{bmatrix} \hat a_j \\ \hat a_j^\dagger \end{bmatrix},
\tag{1.35}
$$

kde $z = r e^{i\phi}$. V kvadraturních operátorech má tento vztah pro $\phi \equiv 0$ tvar

$$
S_j^\dagger(z) \begin{bmatrix} \hat x_j \\ \hat p_j \end{bmatrix} S_j(z)
= \begin{bmatrix} e^{-r} & 0 \\ 0 & e^{r} \end{bmatrix}
\begin{bmatrix} \hat x_j \\ \hat p_j \end{bmatrix}.
\tag{1.36}
$$

Dalším rozborem tohoto vztahu lze odvodit, že po působení stlačovacího hradla na fotonický kvantový stav se rozptyl
veličiny $\hat x_j$ zmenší, což ospravedlňuje název „stlačení“ (squeezing).

*² Přesněji řečeno, „stlačená“ je Wignerova funkce tohoto stavu.*

Dalším významným aktivním lineárním hradlem je *hradlo posunutí* (displacement gate), které má podobně jako
stlačovací hradlo názorný operační význam ve fázovém prostoru. Jak název napovídá, hradlo posunutí odpovídá
„posunutí“ kvantového stavu ve fázovém prostoru.

**Definice 1.2.7 (Hradlo posunutí).** Unitární operátor *hradla posunutí* je

$$
D_j(\alpha) = \exp\left( \alpha \hat a_j^\dagger - \overline{\alpha} \hat a_j \right),
\tag{1.37}
$$

kde $\alpha \in \mathbb{C}$.

Hradlo posunutí transformuje posunovací operátory takto:

$$
D_j^\dagger(\alpha) \begin{bmatrix} \hat a_j \\ \hat a_j^\dagger \end{bmatrix} D_j(\alpha)
= \begin{bmatrix} \hat a_j + \alpha \mathbb{1} \\ \hat a_j^\dagger + \overline{\alpha} \mathbb{1} \end{bmatrix}.
\tag{1.38}
$$

Pro lepší intuici je však užitečné podívat se, jak se transformují kvadraturní operátory $\hat x_j$ a $\hat p_j$
z definice 1.1.1:

$$
D_j^\dagger(\alpha) \begin{bmatrix} \hat x_j \\ \hat p_j \end{bmatrix} D_j(\alpha)
= \begin{bmatrix} \hat x_j + \sqrt{2} \operatorname{Re}(\alpha) \mathbb{1} \\
\hat p_j + \sqrt{2} \operatorname{Im}(\alpha) \mathbb{1} \end{bmatrix}.
\tag{1.39}
$$

To znamená, že parametr $\alpha \in \mathbb{C}$ popisuje posunutí kvadraturních operátorů ve dvourozměrném fázovém
prostoru: reálná část odpovídá posunutí v poloze a imaginární část posunutí v hybnosti. Obecněji, máme-li obvod
s $d$ módy, sloupec hradel posunutí parametrizovaný vektorem $\pmb{\alpha} \in \mathbb{C}^d$ popisuje obecné posunutí
všech kvadraturních operátorů ve fázovém prostoru, což je důležitý nástroj ke studiu kvantové optiky.
""")

SECTION_1_3 = PrimerSection(anchor="skripta-1-3", number="1.3", title="Interferometry a jejich rozklad", body=r"""
Popis hradel fázového posuvu a děliče svazku lze sjednotit, budeme-li uvažovat obecný optický *interferometr*.
Interferometr představuje libovolnou pasivní lineární operaci, jak vyjde najevo později v této kapitole.

**Definice 1.3.1 (Interferometr).** Unitární operátor interferometru lze zapsat jako

$$
I(U) = \exp\left( i\hat H \right),
\tag{1.40}
$$

kde $\hat H$ je kvadratický hamiltonián

$$
\hat H = \pmb{\xi}^\dagger H \pmb{\xi}, \qquad
H = \frac{1}{2} \begin{bmatrix} A & \\ & \overline{A} \end{bmatrix},
\tag{1.41}
$$

kde $A$ je samosdružená matice. Interferometr se často parametrizuje maticí $U = e^{iA}$, což zdůvodníme
v oddílu 1.3.1.

### 1.3.1 Pasivní lineární hradla a permanent

Uvažujme bosonový systém s $d$ módy a jednočásticovým Hilbertovým prostorem $\mathcal{H}$. Dále uvažujme obecné
pasivní lineárně optické hradlo s unitárním operátorem tvaru

$$
\hat U = \exp\left( i\hat H \right), \qquad \hat H = \pmb{\xi}^\dagger H \pmb{\xi}, \qquad
H = \frac{1}{2} \begin{bmatrix} A & \\ & \overline{A} \end{bmatrix},
\tag{1.42}
$$

jak je popsáno v definici 1.3.1. Později uvidíme, že transformaci posunovacích operátorů lze zapsat jako

$$
\begin{aligned}
\hat U^\dagger \hat a_i \hat U &= \sum_{j=1}^{d} U_{ij} \hat a_j, \\
\hat U^\dagger \hat a_i^\dagger \hat U &= \sum_{j=1}^{d} \overline{U_{ij}} \hat a_j^\dagger,
\end{aligned}
\tag{1.43}
$$

neboli stručněji

$$
\hat U^\dagger \pmb{\xi} \hat U = \begin{bmatrix} U & \\ & \overline{U} \end{bmatrix} \pmb{\xi},
\tag{1.44}
$$

kde $U = e^{iA}$. To znamená, že kreační (anihilační) operátory se zobrazí na lineární kombinace kreačních
(anihilačních) operátorů. Navíc každé pasivní lineárně optické hradlo $\hat U$ zachovává vakuový stav, tj.

$$
\hat U |0\rangle = |0\rangle .
\tag{1.45}
$$

Snadno lze spočítat, jak takový operátor působí na jednotlivé částice, neboť

$$
\hat U |e_i\rangle = \hat U \hat a_i^\dagger \hat U^\dagger \underbrace{\hat U |0\rangle}_{= |0\rangle}
= \sum_{j=1}^{d} U_{ji} \hat a_j^\dagger |0\rangle = U |e_i\rangle ,
\tag{1.46}
$$

kde $|e_i\rangle$ je jednočásticový bázový vektor

$$
|0 \dots \underbrace{1}_{i\text{-tá pozice}} \dots 0\rangle =: |e_i\rangle .
\tag{1.47}
$$

Obecněji uvažujme $n$-částicový Fockův bázový stav $|\mathbf{n}\rangle := |n_1, \dots, n_d\rangle$. Pasivní lineárně
optická hradla působí na každou částici nezávisle, což ukazuje následující výpočet:

$$
\begin{aligned}
\hat U |\mathbf{n}\rangle &= \hat U \prod_{i=1}^{d} \frac{(\hat a_i^\dagger)^{n_i}}{\sqrt{n_i!}} |0\rangle
= \prod_{i=1}^{d} \frac{(\hat U \hat a_i^\dagger \hat U^\dagger)^{n_i}}{\sqrt{n_i!}} |0\rangle \\
&= \prod_{i=1}^{d} \frac{\left( \sum_{j=1}^{d} U_{ji} \hat a_j^\dagger \right)^{n_i}}{\sqrt{n_i!}} |0\rangle .
\end{aligned}
\tag{1.48}
$$

Využili jsme zde, že pasivní lineární hradla nemění vakuový stav, tj. $\hat U |0\rangle = |0\rangle$. Nyní každý
činitel roznásobíme podle multinomické věty a zavedeme nezáporná celá čísla $m_{ji}$, která udávají, kolikrát je
ze vstupu $i$ zvolen mód $j$:

$$
\left( \sum_{j=1}^{d} U_{ji} \hat a_j^\dagger \right)^{n_i}
= \sum_{m_{1i} + \dots + m_{di} = n_i} \frac{n_i!}{\prod_j m_{ji}!} \prod_{j=1}^{d} \left( U_{ji} \hat a_j^\dagger
\right)^{m_{ji}} .
\tag{1.49}
$$

Vynásobením přes všechny vstupy $i$ dostaneme součet přes celé nezáporné matice $M = (m_{ji})_{j,i}$ s řádkovými
podmínkami $\sum_{i=1}^{d} m_{ji} =: m_j$ a sloupcovými podmínkami $\sum_{j=1}^{d} m_{ji} = n_i$.

Protože operátory $\hat a_j^\dagger$ navzájem komutují, můžeme psát

$$
\begin{aligned}
&\prod_{i=1}^{d} \sum_{m_{1i} + \dots + m_{di} = n_i} \frac{n_i!}{\prod_j m_{ji}!} \prod_{j=1}^{d}
\left( U_{ji} \hat a_j^\dagger \right)^{m_{ji}} \\
&\qquad = \sum_{\substack{m_{ij} \ge 0 \\ \sum_i m_{ji} = m_j \\ \sum_j m_{ji} = n_i}} \prod_{i,j=1}^{d}
\frac{n_i!}{\prod_j m_{ji}!} U_{ji}^{m_{ji}} (\hat a_j^\dagger)^{m_j}
\end{aligned}
\tag{1.50}
$$

a odtud, splňují-li $\{m_{ji}\}$ řádkové podmínky pro $|\mathbf{m}\rangle = |m_1, \dots, m_d\rangle$, dostáváme

$$
\langle \mathbf{m}| \hat U |\mathbf{n}\rangle
= \sum_{\substack{m_{ij} \ge 0 \\ \sum_i m_{ji} = m_j \\ \sum_j m_{ji} = n_i}} \prod_{i,j=1}^{d}
\frac{\sqrt{n_i! m_j!}}{\prod_j m_{ji}!} U_{ji}^{m_{ji}} .
\tag{1.51}
$$

Nyní potřebujeme následující definici.

**Definice 1.3.2.** *Permanent* matice $A \in \mathbb{C}^{n \times n}$ je definován jako

$$
\operatorname{per}(A) = \sum_{\sigma \in S_n} \prod_{i=1}^{n} A_{\sigma(i), i}, \qquad A \in \mathbb{C}^{n \times n},
\tag{1.52}
$$

kde $S_n$ označuje množinu permutací $n$ prvků.

Snadno nahlédneme, že

$$
\operatorname{per}(\mathrm{r}_{\mathbf{m}, \mathbf{n}} U)
= \sum_{\substack{m_{ij} \ge 0 \\ \sum_i m_{ji} = m_j \\ \sum_j m_{ji} = n_i}} \prod_{i,j=1}^{d}
\frac{n_i! m_j!}{\prod_j m_{ji}!} U_{ji}^{m_{ji}},
\tag{1.53}
$$

kde $\mathrm{r}_{\mathbf{m}, \mathbf{n}}$ je *redukce matice* (matrix reduction), tedy operace, která zopakuje řádky
vstupní matice podle $\mathbf{m}$ a její sloupce podle $\mathbf{n}$. Překryv je tedy

$$
\langle \mathbf{m}| \hat U |\mathbf{n}\rangle = \frac{\operatorname{per}(\mathrm{r}_{\mathbf{m}, \mathbf{n}} U)}
{\sqrt{\mathbf{n}! \, \mathbf{m}!}},
\tag{1.54}
$$

kde jsme označili $\mathbf{n}! = \prod_{i=1}^{d} n_i!$.

*(Pozn. překl.: Součin $\prod_{i,j=1}^{d}$ ve vztazích (1.50), (1.51) a (1.53) je třeba číst volně: faktory, které
závisejí jen na $i$ nebo jen na $j$ (tj. $n_i!$, $m_j!$ a $(\hat a_j^\dagger)^{m_j}$), se v něm berou každý jen
jednou a jmenovatel je součin $m_{ji}!$ přes všechny dvojice $i, j$. Například v (1.53) se tedy sčítají členy
$\prod_i n_i! \prod_j m_j! \prod_{i,j} U_{ji}^{m_{ji}} / m_{ji}!$.)*

### 1.3.2 Clementsův rozklad

Přirozeně se nabízí otázka, jak rozložit libovolnou pasivní lineární operaci (tj. libovolný interferometr)
na elementární stavební bloky, jako jsou děliče svazku a fázové posouvače, protože interferometry obecně nejsou
na fotonickém kvantovém počítači přímo realizovatelné. Řada aplikací fotonického kvantového počítání navíc vyžaduje
konkrétní parametrizaci fotonických kvantových obvodů, a k tomu je takový rozklad neocenitelný.

*Clementsův rozklad* (Clements decomposition) umožňuje rozložit libovolnou pasivní lineární transformaci na děliče
svazku a fázové posouvače [35]. Rozklad je znázorněn na obrázku 1.1. Myšlenka spočívá v opakovaném použití
Givensových rotací na jednočásticovou unitární matici interferometru, přičemž každá Givensova rotace odpovídá
jednomu děliči svazku. Tímto způsobem lze z unitární matice postupně, jeden po druhém, eliminovat všechny
(mimodiagonální) prvky, až zbude diagonální matice odpovídající fázovým posouvačům.

*Obrázek 1.1: Znázornění Clementsova rozkladu pro 6 módů. Dvoumódová hradla představují děliče svazku, jednomódová
hradla fázové posouvače. Obecně se interferometr na $d$ módech rozloží na $d(d-1)/2$ děličů svazku a $d - 1$
fázových posouvačů. Poslední fázový posouvač je vynechán díky invarianci vůči globální fázi.*

[Na obrázku: šest vodorovných čar (módů) vede zleva doprava. Mezi sousedními čarami jsou ve střídajících se
sloupcích, ve vzoru cihlové zdi, zapojeny dvoumódové bloky – děliče svazku s parametry $\theta_1, \phi_1$ až
$\theta_{15}, \phi_{15}$, prostřední bloky jsou jen naznačené třemi tečkami; celkem jde o $6 \cdot 5/2 = 15$ děličů.
První sloupec spojuje módy 2–3 a 4–5, druhý módy 1–2, 3–4 a 5–6 a tak dále. Na pravém konci má každý z prvních pěti
módů jeden jednomódový fázový posouvač $\varphi_1, \dots, \varphi_5$, šestý mód žádný.]
""")

SECTION_1_4 = PrimerSection(anchor="skripta-1-4", number="1.4", title="Měření počtu částic", body=r"""
*Měření počtu částic* (particle number measurement), neboli detekce fotonů, je měření, které se experimentálně
realizuje *detektory rozlišujícími počet fotonů* (photon number-resolving detectors, PNRD). Pravděpodobnost, že
v čistém kvantovém stavu $|\psi\rangle$ naměříme počty částic $\mathbf{n} = (n_1, n_2, \dots, n_d)$, je dána
vztahem

$$
p(\mathbf{n}) = |\langle \mathbf{n}|\psi\rangle|^2 .
\tag{1.55}
$$

Vzorky získané měřením jsou nezáporná celá čísla odpovídající detekovaným počtům fotonů, takže pravděpodobnosti lze
jen přibližně odhadnout z mnoha vzorků. Všimněme si, že vztah (1.55) je v souladu se vztahem (1.14), neboť

$$
|\langle \mathbf{n}|\psi\rangle|^2 = |c_{\mathbf{n}}|^2 = |c_{n_1, \dots, n_d}|^2 .
\tag{1.56}
$$
""")

SECTION_1_5 = PrimerSection(anchor="skripta-1-5", number="1.5", title="Boson Sampling", body=r"""
Jedním z významných schémat kvantové výhody, která lze realizovat na fotonickém kvantovém počítači, je známé
schéma Boson Sampling [29]. Boson Sampling je přístup ke kvantovému počítání, při kterém se generují vzorky měřením
počtu částic (viz oddíl 1.4) z fotonického kvantového stavu, který připraví interferometr z Fockova bázového stavu.
Ačkoli je toto uspořádání teoreticky použitelné pro libovolný bosonový systém, fotonická realizace je nejpřirozenější.
Obecně se uznává, že Boson Sampling provádí výpočetní úlohu efektivněji než klasické počítače: jejím řešením je
vzorkování z výstupního rozdělení pravděpodobnosti počtů částic pro náhodně zvolený interferometr, což se pokládá
za úlohu, kterou klasický výpočet nezvládne. Konkrétně byla obtížnost této úlohy doložena v režimu bez kolizí
(collision-free), kdy počet módů roste kvadraticky s počtem vstupních fotonů [29]. Přestože byl Boson Sampling
navržen především k demonstracím kvantové výhody, bez ohledu na praktické využití, byly pro toto schéma navrženy
i aplikace, například řešení úloh elektronové struktury [36] nebo určování vibronických spekter molekul [5].

Ve standardním uspořádání Boson Samplingu je vstupním stavem obvykle Fockův bázový stav
$|\mathbf{n}\rangle = |n_1, n_2, \dots, n_d\rangle$, kde $n = \sum_{i=1}^{d} n_i$ je celkový počet fotonů. Ačkoli
$|\mathbf{n}\rangle$ může být libovolný, hodnoty $n_i$ se obvykle volí 1 nebo 0. Fotony pak projdou obecným pasivním
lineárně optickým interferometrem, popsaným unitární maticí $U$ rozměru $d \times d$. Protože pasivní lineární obvod
zachovává celkový počet částic, má i výsledný stav celkem $n$ částic. Na konci obvodu se na každém módu provede
detekce fotonů a pravděpodobnost konkrétního výsledku měření $|\mathbf{m}\rangle = |m_1, m_2, \dots, m_d\rangle$ je

$$
p(\mathbf{m})
= \frac{|\operatorname{per}(\mathrm{r}_{\mathbf{m}, \mathbf{n}}(U))|^2}{n_1! \dots n_d! \, m_1! \dots m_d!} .
\tag{1.57}
$$

Zde $U$ je unitární matice pasivního lineárního obvodu a permanent $\operatorname{per}$ matice je definován vztahem
(1.52). A především: právě permanent je zdrojem všeobecně přijímané klasické nezvládnutelnosti úlohy Boson Sampling –
pro obecnou matici $A \in \mathbb{C}^{n \times n}$ je i přibližný výpočet $\operatorname{per}(A)$ #P-úplný
a nalezení polynomiálního algoritmu pro jeho výpočet by implikovalo P = NP [29].

*(Pozn. překl.: Přesněji: přesný výpočet permanentu je #P-úplný a jeho aproximace s multiplikativní chybou je pro
obecné komplexní matice #P-těžká [29].)*
""")

SECTION_1_6 = PrimerSection(anchor="skripta-1-6", number="1.6", title="Ztráty fotonů", body=r"""
*Ztráty fotonů* (photon losses) patří k hlavním výzvám fotonického kvantového počítání; vznikají absorpcí,
rozptylem nebo nedokonalou účinností detektorů. Takové ztráty snižují výpočetní sílu fotonických procesorů, takže
jejich potlačení je klíčovým požadavkem škálovatelných experimentů. Protože všechny současné realizace trpí
nezanedbatelnými ztrátami, je nezbytné vyvíjet přesné analytické i numerické modely ztrátových kanálů.

Ztráty fotonů se obvykle modelují jako interakce s nepřístupným módem prostředí (typicky ve vakuovém stavu)
prostřednictvím děliče svazku: má-li foton pravděpodobnost přežití $\eta$, je mód navázán na vakuový stav prostředí
s amplitudou propustnosti $|t| = \sqrt{\eta}$ a amplitudou odrazu $|r| = \sqrt{1 - \eta}$. S úhlem děliče svazku to
souvisí vztahem $\cos\theta = \sqrt{\eta}$ a pro jednoduchost volíme $\phi = \pi/2$. Kreační operátor se při této
operaci transformuje jako

$$
\hat a^\dagger \mapsto \sqrt{\eta}\, \hat a^\dagger + \sqrt{1 - \eta}\, \hat a_{\text{env}}^\dagger ,
\tag{1.58}
$$

a protože $\hat a^\dagger$ a $\hat a_{\text{env}}^\dagger$ komutují, můžeme psát

$$
\begin{aligned}
|n\rangle = \frac{(\hat a^\dagger)^n}{\sqrt{n!}}
&\mapsto \frac{\left( \sqrt{\eta}\, \hat a^\dagger + \sqrt{1 - \eta}\, \hat a_{\text{env}}^\dagger \right)^n}{\sqrt{n!}}
|0, 0_{\text{env}}\rangle \\
&= \frac{1}{\sqrt{n!}} \sum_{k=0}^{n} \binom{n}{k} (\sqrt{\eta})^k (\sqrt{1 - \eta})^{n-k} (\hat a^\dagger)^k
(\hat a_{\text{env}}^\dagger)^{n-k} |0, 0_{\text{env}}\rangle \\
&= \sum_{k=0}^{n} \sqrt{\binom{n}{k}} (\sqrt{\eta})^k (\sqrt{1 - \eta})^{n-k} |k, (n-k)_{\text{env}}\rangle ,
\end{aligned}
\tag{1.59}
$$

kde jsme pro přehlednost ve Fockových stavech vyznačili módy prostředí (index env).
""")

SECTION_1_7 = PrimerSection(anchor="skripta-1-7", number="1.7", title="Cvičení", body=r"""
**Cvičení 1.7.1.** Nainstalujte Piquasso ve verzi 6.2.0 příkazem

```bash
pip install piquasso
```

Ověřte, že instalace proběhla úspěšně: otevřete terminál Pythonu a balíček naimportujte.

*(Pozn. překl.: Příkaz bez čísla verze nainstaluje nejnovější Piquasso, ne verzi 6.2.0; tu vynutí
`pip install piquasso==6.2.0`. Například verze 8.0.2 potřebuje Python 3.10 nebo novější.)*

**Cvičení 1.7.2.** Pomocí Piquassa připravte Fockův stav $|11\rangle$ se simulátorem `SamplingSimulator`. Detekci
fotonů simulujte pomocí `ParticleNumberMeasurement` a získejte vzorky.

*Řešení.* Kód v Piquassu:

```python
import piquasso as pq

with pq.Program() as program:
    pq.Q() | pq.StateVector(occupation_numbers=(1, 1)) | pq.ParticleNumberMeasurement()

simulator = pq.SamplingSimulator(d=2)

result = simulator.execute(program, shots=20)

print(result.samples)
```

**Cvičení 1.7.3.** Na stav připravený v předchozím cvičení aplikujte dělič svazku 50/50 a poté detekci fotonů.
Odhadněte pravděpodobnosti jednotlivých výstupních konfigurací.

*Řešení.* Kód v Piquassu:

```python
import numpy as np
import piquasso as pq

shots = 100

with pq.Program() as program:
    pq.Q() | pq.StateVector(occupation_numbers=(1, 1))

    pq.Q() | pq.Beamsplitter(theta=np.pi/4, phi=0.0)

    pq.Q() | pq.ParticleNumberMeasurement()

simulator = pq.SamplingSimulator(d=2)

result = simulator.execute(program, shots=shots)

counts = result.get_counts()

print("Relative frequency of (2, 0):", counts[(2, 0)] / shots)
print("Relative frequency of (0, 2):", counts[(0, 2)] / shots)
```

Výsledek $(1, 1)$ se ve vzorcích neobjeví.

**Cvičení 1.7.4.** Pro situaci z předchozího cvičení odvoďte pravděpodobnosti výsledků 20, 11 a 02. Ověřte, že
odpovídají pravděpodobnostem získaným simulací v Piquassu.

*Řešení.* Můžeme psát

$$
|1, 1\rangle = \hat a_1^\dagger \hat a_2^\dagger |0\rangle ,
\tag{1.60}
$$

a po aplikaci hradla děliče svazku 50/50 $\hat U = B_{12}(\theta = \pi/4, \phi = 0)$ dostaneme

$$
\begin{aligned}
\hat U |1, 1\rangle &= \hat U \hat a_1^\dagger \hat a_2^\dagger |0\rangle \\
&= \hat U \hat a_1^\dagger \underbrace{\hat U^\dagger \hat U}_{= \mathbb{1}} \hat a_2^\dagger
\underbrace{\hat U^\dagger \hat U}_{= \mathbb{1}} |0\rangle \\
&\overset{\hat U |0\rangle = |0\rangle}{=} \hat U \hat a_1^\dagger \hat U^\dagger \hat U \hat a_2^\dagger \hat U^\dagger
|0\rangle .
\end{aligned}
\tag{1.61}
$$

Nyní můžeme využít vztah (1.31) a psát

$$
\hat U \hat a_1^\dagger \hat U^\dagger = \frac{1}{\sqrt{2}} (\hat a_1^\dagger + \hat a_2^\dagger),
\tag{1.62}
$$

$$
\hat U \hat a_2^\dagger \hat U^\dagger = \frac{1}{\sqrt{2}} (-\hat a_1^\dagger + \hat a_2^\dagger),
\tag{1.63}
$$

z čehož plyne

$$
\hat U |1, 1\rangle = \frac{1}{2} (\hat a_1^\dagger + \hat a_2^\dagger)(-\hat a_1^\dagger + \hat a_2^\dagger) |0\rangle
= \frac{1}{\sqrt{2}} (|2, 0\rangle + |0, 2\rangle),
\tag{1.64}
$$

kde jsme využili komutativitu kreačních operátorů a vztah (1.2). Pravděpodobnost výsledku $(2, 0)$ i $(0, 2)$ je
tedy $0{,}5$, zatímco výsledek $(1, 1)$ nastat nemůže. Tento jev se nazývá Hong–Ou–Mandelův jev [37].

*(Pozn. překl.: Po roznásobení vychází $\hat U |1, 1\rangle = \frac{1}{\sqrt{2}}(-|2, 0\rangle + |0, 2\rangle)$,
protože $\frac{1}{2}(-\hat a_1^{\dagger 2} + \hat a_2^{\dagger 2})|0\rangle$ dává u $|2, 0\rangle$ záporné znaménko;
v (1.64) originálu toto minus chybí. Na pravděpodobnostech to nic nemění.)*

```python
import numpy as np
import piquasso as pq

shots = 100

with pq.Program() as program:
    pq.Q() | pq.StateVector(occupation_numbers=(1, 1))

    pq.Q() | pq.Beamsplitter(theta=np.pi/4, phi=0.0)

simulator = pq.SamplingSimulator(d=2)

state = simulator.execute(program).state

print("Probability of (2, 0):", state.get_particle_detection_probability((2, 0)))
print("Probability of (0, 2):", state.get_particle_detection_probability((0, 2)))
```

**Cvičení 1.7.5.** Uvažujte stav $|4\rangle$ a aplikujte na něj ztrátu fotonů s $\eta = 0{,}5$. Jaká je
pravděpodobnost, že následná detekce fotonů naměří 2 fotony? Je možné, že nezůstane žádný foton?

*Řešení.* Pravděpodobnost lze přímo spočítat ze vztahu (1.59):

$$
\binom{n}{k} \eta^k (1 - \eta)^{n-k} = \binom{4}{2} \times 0{,}5^2 \times 0{,}5^2 = 3/8.
\tag{1.65}
$$

*(Pozn. překl.: Na druhou otázku řešení přímo neodpovídá: ano, pro $k = 0$ dává tentýž vzorec pravděpodobnost
$(1 - \eta)^4 = 0{,}5^4 = 1/16$.)*

**Cvičení 1.7.6.** Namodelujte předchozí situaci v Piquassu pomocí módu prostředí a děliče svazku. Ověřte
v Piquassu, že výsledný stavový vektor odpovídá očekávanému.

*Řešení.* Kód v Piquassu:

```python
import piquasso as pq

with pq.Program() as program:
    pq.Q() | pq.StateVector(occupation_numbers=(4, 0))  # |1, 1>

    pq.Q(0, 1) | pq.Beamsplitter()

# Alternativní zápis
# program = pq.Program(instructions=[pq.StateVector(occupation_numbers=(1, 1)).on_modes(0, 1)])

simulator = pq.SamplingSimulator(d=2)

result = simulator.execute(program, shots=20)

state = result.state

print("probability of |2, 2>: ", state.get_particle_detection_probability((2, 2)))
```

*(Pozn. překl.: Komentář `# |1, 1>` a alternativní zápis zůstaly v kódu z předchozích cvičení; program připravuje
stav $|4, 0\rangle$, v němž mód 1 hraje roli prostředí. `Beamsplitter()` bez parametrů je v Piquassu dělič 50/50
($\theta = \pi/4$), tedy $\eta = \cos^2\theta = 0{,}5$, a pravděpodobnost výsledku $|2, 2\rangle$ (2 fotony zůstanou,
2 se ztratí) má podle (1.65) vyjít 3/8.)*
""")

CHAPTER = PrimerChapter(
    label="Kapitola 1",
    title="Základy fotonického kvantového počítání",
    intro=r"""
Základem fotonického kvantového počítání je studium bosonových kvantových systémů. Tato kapitola proto probírá
základy a zavádí hlavní pojmy, které v celém textu používáme. Pro úplnost je stručné shrnutí obecných kvantových
systémů uvedeno v dodatku A. Výklad začíná rovnou reprezentací obsazovacích čísel; zvídavému čtenáři však
doporučujeme nahlédnout do dodatku B, kde se dozví, jak se obsazovací čísla získají z jednočásticových vlnových
funkcí.
""",
    sections=(
        INTRODUCTION, SECTION_1_1, SECTION_1_2, SECTION_1_3, SECTION_1_4, SECTION_1_5, SECTION_1_6, SECTION_1_7,
    ),
    original_pages="5–16",
)
