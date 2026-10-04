"""Guide for a beginning PhD student, part 1: the concepts behind the GBS advantage, explained from scratch."""

from __future__ import annotations

from typing import Tuple

from ui.caveats_content import CLOSED_FORM, SIGN_PROBLEM
from ui.theory_content import (
    AARONSON_ARKHIPOV,
    ANDEL_STATISTICS,
    ANDERSEN_SHAN_ADVANTAGE,
    ANDERSEN_SHAN_EXPECTATIONS,
    DRIMAL_MONTE_CARLO,
    DVORAKOVA_MONTE_CARLO,
    GERRY_KNIGHT,
    GLASSERMAN,
    HAMILTON,
    ISSERLIS,
    KRUSE,
    MADSEN,
    SALEH_TEICH,
    VALIANT,
    WICK,
    WIKIPEDIA_COVARIANCE,
    WIKIPEDIA_HAFNIAN,
    ZHONG,
    Reading,
    Source,
    TheoryTopic,
)

STEIN = Source(
    "Stein, C. M.: *Estimation of the mean of a multivariate normal distribution*. The Annals of Statistics 9 "
    "(1981), 1135–1151 – odtud Steinovo lemma, na kterém stojí rekurze pro momenty"
)

BIG_PICTURE = TheoryTopic(
    anchor="pruvodce-velky-obraz",
    title="Velký obraz: o co tu vůbec jde",
    in_short=(
        "Banky počítají střední hodnoty – ceny, rizika – metodou Monte Carlo. U některých úloh, hlavně u polynomů "
        "vysokého stupně, potřebuje Monte Carlo astronomicky mnoho scénářů. Fotonický přístroj GBS má "
        "pravděpodobnosti výsledků rovné druhým mocninám hafniánů, a hafniány jsou přesně gaussovské momenty. "
        "Umí proto tyto střední hodnoty „měřit“ a u vhodných úloh mu stačí mnohem méně vzorků."
    ),
    explanation=r"""
**Celý příběh v pěti krocích.**

1. Ve financích je spousta důležitých čísel *střední hodnotou*: cena opce je střední hodnota její diskontované
   výplaty, riziko portfolia popisují momenty rozdělení výnosu, očekávaný zisk obchodní strategie je střední
   hodnota zisku přes všechny možné budoucnosti.
2. Když jsou výnosy (aspoň přibližně) normálně rozdělené a počítaná funkce je polynom, jde o *gaussovskou úlohu*.
   Pro ni existuje přesný vzorec – Wickova věta: výsledek je součet *hafniánů* kovarianční matice.
3. Hafnián velké matice je ale extrémně těžké spočítat, takže se v praxi sahá po Monte Carlu: vylosuje se
   mnoho náhodných scénářů a výsledky se zprůměrují. U polynomů vysokého stupně je to drahé, protože o výsledku
   rozhodují vzácné extrémní scénáře, které se losují jen zřídka.
4. *Gaussian Boson Sampler* (GBS) je fotonický přístroj: světlo z několika zdrojů projde sítí polopropustných
   zrcadel a na konci se počítají fotony. Pravděpodobnost, že detektory ukážou určitý vzor počtů fotonů, je
   druhá mocnina hafniánu matice, kterou do přístroje „nahrajeme“. Přístroj tedy hafnián nespočítá, ale umí
   losovat vzory přesně s pravděpodobností úměrnou jeho druhé mocnině.
5. Z toho, jak často vzor padá, jde zpátky dopočítat hafnián, a tím i hledanou střední hodnotu. Andersen a Shan
   (2025) dokázali, že u vhodných úloh – polynomů velmi vysokého stupně – takový odhad potřebuje
   *exponenciálně* méně vzorků než obyčejné Monte Carlo. O tento výsledek se opírá firma Qpurpose.

**Co je dokázané a co ne.** Dokázané je tvrzení o *počtu vzorků* ideálního přístroje proti *obyčejnému* Monte
Carlu. Nedokázané (a nepublikované) je, že to přináší užitek na skutečných bankovních úlohách, na skutečném
hardwaru a proti nejlepším klasickým metodám. Rozlišovat tyto dvě roviny je asi nejdůležitější dovednost
při čtení podobných tvrzení.

**Co najdeš v aplikaci.** Na 2. stránce GBS odhaduje moment výnosu portfolia (polynom nízkého stupně). Na
3. stránce je laboratoř: zadáš kovarianční matici a monom, aplikace spočítá přesnou hodnotu, rozptyl obou
metod a obě metody nasimuluje; k tomu pět připravených úloh a skript pro Qiskit. Tento průvodce vysvětluje
všechno od nuly.

**Co budeš potřebovat.** Základy pravděpodobnosti (střední hodnota, rozptyl, normální rozdělení), lineární
algebry (matice, vlastní čísla a vektory) a trochu kombinatoriky. Kvantovou fyziku ne: co je potřeba,
vysvětlíme obrazně a s odkazy, kde se to dá dostudovat.

**Jak číst.** Každá kapitola začíná rámečkem *V kostce*; kdo spěchá, přečte jen rámečky. Vzorce jsou doplněk,
ne podmínka porozumění. Na konci kapitol jsou zdroje.

**Slovníček.**

- *Scénář* – jedna náhodně vylosovaná možnost, jak dopadne budoucnost (u nás jeden vektor výnosů).
- *Monom* – součin mocnin proměnných, třeba $x_1^8 x_2^8$; *stupeň* je součet exponentů (tady 16).
- *Kovarianční matice* $\Sigma$ – na diagonále rozptyly proměnných, mimo ni jejich společné kolísání.
- *Hafnián* – součet přes všechna rozdělení řádků matice do dvojic; gaussovské momenty jsou hafniány.
- *Mód* – jeden světelný kanál přístroje; *foton* – nejmenší „porce“ světla, kterou detektor započítá.
- *Stlačené světlo* – světlo, jehož fotony vznikají po dvojicích; míru udává *parametr stlačení* $r$.
- *Výstřel* – jeden běh přístroje; jeho výsledek je *vzor* $n = (n_1, \dots, n_k)$, počty fotonů v detektorech.
- *GBS-P, GBS-I* – dva způsoby, jak z výstřelů odhadnout střední hodnotu (kapitola 6).
- *Relativní rozptyl jednoho vzorku* – rozptyl jednoho scénáře či výstřelu vydělený druhou mocninou výsledku;
  rozhoduje, kolik vzorků je potřeba.
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "hlavní článek, ze kterého celá stránka vychází"),
        Reading(HAMILTON, "článek, který GBS zavedl"),
        Reading(DVORAKOVA_MONTE_CARLO, "přístupný český úvod do Monte Carla"),
    ),
)

GAUSSIAN_PROBLEM = TheoryTopic(
    anchor="pruvodce-gaussovska-uloha",
    title="Gaussovská úloha: střední hodnota polynomu",
    in_short=(
        r"Hledáme střední hodnotu polynomu v normálně rozdělených proměnných. Stavebním kamenem je monom "
        r"$\mathbb{E}[x_1^{n_1} \cdots x_k^{n_k}]$; podle Wickovy věty se rovná hafniánu kovarianční matice "
        "s opakovanými řádky a sloupci. Pro málo proměnných ho aplikace spočítá přesně rekurzí ze Steinova lemmatu."
    ),
    explanation=r"""
**Normální rozdělení více proměnných.** Vektor $x = (x_1, \dots, x_k)$ má rozdělení $\mathcal{N}(0, \Sigma)$:
každá složka kolísá kolem nuly, $\Sigma_{ii}$ je rozptyl složky $i$ a $\Sigma_{ij} = \rho_{ij}\sigma_i\sigma_j$
říká, jak moc kolísají složky $i$ a $j$ spolu. Ve financích jsou $x_i$ typicky odchylky výnosů od očekávání.
V úloze 4 jsou to roční výnosy amerických akcií, dluhopisů a zlata s volatilitami 19,6 %, 8,0 % a 20,8 %.

**Monom, stupeň a polynom.** Monom je

$$
x^n = x_1^{n_1}\, x_2^{n_2} \cdots x_k^{n_k},
$$

jeho stupeň $|n| = n_1 + \dots + n_k$. Třeba $x_1^8 x_2^8$ má stupeň 16. Polynom je součet monomů
s koeficienty, $f(x) = \sum_n a_n x^n$. Střední hodnota je lineární, takže stačí umět monomy:
$\mathbb{E}[f(x)] = \sum_n a_n \mathbb{E}[x^n]$.

**Proč zrovna polynomy.** Hladké funkce jde polynomy aproximovat (Taylorův rozvoj). Momenty výnosu portfolia
($\mathbb{E}[L^d]$ na 2. stránce) jsou polynomy, společné momenty několika aktiv měří „společné chvosty“ – jak
často jsou aktiva zároveň daleko od průměru. Článek Andersena a Shan pracuje přesně s úlohou
$\mathbb{E}[f(x)]$ pro polynom $f$ stupně nejvýš $K$.

**Liché stupně dávají nulu.** Normální rozdělení se střední hodnotou nula je symetrické: $x$ a $-x$ jsou stejně
pravděpodobné. Monom lichého stupně změní se znaménkem $x$ znaménko, takže se kladné a záporné příspěvky
vyruší. Proto laboratoř chce sudý stupeň.

**Wickova (Isserlisova) věta.** Pro čtyři proměnné platí

$$
\mathbb{E}[x_1x_2x_3x_4] = \Sigma_{12}\Sigma_{34} + \Sigma_{13}\Sigma_{24} + \Sigma_{14}\Sigma_{23} .
$$

Návod: činitele rozdělíme do dvojic všemi možnými způsoby, každou dvojici nahradíme kovariancí a součiny
sečteme. Opakované proměnné se počítají jako různé činitele: $\mathbb{E}[x_1^2] = \Sigma_{11}$,
$\mathbb{E}[x_1^4] = 3\Sigma_{11}^2$ (tři rozdělení čtyř činitelů do dvojic). Rozdělení $2k$ činitelů do dvojic
je $(2k-1)!! = 1\cdot 3\cdot 5 \cdots (2k-1)$, pro dvacet činitelů 654 729 075 – a protože pro jednu
normovanou proměnnou je každá dvojice rovna 1, vychází $\mathbb{E}[X^{20}] = 19!! = 654\,729\,075$ (úloha 1).

**Hafnián.** Součet přes všechna rozdělení indexů do dvojic se jmenuje hafnián:

$$
\mathrm{Haf}(A) = \sum_{\text{rozdělení do dvojic}}\ \prod_{(i,j)} A_{ij}, \qquad
\mathbb{E}[x^n] = \mathrm{Haf}(\Sigma_n),
$$

kde $\Sigma_n$ vznikne z $\Sigma$ zopakováním $i$-tého řádku a sloupce $n_i$-krát. Hafnián je příbuzný
determinantu a permanentu; pro obecné matice je jeho výpočet stejně těžký jako výpočet permanentu, tedy
#P-těžký (Valiant 1979). Pro velké matice ho nikdo neumí spočítat rychle.

**Jak to aplikace přesto počítá rychle.** *Steinovo lemma* říká, že pro $x \sim \mathcal{N}(0, \Sigma)$ je
$\mathbb{E}[x_a\, g(x)] = \sum_b \Sigma_{ab}\, \mathbb{E}[\partial_b g(x)]$. Pro $g(x) = x^{n - e_a}$ (jeden
činitel $x_a$ ubereme) z něj plyne rekurze, která snižuje stupeň o dva:

$$
\mathbb{E}[x^n] = \sum_b \Sigma_{ab}\,(n - e_a)_b\, \mathbb{E}\big[x^{n - e_a - e_b}\big].
$$

Různých mezivýsledků je jen $\prod_i (n_i + 1)$, takže pro málo proměnných je výpočet rychlý i pro stupeň 40.
Těžkost hafniánu se projeví u mnoha proměnných s malými exponenty: padesát proměnných s exponentem 1 by
znamenalo $2^{50}$ mezivýsledků. Úlohy na 3. stránce jsou proto klasicky snadné – záměrně, abychom mohli chybu
obou metod porovnat s přesnou hodnotou.
""",
    further_reading=(
        Reading(ISSERLIS),
        Reading(WICK),
        Reading(WIKIPEDIA_HAFNIAN, "věta a definice hafniánu s příklady"),
        Reading(STEIN),
        Reading(VALIANT, "proč jsou permanent a hafnián výpočetně těžké"),
        Reading(ANDEL_STATISTICS, "vícerozměrné normální rozdělení"),
        Reading(WIKIPEDIA_COVARIANCE),
    ),
    related_caveats=(CLOSED_FORM,),
)

MONTE_CARLO_VARIANCE = TheoryTopic(
    anchor="pruvodce-monte-carlo",
    title="Monte Carlo a rozptyl jednoho vzorku: proč vysoké stupně bolí",
    in_short=(
        r"Monte Carlo zprůměruje $N$ náhodných scénářů a jeho relativní chyba je $\sqrt{v/N}$, kde $v$ je "
        r"relativní rozptyl jednoho scénáře. Pro přesnost $\varepsilon$ potřebuje $N \approx v/\varepsilon^2$ "
        r"scénářů. U monomů vysokého stupně roste $v$ exponenciálně: pro $\mathbb{E}[X^{20}]$ je asi 746 000, "
        "takže na chybu 1 % je potřeba zhruba 7,5 miliardy scénářů."
    ),
    explanation=r"""
**Odhad.** Vylosujeme $N$ nezávislých scénářů $x^{(1)}, \dots, x^{(N)}$ a zprůměrujeme:

$$
\hat\mu_N = \frac{1}{N}\sum_{i=1}^{N} f\big(x^{(i)}\big).
$$

Odhad se v průměru nemýlí a jeho směrodatná odchylka je $\sigma_f/\sqrt{N}$, kde $\sigma_f^2$ je rozptyl
jednoho scénáře. Relativní chyba (vzhledem k výsledku $\mu$) je tedy $\sqrt{v/N}$ s

$$
v = \frac{\sigma_f^2}{\mu^2} = \frac{\mathbb{E}[f^2]}{\mu^2} - 1 .
$$

**Kolik scénářů.** Pro relativní chybu $\varepsilon$ je potřeba $N \approx v/\varepsilon^2$. Chyba 1 % znamená
$N \approx 10\,000\cdot v$. Číslo $v$ je tak „cena“ metody: kdo ho zmenší, ušetří scénáře. Přesně tohle
číslo porovnává laboratoř pro Monte Carlo a pro GBS.

**Pro monom.** Pro $f = x^n$ je $f^2 = x^{2n}$, takže

$$
v_{\mathrm{MC}} = \frac{\mathbb{E}[x^{2n}]}{\mathbb{E}[x^n]^2} - 1 ,
$$

a aplikace ho spočítá toutéž rekurzí jako moment.

**Příklad $\mathbb{E}[X^{20}]$.** $\mathbb{E}[X^{20}] = 19!! \approx 6{,}5\cdot 10^8$ a
$\mathbb{E}[X^{40}] = 39!! \approx 3{,}2\cdot 10^{23}$, takže $v \approx 746\,000$. Na chybu 1 % je potřeba
$7{,}5\cdot 10^9$ scénářů.

**Proč tolik: těžký chvost.** Většina scénářů má $|X| < 2$ a dává $X^{20} < 2^{20} \approx 10^6$, jenže
průměr je $6{,}5\cdot 10^8$. Výsledek dělají vzácné scénáře kolem $|X| \approx \sqrt{20} \approx 4{,}5$: takový
scénář dá $4{,}5^{20} \approx 10^{13}$, ale přijde jen zhruba jednou za 150 000 losování. Kdo ho nevylosuje,
výsledek podhodnotí; kdo ho vylosuje, nadhodnotí. To je ten velký rozptyl. Stejně funguje průměrný příjem:
jeden miliardář ve vzorku rozhodí průměr víc než tisíc obyčejných lidí.

**Jak rychle to roste.** Pro jednu proměnnou a stupeň $2k$ je $v \approx 4^k/\sqrt{2}$: stupeň 2 dá 2,
stupeň 4 dá 10,7, stupeň 10 dá 732, stupeň 20 dá 746 000 a stupeň 40 dá $7{,}8\cdot 10^{11}$. Každé dva stupně
navíc zhruba zčtyřnásobí potřebný počet scénářů – rozptyl roste exponenciálně se stupněm.

**Naměřená chyba klame.** Když se Monte Carlo zopakuje jen 20×, vzácné obří scénáře se většinou neobjeví.
Odhady pak vycházejí spíš pod přesnou hodnotou a naměřená chyba se zdá menší, než říká teorie – dokud jeden
takový scénář nepřijde. Proto laboratoř kreslí i teoretickou čáru $\sqrt{v/N}$.

**Monte Carlo nemusí být obyčejné.** *Metody snižování rozptylu* rozptyl zmenšují. *Vážený výběr* (importance
sampling) losuje častěji tam, kde je integrand velký, a každý scénář převáží. Pro $\mathbb{E}[X^{20}]$ stačí
losovat ze širší normální křivky s rozptylem 21: relativní rozptyl klesne ze 746 000 na asi 2,8. To je férové
měřítko pro GBS – a uvidíme, že GBS se chová právě jako vážený výběr, jen rozdělení mu dodá fyzika.
""",
    further_reading=(
        Reading(DRIMAL_MONTE_CARLO, "kap. 1.4 odhad chyby, kap. 5.7 metoda váženého výběru"),
        Reading(DVORAKOVA_MONTE_CARLO),
        Reading(GLASSERMAN, "kap. 4 snižování rozptylu ve finančních úlohách"),
    ),
)

GBS_DEVICE = TheoryTopic(
    anchor="pruvodce-gbs",
    title="Gaussian Boson Sampler polopatě",
    in_short=(
        "Přístroj s několika světelnými kanály (módy): na vstupu stlačené světlo, jehož fotony vznikají po "
        "dvojicích, uprostřed síť polopropustných zrcadel (interferometr), na výstupu detektory, které počítají "
        r"fotony. Jeden běh je výstřel a jeho výsledek vzor $n$. Vzor padá s pravděpodobností "
        r"$p(n) = \mathrm{Haf}(B_n)^2 / (n!\,\prod_j \cosh r_j)$, kde $B$ je matice, kterou přístroj nese."
    ),
    explanation=r"""
**Módy a fotony.** Mód je jeden světelný kanál – optické vlákno nebo vlnovod na čipu. Stav módu nás zajímá jen
přes to, kolik fotonů v něm detektor napočítá: 0, 1, 2, …

**Stlačené světlo.** Zdroj (nelineární krystal čerpaný laserem) vyrábí světlo, ve kterém fotony vznikají po
dvojicích. Síla zdroje je *parametr stlačení* $r$. Pravděpodobnost $2k$ fotonů je

$$
P(2k) = \frac{(2k)!}{4^k (k!)^2}\,\frac{\tanh^{2k} r}{\cosh r},
$$

liché počty nepadají nikdy a průměr je $\sinh^2 r$; pro $r = 1$ asi 1,4 fotonu. Silnější stlačení znamená víc
fotonů.

**Interferometr.** Síť děličů svazku (polopropustných zrcadel) a fázových posuvů mísí módy podle matice $O$
(obecně unitární, u nás reálné ortogonální). Fotony nevyrábí ani neničí, jen je přerozděluje mezi výstupy –
jeden dělič svazku mezi dvěma módy je „rotace“ o úhel, který určuje, jak velká část světla přejde do druhého
módu. Libovolnou matici $O$ jde složit z děličů mezi dvojicemi módů (Reck 1994, Clements 2016).

**Detektory.** Na výstupu každého módu detektor spočítá fotony. Výsledek jednoho výstřelu je vzor
$n = (n_1, \dots, n_k)$, třeba $(2, 0, 1, 1)$. Proto se přístroji říká vzorkovač: neodpovídá jedním číslem, ale
náhodným vzorem.

**Matice, kterou přístroj nese.** Stlačení a interferometr dohromady popisuje jedna symetrická matice

$$
B = O\,\mathrm{diag}(\tanh r_1, \dots, \tanh r_k)\,O^\top .
$$

A naopak: libovolnou symetrickou matici s vlastními čísly mezi 0 a 1 jde do přístroje nahrát – vlastní čísla
určí stlačení ($\tanh r_j = \lambda_j$) a vlastní vektory interferometr.

**Hlavní vzorec.** Hamilton a kol. (2017) ukázali, že

$$
p(n) = \frac{\mathrm{Haf}(B_n)^2}{n!\,\prod_j \cosh r_j}, \qquad n! = n_1!\cdots n_k! .
$$

Intuice: fotony vznikají v párech a do detektorů se mohou „rozvést“ všemi možnými cestami. Každé rozdělení
naměřených fotonů do párů je jeden člen hafniánu. V kvantové mechanice se sčítají amplitudy, ne
pravděpodobnosti, a pravděpodobnost je druhá mocnina součtu – proto hafnián na druhou.

**Proč je to (zřejmě) klasicky těžké.** Pro velké matice bez zvláštní struktury nikdo nezná rychlý klasický
algoritmus, který by losoval vzory se stejnými pravděpodobnostmi. Na tom stojí experimenty s „kvantovou
výhodou“ – Jiuzhang (Zhong a kol. 2020) a Borealis (Madsen a kol. 2022). Pro malé úlohy jako na této stránce
ale rozdělení spočítáme na notebooku.

**Reálné přístroje ztrácejí fotony.** Část světla se cestou pohltí nebo ji detektor nezachytí. Se ztrátami se
pravděpodobnosti mění a výstup často jde napodobit klasicky (viz kapitola o háčcích). Celá teorie na této
stránce počítá s ideálním bezeztrátovým přístrojem.
""",
    further_reading=(
        Reading(HAMILTON, "vzorec pro p(n)"),
        Reading(KRUSE, "podrobné odvození"),
        Reading(SALEH_TEICH, "česky: světlo, fotony, děliče svazku"),
        Reading(GERRY_KNIGHT, "stlačené světlo"),
        Reading(AARONSON_ARKHIPOV, "proč je boson sampling klasicky těžký"),
        Reading(ZHONG),
        Reading(MADSEN),
    ),
)

TUNING = TheoryTopic(
    anchor="pruvodce-ladeni",
    title="Nahrání matice a ladění stlačení",
    in_short=(
        r"Do přístroje se nahrává zmenšená matice $B = D\Sigma D$. Diagonála $D$ určuje, kolik fotonů v průměru "
        "dopadne do kterého detektoru. Nejlepší je nastavit ji tak, aby průměrný počet fotonů v každém módu "
        "odpovídal exponentu – pak cílový vzor padá nejčastěji. Andersen a Shan ladí jen celkový počet fotonů, "
        "což u proměnných s různou volatilitou může úplně selhat."
    ),
    explanation=r"""
**Proč zmenšovat a proč smíme.** Vlastní čísla $B$ musí být menší než 1 ($\tanh r < 1$). Navíc úlohu jde
přeškálovat, aniž by se změnila: když $y = Dx$ pro kladnou diagonální $D$, je $y \sim \mathcal{N}(0, D\Sigma D)$
a $x^n = y^n / \prod_i d_i^{n_i}$. Stačí tedy odhadnout moment pro $B = D\Sigma D$ a vydělit ho součinem
$\prod_i d_i^{n_i}$. Volba $D$ je nastavení přístroje, výsledek nemění – mění jen to, jak často padá cílový vzor.

**Co $D$ ovlivní.** Průměrný počet fotonů v detektoru $i$ je

$$
\langle n_i\rangle = \big[O\,\mathrm{diag}(\sinh^2 r_j)\,O^\top\big]_{ii},
$$

tedy fotony ze stlačovače $j$ rozdělené interferometrem. Větší $d_i$ pošle do módu $i$ víc fotonů.

**Kdy padá cílový vzor nejčastěji.** Logaritmus pravděpodobnosti cílového vzoru je

$$
\log p(n) = 2\sum_i n_i \log d_i + \tfrac12 \sum_j \log\!\big(1 - \tanh^2 r_j\big) + \text{konst.}
$$

Derivace podle $\log d_i$ vyjde $2\,(n_i - \langle n_i\rangle)$. Maximum je tam, kde
$\langle n_i\rangle = n_i$ pro každý mód: **přístroj má v průměru posílat do každého detektoru přesně tolik
fotonů, kolik jich tam chceme naměřit.** Je to jako ladit rádio na stanici: když je naladěné vedle, slyšíme
hlavně šum.

**Varianta z článku.** Andersen a Shan volí $B = t\,\Sigma$ s jediným číslem $t$ tak, aby se průměrný
*celkový* počet fotonů rovnal stupni polynomu; pro tuto volbu ukazují, že minimalizuje chybu GBS-P. Pro jednu
proměnnou nebo souměrné úlohy dávají obě varianty totéž (úlohy 1 a 2).

**Kdy se liší: historická data.** V úloze 4 mají dluhopisy volatilitu 8 %, akcie a zlato kolem 20 %. Při
$B = t\,\Sigma$ dopadne do detektoru dluhopisů průměrně jen 0,02 fotonu (do akcií 4,4 a do zlata 13,5),
takže vzor $(6, 6, 6)$ padá jednou za zhruba 120 milionů výstřelů a GBS prohraje s Monte Carlem asi 250×.
Naladěním po módech dostane každý detektor průměrně 6 fotonů, vzor padne jednou za asi 2 900 výstřelů a GBS
vyhraje zhruba 170×. Stejná matice, stejná úloha – jen jinak nastavený přístroj.

**Jak to aplikace počítá.** Newtonovou metodou s kontrolou délky kroku (asi deset iterací, milisekundy).
Začíná u matice převedené na jednotkové rozptyly a naladěné jako v článku, takže nikdy neskončí hůř.
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_ADVANTAGE, "ladění středního počtu fotonů a podíl výhodných úloh"),
        Reading(ANDERSEN_SHAN_EXPECTATIONS),
    ),
)

GBS_P_ESTIMATOR = TheoryTopic(
    anchor="pruvodce-gbs-p",
    title="Odhad GBS-P: od četnosti zpět k momentu",
    in_short=(
        r"Pustíme $N$ výstřelů a spočítáme, kolikrát padl přesně cílový vzor $n$. Z relativní četnosti "
        r"$\hat p \approx p(n)$ dopočítáme hafnián a z něj moment. Relativní rozptyl jednoho výstřelu je "
        r"$(1 - p)/(4p)$: tím menší, čím častěji vzor padá."
    ),
    explanation=r"""
**Postup krok za krokem.**

1. Nastav přístroj: $B = D\Sigma D = O\,\mathrm{diag}(\tanh r)\,O^\top$.
2. Pusť $N$ výstřelů.
3. Spočítej, kolikrát padl přesně vzor $n$; to je $c$.
4. Relativní četnost $\hat p = c/N$ odhaduje $p(n)$.
5. Obrať hlavní vzorec: $\mathrm{Haf}(B_n) = \sqrt{\hat p\; n!\; \prod_j \cosh r_j}$.
6. Vrať měřítko: $\mathbb{E}[x^n] = \mathrm{Haf}(B_n) / \prod_i d_i^{n_i}$.

**Znaménko.** Přístroj měří jen $\mathrm{Haf}^2$, takže znaménko musíme znát předem. U sudých exponentů je
moment průměrem druhé mocniny, tedy kladný. U lichých kladnost zaručí nezáporné prvky matice. Jinak nastává
*znaménkový problém* a laboratoř takovou úlohu odmítne.

**Jak velká je chyba.** Počet zásahů $c$ má binomické rozdělení, takže $\hat p$ má relativní rozptyl
$(1-p)/(pN)$. Odmocnina chybu způlí (delta metoda: relativní chyba odmocniny je polovina relativní chyby
argumentu), a proto

$$
v_{\mathrm{GBS}} = \frac{1 - p}{4p}, \qquad \text{relativní chyba} \approx \sqrt{v_{\mathrm{GBS}}/N}.
$$

**Příklad.** Pro $\mathbb{E}[X^{20}]$ padá vzor „20 fotonů“ s pravděpodobností $p \approx 0{,}0236$, tedy
zhruba v každém 42. výstřelu, a $v_{\mathrm{GBS}} \approx 10{,}3$. Na chybu 1 % stačí asi 103 000 výstřelů,
proti 7,5 miliardy scénářů Monte Carla.

**Drobnosti.** Odmocnina z nestranného odhadu není nestranná, vychýlení ale klesá jako $1/N$ a pro rozumné $N$
je zanedbatelné. Když vzor nepadne ani jednou, odhad je nula.

**Druhý odhad z článku: GBS-I.** Losuje vzory a průměruje přeškálované koeficienty polynomu,
$\frac1N\sum a_{n^{(i)}}\, n^{(i)}!/d$ s $d = \prod_j \sqrt{1 - \lambda_j^2}$. Je nestranný, ale odhaduje
$\sum_n a_n \mathrm{Haf}(B_n)^2$, tedy „zdvojenou“ úlohu pro gaussovský vektor s kovariancí $B \oplus B$, ne
původní střední hodnotu. Pro tuto upravenou úlohu dokazuje článek nejsilnější exponenciální výhodu.
Laboratoř počítá jen GBS-P.

**Polynom místo monomu.** Pro $f = \sum a_n x^n$ sečte GBS-P odhady pro všechny vzory; 2. stránka to dělá pro
moment portfolia $(w^\top x)^d$. Rozptyl se pak skládá z podílů jednotlivých vzorů, viz Srovnání na stránce
Teorie.
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "definice GBS-I a GBS-P, jejich rozptyly"),
        Reading(ANDEL_STATISTICS, "binomické rozdělení a delta metoda"),
    ),
    related_caveats=(SIGN_PROBLEM,),
)

WHY_EXPONENTIAL = TheoryTopic(
    anchor="pruvodce-proc-exponencialne",
    title="Proč je výhoda exponenciální – a kdy není",
    in_short=(
        r"U jedné proměnné roste rozptyl Monte Carla se stupněm $2k$ jako $4^k$, rozptyl GBS-P jen lineárně, "
        r"zhruba jako $k$. Rozdíl je exponenciální. S počtem proměnných ale výhoda slábne, protože cílový vzor je "
        "jen jeden z mnoha se stejným počtem fotonů. Proto věta Andersena a Shan chce stupeň aspoň úměrný druhé "
        "mocnině počtu proměnných."
    ),
    explanation=r"""
**Jedna proměnná.** Monte Carlo má $v_{\mathrm{MC}} \approx 4^k/\sqrt{2}$ (Stirlingův vzorec). U GBS s optimálním
stlačením (průměrně $2k$ fotonů) padá vzor „$2k$ fotonů“ s pravděpodobností
$p \approx e^{-1/2}/(\sqrt{2\pi}\,k) \approx 0{,}24/k$, takže $v_{\mathrm{GBS}} \approx 1{,}03\,k$:

| stupeň | $v_{\mathrm{MC}}$ | $v_{\mathrm{GBS}}$ | GBS potřebuje méně vzorků |
|---|---|---|---|
| 10 | 732 | 5,2 | 141× |
| 20 | 746 000 | 10,3 | 72 000× |
| 40 | $7{,}8\cdot 10^{11}$ | 20,7 | $3{,}8\cdot 10^{10}$× |

**Intuice.** Monte Carlo losuje scénáře podle normálního rozdělení, tedy hlavně obyčejné malé hodnoty, kdežto
výsledek dělají vzácné obří. GBS losuje vzory s pravděpodobností úměrnou čtverci jejich příspěvku, takže
„míří“ přímo tam, kde výsledek vzniká. Je to vážený výběr, ve kterém rozdělení nevolíme my, ale fyzika.

**Více proměnných.** Fotony se rozdělí mezi $k$ detektorů. Vzorů se stejným celkovým počtem fotonů $d$ je
$\binom{d + k - 1}{k - 1}$: pro $d = 16$ a dvě proměnné 17, pro $d = 18$ a tři proměnné 190, pro $d = 16$ a čtyři
proměnné 969. I při nejlepším ladění padá konkrétní vzor zhruba s pravděpodobností jedna ku počtu vzorů, takže
$v_{\mathrm{GBS}}$ s počtem proměnných roste. Proto úloha 2 (dvě proměnné, stupeň 16) dá výhodu asi 880×, ale
úloha 5 (čtyři proměnné, stupeň 16) jen asi 60×.

**Kdy GBS prohraje.** U nízkého stupně (u úlohy 5 při stupni 4 je Monte Carlo asi 3× lepší) a u součinu mnoha
různých proměnných s exponentem 1, třeba $x_1x_2\cdots x_6$: vzor $(1, 1, \dots, 1)$ je jen jeden z mnoha
možných. Pro šest proměnných s korelací 0,6 tam Monte Carlo vyhraje asi 6×. Graf „Rozptyl podle stupně“
v laboratoři ukazuje, kde se čáry kříží.

**Co přesně říká věta.** Andersen a Shan dokazují, že pro stupeň $K \ge \zeta N^2$ ($N$ = počet proměnných)
existují úlohy, kde GBS-I potřebuje řádově $N^{3+p}$ vzorků, kdežto Monte Carlo aspoň $e^{cN^2}$. Je to věta
o existenci: říká, že výhodné úlohy jsou a že malá změna matice výhodu nezničí, ale ne, jak častá je výhoda
u konkrétních finančních úloh. Druhý článek to odhaduje numericky na náhodných úlohách: podíl výhodných úloh
roste se stupněm; GBS-P bývá ve výhodných případech zhruba 100× lepší, GBS-I až $10^{10}$×, ale pro nejnižší
zkoumaný stupeň a šest proměnných je u GBS-P výhodných jen 18,7 % úloh.

**Rozptyl není čas.** Všechno výše porovnává počet vzorků. Jak dlouho trvá jeden výstřel proti jednomu scénáři
a kolik stojí, je jiná otázka – rozebírá ji kapitola o háčcích.
""",
    further_reading=(
        Reading(ANDERSEN_SHAN_EXPECTATIONS, "věty 1.3 a 1.5 o exponenciální výhodě"),
        Reading(ANDERSEN_SHAN_ADVANTAGE, "podíl výhodných úloh, obr. 1 a 2"),
        Reading(DRIMAL_MONTE_CARLO, "kap. 5.7 metoda váženého výběru"),
    ),
)

BASICS: Tuple[TheoryTopic, ...] = (
    BIG_PICTURE,
    GAUSSIAN_PROBLEM,
    MONTE_CARLO_VARIANCE,
    GBS_DEVICE,
    TUNING,
    GBS_P_ESTIMATOR,
    WHY_EXPONENTIAL,
)
