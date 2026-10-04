from __future__ import annotations

from typing import List

from dash import dash_table, dcc, html

from gbs.benchmark_problems import BENCHMARK_PROBLEMS, DEFAULT_BENCHMARK
from gbs.monomial_problem import MAX_VARIABLES
from gbs.photon_tuning import TuningMode
from ui import ids
from ui.advantage_content import (
    ASSESSMENT,
    AUTHOR_PAPERS,
    CLAIM_SOURCES,
    CLAIMS,
    HYPOTHESIS,
    IN_SHORT,
    LAB_INTRO,
    LEAD,
    MATRIX_HINT,
    QISKIT_TEXT,
    RELATED_PAPERS,
    TUNING_HINT,
)
from ui.advantage_form import VARIABLE_COLUMN, covariance_column_id, matrix_columns, matrix_rows
from ui.components import (
    REFERENCE_SEED,
    SCROLLABLE_TABLE_STYLE,
    TABLE_CELL_STYLE,
    TABLE_HEADER_STYLE,
    labelled,
    seed_dropdown,
)
from ui.gbs_page import DEFAULT_MAX_SAMPLE_SIZE, SAMPLE_SIZE_OPTIONS
from ui.guide_basics import BIG_PICTURE
from ui.guide_practice import CAVEATS, FIVE_PROBLEMS, QISKIT, QPURPOSE
from ui.navigation import GUIDE_PATH, HIDDEN, guide_href
from ui.topic_sections import markdown_list, source_items

TUNING_OPTIONS = [
    {"label": "Fotony v každém módu = exponent (doporučeno, naše rozšíření)", "value": TuningMode.PER_MODE.value},
    {"label": "Jen celkový počet fotonů = stupeň (jako Andersen a Shan)", "value": TuningMode.TOTAL.value},
]
DEFAULT_TUNING = TuningMode.PER_MODE
LOWER_TRIANGLE_STYLE = {"color": "var(--text-muted)", "backgroundColor": "var(--surface-muted)"}


def build_advantage_page() -> html.Div:
    return html.Div(
        id=ids.ADVANTAGE_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            html.H1("🚀 Výhoda GBS: kdy kvantové vzorkování porazí Monte Carlo"),
            html.P(LEAD, className="lead"),
            dcc.Link(
                "Průvodce pro začínajícího doktoranda: proč a jak to celé funguje →", href=GUIDE_PATH,
                className="back-link",
            ),
            html.Div(className="in-short", children=[html.Strong("V kostce: "), dcc.Markdown(IN_SHORT)]),
            _text_card("Co tvrdí Qpurpose a Jyske Bank", CLAIMS, QPURPOSE.anchor),
            _text_card("Jak to podle nás nejspíš funguje", HYPOTHESIS, BIG_PICTURE.anchor),
            _lab_section(),
            html.Div(id=ids.ADVANTAGE_ERROR_MESSAGE, className="error-message"),
            dcc.Loading(html.Div(id=ids.ADVANTAGE_RESULTS), type="circle"),
            _qiskit_section(),
            _text_card("Co si o tvrzeních myslet", ASSESSMENT, CAVEATS.anchor),
            _papers_section(),
        ],
    )


def _text_card(title: str, markdown: str, guide_anchor: str) -> html.Section:
    return html.Section(
        className="card",
        children=[
            html.H2(title),
            dcc.Markdown(markdown, mathjax=True),
            dcc.Link("Podrobně v průvodci →", href=guide_href(guide_anchor), className="details-link"),
        ],
    )


def _lab_section() -> html.Section:
    rows = matrix_rows(DEFAULT_BENCHMARK.problem)
    return html.Section(
        className="card",
        children=[
            html.H2("Laboratoř: zadej matici a monom"),
            dcc.Markdown(LAB_INTRO, mathjax=True),
            labelled("Připravená úloha", dcc.Dropdown(
                id=ids.ADVANTAGE_PROBLEM_DROPDOWN,
                options=[{"label": benchmark.title, "value": benchmark.key} for benchmark in BENCHMARK_PROBLEMS],
                value=DEFAULT_BENCHMARK.key, clearable=False, searchable=False,
            )),
            dcc.Markdown(DEFAULT_BENCHMARK.description, id=ids.ADVANTAGE_PROBLEM_DESCRIPTION, mathjax=True),
            dcc.Link(
                "Proč je každá z pěti úloh vhodná →", href=guide_href(FIVE_PROBLEMS.anchor), className="details-link",
            ),
            labelled("Počet proměnných", dcc.Dropdown(
                id=ids.ADVANTAGE_VARIABLE_COUNT_DROPDOWN,
                options=[{"label": str(count), "value": count} for count in range(1, MAX_VARIABLES + 1)],
                value=len(rows), clearable=False, searchable=False,
            )),
            dash_table.DataTable(
                id=ids.ADVANTAGE_MATRIX_TABLE,
                data=rows,
                columns=matrix_columns(rows),
                editable=True,
                style_cell=TABLE_CELL_STYLE,
                style_cell_conditional=[{"if": {"column_id": VARIABLE_COLUMN}, "textAlign": "left"}],
                style_header=TABLE_HEADER_STYLE,
                style_data_conditional=_lower_triangle_styles(),
                style_table=SCROLLABLE_TABLE_STYLE,
            ),
            html.P(MATRIX_HINT, className="hint small"),
            html.Div(
                className="control-grid",
                children=[
                    labelled("Ladění stlačení", dcc.RadioItems(
                        id=ids.ADVANTAGE_TUNING_RADIO, options=TUNING_OPTIONS, value=DEFAULT_TUNING.value,
                        className="radio-list",
                    )),
                    labelled("Maximální počet vzorků N", dcc.Dropdown(
                        id=ids.ADVANTAGE_MAX_SHOTS_DROPDOWN,
                        options=[
                            {"label": f"{size:,}".replace(",", " "), "value": size} for size in SAMPLE_SIZE_OPTIONS
                        ],
                        value=DEFAULT_MAX_SAMPLE_SIZE, clearable=False, searchable=False,
                    )),
                    seed_dropdown(ids.ADVANTAGE_SEED_DROPDOWN, default_value=REFERENCE_SEED),
                ],
            ),
            html.P(TUNING_HINT, className="hint small"),
            html.Button("Spočítat a nasimulovat", id=ids.ADVANTAGE_RUN_BUTTON, className="primary-button"),
        ],
    )


def _qiskit_section() -> html.Section:
    """Stays in the initial layout, so the download callback always finds its button."""
    return html.Section(
        className="card",
        children=[
            html.H2("Spustit v Qiskitu"),
            dcc.Markdown(QISKIT_TEXT, mathjax=True),
            html.Button(
                "Stáhnout skript pro Qiskit (.py)", id=ids.QISKIT_DOWNLOAD_BUTTON, className="secondary-button",
            ),
            html.P(id=ids.QISKIT_DOWNLOAD_MESSAGE, className="hint small"),
            dcc.Download(id=ids.QISKIT_DOWNLOAD),
            dcc.Link("Jak skript funguje krok za krokem →", href=guide_href(QISKIT.anchor),
                     className="details-link"),
        ],
    )


def _papers_section() -> html.Section:
    return html.Section(
        className="card",
        children=[
            html.H2("Publikované články a zdroje"),
            html.H3("Od autorů metody"),
            markdown_list(source_items(AUTHOR_PAPERS)),
            html.P(
                "Nic dalšího k metodě publikované není: obě práce jsou zatím preprinty bez recenzované verze "
                "a článek o aplikaci pro Jyske Bank ani o číslech z webu Qpurpose neexistuje.",
                className="hint",
            ),
            html.H3("Nezávislé související práce"),
            markdown_list(source_items(RELATED_PAPERS)),
            html.H3("Odkud jsou tvrzení Qpurpose"),
            markdown_list(source_items(CLAIM_SOURCES)),
        ],
    )


def _lower_triangle_styles() -> List[dict]:
    """Cells below the diagonal mirror the upper triangle, so they look secondary."""
    return [
        {"if": {"row_index": row, "column_id": covariance_column_id(column)}, **LOWER_TRIANGLE_STYLE}
        for row in range(MAX_VARIABLES)
        for column in range(row)
    ]
