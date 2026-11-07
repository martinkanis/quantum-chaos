// Light passing through the photonic chip simulator. ui/chip_animation.py puts an empty .chip-animation element next
// to a chip graph; this script fills it with controls (play/pause, the moment of the passage, its length) and draws
// the passage into the graph: the light shapes are revealed from the left up to the light front and bright pulses
// ride the front along every lit waveguide. Geometry and light come from layout.meta.lightAnimation of the figure
// (gbs/chip_charts.py). Plotly redraws its shapes whenever the figure changes, so every frame is drawn from scratch.
(function () {
    const SVG_NS = "http://www.w3.org/2000/svg";
    const FRAME_SECONDS = 1 / 60;
    const MIN_EXPONENT = -11;
    const MAX_EXPONENT = 1;
    const EXPONENT_STEP = 0.1;
    const DEFAULT_EXPONENT = 0.5;
    const POSITION_STEPS = 400;
    const BISECTION_STEPS = 24;
    const CLIP_MARGIN = 40;
    const ROW_PIXELS_FOR_FULL_PULSE = 80;
    const MIN_PULSE_SCALE = 0.75;
    const VISIBLE_MARGIN = 0.15;
    const PULSE_HALO_COLOR = "rgba(80, 220, 255, 0.3)";
    const PULSE_CORE_RGB = "215, 250, 255";
    const SUPERSCRIPT_DIGITS = "⁰¹²³⁴⁵⁶⁷⁸⁹";
    const UNITS = [[1, "s"], [1e-3, "ms"], [1e-6, "µs"], [1e-9, "ns"], [1e-12, "ps"]];

    let nextClipId = 0;

    function czechNumber(value, decimals) {
        return value.toFixed(decimals).replace(".", ",");
    }

    function shortNumber(value) {
        return czechNumber(value, value >= 10 ? 0 : 1);
    }

    function formatSeconds(seconds) {
        if (seconds <= 0) {
            return "0 s";
        }
        const [unit, symbol] = UNITS.find(([size]) => seconds >= size * 0.9995) || UNITS[UNITS.length - 1];
        return shortNumber(seconds / unit) + " " + symbol;
    }

    function superscript(exponent) {
        return String(exponent).split("").map((digit) => SUPERSCRIPT_DIGITS[Number(digit)]).join("");
    }

    function formatFactor(factor) {
        if (factor < 1000) {
            return shortNumber(factor);
        }
        let exponent = Math.floor(Math.log10(factor));
        let mantissa = Math.round(factor / 10 ** exponent);
        if (mantissa === 10) {
            mantissa = 1;
            exponent += 1;
        }
        return mantissa + " · 10" + superscript(exponent);
    }

    function describeDuration(durationSeconds, transitSeconds) {
        if (durationSeconds < FRAME_SECONDS) {
            return formatSeconds(durationSeconds) + " · kratší než jeden snímek obrazovky, světlo se objeví naráz";
        }
        if (!transitSeconds) {
            return formatSeconds(durationSeconds);
        }
        return formatSeconds(durationSeconds) + " · skutečné světlo asi " + formatSeconds(transitSeconds)
            + " (odhad) · zpomaleno " + formatFactor(durationSeconds / transitSeconds) + "krát";
    }

    function element(tag, className, text) {
        const node = document.createElement(tag);
        node.className = className;
        if (text) {
            node.textContent = text;
        }
        return node;
    }

    function rangeInput(min, max, step, value, label) {
        const input = element("input", "chip-animation-range");
        Object.assign(input, {type: "range", min: String(min), max: String(max), step: String(step)});
        input.value = String(value);
        input.setAttribute("aria-label", label);
        return input;
    }

    function findPlot(graphId) {
        const graph = document.getElementById(graphId);
        if (!graph) {
            return null;
        }
        return graph.classList.contains("js-plotly-plot") ? graph : graph.querySelector(".js-plotly-plot");
    }

    function lightAnimation(plot) {
        const meta = plot && plot.layout && plot.layout.meta;
        return meta ? meta.lightAnimation : undefined;
    }

    function shapePath(plot, index) {
        return plot.querySelector('.shapelayer path[data-index="' + index + '"]');
    }

    // The S-bend from (x0, y0) to (x1, y1) is the cubic Bézier of _svg_path in gbs/chip_charts.py: control points
    // (middle, y0) and (middle, y1). Its x grows with the parameter, so the height at x is found by bisection.
    function bendHeight(x0, x1, y0, y1, x) {
        const middle = (x0 + x1) / 2;
        let low = 0;
        let high = 1;
        for (let step = 0; step < BISECTION_STEPS; step += 1) {
            const t = (low + high) / 2;
            const u = 1 - t;
            const curveX = u * u * u * x0 + 3 * u * u * t * middle + 3 * u * t * t * middle + t * t * t * x1;
            if (curveX < x) {
                low = t;
            } else {
                high = t;
            }
        }
        const t = (low + high) / 2;
        const u = 1 - t;
        return y0 * (u * u * u + 3 * u * u * t) + y1 * (3 * u * t * t + t * t * t);
    }

    // A lane is [light, x0, x1, y0, y1, x0, x1, y0, y1, ...]: one lit piece of waveguide, segment by segment.
    function laneHeightAt(lane, x) {
        for (let index = 1; index < lane.length; index += 4) {
            const [x0, x1, y0, y1] = lane.slice(index, index + 4);
            if (x >= x0 && x < x1) {
                return y0 === y1 ? y0 : bendHeight(x0, x1, y0, y1, x);
            }
        }
        return null;
    }

    function svgElement(tag, parent) {
        const node = document.createElementNS(SVG_NS, tag);
        parent.appendChild(node);
        return node;
    }

    // Own layer on top of the plot, outside the layers Plotly redraws.
    function overlayOf(plot) {
        const svg = plot.querySelector("svg.main-svg");
        let overlay = svg.querySelector(":scope > g.chip-light-overlay");
        if (!overlay) {
            overlay = svgElement("g", svg);
            overlay.setAttribute("class", "chip-light-overlay");
            overlay.setAttribute("pointer-events", "none"); // hover descriptions of the parts stay reachable
            const clipPath = svgElement("clipPath", svgElement("defs", overlay));
            nextClipId += 1;
            clipPath.id = "chip-light-front-" + nextClipId;
            svgElement("rect", clipPath);
            svgElement("g", overlay).setAttribute("class", "chip-light-pulses");
        }
        return {
            clipId: overlay.querySelector("clipPath").id,
            clipRect: overlay.querySelector("clipPath rect"),
            pulses: overlay.querySelector("g.chip-light-pulses"),
        };
    }

    function removeOverlay(plot, animation) {
        const overlay = plot.querySelector("svg.main-svg > g.chip-light-overlay");
        if (overlay) {
            overlay.remove();
        }
        animation.lightShapes.forEach((index) => {
            const path = shapePath(plot, index);
            if (path) {
                path.removeAttribute("clip-path");
            }
        });
    }

    function drawPulse(pulses, index, x, y, light, scale) {
        while (pulses.childNodes.length < 2 * (index + 1)) {
            svgElement("circle", pulses);
        }
        const strength = Math.sqrt(light);
        const core = (2.5 + 4.5 * strength) * scale;
        const halo = pulses.childNodes[2 * index];
        const centre = pulses.childNodes[2 * index + 1];
        halo.setAttribute("r", String(2.4 * core));
        halo.setAttribute("fill", PULSE_HALO_COLOR);
        centre.setAttribute("r", String(core));
        centre.setAttribute("fill", "rgba(" + PULSE_CORE_RGB + ", " + (0.45 + 0.55 * light).toFixed(3) + ")");
        [halo, centre].forEach((circle) => {
            circle.setAttribute("cx", String(x));
            circle.setAttribute("cy", String(y));
        });
    }

    function drawFront(plot, animation, progress) {
        const waveguides = shapePath(plot, animation.waveguideShape);
        const box = waveguides && waveguides.getBBox();
        if (!box || !box.width || !box.height) {
            return; // the page is hidden or the figure is not drawn yet
        }
        const toPixelX = (x) => box.x + (x - animation.start) / (animation.end - animation.start) * box.width;
        const toPixelY = (y) => box.y + (animation.top - y) / animation.top * box.height;
        const front = animation.start + progress * (animation.end - animation.start);
        const overlay = overlayOf(plot);

        overlay.clipRect.setAttribute("x", String(box.x - CLIP_MARGIN));
        overlay.clipRect.setAttribute("y", String(box.y - CLIP_MARGIN));
        overlay.clipRect.setAttribute("width", String(Math.max(0, toPixelX(front) - box.x + CLIP_MARGIN)));
        overlay.clipRect.setAttribute("height", String(box.height + 2 * CLIP_MARGIN));
        animation.lightShapes.forEach((index) => {
            const path = shapePath(plot, index);
            if (path) {
                path.setAttribute("clip-path", "url(#" + overlay.clipId + ")");
            }
        });

        const rowPixels = box.height / animation.top;
        const scale = Math.min(1, Math.max(MIN_PULSE_SCALE, rowPixels / ROW_PIXELS_FOR_FULL_PULSE));
        let count = 0;
        animation.lanes.forEach((lane) => {
            const y = laneHeightAt(lane, front);
            if (y !== null) {
                drawPulse(overlay.pulses, count, toPixelX(front), toPixelY(y), lane[0], scale);
                count += 1;
            }
        });
        while (overlay.pulses.childNodes.length > 2 * count) {
            overlay.pulses.lastChild.remove();
        }
        keepInView(plot, toPixelX(front));
    }

    // On narrow screens a wide chip scrolls sideways (.chip-figure); the scroll follows the light front.
    function keepInView(plot, frontPixel) {
        const scroller = plot.closest(".chip-figure");
        if (!scroller || scroller.scrollWidth <= scroller.clientWidth) {
            return;
        }
        const visibleStart = scroller.scrollLeft + VISIBLE_MARGIN * scroller.clientWidth;
        const visibleEnd = scroller.scrollLeft + (1 - VISIBLE_MARGIN) * scroller.clientWidth;
        if (frontPixel < visibleStart || frontPixel > visibleEnd) {
            scroller.scrollLeft = frontPixel - scroller.clientWidth / 2;
        }
    }

    function createController(root) {
        const graphId = root.dataset.graph;
        const idleLabel = root.dataset.source === "fotony" ? "▶ Pustit fotony" : "▶ Pustit světlo";
        const state = {progress: 1, playing: false, startedAt: 0, durationSeconds: 10 ** DEFAULT_EXPONENT};

        const button = element("button", "secondary-button chip-animation-play", idleLabel);
        button.type = "button";
        const position = rangeInput(0, POSITION_STEPS, 1, POSITION_STEPS, "Okamžik průchodu");
        const clock = element("span", "chip-animation-readout");
        const duration = rangeInput(MIN_EXPONENT, MAX_EXPONENT, EXPONENT_STEP, DEFAULT_EXPONENT, "Délka průchodu");
        const durationText = element("span", "chip-animation-readout");

        const positionRow = element("div", "chip-animation-row");
        const positionField = element("label", "chip-animation-field", "Okamžik");
        positionField.appendChild(position);
        positionRow.append(button, positionField, clock);
        const durationRow = element("div", "chip-animation-row");
        const durationField = element("label", "chip-animation-field", "Délka průchodu");
        durationField.append(
            element("span", "chip-animation-scale", formatSeconds(10 ** MIN_EXPONENT)),
            duration,
            element("span", "chip-animation-scale", formatSeconds(10 ** MAX_EXPONENT)),
        );
        durationRow.append(durationField, durationText);
        root.append(positionRow, durationRow);

        // Plotly redraws the chip whenever the figure changes (another chip, other phases); the frame and the real
        // transit time in the readout follow it.
        let boundPlot = null;

        function bindPlot() {
            const plot = findPlot(graphId);
            if (!plot || plot === boundPlot || typeof plot.on !== "function") {
                return;
            }
            boundPlot = plot;
            plot.on("plotly_afterplot", () => {
                if (root.isConnected) {
                    draw();
                    showState();
                }
            });
            showState();
        }

        function draw() {
            const plot = findPlot(graphId);
            const animation = lightAnimation(plot);
            if (!animation) {
                return;
            }
            if (state.progress >= 1) {
                removeOverlay(plot, animation);
            } else {
                drawFront(plot, animation, state.progress);
            }
        }

        function showState() {
            const animation = lightAnimation(findPlot(graphId));
            const transitSeconds = animation ? animation.transitSeconds : null;
            button.textContent = state.playing ? "⏸ Zastavit" : state.progress > 0 && state.progress < 1
                ? "▶ Pokračovat" : idleLabel;
            position.value = String(Math.round(state.progress * POSITION_STEPS));
            clock.textContent = formatSeconds(state.progress * state.durationSeconds) + " z "
                + formatSeconds(state.durationSeconds)
                + (transitSeconds ? " · ve skutečnosti " + formatSeconds(state.progress * transitSeconds) : "");
            durationText.textContent = describeDuration(state.durationSeconds, transitSeconds);
            duration.setAttribute("aria-valuetext", formatSeconds(state.durationSeconds));
        }

        function frame(now) {
            if (!state.playing) {
                return;
            }
            if (!root.isConnected) {
                state.playing = false;
                return;
            }
            state.progress = Math.min(1, (now - state.startedAt) / (1000 * state.durationSeconds));
            if (state.progress >= 1) {
                state.playing = false;
            } else {
                requestAnimationFrame(frame);
            }
            draw();
            showState();
        }

        function play() {
            if (state.progress >= 1) {
                state.progress = 0;
            }
            state.playing = true;
            state.startedAt = performance.now() - state.progress * 1000 * state.durationSeconds;
            requestAnimationFrame(frame);
        }

        button.addEventListener("click", () => {
            if (state.playing) {
                state.playing = false;
            } else {
                play();
            }
            draw();
            showState();
        });
        position.addEventListener("input", () => {
            state.playing = false;
            state.progress = Number(position.value) / POSITION_STEPS;
            draw();
            showState();
        });
        duration.addEventListener("input", () => {
            state.durationSeconds = 10 ** Number(duration.value);
            if (state.playing) {
                state.startedAt = performance.now() - state.progress * 1000 * state.durationSeconds;
            }
            showState();
        });
        showState();
        return bindPlot;
    }

    let controllers = [];

    // Results of the photon lab replace their controls with every run; controls no longer on the page are dropped.
    function initialise() {
        document.querySelectorAll(".chip-animation:not([data-ready])").forEach((root) => {
            root.dataset.ready = "true";
            controllers.push({root, bindPlot: createController(root)});
        });
        controllers = controllers.filter((controller) => controller.root.isConnected);
        controllers.forEach((controller) => controller.bindPlot());
    }

    function start() {
        initialise();
        new MutationObserver(initialise).observe(document.body, {childList: true, subtree: true});
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", start);
    } else {
        start();
    }
})();
