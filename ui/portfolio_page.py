from __future__ import annotations

from typing import List

from dash import dash_table, dcc, html

from montecarlo.simulation import MAX_SIMULATION_COUNT, MAX_YEARS
from ui import ids
from ui.components import TABLE_CELL_STYLE, TABLE_HEADER_STYLE, labelled, seed_dropdown
from ui.form_parsing import (
    CORRELATION_ROW_LABEL_COLUMN,
    DEFAULT_ASSET_ROWS,
    NAME_COLUMN,
    RANDOM_SEED,
    RETURN_COLUMN,
    VOLATILITY_COLUMN,
    WEIGHT_COLUMN,
    asset_names,
    correlation_column_id,
    default_correlation_rows,
)
from ui.navigation import HIDDEN

DEFAULT_INITIAL_VALUE = 1_000_000
DEFAULT_MONTHLY_CONTRIBUTION = 0
DEFAULT_YEARS = 10
DEFAULT_SIMULATION_COUNT = 5_000
MIN_SIMULATION_COUNT = 100
DEFAULT_PAIRWISE_CORRELATION = 0.2


def build_portfolio_page() -> html.Div:
    return html.Div(
        id=ids.PORTFOLIO_PAGE,
        className="page",
        children=[
            html.Aside(className="sidebar", children=_simulation_parameters()),
            html.Main(
                className="content",
                children=[
                    html.H1("🎲 Monte Carlo simulace portfolia"),
                    html.P(
                        "Zadej složení portfolia a parametry simulace. Výnosy aktiv se modelují jako "
                        "korelovaný geometrický Brownův pohyb s měsíčním rebalancováním na cílové váhy.",
                        className="lead",
                    ),
                    _asset_section(),
                    _correlation_section(),
                    html.Button("Spustit simulaci", id=ids.RUN_BUTTON, className="primary-button"),
                    html.Div(id=ids.ERROR_MESSAGE, className="error-message"),
                    # The download button stays in the initial layout because Dash checks on page load that every
                    # callback input exists. Sharing the Loading hides it together with the results during a re-run.
                    dcc.Loading([html.Div(id=ids.RESULTS), _download_button()], type="circle"),
                    dcc.Store(id=ids.FINAL_VALUES_STORE),
                    dcc.Download(id=ids.DOWNLOAD),
                ],
            ),
        ],
    )


def _simulation_parameters() -> list:
    return [
        html.H2("Parametry simulace"),
        labelled("Počáteční investice", dcc.Input(
            id=ids.INITIAL_VALUE_INPUT, type="number", min=0, step=10_000, value=DEFAULT_INITIAL_VALUE,
        )),
        labelled("Měsíční vklad", dcc.Input(
            id=ids.MONTHLY_CONTRIBUTION_INPUT, type="number", min=0, step=1_000,
            value=DEFAULT_MONTHLY_CONTRIBUTION,
        )),
        labelled("Investiční horizont (roky)", dcc.Slider(
            id=ids.YEARS_SLIDER, min=1, max=MAX_YEARS, step=1, value=DEFAULT_YEARS,
            marks={1: "1", 10: "10", 20: "20", 30: "30", MAX_YEARS: str(MAX_YEARS)},
            tooltip={"placement": "bottom", "always_visible": True},
        )),
        labelled("Počet simulací", dcc.Slider(
            id=ids.SIMULATION_COUNT_SLIDER, min=MIN_SIMULATION_COUNT, max=MAX_SIMULATION_COUNT, step=100,
            value=DEFAULT_SIMULATION_COUNT, marks={MIN_SIMULATION_COUNT: "100", MAX_SIMULATION_COUNT: "10k"},
            tooltip={"placement": "bottom", "always_visible": True},
        )),
        seed_dropdown(ids.SEED_DROPDOWN, default_value=RANDOM_SEED),
    ]


def _asset_section() -> html.Section:
    return html.Section(
        className="card",
        children=[
            html.H2("Portfolio"),
            dash_table.DataTable(
                id=ids.ASSET_TABLE,
                data=DEFAULT_ASSET_ROWS,
                columns=[
                    {"id": NAME_COLUMN, "name": "Aktivum", "type": "text"},
                    {"id": WEIGHT_COLUMN, "name": "Váha (%)", "type": "numeric"},
                    {"id": RETURN_COLUMN, "name": "Očekávaný roční výnos (%)", "type": "numeric"},
                    {"id": VOLATILITY_COLUMN, "name": "Roční volatilita (%)", "type": "numeric"},
                ],
                editable=True,
                row_deletable=True,
                style_cell=TABLE_CELL_STYLE,
                style_cell_conditional=[{"if": {"column_id": NAME_COLUMN}, "textAlign": "left"}],
                style_header=TABLE_HEADER_STYLE,
            ),
            html.Div(
                className="table-footer",
                children=[
                    html.Button("+ Přidat aktivum", id=ids.ADD_ASSET_BUTTON, className="secondary-button"),
                    html.Span(id=ids.WEIGHT_SUM_TEXT),
                ],
            ),
        ],
    )


def _correlation_section() -> html.Details:
    return html.Details(
        className="card",
        children=[
            html.Summary("Korelace mezi aktivy"),
            labelled("Výchozí korelace mezi všemi páry", dcc.Slider(
                id=ids.PAIRWISE_CORRELATION_SLIDER, min=-0.5, max=1.0, step=0.05,
                value=DEFAULT_PAIRWISE_CORRELATION, marks={-0.5: "-0,5", 0: "0", 0.5: "0,5", 1: "1"},
                tooltip={"placement": "bottom", "always_visible": True},
            )),
            html.P(
                "Jednotlivé páry můžeš upravit v matici. Rozhodují hodnoty nad diagonálou.",
                className="hint",
            ),
            # Initial data lets the GBS page read the correlations before this table is first edited.
            dash_table.DataTable(
                id=ids.CORRELATION_TABLE,
                data=default_correlation_rows(_default_names(), DEFAULT_PAIRWISE_CORRELATION),
                columns=correlation_table_columns(_default_names()),
                editable=True,
                style_cell=TABLE_CELL_STYLE,
                style_header=TABLE_HEADER_STYLE,
            ),
        ],
    )


def _download_button() -> html.Button:
    return html.Button(
        "Stáhnout konečné hodnoty (CSV)", id=ids.DOWNLOAD_BUTTON, className="secondary-button download-button",
        style=HIDDEN,
    )


def correlation_table_columns(names: List[str]) -> List[dict]:
    return [{"id": CORRELATION_ROW_LABEL_COLUMN, "name": "", "editable": False}] + [
        {"id": correlation_column_id(index), "name": name, "type": "numeric"}
        for index, name in enumerate(names)
    ]


def _default_names() -> List[str]:
    return asset_names(DEFAULT_ASSET_ROWS)
