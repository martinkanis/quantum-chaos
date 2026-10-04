"""Market presets and predefined assets: ready-made parameters for each asset class."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Collection, Mapping, Optional, Tuple

from montecarlo.historical_returns import AssetClass, period_statistics

ClassPair = Tuple[AssetClass, AssetClass]
DEFAULT_CORRELATION = 0.2
DEFAULT_CLASSES = (AssetClass.STOCKS, AssetClass.BONDS, AssetClass.GOLD)


@dataclass(frozen=True)
class MarketPreset:
    key: str
    name: str
    description: str
    expected_returns: Mapping[AssetClass, float]
    volatilities: Mapping[AssetClass, float]
    correlations: Mapping[ClassPair, float]
    """Correlation of each pair of classes the preset covers."""
    period: Optional[Tuple[int, int]] = None
    """First and last year of the historical data the parameters come from."""

    def covers(self, asset_class: AssetClass) -> bool:
        return asset_class in self.expected_returns

    def class_pairs(self, asset_classes: Collection[AssetClass]) -> Tuple[ClassPair, ...]:
        """Pairs of distinct classes from the portfolio that the preset has a correlation for."""
        return tuple(pair for pair in self.correlations if pair[0] in asset_classes and pair[1] in asset_classes)

    def mean_correlation(self, asset_classes: Collection[AssetClass]) -> float:
        """The model uses one correlation for all pairs, so it takes the mean over the portfolio's class pairs."""
        pairs = self.class_pairs(asset_classes) or tuple(self.correlations)
        return sum(self.correlations[pair] for pair in pairs) / len(pairs)


@dataclass(frozen=True)
class PredefinedAsset:
    name: str
    asset_class: AssetClass
    description: str


def historical_preset(key: str, name: str, first_year: int, last_year: int, description: str) -> MarketPreset:
    statistics = period_statistics(range(first_year, last_year + 1))
    return MarketPreset(
        key=key,
        name=name,
        description=description,
        expected_returns=statistics.expected_returns,
        volatilities=statistics.volatilities,
        correlations=statistics.correlations,
        period=(first_year, last_year),
    )


DEFAULT_PRESET = MarketPreset(
    key="vychozi",
    name="Výchozí nastavení aplikace",
    description="Hodnoty, se kterými aplikace startuje; pokrývá akcie, státní dluhopisy a zlato.",
    expected_returns={AssetClass.STOCKS: 0.07, AssetClass.BONDS: 0.03, AssetClass.GOLD: 0.04},
    volatilities={AssetClass.STOCKS: 0.16, AssetClass.BONDS: 0.05, AssetClass.GOLD: 0.15},
    correlations={pair: DEFAULT_CORRELATION for pair in combinations(DEFAULT_CLASSES, 2)},
)

LONG_RUN_PRESET = historical_preset(
    "historie-1928-2023", "Historie USA 1928–2023", 1928, 2023,
    "Celá dostupná historie včetně Velké hospodářské krize.",
)

MARKET_PRESETS: Tuple[MarketPreset, ...] = (
    DEFAULT_PRESET,
    LONG_RUN_PRESET,
    historical_preset(
        "historie-1972-2023", "Historie USA 1972–2023", 1972, 2023,
        "Období po konci brettonwoodského systému, kdy cena zlata už nebyla pevně daná.",
    ),
    historical_preset(
        "stagflace-1973-1981", "Stagflace 1973–1981", 1973, 1981,
        "Ropné šoky a vysoká inflace; akcie i dluhopisy slabé, zlato velmi rozkolísané.",
    ),
    historical_preset(
        "nizke-sazby-2010-2019", "Nízké sazby 2010–2019", 2010, 2019,
        "Desetiletí téměř nulových sazeb a dlouhého růstu akcií s nízkou volatilitou.",
    ),
)

PREDEFINED_ASSETS: Tuple[PredefinedAsset, ...] = (
    PredefinedAsset("Akcie USA (S&P 500)", AssetClass.STOCKS, "Velké americké firmy včetně dividend."),
    PredefinedAsset("Hotovost (T-bills)", AssetClass.BILLS, "Tříměsíční státní pokladniční poukázky USA."),
    PredefinedAsset("Státní dluhopisy USA", AssetClass.BONDS, "Desetileté státní dluhopisy USA."),
    PredefinedAsset("Firemní dluhopisy Baa", AssetClass.CORPORATE_BONDS, "Dluhopisy firem s ratingem Baa."),
    PredefinedAsset(
        "Nemovitosti USA", AssetClass.REAL_ESTATE, "Ceny domů podle indexu Case-Shiller, bez příjmu z nájmu.",
    ),
    PredefinedAsset("Zlato", AssetClass.GOLD, "Cena zlata."),
)
