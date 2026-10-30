// Offline reading: registers the service worker (served by web/offline.py) and shows a small status badge.
// After every load with a connection the worker checks whether its copy of the pages is current and, if not,
// downloads all of them; the badge shows the progress and, without a connection, that the stored copy is shown.
(function () {
    if (!("serviceWorker" in navigator)) {
        return;
    }
    const SERVICE_WORKER_URL = "/sw.js";
    const BADGE_ID = "offline-status";
    const READY_MILLISECONDS = 4000;
    let hideTimer = null;

    function badge() {
        let element = document.getElementById(BADGE_ID);
        if (!element) {
            element = document.createElement("div");
            element.id = BADGE_ID;
            element.className = "offline-status";
            element.setAttribute("role", "status");
            element.setAttribute("aria-live", "polite");
            document.body.appendChild(element);
        }
        return element;
    }

    function show(text, kind, hideAfter) {
        const element = badge();
        element.textContent = text;
        element.dataset.kind = kind;
        element.hidden = false;
        clearTimeout(hideTimer);
        if (hideAfter) {
            hideTimer = setTimeout(() => { element.hidden = true; }, hideAfter);
        }
    }

    function hide() {
        const element = document.getElementById(BADGE_ID);
        if (element) {
            element.hidden = true;
        }
    }

    function savedOn(timestamp) {
        const format = { day: "numeric", month: "numeric", hour: "2-digit", minute: "2-digit" };
        return new Date(timestamp).toLocaleString("cs-CZ", format);
    }

    function showOffline() {
        show("Offline – čteš uložené stránky. Výpočty a asistent potřebují připojení.", "offline");
    }

    navigator.serviceWorker.addEventListener("message", (event) => {
        const message = event.data || {};
        if (!navigator.onLine) {
            return;
        }
        if (message.type === "offline-progress") {
            show(`Ukládám stránky pro čtení offline: ${Math.round((100 * message.done) / message.total)} %`, "saving");
        } else if (message.type === "offline-ready" && message.fresh) {
            if (message.failed) {
                const text = "Některé stránky se pro offline nepodařilo uložit, zkusím to při dalším načtení.";
                show(text, "warning", READY_MILLISECONDS);
            } else {
                show(`Uloženo pro čtení offline (${savedOn(message.savedAt)})`, "ready", READY_MILLISECONDS);
            }
        }
    });

    window.addEventListener("offline", showOffline);
    window.addEventListener("online", hide);

    window.addEventListener("load", () => {
        if (!navigator.onLine) {
            showOffline();
        }
        navigator.serviceWorker.register(SERVICE_WORKER_URL)
            .then(() => navigator.serviceWorker.ready)
            .then((registration) => {
                if (navigator.onLine && registration.active) {
                    registration.active.postMessage({ type: "warm-up" });
                }
                // Asks the browser not to evict the stored pages when space runs low.
                if (navigator.storage && navigator.storage.persist) {
                    navigator.storage.persist();
                }
            })
            .catch(() => undefined);
    });
})();
