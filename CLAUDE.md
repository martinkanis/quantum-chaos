# Quantum chaos – Monte Carlo portfolia a Gaussian Boson Sampling

Dash aplikace pro výuku a výzkum. Úvodní stránka Témata (`/`) řadí obsah pod témata; vedle ní je Quantum Academy
s odkazy na materiály. Téma „Monte Carlo a modifikované Monte Carlo“ má 1. stránku klasické Monte Carlo portfolia,
2. stránku Monte Carlo na GBS (s podstránkami Háčky a Teorie) a 3. stránku Výhoda GBS (laboratoř, pět úloh, export
do Qiskitu, průvodce). Téma „Kvantová optimalizace portfolia“ má rozbory článků (zatím VQE na IBM Fez,
arXiv:2512.22001; čísla z článku jsou data v `ui/vqe_paper_content.py`). Téma „Fotonika“ má český překlad
skript Kolarovszki–Zimborás o fotonickém kvantovém počítání a GBS (pět stránek `/fotonika/...`), simulátor
programovatelného čipu ze sítě MZI (Clementsův rozklad, výrobní chyby a kalibrace; boson sampling až na
64 světlovodech jako modifikované Monte Carlo proti klasickému), přehled firem,
stránku o simulátoru Piquasso, oddíl o firmě PsiQuantum (přehled a zápisky z videa Bena Milese s prezentací
ke stažení) a zápisky z přednášky Philipa Walthera (2022) se slajdy
a podstránkou o třífotonových GHZ stavech. Novou stránku zařaď do tématu
v `ui/topic_catalog.py`; odtud se kreslí Témata i drobečková navigace. Horní lišta má témata, stránky tématu Monte Carlo
jsou v řádku pod ní (`navigation.py`).
Cílový čtenář je začínající doktorand: texty podrobně, ale polopatě, s odkazy na literaturu.

## Příkazy

- Testy: `/Users/martinkanis/Work/Projects/quantum-chaos/.venv/bin/python -m pytest -q` (z kořene repa i z worktree)
- Lint: stejný Python `-m pyflakes app.py assistant auth edits gbs montecarlo randommatrix scripts ui web tests`
- Lokální běh: `python app.py` → http://localhost:8050 (debug mód); náhled v Claude Code přes `.claude/launch.json`
- Lokálně Python 3.9, v Dockeru 3.12 – žádná syntaxe novější než 3.9 (`X | Y` v typech, `match`).
- Qiskit není závislost aplikace. Test exportu se bez něj přeskočí; ověřit ho jde v pomocném venv
  s `pip install qiskit numpy pytest`.

## Architektura

- `montecarlo/` – doména klasického Monte Carla: portfolio, simulace, historická data (Damodaran 1928–2023),
  předvolby trhu, stresové scénáře.
- `assistant/` – Claude v aplikaci: dovysvětlení označeného textu (`claude.explain`), agenti, kteří úryvek
  rozvedou na novou stránku (`agent.py`, webové vyhledávání + strukturované odevzdání), jejich stav v Postgresu
  (`jobs.py`, bez `DATABASE_URL` jen v paměti) a commit přijatého tématu přes GitHub API (`publish.py`).
  Historie běhů je stránka `/agenti` (`ui/agents_page.py`, trvale v layoutu); odkaz Agenti v liště vedle Odhlásit
  nese počet návrhů ke schválení a návrh se otevírá, přijímá a zamítá v okně asistenta (`ui/assistant_callbacks.py`).
- `content/topics/*.json` – témata, která napsal asistent a uživatel přijal; aplikace je zapisuje sama commitem
  do `main` (před vlastní prací `git pull`). Čte je `ui/generated_topics.py`, stránky staví `ui/generated_page.py`
  a zařazuje je skupina zdrojové stránky v menu a na mapě a téma „Rozvedená témata“ (`topic_catalog.topics_with`).
- `edits/` – ruční úpravy textů (např. špatně přeložený termín): Markdown rozdělený na bloky (`blocks.py`)
  a úpravy v Postgresu (`store.py`, tabulka `text_edits`, bez `DATABASE_URL` jen v paměti). `ui/editable_text.py` dá
  na každé stránce id `{"type": "text-edit", "page", "key", "copy"}` každému bloku `dcc.Markdown` (vícebloký
  rozdělí po odstavcích) a každému prostému textu v html komponentě nebo `dcc.Link` (text mezi jinými prvky obalí
  do `html.Span`); vynechá komponenty s vlastním id, tlačítka, kód a texty bez písmen. Klíč = hash původního textu,
  stejný text na jedné stránce je jeden blok s více kopiemi (nadpis i položka obsahu se mění spolu). `app.layout`
  je proto funkce (`EditablePages.layout`) a odložené stránky se posílají s úpravami. Editor otevírá „Upravit text“
  v liště zvýrazňovače (`assets/text_edit.js`). Když se změní původní text ve zdroji, jeho úprava se přestane
  uplatňovat (zůstane v tabulce i s původním zněním).
- `ui/primer_*_content.py` – překlad skript (jedna kapitola = jeden modul s `CHAPTER`, sekce v Markdownu
  s MathJaxem, čísla rovnic `\tag{…}` a citace `[n]` jako v originálu; literatura v `ui/primer_content.py`).
  Stránky staví `ui/primer_page.py`, formát hlídá `tests/test_primer_pages.py`. Originální PDF v repu není.
- `ui/walther_lecture_*.py` – zápisky z přednášky: kapitoly s časem ve videu a slajdy (`SLIDES`, snímky ze záznamu
  v `content/lectures/<přednáška>/slajdy/`). Slajdy patří autorům, proto je posílá `web/lecture_slides.py` jen
  přihlášeným (`/assets/` je veřejné), stejně jako prezentaci `prezentace.pptx` vedle nich (vyrábí ji skript
  ve `scripts/`, pptxgenjs není závislost aplikace). Zápisky z videa o PsiQuantum (`ui/psiquantum_video_*.py`)
  sdílejí snímky a odkazy do videa přes `slide_figure`. Přepisy a všechny snímky jsou ve větvi `podklady-video`.
- Nové zápisky z přednášek jsou **data**: `content/topics/<slug>.json` s polem `lecture` (kapitoly se `start` a
  snímky, vlastní kapitoly bez času na konci) a `content/lectures/<složka>/` (snímky, `prezentace.json`,
  `prezentace.pptx` ze `scripts/lecture_presentation.js`). Stránku na `/zapisky/<slug>` staví
  `ui/lecture_notes_page.py`. Na `/zapisky-z-prednasek` se přednáška zařadí do fronty (`assistant/lecture_requests.py`,
  tabulka `lecture_requests`); zpracuje ji Claude Code na Macu podle `scripts/zapisky_z_prednasky.md` přes
  `scripts/lecture_queue.py` a API `web/lecture_queue_api.py` (token `LECTURE_WORKER_TOKEN`, mimo přihlášení).
  Nástroje (Whisper, pptxgenjs) instaluje `scripts/lecture_tools.py` do `.lecture-tools/` a podklady přednášek leží
  v `.lecture-work/`, obojí ve složce projektu mimo git.
- `gbs/` – doména GBS: hafnián, sampler, gaussovské momenty (Steinova rekurze), ladění stlačení, odhad GBS-P,
  export do Qiskitu (šablona `qiskit_script_template.txt`), fotonický čip ze sítě MZI (`photonic_chip.py`,
  `clements.py`, `chip_programming.py`, kreslení `chip_charts.py` s polohami `chip_geometry.py` a součástkami
  `chip_parts.py`: každý druh součástky je neviditelná stopa s popiskem, `customdata` končí druhem a číslem
  součástky, podle kterých `ui/chip_interaction_callbacks.py` pozná klik; pracovní stůl `bench.py` (zdroj, ztráty
  vlákno–čip a světlovodů, detektory, čítače jednotlivých fotonů; hodnoty jsou náš odhad); boson sampling na čipu
  `chip_boson_sampling.py` s vektorizovanými permanenty, grafy `chip_sampling_charts.py`); ztráty fotonů
  (`photon_loss.py`: rovnoměrná ztráta = binomické ředění ideálního rozdělení z tabulky momentů, nestranná oprava
  a její rozptyl, prahové detektory; `loss_study.py` odhad GBS-P proti ztrátám, kritická propustnost a hranice
  Qi a kol.; stránka `/vyzkumne-smery/ztraty-fotonu` jako 4. zdroj chyby diagnostiky selhání).
- `ui/` – Dash vrstva: `*_page.py` layout, `*_callbacks.py` callbacky, `*_content.py` texty, `ids.py` všechna id,
  `navigation.py` cesty a přepínání stránek.
- Business logika patří do `gbs/` a `montecarlo/`; UI jen parsuje formulář a vykresluje výsledek.
- `assets/highlighter.js` – zvýrazňování a podtrhávání textu (CSS Custom Highlight API, DOM Dashe nemění), uložené
  v localStorage a ukotvené ke stránkám z `data-highlight-roots` v `ui/layout.py` (= `PAGE_IDS`). Pravidla
  `::highlight()` zpomalují sázení MathJaxu, proto jsou jen pro použité barvy a při změnách DOM se vypínají.
  Vzorce (MathJax je sází do SVG bez textu) vybere klepnutí; Dovysvětlit a Rozvést je dostanou jako zdrojový TeX
  ze seznamu `MathJax.startup.document.math` (`assets/assistant.js`), prompt pro vzorec je v `assistant/prompts.py`.
- `assets/text_links.js` – odkaz v Markdownu na stránku aplikace (`[text](/cesta#kotva)` v kartě `.theory-section`
  nebo ve „V kostce“) přepne stránku jako `dcc.Link`, bez načtení celé aplikace. Že vede na existující stránku
  a kotvu, hlídá `tests/test_text_links.py`.
- `assets/chip_animation.js` – průchod světla čipem: do prázdného `.chip-animation` (`ui/chip_animation.py`) postaví
  ovládání (pustit/zastavit, okamžik, délka průchodu) a v grafu odkrývá tvary světla ořezem a vede pulzy po drahách
  z `layout.meta.lightAnimation` (`gbs/chip_charts.py`). Tvary hledá podle `path[data-index]` v DOM Plotly; když se
  změní pořadí tvarů v `chip_figure`, musí sedět indexy v meta.
- Čtení offline: `assets/offline.js` registruje service worker (`web/service_worker.js`, posílá ho `web/offline.py`
  na `/sw.js`). Ten ukládá aplikaci, slajdy i odpovědi callbacků (stránky Dash skládá z nich) a offline je vrací;
  chybějící odpověď je 204 = beze změny. Po každém nasazení nebo po 12 h stáhne předem všechny stránky podle
  `/offline-manifest.json` (cesty, callbacky závislé jen na cestě, odložený kód Dashe, slajdy). Klíč odpovědi
  u callbacků podle cesty ignoruje store (`*-store`). Odpovědi, které se mění bez čtenáře (seznam agentů), worker
  neukládá (`LIVE_OUTPUTS`). Odhlášení uložené stránky smaže. Nový zdroj, který se
  načítá mimo `/_dash-component-suites/`, `/assets/` a `/prednasky/`, přidej do workeru nebo do manifestu.
- Stránky s formuláři jsou trvale v layoutu a jen se skrývají (`show_page`), takže formuláře přežijí přepnutí.
  Čtecí stránky bez formulářů se posílají až při první návštěvě (`ui/lazy_pages.py`, jinak by prohlížeč při každém
  načtení sázel vzorce všech skrytých stránek); novou stránku bez formuláře přidej do `PAGE_BUILDERS`.

## Konvence

- UI texty, chybové hlášky, názvy testů a commity česky; identifikátory a docstringy anglicky.
- Validace na hranici: vlastní `*Error(ValueError)` s akční českou hláškou, callback ji ukáže v error divu.
- Čísla v UI česky: desetinná čárka, mezery mezi tisíci.
- `dcc.Markdown` s MathJaxem: blokové vzorce `$$` na samostatných řádcích, desetinná čárka v LaTeXu `0{,}5`,
  dlouhé inline vzorce rozbíjejí mobilní zobrazení.
- Čísla uvedená v textech musí sedět s výpočtem a hlídá je test (vzor: `test_cisla_v_popisech_uloh_odpovidaji_vypoctu`).
- Odborná tvrzení: odlišuj doložené (citace jako `Source`) od vlastního odhadu a odhad tak i označ.

## Dash – na co si dát pozor

- Každý Input a State callbacku musí existovat v úvodním layoutu (žádné `suppress_callback_exceptions`);
  tlačítka a `dcc.Download` dávej do layoutu staticky a skrývej je.
- Víc callbacků do stejné vlastnosti potřebuje `allow_duplicate=True`.
- Id i kotvy musí být unikátní napříč všemi stránkami, protože všechny jsou v DOM (průvodce má prefix `pruvodce-`).
- DataTable s dropdownem nesmí být ve scroll kontejneru, jinak se menu ořízne.
- Callback by měl doběhnout do ~30 s (gunicorn: 1 worker, timeout 120 s, 256 MiB); limity drží konstanty `MAX_*`.

## Nasazení

- Rock8Cloud: služba `01a0df3e-9287-76ca-b5c4-3b38297b296f`, organizace `tV6KVvfs0A6NByhPquPHpEUaKjhkzQ7h`,
  https://quantum-chaos.rock8cloud.app
- Push do `main` nasazuje automaticky (zapnuto v Rock8Cloud kvůli přijímání témat z aplikace); po pushi ověř
  `/healthz` a `/_dash-layout`, ručně jde nasadit přes MCP `deploy_service`.
- Proměnné služby pro asistenta: `ANTHROPIC_API_KEY`, `GITHUB_TOKEN` (fine-grained, jen Contents: read and write
  na tento repozitář), `DATABASE_URL` (propojená z Postgresu); volitelně `ASSISTANT_MODEL`, `GITHUB_REPOSITORY`,
  `GITHUB_BRANCH`. Bez nich asistent v okně napíše, co chybí, zbytek aplikace běží.
- `LECTURE_WORKER_TOKEN` (aspoň 32 znaků) otevře frontu přednášek pracovníkovi; bez něj se požadavky jen
  sbírají. Stejný token má Mac v `~/.config/quantum-chaos/lecture-worker-token`.
- Dockerfile kopíruje jen `assets assistant auth content edits gbs montecarlo randommatrix ui web app.py` – nový
  adresář nebo soubor v kořeni do něj přidej.

## Git

- Jediná větev `main` (žádné dev/stage). „Pushni“ znamená `git push origin HEAD:main`, jen na výslovnou žádost.
- Ve worktree `.claude/worktrees/*` commituj tam, pushni `HEAD:main` a lokální `main` srovnej
  `git -C /Users/martinkanis/Work/Projects/quantum-chaos merge --ff-only origin/main`.
