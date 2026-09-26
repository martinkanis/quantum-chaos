from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd
import streamlit as st

from montecarlo.charts import final_value_histogram, percentile_fan_chart
from montecarlo.metrics import BAND_PERCENTILES, SummaryMetrics, percentile_bands, summarize
from montecarlo.portfolio import Asset, Portfolio, PortfolioValidationError, uniform_correlation
from montecarlo.simulation import (
    MAX_SIMULATION_COUNT,
    MAX_YEARS,
    MONTHS_PER_YEAR,
    SimulationParameters,
    SimulationParametersError,
    SimulationResult,
    simulate,
)

PERCENT = 100
RESULT_STATE_KEY = "simulation_result"

NAME_COLUMN = "Aktivum"
WEIGHT_COLUMN = "Váha (%)"
RETURN_COLUMN = "Očekávaný roční výnos (%)"
VOLATILITY_COLUMN = "Roční volatilita (%)"

DEFAULT_ASSETS = pd.DataFrame(
    [
        {NAME_COLUMN: "Akcie svět", WEIGHT_COLUMN: 60.0, RETURN_COLUMN: 7.0, VOLATILITY_COLUMN: 16.0},
        {NAME_COLUMN: "Dluhopisy", WEIGHT_COLUMN: 30.0, RETURN_COLUMN: 3.0, VOLATILITY_COLUMN: 5.0},
        {NAME_COLUMN: "Zlato", WEIGHT_COLUMN: 10.0, RETURN_COLUMN: 4.0, VOLATILITY_COLUMN: 15.0},
    ]
)


def main() -> None:
    st.set_page_config(page_title="Monte Carlo portfolio", page_icon="🎲", layout="wide")
    st.title("🎲 Monte Carlo simulace portfolia")
    st.caption(
        "Zadej složení portfolia a parametry simulace. Výnosy aktiv se modelují jako korelovaný "
        "geometrický Brownův pohyb s měsíčním rebalancováním na cílové váhy."
    )

    parameters = render_simulation_parameters()
    asset_table = render_asset_editor()
    correlation = render_correlation_editor(asset_names(asset_table))

    if st.button("Spustit simulaci", type="primary"):
        run_simulation(asset_table, correlation, parameters)

    result = st.session_state.get(RESULT_STATE_KEY)
    if result is not None:
        render_results(result)


def render_simulation_parameters() -> SimulationParameters | None:
    with st.sidebar:
        st.header("Parametry simulace")
        initial_value = st.number_input("Počáteční investice", min_value=0.0, value=1_000_000.0, step=10_000.0)
        monthly_contribution = st.number_input("Měsíční vklad", min_value=0.0, value=0.0, step=1_000.0)
        years = st.slider("Investiční horizont (roky)", min_value=1, max_value=MAX_YEARS, value=10)
        simulation_count = st.slider(
            "Počet simulací", min_value=100, max_value=MAX_SIMULATION_COUNT, value=5_000, step=100
        )
        use_seed = st.checkbox("Pevný seed (opakovatelné výsledky)", value=False)
        seed = int(st.number_input("Seed", min_value=0, value=42, step=1)) if use_seed else None

    try:
        return SimulationParameters(
            initial_value=initial_value,
            monthly_contribution=monthly_contribution,
            years=years,
            simulation_count=simulation_count,
            seed=seed,
        )
    except SimulationParametersError as error:
        st.sidebar.error(str(error))
        return None


def render_asset_editor() -> pd.DataFrame:
    st.subheader("Portfolio")
    asset_table = st.data_editor(
        DEFAULT_ASSETS,
        num_rows="dynamic",
        use_container_width=True,
        key="asset_editor",
        column_config={
            WEIGHT_COLUMN: st.column_config.NumberColumn(min_value=0.0, max_value=100.0, step=0.5),
            RETURN_COLUMN: st.column_config.NumberColumn(min_value=-100.0, step=0.1),
            VOLATILITY_COLUMN: st.column_config.NumberColumn(min_value=0.0, step=0.1),
        },
    )
    weight_sum = asset_table[WEIGHT_COLUMN].fillna(0).sum()
    st.caption(f"Součet vah: **{weight_sum:.2f} %** (musí být 100 %)")
    return asset_table


def render_correlation_editor(names: List[str]) -> np.ndarray:
    with st.expander("Korelace mezi aktivy"):
        if not has_valid_names(names):
            st.info("Korelace půjde upravit, až budou mít všechna aktiva vyplněný a unikátní název.")
            return np.eye(len(names))
        pairwise_correlation = st.slider(
            "Výchozí korelace mezi všemi páry", min_value=-0.5, max_value=1.0, value=0.2, step=0.05
        )
        st.caption("Jednotlivé páry můžeš upravit v matici. Rozhodují hodnoty nad diagonálou.")
        default_matrix = pd.DataFrame(
            uniform_correlation(len(names), pairwise_correlation), index=names, columns=names
        )
        edited_matrix = st.data_editor(
            default_matrix,
            use_container_width=True,
            key=f"correlation_editor_{'|'.join(names)}_{pairwise_correlation}",
        )
    return symmetric_from_upper_triangle(edited_matrix.to_numpy(dtype=float))


def has_valid_names(names: List[str]) -> bool:
    return bool(names) and all(names) and len(set(names)) == len(names)


def symmetric_from_upper_triangle(matrix: np.ndarray) -> np.ndarray:
    upper = np.triu(matrix, k=1)
    return upper + upper.T + np.eye(len(matrix))


def asset_names(asset_table: pd.DataFrame) -> List[str]:
    return [str(name).strip() for name in asset_table[NAME_COLUMN].fillna("")]


def build_portfolio(asset_table: pd.DataFrame, correlation: np.ndarray) -> Portfolio:
    if asset_table[[WEIGHT_COLUMN, RETURN_COLUMN, VOLATILITY_COLUMN]].isna().any().any():
        raise PortfolioValidationError("Vyplň u všech aktiv váhu, výnos i volatilitu.")

    assets = tuple(
        Asset(
            name=name,
            weight=row[WEIGHT_COLUMN] / PERCENT,
            expected_return=row[RETURN_COLUMN] / PERCENT,
            volatility=row[VOLATILITY_COLUMN] / PERCENT,
        )
        for name, (_, row) in zip(asset_names(asset_table), asset_table.iterrows())
    )
    return Portfolio(assets=assets, correlation=correlation)


def run_simulation(
    asset_table: pd.DataFrame, correlation: np.ndarray, parameters: SimulationParameters | None
) -> None:
    if parameters is None:
        st.error("Oprav parametry simulace v postranním panelu.")
        return
    try:
        portfolio = build_portfolio(asset_table, correlation)
    except PortfolioValidationError as error:
        st.error(str(error))
        return

    with st.spinner("Počítám simulace…"):
        st.session_state[RESULT_STATE_KEY] = simulate(portfolio, parameters)


def render_results(result: SimulationResult) -> None:
    metrics = summarize(result)
    st.divider()
    st.subheader("Výsledky")
    render_metric_tiles(metrics)

    histogram_tab, fan_chart_tab, table_tab = st.tabs(
        ["Histogram konečných hodnot", "Vývoj v čase", "Percentily"]
    )
    with histogram_tab:
        st.plotly_chart(final_value_histogram(result.final_values, metrics), use_container_width=True)
    with fan_chart_tab:
        st.plotly_chart(
            percentile_fan_chart(percentile_bands(result), result.paths), use_container_width=True
        )
    with table_tab:
        st.dataframe(percentile_table(result), use_container_width=True)

    st.download_button(
        "Stáhnout konečné hodnoty (CSV)",
        data=pd.Series(result.final_values, name="final_value").to_csv(index_label="simulation"),
        file_name="monte_carlo_final_values.csv",
        mime="text/csv",
    )


def render_metric_tiles(metrics: SummaryMetrics) -> None:
    first_row = st.columns(4)
    first_row[0].metric("Vloženo celkem", format_money(metrics.total_contributed))
    first_row[1].metric("Medián", format_money(metrics.median))
    first_row[2].metric("Průměr", format_money(metrics.mean))
    first_row[3].metric("Šance na ztrátu", f"{metrics.probability_of_loss * PERCENT:.1f} %")

    second_row = st.columns(4)
    second_row[0].metric(r"5\. percentil", format_money(metrics.percentile_5))
    second_row[1].metric(r"95\. percentil", format_money(metrics.percentile_95))
    second_row[2].metric(
        "VaR 95 %",
        format_money(metrics.value_at_risk),
        help="Ztráta vůči vloženému kapitálu, kterou s 95% pravděpodobností nepřekročíš. "
        "Záporná hodnota = zisk.",
    )
    second_row[3].metric(
        "CVaR 95 %",
        format_money(metrics.conditional_value_at_risk),
        help="Průměrná ztráta vůči vloženému kapitálu v nejhorších 5 % scénářů.",
    )

    if metrics.median_annual_return is not None:
        st.caption(f"Mediánový roční výnos (CAGR): **{metrics.median_annual_return * PERCENT:.2f} %**")


def percentile_table(result: SimulationResult) -> pd.DataFrame:
    bands = percentile_bands(result, BAND_PERCENTILES)
    month_indices = np.arange(0, result.paths.shape[1], MONTHS_PER_YEAR)
    return pd.DataFrame(
        {f"{percentile}. percentil": bands[percentile][month_indices] for percentile in BAND_PERCENTILES},
        index=pd.Index(month_indices // MONTHS_PER_YEAR, name="Rok"),
    ).round(0)


def format_money(value: float) -> str:
    return f"{value:,.0f}".replace(",", " ")


main()
