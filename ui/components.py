"""Building blocks shared by both pages."""

from __future__ import annotations

from typing import Union

from dash import dcc, html

from ui.form_parsing import RANDOM_SEED

TABLE_CELL_STYLE = {"fontFamily": "inherit", "padding": "6px 10px", "textAlign": "right"}
TABLE_HEADER_STYLE = {"fontWeight": "600", "backgroundColor": "var(--surface-muted)"}
SCROLLABLE_TABLE_STYLE = {"overflowX": "auto"}

REFERENCE_SEED = 42
SEED_OPTIONS = [
    {"label": "Náhodný – při každém spuštění jiné výsledky", "value": RANDOM_SEED},
    {"label": "42 – referenční běh", "value": REFERENCE_SEED},
    {"label": "1 – kontrolní běh 1", "value": 1},
    {"label": "2 – kontrolní běh 2", "value": 2},
    {"label": "3 – kontrolní běh 3", "value": 3},
]
SEED_HINT = (
    "Stejný seed a stejné vstupy dají vždy stejné výsledky. Rozdíly mezi kontrolními běhy "
    "ukazují náhodnou chybu simulace – když jsou velké, zvyš počet vzorků."
)


def labelled(label: str, component) -> html.Div:
    return html.Div(className="field", children=[html.Label(label), component])


def seed_dropdown(component_id: str, default_value: Union[str, int]) -> html.Div:
    return html.Div(
        className="field",
        children=[
            html.Label("Seed generátoru náhodných čísel"),
            dcc.Dropdown(
                id=component_id, options=SEED_OPTIONS, value=default_value, clearable=False, searchable=False,
            ),
            html.P(SEED_HINT, className="hint small"),
        ],
    )


def details_link(title: str, href: str) -> dcc.Link:
    return dcc.Link(f"Podrobněji: {title} →", href=href, className="details-link")


def metric_tile(label: str, value: str, hint: str = "") -> html.Div:
    return html.Div(
        className="metric",
        title=hint,
        children=[
            html.Div(label + (" ⓘ" if hint else ""), className="metric-label"),
            html.Div(value, className="metric-value"),
        ],
    )
