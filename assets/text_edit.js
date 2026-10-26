// Bridge between the highlighter toolbar (assets/highlighter.js) and the paragraph editor in Dash
// (ui/text_edit_panel.py): finds the editable paragraph under the selection by its pattern-matching id
// (ui/editable_text.py), opens the pop-up at once and asks the callback for the paragraph's source text.
// Escape closes the pop-up unless the reader is typing in it, so a stray key does not throw away an edit.
(function () {
    "use strict";

    const TYPE = "text-edit";
    const REQUEST = "text-edit-request";
    const MODAL = "text-edit-modal";
    const TEXT = "text-edit-text";
    const MESSAGE = "text-edit-message";
    const MODAL_CLASS = "assistant-modal";
    const OPEN_MODAL_CLASS = "assistant-modal open";

    function setProps(id, props) {
        if (window.dash_clientside && window.dash_clientside.set_props) {
            window.dash_clientside.set_props(id, props);
        }
    }

    function elementOf(node) {
        return node && (node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement);
    }

    /** The page and key of the editable paragraph around the node; Dash writes dict ids as JSON. */
    function blockOf(node) {
        for (let element = elementOf(node); element; element = element.parentElement) {
            if (element.id && element.id.charAt(0) === "{") {
                try {
                    const id = JSON.parse(element.id);
                    if (id.type === TYPE) {
                        return {page: id.page, key: id.key};
                    }
                } catch (error) {
                    // Another pattern-matching id; keep looking further up.
                }
            }
        }
        return null;
    }

    function editableAt(range) {
        return Boolean(range && blockOf(range.startContainer));
    }

    function open(range) {
        const block = range && blockOf(range.startContainer);
        if (!block) {
            return;
        }
        setProps(MODAL, {className: OPEN_MODAL_CLASS});
        setProps(TEXT, {value: ""});
        setProps(MESSAGE, {children: ""});
        setProps(REQUEST, {data: Object.assign({nonce: Date.now()}, block)});
    }

    document.addEventListener("keydown", (event) => {
        const modal = document.getElementById(MODAL);
        if (event.key === "Escape" && modal && modal.classList.contains("open") &&
                !(document.activeElement && document.activeElement.id === TEXT)) {
            setProps(MODAL, {className: MODAL_CLASS});
        }
    });

    window.qcTextEdit = {editableAt, open};
})();
