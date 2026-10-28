// Links in reading text (dcc.Markdown in .theory-section cards and „V kostce“) to a page of the app switch the page
// like dcc.Link instead of reloading the whole app: dcc.Markdown renders them as plain <a>. The hash then scrolls
// to its section through the URL callback in ui/navigation.py. Dash serves every file in assets/ automatically.
(function () {
    const TEXT_LINK_SELECTOR = ".theory-section a[href^='/'], .in-short a[href^='/']";

    // dcc.Link handles its own clicks first (React listens below document) and marks them defaultPrevented.
    document.addEventListener("click", (event) => {
        if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey
            || event.altKey) {
            return;
        }
        const link = event.target.closest(TEXT_LINK_SELECTOR);
        if (!link) {
            return;
        }
        event.preventDefault();
        window.history.pushState({}, "", link.getAttribute("href"));
        window.dispatchEvent(new CustomEvent("_dashprivate_pushstate"));
    });
})();
