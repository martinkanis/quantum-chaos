"""Texts of the text editor (ui/text_edit_panel.py)."""

TITLE = "Upravit text"
SHOWN = (
    "Uložená úprava se ukáže hned, i na dalších místech stránky se stejným textem (třeba v obsahu), a uvidí ji "
    "každý, kdo stránku otevře."
)
MARKDOWN_HINT = (
    "Text je v Markdownu: **tučně**, *kurzívou*, vzorce v LaTeXu mezi $ … $ v řádku a $$ … $$ samostatně. "
    + SHOWN
)
PLAIN_HINT = "Prostý text bez formátování (nadpis, popisek nebo část odstavce). " + SHOWN
MEMORY_HINT = (
    "Pozor: aplikace nemá databázi (chybí proměnná DATABASE_URL), takže úpravy drží jen v paměti "
    "a po restartu zmizí."
)
ORIGINAL_LABEL = "Původní znění"
SAVE_LABEL = "Uložit"
REVERT_LABEL = "Vrátit původní"
CANCEL_LABEL = "Zrušit"
MISSING_BLOCK = (
    "Tenhle text se mezitím změnil, třeba po nasazení nové verze aplikace. Načti stránku znovu a zkus to ještě "
    "jednou."
)
