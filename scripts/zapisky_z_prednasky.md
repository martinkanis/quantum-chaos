# Zápisky z přednášky: postup pro Claude Code

Návod, podle kterého Claude Code na autorově Macu zpracuje záznam přednášky na zápisky v aplikaci a volitelně
prezentaci .pptx a zveřejní je. Požadavek přijde z fronty v aplikaci (stránka `/zapisky-z-prednasek`) přes
naplánovanou úlohu, nebo přímo od uživatele v chatu.

Zápisky jsou **data**, ne kód:

- soubor `content/topics/<slug>.json` s polem `lecture`,
- složka `content/lectures/<složka>/` se snímky (`slajdy/slajd_SSSS.jpg`), popisem prezentace (`prezentace.json`)
  a prezentací (`prezentace.pptx`).

Stránku z nich postaví `ui/lecture_notes_page.py`. Do menu, témat a mapy ji zařadí `ui/topic_catalog.py` a
`ui/knowledge_map_content.py`. Kód se pro novou přednášku nemění.

## 0. Odkud je požadavek

**Z fronty v aplikaci:**

- Spusť v repozitáři `python3 scripts/lecture_queue.py dalsi`.
  - Kód 3 znamená prázdnou frontu, skonči.
  - Jinak dostaneš JSON s poli `id`, `url`, `topic_anchor` (nebo `nove-tema` s `new_topic_title`), `detail`
    (`prehled` | `podrobne` | `do-hloubky`), `presentation` (`zadna` | `snimky` | `vlastni`) a `note`.
- Požadavek je tím označený jako „zpracovává se“.
- Odeslání formuláře je výslovná žádost uživatele o zveřejnění **té jedné** přednášky. Commit a push do `main`
  (krok 7) jsou proto povolené jen pro její soubory.

**Od uživatele v chatu:** stejný postup s jeho volbami, ale bez hlášení stavu do fronty a push jen na jeho žádost.

**Hlášení průběhu:** během práce hlas průběh, třeba
`python3 scripts/lecture_queue.py stav ID zpracovava-se --zprava "Přepisuji zvuk…"`. Když cokoli selže a nejde to
opravit, nahlas `stav ID chyba --zprava "<co a proč, česky>"`, uklid pracovní strom a skonči.

## 1. Pracovní strom a nástroje

Všechno leží ve složce projektu `~/Work/Projects/quantum-chaos`. Pracuj v čistém dočasném worktree z aktuálního
`origin/main`, ne v checkoutu uživatele:

```
git -C ~/Work/Projects/quantum-chaos fetch origin
git -C ~/Work/Projects/quantum-chaos worktree add -b prednaska-<slug> ~/Work/Projects/quantum-chaos/.lecture-work/worktree-<slug> origin/main
```

Nástroje jsou ve složce projektu, mimo git (`.gitignore`). Skripty je najdou i z worktree.

- `.lecture-tools/whisper-venv/bin/mlx_whisper`: Whisper large-v3 na Apple Silicon. Model (asi 6 GB) je ve sdílené
  mezipaměti `~/.cache/huggingface`.
- `.lecture-tools/node/node_modules`: pptxgenjs@3.12.0.
- `yt-dlp`, `ffmpeg`, `soffice` a `pdftoppm` z Homebrew.
- Stav ověří `python3 scripts/lecture_tools.py check`. Chybějící doinstaluje `python3 scripts/lecture_tools.py install`.

Python aplikace (testy, skripty) je `~/Work/Projects/quantum-chaos/.venv/bin/python`.

## 2. Podklady

```
.venv/bin/python scripts/lecture_sources.py URL ~/Work/Projects/quantum-chaos/.lecture-work/<id-videa>
```

Skript vytvoří:

- `info.json`: metadata (název, kanál, datum, délka, kapitoly YouTube, popis),
- `video.mp4`: video do 720p,
- `prepis.txt`: přepis řeči, řádky `[mm:ss] text`,
- `snimky/` a `snimky.tsv`: snímky obrazovek, které vydrží aspoň 3 s.

Jak s podklady pracovat:

- **Přepis přečti celý.** Whisper plete jména (Lu → „Xiaoyang“, Aaronson → „Allison“), opravuj je podle slajdů a
  literatury.
- **Snímky si prohlédni** v náhledových arších:
  `ffmpeg -pattern_type glob -i 'snimky/slajd_*.jpg' -vf "scale=320:180,tile=6x5" arch_%d.jpg`.
- **Čísla, která chceš citovat, čti z plných snímků.** Spoj 4 do jednoho obrázku přes `xstack`.
- Přednáška delší než 9 999 s (2 h 46 min) se nevejde do jmen snímků. Nahlas chybu.

## 3. Zápisky: `content/topics/<slug>.json`

Vzor je `content/topics/lu-gaussian-boson-sampling-a-kvantova-vyhoda.json`. Formát hlídá `assistant/topics.py`
(`topic_from_dict`). Soubor skládej malým Python skriptem v dočasné složce a zapisuj přes
`topic_to_json(topic_from_dict(data))`, aby se chyby ukázaly hned.

**Základní pole:**

- `slug`: z názvu bez diakritiky (`slugify`). Stránka bude na `/zapisky/<slug>`.
- `title`: `Přednáška: <Přednášející> o <tématu> (<rok>)`, nejvýš 120 znaků.
- `description`: jedna věta pro menu.
- `in_short`: odstavec „V kostce“.

**`placement`:**

- `layer`: `fotonika`, `finance`, `gbs-ve-financich`, `vyzkum` nebo `zaklady`.
- `topic_anchor`: z požadavku.
- `section_title`: obvykle `"Přednášky"`.
- `parent_page_id`: `null`.
- Nové téma má navíc:
  - `topic_anchor` = `tema-<slug názvu>`,
  - `topic_title` = název z požadavku,
  - `topic_summary` = jedna až dvě věty o tématu.

**`origin`:**

- `page_id`: `"lecture-requests-page"`.
- `selection`: URL videa.
- `created`: dnešní datum ISO.
- `model`: `"Claude Code"`.

**`lecture`:**

- `folder`: krátký slug, třeba `prijmeni-tema-rok`.
- `video_url`, `video_seconds`, `speaker` (s institucí), `event`, `recorded` (ISO) a `language`.
- `how_made`: přepis Whisperem, počet snímků, co je vynechané a které kapitoly jsou naše.
- `has_presentation`.
- `key_points`: TL;DR, 4–8 bodů s číslem kapitoly.
- `related_page_id`: stránka aplikace, kterou přednáška nejvíc rozvádí. Nastav ho vždy, jinak stránka na mapě
  visí a test v `tests/test_knowledge_map.py` selže.

**`sections`:**

- Nejdřív kapitoly přednášky v pořadí. Každá má `start` (sekunda) a `slides` (snímky z jejího úseku, popisky
  česky).
- Pak vlastní kapitoly bez `start` a bez snímků, třeba „Co se stalo potom“ a „Co si z toho vzít pro náš výzkum“.
- Nejvýš 20 kapitol a 40 snímků na kapitolu.
- Hranice kapitol dávej mezi obrazovky. Snímek `slajd_0335.jpg` ukazuje obrazovku, která trvala **do** 335 s, takže
  patří do kapitoly, která začíná nejpozději v 335 s.

**`sources`:**

- Každý zdroj s odkazem.
- DOI ověř přes `https://api.crossref.org/works/<doi>`, arXiv přes
  `https://export.arxiv.org/api/query?id_list=…`.
- Neověřený zdroj neuváděj.

**Podrobnost podle požadavku:**

- `prehled`: 4–6 kapitol, hlavní myšlenky a čísla, málo snímků.
- `podrobne`: kapitola na každou část přednášky se snímky, pojmy vysvětlené stručně.
- `do-hloubky`: jako `podrobne`, navíc:
  - každý pojem polopatě pro začínajícího doktoranda,
  - vzorce v MathJaxu,
  - odkazy na související stránky aplikace (`[text](/cesta#kotva)`, hlídá je `tests/test_text_links.py`),
  - literatura.
- Poznámku z požadavku (`note`) ber jako zadání, na co se zaměřit.

**Pravidla psaní** (jako u celé aplikace, viz `CLAUDE.md`):

- Česky a polopatě, s odkazy na literaturu.
- Desetinná čárka, v LaTeXu `0{,}5`. Blokové vzorce `$$` na samostatných řádcích.
- Odliš, co řekl přednášející, co je v literatuře a co je **náš** výpočet nebo odhad. Ten tak i označ.
- Přepis necituj ve velkém: zápisky jsou vlastní výklad, ne překlad. Krátké citace jen výjimečně.
- Vlastní výpočty (přepočty čísel ze slajdů) pohlídej testem v `tests/test_lecture_notes.py` podle vzoru
  `test_cisla_v_zapiskach_lu_odpovidaji_vypoctu`.

## 4. Snímky

- Vybrané snímky zkopíruj do `content/lectures/<folder>/slajdy/`.
- Celkem jich dej nejvýš asi 40.
- Vynechej opakované kroky animací, záběry kamery a přechody.

## 5. Prezentace (když `presentation` není `zadna`)

Napiš `content/lectures/<folder>/prezentace.json` podle vzoru `content/lectures/lu-gbs-2021/prezentace.json`. Formát
je popsaný v hlavičce `scripts/lecture_presentation.js`.

- `style`: `snimky` (snímky vedle textu) nebo `vlastni` (bez snímků, text přes celou šířku).
- Asi 12–18 slajdů: titulní, kapitoly a závěr.
- Typy `steps`, `cards`, `stats`, `bullets`, `table` a `closing`.
- Krátké texty a poznámky řečníka (`notes`).

Sestav prezentaci a převeď ji na náhledy:

```
node scripts/lecture_presentation.js content/lectures/<folder>
soffice --headless --convert-to pdf --outdir /tmp/qc-pptx content/lectures/<folder>/prezentace.pptx
pdftoppm -r 50 -png /tmp/qc-pptx/prezentace.pdf /tmp/qc-pptx/s
```

Prohlédni náhledy (`tile`) a oprav přetékající text nebo stísněné tabulky. Tabulka vedle snímku bývá úzká, proto u
ní snímek vynech.

## 6. Kontrola

- Spusť testy a lint:
  - `.venv/bin/python -m pytest -q`
  - `.venv/bin/python -m pyflakes app.py assistant auth edits gbs montecarlo randommatrix scripts ui web tests`
- Kromě známých selhání `tests/test_assistant.py` bez balíku `anthropic` musí vše projít.
- Selže-li test počtu kroků tématu, oprav data, ne test. Ruční stránky drží `tests/photonics_steps.py`.
- Stránku ověř v náhledu (`python app.py`): obsah, vzorce, snímky a stažení prezentace.

## 7. Zveřejnění

1. Commitni v pracovním stromu jen soubory přednášky (a případně test čísel).
   - Zpráva česky, proč: `Zápisky z přednášky <přednášející>: <téma>`.
   - **Žádný `Co-Authored-By` ani jiná AI atribuce.**
2. Pushni: `git push origin HEAD:main`. Push do `main` nasadí aplikaci.
3. Jen když je lokální `main` čistý, srovnej ho: `git -C ~/Work/Projects/quantum-chaos merge --ff-only origin/main`.
4. Nahlas hotovo:
   `python3 scripts/lecture_queue.py stav ID hotovo --stranka /zapisky/<slug> --zprava "Zveřejněno, nasazení běží."`.
5. Smaž dočasný worktree a větev (`git worktree remove .lecture-work/worktree-<slug>`,
   `git branch -D prednaska-<slug>`).
6. Pracovní složku `.lecture-work/<id-videa>` nech. Video a přepis se hodí, když se zápisky budou opravovat.
