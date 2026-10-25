"""Literature review page: the TL;DR first, then the topics of the review and questions to test yourself."""

from __future__ import annotations

from typing import Dict, Tuple

from dash import dcc, html

from ui import ids
from ui.literature_review_content import (
    CLAIMS_TOPIC,
    CRITICISM_TOPIC,
    GATE_BASED_TOPIC,
    HARDWARE_TOPIC,
    INTRO,
    KEY_FINDINGS,
    OPEN_QUESTIONS_TOPIC,
    REVIEW_QUESTIONS,
    SOURCES_ANCHOR,
    THEORY_TOPIC,
    TITLE,
    TOPICS,
    TWENTE_TOPIC,
    ReviewQuestion,
)
from ui.navigation import (
    ACADEMY_PATH,
    ADVANTAGE_PATH,
    HIDDEN,
    PHOTONIC_HARDWARE_PATH,
    caveat_href,
    guide_href,
    literature_review_href,
    theory_href,
)
from ui.topic_sections import (
    RelatedLink,
    key_findings_card,
    related_pages,
    sources_section,
    table_of_contents,
    topic_section,
)

REVIEW_QUESTIONS_ANCHOR = "reserse-otazky"
REVIEW_QUESTIONS_HINT = (
    "Zkus nejdřív odpovědět sám a teprve pak odpověď rozbal. Vybavování si látky ji upevní víc než další čtení "
    "(tzv. testing effect)."
)

RELATED_PAGES: Dict[str, Tuple[RelatedLink, ...]] = {
    CLAIMS_TOPIC.anchor: (
        ("Co tvrdí Qpurpose a jak to číst (Průvodce)", guide_href("pruvodce-qpurpose")),
        ("Výhoda GBS", ADVANTAGE_PATH),
    ),
    THEORY_TOPIC.anchor: (
        ("Co přesně dokázali Andersen a Shan (Teorie)", theory_href("exponencialni-vyhoda")),
        ("Proč je výhoda exponenciální (Průvodce)", guide_href("pruvodce-proc-exponencialne")),
    ),
    TWENTE_TOPIC.anchor: (("Příbuzné práce na stránce Výhoda GBS", ADVANTAGE_PATH),),
    GATE_BASED_TOPIC.anchor: (
        ("Háček: VaR a CVaR nejsou polynomy", caveat_href("var-cvar")),
        ("Classiq a CUDA-Q v Quantum Academy", ACADEMY_PATH),
    ),
    HARDWARE_TOPIC.anchor: (
        ("Háček: reálný hardware není ideální", caveat_href("realny-hardware")),
        ("Platformy Classiq a CUDA-Q (Quantum Academy)", ACADEMY_PATH),
        ("Gaussian Boson Sampler: co je to za zařízení (Teorie)", theory_href("gbs-zarizeni")),
        ("Quandela a fotonický hardware v Evropě", PHOTONIC_HARDWARE_PATH),
    ),
    CRITICISM_TOPIC.anchor: (
        ("Háček: GBS je tady simulované klasicky", caveat_href("klasicka-simulace")),
        ("Klasická simulace GBS (Průvodce)", guide_href("pruvodce-simulace")),
    ),
    OPEN_QUESTIONS_TOPIC.anchor: (("Náměty na další práci (Průvodce)", guide_href("pruvodce-dal")),),
}


def build_literature_review_page() -> html.Div:
    return html.Div(
        id=ids.LITERATURE_REVIEW_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            html.H1(TITLE),
            html.P(INTRO, className="lead"),
            _key_findings_card(),
            table_of_contents(TOPICS, literature_review_href, SOURCES_ANCHOR),
            *[
                topic_section(number, topic, related_pages(RELATED_PAGES.get(topic.anchor, ())))
                for number, topic in enumerate(TOPICS, start=1)
            ],
            _review_questions_card(),
            sources_section(TOPICS, SOURCES_ANCHOR),
        ],
    )


def _key_findings_card() -> html.Section:
    footer = dcc.Link(
        "Na konci stránky si můžeš ověřit porozumění →",
        href=literature_review_href(REVIEW_QUESTIONS_ANCHOR),
        className="details-link",
    )
    return key_findings_card(KEY_FINDINGS, literature_review_href, footer)


def _review_questions_card() -> html.Section:
    return html.Section(
        id=REVIEW_QUESTIONS_ANCHOR,
        className="card theory-section review-questions",
        children=[
            html.H2("Ověř si porozumění"),
            html.P(REVIEW_QUESTIONS_HINT, className="hint"),
            *[_review_question(number, question) for number, question in enumerate(REVIEW_QUESTIONS, start=1)],
        ],
    )


def _review_question(number: int, question: ReviewQuestion) -> html.Details:
    return html.Details(
        className="review-question",
        children=[
            html.Summary(f"{number}. {question.question}"),
            dcc.Markdown(question.answer, mathjax=True),
            dcc.Link("Kde se to probírá →", href=literature_review_href(question.anchor), className="details-link"),
        ],
    )
