from __future__ import annotations

from typing import List

import numpy as np
from dash import dash_table, dcc, html

from montecarlo.charts import final_value_histogram, percentile_fan_chart
from montecarlo.metrics import BAND_PERCENTILES, SummaryMetrics, percentile_bands, summarize
from montecarlo.simulation import MONTHS_PER_YEAR, SimulationResult
from ui import ids
from ui.components import TABLE_CELL_STYLE, TABLE_HEADER_STYLE, metric_tile

PERCENT = 100
YEAR_COLUMN = "year"


def build_results(result: SimulationResult) -> html.Div:
    metrics = summarize(result)
    return html.Div(
        className="results",
        children=[
            html.H2("Výsledky"),
            _metric_tiles(metrics),
            dcc.Tabs(
                children=[
                    dcc.Tab(label="Histogram konečných hodnot", children=dcc.Graph(
                        figure=final_value_histogram(result.final_values, metrics),
                    )),
                    dcc.Tab(label="Vývoj v čase", children=dcc.Graph(
                        figure=percentile_fan_chart(percentile_bands(result), result.paths),
                    )),
                    dcc.Tab(label="Percentily po letech", children=_percentile_table(result)),
                ]
            ),
            html.Button("Stáhnout konečné hodnoty (CSV)", id=ids.DOWNLOAD_BUTTON, className="secondary-button"),
        ],
    )


def format_money(value: float) -> str:
    return f"{value:,.0f}".replace(",", " ")


def _metric_tiles(metrics: SummaryMetrics) -> html.Div:
    tiles = [
        metric_tile("Vloženo celkem", format_money(metrics.total_contributed)),
        metric_tile("Medián", format_money(metrics.median)),
        metric_tile("Průměr", format_money(metrics.mean)),
        metric_tile("Šance na ztrátu", f"{metrics.probability_of_loss * PERCENT:.1f} %"),
        metric_tile("5. percentil", format_money(metrics.percentile_5)),
        metric_tile("95. percentil", format_money(metrics.percentile_95)),
        metric_tile(
            "VaR 95 %", format_money(metrics.value_at_risk),
            hint="Ztráta vůči vloženému kapitálu, kterou s 95% pravděpodobností nepřekročíš. "
            "Záporná hodnota = zisk.",
        ),
        metric_tile(
            "CVaR 95 %", format_money(metrics.conditional_value_at_risk),
            hint="Průměrná ztráta vůči vloženému kapitálu v nejhorších 5 % scénářů.",
        ),
    ]
    if metrics.median_annual_return is not None:
        tiles.append(metric_tile("Mediánový roční výnos", f"{metrics.median_annual_return * PERCENT:.2f} %"))
    return html.Div(className="metric-grid", children=tiles)


def _percentile_table(result: SimulationResult) -> dash_table.DataTable:
    bands = percentile_bands(result, BAND_PERCENTILES)
    month_indices = np.arange(0, result.paths.shape[1], MONTHS_PER_YEAR)
    rows: List[dict] = [
        {
            YEAR_COLUMN: int(month // MONTHS_PER_YEAR),
            **{str(percentile): format_money(bands[percentile][month]) for percentile in BAND_PERCENTILES},
        }
        for month in month_indices
    ]
    columns = [{"id": YEAR_COLUMN, "name": "Rok"}] + [
        {"id": str(percentile), "name": f"{percentile}. percentil"} for percentile in BAND_PERCENTILES
    ]
    return dash_table.DataTable(
        data=rows, columns=columns, style_cell=TABLE_CELL_STYLE, style_header=TABLE_HEADER_STYLE,
    )
