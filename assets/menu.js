// Top menu behaviour (ids from ui/ids.py: main-menu, menu-toggle). Dash serves every file in assets/ automatically.
(function () {
    const GROUP_SELECTOR = "details.nav-link";

    function closeGroups(except) {
        document.querySelectorAll(GROUP_SELECTOR + "[open]").forEach((group) => {
            if (group !== except) {
                group.open = false;
            }
        });
    }

    function closeMenu() {
        closeGroups(null);
        document.body.classList.remove("menu-open");
    }

    // "toggle" does not bubble, so it is caught in the capture phase.
    document.addEventListener("toggle", (event) => {
        const group = event.target;
        if (group instanceof HTMLDetailsElement && group.matches(GROUP_SELECTOR) && group.open) {
            closeGroups(group);
        }
    }, true);

    document.addEventListener("click", (event) => {
        if (event.target.closest("#menu-toggle")) {
            document.body.classList.toggle("menu-open");
            return;
        }
        if (event.target.closest("#main-menu a")) {
            closeMenu();
            return;
        }
        if (!event.target.closest(GROUP_SELECTOR)) {
            closeGroups(null);
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeMenu();
        }
    });
})();
