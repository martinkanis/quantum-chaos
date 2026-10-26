"""Czech translation of chapter 3 of the primer by Kolarovszki and Zimborás (ui/primer_content.py)."""

from __future__ import annotations

from ui.primer_content import PrimerChapter, PrimerSection

INTRO = r"""Tato kapitola podává rychlý a nepříliš rigorózní („quick and dirty“) úvod do formulace kvantové optiky
ve fázovém prostoru (phase space formulation), což je velmi užitečný formalismus. Budeme k tomu používat následující
šikovný vzorec pro gaussovské integrály (Gaussian integrals):

$$
\int_{\mathbb{C}^{d}} \exp\left(-\frac{1}{2}\breve{\pmb{\alpha}}^\dagger \Sigma \breve{\pmb{\alpha}} +
\breve{\pmb{\beta}}^\dagger \breve{\pmb{\alpha}}\right) \mathrm{d}^{2d}\pmb{\alpha}
= \frac{(2\pi)^d}{\sqrt{\det\Sigma}}
\exp\left(\frac{1}{2}\breve{\pmb{\beta}}^\dagger \Sigma^{-1} \breve{\pmb{\beta}}\right),
\tag{3.1}
$$

pro samosdruženou (self-adjoint) matici $\Sigma \in \mathbb{C}^{2d\times 2d}$ takovou, že
$W^\dagger \Sigma W \in \mathbb{R}^{2d\times 2d}$, a pro $\pmb{\beta} \in \mathbb{C}^d$.

*(Pozn. překl.: Při konvenci
$\mathrm{d}^2\alpha = \mathrm{d}\operatorname{Re}\alpha\,\mathrm{d}\operatorname{Im}\alpha$,
kterou skripta zavádějí u vztahu (3.13), má na pravé straně stát $\pi^d/\sqrt{\det\Sigma}$ místo
$(2\pi)^d/\sqrt{\det\Sigma}$: pro $d = 1$, $\Sigma = \mathbb{1}$ a $\pmb{\beta} = 0$ je levá strana
$\int_{\mathbb{C}} e^{-|\alpha|^2}\,\mathrm{d}^2\alpha = \pi$. Výsledky (3.56) a (3.76) odpovídají správnému
faktoru $\pi^d$.)*"""

SECTION_3_1 = PrimerSection(anchor="skripta-3-1", number="3.1", title="Weylovy operátory a koherentní stavy", body=r"""
Důležitou vlastností koherentních stavů (coherent states) z oddílu 2.1 je, že jsou vlastními vektory anihilačního
operátoru (annihilation operator), tj.

$$
a|\alpha\rangle = \alpha|\alpha\rangle,
\tag{3.2}
$$

protože

$$
a|\alpha\rangle = D(\alpha)D^\dagger(\alpha)\,a\,D(\alpha)|0\rangle = D(\alpha)(a+\alpha)|0\rangle
= \alpha D(\alpha)|0\rangle = \alpha|\alpha\rangle.
\tag{3.3}
$$

Odtud lze odvodit

$$
|\alpha\rangle = e^{-\frac{|\alpha|^2}{2}} \sum_{n=0}^{\infty} \frac{\alpha^n}{\sqrt{n!}} |n\rangle.
\tag{3.4}
$$

Pomocí Bakerovy–Campbellovy–Hausdorffovy formule (Baker–Campbell–Hausdorff formula) navíc můžeme psát

$$
D(\alpha) = e^{\alpha\hat a^\dagger - \overline{\alpha}a}
= e^{\alpha\hat a^\dagger} e^{-\overline{\alpha}a} e^{\frac{1}{2}[\alpha\hat a^\dagger, \overline{\alpha}a]}
= e^{\alpha\hat a^\dagger} e^{-\overline{\alpha}a} e^{-\frac{|\alpha|^2}{2}}.
\tag{3.5}
$$

Weylovy operátory (Weyl operators) mají následující důležitou vlastnost:

**Tvrzení 5.** Weylovy operátory splňují následující multiplikativní vztah:

$$
D(\alpha)D(\beta) = e^{\frac{1}{2}(\alpha\overline{\beta} - \overline{\alpha}\beta)} D(\alpha+\beta).
\tag{3.6}
$$

*Důkaz.* Použijeme speciální případ Bakerovy–Campbellovy–Hausdorffovy formule, podle něhož

$$
e^X e^Y = e^{X+Y} e^{\frac{1}{2}[X,Y]},
\tag{3.7}
$$

pokud $[X, Y]$ komutuje s $X$ i s $Y$. V našem případě je

$$
X = \alpha\hat a^\dagger - \overline{\alpha}a,
\tag{3.8a}
$$

$$
Y = \beta\hat a^\dagger - \overline{\beta}a,
\tag{3.8b}
$$

a skutečně můžeme psát

$$
[X, Y] = (\alpha\overline{\beta} - \overline{\alpha}\beta)\underbrace{[a, \hat a^\dagger]}_{=\mathbb{1}}
= (\alpha\overline{\beta} - \overline{\alpha}\beta)\mathbb{1},
\tag{3.9}
$$

z čehož ihned plyne

$$
D(\alpha)D(\beta) = e^{\frac{1}{2}(\alpha\overline{\beta} - \overline{\alpha}\beta)} D(\alpha+\beta).
\tag{3.10}
$$

∎

Důsledkem je, že Weylovy operátory komutují až na fázi, tj.

$$
D(\alpha)D(\beta) = e^{\alpha\overline{\beta} - \overline{\alpha}\beta} D(\beta)D(\alpha).
\tag{3.11}
$$

Jako další důsledek můžeme zapsat překryv koherentních stavů:

$$
\begin{aligned}
\langle\beta|\alpha\rangle &= \langle 0|D(-\beta)D(\alpha)|0\rangle
= e^{-\frac{1}{2}(\alpha\overline{\beta} - \overline{\alpha}\beta)}
\underbrace{\langle 0|D(\alpha-\beta)|0\rangle}_{=\langle 0|\alpha-\beta\rangle} \\
&= e^{-\frac{1}{2}(\alpha\overline{\beta} - \overline{\alpha}\beta)} e^{-\frac{1}{2}|\alpha-\beta|^2}
\neq \delta^{(2)}(\alpha-\beta),
\end{aligned}
\tag{3.12}
$$

kde $\delta^{(2)}(\gamma)$ chápeme jako
$\delta^{(2)}(\gamma) = \delta(\operatorname{Re}(\gamma))\,\delta(\operatorname{Im}(\gamma))$
a $\delta$ je Diracova delta distribuce. To znamená, že koherentní stavy (nepřekvapivě) nejsou ortogonální. Můžeme však
ukázat, že tvoří *úplný systém* (complete set), tj. že jednotkový operátor lze zapsat jako vážený integrál přes
koherentní stavy.

*(Pozn. překl.: Podle tvrzení 5 je
$D(-\beta)D(\alpha) = e^{\frac{1}{2}(\alpha\overline{\beta} - \overline{\alpha}\beta)}D(\alpha-\beta)$,
ve fázovém faktoru (3.12) má tedy být v exponentu znaménko plus. Absolutní hodnotu
$|\langle\beta|\alpha\rangle| = e^{-\frac{1}{2}|\alpha-\beta|^2}$, kterou využívá cvičení 3.5.4, to neovlivní.)*

**Tvrzení 6 (rozklad jednotky, resolution of identity).** Koherentní stavy rozkládají jednotkový operátor na Fockově
prostoru (Fock space), tj.

$$
\mathbb{1} = \frac{1}{\pi}\int_{\mathbb{C}} |\alpha\rangle\langle\alpha|\,\mathrm{d}^2\alpha,
\tag{3.13}
$$

kde $\mathrm{d}^2\alpha$ je zkratka pro $\mathrm{d}\operatorname{Re}\alpha\,\mathrm{d}\operatorname{Im}\alpha$.

*Důkaz.* Dosadíme vztah (3.4) a přejdeme do polárních souřadnic. Přímo dostaneme

$$
\frac{1}{\pi}\int_{\mathbb{C}} |\alpha\rangle\langle\alpha|\,\mathrm{d}^2\alpha
= \sum_{n,m=0}^{\infty} \frac{1}{\pi\sqrt{n!\,m!}} \int_{\mathbb{C}} e^{-|\alpha|^2}\alpha^n\overline{\alpha}^m\,
\mathrm{d}^2\alpha\,|n\rangle\langle m|.
\tag{3.14}
$$

Integrál v polárních souřadnicích můžeme zapsat jako

$$
\begin{aligned}
\int_{\mathbb{C}} e^{-|\alpha|^2}\alpha^n\overline{\alpha}^m\,\mathrm{d}^2\alpha
&= \int_0^{2\pi}\int_0^{\infty} e^{-r^2} r^{n+m+1} e^{i(n-m)\varphi}\,\mathrm{d}r\,\mathrm{d}\varphi \\
&= 2\pi\delta_{nm}\underbrace{\int_0^{\infty} e^{-r^2} r^{2n+1}\,\mathrm{d}r}_{=\frac{n!}{2}}
= \pi\delta_{nm}\,n!,
\end{aligned}
\tag{3.15}
$$

a přímým dosazením dostaneme

$$
\frac{1}{\pi}\int_{\mathbb{C}} |\alpha\rangle\langle\alpha|\,\mathrm{d}^2\alpha
= \sum_{n=0}^{\infty} |n\rangle\langle n|
= \mathbb{1}.
\tag{3.16}
$$

∎

Protože koherentní stavy rozkládají jednotku, ale *nejsou* ortogonální, tvoří *přeúplný systém* (overcomplete set),
tj. systém, který zůstane úplný i po odebrání libovolného prvku. Stopu (trace) operátoru $\hat O$ proto můžeme zapsat
jako integrál přes fázový prostor (phase space):

$$
\operatorname{Tr}\hat O = \sum_{n=0}^{\infty}\langle n|\hat O|n\rangle
= \frac{1}{\pi}\int_{\mathbb{C}}\langle\alpha|\hat O|\alpha\rangle\,\mathrm{d}^2\alpha.
\tag{3.17}
$$

Pro zobecnění na více kvantových módů (qumodes) zapíšeme $d$-módový Weylův operátor jako

$$
D(\pmb{\alpha}) := \prod_{i=1}^{d} D(\alpha_i) = \exp\left(-\breve{\pmb{\alpha}}^\dagger K\pmb{\xi}\right),
\tag{3.18}
$$

kde $\breve{\pmb{\alpha}} := [\pmb{\alpha}, \overline{\pmb{\alpha}}]^T$ a stejně jako dříve

$$
K := \begin{bmatrix} \mathbb{1} & \\ & -\mathbb{1} \end{bmatrix},
\tag{3.19}
$$

přičemž $\pmb{\xi}$ je vektor posunovacích (žebříkových) operátorů (ladder operators) definovaný v oddílu 1.1.
Pro vícemódový Weylův operátor platí následující velmi užitečný vztah. Uvažujme lineární hradlo $U$ a jeho
symplektickou matici $S$ v komplexním tvaru. Pak

$$
\begin{aligned}
U^\dagger D(\pmb{\alpha})U &= \exp\left(-\breve{\pmb{\alpha}}^\dagger KS\pmb{\xi}\right)
= \exp\left(-\breve{\pmb{\alpha}}^\dagger (S^{-1})^\dagger K\pmb{\xi}\right) \\
&= \exp\left(-(S^{-1}\breve{\pmb{\alpha}})^\dagger K\pmb{\xi}\right)
= D\left((S^{-1}\breve{\pmb{\alpha}})_{1:d}\right).
\end{aligned}
\tag{3.20}
$$

To znamená, že transformace Weylova operátoru gaussovským hradlem odpovídá změně báze ve fázovém prostoru.
""")

SECTION_3_2 = PrimerSection(anchor="skripta-3-2", number="3.2", title="Fourierova–Weylova relace", body=r"""
Nyní můžeme propojit operátory s funkcemi na fázovém prostoru. Opírá se to o skutečnost, že Weylovy operátory tvoří
v prostoru operátorů ortogonální úplný systém vzhledem k Hilbertovu–Schmidtovu skalárnímu součinu (Hilbert–Schmidt
inner product) definovanému vztahem $\langle A, B\rangle_{\mathrm{HS}} := \operatorname{Tr} A^\dagger B$.

**Tvrzení 7.** Stopu Weylova operátoru lze spočítat takto:

$$
\operatorname{Tr}D(\alpha) = \pi\delta^{(2)}(\alpha),
\tag{3.21}
$$

kde $\delta^{(2)}(\alpha)$ chápeme jako
$\delta^{(2)}(\alpha) = \delta(\operatorname{Re}(\alpha))\,\delta(\operatorname{Im}(\alpha))$
a $\delta$ je Diracova delta distribuce.

*Důkaz.* Můžeme psát

$$
\operatorname{Tr}D(\alpha) = \frac{1}{\pi}\int_{\mathbb{C}}\langle\beta|D(\alpha)|\beta\rangle\,\mathrm{d}^2\beta.
\tag{3.22}
$$

Weylův operátor lze rozložit jako

$$
D(\alpha) = e^{\alpha\hat a^\dagger} e^{-\overline{\alpha}a} e^{-\frac{|\alpha|^2}{2}},
\tag{3.23}
$$

a proto

$$
\langle\beta|D(\alpha)|\beta\rangle = e^{\alpha\overline{\beta}} e^{-\overline{\alpha}\beta} e^{-\frac{|\alpha|^2}{2}},
\tag{3.24}
$$

a tedy

$$
\operatorname{Tr}D(\alpha) = e^{-\frac{|\alpha|^2}{2}} \frac{1}{\pi}\int_{\mathbb{C}} e^{\alpha\overline{\beta}}
e^{-\overline{\alpha}\beta}\,\mathrm{d}^2\beta.
\tag{3.25}
$$

Nyní položme $\alpha = a + ib$ a $\beta = x + iy$, takže můžeme psát

$$
\alpha\overline{\beta} - \overline{\alpha}\beta = 2i(bx - ay),
\tag{3.26}
$$

a tedy

$$
\operatorname{Tr}D(\alpha) = e^{-\frac{|\alpha|^2}{2}} \frac{1}{\pi}\int_{-\infty}^{\infty} e^{2ibx}\,\mathrm{d}x
\int_{-\infty}^{\infty} e^{-2iay}\,\mathrm{d}y.
\tag{3.27}
$$

Nakonec použijeme vztah

$$
\delta(a) = \frac{1}{2\pi}\int_{-\infty}^{\infty} e^{iax}\,\mathrm{d}x
\tag{3.28}
$$

a dostaneme

$$
\operatorname{Tr}D(\alpha) = e^{-\frac{|\alpha|^2}{2}} \frac{1}{\pi}\pi^2\delta(a)\delta(b) = \pi\delta(a)\delta(b)
= \pi\delta^{(2)}(\alpha).
\tag{3.29}
$$

∎

**Tvrzení 8.** Vakuový stav lze vyjádřit jako vážený integrál přes Weylovy operátory:

$$
|0\rangle\langle 0| = \frac{1}{\pi}\int_{\mathbb{C}} e^{-\frac{|\gamma|^2}{2}} D(\gamma)\,\mathrm{d}^2\gamma.
\tag{3.30}
$$

*Důkaz.* Označme

$$
\hat O = \frac{1}{\pi}\int_{\mathbb{C}} e^{-\frac{|\gamma|^2}{2}} D(\gamma)\,\mathrm{d}^2\gamma.
\tag{3.31}
$$

Ihned vidíme, že tento operátor je ortogonální projektor, tj. $\hat O^2 = \hat O^\dagger = \hat O$. Navíc má jednotkovou
stopu, protože $\operatorname{Tr}D(\alpha) = \pi\delta^{(2)}(\alpha)$. Konečně víme, že se s $|0\rangle\langle 0|$
plně překrývá:

$$
\langle 0|\hat O|0\rangle = \frac{1}{\pi}\int_{\mathbb{C}} e^{-|\gamma|^2}\,\mathrm{d}^2\gamma = 1.
\tag{3.32}
$$

Musí tedy platit $\hat O = |0\rangle\langle 0|$. ∎

To znamená, že vakuum můžeme zapsat jako vážený integrál přes Weylovy operátory. Tato skutečnost platí obecněji
a tvrzení 8 je jen speciálním případem následujícího vztahu:

**Věta 3.2.1 (Fourierova–Weylova relace).** Omezený operátor $\hat O$ na jednomódovém bosonovém Fockově prostoru lze
zapsat jako vážený integrál přes fázový prostor:

$$
\hat O = \frac{1}{\pi}\int_{\mathbb{C}} \operatorname{Tr}\left[D(\alpha)\hat O\right] D(-\alpha)\,\mathrm{d}^2\alpha.
\tag{3.33}
$$

*Důkaz.* Především každý omezený operátor $\hat O$ lze zapsat jako

$$
\hat O = \frac{1}{\pi^2}\int_{\mathbb{C}^2} \langle\alpha|\hat O|\beta\rangle\,|\alpha\rangle\langle\beta|\,
\mathrm{d}^2\alpha\,\mathrm{d}^2\beta.
\tag{3.34}
$$

Pokud tedy ukážeme, že

$$
|\alpha\rangle\langle\beta| = \frac{1}{\pi}\int_{\mathbb{C}} \langle\beta|D(\gamma)|\alpha\rangle\,
D(-\gamma)\,\mathrm{d}^2\gamma,
\tag{3.35}
$$

jsme hotovi. Přímým výpočtem dostaneme

$$
\begin{aligned}
D(-\beta)D(\gamma)D(\alpha)
&\overset{\text{tvrzení 5}}{=} e^{-\frac{1}{2}(\beta\overline{\gamma} - \overline{\beta}\gamma)}
D(\gamma-\beta)D(\alpha) \\
&\overset{\text{tvrzení 5}}{=} e^{-\frac{1}{2}(\beta\overline{\gamma} - \overline{\beta}\gamma)}
e^{\frac{1}{2}((\gamma-\beta)\overline{\alpha} - \overline{(\gamma-\beta)}\alpha)} D(\alpha+\gamma-\beta),
\end{aligned}
\tag{3.36}
$$

z čehož plyne

$$
\begin{aligned}
\langle\beta|D(\gamma)|\alpha\rangle
&= e^{-\frac{1}{2}(\beta\overline{\gamma} - \overline{\beta}\gamma)}
e^{\frac{1}{2}((\gamma-\beta)\overline{\alpha} - \overline{(\gamma-\beta)}\alpha)}
e^{-\frac{|\alpha+\gamma-\beta|^2}{2}} \\
&= \exp\left(-\frac{1}{2}\left(|\alpha|^2 + |\gamma|^2 + |\beta|^2\right) + \alpha\overline{\beta} -
\alpha\overline{\gamma} + \gamma\overline{\beta}\right).
\end{aligned}
\tag{3.37}
$$

Pomocí tvrzení 8 můžeme psát

$$
|\alpha\rangle\langle\beta| = D(\alpha)|0\rangle\langle 0|D(-\beta)
= \frac{1}{\pi}\int_{\mathbb{C}} e^{-\frac{|\gamma|^2}{2}} D(\alpha)D(\gamma)D(-\beta)\,\mathrm{d}^2\gamma,
\tag{3.38}
$$

kde

$$
\begin{aligned}
D(\alpha)D(\gamma)D(-\beta)
&\overset{\text{tvrzení 5}}{=} e^{\frac{1}{2}(\alpha\overline{\gamma} - \overline{\alpha}\gamma)}
D(\alpha+\gamma)D(-\beta) \\
&\overset{\text{tvrzení 5}}{=} e^{-\frac{1}{2}(\alpha\overline{\beta} - \overline{\alpha}\beta)}
e^{\frac{1}{2}((\alpha+\beta)\overline{\gamma} - \overline{(\alpha+\beta)}\gamma)} D(\alpha+\gamma-\beta),
\end{aligned}
\tag{3.39}
$$

což znamená, že

$$
\begin{aligned}
|\alpha\rangle\langle\beta|
&= \frac{1}{\pi} e^{-\frac{1}{2}(\alpha\overline{\beta} - \overline{\alpha}\beta)} \int_{\mathbb{C}}
e^{-\frac{|\gamma|^2}{2}} e^{\frac{1}{2}((\alpha+\beta)\overline{\gamma} - \overline{(\alpha+\beta)}\gamma)}
D(\alpha+\gamma-\beta)\,\mathrm{d}^2\gamma \\
&\overset{-\sigma = \alpha+\gamma-\beta}{=}
\frac{1}{\pi} e^{-\frac{1}{2}(\alpha\overline{\beta} - \overline{\alpha}\beta)}
\int_{\mathbb{C}} e^{-\frac{|\beta-\alpha-\sigma|^2}{2}}
e^{\frac{1}{2}((\alpha+\beta)\overline{(\beta-\alpha-\sigma)} - \overline{(\alpha+\beta)}(\beta-\alpha-\sigma))}
D(-\sigma)\,\mathrm{d}^2\sigma \\
&= \frac{1}{\pi}\int_{\mathbb{C}} \underbrace{\exp\left(-\frac{1}{2}\left(|\alpha|^2 + |\beta|^2 + |\sigma|^2\right) +
\alpha\overline{\beta} - \alpha\overline{\sigma} + \sigma\overline{\beta}\right)}
_{=\langle\beta|D(\sigma)|\alpha\rangle}
D(-\sigma)\,\mathrm{d}^2\sigma \\
&= \frac{1}{\pi}\int_{\mathbb{C}} \langle\beta|D(\sigma)|\alpha\rangle\, D(-\sigma)\,\mathrm{d}^2\sigma.
\end{aligned}
\tag{3.40}
$$

∎
""")

SECTION_3_3 = PrimerSection(anchor="skripta-3-3", number="3.3", title="Charakteristické funkce a Wignerova funkce",
                            body=r"""
Fourierova–Weylova relace je hlavní motivací pro definici následující funkce:

**Definice 3.3.1 (charakteristická funkce).** Pro stav $\rho$ definujeme *charakteristickou funkci* (characteristic
function) jako

$$
\chi_\rho(\alpha) := \operatorname{Tr}\left[D(\alpha)\rho\right].
\tag{3.41}
$$

Význam charakteristické funkce plyne z Fourierovy–Weylovy relace, podle níž lze operátor hustoty (density operator)
$\rho$ zapsat jako integrál přes fázový prostor

$$
\rho = \frac{1}{\pi}\int_{\mathbb{C}} \chi_\rho(\alpha) D(-\alpha)\,\mathrm{d}^2\alpha,
\tag{3.42}
$$

a $\chi_\rho$ tedy nese úplnou informaci o kvantovém stavu $\rho$. Podmínka $\operatorname{Tr}\rho = 1$ se projeví jako

$$
\chi_\rho(0) = 1
\tag{3.43}
$$

a hermitovskost $\rho$ jako

$$
\overline{\chi_\rho(\alpha)} = \chi_\rho(-\overline{\alpha}).
\tag{3.44}
$$

*(Pozn. překl.: Protože $D(\alpha)^\dagger = D(-\alpha)$ a $\rho^\dagger = \rho$, vychází správně
$\overline{\chi_\rho(\alpha)} = \chi_\rho(-\alpha)$, bez komplexního sdružení v argumentu.)*

**Příklad (charakteristická funkce vakua).** Charakteristickou funkci jednomódového vakuového stavu (vacuum state)
lze snadno spočítat:

$$
\chi_{|0\rangle\langle 0|}(\alpha) = \operatorname{Tr}\left[D(\alpha)|0\rangle\langle 0|\right]
= \langle 0|D(\alpha)|0\rangle = e^{-\frac{|\alpha|^2}{2}}.
\tag{3.45}
$$

Pro vícemódový stav $\rho$ se charakteristická funkce definuje analogicky pomocí vícemódového Weylova operátoru:

$$
\chi_\rho(\pmb{\alpha}) := \operatorname{Tr}\left[D(\pmb{\alpha})\rho\right].
\tag{3.46}
$$

Důležitým faktem je, že skládání operátorů hustoty z více podsystémů odpovídá na úrovni charakteristických funkcí
součinu: pro operátory hustoty $\rho_A$, $\rho_B$ na podsystémech $A$, $B$ můžeme charakteristickou funkci složeného
systému zapsat jako

$$
\chi_{\rho_A\otimes\rho_B}(\pmb{\alpha}_A \oplus \pmb{\alpha}_B) = \chi_{\rho_A}(\pmb{\alpha}_A)\,
\chi_{\rho_B}(\pmb{\alpha}_B).
\tag{3.47}
$$

**Příklad (charakteristická funkce centrovaných čistých gaussovských stavů).** Víme, že $d$-módový centrovaný čistý
gaussovský stav (Gaussian state) lze zapsat jako

$$
\rho = G|0\rangle\langle 0|G^\dagger,
\tag{3.48}
$$

kde $G$ je unitární operátor gaussovského hradla. Symplektickou matici (v komplexním tvaru) tohoto gaussovského hradla
označme $S$. Charakteristickou funkci pak můžeme spočítat přímo:

$$
\chi_\rho(\pmb{\alpha}) = \operatorname{Tr}\left[D(\pmb{\alpha})G|0\rangle\langle 0|G^\dagger\right]
= \operatorname{Tr}\left[\underbrace{G^\dagger D(\pmb{\alpha})G}_{=D((S^{-1}\breve{\pmb{\alpha}})_{1:d})}
|0\rangle\langle 0|\right],
\tag{3.49}
$$

kde dolní index $1:d$ znamená, že z vektoru vezmeme prvních $d$ složek. S využitím charakteristické funkce vakua tedy
víme, že

$$
\begin{aligned}
\chi_\rho(\pmb{\alpha})
&= e^{-\frac{1}{4}\breve{\pmb{\alpha}}^\dagger (S^{-1})^\dagger S^{-1}\breve{\pmb{\alpha}}}
\overset{\mathbb{1} = K^2}{=}
e^{-\frac{1}{4}\breve{\pmb{\alpha}}^\dagger (S^{-1})^\dagger K^2 S^{-1}\breve{\pmb{\alpha}}} \\
&\overset{SKS^\dagger = K}{=} e^{-\frac{1}{4}\breve{\pmb{\alpha}}^\dagger KSS^\dagger K\breve{\pmb{\alpha}}}
= e^{-\frac{1}{4}\breve{\pmb{\alpha}}^\dagger K\sigma^{(\mathrm{c})}K\breve{\pmb{\alpha}}},
\end{aligned}
\tag{3.50}
$$

protože kovarianční matici (covariance matrix) stavu $G|0\rangle\langle 0|G^\dagger$ lze zapsat jako

$$
\sigma^{(\mathrm{c})} = SS^\dagger.
\tag{3.51}
$$

Obdobné tvrzení platí i pro smíšené gaussovské stavy, stačí dosadit jejich kovarianční matici. Důležité je pozorování,
že protože charakteristická funkce plně určuje operátor hustoty, závisejí gaussovské stavy jen na svých prvních
a druhých statistických momentech.

### 3.3.1 Wignerova funkce

**Definice 3.3.2.** Wignerova funkce (Wigner function) $d$-módového stavu $\rho$ je definována jako

$$
W_\rho(\pmb{\alpha}) = \frac{1}{\pi^{2d}}\int_{\mathbb{C}^d}
e^{\pmb{\alpha}\overline{\pmb{\beta}} - \overline{\pmb{\alpha}}\pmb{\beta}} \chi_\rho(\pmb{\beta})\,
\mathrm{d}^{2d}\pmb{\beta}.
\tag{3.52}
$$

*Poznámka.* Člen $e^{\pmb{\alpha}\overline{\pmb{\beta}} - \overline{\pmb{\alpha}}\pmb{\beta}}$ v definici může působit
poněkud podivně, je ale dobře motivovaný: integrál lze interpretovat jako Fourierovu transformaci (Fourier transform)
definovanou na fázovém prostoru. Uvažujme zatím $d = 1$ a pišme $\alpha = x + ip$ a $\beta = u + iv$, takže

$$
\alpha\overline{\beta} - \overline{\alpha}\beta = 2i(pu - xv),
\tag{3.53}
$$

a tedy

$$
\begin{aligned}
W_\rho(x+ip) &= \frac{1}{\pi^2}\int_{-\infty}^{\infty}\int_{-\infty}^{\infty} e^{2i(pu-xv)}\chi_\rho(u+iv)\,
\mathrm{d}u\,\mathrm{d}v \\
&= \frac{1}{(2\pi)^2}\int_{-\infty}^{\infty}\int_{-\infty}^{\infty} e^{ipu} e^{-ixv}\chi_\rho(u+iv)\,
\mathrm{d}u\,\mathrm{d}v.
\end{aligned}
\tag{3.54}
$$

*(Pozn. překl.: Druhá rovnost vzniká substitucí $u \to u/2$, $v \to v/2$, po níž má charakteristická funkce
správně argument $(u+iv)/2$.)*

Lze ukázat, že Wignerova funkce je až na faktor $\frac{1}{2^{2d}}$ normalizovaná, tj.

$$
\frac{1}{2^{2d}}\int_{\mathbb{C}^d} W_\rho(\pmb{\alpha})\,\mathrm{d}^{2d}\pmb{\alpha} = 1,
\tag{3.55}
$$

není však nutně nezáporná, a proto ji obecně nelze přeškálovat na rozdělení pravděpodobnosti na $\mathbb{C}$
(např. pro Fockovy stavy jiné než vakuum). Z tohoto důvodu Wignerovu funkci (po normalizaci) nazýváme
*kvazipravděpodobnostním rozdělením* (quasiprobability distribution).

**Příklad (Wignerova funkce centrovaného čistého gaussovského stavu).** Wignerova funkce gaussovského stavu je prostě
gaussovská funkce, což lze ukázat výpočtem gaussovského integrálu s využitím vztahu (3.50):

$$
\begin{aligned}
W_\rho(\pmb{\alpha}) &= \frac{1}{\pi^{2d}}\int_{\mathbb{C}^d} e^{-\breve{\pmb{\alpha}}^\dagger K\breve{\pmb{\beta}}}
e^{-\frac{1}{4}\breve{\pmb{\beta}}^\dagger K\sigma^{(\mathrm{c})}K\breve{\pmb{\beta}}}\,\mathrm{d}^{2d}\pmb{\beta} \\
&= \frac{2^d}{\pi^d\sqrt{\det\sigma^{(\mathrm{c})}}}
e^{-\breve{\pmb{\alpha}}^\dagger(\sigma^{(\mathrm{c})})^{-1}\breve{\pmb{\alpha}}}.
\end{aligned}
\tag{3.56}
$$

Všimněme si, že je skutečně normalizovaná až na faktor $2^{-2d}$, protože

$$
\int_{\mathbb{C}^d} e^{-\breve{\pmb{\alpha}}^\dagger(\sigma^{(\mathrm{c})})^{-1}\breve{\pmb{\alpha}}}\,
\mathrm{d}^{2d}\pmb{\alpha} = (2\pi)^d\sqrt{\det\sigma^{(\mathrm{c})}}.
\tag{3.57}
$$

*(Pozn. překl.: Z definice (3.52) a vztahu (3.28) plyne přímo
$\int_{\mathbb{C}^d} W_\rho(\pmb{\alpha})\,\mathrm{d}^{2d}\pmb{\alpha} = \chi_\rho(0) = 1$, Wignerova funkce je tedy
normalizovaná i bez faktoru $2^{-2d}$ ve (3.55). Integrál (3.57) má správně hodnotu
$(\pi/2)^d\sqrt{\det\sigma^{(\mathrm{c})}}$ (pro vakuum je
$\int_{\mathbb{C}} e^{-2|\alpha|^2}\,\mathrm{d}^2\alpha = \pi/2$), takže i (3.56) je normalizovaná na jedničku.)*

### 3.3.2 $s$-uspořádané charakteristické funkce

V literatuře o kvantové optice se lze setkat s několika verzemi charakteristické funkce; souvisejí s různými
uspořádáními operátorů, která z nich lze získat.

**Definice 3.3.3 ($s$-uspořádaná charakteristická funkce).** Pro operátor hustoty $\rho$ je *$s$-uspořádaná
charakteristická funkce* ($s$-ordered characteristic function) definována jako

$$
\chi_\rho^{(s)}(\pmb{\alpha}) = \chi_\rho(\pmb{\alpha})\,e^{\frac{s}{2}\lVert\pmb{\alpha}\rVert^2}.
\tag{3.58}
$$

Zajímají nás případy $s = -1, 0, 1$, a když mluvíme o „té“ charakteristické funkci, máme obvykle na mysli případ
$s = 0$. Exponenciální člen je motivován následujícími vztahy:

$$
D(\pmb{\alpha}) = e^{\pmb{\alpha}\hat a^\dagger} e^{-\overline{\pmb{\alpha}}a}
e^{-\frac{1}{2}\lVert\pmb{\alpha}\rVert^2}
\qquad (s = +1),
\tag{3.59}
$$

$$
D(\pmb{\alpha}) = e^{-\overline{\pmb{\alpha}}a} e^{\pmb{\alpha}\hat a^\dagger}
e^{+\frac{1}{2}\lVert\pmb{\alpha}\rVert^2}
\qquad (s = -1).
\tag{3.60}
$$

První vztah jsme už viděli ve (3.5), druhý lze získat analogicky. Zajímají nás především proto, že jde o vytvořující
funkce (generating functions) normálně a antinormálně uspořádaných středních hodnot posunovacích operátorů:

$$
\begin{aligned}
\operatorname{Tr}\left[(\hat a_1^\dagger)^{n_1}\cdots(\hat a_d^\dagger)^{n_d} a_1^{m_1}\cdots a_d^{m_d}\rho\right]
&= (-1)^{\mathbf{m}} \left(\frac{\partial}{\partial\pmb{\alpha}}\right)^{\mathbf{n}}
\left(\frac{\partial}{\partial\overline{\pmb{\alpha}}}\right)^{\mathbf{m}}
\chi_\rho^{(1)}(\pmb{\alpha})\Big|_{\pmb{\alpha}=0}, && \text{(normální uspořádání)} \\
\operatorname{Tr}\left[(\hat a_1^\dagger)^{m_1}\cdots(\hat a_d^\dagger)^{m_d} a_1^{n_1}\cdots a_d^{n_d}\rho\right]
&= (-1)^{\mathbf{m}} \left(\frac{\partial}{\partial\pmb{\alpha}}\right)^{\mathbf{n}}
\left(\frac{\partial}{\partial\overline{\pmb{\alpha}}}\right)^{\mathbf{m}}
\chi_\rho^{(-1)}(\pmb{\alpha})\Big|_{\pmb{\alpha}=0}. && \text{(antinormální uspořádání)}
\end{aligned}
\tag{3.61}
$$

Použili jsme zde multiindexový zápis. Podobně pro $s = 0$ dává tatáž derivace normalizovaný součet středních hodnot
přes všechna možná uspořádání $n$ kreačních a $m$ anihilačních operátorů, tzv. *symetrické uspořádání* (symmetric
ordering). Případy $s = -1, 0, 1$ tedy odpovídají středním hodnotám součinů posunovacích operátorů v antinormálním,
symetrickém a normálním uspořádání (anti-normal, symmetric and normal ordering).

*(Pozn. překl.: Derivace $\chi_\rho^{(-1)}$ ve druhém řádku (3.61) dává antinormálně uspořádanou střední hodnotu
s anihilačními operátory vlevo, pro jeden mód $\operatorname{Tr}[a^m(\hat a^\dagger)^n\rho]$; levá strana druhého
řádku v originále je uspořádaná normálně.)*

Nabízí se otázka: jaké jsou tyto střední hodnoty pro gaussovské stavy, tj. co dá vztah (3.61), dosadíme-li do něj
charakteristickou funkci gaussovského stavu? K tomu potřebujeme určit libovolné derivace gaussovských funkcí v bodě
$\pmb{\alpha} \equiv 0$. Abychom tyto střední hodnoty vyjádřili kompaktněji, použijeme následující veličinu, zvanou
*hafnián* (hafnian).

**Definice 3.3.4 (hafnián).** *Hafnián* symetrické matice $A$ rozměru $2m \times 2m$ je definován jako

$$
\operatorname{haf}(A) := \sum_{p\in\mathrm{PM}([2m])}\prod_{(i,j)\in p} A_{ij},
\tag{3.62}
$$

kde $\mathrm{PM}([2m])$ označuje množinu perfektních párování (perfect matchings) množiny $[2m]$.

**Tvrzení 9.** Uvažujme symetrickou matici $\Sigma \in \mathbb{R}^{n\times n}$ a řetězec nezáporných celých čísel
(nat-string) $\mathbf{n} \in \mathbb{N}_0^n$. Pak

$$
\left(\frac{\partial}{\partial\mathbf{x}}\right)^{\mathbf{n}}
\exp\left(\frac{1}{2}\mathbf{x}^T\Sigma\mathbf{x}\right)\bigg|_{\mathbf{x}=0}
= \operatorname{haf}(\mathrm{r}_{\mathbf{n}}(\Sigma)).
\tag{3.63}
$$

*Důkaz.* Uvažujme nejprve případ $\mathbf{n} = (1, \dots, 1)$. Rozviňme exponenciálu:

$$
\exp\left(\frac{1}{2}\mathbf{x}^T\Sigma\mathbf{x}\right)
= \sum_{k=0}^{\infty}\frac{1}{2^k k!}\left(\sum_{i,j=1}^{n}\Sigma_{ij}x_i x_j\right)^{k}.
\tag{3.64}
$$

Hledáme koeficient u $x_1 \cdots x_n$, který je zjevně nulový pro liché $n$, protože členy $x_i$ se ve vzorci
vyskytují po dvojicích. Je-li $n = 2m$ sudé, musíme započítat všechna párování indexů $[2m] := (1, \dots, 2m)$.
Dané párování však lze získat $2^m m!$ způsoby, což se vykrátí se jmenovatelem, a koeficient u $x_1 \cdots x_n$
je proto

$$
\sum_{p\in\mathrm{PM}([2m])}\prod_{(i,j)\in p}\Sigma_{ij} = \operatorname{haf}(\Sigma).
\tag{3.65}
$$

*(Pozn. překl.: V originále má řada (3.64) sčítací index $n$, stejný jako rozměr, a u závorky chybí exponent;
index jsme přeznačili na $k$. K hledanému koeficientu přispívá jen člen $k = m$, proto v textu stojí $2^m m!$
(v originále „$2^n n!$“ ve smyslu sčítacího indexu).)*

Pro další zobecnění uvažujme $\mathbf{n} \in \{0, 1\}^n$ a označme $I$ množinu indexů, v nichž je složka
$\mathbf{n}$ rovna 1. Exponenciálu pak můžeme rozložit:

$$
\begin{aligned}
\exp\left(\frac{1}{2}\mathbf{x}^T\Sigma\mathbf{x}\right)
&= \exp\left(\frac{1}{2}\sum_{\substack{i\in I\\ j\in I}}\Sigma_{ij}x_i x_j\right) \\
&\quad\times\exp\left(\frac{1}{2}\left(\sum_{\substack{i\notin I\\ j\in I}}\Sigma_{ij}x_i x_j +
\sum_{\substack{i\in I\\ j\notin I}}\Sigma_{ij}x_i x_j +
\sum_{\substack{i\notin I\\ j\notin I}}\Sigma_{ij}x_i x_j\right)\right).
\end{aligned}
\tag{3.66}
$$

Víme, že druhá exponenciála nepřispívá, protože derivováním by z ní vystoupily členy $x_i$ s $i \notin I$, a ty tedy
nepřispějí. V tomto případě tak dostaneme

$$
\left(\frac{\partial}{\partial\mathbf{x}}\right)^{\mathbf{n}}
\exp\left(\frac{1}{2}\mathbf{x}^T\Sigma\mathbf{x}\right)\bigg|_{\mathbf{x}=0}
= \operatorname{haf}(\mathrm{r}_{\mathbf{n}}(\Sigma)).
\tag{3.67}
$$

Násobnosti lze ošetřit například tak, že proměnnou $x_i$ s násobností $n_i$ budeme považovat za $n_i$ nezávislých
proměnných $x_i^{(1)}, \dots, x_i^{(n_i)}$. ∎
""")

SECTION_3_4 = PrimerSection(anchor="skripta-3-4", number="3.4",
                            title="Glauberova–Sudarshanova P-reprezentace, Husimiho Q-funkce", body=r"""
**Definice 3.4.1 ($s$-uspořádané kvazipravděpodobnostní rozdělení).** $s$-uspořádané kvazipravděpodobnostní
rozdělení ($s$-ordered quasiprobability distribution) je definováno jako

$$
W_\rho^{(s)}(\pmb{\alpha}) = \frac{1}{\pi^{2d}}\int_{\mathbb{C}^d}
e^{\pmb{\alpha}\overline{\pmb{\beta}} - \overline{\pmb{\alpha}}\pmb{\beta}}\chi_\rho^{(s)}(\pmb{\beta})\,
\mathrm{d}^{2d}\pmb{\beta}.
\tag{3.68}
$$

Pro $s = 0$ dostaneme dříve zavedenou Wignerovu funkci.

**Věta 3.4.2 (Glauberova–Sudarshanova P-reprezentace kvantového stavu; Glauber–Sudarshan P-representation).**
$d$-módový operátor hustoty $\rho$ lze zapsat jako následující vážený integrál přes fázový prostor:

$$
\rho = \int_{\mathbb{C}^d} P_\rho(\pmb{\alpha})\,|\pmb{\alpha}\rangle\langle\pmb{\alpha}|\,\mathrm{d}^{2d}\pmb{\alpha},
\tag{3.69}
$$

kde se $P_\rho(\pmb{\alpha}) = W^{(+1)}(\pmb{\alpha})$ nazývá *P-funkce* (P-function).

*Důkaz.* Tuto větu zde dokazovat nebudeme; zájemce najde důkaz v [38]. ∎

Analogicky k P-funkci, která je definována pomocí charakteristické funkce pro $s = +1$, se Q-funkce definuje pomocí
případu $s = -1$:

**Definice 3.4.3 (Husimiho Q-funkce).** *Q-funkce* (Husimi Q-function) $d$-módového stavu s operátorem hustoty
$\rho$ je definována jako

$$
Q_\rho(\pmb{\alpha}) = W_\rho^{(-1)}(\pmb{\alpha}).
\tag{3.70}
$$

Q-funkci lze jednoduše zapsat jako

$$
Q_\rho(\pmb{\alpha}) = \frac{1}{\pi^d}\langle\pmb{\alpha}|\rho|\pmb{\alpha}\rangle.
\tag{3.71}
$$

Stejně jako charakteristická funkce určuje i Q-funkce kvantový stav úplně.

Poznamenejme, že P-funkce nemusí být funkcemi v obvyklém smyslu. Standardním příkladem je P-funkce jednomódového
Fockova stavu (Fock state):

**Tvrzení 10 (P-funkce jednomódových Fockových stavů).**

$$
P_{|n\rangle\langle n|}(\alpha) = \frac{e^{|\alpha|^2}}{n!}
\left(\frac{\partial^2}{\partial\alpha\,\partial\overline{\alpha}}\right)^n \delta^{(2)}(\alpha).
\tag{3.72}
$$

*Důkaz.* Můžeme psát

$$
|n\rangle\langle n| = \int_{\mathbb{C}} P(\alpha)\,|\alpha\rangle\langle\alpha|\,\mathrm{d}^2\alpha.
\tag{3.73}
$$

Překryv s koherentním stavem $|\beta\rangle\langle\beta|$ pak vyjádříme jako

$$
|\langle n|\beta\rangle|^2 = \frac{|\beta|^{2n}}{n!}e^{-|\beta|^2}
= \int_{\mathbb{C}} P(\alpha)|\langle\alpha|\beta\rangle|^2\,\mathrm{d}^2\alpha
= \int_{\mathbb{C}} P(\alpha)e^{-|\alpha-\beta|^2}\,\mathrm{d}^2\alpha.
\tag{3.74}
$$

Dosazením vztahu (3.72) dostaneme

$$
\begin{aligned}
\int_{\mathbb{C}} P(\alpha)e^{-|\alpha-\beta|^2}\,\mathrm{d}^2\alpha
&= \frac{1}{n!}\int_{\mathbb{C}} e^{-|\alpha-\beta|^2} e^{|\alpha|^2}
\left(\frac{\partial^2}{\partial\alpha\,\partial\overline{\alpha}}\right)^n \delta^{(2)}(\alpha)\,\mathrm{d}^2\alpha \\
&= \frac{1}{n!}\int_{\mathbb{C}} \delta^{(2)}(\alpha)
\left(\frac{\partial^2}{\partial\alpha\,\partial\overline{\alpha}}\right)^n e^{|\alpha|^2} e^{-|\alpha-\beta|^2}\,
\mathrm{d}^2\alpha \\
&= \frac{1}{n!}\left(\frac{\partial^2}{\partial\alpha\,\partial\overline{\alpha}}\right)^n
e^{|\alpha|^2} e^{-|\alpha-\beta|^2}\Big|_{\alpha=0} \\
&= \frac{e^{-|\beta|^2}}{n!}\left(\frac{\partial^2}{\partial\alpha\,\partial\overline{\alpha}}\right)^n
e^{\alpha\overline{\beta} + \overline{\alpha}\beta}\Big|_{\alpha=0} \\
&= \frac{e^{-|\beta|^2}}{n!}|\beta|^{2n}.
\end{aligned}
\tag{3.75}
$$

∎

**Tvrzení 11 (Q-funkce centrovaných gaussovských stavů).** Q-funkce $d$-módového centrovaného gaussovského stavu
$\rho$ s komplexní kovarianční maticí $\sigma^{(\mathrm{c})}$ je

$$
Q_\rho(\pmb{\alpha}) = \frac{1}{\pi^d\sqrt{\det\Sigma}}
\exp\left(-\frac{1}{2}\breve{\pmb{\alpha}}^\dagger\Sigma^{-1}\breve{\pmb{\alpha}}\right),
\tag{3.76}
$$

kde

$$
\Sigma := \frac{1}{2}\left(\sigma^{(\mathrm{c})} + \mathbb{1}\right).
\tag{3.77}
$$

*Důkaz.* Vzorec dostaneme z definice $Q_\rho(\pmb{\alpha}) = W_\rho^{(-1)}(\pmb{\alpha})$ výpočtem
gaussovského integrálu z charakteristické funkce (podobně jako ve vztahu (3.56)):

$$
\begin{aligned}
Q_\rho(\pmb{\alpha})
&= \frac{1}{\pi^{2d}}\int_{\mathbb{C}^d} e^{-\breve{\pmb{\alpha}}^\dagger K\breve{\pmb{\beta}}}
e^{-\frac{1}{4}\breve{\pmb{\beta}}^\dagger K\sigma^{(\mathrm{c})}K\breve{\pmb{\beta}}}
e^{-\frac{1}{4}\breve{\pmb{\beta}}^\dagger\breve{\pmb{\beta}}}\,\mathrm{d}^{2d}\pmb{\beta} \\
&= \frac{1}{\pi^d\sqrt{\det\Sigma}} e^{-\frac{1}{2}\breve{\pmb{\alpha}}^\dagger\Sigma^{-1}\breve{\pmb{\alpha}}}.
\end{aligned}
\tag{3.78}
$$

∎
""")

SECTION_3_5 = PrimerSection(anchor="skripta-3-5", number="3.5", title="Cvičení", body=r"""
**Cvičení 3.5.1.** Dokažte vztah (3.4). *Nápověda: Zapište $|\alpha\rangle = \sum_{n=0}^{\infty} c_n|n\rangle$
a pomocí vztahu (3.2) odvoďte vztah pro $c_n$.*

*Řešení.* Nechť

$$
|\alpha\rangle = \sum_{n=0}^{\infty} c_n|n\rangle, \qquad a|n\rangle = \sqrt{n}\,|n-1\rangle.
\tag{3.79}
$$

Z rovnice pro vlastní vektor $a|\alpha\rangle = \alpha|\alpha\rangle$ dostaneme

$$
a|\alpha\rangle = \sum_{n=0}^{\infty} c_n\sqrt{n}\,|n-1\rangle = \sum_{n=0}^{\infty} c_{n+1}\sqrt{n+1}\,|n\rangle,
\tag{3.80}
$$

zatímco

$$
\alpha|\alpha\rangle = \sum_{n=0}^{\infty}\alpha\, c_n|n\rangle.
\tag{3.81}
$$

Porovnáním koeficientů u $|n\rangle$ dostaneme rekurenci

$$
c_{n+1} = \frac{\alpha}{\sqrt{n+1}}c_n \quad\Longrightarrow\quad c_n = \frac{\alpha^n}{\sqrt{n!}}c_0.
\tag{3.82}
$$

Normalizujme $|\alpha\rangle$:

$$
1 = \langle\alpha|\alpha\rangle = \sum_{n=0}^{\infty}|c_n|^2 = |c_0|^2\sum_{n=0}^{\infty}\frac{|\alpha|^{2n}}{n!}
= |c_0|^2 e^{|\alpha|^2} \;\Rightarrow\; |c_0| = e^{-|\alpha|^2/2}.
\tag{3.83}
$$

Zvolíme-li pro $c_0$ obvyklou reálnou kladnou fázi, je $c_0 = e^{-|\alpha|^2/2}$. Tedy

$$
|\alpha\rangle = e^{-|\alpha|^2/2}\sum_{n=0}^{\infty}\frac{\alpha^n}{\sqrt{n!}}|n\rangle.
\tag{3.84}
$$

**Cvičení 3.5.2.** Vykreslete v Piquassu Wignerovu funkci jednomódového vakuového stavu.

*Řešení.* Použijte [https://app.piquasso.com/](https://app.piquasso.com/).

**Cvičení 3.5.3.** Vykreslete v Piquassu Wignerovu funkci jednomódového koherentního stavu.

*Řešení.* Použijte [https://app.piquasso.com/](https://app.piquasso.com/).

**Cvičení 3.5.4.** Spočítejte Q-funkci jednomódového koherentního stavu.

*Řešení.* Pomocí vztahů (3.71) a (3.12) můžeme psát

$$
Q_{|\alpha\rangle\langle\alpha|}(\beta) = \frac{1}{\pi}|\langle\beta|\alpha\rangle|^2
= \frac{1}{\pi}e^{-|\alpha-\beta|^2}.
\tag{3.85}
$$

**Cvičení 3.5.5.** Spočítejte P-funkci jednomódového koherentního stavu.

*Řešení.* Nejprve musíme spočítat charakteristickou funkci stavu $\rho = |\alpha\rangle\langle\alpha|$. Ta je

$$
\chi_{|\alpha\rangle\langle\alpha|}(\beta) = \operatorname{Tr}\left[D(\beta)|\alpha\rangle\langle\alpha|\right]
= \langle\alpha|D(\beta)|\alpha\rangle
\overset{\text{vztah (3.24)}}{=} e^{\overline{\alpha}\beta - \alpha\overline{\beta}} e^{-\frac{|\beta|^2}{2}},
\tag{3.86}
$$

a tedy

$$
\chi_{|\alpha\rangle\langle\alpha|}^{(+1)}(\beta) = \chi_{|\alpha\rangle\langle\alpha|}(\beta)\,e^{\frac{|\beta|^2}{2}}
= e^{\overline{\alpha}\beta - \alpha\overline{\beta}}.
\tag{3.87}
$$

Víme, že

$$
P_{|\alpha\rangle\langle\alpha|}(\gamma)
= \frac{1}{\pi^2}\int_{\mathbb{C}} e^{\gamma\overline{\beta} - \overline{\gamma}\beta}
e^{\overline{\alpha}\beta - \alpha\overline{\beta}}\,\mathrm{d}^2\beta
= \frac{1}{\pi^2}\int_{\mathbb{C}} e^{\overline{(\alpha-\gamma)}\beta - (\alpha-\gamma)\overline{\beta}}\,
\mathrm{d}^2\beta.
\tag{3.88}
$$

Postupem z důkazu tvrzení 7 můžeme psát

$$
\int_{\mathbb{C}} e^{\overline{(\alpha-\gamma)}\beta - (\alpha-\gamma)\overline{\beta}}\,\mathrm{d}^2\beta
= \pi^2\delta^{(2)}(\alpha-\gamma),
\tag{3.89}
$$

a proto

$$
P_{|\alpha\rangle\langle\alpha|}(\gamma) = \delta^{(2)}(\alpha-\gamma).
\tag{3.90}
$$

Poznamenejme, že tento vzorec bylo možné snadno uhodnout i z věty 3.4.2.

**Cvičení 3.5.6.** Spočítejte Q-funkci jednomódového stlačeného stavu (squeezed state).

*Řešení.* Použijeme tvrzení 11 a kovarianční matici ze cvičení 2.7.6. Můžeme psát

$$
\Sigma = \frac{1}{2}\left(\sigma^{(\mathrm{c})} + \mathbb{1}\right)
= \frac{1}{2}\begin{bmatrix} \cosh(2r)+1 & -e^{i\phi}\sinh(2r) \\ -e^{-i\phi}\sinh(2r) & \cosh(2r)+1 \end{bmatrix},
\tag{3.91}
$$

kde $z = re^{i\phi}$. Přímým výpočtem také zjistíme, že

$$
\det\Sigma = \frac{1}{4}\left((\cosh(2r)+1)^2 - \sinh^2(2r)\right) = \cosh^2(r),
\tag{3.92}
$$

a inverzní matice $\Sigma^{-1}$ je

$$
\Sigma^{-1} = \begin{bmatrix} 1 & e^{i\phi}\tanh(r) \\ e^{-i\phi}\tanh(r) & 1 \end{bmatrix}.
\tag{3.93}
$$

*(Pozn. překl.: Řešení v originále zde končí. Dosazením (3.92) a (3.93) do (3.76) vychází Q-funkce stlačeného stavu)*

$$
Q_\rho(\alpha) = \frac{1}{\pi\cosh r}
\exp\left(-|\alpha|^2 - \tanh(r)\operatorname{Re}\left(e^{-i\phi}\alpha^2\right)\right).
$$

*(Kontrola: pro $r = 0$ vychází $e^{-|\alpha|^2}/\pi$, tedy Q-funkce vakua.)*
""")

CHAPTER = PrimerChapter(
    label="Kapitola 3",
    title="Kvantová optika ve fázovém prostoru",
    intro=INTRO,
    sections=(SECTION_3_1, SECTION_3_2, SECTION_3_3, SECTION_3_4, SECTION_3_5),
    original_pages="27–35",
)
