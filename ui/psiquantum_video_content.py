"""Notes from Dr Ben Miles's video „The Genius of Computing with Light“ (February 2026) about PsiQuantum.

A subpage of the PsiQuantum page: the video's chapters with frames and links into the video, then a chapter of our
own on what the video leaves out. Frames and the presentation are served behind the login (web/lecture_slides.py);
the transcript and all 191 frames are on the branch podklady-video. Our own numbers are checked by
tests/test_psiquantum_video_page.py.
"""

from __future__ import annotations

from typing import Tuple

from ui.photonics_landscape_content import PSIQUANTUM_OMEGA
from ui.psiquantum_content import LINDE_CRYOPLANT
from ui.theory_content import KeyFinding, Reading, Source, TheoryTopic
from ui.walther_lecture_content import ChapterTime, LectureSlide

LECTURE = "psiquantum-video-2026"
"""Folder of the frames and the presentation in content/lectures and part of their URL."""
VIDEO_URL = "https://youtu.be/rbxcd9gaims"
VIDEO_SECONDS = 1941
"""Length of the recording, 32:21."""
SPONSOR_START, SPONSOR_END = 648, 714
"""The sponsor segment (Shortform), left out of the notes."""
TITLE = "Video: The Genius of Computing with Light (Dr Ben Miles, 2026)"
SOURCES_ANCHOR = "psiv-zdroje"

INTRO = (
    "Zápisky z videa fyzika a youtubera Bena Milese (únor 2026, 32 minut, anglicky), který jako jeden z mála dostal "
    "přístup do laboratoří PsiQuantum. Video prochází součástky fotonického kvantového počítače jednu po druhé: zdroj "
    "jednotlivých fotonů, detektory, rychlé přepínače z titaničitanu barnatého, interferometry, kryostaty a převod "
    "qubitu z prostoru do času, kterým se propojují čipy. Kapitoly sledují video; u každé jsou snímky a odkaz na čas. "
    "Na konci je naše kapitola o tom, co video neříká – navazuje na stránku o PsiQuantum."
)

HOW_MADE = (
    "Jak stránka vznikla: zvuk jsme přepsali modelem Whisper large-v3 a snímky vytáhli ze záznamu při změnách obrazu "
    "(191 snímků, zde vybrané). Video natočil autor se souhlasem firmy, ale podle svých slov bez placení od ní; "
    "sponzorem je služba Shortform (reklama 10:48–11:54, viz Quantum Academy). Prezentace ke stažení vychází z těchto "
    "zápisků. Snímky i prezentace jsou jen pro přihlášené."
)

KEY_FINDINGS = (
    KeyFinding(
        "**Qubit je dráha fotonu** ve vlnovodu na křemíkovém čipu (dvoukolejné kódování); čipy se vyrábějí na 300mm "
        "deskách stejně jako běžná elektronika.",
        "psiv-svetlo",
    ),
    KeyFinding(
        "**Zdroj:** laserové pulzy v prstencových rezonátorech vyrobí pár fotonů (čtyřvlnné směšování); detekce "
        "jednoho z páru ohlásí, že druhý existuje, a rychlý přepínač ho pošle do výpočtu. Mnoho zdrojů vedle sebe "
        "dělá z náhody „hodiny“.",
        "psiv-hodiny",
    ),
    KeyFinding(
        "**Detektory a přepínače:** supravodivé nanodrátky (na čipu přes 93 %, další generace 99 %) a přepínače "
        "z titaničitanu barnatého (BTO), které reagují za zlomky nanosekundy – růst BTO na křemíku trval "
        "přes deset let.",
        "psiv-bto",
    ),
    KeyFinding(
        "**Chlazení na 2 K** v kryostatech „Mark II“, stokrát tepleji než supravodivé qubity (20 mK); cílem jsou 4 K.",
        "psiv-matematika",
    ),
    KeyFinding(
        "**Propojení čipů:** qubit se převede z dvou drah na dva časové okamžiky vzdálené 1 ns, proletí "
        "vláknem a znovu "
        "se převede zpět; přes 250 m vlákna s věrností 99,7 % (článek v Nature 2025).",
        "psiv-cas",
    ),
    KeyFinding(
        "**Co video neříká:** věrnosti jsou podmíněné tím, že foton dorazil; ztráty, logický qubit ani termíny "
        "nepadnou. Je to výborný průvodce součástkami, ne nezávislé hodnocení firmy.",
        "psiv-kriticky",
    ),
)

MILES_VIDEO = Source(
    "Miles, B.: *The Genius of Computing with Light*. YouTube, 15. 2. 2026, "
    "[video](https://youtu.be/rbxcd9gaims)"
)
SILVERSTONE_2014 = Source(
    "Silverstone, J. W. a kol.: *On-chip quantum interference between silicon photon-pair sources*. Nature Photonics "
    "8, 104–108 (2014)"
)
NATARAJAN_2012 = Source(
    "Natarajan, C. M., Tanner, M. G., Hadfield, R. H.: *Superconducting nanowire single-photon detectors: physics and "
    "applications*. Superconductor Science and Technology 25, 063001 (2012)"
)
ABEL_2019 = Source(
    "Abel, S. a kol.: *Large Pockels effect in micro- and nanostructured barium titanate integrated on silicon*. "
    "Nature Materials 18, 42–47 (2019)"
)
BRENDEL_1999 = Source(
    "Brendel, J., Gisin, N., Tittel, W., Zbinden, H.: *Pulsed energy-time entangled twin-photon source for quantum "
    "communication*. Physical Review Letters 82, 2594 (1999) – kódování do časových okamžiků (time-bin)"
)

INTRO_TOPIC = TheoryTopic(
    anchor="psiv-uvod",
    title="Nejtajnější kvantový počítač Silicon Valley",
    in_short=(
        "Ben Miles dělal doktorát v budově v Bristolu, ze které PsiQuantum vzešel, a pět let firmu přemlouval, aby ho "
        "pustila dovnitř. Cílem firmy je jediná věc: první užitečný kvantový počítač, vyráběný jako továrna."
    ),
    explanation=r"""
Video začíná u kryostatu: „tohle by mohla být budoucnost kvantového počítání“. Miles zdůrazňuje, že nejde o křehké
laboratorní zařízení, ale o systém navržený pro provoz v měřítku celé továrny, chlazený na **2 K** – chladněji než
vesmír. PsiQuantum podle něj právě získal miliardu dolarů (kolo ze září 2025, viz
[stránka o PsiQuantum](/fotonika-ve-svete/psiquantum#psiq-penize)).

**Proč zrovna on.** Miles dělal doktorát z optické fyziky v Bristolu, v budově, odkud firma vzešla, a s několika
lidmi z PsiQuantum studoval. I tak trvalo pět let, než natáčení povolili. Říká, že video firma neplatí; sponzorem je
služba Shortform (reklamu v 10:48–11:54 zápisky vynechávají; co Shortform je, popisuje
[Quantum Academy](/quantum-academy)).

**O čem video je.** Ne o algoritmech, ale o součástkách: „tam se odehrává inženýrská magie“. To je pro doktoranda
cenné – kapitoly odpovídají tomu, co v [přednášce Philipa Walthera](/fotonika/prednaska-walther-2022#walther-hardware)
zaznělo obecně, jen tady s konkrétními řešeními jedné firmy.
""",
    further_reading=(Reading(MILES_VIDEO),),
)

LIGHT_TOPIC = TheoryTopic(
    anchor="psiv-svetlo",
    title="Kvantový počítač, který běží na světle",
    in_short=(
        "Křemíkové desky o průměru 300 mm, do nich vyleptané vlnovody a qubit zapsaný do toho, kterou ze dvou drah "
        "foton letí. Podle Marka Thompsona fotony nedekoherují a navíc se dají posílat mezi čipy."
    ),
    explanation=r"""
**Čip.** Ben Burridge, který má v PsiQuantum na starost zdroje světla, ukazuje jednu z prvních 300mm křemíkových
desek. Stejnou litografií jako v polovodičovém průmyslu se do ní vyleptají hřebínky široké asi 100 nm – **vlnovody**.
Vedou světlo jako optické vlákno, protože mají vyšší index lomu než okolí. Rozdíl proti běžnému čipu: neteče jimi
proud, ale světlo, a informace je v tom, **kudy foton letí**.

**Qubit.** Vlnovod se rozdělí na dvě dráhy: foton v jedné je $|0\rangle$, v druhé $|1\rangle$ (dvoukolejné
kódování). Přiblíží-li se dráhy na krátkém úseku k sobě, foton může „přeskočit“ – vznikne dělič svazku; u děliče
50 : 50 je foton se stejnou pravděpodobností v obou drahách a dokud ho neměříme, je v superpozici obou.

**Proč fotony podle firmy.** Spoluzakladatel a technický ředitel Mark Thompson uvádí dva důvody:

1. *Nedekoherují.* Fotony letí rychlostí světla a „nezažívají čas“; polarizace reliktního záření je podle něj
   zachovaná od vzniku vesmíru, takže doba dekoherence fotonů je „aspoň stáří vesmíru“, kdežto qubity z hmoty mají
   podle něj nanosekundy až mikrosekundy.
2. *Cestují.* Velký počítač nikdy nebude na jednom čipu – ani notebook není jeden čip a datová centra pro AI spojují
   statisíce čipů. Fotony jsou přirozený způsob, jak přenášet kvantovou informaci mezi moduly.

*Vlastní poznámka:* bod 1 je v jádru pravdivý (rozvádí ho
[doplněk o koherenci](/fotonika/prednaska-walther-2022#walther-provazani)), ale formulace je přehnaná. Qubity z iontů
nebo neutrálních atomů drží koherenci i sekundy, ne jen mikrosekundy, a skutečnou „dekoherencí“ fotonů je ztráta –
foton zmizí. Polarizace reliktního záření se navíc otiskla až zhruba 380 000 let po velkém třesku, ne při něm.
""",
    further_reading=(Reading(MILES_VIDEO, "od 1:38"),),
)

SOURCE_TOPIC = TheoryTopic(
    anchor="psiv-zdroj",
    title="Jak vyrobit jeden foton",
    in_short=(
        "Laserové pulzy (1 550 nm) krouží v prstencových rezonátorech a nelinearita křemíku občas promění dva fotony "
        "laseru v pár nových fotonů – „modrý“ a „červený“. Filtr pustí dál jen modrý. Jenže se to stane zhruba jednou "
        "z milionu."
    ),
    explanation=r"""
Výpočet potřebuje pravidelný proud **přesně jednoho fotonu najednou** – obdobu hodin v běžné elektronice. PsiQuantum
na to podle Milese strávil většinu inženýrské práce prvních let. Řešení: „světlem vyrobit světlo“.

**Jak to funguje (zjednodušeně):**

1. Krátké pulzy laseru s vlnovou délkou **1 550 nm** (pumpa) vstupují do řady **prstencových rezonátorů** – kruhových
   vlnovodů, jejichž obvod je celistvým násobkem vlnové délky. Světlo v prstenci oběhne tisíckrát a pokaždé se
   samo se sebou sčítá, takže intenzita v prstenci je obrovská.
2. Tak silné pole rozkmitá elektrony v křemíku nelineárně (nelinearita třetího řádu, $\chi^{(3)}$). Díky tomu
   mohou dva fotony laseru spontánně zaniknout a vytvořit **nový pár fotonů** – *spontánní čtyřvlnné směšování*.
   Jeden má trochu vyšší energii („modrý“), druhý nižší („červený“); vznikají spolu, v korelovaném stavu.
3. Za rezonátorem **odrazný filtr** vrátí zbytek laseru i červený foton a dál do čipu pustí jen modrý („signální“).

Každý pulz laseru otevírá jeden takt hodin – časové okno řádově pikosekund.

**Háček.** Pár vznikne jen zřídka – podle videa zhruba jednou na milion fotonů laseru. Hodiny by tikaly nepravidelně
a pomalu. A zvýšit výkon nejde donekonečna: s vyšší pravděpodobností páru roste i šance, že vzniknou dva páry
najednou, a to je chyba (*vlastní poznámka*, stejný problém jako u sestupné konverze v
[přednášce](/fotonika/prednaska-walther-2022#walther-hardware)).
""",
    further_reading=(
        Reading(MILES_VIDEO, "od 6:03"),
        Reading(SILVERSTONE_2014, "zdroje fotonových párů na křemíkovém čipu"),
    ),
)

CLOCK_TOPIC = TheoryTopic(
    anchor="psiv-hodiny",
    title="Kvantové hodiny: ohlašování a multiplexování",
    in_short=(
        "Mnoho zdrojů vedle sebe a druhý foton z páru jako „hlásný“: když ho detektor zachytí, víme, že jeho dvojče "
        "existuje, a rychlý přepínač pošle právě tenhle zdroj do výpočtu. Ze zdrojů, které fungují náhodně, jsou "
        "hodiny."
    ),
    explanation=r"""
**Multiplexování.** PsiQuantum zdroj zopakuje mnohokrát vedle sebe. V každém taktu se pak najde zdroj, který foton
vyrobil, a jen jeho dráha se připojí na „světočáru“ (*world line*) – hlavní vlnovod, který vede do výpočtu. Ostatní
dráhy končí slepě, aby do výpočtu nevlétly dva fotony najednou.

*Vlastní výpočet, proč to funguje:* má-li jeden zdroj v taktu pravděpodobnost $p$, že vyrobí foton, pak aspoň jeden
z $N$ zdrojů uspěje s pravděpodobností

$$
P = 1 - (1 - p)^N .
$$

Při $p = 5\,\%$ stačí na 99 % taktů $N = 90$ zdrojů, při $p = 10\,\%$ jen 44. Malé $p$ je přitom nutné kvůli šumu
dvou párů – proto jsou zdrojů stovky a proto je klíčová vyrobitelnost.

**Jak poznat, který zdroj uspěl, bez zničení fotonu.** Kvantová „hlava 22“: stav částice poznáme jen měřením, a měření
ji zničí. Řešení přišlo z toho, co dřív překáželo – pár má **dva** fotony. Druhý (červený) se místo zahození
detekuje: jeho cvaknutí ohlásí, že signální foton existuje, aniž bychom se ho dotkli. Ve firmě mu nejdřív říkali
„obětní foton“, po „krizové interní poradě o PR“ **ohlašovací** (*heralding*). Je to stejný princip jako u ohlašovaných
zdrojů v [přednášce](/fotonika/prednaska-walther-2022#walther-hardware) a na stránce o
[GHZ stavech](/fotonika/prednaska-walther-2022/ghz-stavy#ghz-dnes).
""",
    further_reading=(Reading(MILES_VIDEO, "od 9:00"),),
)

DETECTOR_TOPIC = TheoryTopic(
    anchor="psiv-detektory",
    title="Detekce jednotlivých fotonů",
    in_short=(
        "Supravodivý nanodrát z nitridu niobu (100 nm) těsně pod kritickým proudem: jeden foton rozbije "
        "Cooperovy páry, "
        "kousek drátu přestane být supravodivý a vznikne puls o několika milivoltech. Na čipu přes 93 %, další "
        "generace kolem 99 %."
    ),
    explanation=r"""
Ohlašovací foton je potřeba spolehlivě zachytit – a detekce jediného fotonu je sama o sobě těžká. Detektor musí
„balancovat na ostří nože“ mezi dvěma stavy. Princip vysvětluje Jonathan Matthews, ředitel pro nové technologie
PsiQuantum. Firma používá **supravodivé nanodrátkové detektory (SNSPD)**:

1. Nanodrát z **nitridu niobu** široký asi **100 nm** je ochlazený pod kritickou teplotu, odpor je nulový
   a elektrony tvoří **Cooperovy páry**.
2. Drátem teče proud těsně pod hodnotou, při které by supravodivost zanikla.
3. Dopadne-li foton, jeho energie v malé oblasti rozbije část Cooperových párů, kousek drátu přestane být supravodivý
   a vznikne napěťový puls **několika milivoltů** – „cvaknutí“.
4. Celé to trvá asi **nanosekundu**, pak se drát znovu ochladí a je připravený na další foton.

Fyzika je známá dávno (slajd o detektorech je i v [přednášce](/fotonika/prednaska-walther-2022#walther-hardware)); nové
je, že detektory musí být integrované přímo na křemíkovém čipu, zarovnané s vlnovody na nanometry, stejné v tisících
kusů a zachytit prakticky každý foton. Podle týmu mají detektory na čipu už **přes 93 %** a další generace **kolem
99 %** – a ani to podle Milese na plnou vizi nestačí.

*Vlastní výpočet, proč na tom tolik záleží:* projde-li výpočtem 50 fotonů a každý detektor zachytí 93 %, zachytí se
všechny jen s pravděpodobností asi 2,7 %; při 99 % je to asi 61 %. Proto se ve fotonice o každé desetině procenta
účinnosti bojuje.
""",
    further_reading=(
        Reading(MILES_VIDEO, "od 11:54"),
        Reading(NATARAJAN_2012, "přehled SNSPD"),
    ),
)

BTO_TOPIC = TheoryTopic(
    anchor="psiv-bto",
    title="Dokonalý materiál: titaničitan barnatý",
    in_short=(
        "Přepínač musí přesměrovat foton dřív, než doletí na konec zdrojové dráhy. Umí to titaničitan barnatý (BTO): "
        "napětí změní jeho index lomu (Pockelsův jev) za zlomky nanosekundy. Naučit BTO růst na křemíku trvalo přes "
        "deset let."
    ),
    explanation=r"""
Řetězec „detekce ohlašovacího fotonu → elektronický signál → přepnutí zdrojové dráhy na světočáru“ musí proběhnout
dřív, než signální foton doletí na konec zdrojové dráhy. To vyžaduje přepínač o řády rychlejší než běžné optické
součástky.

**Pockelsův jev.** **Titaničitan barnatý (BTO)** je feroelektrický krystal: kladné a záporné náboje v jeho mřížce jsou
trochu posunuté a materiál má vlastní elektrickou polarizaci. Přiložené napětí atomy nepatrně posune, změní vnitřní
pole i **index lomu** – a tím rychlost fotonu. V interferometru taková změna fáze přesune foton z jedné dráhy do
druhé. U BTO jde o změny rychlé, lokální a opakovatelné až na gigahertzových frekvencích.

**Proč to trvalo deset let.** Křemík má pravidelnou krystalovou mřížku, BTO jinou; růst přímo na křemíku vede k pnutí,
prasklinám a ztrátě elektrooptických vlastností. Součástky navíc musí přežít ochlazení z pokojové teploty na 2 K.
PsiQuantum vyvinul vrstvení s postupným přechodem křemík → oxid → BTO, s atomy nanášenými po vrstvách ve vlastním
zařízení; podle Milese „trochu černá magie“ s tisíci iterací. Tam, kde přepínač nestihne, pomůže krátké zpoždění
signální dráhy – ale jen minimální, protože každé zpoždění znamená ztráty.

*Vlastní poznámka:* Miles BTO označuje za „nejrychleji přepínající materiál, jaký lidstvo vyrobilo“ – to je spíš
nadsázka; podstatné je, že BTO kombinuje rychlost s malými ztrátami a jde integrovat na křemík. Podrobnosti
o materiálu popisuje práce o Pockelsově jevu v BTO na křemíku (Abel a kol., 2019).
""",
    further_reading=(
        Reading(MILES_VIDEO, "od 15:00"),
        Reading(ABEL_2019, "Pockelsův jev v BTO na křemíku"),
        Reading(PSIQUANTUM_OMEGA, "článek, ve kterém PsiQuantum přepínače z BTO popisuje"),
    ),
)

MATH_TOPIC = TheoryTopic(
    anchor="psiv-matematika",
    title="Jak počítat se světlem – a v jakém chladu",
    in_short=(
        "Machův–Zehnderův interferometr s ovladatelnou fází je základní hradlo; síť interferometrů je programovatelný "
        "obvod. Topení je pomalé, proto i tady BTO. Detektory vyžadují 2 K – kryostaty Mark II jsou čtyřmetrové "
        "a chlazené heliem."
    ),
    explanation=r"""
**Machův–Zehnderův interferometr.** Dva děliče 50 : 50 za sebou. Bez zásahu foton vyjde, jako by se nic nestalo;
zpozdí-li se ale jedna polovina vlnové funkce (fázový posun), pravděpodobnosti na výstupu se změní. Klasicky se fáze
nastavuje **topením** – teplejší křemík má vyšší index lomu (termooptický jev). Síť mnoha interferometrů je
**programovatelný optický obvod**, fotonická obdoba hradel. (Výpočet pravděpodobností $\sin^2(\varphi/2)$
a $\cos^2(\varphi/2)$ je v [přednášce](/fotonika/prednaska-walther-2022#walther-hardware).)

**Proč topení nestačí.** Ohřát a ochladit křemík trvá mikrosekundy až milisekundy – pro foton věčnost; teplo navíc
prosakuje k sousedním interferometrům a malé drifty se sčítají. Miles vzpomíná, jak doktorandi ve svých laboratořích
nadávali na křehké rané čipy. PsiQuantum proto stejný BTO, který přepíná zdroje, používá i k řízení interferometrů.

**Výsledek výpočtu.** Na konci všech drah jsou detektory; foton se najde jen v jednom, s pravděpodobností danou
obvodem. Výpočet se opakuje mnohokrát a odpověď je výsledek, který v rozdělení převládá.

**Chlazení.** Kvůli detektorům běží celý systém v **kryostatech „Mark II“** – čtyřmetrových ocelových skříních. Čipy
jsou na svislých „čepelích“ ve vysokém vakuu, kolem jsou vrstvy tepelného a elektromagnetického stínění. Kapalné
helium proudí od zásobníku vzhůru kolem čepelí a po několika minutách se odvádí, znovu zkapalňuje a vrací.

- **Dnes 2 K**, cílem pro masové nasazení jsou **4 K**.
- Supravodivé qubity potřebují kolem **20 mK** – 2 K je tedy **stokrát** tepleji, a u absolutní nuly je odvod tepla
  exponenciálně těžší (pár mikrowattů navíc přetíží systém na 20 mK).
- Méně energie na chlazení je podle Milese podmínka, aby šlo uvažovat o milionech qubitů, ne desítkách.

*Oprava na naší stránce:* stránka o PsiQuantum uváděla „kolem 4 K“; podle videa je to dnes 2 K a 4 K je cíl.
""",
    further_reading=(
        Reading(MILES_VIDEO, "od 18:19"),
        Reading(LINDE_CRYOPLANT, "heliový kryosystém pro australskou stavbu"),
    ),
)

SCALE_TOPIC = TheoryTopic(
    anchor="psiv-skalovani",
    title="Jak postavit škálovatelný počítač",
    in_short=(
        "Na čip se vejde jen omezeně obvodů a do kryostatu jen omezeně čipů. Užitečný počítač proto musí přenášet "
        "kvantový stav z čipu na čip, aniž by ho zničil – a právě to je „poslední skok“."
    ),
    explanation=r"""
Informace qubitu není ve světle samotném, ale v **přesném fázovém vztahu** mezi dvěma částmi stavu fotonu (dvěma
drahami). Ten je citlivý na každý rozdíl mezi drahami. Kdyby se obě dráhy vyvedly do dvou optických vláken a vedly
k dalšímu čipu, změny teploty, rozdíly délek vláken a otřesy by fázi rozhodily a qubit by zanikl.

Je to stejný problém, jaký má každá fyzikální platforma s propojováním modulů – jen u fotonů je řešitelný elegantně,
protože foton je sám nosičem, který cestuje (viz další kapitola). Firma interně mluví o projektu „Quantum Leap“.
""",
    further_reading=(Reading(MILES_VIDEO, "od 21:45"),),
)

TIME_TOPIC = TheoryTopic(
    anchor="psiv-cas",
    title="Převod prostoru na čas",
    in_short=(
        "Qubit ve dvou drahách se převede na qubit ve dvou časových okamžicích vzdálených 1 ns. Obě části pak letí "
        "stejným vláknem, takže je pomalé změny teploty a délky ovlivní stejně a fázový vztah přežije. Na druhém čipu "
        "se převod obrátí."
    ),
    explanation=r"""
**Převodník prostor → čas.** Foton na děliči svazku vstoupí do dvou drah, z nichž jedna je delší o zhruba **1 ns**.
Pro světlo to jsou desítky centimetrů (*vlastní výpočet:* ve vakuu 30 cm, ve vlnovodu s indexem kolem 2 asi 15 cm),
proto na čipu dlouhé spirály. Obě dráhy se pak spojí do **jednoho vlákna**: z qubitu „dráha 0 / dráha 1“ je qubit
„dřív / později“ – **časové kódování** (*time-bin*), známé z kvantové komunikace.

**Proč to funguje.** Tepelné změny, posuny délky vlákna a otřesy jsou o mnoho řádů pomalejší než 1 ns. Obě časové
části fotonu tedy zažijí prakticky stejné poruchy, jejich fázový vztah se nezmění a qubit dorazí neporušený. Na
druhém čipu stejný obvod pozpátku převede časové kódování zpět na dvě dráhy. Podle Jonathana Frazera, inženýra
experimentálních kvantových systémů, změřili věrnost „daleko přes 99 %“ – a podle Milese je to schopnost, kterou jiné
platformy skoro nemají.

*Vlastní poznámka:* fyzikálně je to stejný důvod, proč se v [doplňku o
dekoherenci](/fotonika/prednaska-walther-2022#walther-provazani)
uvádí kódování do času jako ochrana proti driftu ve vláknech.
""",
    further_reading=(
        Reading(MILES_VIDEO, "od 24:27"),
        Reading(BRENDEL_1999, "časové kódování v kvantové komunikaci"),
    ),
)

DEMONSTRATOR_TOPIC = TheoryTopic(
    anchor="psiv-demonstrator",
    title="První demonstrátor: qubit tunelem mezi laboratořemi",
    in_short=(
        "Dva čipy v samostatných kryostatech spojené 250 m vlákna v tunelu pod laboratořemi: zdroj, ohlášení, BTO "
        "přepínač, qubit, převod na čas, vlákno, převod zpět, detektory. Věrnost přeneseného stavu 99,7 %."
    ),
    explanation=r"""
Miles prochází tunelem, kterým vede vlákno, a pak celý experiment krok za krokem:

1. **První čip:** laserový pulz v prstencových rezonátorech vyrobí pár fotonů; filtr pošle červený na detektor.
2. Detekce ohlašovacího fotonu přepne **přepínač z BTO** a zdrojová dráha se připojí na světočáru.
3. Interferometr z fotonu udělá **qubit ve dvou drahách**, převodník ho změní na **časový qubit** (jedna polovina
   rovnou do vlákna, druhá přes zpoždění 1 ns).
4. Qubit proletí **asi 250 m** standardního jednovidového vlákna do druhého kryostatu.
5. **Druhý čip** převede časový qubit zpět na dvě dráhy, každou zakončenou supravodivým detektorem.

Ve zjednodušeném uspořádání zůstalo rozdělení přesně 50 : 50 – fázový vztah se nezměnil. Podle článku firmy se
přenesený stav shodoval s původním s **věrností 99,7 %** (v Nature 2025 je to 99,72 %). Podle Milese právě tohle
číslo dělá z PsiQuantum jednu z nejslibnějších firem: kvantový počítač nemusí žít na jednom čipu ani v jednom kryostatu.

*Vlastní kontrola čísel:* Miles uvádí, že qubit proletí „délku tří fotbalových hřišť za 800 ns“. Ve vlákně s indexem
lomu asi 1,47 je ale 250 m na asi 1,2 µs a za 800 ns světlo urazí jen asi 163 m – jedno z čísel ve videu je tedy
zaokrouhlené nebo nepřesné.

**Vize.** Modul (kryostat) s tisíci generátory qubitů, moduly propojené vlákny „stejně, jako je váš dům připojený
k telefonní ústředně“; škálování jako u datových center. Každý Mark II pojme mnoho čipů – zdroje, výpočet, detekce.
Stavby v **Austrálii** a v **Chicagu** mají mít stovky kryostatů se stovkami čipů. Miles končí tím, že trvalo deset let
a může trvat dalších deset, než přijde něco opravdu převratného.
""",
    further_reading=(
        Reading(MILES_VIDEO, "od 27:25"),
        Reading(PSIQUANTUM_OMEGA, "propojení čipů s věrností 99,72 %"),
    ),
)

CRITICAL_TOPIC = TheoryTopic(
    anchor="psiv-kriticky",
    title="Kriticky: co video neříká",
    in_short=(
        "Video je výborný průvodce součástkami, ale natočené s přístupem a se souhlasem firmy. Nepadne v něm, kolik "
        "fotonů se ztratí, že věrnosti platí jen pro fotony, které dorazily, ani kdy bude stroj hotový."
    ),
    explanation=r"""
*Celá kapitola je náš pohled, ne obsah videa.*

- **Ztráty.** Věrnost 99,7 % platí pro fotony, které **dorazily** a byly detekované; kolik se jich cestou ztratilo,
  video neříká. Pro fúzní architekturu je ale rozhodující právě ztráta (asi 2,7 % na foton, viz
  [plán PsiQuantum](/fotonika-ve-svete/psiquantum#psiq-plan) a [doplněk o
  dekoherenci](/fotonika/prednaska-walther-2022#walther-provazani)).
- **Chybí celý systém.** Ukázané jsou součástky a propojení dvou čipů. Generátor zdrojových stavů, fúze ve velkém ani
  logický qubit ve videu nejsou – stejně jako ve veřejných výsledcích firmy
  ([co je ukázané](/fotonika-ve-svete/psiquantum#psiq-omega)).
- **Termíny.** Australská i chicagská stavba jsou zmíněné jako „oznámené“, bez dat; jak se termíny posouvají, je na
  [stránce o PsiQuantum](/fotonika-ve-svete/psiquantum#psiq-kde-a-kdy).
- **Nadsázky.** „Fotony nedekoherují“, „qubity z hmoty vydrží nanosekundy“ a „nejrychlejší přepínací materiál“ jsou
  zjednodušení (kapitoly 2 a 6); čas letu 800 ns neodpovídá 250 m vlákna (kapitola 10).
- **Co je přínosné.** Konkrétní řešení pro zdroje (multiplexované ohlašování), přepínače (BTO), chlazení (2 K) a hlavně
  **převod prostoru na čas**, který vysvětluje, jak se má fotonický počítač skládat z modulů.
""",
    further_reading=(Reading(PSIQUANTUM_OMEGA),),
)

TOPICS: Tuple[TheoryTopic, ...] = (
    INTRO_TOPIC, LIGHT_TOPIC, SOURCE_TOPIC, CLOCK_TOPIC, DETECTOR_TOPIC, BTO_TOPIC, MATH_TOPIC, SCALE_TOPIC,
    TIME_TOPIC, DEMONSTRATOR_TOPIC, CRITICAL_TOPIC,
)

CHAPTER_TIMES: Tuple[ChapterTime, ...] = (
    ChapterTime(INTRO_TOPIC.anchor, 0),
    ChapterTime(LIGHT_TOPIC.anchor, 98),
    ChapterTime(SOURCE_TOPIC.anchor, 363),
    ChapterTime(CLOCK_TOPIC.anchor, 540),
    ChapterTime(DETECTOR_TOPIC.anchor, 714),
    ChapterTime(BTO_TOPIC.anchor, 900),
    ChapterTime(MATH_TOPIC.anchor, 1099),
    ChapterTime(SCALE_TOPIC.anchor, 1305),
    ChapterTime(TIME_TOPIC.anchor, 1467),
    ChapterTime(DEMONSTRATOR_TOPIC.anchor, 1645),
)
"""The video's own chapters; the sponsor segment between 648 and 714 s belongs to none. The last topic is ours."""

SLIDES: Tuple[LectureSlide, ...] = (
    LectureSlide(
        "slajd_0005.jpg", "Vizualizace budovy PsiQuantum s řadami kryostatů – cílová podoba kvantového datacentra",
    ),
    LectureSlide(
        "slajd_0010.jpg", "Tisková zpráva: PsiQuantum získal 1 mld. USD (Series E) na stavby v Brisbane a Chicagu",
    ),
    LectureSlide("slajd_0012.jpg", "Vizualizace: řady racků a kryostatů propojených potrubím"),
    LectureSlide("slajd_0026.jpg", "Uvnitř kryostatu: pozlacené stupně, kabely a vlnovce"),
    LectureSlide("slajd_0036.jpg", "Kryostat PsiQuantum – provozní teplota 2 K"),
    LectureSlide("slajd_0126.jpg", "Křemíková deska (wafer) v přepravním pouzdře"),
    LectureSlide("slajd_0132.jpg", "Dr Ben Burridge, vedoucí zdrojů světla v PsiQuantum"),
    LectureSlide("slajd_0150.jpg", "Mikrofotografie čipu: mřížka, prstence, kontaktní plocha"),
    LectureSlide("slajd_0170.jpg", "Vizualizace fotonického čipu: vlnovody, prstencové rezonátory, spojky"),
    LectureSlide("slajd_0174.jpg", "Čipové moduly montované do kryogenního držáku"),
    LectureSlide("slajd_0178.jpg", "Řídicí deska PsiQuantum (budiče přepínačů, FPGA) s kapalinovým chlazením"),
    LectureSlide("slajd_0190.jpg", "Animace: foton (žlutá kulička) ve vlnovodu"),
    LectureSlide("slajd_0249.jpg", "Prof. Mark Thompson, spoluzakladatel a technický ředitel PsiQuantum"),
    LectureSlide("slajd_0254.jpg", "Mapa reliktního záření – Thompsonův argument, že fotony nedekoherují (záběr BBC)"),
    LectureSlide("slajd_0328.jpg", "Svazek optických vláken – fotony jako nosič informace mezi moduly"),
    LectureSlide("slajd_0367.jpg", "Pulzní laser na optickém stole (pumpa)"),
    LectureSlide("slajd_0405.jpg", "Náčrt zdroje na tabuli: řada prstenců, filtrace, detektor (2,5–6 K)"),
    LectureSlide("slajd_0424.jpg", "Celá tabule „Single Photon Source“: prstence, filtr, detektor"),
    LectureSlide("slajd_0484.jpg", "Animace: korelovaný pár fotonů ze čtyřvlnného směšování"),
    LectureSlide("slajd_0552.jpg", "Multiplexování: čtyři vlnovody, každý se čtyřmi prstencovými rezonátory"),
    LectureSlide("slajd_0612.jpg", "Schéma ohlašování: rezonátory, filtr, odbočka k detektoru"),
    LectureSlide("slajd_0630.jpg", "Ohlašovací foton míří k detektoru"),
    LectureSlide("slajd_0732.jpg", "Prof. Jonathan Matthews, ředitel pro nové technologie PsiQuantum"),
    LectureSlide("slajd_0763.jpg", "Animace: vrstva nitridu niobu – materiál detektoru"),
    LectureSlide("slajd_0769.jpg", "Levitace magnetu nad supravodičem – co znamená supravodivost"),
    LectureSlide("slajd_0838.jpg", "Testovací optická lavice s čipem PsiQuantum"),
    LectureSlide("slajd_0842.jpg", "Rack s vlákny a pouzdřenými čipy"),
    LectureSlide("slajd_0854.jpg", "Měděný držák s deskou a navinutým vláknem"),
    LectureSlide("slajd_0861.jpg", "Testovací deska s optickým přepínačem (interferometr) a vláknem"),
    LectureSlide("slajd_0890.jpg", "Animace přepínače: foton poslaný do jedné ze dvou drah"),
    LectureSlide("slajd_0904.jpg", "Čistá místnost: vzorky materiálu pro růst BTO"),
    LectureSlide("slajd_0975.jpg", "Barevné čipy – výsledek výroby"),
    LectureSlide("slajd_0987.jpg", "Manipulace s deskou v čisté místnosti"),
    LectureSlide("slajd_0991.jpg", "Animace: pravidelná krystalová mřížka"),
    LectureSlide("slajd_1002.jpg", "Animace: vrstvení dvou různých krystalových mřížek – problém růstu BTO na křemíku"),
    LectureSlide("slajd_1011.jpg", "Ochlazování čipu: teplota v kelvinech v čase (hodiny)"),
    LectureSlide("slajd_1064.jpg", "Náčrt na tabuli: fotony, filtrace, detektor 2,5–4 K a stavy |0⟩, |1⟩"),
    LectureSlide(
        "slajd_1087.jpg",
        "Článek PsiQuantum o platformě Omega (arXiv 2024): věrnosti 99,98 %, 99,50 %, 99,22 %, 99,72 %",
    ),
    LectureSlide("slajd_1105.jpg", "Směrová spojka 50 : 50: foton vyjde každým ramenem s pravděpodobností 50 %"),
    LectureSlide("slajd_1139.jpg", "Machův–Zehnderův interferometr ze dvou spojek"),
    LectureSlide("slajd_1156.jpg", "Termokamera: zahřívaná součástka – proč je topení pomalé"),
    LectureSlide("slajd_1159.jpg", "Index lomu křemíku roste s teplotou (termooptický jev)"),
    LectureSlide("slajd_1219.jpg", "Síť interferometrů s fázovými posuvy pro pět vlnovodů"),
    LectureSlide("slajd_1295.jpg", "Kryostat je stíněný proti záření"),
    LectureSlide("slajd_1311.jpg", "Kryostat Mark II v testovací hale"),
    LectureSlide("slajd_1336.jpg", "Uvnitř kryostatu: svislé „čepele“ pro čipy"),
    LectureSlide("slajd_1356.jpg", "Řez kryostatem (vizualizace): rack s konektory a chladicí blok"),
    LectureSlide("slajd_1379.jpg", "Strojovna s heliovými nádržemi a potrubím"),
    LectureSlide("slajd_1400.jpg", "Pro srovnání: supravodivé qubity (IBM) při 20 mK"),
    LectureSlide("slajd_1414.jpg", "Vize: hala se stovkami stejných modulů (vizualizace)"),
    LectureSlide("slajd_1452.jpg", "Kryostat se vysunutými racky mezi servery"),
    LectureSlide("slajd_1535.jpg", "Převodník prostor → čas: foton před rozdělením"),
    LectureSlide("slajd_1551.jpg", "Čip pod mikroskopem: spirála zpožďovací dráhy"),
    LectureSlide("slajd_1557.jpg", "Spirálová zpožďovací dráha a spojení dvou drah do jedné"),
    LectureSlide("slajd_1571.jpg", "Dr Jonathan Frazer, inženýr experimentálních kvantových systémů"),
    LectureSlide("slajd_1617.jpg", "Časový qubit: dvě části fotonu za sebou v jednom vlnovodu"),
    LectureSlide("slajd_1624.jpg", "Zpětný převod čas → prostor na druhém čipu"),
    LectureSlide("slajd_1665.jpg", "Vstup do „kvantového tunelu“ s vláknem mezi laboratořemi"),
    LectureSlide("slajd_1682.jpg", "Animace demonstrátoru: zdroj fotonů na prvním čipu"),
    LectureSlide("slajd_1764.jpg", "Výsledky v Nature 2025: propojení čipů 99,72 %, bez započtení ztrát"),
    LectureSlide("slajd_1785.jpg", "Vizualizace modulu s čipy"),
    LectureSlide("slajd_1825.jpg", "Vizualizace haly s řadami kryostatů"),
    LectureSlide("slajd_1835.jpg", "Vizualizace areálu PsiQuantum u vody"),
    LectureSlide("slajd_1837.jpg", "Článek o plánu PsiQuantum v Brisbane (květen 2025)"),
    LectureSlide("slajd_1841.jpg", "Vizualizace budovy s přechodnými testovacími systémy"),
    LectureSlide("slajd_1856.jpg", "Pozlacený stupeň kryostatu s kabeláží"),
    LectureSlide("slajd_1906.jpg", "Ben Miles u velkého ocelového kryostatu"),
)
"""Informative frames; the sponsor segment, film clips, repeated and talking-head frames are left out."""


def chapter_start(anchor: str) -> int:
    return next(chapter.start for chapter in CHAPTER_TIMES if chapter.anchor == anchor)


def chapter_end(anchor: str) -> int:
    anchors = [chapter.anchor for chapter in CHAPTER_TIMES]
    index = anchors.index(anchor)
    end = CHAPTER_TIMES[index + 1].start if index + 1 < len(anchors) else VIDEO_SECONDS
    return SPONSOR_START if anchor == CLOCK_TOPIC.anchor else end


def chapter_slides(anchor: str) -> Tuple[LectureSlide, ...]:
    if anchor not in {chapter.anchor for chapter in CHAPTER_TIMES}:
        return ()
    start, end = chapter_start(anchor), chapter_end(anchor)
    return tuple(slide for slide in SLIDES if start <= slide.seconds < end)
