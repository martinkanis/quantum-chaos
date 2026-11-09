"""Texts of the assistant pop-up and of the agents page."""

from __future__ import annotations

from assistant.jobs import JobStatus

EXPLAIN_TITLE = "Dovysvětlení"
EXPAND_TITLE = "Rozvedení tématu"
PREVIEW_TITLE = "Návrh nové stránky"
AGENT_TITLE = "Agent"
EXPAND_LABEL = "Rozvést jako samostatné téma"
ACCEPT_LABEL = "Přijmout, commitnout a nasadit"
REJECT_LABEL = "Zamítnout"
CLOSE_LABEL = "Zavřít"
START_LABEL = "Spustit agenta"
AGENTS_LABEL = "Agenti"

EXPLANATION_NOTE = "Vysvětlení píše jazykový model Claude; zdroje, které uvádí, si ověř."
AGENT_STARTED = (
    "Agent hledá zdroje a píše novou stránku, obvykle 1–3 minuty. Okno můžeš zavřít a číst dál: až doběhne, odkaz "
    "Agenti v horní liště ukáže počet návrhů ke schválení, a pokud jsi je povolil, ozve se i notifikace prohlížeče. "
    "Stránku pak uvidíš jako návrh a rozhodneš, jestli ji přijmeš."
)
STILL_RUNNING = "Agent pořád pracuje. Až doběhne, odkaz Agenti v horní liště ukáže návrh ke schválení."
PLACEMENT_HINT = (
    "Vyber, pod které téma se nová stránka zařadí na stránce Témata; v horní liště a na mapě bude u skupiny "
    "stránky, ze které vzešla. Bez výběru skončí v tématu Rozvedená témata. Téma jde ještě změnit při schvalování."
)
ACCEPT_HINT = (
    "Přijetím aplikace uloží stránku do repozitáře (commit a push do main) a Rock8Cloud ji během pár minut nasadí. "
    "Stránka se zařadí do skupiny „{group}“ pod stránku „{parent}“ a do tématu, které vybereš dole."
)
TOPIC_LABEL = "Téma na stránce Témata"
DEFAULT_TOPIC_SUFFIX = " (výchozí)"
NEW_TOPIC_OPTION = "Nové téma…"
NEW_TOPIC_LABEL = "Název nového tématu (jen když vybereš „Nové téma…“)"
NEW_TOPIC_PLACEHOLDER = "Třeba: Kvantové tečky"
RUNNING_AGENTS_WARNING = (
    " Pozor: nasazení restartuje aplikaci a agenti, kteří ještě běží ({count}), se přeruší; pak je spustíš znovu."
)
REJECTED = "Návrh jsi zamítl, do aplikace se nedostane."
DEPLOYING = (
    "Stránka je commitnutá a pushnutá. Rock8Cloud teď sestavuje a nasazuje novou verzi aplikace, obvykle pár minut. "
    "Až bude hotovo, stránka Agenti ukáže „Nasazeno“ a novou stránku otevřeš odkazem."
)
DEPLOYED = "Stránka je v aplikaci. Odkaz načte aplikaci znovu, aby v ní byla i nová stránka."
COMMIT_LINK = "Commit na GitHubu"
OPEN_PAGE = "Otevřít stránku"
NO_PLACEMENT = (
    "Z této stránky nejde téma rozvést, nepatří do žádné skupiny. Označ text na některé studijní stránce."
)
MISSING_JOB = "Tohoto agenta už aplikace nezná."

OPEN_JOB = "Zobrazit"
OPEN_PROPOSAL = "Otevřít návrh ke schválení"
RETRY_JOB = "Spustit znovu"
DISMISS_JOB = "Skrýt"

# The page with the history of the agents (ui/agents_page.py).
AGENTS_TITLE = "Agenti"
AGENTS_LEAD = (
    "Agent je Claude, který z označeného úryvku napíše návrh nové stránky: vyhledá zdroje, text sepíše a počká, až "
    "ho schválíš. Spustíš ho tak, že na studijní stránce označíš text a v liště zvýrazňovače zvolíš „Rozvést na "
    "téma“. Tady je historie všech běhů od nejnovějšího; návrh ke schválení odsud otevřeš, přečteš a přijmeš, nebo "
    "zamítneš."
)
AGENTS_HINT = (
    "Odkaz Agenti v horní liště ukazuje, kolik návrhů čeká na schválení. Běh, který skryješ tlačítkem Skrýt, "
    "se v seznamu už neobjeví."
)
HISTORY_TITLE = "Historie běhů"
LOADING_HISTORY = "Načítám seznam agentů…"
EMPTY_HISTORY = "Zatím žádný agent neběžel."
ORIGIN_LABEL = "Ze stránky"
EXCERPT_LABEL = "úryvek"
UNKNOWN_PAGE = "neznámá stránka"
TOPIC_META_LABEL = "téma"
STARTED_LABEL = "Začátek"
FINISHED_LABEL = "Konec"
STILL_RUNNING_LABEL = "zatím běží"

STATUS_LABELS = {
    JobStatus.RUNNING: "Pracuje…",
    JobStatus.READY: "Ke schválení",
    JobStatus.FAILED: "Selhal",
    JobStatus.INTERRUPTED: "Přerušen",
    JobStatus.REJECTED: "Zamítnuto",
    JobStatus.DEPLOYING: "Nasazuje se…",
    JobStatus.DEPLOYED: "Nasazeno",
}
