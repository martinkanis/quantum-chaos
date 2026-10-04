from __future__ import annotations

import numpy as np
from dash import dash_table, dcc, html

from gbs.demo import MAX_SAMPLE_SIZE
from gbs.expectation import ALLOWED_DEGREES
from gbs.sampler import MAX_MODES
from montecarlo.portfolio import Portfolio
from ui import ids
from ui.caveats_content import CAVEATS, REFERENCES_MARKDOWN, SIGN_PROBLEM
from ui.components import (
    ASSET_CLASS_COLUMN,
    ASSET_CLASS_DROPDOWN,
    REFERENCE_SEED,
    SCROLLABLE_TABLE_STYLE,
    TABLE_CELL_STYLE,
    TABLE_HEADER_STYLE,
    details_link,
    labelled,
    seed_dropdown,
)
from ui.form_parsing import (
    DEFAULT_ASSET_ROWS,
    NAME_COLUMN,
    VOLATILITY_COLUMN,
    WEIGHT_COLUMN,
    asset_names,
    build_centered_portfolio,
    default_correlation_rows,
)
from ui.market_presets import (
    ASSET_TABLE_HINT,
    PREDEFINED_ASSET_OPTIONS,
    PRESET_HINT,
    PRESET_OPTIONS,
    SliderRange,
)
from ui.navigation import CAVEATS_PATH, HIDDEN, THEORY_PATH, caveat_href, theory_href
from ui.portfolio_page import DEFAULT_PAIRWISE_CORRELATION, correlation_table_columns
from ui.theory_content import (
    CORRELATION,
    ESTIMATOR,
    GBS_DEVICE,
    MONTE_CARLO,
    SOURCES_ANCHOR,
    WICK_THEOREM,
    TheoryTopic,
)

DEFAULT_DEGREE = 4
DEFAULT_SQUEEZING_STRENGTH = 0.7
MIN_SQUEEZING_STRENGTH = 0.1
MAX_SQUEEZING_STRENGTH = 0.95
SQUEEZING_STEP = 0.05
DEFAULT_MAX_SAMPLE_SIZE = 100_000
SAMPLE_SIZE_OPTIONS = (10_000, DEFAULT_MAX_SAMPLE_SIZE, MAX_SAMPLE_SIZE)
MIN_PAIRWISE_CORRELATION = 0.0
MAX_PAIRWISE_CORRELATION = 1.0
CORRELATION_STEP = 0.05
CORRELATION_SLIDER = SliderRange(MIN_PAIRWISE_CORRELATION, MAX_PAIRWISE_CORRELATION, CORRELATION_STEP)

DEGREE_LABELS = {
    2: "E[L²] – rozptyl výnosu portfolia",
    4: "E[L⁴] – 4. moment (citlivost na tlusté chvosty)",
    6: "E[L⁶] – 6. moment (extrémní pohyby)",
}

MONTE_CARLO_PRINCIPLE = r"""
Klasické Monte Carlo odhaduje střední hodnotu $\mathbb{E}[f(X)]$ výběrovým průměrem přes $N$ náhodných scénářů;
chyba klesá jako $1/\sqrt{N}$.
"""

WICK_PRINCIPLE = r"""
Pro gaussovské výnosy $X \sim \mathcal{N}(0, \Sigma)$ je moment vážený součet **hafniánů** kovarianční matice –
součtů přes všechna rozdělení činitelů do dvojic:

$$
\mathbb{E}[L^d] = \sum_{|n| = d} c_n\,\mathrm{Haf}(\Sigma_n), \qquad L = w^\top X .
$$
"""

GBS_PRINCIPLE = r"""
Fotonické zařízení, jehož výstupní pravděpodobnosti jsou **druhé mocniny hafniánů**:

$$
p(n) = \frac{\mathrm{Haf}(B_n)^2}{n!\,\prod_j \cosh r_j}, \qquad B = U\,\mathrm{diag}(\tanh r)\,U^\top .
$$
"""

ESTIMATOR_PRINCIPLE = r"""
Když do zařízení „nahrajeme“ $B = \gamma\Sigma$, četnosti naměřených vzorů fotonů prozradí hafniány a z nich
odhad $\mathbb{E}[L^d]$ – místo generování scénářů se počítají fotony.
"""

PRINCIPLE_BLOCKS = (
    ("Klasické Monte Carlo: průměr přes náhodné scénáře", MONTE_CARLO_PRINCIPLE, MONTE_CARLO),
    ("Wickova–Isserlisova věta: moment jako součet hafniánů", WICK_PRINCIPLE, WICK_THEOREM),
    ("Gaussian Boson Sampler: pravděpodobnosti jsou hafniány", GBS_PRINCIPLE, GBS_DEVICE),
    ("Nahrání Σ a odhad z četností", ESTIMATOR_PRINCIPLE, ESTIMATOR),
)

PORTFOLIO_HINT = (
    "Nastavuje se zvlášť, nezávisle na 1. stránce. Stačí váhy, volatility a korelace: úloha pracuje s výnosy "
    "očištěnými o střední hodnotu, takže očekávané výnosy nehrají roli. "
    f"Simulace zvládne nejvýše {MAX_MODES} aktiv a jen nezáporné korelace – "
)

ESTIMATOR_NOTE = (
    "Estimátor na této stránce odhaduje hafniány přímo z četností vzorů. Jde o ilustraci principu; "
    "konkrétní estimátory v uvedených pracích se mohou lišit."
)


def build_gbs_page() -> html.Div:
    return html.Div(
        id=ids.GBS_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            html.H1("⚛️ Monte Carlo na Gaussian Boson Sampleru"),
            html.P(
                "Jak by vypadal odhad rizikového ukazatele portfolia, kdyby vzorky místo generátoru "
                "náhodných čísel dodával fotonický kvantový počítač. Všechno níže je klasická simulace "
                "ideálního (bezztrátového) GBS.",
                className="lead",
            ),
            _principle_section(),
            _portfolio_section(),
            _correlation_section(),
            _controls(),
            html.Div(id=ids.GBS_ERROR_MESSAGE, className="error-message"),
            dcc.Loading(html.Div(id=ids.GBS_RESULTS), type="circle"),
            _caveats_summary(),
            html.Section(
                className="card",
                children=[
                    html.H2("Literatura"),
                    dcc.Markdown(REFERENCES_MARKDOWN),
                    html.P(ESTIMATOR_NOTE, className="hint"),
                    dcc.Link(
                        "Všechny zdroje včetně české literatury →", href=theory_href(SOURCES_ANCHOR),
                        className="back-link",
                    ),
                ],
            ),
        ],
    )


def default_portfolio() -> Portfolio:
    """The portfolio the GBS form starts with; the caveats and theory pages illustrate it."""
    names = asset_names(DEFAULT_ASSET_ROWS)
    return build_centered_portfolio(DEFAULT_ASSET_ROWS, default_correlation_rows(names, DEFAULT_PAIRWISE_CORRELATION))


def squeezing_strength_grid() -> np.ndarray:
    """Every value the squeezing slider offers."""
    return np.round(np.arange(MIN_SQUEEZING_STRENGTH, MAX_SQUEEZING_STRENGTH + SQUEEZING_STEP / 2, SQUEEZING_STEP), 2)


def _principle_section() -> html.Section:
    return html.Section(
        className="card step",
        children=[
            html.H2("Princip v kostce"),
            *[
                _principle_block(number, title, text, topic)
                for number, (title, text, topic) in enumerate(PRINCIPLE_BLOCKS, start=1)
            ],
            dcc.Link("Veškerá podrobná vysvětlení na stránce Teorie →", href=THEORY_PATH, className="back-link"),
        ],
    )


def _principle_block(number: int, title: str, text: str, topic: TheoryTopic) -> html.Div:
    return html.Div(
        className="principle-block",
        children=[
            html.H3(f"{number} · {title}"),
            dcc.Markdown(text, mathjax=True),
            details_link(topic.title, theory_href(topic.anchor)),
        ],
    )


def _portfolio_section() -> html.Section:
    return html.Section(
        className="card",
        children=[
            html.H2("Portfolio pro tuto stránku"),
            html.P(
                className="hint",
                children=[PORTFOLIO_HINT, dcc.Link("proč?", href=caveat_href(SIGN_PROBLEM.anchor))],
            ),
            labelled("Předvolba trhu", dcc.Dropdown(
                id=ids.GBS_MARKET_PRESET_DROPDOWN, options=PRESET_OPTIONS, placeholder="Vyber předvolbu…",
                clearable=False, searchable=False,
            )),
            html.P(PRESET_HINT, className="hint small"),
            html.P(id=ids.GBS_MARKET_PRESET_SUMMARY, className="hint small"),
            # The rows keep the hidden expected-return column of page 1; build_centered_portfolio ignores it.
            # No horizontal scrolling here: a scroll container would clip the asset-class dropdown menus.
            dash_table.DataTable(
                id=ids.GBS_ASSET_TABLE,
                data=DEFAULT_ASSET_ROWS,
                columns=[
                    {"id": NAME_COLUMN, "name": "Aktivum", "type": "text"},
                    ASSET_CLASS_COLUMN,
                    {"id": WEIGHT_COLUMN, "name": "Váha (%)", "type": "numeric"},
                    {"id": VOLATILITY_COLUMN, "name": "Roční volatilita (%)", "type": "numeric"},
                ],
                dropdown=ASSET_CLASS_DROPDOWN,
                editable=True,
                row_deletable=True,
                style_cell=TABLE_CELL_STYLE,
                style_cell_conditional=[{"if": {"column_id": NAME_COLUMN}, "textAlign": "left"}],
                style_header=TABLE_HEADER_STYLE,
            ),
            html.Div(
                className="table-footer",
                children=[
                    html.Button("+ Přidat aktivum", id=ids.GBS_ADD_ASSET_BUTTON, className="secondary-button"),
                    html.Span(id=ids.GBS_WEIGHT_SUM_TEXT),
                ],
            ),
            dcc.Dropdown(
                id=ids.GBS_PREDEFINED_ASSET_DROPDOWN, options=PREDEFINED_ASSET_OPTIONS,
                placeholder="+ Přidat aktivum z nabídky…", searchable=False, className="predefined-asset-picker",
            ),
            html.P(ASSET_TABLE_HINT, className="hint small"),
        ],
    )


def _correlation_section() -> html.Details:
    names = asset_names(DEFAULT_ASSET_ROWS)
    return html.Details(
        className="card",
        children=[
            html.Summary("Korelace mezi aktivy (jen nezáporné)"),
            labelled("Výchozí korelace mezi všemi páry", dcc.Slider(
                id=ids.GBS_PAIRWISE_CORRELATION_SLIDER, min=MIN_PAIRWISE_CORRELATION, max=MAX_PAIRWISE_CORRELATION,
                step=CORRELATION_STEP, value=DEFAULT_PAIRWISE_CORRELATION, marks={0: "0", 0.5: "0,5", 1: "1"},
                tooltip={"placement": "bottom", "always_visible": True},
            )),
            html.P(
                "Jednotlivé páry můžeš upravit v matici. Rozhodují hodnoty nad diagonálou.",
                className="hint",
            ),
            details_link(CORRELATION.title, theory_href(CORRELATION.anchor)),
            # Initial data lets the automatic first run read the correlations before the reset callback fills them.
            dash_table.DataTable(
                id=ids.GBS_CORRELATION_TABLE,
                data=default_correlation_rows(names, DEFAULT_PAIRWISE_CORRELATION),
                columns=correlation_table_columns(names),
                editable=True,
                style_cell=TABLE_CELL_STYLE,
                style_header=TABLE_HEADER_STYLE,
                style_table=SCROLLABLE_TABLE_STYLE,
            ),
        ],
    )


def _caveats_summary() -> html.Section:
    return html.Section(
        className="card",
        children=[
            html.H2("Kde jsou háčky"),
            html.Ol(
                className="caveat-list",
                children=[
                    html.Li([
                        html.Strong(caveat.title),
                        dcc.Markdown(caveat.summary, mathjax=True),
                        dcc.Link("Podrobněji →", href=caveat_href(caveat.anchor)),
                    ])
                    for caveat in CAVEATS
                ],
            ),
            dcc.Link("Všechny háčky podrobně na samostatné stránce →", href=CAVEATS_PATH, className="back-link"),
        ],
    )


def _controls() -> html.Section:
    return html.Section(
        className="card",
        children=[
            html.H2("Nastavení"),
            html.Div(
                className="control-grid",
                children=[
                    labelled("Odhadovaná veličina (L = roční výnos portfolia)", dcc.RadioItems(
                        id=ids.GBS_DEGREE_RADIO,
                        options=[{"label": DEGREE_LABELS[degree], "value": degree} for degree in ALLOWED_DEGREES],
                        value=DEFAULT_DEGREE,
                        className="radio-list",
                    )),
                    html.Div(children=[
                        labelled("Síla stlačení tanh(r_max) – vyšší = více fotonů", dcc.Slider(
                            id=ids.GBS_STRENGTH_SLIDER, min=MIN_SQUEEZING_STRENGTH, max=MAX_SQUEEZING_STRENGTH,
                            step=SQUEEZING_STEP, value=DEFAULT_SQUEEZING_STRENGTH,
                            marks={MIN_SQUEEZING_STRENGTH: "0,1", 0.5: "0,5", MAX_SQUEEZING_STRENGTH: "0,95"},
                            tooltip={"placement": "bottom", "always_visible": True},
                        )),
                        labelled("Maximální počet vzorků N", dcc.Dropdown(
                            id=ids.GBS_MAX_SHOTS_DROPDOWN,
                            options=[
                                {"label": f"{size:,}".replace(",", " "), "value": size} for size in SAMPLE_SIZE_OPTIONS
                            ],
                            value=DEFAULT_MAX_SAMPLE_SIZE, clearable=False, searchable=False,
                        )),
                    ]),
                    seed_dropdown(ids.GBS_SEED_DROPDOWN, default_value=REFERENCE_SEED),
                ],
            ),
            html.Button("Spustit GBS simulaci", id=ids.GBS_RUN_BUTTON, className="primary-button"),
        ],
    )
