from __future__ import annotations

from typing import Callable, Dict, List

import numpy as np
from dash import dcc, html

from gbs.charts import useful_fraction_chart
from gbs.demo import useful_shot_fractions
from gbs.expectation import ALLOWED_DEGREES
from ui import ids
from ui.caveats_content import CAVEATS, DISCARDED_SHOTS, REFERENCES_MARKDOWN, Caveat
from ui.form_parsing import DEFAULT_ASSET_ROWS, asset_names, build_portfolio, default_correlation_rows
from ui.gbs_page import DEFAULT_SQUEEZING_STRENGTH, MAX_SQUEEZING_STRENGTH, MIN_SQUEEZING_STRENGTH, SQUEEZING_STEP
from ui.navigation import GBS_PATH, HIDDEN, caveat_href
from ui.portfolio_page import DEFAULT_PAIRWISE_CORRELATION

INTRO = (
    "Rozvedení omezení z 2. stránky. U každého háčku: co přesně znamená, proč vzniká, konkrétní příklad "
    "a co by se s ním dalo dělat."
)


def build_caveats_page() -> html.Div:
    return html.Div(
        id=ids.CAVEATS_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            _back_link(),
            html.H1("Háčky Monte Carla na GBS podrobně"),
            html.P(INTRO, className="lead"),
            _table_of_contents(),
            *[_caveat_section(number, caveat) for number, caveat in enumerate(CAVEATS, start=1)],
            html.Section(className="card", children=[html.H2("Zdroje"), dcc.Markdown(REFERENCES_MARKDOWN)]),
            _back_link(),
        ],
    )


def _table_of_contents() -> html.Nav:
    return html.Nav(
        className="card toc",
        children=[
            html.H2("Obsah"),
            html.Ol([html.Li(dcc.Link(caveat.title, href=caveat_href(caveat.anchor))) for caveat in CAVEATS]),
        ],
    )


def _caveat_section(number: int, caveat: Caveat) -> html.Section:
    return html.Section(
        id=caveat.anchor,
        className="card step caveat-section",
        children=[
            html.H2([html.Span(str(number), className="step-number"), caveat.title]),
            html.Div(className="in-short", children=[
                html.Strong("V kostce: "), dcc.Markdown(caveat.summary, mathjax=True),
            ]),
            dcc.Markdown(caveat.explanation, mathjax=True),
            *_illustrations(caveat),
            html.H3("Co s tím"),
            dcc.Markdown(caveat.remedies, mathjax=True),
        ],
    )


def _illustrations(caveat: Caveat) -> List:
    build_illustration = ILLUSTRATIONS.get(caveat.anchor)
    return [build_illustration()] if build_illustration else []


def _useful_fraction_graph() -> html.Div:
    names = asset_names(DEFAULT_ASSET_ROWS)
    portfolio = build_portfolio(DEFAULT_ASSET_ROWS, default_correlation_rows(names, DEFAULT_PAIRWISE_CORRELATION))
    strengths = np.round(np.arange(MIN_SQUEEZING_STRENGTH, MAX_SQUEEZING_STRENGTH + SQUEEZING_STEP / 2, SQUEEZING_STEP), 2)
    fractions = useful_shot_fractions(portfolio.covariance(), strengths, ALLOWED_DEGREES)
    return html.Div([
        html.H4("Podíl užitečných výstřelů (s přesně d fotony) pro výchozí portfolio"),
        dcc.Graph(figure=useful_fraction_chart(strengths, fractions, DEFAULT_SQUEEZING_STRENGTH)),
    ])


def _back_link() -> dcc.Link:
    return dcc.Link("← Zpět na Monte Carlo na GBS", href=GBS_PATH, className="back-link")


ILLUSTRATIONS: Dict[str, Callable[[], html.Div]] = {DISCARDED_SHOTS.anchor: _useful_fraction_graph}
