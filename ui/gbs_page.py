from __future__ import annotations

from dash import dcc, html

from gbs.demo import MAX_SAMPLE_SIZE
from gbs.expectation import ALLOWED_DEGREES
from gbs.sampler import MAX_MODES
from ui import ids
from ui.components import REFERENCE_SEED, labelled, seed_dropdown
from ui.navigation import HIDDEN

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

CAVEATS_MARKDOWN = r"""
- **GBS je tady simulované klasicky.** Pro pár módů je to snadné. Kvantová výhoda může vzniknout jen
  tam, kde klasická simulace GBS selhává – a tahle hranice se posouvá (tensor-network simulace
  z roku 2024 dohnaly i velké experimenty).
- **Pro tento konkrétní moment existuje vzorec** $\mathbb{E}[L^d] = (d-1)!!\,(w^\top \Sigma w)^{d/2}$.
  Používá se tu jen jako kontrola správnosti. Smysl má GBS u obecných polynomů ve vysoké dimenzi,
  kde je výpočet hafniánů exponenciálně drahý.
- **Znaménkový problém.** Měří se $\mathrm{Haf}^2$, ne $\mathrm{Haf}$, takže tento estimátor funguje jen
  pro nezáporné korelace.
- **Většina výstřelů se zahodí.** Informaci nesou jen výstřely s přesně $d$ fotony. Síla stlačení je
  kompromis: slabé stlačení dá málo fotonů, silné je rozprostře do vyšších počtů.
- **Reálný hardware** má ztráty fotonů, šum a často jen prahové detektory (foton ano/ne). Výstupní
  rozdělení je pak jiné a estimátor se musí upravit.
- **VaR a CVaR nejsou polynomy.** Ukazatele s indikátorovou funkcí by se musely aproximovat polynomem
  vysokého stupně a počet potřebných vzorů roste kombinatoricky.
- **Srovnání je v počtu vzorků, ne v čase** – rychlost vzorkování hardwaru se tu nemodeluje.
"""

REFERENCES_MARKDOWN = """
- Hamilton et al.: *Gaussian Boson Sampling*, Phys. Rev. Lett. 119, 170501 (2017).
- Arrazola, Rebentrost, Weedbrook: *Quantum supremacy and high-dimensional integration*, arXiv (2017).
- Andersen, Shan: *Using Gaussian Boson Samplers to Approximate Gaussian Expectation Problems*, arXiv (2025).
- Oh et al.: *Classical algorithm for simulating experimental Gaussian boson sampling*, Nature Physics 20, 1461 (2024).

Estimátor na této stránce odhaduje hafniány přímo z četností vzorů. Jde o ilustraci principu;
konkrétní estimátory v uvedených pracích se mohou lišit.
"""


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
            html.Section(
                className="card",
                children=[html.H2("Kde jsou háčky"), dcc.Markdown(CAVEATS_MARKDOWN, mathjax=True)],
            ),
            html.Section(className="card", children=[html.H2("Literatura"), dcc.Markdown(REFERENCES_MARKDOWN)]),
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
