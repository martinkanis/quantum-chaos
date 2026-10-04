"""Guide for a beginning PhD student, part 2: the five problems, the simulation, Qiskit, caveats and next steps."""

from __future__ import annotations

from typing import Tuple

from ui.advantage_content import (
    AARHUS_TALK,
    ANAND_POLYNOMIAL_SIMULATION,
    ANGUITA_MONTE_CARLO_ACCELERATOR,
    DANISH_QUANTUM_USE_CASES_PAGE,
    QISKIT_DOCUMENTATION,
    QPURPOSE_FINANCE,
    SHAN_SHAN_HOMEPAGE,
    ZHANG_GBS_MCMC,
)
from ui.caveats_content import CLASSICAL_SIMULATION, CLOSED_FORM, SAMPLES_NOT_TIME, SIGN_PROBLEM
from ui.theory_content import (
    ANDERSEN_SHAN_ADVANTAGE,
    ANDERSEN_SHAN_EXPECTATIONS,
    CLEMENTS,
    DAMODARAN_RETURNS,
    DANISH_QUANTUM_USE_CASES,
    DRIMAL_MONTE_CARLO,
    GLASSERMAN,
    HAMILTON,
    KRUSE,
    OH_CLASSICAL_SIMULATION,
    RECK,
    SDU_QUANTUM_FINANCE,
    WALRUS_HAFNIAN,
    Reading,
    Source,
    TheoryTopic,
)

SHARPE_SINGLE_INDEX = Source(
    "Sharpe, W. F.: *A Simplified Model for Portfolio Analysis*. Management Science 9 (1963), 277–293 – "
    "jednofaktorový (indexový) model trhu"
)
GOLUB_VAN_LOAN = Source(
    "Golub, G. H., Van Loan, C. F.: *Matrix Computations*. 4. vyd., Johns Hopkins University Press 2013 – "
    "Householderovy reflexe a Givensovy rotace (kap. 5)"
)
STRAWBERRY_FIELDS = Source(
    "Killoran, N., Izaac, J., Quesada, N., Bergholm, V., Amy, M., Weedbrook, C.: *Strawberry Fields: A Software "
    "Platform for Photonic Quantum Computing*. Quantum 3, 129 (2019) – knihovna pro simulaci fotonických obvodů"
)

FIVE_PROBLEMS = TheoryTopic(
    anchor="pruvodce-pet-uloh",
    title="Pět připravených úloh: proč jsou vhodné",
    in_short=(
        "Všech pět úloh má vysoký stupeň (16–20) a málo proměnných (1–4), tedy přesně to, co teorie chce. "
        "Liší se tím, co ukazují: čistou exponenciální výhodu, společné chvosty, nesouměrné exponenty, past "
        "špatného ladění na reálných datech a slábnutí výhody s počtem proměnných."
    ),
    explanation=r"""
**Přehled** (ladění fotonů po módech, $v$ = relativní rozptyl jednoho vzorku):

| úloha | proměnné | stupeň | $v_{\mathrm{MC}}$ | cílový vzor padá | $v_{\mathrm{GBS}}$ | výhoda GBS | Qiskit |
|---|---|---|---|---|---|---|---|
| 1 · $\mathbb{E}[X^{20}]$ | 1 | 20 | 746 000 | 1× za 42 výstřelů | 10,3 | 72 000× | 8 qubitů |
| 2 · $\mathbb{E}[X_1^8X_2^8]$ | 2 | 16 | 54 600 | 1× za 250 | 61,9 | 880× | 10 qubitů |
| 3 · $\mathbb{E}[X_1^{12}X_2^4]$ | 2 | 16 | 53 700 | 1× za 210 | 51,4 | 1 000× | 10 qubitů |
| 4 · akcie, dluhopisy, zlato | 3 | 18 | 120 000 | 1× za 2 900 | 721 | 170× | 15 qubitů |
| 5 · tržní faktor | 4 | 16 | 60 600 | 1× za 4 000 | 1 006 | 60× | 20 qubitů |

**Úloha 1: extrémní moment jedné veličiny.** Normovaná veličina, třeba denní výnos vydělený volatilitou,
a její 20. moment. Nejčistší ukázka exponenciální výhody: Monte Carlo trpí těžkým chvostem (kapitola 3),
GBS s jedním módem padá na vzor „20 fotonů“ zhruba v každém 42. výstřelu. Vyzkoušej: změň exponent na 10,
30 nebo 40 a sleduj, jak výhoda roste zhruba 4× na každé dva stupně.

**Úloha 2: společný extrém dvou aktiv.** Dvě aktiva s korelací 0,5 a součin jejich osmých mocnin – měří, jak
často jsou obě zároveň daleko od průměru. Dva módy, vzor $(8, 8)$ je jeden ze 17 vzorů s 16 fotony a padá
v každém 250. výstřelu. Vyzkoušej: korelace 0, 0,5 a 0,9 – výhoda s korelací roste zhruba od 440× do 1 050×,
protože silně korelovaná aktiva mají extrémy častěji společně.

**Úloha 3: nesouměrný monom.** Stejná dvojice, exponenty 12 a 4. Ukazuje, proč ladit fotony po módech: při
ladění jen celkového počtu (jako v článku) padá vzor $(12, 4)$ jednou za 610 výstřelů a výhoda klesne asi na
350×. Vyzkoušej: přepni ladění a porovnej tabulku „Nastavení zařízení“.

**Úloha 4: akcie, dluhopisy a zlato (USA 1928–2023).** Skutečná kovarianční matice ročních výnosů (data
A. Damodarana, NYU Stern) a společný šestý moment. Korelace jsou skoro nulové, ale volatility různé: dluhopisy
8 %, akcie a zlato kolem 20 %. Varování i poučení zároveň – při ladění z článku GBS prohraje asi 250×, po
módech vyhraje asi 170× (podrobně v kapitole 5). Vyzkoušej: přepni ladění a sleduj průměrné počty fotonů.

**Úloha 5: čtyři aktiva s tržním faktorem.** Korelace vznikají z jednoho společného faktoru, trhu
(jednofaktorový model Sharpeho typu): $\Sigma_{ij} = \beta_i\beta_j$ s citlivostmi 0,9; 0,8; 0,7 a 0,6, na
diagonále jedničky. Stupeň 16 jako v úloze 2, ale proměnné jsou čtyři: vzorů s 16 fotony je 969 a výhoda
klesne na desítky. Ukazuje, proč musí stupeň růst rychleji než počet proměnných. Vyzkoušej: graf „Rozptyl
podle stupně“ – při stupni 4 tu ještě vyhrává Monte Carlo, při stupni 8 jsou metody zhruba vyrovnané.

**Najdi úlohu, kde GBS prohraje.** Nastav šest proměnných, všechny exponenty 1 a korelace 0,6: Monte Carlo
vyhraje asi 6×. Polynom nízkého stupně v mnoha proměnných je pro GBS nevhodný – a přesně takové bývají
běžné finanční úlohy.
""",
    further_reading=(
        Reading(DAMODARAN_RETURNS, "data k úloze 4"),
        Reading(SHARPE_SINGLE_INDEX, "model k úloze 5"),
        Reading(ANDERSEN_SHAN_ADVANTAGE, "které úlohy jsou výhodné"),
    ),
)

SIMULATION_AND_CHARTS = TheoryTopic(
    anchor="pruvodce-simulace",
    title="Jak aplikace simuluje a jak číst grafy",
    in_short=(
        "GBS se simuluje jako ideální přístroj: protože odhad GBS-P potřebuje jen počet výstřelů s cílovým vzorem, "
        "losuje se rovnou z binomického rozdělení. Monte Carlo generuje skutečné gaussovské scénáře. Obě metody se "
        "opakují 20× a grafy ukazují relativní chybu proti počtu vzorků, rozptyl podle stupně a rozptyl odhadů."
    ),
    explanation=r"""
**Simulace GBS.** Přístroj by vracel celé vzory, ale odhad GBS-P z nich použije jen jedno číslo: kolikrát padl
cílový vzor. Ze $N$ nezávislých výstřelů má tento počet přesně binomické rozdělení s parametry $N$ a $p(n)$,
takže ho aplikace losuje přímo – výsledek je stejný, jako kdyby simulovala každý výstřel. Pravděpodobnost
$p(n)$ zná přesně (hafnián spočítaný rekurzí). Přístroj je ideální: žádné ztráty, žádný šum, dokonalé
detektory.

**Simulace Monte Carla.** Skutečné losování z $\mathcal{N}(0, \Sigma)$ po dávkách 100 000 scénářů, pro každý se
spočítá $x^n$ a výsledky se průměrují.

**Opakování a počty vzorků.** Pro 13 počtů vzorků od 100 do zvoleného maxima (logaritmicky rozložených) se
odhad spočítá 20× s jinými náhodnými čísly; větší počty vzorků znovu použijí ty předchozí. Z 20 odhadů se
spočítá *relativní RMSE*, typická odchylka odhadu od přesné hodnoty v procentech. Seed určuje náhodná čísla:
stejný seed dá stejný výsledek, různé seedy ukážou, jak moc výsledek kolísá.

**Graf „Rozptyl podle stupně“.** Bere stejný poměr exponentů (třeba $X_1X_2$, $X_1^2X_2^2$, $X_1^3X_2^3$, …)
a pro rostoucí stupeň kreslí relativní rozptyl jednoho vzorku. Svislá osa je logaritmická: přímka znamená
exponenciální růst. Monte Carlo je přímka, GBS-P roste mnohem pomaleji; tečkovaná svislá čára je zadaný monom.
Šedá čárkovaná čára je druhá varianta ladění.

**Graf konvergence.** Relativní chyba proti počtu vzorků, obě osy logaritmické. Obě metody mají sklon
$-\tfrac12$ (čtyřikrát víc vzorků, poloviční chyba); čárkovaně je teorie $\sqrt{v/N}$. O vítězi rozhoduje jen
výška čáry, tedy $v$.

**Graf rozptylu odhadů.** Odhady všech 20 opakování po největším počtu vzorků, vydělené přesnou hodnotou
(1 = přesně). GBS-P tvoří úzký shluk kolem jedničky. Monte Carlo je rozházené a většinou *pod* jedničkou: vzácné
obří scénáře, které výsledek tvoří, se do většiny běhů nevejdou. Proto naměřená chyba Monte Carla často vyjde
menší, než říká teorie – a občas, když obří scénář přijde, mnohem větší.

**Co si odnést.** Zbytečně nevěř jedné simulaci; čti spolu teorii, opakování a rozptyl odhadů. To platí
i mimo tuto aplikaci.
""",
    further_reading=(
        Reading(DRIMAL_MONTE_CARLO, "odhad chyby Monte Carla a interval spolehlivosti"),
    ),
)

QISKIT = TheoryTopic(
    anchor="pruvodce-qiskit",
    title="Qiskit: jak se fotony emulují na qubitech",
    in_short=(
        "Qiskit pracuje s qubity, ne s fotony. Skript proto každý mód zakóduje do několika qubitů (binární číslo = "
        "počet fotonů), připraví stlačené vakuum, interferometr složí z děličů svazku (Givensových rotací), změří "
        "qubity a z četnosti cílového vzoru spočítá odhad GBS-P. Ověřuje vzorce; kvantovou výhodu nepřináší."
    ),
    explanation=r"""
**Spuštění.** Stáhni skript tlačítkem na 3. stránce (obsahuje matici a exponenty z laboratoře) a v terminálu:

```
pip install "qiskit>=1.0" numpy
python gbs_monom_qiskit.py
```

Potřebuje Python 3.9 nebo novější. Úlohy s 8–15 qubity doběhnou za pár sekund, s 20 qubity asi za 10 s.

**1. Mód jako binární číslo.** Mód může nést 0, 1, 2, … fotonů, qubit jen 0 nebo 1. Mód proto dostane $q$ qubitů
a jejich bity tvoří binární zápis počtu fotonů: s $q = 5$ jde zapsat 0 až 31 fotonů. Víc fotonů se do módu
„nevejde“ – tomu se říká *ořez*. Interferometr počet fotonů zachovává, takže pro cílový vzor se stupněm $|n|$
stačí ořez nad $|n|$: amplituda cílového vzoru pak vyjde přesně. Ořez ale zahodí malou část stlačeného světla;
skript vypíše, kolik pravděpodobnosti zachoval, a odhad o ni opraví.

**2. Stlačené vakuum.** Amplitudy jsou známé přesně:

$$
\langle 2k|\psi\rangle = \frac{\tanh^k r\,\sqrt{(2k)!}}{2^k\,k!\,\sqrt{\cosh r}},
$$

skript je počítá rekurzí $a_{2k} = a_{2k-2}\tanh r\,\sqrt{(2k-1)/(2k)}$, aby faktoriály nepřetekly. Stav
z $|0\rangle$ připraví *Householderova reflexe* $U = I - 2ww^\top/(w^\top w)$ s $w = e_0 - \psi$ – unitární
matice, která převede vektor $e_0$ na $\psi$. V Qiskitu je to `UnitaryGate` na $q$ qubitech módu.

**3. Interferometr z děličů svazku.** Ortogonální matici $O$ z rozkladu $B = O\,\mathrm{diag}(\tanh r)\,O^\top$
rozloží QR rozklad na *Givensovy rotace* – otočení ve dvou souřadnicích. Fyzikálně je každá rotace dělič
svazku mezi dvěma módy, $\exp\big(\theta\,(a_i^\dagger a_j - a_j^\dagger a_i)\big)$, kde $a$ ruší a $a^\dagger$
přidává foton. Skript jeho matici na $2q$ qubitech spočítá diagonalizací (generátor je antisymetrický)
a vloží jako další `UnitaryGate`. Pořadí a znaménka rotací musí sedět tak, aby výsledný přístroj nesl právě
$B$ – kontrola v kroku 5 to ověří.

**4. Měření.** `measure_all()` změří všechny qubity a `StatevectorSampler` (přesný simulátor) vrátí četnosti
bitových řetězců. Bity módu $i$ jsou binární zápis počtu fotonů v detektoru $i$; skript z nich pozná, kolikrát
padl cílový vzor.

**5. Kontrola a odhad.** Skript nejdřív spočítá pravděpodobnost cílového vzoru ze stavového vektoru a porovná
ji se vzorcem s hafniánem – musí se shodovat na všech vypsaných číslicích. Pak z četnosti spočítá odhad GBS-P
a porovná ho s přesnou hodnotou (Steinova rekurze) a s klasickým Monte Carlem se stejným počtem vzorků. Pro
úlohu 1 vyšlo: GBS-P 2 356 zásahů ze 100 000 výstřelů a chyba −0,1 %, Monte Carlo chyba +131 %.

**Proč žádná kvantová výhoda.** Emulace na qubitech je jen jiný zápis téže fyziky: simulátor drží celý stav
($2^{20}$ amplitud pro 20 qubitů) a amplitudy jsme připravili z klasického výpočtu. Na skutečném qubitovém
počítači by se brány na 5–10 qubitech rozložily na tisíce dvouqubitových bran a dnešní šum by výsledek zničil.
Skutečný GBS je fotonický čip (Xanadu, USTC); pro simulaci fotonických obvodů jsou knihovny Strawberry Fields
a The Walrus.

**Limity skriptu.** Nejvýš 20 qubitů; pro víc módů nejvýš 5 qubitů na mód (dělič svazku je pak matice
1024 × 1024), takže stupeň do 31.
""",
    further_reading=(
        Reading(QISKIT_DOCUMENTATION, "instalace, obvody a primitivum Sampler"),
        Reading(GOLUB_VAN_LOAN, "Householderovy reflexe a Givensovy rotace"),
        Reading(RECK, "složení libovolného interferometru z děličů svazku"),
        Reading(CLEMENTS, "úspornější uspořádání děličů"),
        Reading(KRUSE, "stav GBS ve Fockově bázi"),
        Reading(STRAWBERRY_FIELDS),
        Reading(WALRUS_HAFNIAN),
    ),
)

CAVEATS = TheoryTopic(
    anchor="pruvodce-hacky",
    title="Háčky: proč to (zatím) není výhra",
    in_short=(
        "Výhoda je spočítaná v počtu vzorků ideálního přístroje proti obyčejnému Monte Carlu. Chytřejší klasické "
        "metody umí totéž, výstřel není zadarmo, reálné přístroje ztrácejí fotony, rozdělení GBS jde pro mnoho "
        "struktur vzorkovat klasicky a znaménko výsledku musí být známé předem."
    ),
    explanation=r"""
**1. Soupeřem není obyčejné Monte Carlo.** Kdo počítá $\mathbb{E}[X^{20}]$, nepoužije obyčejné Monte Carlo.
Vážený výběr ze širší normální křivky (rozptyl 21) dá relativní rozptyl asi 2,8, tedy dokonce lepší než GBS-P
(10,3). Pro malé úlohy jsou navíc k dispozici přesné vzorce. Férové srovnání musí brát nejlepší klasickou
metodu, ne nejslabší.

**2. Počet vzorků není čas ani cena.** Procesor vygeneruje desítky až stovky milionů gaussovských čísel za
sekundu. U fotonického přístroje se k rychlosti výstřelů přidává nastavení interferometru pro každou matici,
kalibrace, fronta na přístroj a přenos dat. Výhoda „1 000× méně vzorků“ může v čase znamenat cokoli.

**3. Ztráty a šum.** Každý ztracený foton změní vzor a tím i odhad. Se ztrátami se pravděpodobnosti od vzorce
s hafniánem odchylují a výstup reálných zařízení jde napodobit klasickými algoritmy (Oh a kol. 2024).

**4. Klasicky vzorkovatelné struktury.** Pro nezáporné matice a grafy vyšly v roce 2025 efektivní klasické
samplery (Zhang a kol.; Anand a kol.). Finanční kovarianční matice bývají právě takové. Pak lze stejný „vážený
výběr podle GBS“ provést klasicky – výhoda v rozptylu zůstane, kvantová výhoda zmizí. Pravděpodobně proto
Qpurpose mluví o „quantum-inspired“ modelech na HPC.

**5. Znaménkový problém.** Přístroj měří $\mathrm{Haf}^2$. U polynomů se smíšenými znaménky koeficientů nebo
se zápornými korelacemi a lichými exponenty je potřeba znaménko každého členu zjistit jinak.

**6. Malé úlohy jsou klasicky snadné.** Všechno na 3. stránce spočítáme přesně za milisekundy. Těžké jsou
hafniány velkých matic s malými exponenty – a tam je zase výhoda v rozptylu nejslabší (kapitola 7).

**7. Věta o existenci.** Exponenciální výhoda platí pro *některé* úlohy vysokého stupně. Že mezi nimi jsou
užitečné finanční úlohy, zatím nikdo neukázal.

**Co z toho plyne.** Myšlenka je matematicky správná a zajímavá; výhoda proti obyčejnému Monte Carlu je reálná
u úloh vysokého stupně s málo proměnnými. Mezi „dokázaná výhoda v počtu vzorků“ a „rychlejší a přesnější
obchodování v bance“ ale zbývá několik nedoložených kroků.
""",
    further_reading=(
        Reading(OH_CLASSICAL_SIMULATION, "klasická simulace ztrátových přístrojů"),
        Reading(ZHANG_GBS_MCMC, "klasické vzorkování GBS pro grafy"),
        Reading(ANAND_POLYNOMIAL_SIMULATION),
        Reading(GLASSERMAN, "nejlepší klasické metody snižování rozptylu"),
    ),
    related_caveats=(SAMPLES_NOT_TIME, CLASSICAL_SIMULATION, SIGN_PROBLEM, CLOSED_FORM),
)

QPURPOSE = TheoryTopic(
    anchor="pruvodce-qpurpose",
    title="Qpurpose a Jyske Bank: co tvrdí a jak to číst",
    in_short=(
        "Qpurpose je spin-off Centra kvantové matematiky na University of Southern Denmark. S Jyske Bank tvrdí "
        "přesnější krátkodobé předpovědi cen a „exponenciální zrychlení“. Veřejně doložená je jen matematika "
        "Andersena a Shan; bankovní aplikace ani čísla z webu publikované nejsou."
    ),
    explanation=r"""
**Kdo to je.** Jørgen Ellegaard Andersen vede Centre for Quantum Mathematics (QM) na University of Southern
Denmark, Shan Shan je jeho spoluautorka. Firma Qpurpose vznikla v roce 2022 jako spin-off centra a spolupracuje
s dánskou Jyske Bank.

**Co tvrdí.**

- Web Qpurpose: předpověď krátkodobých cen a směru trhu pro více než 300 akcií z živých dat, tříletá spolupráce
  s Jyske Bank, „exponenciální zrychlení oproti konvenčním metodám“, odchylka 2 bazické body a pětkrát vyšší
  přesnost ocenění. Bez metodiky a bez odkazu na články.
- Brožura *16 Danish Quantum Use Cases* (prosinec 2024), případ 16: algoritmus zatím běží simulovaný na
  klasickém počítači, „v určitých případech“ má dávat exponenciální zrychlení, jde o gaussovsky vážené
  integrály a cílem jsou vyšší výnosy z obchodování.
- Stránka SDU: rámec „Gaussian Boson Sampling applied to Gaussian Weighted Integrals“ (Andersen, Shan),
  „quantum-inspired“ modely, denní HPC simulace na tradingovém desku banky.

**Jak to nejspíš funguje (náš odhad).** (1) Pohyby cen jako vícerozměrné normální rozdělení odhadnuté z dat.
(2) Hledaná veličina jako $\mathbb{E}[f(X)]$ pro polynom nebo mocninnou řadu, tedy součet hafniánů. (3) Odhad
GBS-I nebo GBS-P místo obyčejného Monte Carla. (4) Protože kvantový přístroj nemají, vzorkují rozdělení GBS
klasicky – přesně pro malé úlohy, efektivními samplery pro nezáporné matice. Výhoda v rozptylu tak může být
reálná, ale je klasická.

**Kontrolní otázky pro čtení podobných tvrzení.**

1. S čím se srovnává – s obyčejným Monte Carlem, nebo s nejlepší klasickou metodou?
2. Měří se počet vzorků, čas, nebo cena?
3. Jde rozdělení klasicky vzorkovat? Pokud ano, kde je kvantová část?
4. Je výsledek recenzovaný a dá se zopakovat?
5. Co přesně znamená „odchylka 2 bazické body“ – chyba čeho, proti čemu a na jakých datech?

**Co je publikované.** Jen dva preprinty na arXivu (únor 2025): o odhadech GBS-I a GBS-P a o podílu výhodných
úloh. Recenzovanou verzi ani článek o aplikaci pro banku se dohledat nepodařilo. Andersen téma představil
v přednášce na Aarhus University (15. 9. 2025), bez odkazu na další práce.
""",
    further_reading=(
        Reading(QPURPOSE_FINANCE),
        Reading(DANISH_QUANTUM_USE_CASES, "celá brožura"),
        Reading(DANISH_QUANTUM_USE_CASES_PAGE, "jen strana s případem Jyske Bank"),
        Reading(SDU_QUANTUM_FINANCE),
        Reading(ANDERSEN_SHAN_EXPECTATIONS),
        Reading(ANDERSEN_SHAN_ADVANTAGE),
        Reading(SHAN_SHAN_HOMEPAGE),
        Reading(AARHUS_TALK),
    ),
)

NEXT_STEPS = TheoryTopic(
    anchor="pruvodce-dal",
    title="Jak pokračovat: náměty pro doktoranda",
    in_short=(
        "Doporučené pořadí čtení, sedm cvičení v laboratoři a se skriptem pro Qiskit a otevřené otázky, které by "
        "mohly být tématem vlastní práce."
    ),
    explanation=r"""
**Pořadí čtení.**

1. Hamilton a kol. 2017 – co je GBS a odkud se bere hafnián (krátký článek).
2. Kruse a kol. 2019 – totéž podrobně, s odvozením.
3. Andersen a Shan 2025 – úloha, odhady GBS-I a GBS-P, věty o výhodě; pak druhý preprint o podílu výhodných
   úloh.
4. Oh a kol. 2024, Zhang a kol. 2025, Anand a kol. 2025 – kdy jde GBS simulovat klasicky.
5. Anguita a kol. 2025 – experiment, kde boson sampling slouží jako vážený výběr pro Monte Carlo.
6. Glasserman 2004, kap. 4 – klasické snižování rozptylu, tedy férový soupeř.

**Cvičení.**

1. Úloha 1: změň exponent na 10, 30 a 40. Ověř, že výhoda roste zhruba 4× na každé dva stupně.
2. Úloha 2: zkus korelace 0, 0,5 a 0,9. Jak se mění pravděpodobnost cílového vzoru a proč?
3. Najdi úlohu, kde vyhraje Monte Carlo (tip: mnoho proměnných s exponentem 1).
4. Úloha 4: přepni ladění. Vysvětli z tabulky „Nastavení zařízení“, proč je rozdíl tak obrovský.
5. Stáhni skript pro Qiskit a spusť ho. Porovnej kontrolu $p(n)$ s laboratoří a změň `SHOTS` – jak se mění
   chyba?
6. Pokročilé: naprogramuj klasický vážený výběr pro $\mathbb{E}[X^{20}]$ a najdi nejlepší rozptyl širší
   normální křivky. Proč vyjde lepší než GBS-P?
7. Pokročilé: přidej do skriptu ztráty (dělič svazku do pomocného módu, který se neměří) a sleduj, jak se
   odhad rozbije.

**Otevřené otázky.**

- Které finanční veličiny jsou opravdu polynomy vysokého stupně v málo proměnných?
- Jak se vyrovnat se znaménkovým problémem u polynomů se smíšenými znaménky?
- Jak výhoda přežije ztráty a omezené detektory reálných přístrojů?
- Jsou matice z finančních dat (často nezáporné korelace) klasicky snadno vzorkovatelné? Pokud ano, kolik
  z výhody je vlastně klasické?
- Jak vypadá férové srovnání s quasi-Monte Carlem, váženým výběrem a řídicími proměnnými?

**Nástroje.** Qiskit (qubitová emulace jako tady), Strawberry Fields a The Walrus (fotonické obvody
a hafniány), NumPy pro vlastní experimenty. Zdrojový kód této aplikace je dobrý začátek: gaussovské momenty
jsou v `gbs/gaussian_moments.py`, ladění stlačení v `gbs/photon_tuning.py` a odhady v `gbs/monomial_problem.py`.
""",
    further_reading=(
        Reading(HAMILTON),
        Reading(KRUSE),
        Reading(ANDERSEN_SHAN_EXPECTATIONS),
        Reading(ANDERSEN_SHAN_ADVANTAGE),
        Reading(ANGUITA_MONTE_CARLO_ACCELERATOR),
        Reading(GLASSERMAN),
    ),
)

PRACTICE: Tuple[TheoryTopic, ...] = (
    FIVE_PROBLEMS,
    SIMULATION_AND_CHARTS,
    QISKIT,
    CAVEATS,
    QPURPOSE,
    NEXT_STEPS,
)
