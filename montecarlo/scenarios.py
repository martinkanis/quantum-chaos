"""Stress scenarios: what one year of given asset-class returns does to the portfolio."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Optional, Sequence, Tuple

from montecarlo.historical_returns import AssetClass, annual_returns


class ScenarioValidationError(ValueError):
    """Raised when a user-defined scenario is incomplete."""


@dataclass(frozen=True)
class StressScenario:
    name: str
    returns: Mapping[AssetClass, float]
    """Return over the scenario year per asset class, as a fraction (0.07 = 7 %)."""
    year: Optional[int] = None
    description: str = ""


def historical_scenario(year: int, name: str, description: str) -> StressScenario:
    return StressScenario(name=name, returns=annual_returns(year), year=year, description=description)


def portfolio_return(
    weights: Sequence[float], asset_classes: Sequence[AssetClass], scenario: StressScenario
) -> float:
    """Return of the portfolio held through the scenario year; every asset moves like its class."""
    return float(sum(weight * scenario.returns[asset_class] for weight, asset_class in zip(weights, asset_classes)))


STRESS_SCENARIOS: Tuple[StressScenario, ...] = (
    historical_scenario(
        1931, "Velká hospodářská krize",
        "Nejhorší rok akcií v datech: krachy bank, deflace a Británie opustila zlatý standard.",
    ),
    historical_scenario(
        1937, "Recese 1937", "Druhá vlna krize po zpřísnění měnové a fiskální politiky.",
    ),
    historical_scenario(
        1973, "Ropný šok", "Ropné embargo OPEC a konec brettonwoodského systému; zlato prudce zdražilo.",
    ),
    historical_scenario(
        1974, "Stagflace", "Pokračující ropná krize a vysoká inflace, akcie v hlubokém medvědím trhu.",
    ),
    historical_scenario(
        1979, "Inflace a zlatá horečka",
        "Druhý ropný šok po íránské revoluci a dvouciferná inflace; zlato víc než zdvojnásobilo cenu.",
    ),
    historical_scenario(
        1981, "Volckerovy sazby", "Fed držel sazby kolem 20 %, aby zkrotil inflaci; zlato ztratilo třetinu.",
    ),
    historical_scenario(
        1987, "Černé pondělí",
        "19. října akcie spadly za jediný den o víc než 20 %, celý rok ale skončil v plusu.",
    ),
    historical_scenario(
        1994, "Výprodej dluhopisů", "Fed nečekaně rychle zvyšoval sazby a ceny dluhopisů prudce klesly.",
    ),
    historical_scenario(
        1995, "Boom akcií i dluhopisů", "Po poklesu dlouhodobých sazeb rostly akcie i dluhopisy o víc než 20 %.",
    ),
    historical_scenario(
        1999, "Vrchol dot-com bubliny", "Technologická horečka; rostoucí sazby srazily ceny dluhopisů.",
    ),
    historical_scenario(
        2000, "Splasknutí dot-com bubliny", "Technologické akcie se propadly, státní dluhopisy posílily.",
    ),
    historical_scenario(
        2001, "Recese a 11. září", "Hospodářská recese a teroristické útoky, druhý rok poklesu akcií.",
    ),
    historical_scenario(
        2002, "Účetní skandály", "Krachy Enronu a WorldComu, třetí rok poklesu akcií v řadě.",
    ),
    historical_scenario(
        2008, "Globální finanční krize",
        "Hypoteční krize a pád Lehman Brothers; ceny domů klesly, státní dluhopisy byly bezpečným přístavem.",
    ),
    historical_scenario(
        2009, "Oživení po krizi", "Od březnového dna rostly akcie i zlato, dluhopisy ztrácely.",
    ),
    historical_scenario(
        2011, "Dluhová krize eurozóny", "Obavy o Řecko a snížení ratingu USA; dluhopisy i zlato posílily.",
    ),
    historical_scenario(
        2013, "Taper tantrum",
        "Fed naznačil utlumení nákupů dluhopisů; akcie rostly, zlato ztratilo přes čtvrtinu.",
    ),
    historical_scenario(
        2018, "Výprodej na konci roku",
        "Zvyšování sazeb a obchodní válka USA s Čínou; všechny tři třídy mírně v minusu.",
    ),
    historical_scenario(
        2020, "Covid", "Propad v březnu se do konce roku vymazal, celý rok vyšel všem třídám kladně.",
    ),
    historical_scenario(
        2022, "Inflační šok",
        "Rychlé zvyšování sazeb kvůli inflaci; akcie i dluhopisy klesly současně zhruba o 18 %.",
    ),
)
