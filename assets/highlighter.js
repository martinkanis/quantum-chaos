// Text highlighter: select text with the mouse (on a phone or tablet hold it, or swipe a finger sideways across it),
// then highlight or underline it in one of nine pastel colours; a tap on a mark changes or removes it, and selected
// text that is marked can be erased from its marks. The same toolbar asks Claude to explain the selection or to
// expand it into a new topic (assets/assistant.js).
// The marks are painted with the CSS Custom Highlight API, so the DOM that Dash (React) renders is never changed,
// and they are kept in this browser's localStorage, anchored to the page container (ids in data-highlight-roots,
// set in ui/layout.py) by text offsets and the text around them, so they survive edits elsewhere on the page.
(function () {
    "use strict";

    if (!window.CSS || !CSS.highlights || typeof Highlight === "undefined") {
        return;
    }

    const ROOTS_ATTRIBUTE = "data-highlight-roots";
    const STORAGE_KEY = "qc-highlights";
    const PREFERENCES_KEY = "qc-highlighter-preferences";
    const CONTEXT_LENGTH = 32;
    const MAX_MARKS = 5000;
    const KINDS = ["mark", "underline"];
    const COLORS = [
        {name: "Žlutá", fill: "#fff1a6", line: "#e0b814"},
        {name: "Broskvová", fill: "#ffdabb", line: "#ec9549"},
        {name: "Korálová", fill: "#ffcbc4", line: "#e5715f"},
        {name: "Růžová", fill: "#fbcbe2", line: "#d96fa6"},
        {name: "Levandulová", fill: "#e2d8fb", line: "#9580e4"},
        {name: "Modrá", fill: "#d0e4fd", line: "#5b98ea"},
        {name: "Tyrkysová", fill: "#c5eeec", line: "#38aea7"},
        {name: "Mátová", fill: "#cff2d6", line: "#56ba72"},
        {name: "Limetková", fill: "#e6f3b8", line: "#97b934"},
    ];
    // Text inside these elements is neither highlighted nor counted in the anchors: MathJax keeps a hidden copy of
    // every formula as text, and charts, tables and form controls change on their own.
    const SKIPPED = "mjx-container, script, style, noscript, svg, canvas, textarea, select, button, " +
        ".js-plotly-plot, .dash-table-container, .dash-dropdown, #qc-highlighter";
    // A tap or a swipe that starts here belongs to the control, not to the highlighter.
    const INTERACTIVE = "a, button, summary, label, input, select, textarea, [contenteditable], [role='button'], " +
        "canvas, .js-plotly-plot, .dash-table-container, .dash-dropdown";
    const WORD_CHARACTER = /[\p{L}\p{N}_]/u;
    const TAP_DISTANCE = 10;
    const TAP_MILLISECONDS = 600;
    const SWIPE_START_DISTANCE = 8;
    const REPAINT_DELAY = 150;
    const REPAINT_MAX_WAIT = 600;
    // Any ::highlight() rule makes each style recalculation in Chromium several times slower, and MathJax recalculates
    // styles for every formula it typesets (the Theory page typeset in 20 s instead of 12 s with one rule and in 60 s
    // with all 18, measured in headless Chromium).
    // So the stylesheet holds only the colours in use, and while the page is busy changing it is switched off and
    // the marks wait until the page calms down. Swiping waits too: a touchmove listener that may cancel scrolling
    // makes the browser ask the busy page before every scroll.
    const BUSY_MUTATIONS = 40;
    const BUSY_QUIET_DELAY = 400;
    const BUSY_MAX_WAIT = 3000;
    const TOOLBAR_GAP = 8;
    const TOUCH_TOOLBAR_GAP = 28;
    // A tap on the toolbar may clear the selection on a phone; for this long that does not close the toolbar.
    const TOOLBAR_GRACE_MILLISECONDS = 800;

    const highlights = new Map();
    let marks = loadMarks();
    let preferences = loadPreferences();
    let liveRanges = new Map();
    let markedFormulas = new Set();
    // erasable: the pending selection covers text of a mark, so the toolbar offers to erase it.
    let state = {mode: null, pending: null, editing: null, erasable: false};
    let rootIds = null;
    let toolbar = null;
    let lastPointerType = "mouse";
    let mouseIsDown = false;
    let tap = null;
    let swipe = {phase: "idle"};
    let toolbarTouchedAt = 0;
    let selectionTimer = 0;
    let repaintTimer = 0;
    let repaintDue = 0;
    let pendingMutations = 0;
    let colorStyle = null;
    let swipeListening = false;
    let positionFrame = 0;

    // ---- Storage ---------------------------------------------------------------------------------------------

    function isColor(value) {
        return Number.isInteger(value) && value >= 0 && value < COLORS.length;
    }

    function isMark(value) {
        return Boolean(value) && typeof value.id === "string" && typeof value.root === "string" &&
            Number.isInteger(value.start) && Number.isInteger(value.end) && value.end > value.start &&
            typeof value.text === "string" && typeof value.prefix === "string" && typeof value.suffix === "string" &&
            KINDS.includes(value.kind) && isColor(value.color);
    }

    function readJson(key, fallback) {
        try {
            const raw = window.localStorage.getItem(key);
            return raw ? JSON.parse(raw) : fallback;
        } catch (error) {
            return fallback;
        }
    }

    function writeJson(key, value) {
        try {
            window.localStorage.setItem(key, JSON.stringify(value));
        } catch (error) {
            // Private mode or a full storage: the marks stay until the page is reloaded.
        }
    }

    function loadMarks() {
        const stored = readJson(STORAGE_KEY, []);
        return Array.isArray(stored) ? stored.filter(isMark) : [];
    }

    function saveMarks() {
        if (marks.length > MAX_MARKS) {
            marks = marks.slice().sort((a, b) => a.created - b.created).slice(-MAX_MARKS);
        }
        writeJson(STORAGE_KEY, marks);
    }

    function loadPreferences() {
        const stored = readJson(PREFERENCES_KEY, {});
        return {
            kind: stored && KINDS.includes(stored.kind) ? stored.kind : KINDS[0],
            color: stored && isColor(stored.color) ? stored.color : 0,
        };
    }

    function newId() {
        return Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
    }

    // ---- Anchors: a mark is a span of the page's text --------------------------------------------------------

    function pageRoots() {
        if (!rootIds) {
            const holder = document.querySelector("[" + ROOTS_ATTRIBUTE + "]");
            if (!holder) {
                return new Set();
            }
            rootIds = new Set(holder.getAttribute(ROOTS_ATTRIBUTE).split(/\s+/).filter(Boolean));
        }
        return rootIds;
    }

    function elementOf(node) {
        return node && (node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement);
    }

    function rootOf(node) {
        const roots = pageRoots();
        for (let element = elementOf(node); element; element = element.parentElement) {
            if (element.id && roots.has(element.id)) {
                return element;
            }
        }
        return null;
    }

    function isSkipped(node) {
        const element = elementOf(node);
        return !element || Boolean(element.closest(SKIPPED));
    }

    /** All counted text of a page: its text nodes in document order and where each starts in the joined text. */
    function textIndex(root) {
        const nodes = [];
        const starts = [];
        const parts = [];
        let length = 0;
        const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, {
            acceptNode(node) {
                if (node.nodeType === Node.TEXT_NODE) {
                    return node.length ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP;
                }
                return node.matches(SKIPPED) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_SKIP;
            },
        });
        for (let node = walker.nextNode(); node; node = walker.nextNode()) {
            nodes.push(node);
            starts.push(length);
            parts.push(node.data);
            length += node.length;
        }
        return {root, nodes, starts, text: parts.join(""), positions: new Map(nodes.map((node, i) => [node, i]))};
    }

    /** Offset in the page text of a DOM point; a point between elements or inside a formula counts the text before it. */
    function offsetOf(index, node, offset) {
        const position = index.positions.get(node);
        if (position !== undefined) {
            return index.starts[position] + offset;
        }
        const point = document.createRange();
        point.setStart(node, offset);
        let low = 0;
        let high = index.nodes.length;
        while (low < high) {
            const middle = (low + high) >> 1;
            if (point.comparePoint(index.nodes[middle], 0) > 0) {
                high = middle;
            } else {
                low = middle + 1;
            }
        }
        return low < index.nodes.length ? index.starts[low] : index.text.length;
    }

    /** DOM point of a text offset; a start goes to the beginning of the next node, an end stays at the end of its node. */
    function pointAt(index, offset, isEnd) {
        let low = 0;
        let high = index.nodes.length - 1;
        let found = 0;
        while (low <= high) {
            const middle = (low + high) >> 1;
            const start = index.starts[middle];
            if (isEnd ? start < offset : start <= offset) {
                found = middle;
                low = middle + 1;
            } else {
                high = middle - 1;
            }
        }
        return {node: index.nodes[found], offset: offset - index.starts[found]};
    }

    /** The selected text of a page as offsets, without the white space at its ends; null if nothing counts. */
    function spanOf(range) {
        const root = rootOf(range.commonAncestorContainer);
        if (!root) {
            return null;
        }
        const index = textIndex(root);
        if (!index.nodes.length) {
            return null;
        }
        const trimmed = trim(index.text, offsetOf(index, range.startContainer, range.startOffset),
            offsetOf(index, range.endContainer, range.endOffset));
        return trimmed ? {index, start: trimmed.start, end: trimmed.end} : null;
    }

    function trim(text, start, end) {
        while (start < end && /\s/.test(text[start])) {
            start += 1;
        }
        while (end > start && /\s/.test(text[end - 1])) {
            end -= 1;
        }
        return end > start ? {start, end} : null;
    }

    function describe(index, start, end, kind, color, created) {
        return {
            id: newId(),
            root: index.root.id,
            start,
            end,
            text: index.text.slice(start, end),
            prefix: index.text.slice(Math.max(0, start - CONTEXT_LENGTH), start),
            suffix: index.text.slice(end, end + CONTEXT_LENGTH),
            kind,
            color,
            created: created || Date.now(),
        };
    }

    function nearestOccurrence(text, needle, around) {
        let best = -1;
        for (let at = text.indexOf(needle); at >= 0; at = text.indexOf(needle, at + 1)) {
            if (best < 0 || Math.abs(at - around) < Math.abs(best - around)) {
                best = at;
            } else if (at > around) {
                break;
            }
        }
        return best;
    }

    /** Where the marked text is now: at its offsets if the page did not change, else next to the same neighbours. */
    function locate(index, mark) {
        const text = index.text;
        if (text.slice(mark.start, mark.end) === mark.text &&
            text.slice(Math.max(0, mark.start - mark.prefix.length), mark.start) === mark.prefix) {
            return mark.start;
        }
        const searches = [
            [mark.prefix + mark.text + mark.suffix, mark.prefix.length],
            [mark.prefix + mark.text, mark.prefix.length],
            [mark.text + mark.suffix, 0],
            [mark.text, 0],
        ];
        for (const [needle, shift] of searches) {
            const found = nearestOccurrence(text, needle, mark.start - shift);
            if (found >= 0) {
                return found + shift;
            }
        }
        return -1;
    }

    function rangeOf(index, start, end) {
        const from = pointAt(index, start, false);
        const to = pointAt(index, end, true);
        const range = document.createRange();
        range.setStart(from.node, from.offset);
        range.setEnd(to.node, to.offset);
        return range;
    }

    function liveSpan(index, mark) {
        const range = liveRanges.get(mark.id);
        return range ? {start: offsetOf(index, range.startContainer, range.startOffset),
            end: offsetOf(index, range.endContainer, range.endOffset)} : null;
    }

    // ---- Painting --------------------------------------------------------------------------------------------

    function highlightName(kind, color) {
        return "qc-" + kind + "-" + color;
    }

    function installHighlights() {
        KINDS.forEach((kind, priority) => {
            COLORS.forEach((color, i) => {
                const highlight = new Highlight();
                highlight.priority = priority;
                CSS.highlights.set(highlightName(kind, i), highlight);
                highlights.set(highlightName(kind, i), highlight);
            });
        });
        colorStyle = document.createElement("style");
        colorStyle.id = "qc-highlighter-colors";
        document.head.appendChild(colorStyle);
        // Dash is about to render the pages and MathJax to typeset them: the first repaint ends this.
        setBusy(true);
    }

    function isBusy() {
        return colorStyle.media !== "all";
    }

    function setBusy(busy) {
        colorStyle.media = busy ? "not all" : "all";
        if (swipeListening === busy) {
            swipeListening = !busy;
            const method = busy ? "removeEventListener" : "addEventListener";
            document[method]("touchmove", onTouchMove, {capture: true, passive: false});
        }
    }

    function colorRules(kind, i) {
        const color = COLORS[i];
        // Formulas are drawn as SVG, which the Highlight API does not paint, so they get the colour directly.
        if (kind === "mark") {
            return "::highlight(" + highlightName(kind, i) + ") { background-color: " + color.fill + "; }\n" +
                "mjx-container[data-qc-mark='" + i + "'] > svg { background-color: " + color.fill + "; }";
        }
        return "::highlight(" + highlightName(kind, i) + ") { text-decoration-line: underline; " +
            "text-decoration-color: " + color.line + "; text-decoration-thickness: 0.14em; }\n" +
            "mjx-container[data-qc-underline='" + i + "'] > svg { box-shadow: inset 0 -0.14em 0 " + color.line + "; }";
    }

    function updateColorStyle() {
        const rules = [];
        KINDS.forEach((kind) => COLORS.forEach((color, i) => {
            if (highlights.get(highlightName(kind, i)).size) {
                rules.push(colorRules(kind, i));
            }
        }));
        const css = rules.join("\n");
        if (colorStyle.textContent !== css) {
            colorStyle.textContent = css;
        }
        setBusy(false);
    }

    function repaint() {
        pendingMutations = 0;
        highlights.forEach((highlight) => highlight.clear());
        liveRanges = new Map();
        const formulas = new Map();
        const marksByRoot = new Map();
        marks.forEach((mark) => {
            if (!marksByRoot.has(mark.root)) {
                marksByRoot.set(mark.root, []);
            }
            marksByRoot.get(mark.root).push(mark);
        });
        marksByRoot.forEach((rootMarks, rootId) => {
            const root = document.getElementById(rootId);
            const index = root && textIndex(root);
            if (!index || !index.nodes.length) {
                return;
            }
            const rootFormulas = Array.from(root.querySelectorAll("mjx-container"));
            rootMarks.forEach((mark) => {
                const start = locate(index, mark);
                if (start < 0) {
                    return;
                }
                const range = rangeOf(index, start, start + mark.text.length);
                liveRanges.set(mark.id, range);
                highlights.get(highlightName(mark.kind, mark.color)).add(range);
                rootFormulas.forEach((formula) => {
                    if (range.intersectsNode(formula)) {
                        formulas.set(formula, Object.assign(formulas.get(formula) || {}, {[mark.kind]: mark.color}));
                    }
                });
            });
        });
        markedFormulas.forEach((formula) => {
            if (!formulas.has(formula)) {
                KINDS.forEach((kind) => formula.removeAttribute("data-qc-" + kind));
            }
        });
        formulas.forEach((colors, formula) => {
            KINDS.forEach((kind) => {
                if (colors[kind] === undefined) {
                    formula.removeAttribute("data-qc-" + kind);
                } else {
                    formula.setAttribute("data-qc-" + kind, String(colors[kind]));
                }
            });
        });
        markedFormulas = new Set(formulas.keys());
        updateColorStyle();
        if (state.mode === "edit" && !liveRanges.has(state.editing)) {
            hideToolbar();
        } else if (state.mode) {
            schedulePosition();
        }
    }

    function scheduleRepaint() {
        clearTimeout(repaintTimer);
        const now = Date.now();
        const busy = isBusy();
        repaintDue = repaintDue || now + (busy ? BUSY_MAX_WAIT : REPAINT_MAX_WAIT);
        repaintTimer = setTimeout(() => {
            repaintDue = 0;
            repaint();
        }, Math.max(0, Math.min(busy ? BUSY_QUIET_DELAY : REPAINT_DELAY, repaintDue - now)));
    }

    function onMutations(mutations) {
        const relevant = mutations.filter((mutation) => {
            const element = elementOf(mutation.target);
            return element && !element.closest("#qc-highlighter, .js-plotly-plot");
        }).length;
        if (!relevant) {
            return;
        }
        pendingMutations += relevant;
        if (pendingMutations > BUSY_MUTATIONS && !isBusy()) {
            setBusy(true);
            repaintDue = 0;
        }
        scheduleRepaint();
    }

    // ---- Changes to the marks --------------------------------------------------------------------------------

    /** The marks with the text between start and end cut out of those of the page (and of the kind, if given). */
    function cutOut(index, start, end, kind) {
        const kept = [];
        marks.forEach((other) => {
            const span = other.root === index.root.id && (!kind || other.kind === kind) ? liveSpan(index, other) : null;
            if (!span || span.end <= start || span.start >= end) {
                kept.push(other);
                return;
            }
            [[span.start, start], [end, span.end]].forEach(([pieceStart, pieceEnd]) => {
                const piece = pieceStart < pieceEnd ? trim(index.text, pieceStart, pieceEnd) : null;
                if (piece) {
                    kept.push(describe(index, piece.start, piece.end, other.kind, other.color, other.created));
                }
            });
        });
        return kept;
    }

    /** Marks of one kind never overlap: the new one takes over the text that older ones had under it. */
    function insertMark(index, mark) {
        marks = cutOut(index, mark.start, mark.end, mark.kind).concat([mark]);
        saveMarks();
        repaint();
    }

    /** Whether some mark covers text of the selection (widened to whole words, as a new mark would be). */
    function isMarked(span) {
        const words = wholeWords(span.index, span.start, span.end);
        return marks.some((mark) => {
            const live = mark.root === span.index.root.id ? liveSpan(span.index, mark) : null;
            return Boolean(live) && live.start < words.end && live.end > words.start;
        });
    }

    /** Erases the selected words from the highlights and underlines; the rest of a longer mark stays. */
    function eraseMarks(range) {
        const span = spanOf(range);
        if (span) {
            const words = wholeWords(span.index, span.start, span.end);
            marks = cutOut(span.index, words.start, words.end, null);
            saveMarks();
            repaint();
        }
    }

    /**
     * A selection rarely ends inside a word on purpose (a finger is not precise), so a mark covers whole words.
     * The words end with their text node: the joined page text has no space between two paragraphs.
     */
    function wholeWords(index, start, end) {
        const text = index.text;
        const first = pointAt(index, start, false);
        const last = pointAt(index, end, true);
        const firstNodeStart = start - first.offset;
        const lastNodeEnd = end - last.offset + last.node.length;
        while (start > firstNodeStart && WORD_CHARACTER.test(text[start - 1])) {
            start -= 1;
        }
        while (end < lastNodeEnd && WORD_CHARACTER.test(text[end])) {
            end += 1;
        }
        return {start, end};
    }

    function addMark(range, kind, color) {
        const span = spanOf(range);
        if (span) {
            const words = wholeWords(span.index, span.start, span.end);
            insertMark(span.index, describe(span.index, words.start, words.end, kind, color));
        }
    }

    function markById(id) {
        return marks.find((mark) => mark.id === id) || null;
    }

    function changeMark(id, kind, color) {
        const mark = markById(id);
        const root = mark && document.getElementById(mark.root);
        if (!root) {
            return;
        }
        const index = textIndex(root);
        const span = liveSpan(index, mark);
        if (!span) {
            return;
        }
        marks = marks.filter((other) => other.id !== id);
        const changed = describe(index, span.start, span.end, kind, color, mark.created);
        changed.id = id;
        insertMark(index, changed);
    }

    function removeMark(id) {
        marks = marks.filter((mark) => mark.id !== id);
        saveMarks();
        repaint();
    }

    // ---- Toolbar ---------------------------------------------------------------------------------------------

    const TRASH_ICON = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" ' +
        'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
        '<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/></svg>';

    function buildToolbar() {
        const bar = document.createElement("div");
        bar.id = "qc-highlighter";
        bar.className = "qc-highlighter";
        bar.setAttribute("role", "toolbar");
        bar.setAttribute("aria-label", "Zvýraznění textu");
        bar.hidden = true;
        const swatches = COLORS.map((color, i) =>
            '<button type="button" class="qc-highlighter-swatch" data-color="' + i + '" title="' + color.name +
            '" aria-label="' + color.name + '" style="--qc-fill: ' + color.fill + "; --qc-line: " + color.line +
            '"></button>').join("");
        bar.innerHTML =
            '<div class="qc-highlighter-row">' +
            '<button type="button" class="qc-highlighter-kind" data-kind="mark" title="Zvýraznit barvou pozadí">' +
            '<span class="qc-highlighter-icon mark" aria-hidden="true">ab</span>Zvýraznit</button>' +
            '<button type="button" class="qc-highlighter-kind" data-kind="underline" title="Podtrhnout barevnou čarou">' +
            '<span class="qc-highlighter-icon underline" aria-hidden="true">ab</span>Podtrhnout</button>' +
            '<button type="button" class="qc-highlighter-remove" data-action="remove" ' +
            'title="Vymazat zvýraznění a podtržení">' + TRASH_ICON + "Vymazat</button>" +
            "</div>" +
            '<div class="qc-highlighter-colors">' + swatches + "</div>" +
            // Claude (assets/assistant.js) and the paragraph editor (assets/text_edit.js); each button shows only
            // when its script is on the page, the editor's only over an editable paragraph.
            '<div class="qc-highlighter-row qc-highlighter-assistant" hidden>' +
            '<button type="button" class="qc-highlighter-ask" data-assistant="explain" ' +
            'title="Claude vysvětlí označený text v okně">💡 Dovysvětlit</button>' +
            '<button type="button" class="qc-highlighter-ask" data-assistant="expand" ' +
            'title="Agent napíše o označeném textu novou stránku, kterou pak schválíš">➕ Rozvést na téma</button>' +
            '<button type="button" class="qc-highlighter-ask" data-text-edit ' +
            'title="Ručně přepsat odstavec, nadpis nebo popisek, ve kterém je označený text">✏️ Upravit text</button>' +
            "</div>";
        // Pressing a button must neither move the focus nor clear the selection it is about to mark.
        bar.addEventListener("mousedown", (event) => event.preventDefault());
        bar.addEventListener("click", onToolbarClick);
        document.body.appendChild(bar);
        return bar;
    }

    function shownMark() {
        return state.mode === "edit" ? markById(state.editing) : null;
    }

    function renderToolbar() {
        const current = shownMark() || preferences;
        const color = COLORS[current.color];
        toolbar.dataset.kind = current.kind;
        toolbar.style.setProperty("--qc-fill", color.fill);
        toolbar.style.setProperty("--qc-line", color.line);
        toolbar.querySelectorAll("[data-kind]").forEach((button) => {
            button.setAttribute("aria-pressed", String(button.dataset.kind === current.kind));
        });
        toolbar.querySelectorAll("[data-color]").forEach((button) => {
            button.setAttribute("aria-pressed", String(Number(button.dataset.color) === current.color));
        });
        toolbar.querySelector("[data-action='remove']").hidden = state.mode !== "edit" && !state.erasable;
        const range = activeRange();
        toolbar.querySelectorAll("[data-assistant]").forEach((button) => {
            button.hidden = !window.qcAssistant;
        });
        toolbar.querySelector("[data-text-edit]").hidden = !(window.qcTextEdit && window.qcTextEdit.editableAt(range));
        const row = toolbar.querySelector(".qc-highlighter-assistant");
        row.hidden = Array.from(row.querySelectorAll("button")).every((button) => button.hidden);
    }

    function showToolbar(nextState) {
        state = nextState;
        renderToolbar();
        toolbar.hidden = false;
        positionToolbar();
    }

    function hideToolbar() {
        state = {mode: null, pending: null, editing: null, erasable: false};
        if (toolbar) {
            toolbar.hidden = true;
        }
    }

    function activeRange() {
        return state.mode === "new" ? state.pending : liveRanges.get(state.editing);
    }

    function positionToolbar() {
        positionFrame = 0;
        const range = state.mode && activeRange();
        const rects = range ? Array.from(range.getClientRects()).filter((rect) => rect.width > 0) : [];
        if (!rects.length) {
            hideToolbar();
            return;
        }
        const first = rects[0];
        const last = rects[rects.length - 1];
        const viewport = window.visualViewport;
        const viewLeft = viewport ? viewport.offsetLeft : 0;
        const viewTop = viewport ? viewport.offsetTop : 0;
        const viewWidth = viewport ? viewport.width : window.innerWidth;
        const viewHeight = viewport ? viewport.height : window.innerHeight;
        const header = document.querySelector(".site-header");
        const topLimit = Math.max(viewTop, header ? header.getBoundingClientRect().bottom : 0) + TOOLBAR_GAP;
        const width = toolbar.offsetWidth;
        const height = toolbar.offsetHeight;
        const isTouch = lastPointerType !== "mouse";
        // Phones and tablets show their own selection menu above the text, so the toolbar goes below it there.
        const above = first.top - height - TOOLBAR_GAP;
        const below = last.bottom + (isTouch ? TOUCH_TOOLBAR_GAP : TOOLBAR_GAP);
        const fitsAbove = above >= topLimit;
        const fitsBelow = below + height <= viewTop + viewHeight - TOOLBAR_GAP;
        const useBelow = isTouch ? fitsBelow || !fitsAbove : !fitsAbove && fitsBelow;
        const anchor = useBelow ? last : first;
        const left = anchor.left + anchor.width / 2 - width / 2;
        const maxLeft = viewLeft + viewWidth - width - TOOLBAR_GAP;
        toolbar.style.left = Math.max(viewLeft + TOOLBAR_GAP, Math.min(left, maxLeft)) + "px";
        toolbar.style.top = (useBelow ? below : above) + "px";
    }

    function schedulePosition() {
        if (state.mode && !positionFrame) {
            positionFrame = window.requestAnimationFrame(positionToolbar);
        }
    }

    function restoreSelection(range) {
        const selection = document.getSelection();
        selection.removeAllRanges();
        selection.addRange(range.cloneRange());
    }

    function onToolbarClick(event) {
        const button = event.target.closest("button");
        if (!button) {
            return;
        }
        toolbarTouchedAt = Date.now();
        const editing = shownMark();
        if (button.dataset.assistant) {
            const range = activeRange();
            if (range && window.qcAssistant) {
                window.qcAssistant.ask(button.dataset.assistant, range.cloneRange());
            }
            document.getSelection().removeAllRanges();
            hideToolbar();
        } else if (button.dataset.textEdit !== undefined) {
            const range = activeRange();
            if (range && window.qcTextEdit) {
                window.qcTextEdit.open(range.cloneRange());
            }
            document.getSelection().removeAllRanges();
            hideToolbar();
        } else if (button.dataset.kind) {
            preferences = {kind: button.dataset.kind, color: editing ? editing.color : preferences.color};
            writeJson(PREFERENCES_KEY, preferences);
            if (editing) {
                changeMark(editing.id, button.dataset.kind, editing.color);
            } else if (state.pending) {
                restoreSelection(state.pending);
            }
            renderToolbar();
        } else if (button.dataset.color !== undefined) {
            const color = Number(button.dataset.color);
            preferences = {kind: editing ? editing.kind : preferences.kind, color};
            writeJson(PREFERENCES_KEY, preferences);
            if (editing) {
                changeMark(editing.id, editing.kind, color);
                renderToolbar();
            } else if (state.pending) {
                addMark(state.pending, preferences.kind, color);
                document.getSelection().removeAllRanges();
                hideToolbar();
            }
        } else if (button.dataset.action === "remove") {
            if (editing) {
                removeMark(editing.id);
            } else if (state.pending) {
                eraseMarks(state.pending);
                document.getSelection().removeAllRanges();
            }
            hideToolbar();
        }
    }

    // ---- Selecting text --------------------------------------------------------------------------------------

    function isTyping() {
        const active = document.activeElement;
        return Boolean(active) && active.matches("input, textarea, select, [contenteditable]");
    }

    function evaluateSelection() {
        clearTimeout(selectionTimer);
        const selection = document.getSelection();
        const range = selection && selection.rangeCount && !selection.isCollapsed ? selection.getRangeAt(0) : null;
        const span = range && !isTyping() ? spanOf(range) : null;
        if (span) {
            showToolbar({mode: "new", pending: range.cloneRange(), editing: null, erasable: isMarked(span)});
        } else if (state.mode === "new" && Date.now() - toolbarTouchedAt > TOOLBAR_GRACE_MILLISECONDS) {
            hideToolbar();
        }
    }

    /** The mark under a point; of overlapping ones the newest. */
    function markAt(x, y) {
        let found = null;
        liveRanges.forEach((range, id) => {
            const hit = Array.from(range.getClientRects()).some((rect) =>
                rect.width > 0 && x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom);
            const mark = hit ? markById(id) : null;
            if (mark && (!found || mark.created > found.created)) {
                found = mark;
            }
        });
        return found;
    }

    function caretAt(x, y) {
        if (document.caretPositionFromPoint) {
            const position = document.caretPositionFromPoint(x, y);
            return position ? {node: position.offsetNode, offset: position.offset} : null;
        }
        if (document.caretRangeFromPoint) {
            const range = document.caretRangeFromPoint(x, y);
            return range ? {node: range.startContainer, offset: range.startOffset} : null;
        }
        return null;
    }

    /** A caret in highlightable text right under the finger; the caret alone snaps to text even from a margin. */
    function textCaretAt(x, y) {
        const caret = caretAt(x, y);
        if (!caret || caret.node.nodeType !== Node.TEXT_NODE || isSkipped(caret.node) || !rootOf(caret.node)) {
            return null;
        }
        const around = document.createRange();
        around.setStart(caret.node, Math.max(0, caret.offset - 1));
        around.setEnd(caret.node, Math.min(caret.node.length, caret.offset + 1));
        const onText = Array.from(around.getClientRects()).some((rect) =>
            x >= rect.left - TAP_DISTANCE && x <= rect.right + TAP_DISTANCE && y >= rect.top && y <= rect.bottom);
        return onText ? caret : null;
    }

    /** Wide tables and formulas scroll sideways, so a sideways swipe over them keeps scrolling. */
    function insideSideScroller(element) {
        for (let current = element; current && current !== document.body; current = current.parentElement) {
            if (current.scrollWidth > current.clientWidth + 1) {
                const overflow = window.getComputedStyle(current).overflowX;
                if (overflow === "auto" || overflow === "scroll") {
                    return true;
                }
            }
        }
        return false;
    }

    /** A finger is not precise, so a swiped selection grows to whole words. */
    function snapSelectionToWords() {
        const selection = document.getSelection();
        if (!selection.rangeCount || selection.isCollapsed) {
            return;
        }
        const range = selection.getRangeAt(0);
        let startNode = range.startContainer;
        let start = range.startOffset;
        let endNode = range.endContainer;
        let end = range.endOffset;
        if (startNode.nodeType === Node.TEXT_NODE) {
            while (start > 0 && WORD_CHARACTER.test(startNode.data[start - 1])) {
                start -= 1;
            }
        }
        if (endNode.nodeType === Node.TEXT_NODE) {
            while (end < endNode.length && WORD_CHARACTER.test(endNode.data[end])) {
                end += 1;
            }
        }
        selection.setBaseAndExtent(startNode, start, endNode, end);
    }

    function onPointerDown(event) {
        lastPointerType = event.pointerType || "mouse";
        if (toolbar.contains(event.target)) {
            toolbarTouchedAt = Date.now();
            return;
        }
        mouseIsDown = lastPointerType === "mouse" && event.button === 0;
        tap = {x: event.clientX, y: event.clientY, at: Date.now(), pointerId: event.pointerId};
        hideToolbar();
    }

    function onPointerUp(event) {
        if (toolbar.contains(event.target)) {
            return;
        }
        const wasMouseDrag = mouseIsDown;
        mouseIsDown = false;
        const isTap = tap && tap.pointerId === event.pointerId && Date.now() - tap.at < TAP_MILLISECONDS &&
            Math.hypot(event.clientX - tap.x, event.clientY - tap.y) < TAP_DISTANCE;
        tap = null;
        const target = elementOf(event.target);
        // The browser settles the selection only after the button is released.
        setTimeout(() => {
            const selection = document.getSelection();
            const collapsed = !selection || selection.isCollapsed;
            if (isTap && collapsed && target && !target.closest(INTERACTIVE)) {
                const mark = markAt(event.clientX, event.clientY);
                if (mark) {
                    showToolbar({mode: "edit", pending: null, editing: mark.id});
                    return;
                }
            }
            if (wasMouseDrag) {
                evaluateSelection();
            }
        }, 0);
    }

    function onSelectionChange() {
        if (mouseIsDown || swipe.phase === "selecting") {
            return;
        }
        clearTimeout(selectionTimer);
        selectionTimer = setTimeout(evaluateSelection, 250);
    }

    function onTouchStart(event) {
        swipe = {phase: "idle"};
        if (event.touches.length !== 1 || toolbar.contains(event.target)) {
            return;
        }
        // Zoomed in, a sideways swipe moves the view.
        if (window.visualViewport && window.visualViewport.scale > 1.05) {
            return;
        }
        const target = elementOf(event.target);
        if (!target || target.closest(INTERACTIVE) || !rootOf(target) || insideSideScroller(target)) {
            return;
        }
        const touch = event.touches[0];
        swipe = {phase: "pending", x: touch.clientX, y: touch.clientY};
    }

    // A sideways swipe across text selects it; any other direction scrolls the page as usual.
    function onTouchMove(event) {
        if (swipe.phase === "idle" || event.touches.length !== 1) {
            swipe = {phase: "idle"};
            return;
        }
        const touch = event.touches[0];
        if (swipe.phase === "pending") {
            const dx = touch.clientX - swipe.x;
            const dy = touch.clientY - swipe.y;
            if (Math.hypot(dx, dy) < SWIPE_START_DISTANCE) {
                return;
            }
            const anchor = event.cancelable && Math.abs(dx) > 1.5 * Math.abs(dy) ? textCaretAt(swipe.x, swipe.y) : null;
            if (!anchor) {
                swipe = {phase: "idle"};
                return;
            }
            swipe = {phase: "selecting", anchor, root: rootOf(anchor.node)};
            hideToolbar();
        }
        event.preventDefault();
        const focus = caretAt(touch.clientX, touch.clientY);
        if (focus && rootOf(focus.node) === swipe.root) {
            document.getSelection().setBaseAndExtent(swipe.anchor.node, swipe.anchor.offset, focus.node, focus.offset);
        }
    }

    function onTouchEnd() {
        if (swipe.phase === "selecting") {
            swipe = {phase: "idle"};
            snapSelectionToWords();
            evaluateSelection();
        }
        swipe = {phase: "idle"};
    }

    // ---- Start -----------------------------------------------------------------------------------------------

    function start() {
        installHighlights();
        toolbar = buildToolbar();
        document.addEventListener("pointerdown", onPointerDown, true);
        document.addEventListener("pointerup", onPointerUp, true);
        document.addEventListener("pointercancel", () => { mouseIsDown = false; tap = null; }, true);
        document.addEventListener("selectionchange", onSelectionChange);
        document.addEventListener("touchstart", onTouchStart, {capture: true, passive: true});
        document.addEventListener("touchend", onTouchEnd, true);
        document.addEventListener("touchcancel", () => { swipe = {phase: "idle"}; }, true);
        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                hideToolbar();
            }
        });
        window.addEventListener("scroll", schedulePosition, {capture: true, passive: true});
        window.addEventListener("resize", schedulePosition);
        if (window.visualViewport) {
            window.visualViewport.addEventListener("resize", schedulePosition);
            window.visualViewport.addEventListener("scroll", schedulePosition);
        }
        // Another tab of the app changed the marks.
        window.addEventListener("storage", (event) => {
            if (event.key === STORAGE_KEY) {
                marks = loadMarks();
                repaint();
            }
        });
        // Dash renders pages and results, MathJax typesets formulas: the marks are placed again on the new text.
        new MutationObserver(onMutations).observe(document.body, {childList: true, subtree: true, characterData: true});
        scheduleRepaint();
    }

    if (document.body) {
        start();
    } else {
        document.addEventListener("DOMContentLoaded", start);
    }
})();
