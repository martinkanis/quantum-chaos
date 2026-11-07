// Builds content/lectures/psiquantum-video-2026/prezentace.pptx from the notes on Ben Miles's video about PsiQuantum
// (ui/psiquantum_video_content.py) and its frames. pptxgenjs is not a dependency of the app:
//   npm install pptxgenjs && node scripts/psiquantum_video_presentation.js
const path = require("path");
const pptxgen = require("pptxgenjs");

const LECTURE_DIR = path.join(__dirname, "..", "content", "lectures", "psiquantum-video-2026");
const frame = (seconds) => path.join(LECTURE_DIR, "slajdy", `slajd_${seconds}.jpg`);
const OUTPUT = path.join(LECTURE_DIR, "prezentace.pptx");

const COLORS = {
  night: "0B1A2E", // dark background: an optics lab with the lights off
  ink: "1B2433",
  muted: "5A6578",
  laser: "E8462A", // accent: the pump laser
  cyan: "2BA6C2", // supporting tone: guided light
  mist: "EEF3F8", // card tint on white slides
  white: "FFFFFF",
};
const HEAD = "Cambria";
const BODY = "Calibri";
const W = 10;
const IMAGE_W = 4.6;
const IMAGE_H = (IMAGE_W * 9) / 16;

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Kvantový počítač ze světla – PsiQuantum zblízka";
pres.author = "Quantum Knowledge Base";
pres.theme = { headFontFace: HEAD, bodyFontFace: BODY };

pres.defineSlideMaster({
  title: "TITLE_DARK",
  background: { color: COLORS.night },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 1.4, w: 4.6, h: 1.6, fontFace: HEAD,
      fontSize: 36, bold: true, color: COLORS.white, valign: "top", align: "left" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 3.1, w: 4.6, h: 1.4, fontFace: BODY,
      fontSize: 16, color: "C9D6E6", valign: "top" }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: COLORS.white },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.3, w: 9, h: 0.75, fontFace: HEAD,
      fontSize: 30, bold: true, color: COLORS.ink, valign: "middle", align: "left" }, text: "" } },
    { text: { text: "PsiQuantum zblízka · zápisky z videa Bena Milese (2026)", options: { x: 0.5, y: 5.2, w: 6.5,
      h: 0.3, fontFace: BODY, fontSize: 10, color: COLORS.muted } } },
  ],
  slideNumber: { x: 9.0, y: 5.2, w: 0.5, h: 0.3, fontFace: BODY, fontSize: 10, color: COLORS.muted, align: "right" },
});

function image(slide, seconds, x, y, caption) {
  slide.addImage({ path: frame(seconds), x, y, w: IMAGE_W, h: IMAGE_H, objectName: `snimek-${seconds}`,
    shadow: { type: "outer", color: "000000", opacity: 0.25, blur: 6, offset: 2, angle: 90 } });
  if (caption) {
    slide.addText(caption, { x, y: y + IMAGE_H + 0.05, w: IMAGE_W, h: 0.45, fontFace: BODY, fontSize: 10,
      color: COLORS.muted, isTextBox: true, margin: 0, valign: "top" });
  }
}

function steps(slide, items, x, y, w) {
  items.forEach(([head, text], index) => {
    const top = y + index * 1.05;
    slide.addShape(pres.shapes.OVAL, { x, y: top, w: 0.42, h: 0.42, fill: { color: COLORS.laser },
      line: { color: COLORS.laser }, objectName: `krok-${index + 1}` });
    slide.addText(String(index + 1), { x, y: top, w: 0.42, h: 0.42, fontFace: HEAD, fontSize: 16, bold: true,
      color: COLORS.white, align: "center", valign: "middle", isTextBox: true, margin: 0 });
    slide.addText([
      { text: head, options: { bold: true, color: COLORS.ink, breakLine: true } },
      { text, options: { color: COLORS.muted } },
    ], { x: x + 0.6, y: top - 0.05, w: w - 0.6, h: 0.95, fontFace: BODY, fontSize: 14, valign: "top",
      isTextBox: true, margin: 0 });
  });
}

function stat(slide, value, label, x, y, w) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 1.25, fill: { color: COLORS.mist },
    line: { color: COLORS.mist }, rectRadius: 0.08, objectName: `cislo-${value}` });
  slide.addText(value, { x: x + 0.2, y: y + 0.1, w: w - 0.4, h: 0.65, fontFace: HEAD, fontSize: 32, bold: true,
    color: COLORS.laser, isTextBox: true, margin: 0 });
  slide.addText(label, { x: x + 0.2, y: y + 0.75, w: w - 0.4, h: 0.45, fontFace: BODY, fontSize: 12,
    color: COLORS.ink, isTextBox: true, margin: 0, valign: "top" });
}

function card(slide, head, text, x, y, w, h) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: COLORS.mist },
    line: { color: COLORS.mist }, rectRadius: 0.08, objectName: `karta-${head}` });
  slide.addText([
    { text: head, options: { bold: true, color: COLORS.ink, fontSize: 16, breakLine: true } },
    { text, options: { color: COLORS.muted, fontSize: 13 } },
  ], { x: x + 0.2, y: y + 0.15, w: w - 0.4, h: h - 0.3, fontFace: BODY, valign: "top", isTextBox: true,
    margin: 0, paraSpaceAfter: 4 });
}

function content(section, title, notes) {
  const slide = pres.addSlide({ masterName: "CONTENT", sectionTitle: section });
  slide.addText(title, { placeholder: "title" });
  slide.addNotes(notes);
  return slide;
}

// 1 Title
pres.addSection({ title: "Úvod" });
let slide = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Úvod" });
slide.addText("Kvantový počítač ze světla", { placeholder: "title" });
slide.addText("PsiQuantum zblízka – zápisky z videa Bena Milese „The Genius of Computing with Light“ (2026)",
  { placeholder: "body" });
slide.addImage({ path: frame("0036"), x: 5.4, y: 1.3, w: IMAGE_W, h: IMAGE_H, objectName: "titulni-snimek" });
slide.addText("Kryostat PsiQuantum, provozní teplota 2 K", { x: 5.4, y: 1.3 + IMAGE_H + 0.05, w: IMAGE_W, h: 0.4,
  fontFace: BODY, fontSize: 10, color: "9FB0C6", isTextBox: true, margin: 0 });
slide.addNotes("Video fyzika Bena Milese z laboratoří PsiQuantum (únor 2026, 32 minut). Prochází součástky "
  + "fotonického počítače jednu po druhé. Na konci je náš kritický pohled. Podrobné zápisky jsou v aplikaci "
  + "Quantum Knowledge Base na stránce PsiQuantum.");

// About the video
pres.addSection({ title: "Úvod" + "​" });
slide = content("Úvod" + "​", "O videu a autorovi",
  "Ben Miles dělal doktorát z optické fyziky v Bristolu, v budově, odkud PsiQuantum vzešel. Pět let firmu "
  + "přemlouval, aby ho pustila dovnitř. Podle svých slov video firma neplatí; sponzorem je Shortform. Zajímají ho "
  + "součástky, ne algoritmy.");
steps(slide, [
  ["Ben Miles", "fyzik a youtuber, doktorát v Bristolu vedle budoucích zakladatelů"],
  ["Pět let přemlouvání", "první natáčení uvnitř jedné z nejtajnějších kvantových firem"],
  ["Téma: součástky", "zdroje, detektory, přepínače, chlazení, propojení čipů"],
], 0.5, 1.4, 4.4);
image(slide, "1906", 5.1, 1.3, "Ben Miles u kryostatu PsiQuantum");

// 2 Why photons
pres.addSection({ title: "Součástky" });
slide = content("Součástky", "Proč počítat se světlem",
  "Mark Thompson, spoluzakladatel PsiQuantum, uvádí dva důvody. Fotony téměř nedekoherují, protože s okolím "
  + "skoro neinteragují. A cestují, takže propojí moduly. Výhrada: ionty a atomy drží koherenci i sekundy a "
  + "skutečnou chybou fotonů je ztráta.");
card(slide, "Skoro nedekoherují", "S okolím téměř neinteragují a fungují i za pokojové teploty. Hlavní chybou "
  + "není dekoherence, ale ztráta – foton zmizí.", 0.5, 1.3, 4.2, 1.7);
card(slide, "Cestují", "Velký počítač nebude na jednom čipu. Fotony jsou přirozený způsob, jak přenášet "
  + "kvantovou informaci mezi moduly vláknem.", 0.5, 3.15, 4.2, 1.7);
image(slide, "0254", 5.1, 1.3, "Thompsonův argument: polarizace reliktního záření přežila miliardy let (záběr BBC)");

// Decoherence versus loss
slide = content("Součástky", "Dekoherence, nebo ztráta?",
  "Tepelný šum: v módu telekomunikačního fotonu při pokojové teplotě je jen asi 3,7 krát deset na minus čtrnáctou "
  + "tepelných fotonů, u supravodivého qubitu na pěti gigahertzech asi 1 250, proto se chladí na deset milikelvinů. "
  + "Fotony tedy prakticky nedekoherují, jejich chybou je ztráta. Výpočty jsou v zápiscích k Waltherově přednášce.");
stat(slide, "3,7 · 10⁻¹⁴", "tepelných fotonů v módu 1 550 nm při 300 K (vlastní výpočet)", 0.5, 1.35, 4.3);
stat(slide, "≈ 1 250", "tepelných fotonů v módu supravodivého qubitu 5 GHz při 300 K", 0.5, 2.8, 4.3);
image(slide, "0328", 5.1, 1.3, "Skutečnou chybou fotonů je ztráta – foton se ve vlákně nebo na čipu ztratí");

// Wafers
slide = content("Součástky", "Kvantový čip z běžné továrny",
  "Čipy vyrábí GlobalFoundries na 300mm deskách stejnou litografií jako běžnou elektroniku. Vlnovody jsou "
  + "hřebínky široké asi sto nanometrů. Hotové čipy se montují do modulů v kryostatu.");
steps(slide, [
  ["300mm desky", "stejná technologie jako u běžných čipů – podmínka pro miliony qubitů"],
  ["Vlnovody ~100 nm", "vedou světlo díky vyššímu indexu lomu než okolí"],
  ["Moduly v kryostatu", "čipy na deskách s vlákny a řídicí elektronikou"],
], 0.5, 1.4, 4.4);
image(slide, "0174", 5.1, 1.3, "Čipové moduly montované do kryogenního držáku");

// 3 Qubit
slide = content("Součástky", "Qubit je dráha fotonu",
  "Čipy se vyrábějí na 300mm křemíkových deskách stejně jako běžná elektronika. Vlnovody vedou světlo jako "
  + "optické vlákno. Foton v horní dráze je nula, v dolní jednička. Dělič 50 : 50 vyrobí superpozici.");
steps(slide, [
  ["Křemíkový čip", "300mm desky, vlnovody vyleptané běžnou litografií"],
  ["Dvě dráhy = jeden qubit", "foton v jedné dráze je |0⟩, v druhé |1⟩"],
  ["Dělič 50 : 50", "přiblížené vlnovody: foton je v obou drahách současně"],
], 0.5, 1.4, 4.4);
image(slide, "0170", 5.1, 1.3, "Vizualizace čipu: vlnovody, prstencové rezonátory a spojky");

// 4 Source
slide = content("Součástky", "Jak vyrobit jeden foton",
  "Laserové pulzy na 1 550 nm krouží v prstencových rezonátorech. Nelinearita křemíku občas promění dva fotony "
  + "laseru v pár nových fotonů, modrý a červený. Filtr pustí dál jen modrý. Pravděpodobnost je zhruba jedna "
  + "ku milionu.");
steps(slide, [
  ["Pumpa 1 550 nm", "krátké laserové pulzy, každý otevírá takt hodin"],
  ["Prstencový rezonátor", "čtyřvlnné směšování vyrobí pár fotonů"],
  ["Filtr", "dál jde jen signální foton, zbytek laseru se odrazí"],
], 0.5, 1.4, 4.4);
image(slide, "0405", 5.1, 1.3, "Náčrt zdroje na tabuli: prstence, filtrace, detektor");

// Correlated pair
slide = content("Součástky", "Jak vzniká pár fotonů",
  "V prstenci světlo oběhne tisíckrát a pole je tak silné, že křemík reaguje nelineárně. Dva fotony laseru se "
  + "spontánně promění v pár: jeden s trochu vyšší energií, modrý, druhý s nižší, červený. Pravděpodobnost je "
  + "zhruba jedna ku milionu.");
card(slide, "Prstencový rezonátor", "Obvod je celistvým násobkem vlnové délky – světlo se tisíckrát sčítá samo "
  + "se sebou.", 0.5, 1.3, 4.2, 1.15);
card(slide, "Nelinearita χ⁽³⁾", "Čtyřvlnné směšování: dva fotony pumpy → modrý a červený foton.", 0.5, 2.6, 4.2, 1.0);
card(slide, "Jedna ku milionu", "Pár vznikne zřídka a náhodně – proto ohlašování a multiplexování.",
  0.5, 3.75, 4.2, 1.15);
image(slide, "0484", 5.1, 1.3, "Korelovaný pár fotonů ze čtyřvlnného směšování");

// 5 Heralding and multiplexing
slide = content("Součástky", "Ohlašování a multiplexování",
  "Druhý foton z páru se detekuje a ohlásí, že jeho dvojče existuje. Mnoho zdrojů vedle sebe: přepínač pošle do "
  + "výpočtu ten, který uspěl. Vlastní výpočet: s pravděpodobností 5 % na zdroj stačí 90 zdrojů na 99 % taktů.");
stat(slide, "90 zdrojů", "stačí na foton v 99 % taktů, když jeden uspěje s pravděpodobností 5 % (vlastní výpočet)",
  0.5, 1.35, 4.3);
card(slide, "Ohlašovací foton", "Detekce červeného fotonu ohlásí modrý, aniž bychom se ho dotkli. Rychlý přepínač "
  + "pak připojí jeho zdroj na hlavní vlnovod.", 0.5, 2.8, 4.3, 1.75);
image(slide, "0552", 5.1, 1.3, "Multiplexování: čtyři vlnovody, každý se čtyřmi rezonátory");

// Heralding photon
slide = content("Součástky", "Ohlašovací foton krok za krokem",
  "Kvantová hlava 22: stav poznáme jen měřením, ale měření foton zničí. Řešení: pár má dva fotony. Červený se "
  + "detekuje a ohlásí modrý. Ve firmě mu říkali obětní foton, po poradě o PR ohlašovací.");
steps(slide, [
  ["Pár vznikne", "modrý (signální) a červený foton současně"],
  ["Červený na detektor", "jeho cvaknutí ohlásí, že modrý existuje"],
  ["Přepínač připojí zdroj", "jen ten, který uspěl, jde na hlavní vlnovod"],
], 0.5, 1.4, 4.4);
image(slide, "0630", 5.1, 1.3, "Ohlašovací foton míří k detektoru");

// 6 Detectors
slide = content("Součástky", "Detekce jednotlivých fotonů",
  "Supravodivý nanodrát z nitridu niobu, široký asi 100 nanometrů, těsně pod kritickým proudem. Foton rozbije "
  + "Cooperovy páry a vznikne puls. Na čipu přes 93 procent, další generace 99. Vlastní výpočet: při 93 procentech "
  + "se všech 50 fotonů zachytí jen asi ve 2,7 procenta případů.");
stat(slide, "93 % → 99 %", "účinnost detektorů na čipu dnes a v další generaci", 0.5, 1.35, 4.3);
stat(slide, "2,7 %", "šance zachytit všech 50 fotonů při účinnosti 93 % (vlastní výpočet)", 0.5, 2.8, 4.3);
image(slide, "0763", 5.1, 1.3, "Vrstva nitridu niobu – materiál supravodivého detektoru");

// How the nanowire clicks
slide = content("Součástky", "Jak nanodrát cvakne",
  "Nanodrát z nitridu niobu je supravodivý a teče jím proud těsně pod kritickou hodnotou. Foton rozbije Cooperovy "
  + "páry, kousek drátu přestane být supravodivý a vznikne puls několika milivoltů. Za nanosekundu je drát zase "
  + "připravený.");
steps(slide, [
  ["Supravodivý drát", "nitrid niobu ~100 nm, proud těsně pod kritickou hodnotou"],
  ["Foton dopadne", "rozbije Cooperovy páry, kousek drátu přestane být supravodivý"],
  ["Puls a reset", "napětí několika mV, za ~1 ns připraveno na další foton"],
], 0.5, 1.4, 4.4);
image(slide, "0769", 5.1, 1.3, "Levitace nad supravodičem – co znamená supravodivost");

// 7 BTO
slide = content("Součástky", "BTO: přepínač rychlejší než foton",
  "Přepínač musí přesměrovat foton dřív, než doletí na konec zdrojové dráhy. Titaničitan barnatý mění index lomu "
  + "napětím, to je Pockelsův jev, až na gigahertzových frekvencích. Naučit ho růst na křemíku trvalo přes "
  + "deset let.");
steps(slide, [
  ["Pockelsův jev", "napětí změní index lomu a foton přejde do jiné dráhy"],
  ["Gigahertzové rychlosti", "topení na křemíku je o mnoho řádů pomalejší"],
  ["Deset let vývoje", "vrstvy křemík → oxid → BTO, aby krystal nepraskal"],
], 0.5, 1.4, 4.4);
image(slide, "1002", 5.1, 1.3, "Dvě různé krystalové mřížky na sobě – proč je růst BTO těžký");

// Why BTO took ten years
slide = content("Součástky", "Proč BTO trval deset let",
  "Křemík a titaničitan barnatý mají různé krystalové mřížky. Přímý růst vede k pnutí a prasklinám. Součástky navíc "
  + "musí přežít ochlazení z pokojové teploty na dva kelviny. PsiQuantum vyvinul postupné vrstvení a tisíce "
  + "iterací receptu.");
card(slide, "Různé mřížky", "Přímý růst na křemíku → pnutí, praskliny, ztráta elektrooptických vlastností.",
  0.5, 1.3, 4.2, 1.15);
card(slide, "Z 300 K na 2 K", "Extrémní teplotní cesta, kterou musí přežít každá vrstva.", 0.5, 2.6, 4.2, 1.0);
card(slide, "Vrstvení", "Křemík → oxid → BTO, atomy po vrstvách, tisíce iterací.", 0.5, 3.75, 4.2, 1.15);
image(slide, "1011", 5.1, 1.3, "Ochlazování čipu: teplota v kelvinech v čase");

// 8 Interferometers
slide = content("Součástky", "Počítání interferometry",
  "Machův–Zehnderův interferometr s ovladatelnou fází je základní hradlo. Síť interferometrů je programovatelný "
  + "obvod. Topení je pomalé a ovlivňuje sousedy, proto i tady BTO. Výpočet se opakuje a odpověď je výsledek, "
  + "který převládá.");
card(slide, "Machův–Zehnderův interferometr", "Dva děliče a fázový posun mezi nimi nastaví, kterým výstupem "
  + "foton vyjde.", 0.5, 1.3, 4.2, 1.15);
card(slide, "Síť interferometrů", "Programovatelný optický obvod – fotonická obdoba hradel.", 0.5, 2.6, 4.2, 1.0);
card(slide, "Topení vs. BTO", "Teplo mění fázi za mikro- až milisekundy a prosakuje k sousedům; BTO je rychlý "
  + "a lokální.", 0.5, 3.75, 4.2, 1.15);
image(slide, "1219", 5.1, 1.3, "Síť interferometrů s fázovými posuvy pro pět vlnovodů");

// Heat is slow
slide = content("Součástky", "Proč topení nestačí",
  "Teplejší křemík má vyšší index lomu, tak se klasicky nastavuje fáze. Ohřát a ochladit ho ale trvá mikrosekundy "
  + "až milisekundy a teplo prosakuje k sousedním interferometrům. Pro foton je to věčnost, proto i tady BTO.");
stat(slide, "µs – ms", "doba ohřátí a ochlazení křemíku – pro foton věčnost", 0.5, 1.35, 4.3);
card(slide, "Přeslech", "Teplo prosakuje k sousedům a malé drifty se sčítají přes celý obvod.", 0.5, 2.8, 4.3, 1.3);
image(slide, "1159", 5.1, 1.3, "Index lomu křemíku roste s teplotou (termooptický jev)");

// 9 Cooling
slide = content("Součástky", "Chlazení na 2 K",
  "Kvůli detektorům běží všechno v kryostatech Mark II při dvou kelvinech. Supravodivé qubity potřebují kolem "
  + "dvaceti milikelvinů, tedy stokrát méně. Cílem jsou čtyři kelviny. Méně energie na chlazení je podmínka "
  + "pro miliony qubitů.");
stat(slide, "2 K", "provozní teplota dnes; cílem pro nasazení ve velkém jsou 4 K", 0.5, 1.35, 4.3);
stat(slide, "100×", "tepleji než supravodivé qubity (kolem 20 mK)", 0.5, 2.8, 4.3);
image(slide, "1336", 5.1, 1.3, "Uvnitř kryostatu Mark II: svislé „čepele“ pro čipy");

// Inside the cryostat
slide = content("Součástky", "Kryostat Mark II zevnitř",
  "Čtyřmetrová ocelová skříň. Čipy na svislých čepelích ve vysokém vakuu, kolem vrstvy stínění. Kapalné helium "
  + "proudí kolem čepelí a po pár minutách se odvádí, znovu zkapalňuje a vrací.");
steps(slide, [
  ["Vakuum", "žádný vzduch, který by vedl teplo nebo rušil detektory"],
  ["Stínění", "tepelné a elektromagnetické vrstvy kolem čepelí"],
  ["Helium v oběhu", "proudí vzhůru, po pár minutách se znovu zkapalní"],
], 0.5, 1.4, 4.4);
image(slide, "1356", 5.1, 1.3, "Řez kryostatem (vizualizace): rack s konektory a chladicí blok");

// Why connect chips
pres.addSection({ title: "Škálování" });
slide = content("Škálování", "Proč propojovat čipy",
  "Na čip se vejde jen omezeně obvodů a do kryostatu jen omezeně čipů. Užitečný počítač proto musí přenášet "
  + "kvantový stav z čipu na čip. Qubit je ale v přesném fázovém vztahu dvou drah a ten rozhodí teplota, rozdíl "
  + "délek vláken i otřesy.");
card(slide, "Limit čipu a kryostatu", "Velký počítač bude modulární – jako datové centrum.", 0.5, 1.3, 4.2, 1.15);
card(slide, "Křehká fáze", "Dvě dráhy ve dvou vláknech: každá změna délky nebo teploty qubit zničí.",
  0.5, 2.6, 4.2, 1.15);
image(slide, "1414", 5.1, 1.3, "Vize: hala se stovkami stejných modulů (vizualizace)");

// 10 Space to time
slide = content("Škálování", "Převod qubitu z prostoru do času",
  "Qubit ve dvou drahách se převede na dva časové okamžiky vzdálené jednu nanosekundu. Obě části letí stejným "
  + "vláknem, pomalé poruchy je ovlivní stejně a fázový vztah přežije. Na druhém čipu se převod obrátí.");
steps(slide, [
  ["Rozdělení", "jedna dráha je delší o 1 ns – na čipu dlouhá spirála"],
  ["Jedno vlákno", "qubit „dřív / později“ – drift vlákna zasáhne obě části stejně"],
  ["Zpětný převod", "druhý čip vrátí qubit do dvou drah"],
], 0.5, 1.4, 4.4);
image(slide, "1557", 5.1, 1.3, "Spirálová zpožďovací dráha a spojení dvou drah do jedné");

// Why time-bin works
slide = content("Škálování", "Proč časový qubit přežije",
  "Obě části fotonu jsou od sebe jen nanosekundu. Změny teploty a délky vlákna jsou o mnoho řádů pomalejší, "
  + "takže zasáhnou obě části stejně a fázový vztah se nezmění. Ve vakuu urazí světlo za nanosekundu třicet "
  + "centimetrů, ve vlnovodu asi patnáct.");
stat(slide, "1 ns", "rozestup obou částí fotonu – poruchy jsou mnohem pomalejší", 0.5, 1.35, 4.3);
stat(slide, "≈ 30 cm", "dráha světla ve vakuu za 1 ns; na čipu proto dlouhé spirály", 0.5, 2.8, 4.3);
image(slide, "1617", 5.1, 1.3, "Časový qubit: dvě části fotonu za sebou v jednom vlnovodu");

// 11 Demonstrator
slide = content("Škálování", "Demonstrátor: qubit tunelem",
  "Dva čipy v samostatných kryostatech spojené 250 metry vlákna v tunelu. Věrnost přeneseného stavu 99,7 procenta, "
  + "v Nature 2025 99,72 procenta. Ve videu zazní 800 nanosekund, ale 250 metrů vlákna světlo proletí asi za "
  + "1,2 mikrosekundy – jedno z čísel je nepřesné.");
stat(slide, "99,7 %", "věrnost qubitu přeneseného 250 m vlákna mezi dvěma kryostaty", 0.5, 1.35, 4.3);
card(slide, "Kontrola čísel", "Ve videu „800 ns“, ale 250 m vlákna světlo proletí asi za 1,2 µs (vlastní "
  + "výpočet).", 0.5, 2.8, 4.3, 1.3);
image(slide, "1665", 5.1, 1.3, "Vstup do „kvantového tunelu“ s vláknem mezi laboratořemi");

// Demonstrator step by step
slide = content("Škálování", "Demonstrátor krok za krokem",
  "Zdroj s ohlašováním a přepínačem z BTO, interferometr vyrobí qubit, převodník ho změní na časový, 250 metrů "
  + "vlákna, druhý čip převede qubit zpět a supravodivé detektory ho změří. Rozdělení zůstalo 50 na 50.");
steps(slide, [
  ["Čip 1", "zdroj → ohlášení → přepínač BTO → qubit → převod na čas"],
  ["250 m vlákna", "tunelem pod laboratořemi do druhého kryostatu"],
  ["Čip 2", "převod zpět na dvě dráhy → supravodivé detektory"],
], 0.5, 1.4, 4.4);
image(slide, "1682", 5.1, 1.3, "Animace demonstrátoru: zdroj fotonů na prvním čipu");

// Numbers from Nature
slide = content("Škálování", "Čísla z článku v Nature 2025",
  "Platforma Omega: příprava a měření qubitu 99,98 procenta, interference fotonů z nezávislých zdrojů 99,5, fúze "
  + "99,22, propojení čipů 99,72 procenta. Všechna čísla platí pro fotony, které dorazily – ztráty v nich nejsou.");
stat(slide, "99,98 %", "příprava a měření qubitu", 0.5, 1.3, 2.05);
stat(slide, "99,50 %", "interference fotonů ze dvou zdrojů", 2.75, 1.3, 2.05);
stat(slide, "99,22 %", "dvouqubitová fúze", 0.5, 2.75, 2.05);
stat(slide, "99,72 %", "propojení dvou čipů", 2.75, 2.75, 2.05);
slide.addText("Podmíněno detekcí fotonů – bez započtení ztrát.", { x: 0.5, y: 4.15, w: 4.3, h: 0.4,
  fontFace: BODY, fontSize: 12, italic: true, color: COLORS.laser, isTextBox: true, margin: 0 });
image(slide, "1087", 5.1, 1.3, "Článek PsiQuantum o platformě Omega (preprint 2024, Nature 2025)");

// Sites
slide = content("Škálování", "Kam to míří: Brisbane a Chicago",
  "Ve videu stavby zazní bez termínů. Podle tisku: australská stavba se přestěhovala do Moreton Bay a základní "
  + "kámen padl v červnu 2026, píše se o provozu v roce 2029. V Chicagu má být testovací systém pro DARPA kolem "
  + "roku 2028. Podrobnosti na stránce PsiQuantum v aplikaci.");
card(slide, "Brisbane / Moreton Bay", "Původně do konce 2027; základní kámen 06/2026, tisk píše o roce 2029.",
  0.5, 1.3, 4.2, 1.3);
card(slide, "Chicago", "Kvantový park, testovací systém pro DARPA kolem roku 2028.", 0.5, 2.8, 4.2, 1.3);
image(slide, "1837", 5.1, 1.3, "Článek o plánu PsiQuantum v Brisbane (květen 2025)");

// 12 Critical
pres.addSection({ title: "Závěr" });
slide = content("Závěr", "Co video neříká",
  "Video je výborný průvodce součástkami, ale je natočené s přístupem firmy. Věrnosti platí jen pro fotony, které "
  + "dorazily; ztráty, logický qubit ani termíny nepadnou. Podrobnosti na stránce PsiQuantum v aplikaci.");
card(slide, "Ztráty", "Věrnost 99,7 % platí jen pro fotony, které dorazily. Rozhodující jsou ztráty.",
  0.5, 1.3, 4.35, 1.75);
card(slide, "Celý systém", "Ukázané jsou součástky a propojení dvou čipů, ne logický qubit.", 5.15, 1.3, 4.35, 1.75);
card(slide, "Termíny", "Stavby v Austrálii a Chicagu bez dat; termíny se posouvají.", 0.5, 3.25, 4.35, 1.75);
card(slide, "Nadsázky", "„Fotony nedekoherují“, „nejrychlejší materiál“ – zjednodušení.", 5.15, 3.25, 4.35, 1.75);

// Blueprint 2017
slide = content("Závěr", "Souvislosti: plán z roku 2017",
  "Video ukazuje součástky plánu Terryho Rudolpha z roku 2017: multiplexované ohlašované fotony, malé provázané "
  + "stavy, fúze a výpočet měřením. Dnes se mu říká fúzní kvantové počítání. Proč jsou potřeba třífotonové GHZ "
  + "stavy, vysvětluje stránka o GHZ stavech v aplikaci.");
steps(slide, [
  ["Fotony na povel", "ohlašování + multiplexování (zdroje, přepínače BTO)"],
  ["Malé provázané stavy", "třífotonové GHZ stavy z jednotlivých fotonů"],
  ["Fúze a měření", "spojování do velkého stavu, výpočet měřením; moduly přes vlákna"],
], 0.5, 1.4, 4.4);
image(slide, "0170", 5.1, 1.3, "Fotonický čip: vlnovody, prstencové rezonátory a spojky");

// 13 Summary
slide = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Závěr" });
slide.addText("Co si odnést", { placeholder: "title" });
slide.addText([
  { text: "Fotonický počítač je hlavně inženýrský problém: zdroje, detektory, přepínače, chlazení.",
    options: { bullet: true, breakLine: true } },
  { text: "Převod prostoru na čas vysvětluje, jak se má počítač skládat z modulů.",
    options: { bullet: true, breakLine: true } },
  { text: "Ztráty a chybějící logický qubit jsou otevřené otázky.", options: { bullet: true } },
], { x: 0.6, y: 2.2, w: 4.6, h: 2.6, fontFace: BODY, fontSize: 16, color: "C9D6E6", isTextBox: true,
  valign: "top", paraSpaceAfter: 6 });
slide.addText([
  { text: "Zdroje", options: { bold: true, color: COLORS.white, breakLine: true } },
  { text: "B. Miles: The Genius of Computing with Light, YouTube 2026", options: { breakLine: true } },
  { text: "PsiQuantum: A manufacturable platform for photonic quantum computing, Nature 641, 876 (2025)",
    options: { breakLine: true } },
  { text: "Quantum Knowledge Base: stránky PsiQuantum a zápisky z videa" },
], { x: 5.4, y: 1.4, w: 4.1, h: 2.6, fontFace: BODY, fontSize: 12, color: "C9D6E6", isTextBox: true,
  valign: "top", paraSpaceAfter: 6 });
slide.addNotes("Shrnutí a zdroje. Kritický pohled a souvislosti, například plán z roku 2017, peníze a termíny, "
  + "jsou na stránce PsiQuantum v aplikaci.");

pres.writeFile({ fileName: OUTPUT }).then((file) => {
  // Folder entries in the ZIP make some cloud services refuse to open the deck.
  try {
    require("child_process").execFileSync("zip", ["-dq", file, "*/"]);
  } catch (error) {
    // zip exits non-zero when there is nothing to delete
  }
  console.log(`Uloženo: ${file}`);
});
