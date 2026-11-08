// Builds content/lectures/<folder>/prezentace.pptx from prezentace.json next to it and the frames in slajdy/.
// The JSON describes the deck, so notes from any lecture get a presentation without code changes.
// pptxgenjs is not a dependency of the app; scripts/lecture_tools.py installs it into .lecture-tools/node of the
// project folder, where this script finds it also when run from a git worktree:
//   python3 scripts/lecture_tools.py install && node scripts/lecture_presentation.js content/lectures/<folder>
//
// prezentace.json:
//   { "title", "subtitle", "footer", "style": "snimky" | "vlastni",
//     "slides": [ { "type": "title" | "steps" | "cards" | "stats" | "bullets" | "table" | "closing",
//                   "section", "title", "items", "image", "caption", "notes", "header", "rows" } ] }
// "items": steps and cards take [heading, text] pairs, stats [value, label] pairs, bullets and closing strings.
// "image" is a frame from slajdy/; style "vlastni" leaves frames out and uses the whole width for the text.
const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");

function projectNodeModules() {
  const common = execFileSync("git", ["rev-parse", "--path-format=absolute", "--git-common-dir"],
    { cwd: __dirname, encoding: "utf8" }).trim();
  return path.join(path.dirname(common), ".lecture-tools", "node", "node_modules");
}

const pptxgen = require(require.resolve("pptxgenjs", { paths: [projectNodeModules(), ...module.paths] }));

const COLORS = {
  night: "0B1A2E",
  ink: "1B2433",
  muted: "5A6578",
  accent: "E8462A",
  cyan: "2BA6C2",
  mist: "EEF3F8",
  white: "FFFFFF",
  lead: "C9D6E6",
};
const HEAD = "Cambria";
const BODY = "Calibri";
const IMAGE_W = 4.6;
const IMAGE_H = (IMAGE_W * 9) / 16;
const TEXT_X = 0.5;
const IMAGE_X = 5.1;
const NARROW_W = 4.4;
const WIDE_W = 9;
const MAX_ITEMS = { steps: 4, cards: 4, stats: 4, bullets: 7, closing: 6 };

function readDeck(folder) {
  const deck = JSON.parse(fs.readFileSync(path.join(folder, "prezentace.json"), "utf8"));
  if (!Array.isArray(deck.slides) || deck.slides.length === 0) {
    throw new Error("prezentace.json: chybí seznam slajdů (slides)");
  }
  deck.slides.forEach((slide, index) => checkSlide(folder, slide, index + 1));
  return deck;
}

function checkSlide(folder, slide, number) {
  const where = `prezentace.json, slajd ${number}`;
  if (!RENDERERS[slide.type]) {
    throw new Error(`${where}: neznámý typ „${slide.type}“, povolené jsou ${Object.keys(RENDERERS).join(", ")}`);
  }
  if (!slide.title) throw new Error(`${where}: chybí nadpis (title)`);
  if (slide.type === "table" && (!Array.isArray(slide.header) || !Array.isArray(slide.rows))) {
    throw new Error(`${where}: tabulka potřebuje záhlaví (header) a řádky (rows)`);
  }
  const limit = MAX_ITEMS[slide.type];
  if (limit && (!Array.isArray(slide.items) || slide.items.length === 0 || slide.items.length > limit)) {
    throw new Error(`${where}: typ ${slide.type} potřebuje 1 až ${limit} položek (items)`);
  }
  if (slide.image && !fs.existsSync(path.join(folder, "slajdy", slide.image))) {
    throw new Error(`${where}: snímek ${slide.image} není ve složce slajdy`);
  }
}

function build(folder) {
  const deck = readDeck(folder);
  const withFrames = deck.style !== "vlastni";
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.title = deck.title;
  pres.author = "Quantum Knowledge Base";
  pres.theme = { headFontFace: HEAD, bodyFontFace: BODY };
  defineMasters(pres, deck.footer || deck.title);

  const sections = new Set();
  deck.slides.forEach((spec) => {
    const section = spec.section || "Přednáška";
    if (!sections.has(section)) {
      pres.addSection({ title: section });
      sections.add(section);
    }
    const image = withFrames && spec.image ? path.join(folder, "slajdy", spec.image) : null;
    RENDERERS[spec.type](pres, spec, section, image);
  });
  const output = path.join(folder, "prezentace.pptx");
  return pres.writeFile({ fileName: output }).then(() => output);
}

function defineMasters(pres, footer) {
  pres.defineSlideMaster({
    title: "TITLE_DARK",
    background: { color: COLORS.night },
    objects: [],
  });
  pres.defineSlideMaster({
    title: "CONTENT",
    background: { color: COLORS.white },
    objects: [
      { text: { text: footer, options: { x: 0.5, y: 5.2, w: 7.5, h: 0.3, fontFace: BODY, fontSize: 10,
        color: COLORS.muted } } },
    ],
    slideNumber: { x: 9.0, y: 5.2, w: 0.5, h: 0.3, fontFace: BODY, fontSize: 10, color: COLORS.muted, align: "right" },
  });
}

function contentSlide(pres, spec, section) {
  const slide = pres.addSlide({ masterName: "CONTENT", sectionTitle: section });
  slide.addText(spec.title, { x: 0.5, y: 0.3, w: 9, h: 0.75, fontFace: HEAD, fontSize: 28, bold: true,
    color: COLORS.ink, valign: "middle", margin: 0, fit: "shrink" });
  if (spec.notes) slide.addNotes(spec.notes);
  return slide;
}

function addImage(slide, image, caption, x, y, captionColor) {
  slide.addImage({ path: image, x, y, w: IMAGE_W, h: IMAGE_H, objectName: path.basename(image, ".jpg"),
    shadow: { type: "outer", color: "000000", opacity: 0.25, blur: 6, offset: 2, angle: 90 } });
  if (caption) {
    slide.addText(caption, { x, y: y + IMAGE_H + 0.05, w: IMAGE_W, h: 0.5, fontFace: BODY, fontSize: 10,
      color: captionColor || COLORS.muted, isTextBox: true, margin: 0, valign: "top", fit: "shrink" });
  }
}

function textWidth(image) {
  return image ? NARROW_W : WIDE_W;
}

function finish(slide, spec, image) {
  if (image) addImage(slide, image, spec.caption, IMAGE_X, 1.3);
}

function renderTitle(pres, spec, section, image) {
  const slide = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: section });
  const width = image ? 4.6 : 8.8;
  slide.addText(spec.title, { x: 0.6, y: 1.2, w: width, h: 1.8, fontFace: HEAD, fontSize: 34, bold: true,
    color: COLORS.white, valign: "top", margin: 0, fit: "shrink" });
  if (spec.subtitle) {
    slide.addText(spec.subtitle, { x: 0.6, y: 3.1, w: width, h: 1.6, fontFace: BODY, fontSize: 15,
      color: COLORS.lead, valign: "top", margin: 0, fit: "shrink" });
  }
  if (image) addImage(slide, image, spec.caption, 5.4, 1.3, "9FB0C6");
  if (spec.notes) slide.addNotes(spec.notes);
}

function renderSteps(pres, spec, section, image) {
  const slide = contentSlide(pres, spec, section);
  const width = textWidth(image);
  const gap = 3.7 / spec.items.length;
  spec.items.forEach(([head, text], index) => {
    const top = 1.35 + index * gap;
    slide.addShape(pres.shapes.OVAL, { x: TEXT_X, y: top, w: 0.42, h: 0.42, fill: { color: COLORS.accent },
      line: { color: COLORS.accent } });
    slide.addText(String(index + 1), { x: TEXT_X, y: top, w: 0.42, h: 0.42, fontFace: HEAD, fontSize: 16,
      bold: true, color: COLORS.white, align: "center", valign: "middle", isTextBox: true, margin: 0 });
    slide.addText([
      { text: head, options: { bold: true, color: COLORS.ink, breakLine: true } },
      { text, options: { color: COLORS.muted } },
    ], { x: TEXT_X + 0.6, y: top - 0.05, w: width - 0.6, h: gap - 0.1, fontFace: BODY, fontSize: 14,
      valign: "top", isTextBox: true, margin: 0, fit: "shrink" });
  });
  finish(slide, spec, image);
}

function renderCards(pres, spec, section, image) {
  const slide = contentSlide(pres, spec, section);
  const width = textWidth(image);
  const columns = image || spec.items.length < 3 ? 1 : 2;
  const rows = Math.ceil(spec.items.length / columns);
  const cardW = (width - (columns - 1) * 0.2) / columns;
  const cardH = (3.7 - (rows - 1) * 0.15) / rows;
  spec.items.forEach(([head, text], index) => {
    const x = TEXT_X + (index % columns) * (cardW + 0.2);
    const y = 1.3 + Math.floor(index / columns) * (cardH + 0.15);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: cardW, h: cardH, fill: { color: COLORS.mist },
      line: { color: COLORS.mist }, rectRadius: 0.08 });
    slide.addText([
      { text: head, options: { bold: true, color: COLORS.ink, fontSize: 16, breakLine: true } },
      { text, options: { color: COLORS.muted, fontSize: 13 } },
    ], { x: x + 0.2, y: y + 0.12, w: cardW - 0.4, h: cardH - 0.24, fontFace: BODY, valign: "top",
      isTextBox: true, margin: 0, paraSpaceAfter: 4, fit: "shrink" });
  });
  finish(slide, spec, image);
}

function renderStats(pres, spec, section, image) {
  const slide = contentSlide(pres, spec, section);
  const width = textWidth(image);
  const columns = image ? 1 : 2;
  const rows = Math.ceil(spec.items.length / columns);
  const statW = (width - (columns - 1) * 0.2) / columns;
  const statH = Math.min(1.25, (3.7 - (rows - 1) * 0.15) / rows);
  spec.items.forEach(([value, label], index) => {
    const x = TEXT_X + (index % columns) * (statW + 0.2);
    const y = 1.3 + Math.floor(index / columns) * (statH + 0.15);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: statW, h: statH, fill: { color: COLORS.mist },
      line: { color: COLORS.mist }, rectRadius: 0.08 });
    slide.addText(value, { x: x + 0.2, y: y + 0.08, w: statW - 0.4, h: statH * 0.5, fontFace: HEAD, fontSize: 28,
      bold: true, color: COLORS.accent, isTextBox: true, margin: 0, fit: "shrink" });
    slide.addText(label, { x: x + 0.2, y: y + statH * 0.55, w: statW - 0.4, h: statH * 0.42, fontFace: BODY,
      fontSize: 12, color: COLORS.ink, isTextBox: true, margin: 0, valign: "top", fit: "shrink" });
  });
  finish(slide, spec, image);
}

function renderBullets(pres, spec, section, image) {
  const slide = contentSlide(pres, spec, section);
  slide.addText(spec.items.map((text) => ({ text, options: { bullet: { indent: 18 }, breakLine: true } })), {
    x: TEXT_X, y: 1.3, w: textWidth(image), h: 3.75, fontFace: BODY, fontSize: 16, color: COLORS.ink,
    valign: "top", margin: 0, paraSpaceAfter: 8, fit: "shrink",
  });
  finish(slide, spec, image);
}

function renderTable(pres, spec, section, image) {
  const slide = contentSlide(pres, spec, section);
  const header = spec.header.map((text) => ({ text, options: { bold: true, color: COLORS.white,
    fill: { color: COLORS.ink } } }));
  slide.addTable([header, ...spec.rows], { x: TEXT_X, y: 1.35, w: textWidth(image), fontFace: BODY, fontSize: 13,
    color: COLORS.ink, border: { type: "solid", pt: 0.5, color: "C9D1DC" }, fill: { color: COLORS.white },
    autoPage: false });
  finish(slide, spec, image);
}

function renderClosing(pres, spec, section, image) {
  const slide = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: section });
  slide.addText(spec.title, { x: 0.6, y: 0.5, w: 8.8, h: 0.8, fontFace: HEAD, fontSize: 30, bold: true,
    color: COLORS.white, margin: 0 });
  slide.addText(spec.items.map((text) => ({ text, options: { bullet: { indent: 18 }, breakLine: true } })), {
    x: 0.6, y: 1.5, w: image ? 4.6 : 8.8, h: 3.6, fontFace: BODY, fontSize: 16, color: COLORS.lead,
    valign: "top", margin: 0, paraSpaceAfter: 8, fit: "shrink",
  });
  if (image) addImage(slide, image, spec.caption, 5.4, 1.5, "9FB0C6");
  if (spec.notes) slide.addNotes(spec.notes);
}

const RENDERERS = {
  title: renderTitle,
  steps: renderSteps,
  cards: renderCards,
  stats: renderStats,
  bullets: renderBullets,
  table: renderTable,
  closing: renderClosing,
};

const folder = process.argv[2];
if (!folder) {
  console.error("Použití: node scripts/lecture_presentation.js content/lectures/<složka>");
  process.exit(1);
}
build(path.resolve(folder))
  .then((output) => console.log(`Hotovo: ${output}`))
  .catch((error) => {
    console.error(error.message);
    process.exit(1);
  });
