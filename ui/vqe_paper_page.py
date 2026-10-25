from __future__ import annotations

from dash import dcc, html

from ui import ids
from ui.navigation import HIDDEN
from ui.topic_sections import markdown_list, source_items
from ui.vqe_paper_content import IN_ONE_SENTENCE, SOURCES, PaperSection, paper_sections

LEAD = (
    "Shrnutí článku De León a kol. (arXiv:2512.22001, prosinec 2025): VQE pro dynamickou optimalizaci portfolia "
    "na reálném čipu IBM Fez se 156 qubity, až 38 aktiv. Čísla jsme ověřili proti verzi v1 článku; vlastní dopočty "
    "a hodnocení jsou tak označené."
)


def build_vqe_paper_page() -> html.Div:
    return html.Div(
        id=ids.VQE_PAPER_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            html.H1("Článek De Leóna a kol.: VQE pro optimalizaci portfolia na IBM Fez"),
            html.P(LEAD, className="lead"),
            html.Div(className="in-short", children=[html.Strong("V jedné větě: "), html.Span(IN_ONE_SENTENCE)]),
            *[_section(section) for section in paper_sections()],
            html.Section(
                className="card theory-section",
                children=[html.H2("Zdroje"), markdown_list(source_items(SOURCES))],
            ),
        ],
    )


def _section(section: PaperSection) -> html.Section:
    return html.Section(
        className="card theory-section",
        children=[html.H2(section.title), dcc.Markdown(section.markdown, mathjax=True)],
    )
