from __future__ import annotations

from dash import dcc, html

from gbs.demo import MAX_SAMPLE_SIZE
from gbs.expectation import ALLOWED_DEGREES
from gbs.sampler import MAX_MODES
from ui import ids
from ui.caveats_content import CAVEATS, REFERENCES_MARKDOWN
from ui.components import REFERENCE_SEED, labelled, seed_dropdown
from ui.navigation import CAVEATS_PATH, HIDDEN, caveat_href

DEFAULT_DEGREE = 4
DEFAULT_SQUEEZING_STRENGTH = 0.7
MIN_SQUEEZING_STRENGTH = 0.1
MAX_SQUEEZING_STRENGTH = 0.95
SQUEEZING_STEP = 0.05
DEFAULT_MAX_SAMPLE_SIZE = 100_000
SAMPLE_SIZE_OPTIONS = (10_000, DEFAULT_MAX_SAMPLE_SIZE, MAX_SAMPLE_SIZE)

DEGREE_LABELS = {
    2: "E[L²] – rozptyl výnosu portfolia",
    4: "E[L⁴] – 4. moment (citlivost na tlusté chvosty)",
    6: "E[L⁶] – 6. moment (extrémní pohyby)",
}

PRINCIPLE_MARKDOWN = r"""
**Myšlenka.** Klasické Monte Carlo odhaduje očekávanou hodnotu průměrem přes náhodné scénáře.
Pro gaussovské výnosy $X \sim \mathcal{N}(0, \Sigma)$ a polynomiální funkci lze očekávanou hodnotu
přepsat na vážený součet **hafniánů** kovarianční matice (Wickova–Isserlisova věta):

$$\mathbb{E}\left[L^d\right] = \sum_{|n| = d} c_n \, \mathrm{Haf}(\Sigma_n), \qquad L = w^\top X$$

Gaussian Boson Sampler (GBS) je fotonické zařízení, jehož výstupní pravděpodobnosti jsou
**druhé mocniny hafniánů**:

$$p(n) = \frac{\mathrm{Haf}(B_n)^2}{n!\,\prod_j \cosh r_j}, \qquad B = \gamma\,\Sigma = U\,\mathrm{diag}(\tanh r)\,U^\top$$

Když do zařízení „nahrajeme“ $\Sigma$, četnosti naměřených vzorů fotonů prozradí hafniány a z nich
odhad $\mathbb{E}[L^d]$ – místo generování scénářů se počítají fotony.
"""

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
            html.Section(className="card", children=dcc.Markdown(PRINCIPLE_MARKDOWN, mathjax=True)),
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
                ],
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
            html.P(
                f"Portfolio (váhy, volatility a korelace) se přebírá z 1. stránky. Simulace zvládne "
                f"nejvýše {MAX_MODES} aktiv a jen nezáporné korelace.",
                className="hint",
            ),
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
