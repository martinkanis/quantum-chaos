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

// 5 Heralding and multiplexing
slide = content("Součástky", "Ohlašování a multiplexování",
  "Druhý foton z páru se detekuje a ohlásí, že jeho dvojče existuje. Mnoho zdrojů vedle sebe: přepínač pošle do "
  + "výpočtu ten, který uspěl. Vlastní výpočet: s pravděpodobností 5 % na zdroj stačí 90 zdrojů na 99 % taktů.");
stat(slide, "90 zdrojů", "stačí na foton v 99 % taktů, když jeden uspěje s pravděpodobností 5 % (vlastní výpočet)",
  0.5, 1.35, 4.3);
card(slide, "Ohlašovací foton", "Detekce červeného fotonu ohlásí modrý, aniž bychom se ho dotkli. Rychlý přepínač "
  + "pak připojí jeho zdroj na hlavní vlnovod.", 0.5, 2.8, 4.3, 1.75);
image(slide, "0552", 5.1, 1.3, "Multiplexování: čtyři vlnovody, každý se čtyřmi rezonátory");

// 6 Detectors
slide = content("Součástky", "Detekce jednotlivých fotonů",
  "Supravodivý nanodrát z nitridu niobu, široký asi 100 nanometrů, těsně pod kritickým proudem. Foton rozbije "
  + "Cooperovy páry a vznikne puls. Na čipu přes 93 procent, další generace 99. Vlastní výpočet: při 93 procentech "
  + "se všech 50 fotonů zachytí jen asi ve 2,7 procenta případů.");
stat(slide, "93 % → 99 %", "účinnost detektorů na čipu dnes a v další generaci", 0.5, 1.35, 4.3);
stat(slide, "2,7 %", "šance zachytit všech 50 fotonů při účinnosti 93 % (vlastní výpočet)", 0.5, 2.8, 4.3);
image(slide, "0763", 5.1, 1.3, "Vrstva nitridu niobu – materiál supravodivého detektoru");

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

// 9 Cooling
slide = content("Součástky", "Chlazení na 2 K",
  "Kvůli detektorům běží všechno v kryostatech Mark II při dvou kelvinech. Supravodivé qubity potřebují kolem "
  + "dvaceti milikelvinů, tedy stokrát méně. Cílem jsou čtyři kelviny. Méně energie na chlazení je podmínka "
  + "pro miliony qubitů.");
stat(slide, "2 K", "provozní teplota dnes; cílem pro nasazení ve velkém jsou 4 K", 0.5, 1.35, 4.3);
stat(slide, "100×", "tepleji než supravodivé qubity (kolem 20 mK)", 0.5, 2.8, 4.3);
image(slide, "1336", 5.1, 1.3, "Uvnitř kryostatu Mark II: svislé „čepele“ pro čipy");

// 10 Space to time
pres.addSection({ title: "Škálování" });
slide = content("Škálování", "Převod qubitu z prostoru do času",
  "Qubit ve dvou drahách se převede na dva časové okamžiky vzdálené jednu nanosekundu. Obě části letí stejným "
  + "vláknem, pomalé poruchy je ovlivní stejně a fázový vztah přežije. Na druhém čipu se převod obrátí.");
steps(slide, [
  ["Rozdělení", "jedna dráha je delší o 1 ns – na čipu dlouhá spirála"],
  ["Jedno vlákno", "qubit „dřív / později“ – drift vlákna zasáhne obě části stejně"],
  ["Zpětný převod", "druhý čip vrátí qubit do dvou drah"],
], 0.5, 1.4, 4.4);
image(slide, "1557", 5.1, 1.3, "Spirálová zpožďovací dráha a spojení dvou drah do jedné");

// 11 Demonstrator
slide = content("Škálování", "Demonstrátor: qubit tunelem",
  "Dva čipy v samostatných kryostatech spojené 250 metry vlákna v tunelu. Věrnost přeneseného stavu 99,7 procenta, "
  + "v Nature 2025 99,72 procenta. Ve videu zazní 800 nanosekund, ale 250 metrů vlákna světlo proletí asi za "
  + "1,2 mikrosekundy – jedno z čísel je nepřesné.");
stat(slide, "99,7 %", "věrnost qubitu přeneseného 250 m vlákna mezi dvěma kryostaty", 0.5, 1.35, 4.3);
card(slide, "Kontrola čísel", "Ve videu „800 ns“, ale 250 m vlákna světlo proletí asi za 1,2 µs (vlastní "
  + "výpočet).", 0.5, 2.8, 4.3, 1.3);
image(slide, "1665", 5.1, 1.3, "Vstup do „kvantového tunelu“ s vláknem mezi laboratořemi");

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
