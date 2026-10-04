from __future__ import annotations

from typing import Callable, Dict, List, Tuple

from dash import dcc, html

from gbs.advantage_charts import degree_sweep_chart
from gbs.benchmark_problems import DEFAULT_BENCHMARK
from gbs.monomial_problem import degree_sweep
from gbs.photon_tuning import TuningMode
from ui import ids
from ui.guide_basics import BASICS, WHY_EXPONENTIAL
from ui.guide_practice import PRACTICE
from ui.navigation import ADVANTAGE_PATH, HIDDEN, guide_href
from ui.theory_content import TheoryTopic
from ui.topic_sections import sources_section, table_of_contents, topic_section

GUIDE_TOPICS: Tuple[TheoryTopic, ...] = BASICS + PRACTICE
GUIDE_SOURCES_ANCHOR = "pruvodce-zdroje"

INTRO = (
    "Podrobný výklad ke 3. stránce psaný pro začínajícího doktoranda: proč a jak celé Monte Carlo na Gaussian "
    "Boson Sampleru funguje, od gaussovských momentů přes fotony a ladění přístroje až po skript pro Qiskit, "
    "tvrzení firmy Qpurpose a náměty na vlastní práci. Stačí základy pravděpodobnosti a lineární algebry; "
    "kapitoly jdou číst popořadě a každá začíná krátkým shrnutím."
)


def build_guide_page() -> html.Div:
    return html.Div(
        id=ids.GUIDE_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            _back_link(),
            html.H1("Průvodce: proč a jak funguje výhoda GBS"),
            html.P(INTRO, className="lead"),
            table_of_contents(GUIDE_TOPICS, guide_href, GUIDE_SOURCES_ANCHOR),
            *[
                topic_section(number, topic, _illustrations(topic))
                for number, topic in enumerate(GUIDE_TOPICS, start=1)
            ],
            sources_section(GUIDE_TOPICS, GUIDE_SOURCES_ANCHOR),
            _back_link(),
        ],
    )


def _illustrations(topic: TheoryTopic) -> List[html.Div]:
    build_illustration = ILLUSTRATIONS.get(topic.anchor)
    return [build_illustration()] if build_illustration else []


def _single_variable_sweep() -> html.Div:
    problem = DEFAULT_BENCHMARK.problem
    return html.Div([
        html.H4("Rozptyl jednoho vzorku pro E[X²ᵏ] podle stupně (logaritmická osa)"),
        dcc.Graph(figure=degree_sweep_chart(degree_sweep(problem), problem.degree, TuningMode.PER_MODE)),
    ])


def _back_link() -> dcc.Link:
    return dcc.Link("← Zpět na Výhodu GBS", href=ADVANTAGE_PATH, className="back-link")


ILLUSTRATIONS: Dict[str, Callable[[], html.Div]] = {WHY_EXPONENTIAL.anchor: _single_variable_sweep}
