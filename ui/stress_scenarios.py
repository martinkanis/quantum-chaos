"""Stress-scenario section of page 1: what one historical year would do to the portfolio."""

from __future__ import annotations

from dash import dash_table, dcc, html

from montecarlo.historical_returns import SOURCE_URL, AssetClass
from montecarlo.scenarios import STRESS_SCENARIOS
from ui import ids
from ui.components import ASSET_CLASS_LABELS, SCROLLABLE_TABLE_STYLE, TABLE_CELL_STYLE, TABLE_HEADER_STYLE
from ui.form_parsing import SCENARIO_DESCRIPTION_COLUMN, SCENARIO_NAME_COLUMN, scenario_rows

TEXT_COLUMNS = (SCENARIO_NAME_COLUMN, SCENARIO_DESCRIPTION_COLUMN)
PLACEHOLDER_SCENARIO_NAME = "Vlastní scénář"
INTRO = (
    "Co by s portfoliem udělal jeden konkrétní rok. Každé aktivum se pohne jako jeho třída ze sloupce Třída "
    "v tabulce portfolia; částka v Kč je dopad na počáteční investici. Výnosy jsou za celý kalendářní rok v USD: "
    "akcie = S&P 500 včetně dividend, dluhopisy = 10leté státní dluhopisy USA, zlato. "
)
EMPTY_SCENARIO_ROW = {
    **{asset_class.value: 0 for asset_class in AssetClass},
    SCENARIO_DESCRIPTION_COLUMN: "",
}


def custom_scenario_row(row_count: int) -> dict:
    """The number keeps new rows unique – scenarios with the same name would merge into one bar."""
    return {SCENARIO_NAME_COLUMN: f"{PLACEHOLDER_SCENARIO_NAME} {row_count + 1}", **EMPTY_SCENARIO_ROW}


def build_stress_section() -> html.Section:
    return html.Section(
        className="card",
        children=[
            html.H2("Stresové scénáře: co kdyby se zopakoval historický rok"),
            html.P(
                className="hint",
                children=[
                    INTRO,
                    "Zdroj: A. Damodaran, NYU Stern (",
                    html.A("data 1928–2023", href=SOURCE_URL, target="_blank"),
                    ").",
                ],
            ),
            html.Div(id=ids.STRESS_SCENARIO_MESSAGE, className="error-message"),
            dcc.Graph(id=ids.STRESS_SCENARIO_CHART, config={"displayModeBar": False}),
            html.Details(
                children=[
                    html.Summary("Upravit scénáře nebo přidat vlastní"),
                    dash_table.DataTable(
                        id=ids.STRESS_SCENARIO_TABLE,
                        data=scenario_rows(list(STRESS_SCENARIOS)),
                        columns=[
                            {"id": SCENARIO_NAME_COLUMN, "name": "Scénář", "type": "text"},
                            *[_class_return_column(asset_class) for asset_class in AssetClass],
                            {"id": SCENARIO_DESCRIPTION_COLUMN, "name": "Popis", "type": "text"},
                        ],
                        editable=True,
                        row_deletable=True,
                        style_cell=TABLE_CELL_STYLE,
                        style_cell_conditional=[
                            {"if": {"column_id": column}, "textAlign": "left"} for column in TEXT_COLUMNS
                        ],
                        style_data={"whiteSpace": "normal", "height": "auto"},
                        style_header=TABLE_HEADER_STYLE,
                        style_table=SCROLLABLE_TABLE_STYLE,
                    ),
                    html.Button(
                        "+ Přidat vlastní scénář", id=ids.ADD_STRESS_SCENARIO_BUTTON, className="secondary-button",
                    ),
                ],
            ),
        ],
    )


def _class_return_column(asset_class: AssetClass) -> dict:
    return {"id": asset_class.value, "name": f"{ASSET_CLASS_LABELS[asset_class]} (%)", "type": "numeric"}
