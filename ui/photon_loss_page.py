"""Page of the photon loss lab: the fourth source of error of a GBS risk estimate, with the lab and the chapters."""

from __future__ import annotations

from dash import dcc, html

from gbs.benchmark_problems import BENCHMARK_PROBLEMS, find_benchmark
from ui import ids
from ui.advantage_page import DEFAULT_TUNING, TUNING_OPTIONS
from ui.components import labelled
from ui.navigation import ADVANTAGE_PATH, FAILURE_DIAGNOSTICS_PATH, HIDDEN, photon_loss_href
from ui.photon_loss_content import (
    EXAMPLE_BENCHMARK_KEY,
    IN_SHORT,
    LAB_ANCHOR,
    LAB_INTRO,
    LEAD,
    SOURCES_ANCHOR,
    TOPICS,
    TRANSMISSION_HINT,
)
from ui.topic_sections import sources_section, table_of_contents, topic_section

TITLE = "Ztráty fotonů: kdy odhad GBS-P přežije nedokonalý přístroj"
DEFAULT_TRANSMISSION_PERCENT = 90
MIN_TRANSMISSION_PERCENT = 10
MAX_TRANSMISSION_PERCENT = 100
TRANSMISSION_MARK_STEP = 10
DEFAULT_PROBLEM = find_benchmark(EXAMPLE_BENCHMARK_KEY)
"""The problem the texts of the page quote, so that the first run shows the numbers the reader has just read."""


def build_photon_loss_page() -> html.Div:
    return html.Div(
        id=ids.PHOTON_LOSS_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            html.H1(TITLE),
            html.P(LEAD, className="lead"),
            html.Div(dcc.Link(
                "← Kdy odhad rizika přes GBS selže: čtyři zdroje chyby", href=FAILURE_DIAGNOSTICS_PATH,
                className="back-link",
            )),
            html.Div(dcc.Link("Výhoda GBS: tytéž úlohy bez ztrát →", href=ADVANTAGE_PATH, className="back-link")),
            html.Div(className="in-short", children=[html.Strong("V kostce: "), dcc.Markdown(IN_SHORT)]),
            table_of_contents(TOPICS, photon_loss_href, SOURCES_ANCHOR),
            _lab_section(),
            html.Div(id=ids.PHOTON_LOSS_ERROR_MESSAGE, className="error-message"),
            dcc.Loading(html.Div(id=ids.PHOTON_LOSS_RESULTS), type="circle"),
            *[topic_section(number, topic) for number, topic in enumerate(TOPICS, start=1)],
            sources_section(TOPICS, SOURCES_ANCHOR),
        ],
    )


def _lab_section() -> html.Section:
    marks = {
        value: f"{value} %"
        for value in range(MIN_TRANSMISSION_PERCENT, MAX_TRANSMISSION_PERCENT + 1, TRANSMISSION_MARK_STEP)
    }
    return html.Section(
        id=LAB_ANCHOR,
        className="card",
        children=[
            html.H2("Laboratoř: ztráty fotonů a odhad GBS-P"),
            dcc.Markdown(LAB_INTRO, mathjax=True),
            labelled("Připravená úloha", dcc.Dropdown(
                id=ids.PHOTON_LOSS_PROBLEM_DROPDOWN,
                options=[{"label": benchmark.title, "value": benchmark.key} for benchmark in BENCHMARK_PROBLEMS],
                value=DEFAULT_PROBLEM.key, clearable=False, searchable=False,
            )),
            dcc.Markdown(DEFAULT_PROBLEM.description, id=ids.PHOTON_LOSS_PROBLEM_DESCRIPTION, mathjax=True),
            html.Div(
                className="control-grid",
                children=[
                    labelled("Ladění stlačení", dcc.RadioItems(
                        id=ids.PHOTON_LOSS_TUNING_RADIO, options=TUNING_OPTIONS, value=DEFAULT_TUNING.value,
                        className="radio-list",
                    )),
                    labelled("Propustnost η: podíl fotonů, které dorazí k detektorům", dcc.Slider(
                        id=ids.PHOTON_LOSS_TRANSMISSION_SLIDER,
                        min=MIN_TRANSMISSION_PERCENT, max=MAX_TRANSMISSION_PERCENT, step=1,
                        value=DEFAULT_TRANSMISSION_PERCENT, marks=marks, updatemode="mouseup",
                        tooltip={"placement": "bottom"},
                    )),
                ],
            ),
            html.P(TRANSMISSION_HINT, className="hint small"),
            html.Button("Spočítat", id=ids.PHOTON_LOSS_RUN_BUTTON, className="primary-button"),
        ],
    )
