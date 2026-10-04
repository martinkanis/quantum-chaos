"""Market presets and predefined assets on the portfolio forms."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Set

from montecarlo.historical_returns import AssetClass
from montecarlo.presets import (
    LONG_RUN_PRESET,
    MARKET_PRESETS,
    PREDEFINED_ASSETS,
    ClassPair,
    MarketPreset,
    PredefinedAsset,
)
from ui.components import ASSET_CLASS_LABELS
from ui.form_parsing import (
    CLASS_COLUMN,
    NAME_COLUMN,
    RETURN_COLUMN,
    VOLATILITY_COLUMN,
    WEIGHT_COLUMN,
    Row,
    asset_names,
    parse_asset_class,
)

PERCENT = 100
PERCENT_DECIMALS = 1
CORRELATION_DECIMALS = 2

PRESET_OPTIONS = [{"label": preset.name, "value": preset.key} for preset in MARKET_PRESETS]
PRESET_HINT = (
    "Předvolba vyplní u každého aktiva výnos a volatilitu podle jeho třídy a nastaví korelaci na průměr "
    "za dané období. Hodnoty pak můžeš dál upravovat."
)
PREDEFINED_ASSET_OPTIONS = [
    {"label": f"{asset.name} – {asset.description}", "value": asset.name} for asset in PREDEFINED_ASSETS
]
ASSET_TABLE_HINT = (
    "Aktivum smažeš křížkem × na začátku řádku. Přidat jde prázdný řádek, nebo aktivum z nabídky s parametry "
    f"z historie USA {LONG_RUN_PRESET.period[0]}–{LONG_RUN_PRESET.period[1]}; váhu pak doplň."
)


@dataclass(frozen=True)
class SliderRange:
    minimum: float
    maximum: float
    step: float


class UnknownOptionError(ValueError):
    """Raised when a dropdown sends a value that no preset or predefined asset has."""


def find_preset(key: str) -> MarketPreset:
    for preset in MARKET_PRESETS:
        if preset.key == key:
            return preset
    raise UnknownOptionError(f"Neznámá předvolba trhu: {key!r}.")


def find_predefined_asset(name: str) -> PredefinedAsset:
    for asset in PREDEFINED_ASSETS:
        if asset.name == name:
            return asset
    raise UnknownOptionError(f"Neznámé předvolené aktivum: {name!r}.")


def portfolio_classes(asset_rows: List[Row]) -> Set[AssetClass]:
    classes = (parse_asset_class(row.get(CLASS_COLUMN)) for row in asset_rows)
    return {asset_class for asset_class in classes if asset_class is not None}


def apply_preset(asset_rows: List[Row], preset: MarketPreset) -> List[Row]:
    """Rows whose class the preset does not cover keep their values."""
    return [_apply_to_row(row, preset) for row in asset_rows]


def slider_correlation(preset: MarketPreset, asset_rows: List[Row], slider: SliderRange) -> float:
    """The preset's mean correlation over the portfolio's classes, snapped to the slider grid and range."""
    snapped = round(preset.mean_correlation(portfolio_classes(asset_rows)) / slider.step) * slider.step
    return round(min(max(snapped, slider.minimum), slider.maximum), CORRELATION_DECIMALS)


def preset_summary(preset: MarketPreset, asset_rows: List[Row], slider_value: float, show_returns: bool = True) -> str:
    classes = portfolio_classes(asset_rows)
    covered = [asset_class for asset_class in AssetClass if asset_class in classes and preset.covers(asset_class)]
    parameters = "; ".join(_class_parameters(preset, asset_class, show_returns) for asset_class in covered)
    correlations = ", ".join(
        f"{_pair_label(pair)} {preset.correlations[pair]:.2f}" for pair in preset.class_pairs(classes)
    )
    return (
        f"{preset.name}: {preset.description} {parameters}. Korelace {correlations or 'pro tyto třídy není'}; "
        f"průměr {preset.mean_correlation(classes):.2f}, posuvník {slider_value:.2f}."
    )


def add_predefined_asset(asset_rows: List[Row], asset: PredefinedAsset) -> List[Row]:
    """Appends the asset with long-run historical parameters and zero weight; the name is kept unique."""
    row = {
        NAME_COLUMN: _unique_name(asset.name, asset_names(asset_rows)),
        CLASS_COLUMN: asset.asset_class.value,
        WEIGHT_COLUMN: 0,
    }
    return asset_rows + [_apply_to_row(row, LONG_RUN_PRESET)]


def _unique_name(name: str, existing_names: List[str]) -> str:
    candidate, number = name, 2
    while candidate in existing_names:
        candidate, number = f"{name} {number}", number + 1
    return candidate


def _pair_label(pair: ClassPair) -> str:
    return "–".join(ASSET_CLASS_LABELS[asset_class].lower() for asset_class in pair)


def _class_parameters(preset: MarketPreset, asset_class: AssetClass, show_returns: bool) -> str:
    volatility = f"volatilita {preset.volatilities[asset_class] * PERCENT:.1f} %"
    expected_return = f"výnos {preset.expected_returns[asset_class] * PERCENT:.1f} %, " if show_returns else ""
    return f"{ASSET_CLASS_LABELS[asset_class]} {expected_return}{volatility}"


def _apply_to_row(row: Row, preset: MarketPreset) -> Row:
    asset_class = parse_asset_class(row.get(CLASS_COLUMN))
    if asset_class is None or not preset.covers(asset_class):
        return row
    return {
        **row,
        RETURN_COLUMN: round(preset.expected_returns[asset_class] * PERCENT, PERCENT_DECIMALS),
        VOLATILITY_COLUMN: round(preset.volatilities[asset_class] * PERCENT, PERCENT_DECIMALS),
    }
