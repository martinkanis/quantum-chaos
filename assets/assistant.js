// Bridge between the highlighter toolbar (assets/highlighter.js) and the assistant in Dash (ui/assistant_panel.py):
// sends the selected text with its context to the callbacks, opens the pop-up at once, closes it with Escape or
// a click beside it, and shows a browser notification when an agent finishes. Ids are the ones in ui/ids.py.
// Formulas go along as their TeX source: MathJax typesets them as SVG drawings, whose selection has no text.
(function () {
    "use strict";

    const ROOTS_ATTRIBUTE = "data-highlight-roots";
    const REQUEST = "assistant-request";
    const MODAL = "assistant-modal";
    const TITLE = "assistant-modal-title";
    const BODY = "assistant-modal-body";
    const MESSAGE = "assistant-modal-message";
    const START_BUTTON = "assistant-start-button";
    const MODAL_CLASS = "assistant-modal";
    const OPEN_MODAL_CLASS = "assistant-modal open";
    const NOTIFIED_KEY = "qc-agents-notified";
    const FORMULA = "mjx-container";
    const FORMULA_MATHML = "mjx-assistive-mml";
    const BLOCKS = "p, li, td, th, dd, dt, blockquote, figcaption, h1, h2, h3, h4, h5, h6";
    const HEADINGS = "h2, h3";
    // Charts, tables and controls hold no prose; the SVG of a formula is read through its TeX instead.
    const SKIPPED = "script, style, svg, .js-plotly-plot, .dash-table-container, .dash-dropdown";
    const PARAGRAPH_LENGTH = 4000;
    const NEIGHBOUR_LENGTH = 1200;
    const SELECTION_LENGTH = 2000;
    const TITLE_LENGTH = 300;
    const TITLES = {explain: "Dovysvětlení", expand: "Rozvedení tématu"};
    const WAITING = {
        explain: "Claude píše vysvětlení, obvykle do půl minuty…",
        expand: "Připravuji rozvedení…",
    };
    const WAITING_FORMULA = "Claude rozepisuje vzorec krok za krokem, obvykle do minuty…";
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
                title = textOf(heading, TITLE_LENGTH);
            }
        });
        return title;
    }

    // ---- Text with formulas as TeX ---------------------------------------------------------------------------

    /** TeX of every formula MathJax typeset, by its mjx-container; the list also keeps items of re-rendered text. */
    function formulaSources() {
        const sources = new Map();
        const mathJax = window.MathJax;
        const typeset = mathJax && mathJax.startup && mathJax.startup.document && mathJax.startup.document.math;
        if (typeset) {
            for (const item of typeset) {
                if (item.typesetRoot) {
                    sources.set(item.typesetRoot, {tex: item.math, display: Boolean(item.display)});
                }
            }
        }
        return sources;
    }

    /** The formula as its author wrote it, $…$ in a line and $$ … $$ on its own; MathML when the source is gone. */
    function formulaText(formula, sources) {
        const source = sources.get(formula);
        if (source) {
            return source.display ? "$$ " + source.tex.trim() + " $$" : "$" + source.tex.trim() + "$";
        }
        const mathml = formula.querySelector(FORMULA_MATHML);
        return mathml ? mathml.innerHTML.trim() : "";
    }

    /** Pieces of the text inside the range in document order: text, a break after each block, TeX of formulas. */
    function piecesOf(range, sources, node, pieces) {
        if (!range.intersectsNode(node)) {
            return;
        }
        if (node.nodeType === Node.TEXT_NODE) {
            const start = node === range.startContainer ? range.startOffset : 0;
            const end = node === range.endContainer ? range.endOffset : node.length;
            pieces.push({text: node.data.slice(start, end), formula: false});
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            if (node.matches(FORMULA)) {
                pieces.push({text: formulaText(node, sources), formula: true});
                return;
            }
            if (node.matches(SKIPPED)) {
                return;
            }
            node.childNodes.forEach((child) => piecesOf(range, sources, child, pieces));
            if (node.matches(BLOCKS)) {
                pieces.push({text: "\n", formula: false});
            }
        }
    }

    /** The pieces as one text within the limit; a formula that does not fit is left out whole, so no TeX breaks. */
    function joinPieces(pieces, limit) {
        let text = "";
        let formulas = 0;
        for (const piece of pieces) {
            if (text.length + piece.text.length > limit) {
                if (!piece.formula) {
                    text += piece.text.slice(0, limit - text.length);
                }
                break;
            }
            text += piece.text;
            formulas += piece.formula ? 1 : 0;
        }
        return {text: text.replace(/\s+/g, " ").trim(), formulas};
    }

    /** Text inside the range with each formula as TeX, and how many formulas it holds. */
    function rangeText(range, limit, sources) {
        const pieces = [];
        const ancestor = elementOf(range.commonAncestorContainer);
        const enclosing = ancestor && ancestor.closest(FORMULA);
        piecesOf(range, sources, enclosing || range.commonAncestorContainer, pieces);
        return joinPieces(pieces, limit);
    }

    function elementText(element, limit, sources) {
        if (!element) {
            return "";
        }
        const range = document.createRange();
        range.selectNodeContents(element);
        return rangeText(range, limit, sources).text;
    }

    /** The outermost element holding nothing but the given one: a display formula sits alone in its Markdown block. */
    function loneWrapper(element, root) {
        let wrapper = element;
        while (wrapper.parentElement && wrapper.parentElement !== root && wrapper.parentElement.children.length === 1) {
            wrapper = wrapper.parentElement;
        }
        return wrapper;
    }

    /** The paragraph (list item, cell…) around the node; a display formula has none, so its own block stands in. */
    function blockAround(node, root) {
        const element = elementOf(node);
        if (!element || !root) {
            return null;
        }
        const start = element.closest(FORMULA) || element;
        return start.closest(BLOCKS) || loneWrapper(start, root);
    }

    /**
     * Context of the selection: the block it starts in and, around a formula, the blocks before and after it too,
     * because a formula is introduced by the paragraph before it and read in the paragraph after it.
     */
    function surroundingText(range, root, withNeighbours, sources) {
        const block = blockAround(range.startContainer, root);
        if (!block) {
            return "";
        }
        if (!withNeighbours) {
            return elementText(block, PARAGRAPH_LENGTH, sources);
        }
        const wrapper = loneWrapper(block, root);
        const before = elementText(wrapper.previousElementSibling, NEIGHBOUR_LENGTH, sources);
        const after = elementText(wrapper.nextElementSibling, NEIGHBOUR_LENGTH, sources);
        const own = elementText(block, PARAGRAPH_LENGTH - before.length - after.length - 2, sources);
        return [before, own, after].filter(Boolean).join(" ");
    }

    function contextOf(range) {
        const root = pageRoot(range.startContainer);
        const sources = formulaSources();
        const selected = rangeText(range, SELECTION_LENGTH, sources);
        return {
            page_id: root ? root.id : "",
            page_title: root ? textOf(root.querySelector("h1"), TITLE_LENGTH) : "",
            section_title: root ? sectionTitle(root, range.startContainer) : "",
            selection: selected.text,
            paragraph: surroundingText(range, root, selected.formulas > 0, sources),
            has_formula: selected.formulas > 0,
        };
    }

    // ---- Pop-up and notifications ----------------------------------------------------------------------------

    function askForNotifications() {
        if ("Notification" in window && Notification.permission === "default") {
            Notification.requestPermission().catch(() => {});
        }
    }

    function ask(action, range) {
        const context = contextOf(range);
        setProps(MODAL, {className: OPEN_MODAL_CLASS});
        setProps(TITLE, {children: TITLES[action]});
        setProps(BODY, {children: action === "explain" && context.has_formula ? WAITING_FORMULA : WAITING[action]});
        setProps(MESSAGE, {children: ""});
        setProps(REQUEST, {data: Object.assign({action, nonce: Date.now()}, context)});
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
        } else if (event.target.closest("#" + START_BUTTON)) {
            // The agent starts here, so this click is the user gesture the permission prompt needs.
            askForNotifications();
        }
    });

    window.qcAssistant = {ask, notify};
})();
