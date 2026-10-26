"""Texts of the assistant pop-up and of the agents panel."""

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
AGENTS_LABEL = "Agenti"

EXPLANATION_NOTE = "Vysvětlení píše jazykový model Claude; zdroje, které uvádí, si ověř."
AGENT_STARTED = (
    "Agent hledá zdroje a píše novou stránku, obvykle 1–3 minuty. Okno můžeš zavřít a číst dál: až doběhne, ozve se "
    "okénko Agenti vpravo nahoře, a pokud jsi je povolil, i notifikace prohlížeče. Stránku pak uvidíš jako návrh "
    "a rozhodneš, jestli ji přijmeš."
)
STILL_RUNNING = "Agent pořád pracuje. Až doběhne, ozve se okénko Agenti vpravo nahoře."
ACCEPT_HINT = (
    "Přijetím aplikace uloží stránku do repozitáře (commit a push do main) a Rock8Cloud ji během pár minut nasadí. "
    "Stránka se zařadí do skupiny „{group}“ pod stránku „{parent}“ a do tématu Rozvedená témata."
)
RUNNING_AGENTS_WARNING = (
    " Pozor: nasazení restartuje aplikaci a agenti, kteří ještě běží ({count}), se přeruší; pak je spustíš znovu."
)
REJECTED = "Návrh jsi zamítl, do aplikace se nedostane."
DEPLOYING = (
    "Stránka je commitnutá a pushnutá. Rock8Cloud teď sestavuje a nasazuje novou verzi aplikace, obvykle pár minut. "
    "Až bude hotovo, okénko Agenti ukáže „Nasazeno“ a stránku otevřeš odkazem."
)
DEPLOYED = "Stránka je v aplikaci. Odkaz načte aplikaci znovu, aby v ní byla i nová stránka."
COMMIT_LINK = "Commit na GitHubu"
OPEN_PAGE = "Otevřít stránku"
NO_PLACEMENT = (
    "Z této stránky nejde téma rozvést, nepatří do žádné skupiny. Označ text na některé studijní stránce."
)
MISSING_JOB = "Tohoto agenta už aplikace nezná."

OPEN_JOB = "Zobrazit"
RETRY_JOB = "Spustit znovu"
DISMISS_JOB = "Skrýt"

STATUS_LABELS = {
    JobStatus.RUNNING: "Pracuje…",
    JobStatus.READY: "Ke schválení",
    JobStatus.FAILED: "Selhal",
    JobStatus.INTERRUPTED: "Přerušen",
    JobStatus.REJECTED: "Zamítnuto",
    JobStatus.DEPLOYING: "Nasazuje se…",
    JobStatus.DEPLOYED: "Nasazeno",
}
