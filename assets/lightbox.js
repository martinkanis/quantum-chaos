// Slides from lectures and videos (.lecture-slide figures in a .slide-gallery) open in a full-screen viewer instead
// of a new tab: arrows, ←/→ and swiping move within the gallery, Esc or the cross closes it. The figure's link to
// the image stays as the fallback for a middle click or Ctrl/Cmd+click. Dash serves every file in assets/.
(function () {
    const SLIDE_LINK_SELECTOR = ".lecture-slide a.lecture-slide-link";
    const SWIPE_PIXELS = 50;

    let viewer = null;
    let slides = [];
    let index = 0;
    let returnFocus = null;
    let touchStart = null;

    function button(className, label, text) {
        const element = document.createElement("button");
        element.type = "button";
        element.className = className;
        element.setAttribute("aria-label", label);
        element.title = label;
        element.textContent = text;
        return element;
    }

    function buildViewer() {
        const root = document.createElement("div");
        root.className = "slide-viewer";
        root.hidden = true;
        root.setAttribute("role", "dialog");
        root.setAttribute("aria-modal", "true");
        root.setAttribute("aria-label", "Prohlížení snímků");

        const close = button("slide-viewer-close", "Zavřít (Esc)", "×");
        const previous = button("slide-viewer-nav slide-viewer-previous", "Předchozí snímek (←)", "‹");
        const next = button("slide-viewer-nav slide-viewer-next", "Další snímek (→)", "›");
        const stage = document.createElement("div");
        stage.className = "slide-viewer-stage";
        const image = document.createElement("img");
        image.className = "slide-viewer-image";
        stage.appendChild(image);
        const footer = document.createElement("div");
        footer.className = "slide-viewer-footer";
        const counter = document.createElement("span");
        counter.className = "slide-viewer-counter";
        const caption = document.createElement("div");
        caption.className = "slide-viewer-caption";
        footer.append(counter, caption);
        root.append(stage, previous, next, close, footer);

        close.addEventListener("click", closeViewer);
        previous.addEventListener("click", () => show(index - 1));
        next.addEventListener("click", () => show(index + 1));
        // A click on the dark backdrop closes, a click on the image does not.
        stage.addEventListener("click", (event) => {
            if (event.target === stage) {
                closeViewer();
            }
        });
        root.addEventListener("touchstart", (event) => {
            touchStart = event.touches.length === 1 ? {x: event.touches[0].clientX, y: event.touches[0].clientY} : null;
        }, {passive: true});
        root.addEventListener("touchend", (event) => {
            if (!touchStart || event.changedTouches.length !== 1) {
                return;
            }
            const dx = event.changedTouches[0].clientX - touchStart.x;
            const dy = event.changedTouches[0].clientY - touchStart.y;
            touchStart = null;
            // Ignore swipes while the page is pinch-zoomed: the finger then pans the zoomed image.
            if (Math.abs(dx) > SWIPE_PIXELS && Math.abs(dx) > 1.5 * Math.abs(dy)
                && (!window.visualViewport || window.visualViewport.scale <= 1.01)) {
                show(index + (dx < 0 ? 1 : -1));
            }
        });
        document.body.appendChild(root);
        return {root, image, counter, caption, previous, next, close};
    }

    function captionOf(figure) {
        const figcaption = figure.querySelector("figcaption");
        if (!figcaption) {
            return document.createTextNode("");
        }
        // A copy without ids: the text editor and highlighter look elements up by id and must not find it twice.
        const copy = figcaption.cloneNode(true);
        copy.removeAttribute("id");
        copy.querySelectorAll("[id]").forEach((element) => element.removeAttribute("id"));
        const fragment = document.createDocumentFragment();
        fragment.append(...copy.childNodes);
        return fragment;
    }

    function preload(position) {
        if (position >= 0 && position < slides.length) {
            new Image().src = slides[position].href;
        }
    }

    function show(position) {
        if (position < 0 || position >= slides.length) {
            return;
        }
        index = position;
        const slide = slides[index];
        viewer.image.src = slide.href;
        viewer.image.alt = slide.alt;
        viewer.counter.textContent = `${index + 1} / ${slides.length}`;
        viewer.caption.replaceChildren(captionOf(slide.figure));
        viewer.previous.disabled = index === 0;
        viewer.next.disabled = index === slides.length - 1;
        preload(index + 1);
        preload(index - 1);
    }

    function openViewer(link) {
        const gallery = link.closest(".slide-gallery") || document;
        slides = Array.from(gallery.querySelectorAll(SLIDE_LINK_SELECTOR)).map((element) => ({
            href: element.getAttribute("href"),
            alt: (element.querySelector("img") || {}).alt || "",
            figure: element.closest(".lecture-slide"),
        }));
        viewer = viewer || buildViewer();
        returnFocus = document.activeElement;
        viewer.root.hidden = false;
        document.documentElement.classList.add("slide-viewer-open");
        show(Math.max(0, slides.findIndex((slide) => slide.figure === link.closest(".lecture-slide"))));
        viewer.close.focus();
    }

    function closeViewer() {
        if (!viewer || viewer.root.hidden) {
            return;
        }
        viewer.root.hidden = true;
        viewer.image.removeAttribute("src");
        document.documentElement.classList.remove("slide-viewer-open");
        if (returnFocus && document.contains(returnFocus)) {
            returnFocus.focus();
        }
    }

    document.addEventListener("click", (event) => {
        if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey
            || event.altKey) {
            return;
        }
        const link = event.target.closest(SLIDE_LINK_SELECTOR);
        if (link) {
            event.preventDefault();
            openViewer(link);
        }
    });

    document.addEventListener("keydown", (event) => {
        if (!viewer || viewer.root.hidden) {
            return;
        }
        if (event.key === "Escape") {
            closeViewer();
        } else if (event.key === "ArrowLeft") {
            show(index - 1);
        } else if (event.key === "ArrowRight") {
            show(index + 1);
        } else if (event.key === "Tab") {
            // Keep the focus inside the dialog.
            const focusable = Array.from(viewer.root.querySelectorAll("button:not([disabled]), a[href]"));
            const first = focusable[0];
            const last = focusable[focusable.length - 1];
            if (event.shiftKey && document.activeElement === first) {
                last.focus();
            } else if (!event.shiftKey && document.activeElement === last) {
                first.focus();
            } else if (!viewer.root.contains(document.activeElement)) {
                first.focus();
            } else {
                return;
            }
        } else {
            return;
        }
        event.preventDefault();
    });

    // Leaving the page (back button, a link in the caption) closes the viewer.
    window.addEventListener("popstate", closeViewer);
})();
