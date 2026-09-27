"""Texts of the GBS caveats; the GBS page shows the summaries, the caveats page everything."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Caveat:
    anchor: str
    title: str
    summary: str
    explanation: str
    remedies: str


CLASSICAL_SIMULATION = Caveat(
    anchor="klasicka-simulace",
    title="GBS je tady simulované klasicky",
    summary=(
        "Všechno na 2. stránce počítá obyčejný procesor. Kvantový počítač by se mohl vyplatit jen tam, "
        "kde takový výpočet nezvládne ani superpočítač – a tahle hranice se neustále posouvá."
    ),
    explanation=r"""
Aplikace nepoužívá žádný kvantový hardware. Pravděpodobnost $p(n)$ každého vzoru fotonů spočítá přímo
ze vzorce s hafniánem a výstřely z ní vylosuje obyčejným generátorem náhodných čísel. Chová se tedy přesně
jako **ideální** GBS – bez ztrát a šumu – ale nic neříká o tom, jestli by skutečné zařízení bylo rychlejší.

Klasická simulace je tu snadná, protože úloha je malá: nejvýše 6 aktiv (6 módů) a vzory s nejvýše
6 fotony. Hafnián matice $2m \times 2m$ je součet přes $(2m-1)!!$ perfektních párování – pro 6 fotonů jen
15 členů, což procesor sečte za mikrosekundy. Tento počet ale roste exponenciálně: nejlepší známé přesné
algoritmy potřebují řádově $n^3\,2^{n/2}$ operací pro matici $n \times n$. Při desítkách detekovaných fotonů
už přesný výpočet nezvládne ani superpočítač – a právě tam experimenty (Jiuzhang, Borealis a jejich
nástupci) hledají kvantovou výhodu.

Hranice ale není pevná. Reálná zařízení ztrácejí velkou část fotonů a klasické algoritmy to umějí využít:
tensor-network metoda Oh et al. (Nature Physics 2024) napodobila tehdy největší experiment s poměrně
skromnými výpočetními prostředky a podle autorů se ideálnímu rozdělení přiblížila lépe než experiment
samotný. Tvrzení o kvantové výhodě se tak opakovaně zpochybňují a pro konkrétní aplikaci – třeba odhad
rizika – je potřeba výhodu prokázat znovu, ne se odvolat na obecné výsledky o boson samplingu.
""",
    remedies=r"""
- Ověřit estimátor na **simulátoru se ztrátami a šumem** (knihovny Strawberry Fields, The Walrus,
  Perceval), ne jen na ideálním modelu jako tady.
- Spustit ho na **skutečném fotonickém procesoru** a porovnat s ideální simulací.
- Srovnávat vždy s **nejlepším klasickým postupem** – nejen s naivním Monte Carlem, ale i s klasickými
  „quantum-inspired“ algoritmy, které simulují právě GBS.
""",
)

CLOSED_FORM = Caveat(
    anchor="uzavreny-vzorec",
    title="Pro tento moment existuje vzorec",
    summary=(
        r"Momenty výnosu gaussovského portfolia jdou spočítat na kalkulačce: "
        r"$\mathbb{E}[L^d] = (d-1)!!\,(w^\top\Sigma w)^{d/2}$. Na 2. stránce slouží jen jako testovací úloha "
        "se známým výsledkem."
    ),
    explanation=r"""
Výnos portfolia $L = w^\top X$ je lineární kombinace gaussovských veličin, takže je sám gaussovský:
$L \sim \mathcal{N}(0, \sigma^2)$ s $\sigma^2 = w^\top \Sigma w$. Pro jednorozměrné normální rozdělení
platí $\mathbb{E}[L^2] = \sigma^2$, $\mathbb{E}[L^4] = 3\sigma^4$ a $\mathbb{E}[L^6] = 15\sigma^6$. Celý
součet hafniánů z kroku 2 – 15 členů pro 3 aktiva a $d = 4$, 462 členů pro 6 aktiv a $d = 6$ – se tedy
„složí“ do jediného čísla.

Právě proto je to dobrá **testovací úloha**: aplikace ví, jaký výsledek má vyjít. Automatické testy
ověřují, že hafniánová cesta i GBS estimátor s přesnými pravděpodobnostmi vracejí totéž co vzorec
(s relativní přesností $10^{-12}$, resp. $10^{-9}$). Kdyby se někde spletlo znaménko, faktoriál nebo
škálování $\gamma$, testy by selhaly.

Skutečný smysl má GBS u funkcí, které se takto „složit“ nedají: u obecných polynomů v mnoha proměnných,
např. $\mathbb{E}[X_1^2 X_2^2 \cdots X_k^2]$, který vede na hafnián matice $2k \times 2k$, nebo u polynomů
z rozvoje složitější výplatní funkce. Pozor ale na častý omyl: **to, že je přesný výpočet exponenciálně
drahý, ještě neznamená výhodu GBS.** Konkurentem není přesný výpočet hafniánů, ale klasické Monte Carlo,
které hafniány vůbec nepočítá – jen průměruje $f(X)$ přes náhodné scénáře. Rozhoduje, čí odhad má při
stejném počtu vzorků menší rozptyl. Andersen a Shan (2025) dokazují, že exponenciální úspora vzorků oproti
Monte Carlu existuje na otevřené neprázdné podmnožině gaussovských úloh – tedy pro některé úlohy,
ne pro všechny.
""",
    remedies=r"""
- Pro výzkum zvolit testovací úlohy **bez uzavřeného vzorce**, které jde v malé dimenzi ještě přesně
  zkontrolovat, a teprve pak škálovat.
- Výhodu měřit **proti Monte Carlu při stejné přesnosti** (graf v kroku 6), ne proti přesnému výpočtu
  hafniánů.
""",
)

SIGN_PROBLEM = Caveat(
    anchor="znamenko",
    title="Znaménkový problém",
    summary=(
        r"Detektor „vidí“ pravděpodobnost úměrnou $\mathrm{Haf}^2$, takže z měření jde vytáhnout jen "
        r"$|\mathrm{Haf}|$ – znaménko se ztratí. Estimátor proto funguje jen pro nezáporné korelace."
    ),
    explanation=r"""
Estimátor z kroku 5 počítá $\mathrm{Haf}(\Sigma_n) \approx \gamma^{-d/2}\sqrt{\hat p(n)\, n!\, \prod_j \cosh r_j}$.
Odmocnina z pravděpodobnosti je vždy nezáporná, takže dostaneme jen **absolutní hodnotu** hafniánu.
Moment $\mathbb{E}[L^d] = \sum_n c_n\, \mathrm{Haf}(\Sigma_n)$ ale potřebuje hafniány i se znaménky –
kladné a záporné členy se v součtu navzájem ruší.

Když jsou všechny prvky $\Sigma$ nezáporné (všechny korelace $\geq 0$), je hafnián součtem součinů
nezáporných čísel, a tedy nezáporný: znaménko známe předem a problém nenastane. Proto aplikace záporné
korelace odmítne.

**Proč na tom ve financích záleží:** záporná korelace je podstata zajištění (hedgingu). Vezměme portfolio
50/50 ze dvou aktiv s volatilitou 20 % a korelací −0,5. Skutečný rozptyl je
$0{,}25 \cdot 0{,}04 + 2 \cdot 0{,}25 \cdot (-0{,}02) + 0{,}25 \cdot 0{,}04 = 0{,}01$, tedy volatilita
**10 %**. Estimátor bez znamének by prostřední člen přičetl místo odečetl: rozptyl $0{,}03$ a volatilita
**17,3 %**. Zajištěné portfolio by vypadalo o 73 % rizikovější, než ve skutečnosti je – a to právě
u portfolií, kde na přesném odhadu rizika záleží nejvíc.
""",
    remedies=r"""
- **Otočit znaménko některých aktiv.** Když se aktivum $i$ nahradí veličinou $-X_i$ (short místo long),
  změní se znaménka jeho korelací a znaménko se přesune do vah $w$, tedy do klasicky známých koeficientů
  $c_n$ – a ty znaménko mít smějí. Funguje to, pokud jde znaménka všech korelací takto „srovnat“ najednou.
  U „frustrovaných“ struktur – třeba tři aktiva, z nichž každé je se dvěma ostatními korelované záporně –
  to nejde.
- **Jiný typ estimátoru**, který hafnián z pravděpodobnosti neodmocňuje. To je otevřené výzkumné téma;
  tato aplikace takový estimátor neimplementuje.
""",
)

DISCARDED_SHOTS = Caveat(
    anchor="zahozene-vystrely",
    title="Většina výstřelů se zahodí",
    summary=(
        r"Informaci pro $\mathbb{E}[L^d]$ nesou jen výstřely s přesně $d$ fotony. Při výchozím nastavení je to "
        "zhruba každý dvanáctý výstřel – zbytek je zaplacený čas zařízení bez užitku."
    ),
    explanation=r"""
Odhad potřebuje četnosti vzorů $n$ se součtem $|n| = d$. Výstřel s jiným celkovým počtem fotonů nese
informaci o úplně jiných hafniánech – pro danou úlohu je k ničemu. Celkový počet fotonů je přitom náhodný
a **neřídí ho interferometr**, protože ten fotony jen přerozděluje mezi módy. Určuje ho jen stlačení:
každý vstupní mód nezávisle vyzáří $0, 2, 4, \dots$ fotonů s pravděpodobností

$$P(2m) = \frac{(2m)!}{(2^m\, m!)^2}\,\frac{\tanh^{2m} r}{\cosh r}.$$

Síla stlačení je proto **kompromis**. Při slabém stlačení je většina výstřelů prázdná (vakuum) a vzory
se 6 fotony jsou vzácné. Při silném stlačení roste střední počet fotonů $\bar n = \sum_j \sinh^2 r_j$ velmi
rychle – pro výchozí portfolio je při $\tanh r_{\max} = 0{,}9$ asi 4,8, při $0{,}99$ už asi 50 –
a pravděpodobnost se rozprostře do vysokých počtů fotonů, takže podíl výstřelů s přesně $d$ fotony zase
klesá. Graf níže ukazuje, že pro výchozí portfolio je užitečných nejvýš asi 23 % výstřelů pro $d = 2$,
13 % pro $d = 4$ a 8 % pro $d = 6$. Andersen a Shan v navazující práci (2025) ukazují, že když se
střední počet fotonů vyladí na konkrétní úlohu, má GBS výhodu na podstatné části prostoru úloh.

**Horší problém přichází s rozměrem.** Tento estimátor potřebuje odhadnout pravděpodobnost každého vzoru
zvlášť. Počet vzorů se součtem $d$ v $k$ módech je $\binom{d+k-1}{k-1}$: pro 3 aktiva a $d = 4$ je to 15,
pro 10 aktiv a $d = 10$ už 92 378 a pro 100 aktiv a $d = 10$ přibližně $4 \cdot 10^{13}$. Tolik vzorů nejde
ani jednou pozorovat, natož spolehlivě odhadnout jejich četnosti. Nepozorované vzory estimátor počítá jako
nulu, takže výsledek je systematicky podhodnocený.
""",
    remedies=r"""
- **Vyladit stlačení** na konkrétní úlohu – vyzkoušej posuvník na 2. stránce; v literatuře se optimalizuje
  střední počet fotonů.
- Uvažovat estimátory, které **průměrují přes jednotlivé výstřely** (typ importance sampling) místo odhadu
  pravděpodobnosti každého vzoru zvlášť. Mívají ale vlastní cenu – často je nutné pro každý pozorovaný vzor
  klasicky spočítat hafnián.
- U velkých úloh počítat s tím, že o celkové ceně rozhodne spíš **podíl užitečných výstřelů** a **počet
  vzorů** než samotná rychlost zařízení.
""",
)

REAL_HARDWARE = Caveat(
    anchor="realny-hardware",
    title="Reálný hardware není ideální",
    summary=(
        "Skutečné zařízení ztrácí fotony, šumí a často pozná jen „foton ano/ne“. Výstupní rozdělení je pak "
        "jiné, než předpokládá vzorec, a estimátor bez úpravy dává zkreslené výsledky."
    ),
    explanation=r"""
**Ztráty fotonů.** Každá optická součástka – zdroj, vlnovod, dělič svazku, spojka s vláknem, detektor –
část světla pohltí nebo rozptýlí. Ztráta se modeluje jako dělič svazku, který část světla odvede
„do prostředí“. Stav tím přestane být čistý (je smíšený) a pravděpodobnosti už nejsou
$\mathrm{Haf}(B_n)^2 / (n! \prod_j \cosh r_j)$, ale hafniány větší matice $A$ rozměru $2k \times 2k$
sestavené z kovarianční matice smíšeného stavu:

$$p(n) = \frac{\mathrm{Haf}(A_n)}{n!\,\sqrt{\det \sigma_Q}}.$$

Estimátor, který s tím nepočítá a pořád jen odmocňuje, je **vychýlený** – a tuto chybu nesníží žádný počet
výstřelů. Ztráty navíc jdou proti kvantové výhodě podruhé: čím víc fotonů se ztratí, tím snáz jde zařízení
klasicky napodobit (viz první háček).

**Prahové detektory.** Detektory rozlišující počet fotonů (PNR) obvykle vyžadují kryogenní chlazení
a jsou pomalejší, proto řada zařízení používá prahové detektory, které poznají jen „žádný foton“ vs.
„aspoň jeden“. Vzory $(2,0,2)$ i $(1,0,1)$ pak vypadají stejně a pravděpodobnosti se místo hafniánem
počítají tzv. torontiánem. Náš estimátor ale potřebuje právě vzory s opakováním, jako je $(4,0,0)$,
které prahový detektor vůbec nerozliší. Řešením je rozdělit každý mód do několika detektorů
(multiplexing) – to ale přidává další módy a další ztráty.

**Šum a kalibrace.** Skutečné stlačení $r_j$ a nastavení interferometru $U$ se od požadovaných liší, fáze
se časem posouvají a fotony z různých zdrojů nejsou dokonale nerozlišitelné. Zařízení tak ve skutečnosti
implementuje jinou matici než $\gamma\Sigma$ a odhad míří na trochu jiný integrál. I tato chyba je
systematická.
""",
    remedies=r"""
- **Zahrnout známé ztráty do modelu** a estimátor odvodit pro smíšený stav (vzorec výše) místo pro čistý.
- Nejdřív ověřit na **simulátoru se ztrátami a šumem**, pak na hardwaru. Úloha s uzavřeným vzorcem
  (druhý háček) je k tomu ideální kalibrační test.
- Počítat s tím, že vyšší ztráty zároveň **usnadňují klasickou simulaci** – výhodu je nutné hledat
  v režimu nízkých ztrát.
""",
)

TAIL_RISK = Caveat(
    anchor="var-cvar",
    title="VaR a CVaR nejsou polynomy",
    summary=(
        "Regulatorně nejdůležitější ukazatele rizika měří pravděpodobnost nebo průměr ztráty v chvostu – "
        "to jsou funkce se skokem, ne polynomy. GBS estimátor je umí jen aproximovat, a to draze."
    ),
    explanation=r"""
GBS estimátor umí $\mathbb{E}[f(X)]$ jen pro polynom $f$, protože jen polynom se rozpadne na konečný součet
hafniánů. Ukazatele rizika jsou ale jiné:

- **Pravděpodobnost ztráty nad prahem** je očekávaná hodnota indikátorové funkce:
  $P(\text{ztráta} > v) = \mathbb{E}[\mathbf{1}\{\text{ztráta} > v\}]$. Funkce $\mathbf{1}\{\cdot\}$
  má skok.
- **VaR** na hladině 99 % je práh $v$, pro který je tato pravděpodobnost 1 % – kvantil, který se hledá
  opakovaným vyhodnocením indikátoru.
- **CVaR (Expected Shortfall)** je průměrná ztráta v tomto chvostu:
  $\mathbb{E}[\text{ztráta} \cdot \mathbf{1}\{\text{ztráta} > \mathrm{VaR}\}] / 0{,}01$.

Indikátor se dá polynomem jen **aproximovat**, pro gaussovská rozdělení přirozeně rozvojem do Hermitových
polynomů. Rozvoj funkce se skokem ale konverguje pomalu a kolem skoku osciluje (Gibbsův jev) – a nás přitom
zajímá právě okolí prahu v chvostu, kde je pravděpodobnostní hmoty málo. Pro přesnost potřebnou v řízení
rizika je nutný vysoký stupeň $D$ a počet vzorů se součtem nejvýše $D$ je $\binom{D+k}{k}$: pro 10 aktiv
a $D = 20$ přes 30 milionů. Každý stupeň navíc potřebuje výstřely s přesně tolika fotony, a těch je čím
dál méně (čtvrtý háček).

Pro úplnost: u čistě lineárního gaussovského portfolia je i VaR vzorec, $\mathrm{VaR}_{99\,\%} = 2{,}33\,\sigma$
(bez střední hodnoty). Zajímavé – a těžké – to je až u **nelineárních portfolií** (opce, deriváty), kde je
ztráta nelineární funkcí $X$. Tam je ale i indikátor $\mathbf{1}\{g(X) > v\}$ složitější.
""",
    remedies=r"""
- Počítat na GBS **momenty** a VaR/CVaR z nich odhadnout momentovou aproximací (např. Cornishova–Fisherova
  expanze ze šikmosti a špičatosti).
- **Hybridní přístup**: hladkou část úlohy přes GBS, chvost klasickým Monte Carlem s importance samplingem.
- Pečlivě změřit, jak **chyba aproximace indikátoru** roste v chvostu – jinak se chyba GBS estimátoru schová
  za chybu polynomu.
""",
)

SAMPLES_NOT_TIME = Caveat(
    anchor="cas",
    title="Srovnání je v počtu vzorků, ne v čase",
    summary=(
        "Graf v kroku 6 porovnává, kolik vzorků potřebují obě metody, ne kolik sekund nebo peněz. Pro praxi "
        "rozhoduje čas (a cena) do dosažení požadované přesnosti."
    ),
    explanation=r"""
Chyba obou metod klesá zhruba jako $1/\sqrt{N}$. Když má GBS estimátor při stejném $N$ chybu $q$-krát
menší, potřebuje k téže přesnosti $q^2$-krát méně vzorků – při 1,6× menší chybě asi 2,6× méně.
**V čase** ale vyhraje jen tehdy, když jeden výstřel GBS není dražší než $q^2$ klasických vzorků:

$$T(\varepsilon) \approx \frac{\sigma^2_{\text{na vzorek}}}{\varepsilon^2}\cdot t_{\text{vzorek}}.$$

A tady je klasické Monte Carlo velmi silné: vygenerovat gaussovský vektor a spočítat $f(X)$ stojí na
procesoru zlomek mikrosekundy a úloha se triviálně paralelizuje na tisíce jader nebo GPU. Na straně GBS se
naopak sčítá rychlost opakování výstřelů, kalibrace a přeprogramování interferometru pro každou novou matici
$\Sigma$, fronta a přenos dat u cloudových zařízení a klasické dopočty (četnosti, odmocniny, u jiných
estimátorů hafniány pozorovaných vzorů).

Teoretické výsledky o exponenciální výhodě (Andersen a Shan 2025) jsou formulované právě v počtu vzorků –
jako garantovaná velikost vzorku pro danou přesnost $\varepsilon$ a pravděpodobnost úspěchu $\delta$ –
a týkají se škálování s velikostí úlohy, ne konstant. Pro praktické nasazení rozhoduje obojí: jak rychle
roste počet vzorků **a** kolik stojí jeden vzorek.
""",
    remedies=r"""
- Porovnávat **čas a cenu do cílové přesnosti** (time-to-solution), ne jen počet vzorků.
- Do srovnání započítat **celou pipeline**: kalibraci, přenos dat, frontu i klasický dopočet.
- Pro férovost použít **nejlepší klasickou implementaci** Monte Carla (vektorizace, GPU, variance
  reduction), ne naivní smyčku.
""",
)

CAVEATS: Tuple[Caveat, ...] = (
    CLASSICAL_SIMULATION,
    CLOSED_FORM,
    SIGN_PROBLEM,
    DISCARDED_SHOTS,
    REAL_HARDWARE,
    TAIL_RISK,
    SAMPLES_NOT_TIME,
)

REFERENCES_MARKDOWN = """
- Hamilton et al.: *Gaussian Boson Sampling*, Phys. Rev. Lett. 119, 170501 (2017).
- Arrazola, Rebentrost, Weedbrook: *Quantum supremacy and high-dimensional integration*, arXiv (2017).
- Andersen, Shan: *Using Gaussian Boson Samplers to Approximate Gaussian Expectation Problems*,
  [arXiv:2502.19336](https://arxiv.org/abs/2502.19336) (2025).
- Andersen, Shan: *Estimating the Percentage of GBS Advantage in Gaussian Expectation Problems*,
  [arXiv:2502.19362](https://arxiv.org/abs/2502.19362) (2025).
- Oh, Liu, Alexeev, Fefferman, Jiang: *Classical algorithm for simulating experimental Gaussian boson
  sampling*, [Nature Physics 20, 1461](https://www.nature.com/articles/s41567-024-02535-8) (2024).
- Qi, Brod, Quesada, García-Patrón: *Regimes of classical simulability for noisy Gaussian boson sampling*,
  Phys. Rev. Lett. 124, 100502 (2020).
- Quesada, Arrazola, Killoran: *Gaussian boson sampling using threshold detectors*, Phys. Rev. A 98,
  062322 (2018).
- Björklund, Gupt, Quesada: *A faster hafnian formula for complex matrices and its benchmarking on
  a supercomputer*, ACM Journal of Experimental Algorithmics (2019).
"""
