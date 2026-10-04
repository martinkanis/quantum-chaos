from __future__ import annotations

from typing import Callable, Dict, List

from dash import dcc, html

from gbs.charts import error_constant_chart
from gbs.demo import gbs_error_constants
from gbs.expectation import ALLOWED_DEGREES, MomentProblem, hafnian_terms, mc_relative_error_constant
from ui import ids
from ui.gbs_page import DEFAULT_DEGREE, DEFAULT_SQUEEZING_STRENGTH, default_portfolio, squeezing_strength_grid
from ui.gbs_results import hafnian_table
from ui.navigation import GBS_PATH, HIDDEN, theory_href
from ui.theory_content import COMPARISON, SOURCES_ANCHOR, TOPICS, WICK_THEOREM, TheoryTopic
from ui.topic_sections import sources_section, table_of_contents, topic_section

INTRO = (
    "Veškerá podrobná vysvětlení ke 2. stránce na jednom místě: co jednotlivé pojmy znamenají, proč jednotlivé "
    "kroky fungují, čísla pro výchozí portfolio (akcie 60 %, dluhopisy 30 %, zlato 10 %) a literatura – u každého "
    "tématu i souhrnně na konci stránky, česká i původní články."
)


def build_theory_page() -> html.Div:
    return html.Div(
        id=ids.THEORY_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            _back_link(),
            html.H1("Teorie Monte Carla na GBS krok za krokem"),
            html.P(INTRO, className="lead"),
            table_of_contents(TOPICS, theory_href, SOURCES_ANCHOR),
            *[topic_section(number, topic, _illustrations(topic)) for number, topic in enumerate(TOPICS, start=1)],
            sources_section(TOPICS, SOURCES_ANCHOR),
            _back_link(),
        ],
    )


def _illustrations(topic: TheoryTopic) -> List[html.Div]:
    build_illustration = ILLUSTRATIONS.get(topic.anchor)
    return [build_illustration()] if build_illustration else []


def _wick_table() -> html.Div:
    portfolio = default_portfolio()
    problem = MomentProblem(covariance=portfolio.covariance(), weights=portfolio.weights, degree=DEFAULT_DEGREE)
    terms = hafnian_terms(problem)
    return html.Div([
        html.H4(f"Všech {len(terms)} členů pro výchozí portfolio a d = {DEFAULT_DEGREE} (aktiva 1–3: akcie, "
                "dluhopisy, zlato)"),
        hafnian_table(terms, moment=sum(term.contribution for term in terms)),
    ])


def _error_constant_graph() -> html.Div:
    portfolio = default_portfolio()
    strengths = squeezing_strength_grid()
    gbs_constants = gbs_error_constants(portfolio.covariance(), portfolio.weights, strengths, ALLOWED_DEGREES)
    mc_constants = {degree: mc_relative_error_constant(degree) for degree in ALLOWED_DEGREES}
    return html.Div([
        html.H4("Konstanta chyby c pro výchozí portfolio: GBS (plná čára) a klasické MC (čárkovaně)"),
        dcc.Graph(figure=error_constant_chart(strengths, gbs_constants, mc_constants, DEFAULT_SQUEEZING_STRENGTH)),
        html.P(
            "Nižší je lepší. Tam, kde plná čára leží pod čárkovanou stejné barvy, potřebuje GBS k téže přesnosti "
            "méně vzorků než klasické Monte Carlo – (c_MC / c_GBS)² krát méně.",
            className="hint small",
        ),
    ])


def _back_link() -> dcc.Link:
    return dcc.Link("← Zpět na Monte Carlo na GBS", href=GBS_PATH, className="back-link")


ILLUSTRATIONS: Dict[str, Callable[[], html.Div]] = {
    WICK_THEOREM.anchor: _wick_table,
    COMPARISON.anchor: _error_constant_graph,
}
