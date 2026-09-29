from __future__ import annotations

from typing import Callable, Dict, List

from dash import dcc, html

from gbs.charts import error_constant_chart
from gbs.demo import gbs_error_constants
from gbs.expectation import ALLOWED_DEGREES, MomentProblem, hafnian_terms, mc_relative_error_constant
from ui import ids
from ui.gbs_page import DEFAULT_DEGREE, DEFAULT_SQUEEZING_STRENGTH, default_portfolio, squeezing_strength_grid
from ui.gbs_results import hafnian_table
from ui.navigation import GBS_PATH, HIDDEN, caveat_href, theory_href
from ui.theory_content import COMPARISON, TOPICS, WICK_THEOREM, TheoryTopic

INTRO = (
    "Podrobné vysvětlení kroků z 2. stránky: co jednotlivé pojmy znamenají, proč jednotlivé kroky fungují, "
    "čísla pro výchozí portfolio (akcie 60 %, dluhopisy 30 %, zlato 10 %) a literatura – české zdroje "
    "i původní články."
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
            _table_of_contents(),
            *[_topic_section(number, topic) for number, topic in enumerate(TOPICS, start=1)],
            _back_link(),
        ],
    )


def _table_of_contents() -> html.Nav:
    return html.Nav(
        className="card toc",
        children=[
            html.H2("Obsah"),
            html.Ol([html.Li(dcc.Link(topic.title, href=theory_href(topic.anchor))) for topic in TOPICS]),
        ],
    )


def _topic_section(number: int, topic: TheoryTopic) -> html.Section:
    return html.Section(
        id=topic.anchor,
        className="card step theory-section",
        children=[
            html.H2([html.Span(str(number), className="step-number"), topic.title]),
            html.Div(className="in-short", children=[
                html.Strong("V kostce: "), dcc.Markdown(topic.in_short, mathjax=True),
            ]),
            dcc.Markdown(topic.explanation, mathjax=True),
            *_illustrations(topic),
            *_related_caveats(topic),
            html.H3("Kde číst dál"),
            dcc.Markdown(topic.further_reading, mathjax=True, link_target="_blank"),
        ],
    )


def _illustrations(topic: TheoryTopic) -> List:
    build_illustration = ILLUSTRATIONS.get(topic.anchor)
    return [build_illustration()] if build_illustration else []


def _related_caveats(topic: TheoryTopic) -> List:
    if not topic.related_caveats:
        return []
    links: List = []
    for caveat in topic.related_caveats:
        if links:
            links.append(", ")
        links.append(dcc.Link(caveat.title, href=caveat_href(caveat.anchor)))
    return [html.P(className="hint", children=["Související háčky: ", *links])]


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
