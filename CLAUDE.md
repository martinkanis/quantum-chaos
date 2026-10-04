# Quantum chaos – Monte Carlo portfolia a Gaussian Boson Sampling

Dash aplikace pro výuku a výzkum: 1. stránka klasické Monte Carlo portfolia, 2. stránka Monte Carlo na GBS
(s podstránkami Háčky a Teorie), 3. stránka Výhoda GBS (laboratoř, pět úloh, export do Qiskitu, průvodce).
Cílový čtenář je začínající doktorand: texty podrobně, ale polopatě, s odkazy na literaturu.

## Příkazy

- Testy: `/Users/martinkanis/Work/Projects/quantum-chaos/.venv/bin/python -m pytest -q` (z kořene repa i z worktree)
- Lint: stejný Python `-m pyflakes app.py gbs ui montecarlo tests`
- Lokální běh: `python app.py` → http://localhost:8050 (debug mód); náhled v Claude Code přes `.claude/launch.json`
- Lokálně Python 3.9, v Dockeru 3.12 – žádná syntaxe novější než 3.9 (`X | Y` v typech, `match`).
- Qiskit není závislost aplikace. Test exportu se bez něj přeskočí; ověřit ho jde v pomocném venv
  s `pip install qiskit numpy pytest`.

## Architektura

- `montecarlo/` – doména klasického Monte Carla: portfolio, simulace, historická data (Damodaran 1928–2023),
  předvolby trhu, stresové scénáře.
- `gbs/` – doména GBS: hafnián, sampler, gaussovské momenty (Steinova rekurze), ladění stlačení, odhad GBS-P,
  export do Qiskitu (šablona `qiskit_script_template.txt`).
- `ui/` – Dash vrstva: `*_page.py` layout, `*_callbacks.py` callbacky, `*_content.py` texty, `ids.py` všechna id,
  `navigation.py` cesty a přepínání stránek.
- Business logika patří do `gbs/` a `montecarlo/`; UI jen parsuje formulář a vykresluje výsledek.
- Všechny stránky jsou trvale v layoutu a jen se skrývají (`show_page`), takže formuláře přežijí přepnutí.

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
- Push do `main` nenasazuje automaticky: nasadit přes MCP `deploy_service`, pak ověřit `/healthz` a `/_dash-layout`.
- Dockerfile kopíruje jen `assets gbs montecarlo ui app.py` – nový adresář nebo soubor v kořeni do něj přidej.

## Git

- Jediná větev `main` (žádné dev/stage). „Pushni“ znamená `git push origin HEAD:main`, jen na výslovnou žádost.
- Ve worktree `.claude/worktrees/*` commituj tam, pushni `HEAD:main` a lokální `main` srovnej
  `git -C /Users/martinkanis/Work/Projects/quantum-chaos merge --ff-only origin/main`.
