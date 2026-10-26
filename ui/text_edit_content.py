"""Texts of the paragraph editor (ui/text_edit_panel.py)."""

TITLE = "Upravit odstavec"
MARKDOWN_HINT = (
    "Text je v Markdownu: **tučně**, *kurzívou*, vzorce v LaTeXu mezi $ … $ v řádku a $$ … $$ samostatně. "
    "Uložená úprava se ukáže hned a uvidí ji každý, kdo stránku otevře."
)
PLAIN_HINT = "Prostý text bez formátování. Uložená úprava se ukáže hned a uvidí ji každý, kdo stránku otevře."
MEMORY_HINT = (
    "Pozor: aplikace nemá databázi (chybí proměnná DATABASE_URL), takže úpravy drží jen v paměti "
    "a po restartu zmizí."
)
ORIGINAL_LABEL = "Původní znění"
SAVE_LABEL = "Uložit"
REVERT_LABEL = "Vrátit původní"
CANCEL_LABEL = "Zrušit"
MISSING_BLOCK = (
    "Tenhle odstavec se mezitím změnil, třeba po nasazení nové verze aplikace. Načti stránku znovu a zkus to ještě "
    "jednou."
)
