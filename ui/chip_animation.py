"""Place for the light animation controls next to a chip graph; assets/chip_animation.js builds and runs them."""

from __future__ import annotations

from dash import html

from gbs.bench import LightSource

ANIMATION_CLASS = "chip-animation"


def light_animation_controls(graph_id: str, source: LightSource) -> html.Div:
    """The controls live only in the browser: moving the light 60 times a second cannot wait for the server. The
    chip itself, with its size and the estimated real transit time, comes from the figure of the graph."""
    return html.Div(className=ANIMATION_CLASS, **{"data-graph": graph_id, "data-source": source.value})
