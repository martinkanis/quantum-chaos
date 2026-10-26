// Bridge between the highlighter toolbar (assets/highlighter.js) and the assistant in Dash (ui/assistant_panel.py):
// sends the selected text with its context to the callbacks, opens the pop-up at once, closes it with Escape or
// a click beside it, and shows a browser notification when an agent finishes. Ids are the ones in ui/ids.py.
(function () {
    "use strict";

    const ROOTS_ATTRIBUTE = "data-highlight-roots";
    const REQUEST = "assistant-request";
    const MODAL = "assistant-modal";
    const TITLE = "assistant-modal-title";
    const BODY = "assistant-modal-body";
    const MESSAGE = "assistant-modal-message";
    const EXPAND_BUTTON = "assistant-expand-button";
    const MODAL_CLASS = "assistant-modal";
    const OPEN_MODAL_CLASS = "assistant-modal open";
    const NOTIFIED_KEY = "qc-agents-notified";
    const BLOCKS = "p, li, td, th, dd, dt, blockquote, figcaption, h1, h2, h3, h4, h5, h6";
    const HEADINGS = "h2, h3";
    const PARAGRAPH_LENGTH = 4000;
    const SELECTION_LENGTH = 2000;
    const TITLES = {explain: "Dovysvětlení", expand: "Rozvedení tématu"};
    const WAITING = {
        explain: "Claude píše vysvětlení, obvykle do půl minuty…",
        expand: "Spouštím agenta…",
    };
    const APP_TITLE = document.title;

    function setProps(id, props) {
        if (window.dash_clientside && window.dash_clientside.set_props) {
            window.dash_clientside.set_props(id, props);
        }
    }

    function elementOf(node) {
        return node && (node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement);
    }

    function pageRoot(node) {
        const holder = document.querySelector("[" + ROOTS_ATTRIBUTE + "]");
        const roots = new Set(holder ? holder.getAttribute(ROOTS_ATTRIBUTE).split(/\s+/) : []);
        for (let element = elementOf(node); element; element = element.parentElement) {
            if (element.id && roots.has(element.id)) {
                return element;
            }
        }
        return null;
    }

    function textOf(element, limit) {
        return element ? element.textContent.replace(/\s+/g, " ").trim().slice(0, limit) : "";
    }

    /** The chapter heading the selection sits under: the last h2/h3 before it on the page. */
    function sectionTitle(root, node) {
        let title = "";
        root.querySelectorAll(HEADINGS).forEach((heading) => {
            if (heading.compareDocumentPosition(node) & Node.DOCUMENT_POSITION_FOLLOWING) {
                title = textOf(heading, 300);
            }
        });
        return title;
    }

    function contextOf(range) {
        const start = elementOf(range.startContainer);
        const root = pageRoot(start);
        return {
            page_id: root ? root.id : "",
            page_title: root ? textOf(root.querySelector("h1"), 300) : "",
            section_title: root ? sectionTitle(root, range.startContainer) : "",
            selection: range.toString().replace(/\s+/g, " ").trim().slice(0, SELECTION_LENGTH),
            paragraph: textOf(start && start.closest(BLOCKS), PARAGRAPH_LENGTH),
        };
    }

    function askForNotifications() {
        if ("Notification" in window && Notification.permission === "default") {
            Notification.requestPermission().catch(() => {});
        }
    }

    function ask(action, range) {
        if (action === "expand") {
            askForNotifications();
        }
        setProps(MODAL, {className: OPEN_MODAL_CLASS});
        setProps(TITLE, {children: TITLES[action]});
        setProps(BODY, {children: WAITING[action]});
        setProps(MESSAGE, {children: ""});
        setProps(REQUEST, {data: Object.assign({action, nonce: Date.now()}, contextOf(range))});
    }

    function closeModal() {
        const modal = document.getElementById(MODAL);
        if (modal && modal.classList.contains("open")) {
            setProps(MODAL, {className: MODAL_CLASS});
        }
    }

    function readNotified() {
        try {
            const stored = JSON.parse(window.localStorage.getItem(NOTIFIED_KEY) || "[]");
            return new Set(Array.isArray(stored) ? stored : []);
        } catch (error) {
            return new Set();
        }
    }

    function show(title, body) {
        if (!("Notification" in window) || Notification.permission !== "granted") {
            return;
        }
        try {
            new Notification(title, {body, tag: "qc-agent"});
        } catch (error) {
            // Phones allow notifications only from a service worker; the agents panel still shows the state.
        }
    }

    /** Called by a callback with the agents state; each finished agent is announced once per browser. */
    function notify(state) {
        if (!state) {
            return;
        }
        const ready = state.ready || [];
        document.title = ready.length ? "(" + ready.length + ") " + APP_TITLE : APP_TITLE;
        const notified = readNotified();
        ready.forEach((job) => {
            if (!notified.has("ready:" + job.id)) {
                show("Agent dokončil téma – čeká na schválení", job.title || "");
                notified.add("ready:" + job.id);
            }
        });
        (state.deployed || []).forEach((job) => {
            if (!notified.has("deployed:" + job.id)) {
                show("Nové téma je nasazené", job.title || "");
                notified.add("deployed:" + job.id);
            }
        });
        try {
            window.localStorage.setItem(NOTIFIED_KEY, JSON.stringify(Array.from(notified).slice(-200)));
        } catch (error) {
            // Without storage a finished agent may be announced again after a reload.
        }
    }

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeModal();
        }
    });
    document.addEventListener("click", (event) => {
        if (event.target.id === MODAL) {
            closeModal();
        } else if (event.target.closest("#" + EXPAND_BUTTON)) {
            askForNotifications();
        }
    });

    window.qcAssistant = {ask, notify};
})();
