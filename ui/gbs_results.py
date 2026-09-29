from __future__ import annotations

from collections import Counter
from math import floor, log10, prod
from typing import List, Sequence

import numpy as np
from dash import dash_table, dcc, html

from gbs.charts import (
    circuit_diagram,
    convergence_chart,
    covariance_heatmap,
    interferometer_heatmap,
    pattern_frequency_chart,
    pattern_label,
    photon_total_chart,
    shot_stream_heatmap,
    trajectory_chart,
)
from gbs.demo import REPETITIONS, SHOT_PREVIEW_MAX_TOTAL, GbsDemoRun
from gbs.expectation import HafnianTerm, hafnian_terms
from gbs.hafnian import hafnian_expansion
from ui.components import SCROLLABLE_TABLE_STYLE, TABLE_CELL_STYLE, TABLE_HEADER_STYLE, details_link, metric_tile
from ui.navigation import theory_href
from ui.theory_content import (
    COMPARISON,
    ENCODING,
    ESTIMATOR,
    PORTFOLIO_MOMENT,
    SHOTS,
    WICK_THEOREM,
    TheoryTopic,
)

PERCENT = 100
HAFNIAN_TABLE_ROWS = 8
COMPARABLE_ERROR_RATIO = 1.2
TARGET_RELATIVE_ERROR = 0.01
SAMPLE_COUNT_SIGNIFICANT_DIGITS = 3
SUBSCRIPT_DIGITS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUPERSCRIPT_DIGITS = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
FORMULA_COLUMNS = ("monomial", "wick")

DEGREE_MEANING = {
    2: r"Pro $d = 2$ je to rozptyl – čtverec volatility portfolia.",
    4: (
        r"Čtvrtá mocnina zdůrazní velké výkyvy; poměr $\mathbb{E}[L^4]/\sigma_p^4$ je špičatost "
        "(pro normální rozdělení 3)."
    ),
    6: "Šestá mocnina je na extrémní roky citlivá ještě víc než čtvrtá.",
}


def build_gbs_results(run: GbsDemoRun, mode_labels: Sequence[str]) -> html.Div:
    return html.Div(
        className="results",
        children=[
            _problem_step(run, mode_labels),
            _hafnian_step(run),
            _encoding_step(run, mode_labels),
            _measurement_step(run, mode_labels),
            _frequency_step(run),
            _comparison_step(run),
        ],
    )


def hafnian_table(terms: Sequence[HafnianTerm], moment: float) -> dash_table.DataTable:
    rows = [
        {
            "pattern": pattern_label(term.pattern),
            "monomial": monomial_label(term.pattern),
            "wick": wick_formula(term.pattern),
            "coefficient": f"{term.coefficient:.4g}",
            "hafnian": _scientific(term.hafnian),
            "contribution": _scientific(term.contribution),
            "share": f"{term.contribution / moment * PERCENT:.1f} %",
        }
        for term in terms
    ]
    return dash_table.DataTable(
        data=rows,
        columns=[
            {"id": "pattern", "name": "Vzor n"},
            {"id": "monomial", "name": "Monom xⁿ"},
            {"id": "wick", "name": "E[xⁿ] podle Wicka"},
            {"id": "coefficient", "name": "Koeficient c_n"},
            {"id": "hafnian", "name": "Haf(Σ_n)"},
            {"id": "contribution", "name": "Příspěvek c_n·Haf"},
            {"id": "share", "name": "Podíl"},
        ],
        style_cell=TABLE_CELL_STYLE,
        style_cell_conditional=[{"if": {"column_id": column}, "textAlign": "left"} for column in FORMULA_COLUMNS],
        style_data={"whiteSpace": "normal", "height": "auto"},
        style_header=TABLE_HEADER_STYLE,
        style_table=SCROLLABLE_TABLE_STYLE,
    )


def monomial_label(pattern: Sequence[int]) -> str:
    """Pattern (2, 1, 0) is the monomial X₁²X₂."""
    return "".join(f"X{_subscript(asset + 1)}{_power(count)}" for asset, count in enumerate(pattern) if count)


def wick_formula(pattern: Sequence[int]) -> str:
    """E[xⁿ] as a sum over pairings, e.g. Σ₁₁Σ₂₂ + 2Σ₁₂² for pattern (2, 2)."""
    terms = []
    for product, multiplicity in hafnian_expansion(pattern).items():
        entries = "".join(
            f"Σ{_subscript(row + 1)}{_subscript(column + 1)}{_power(power)}"
            for (row, column), power in Counter(product).items()
        )
        terms.append(f"{multiplicity if multiplicity > 1 else ''}{entries}")
    return " + ".join(terms)


def _problem_step(run: GbsDemoRun, mode_labels: Sequence[str]) -> html.Section:
    problem = run.problem
    degree = problem.degree
    volatility = float(np.sqrt(problem.portfolio_variance))
    pairing_count = prod(range(degree - 1, 0, -2))
    moment_factor = str(pairing_count) if pairing_count > 1 else ""
    return _step(1, "Úloha: moment výnosu portfolia", [
        html.Div(className="two-columns", children=[
            html.Div([
                _markdown(rf"""
**Co počítáme.** $X_i$ je roční výnos aktiva $i$ **minus jeho očekávaný výnos** – jen „překvapení“, o kolik
se rok odchýlí od očekávání. Model předpokládá vícerozměrné normální rozdělení $X \sim \mathcal{{N}}(0, \Sigma)$,
kde $\Sigma_{{ij}} = \rho_{{ij}}\,\sigma_i\,\sigma_j$ skládá volatility $\sigma_i$ a korelace $\rho_{{ij}}$
z tabulky portfolia. Odchylka výnosu celého portfolia s vahami $w$ je

$$
L = w^\top X = w_1X_1 + \dots + w_kX_k .
$$

**Co hledáme.** Moment $\mathbb{{E}}[L^{degree}]$ – průměrnou {degree}. mocninu odchylky.
{DEGREE_MEANING[degree]} Liché momenty jsou u symetrického rozdělení nulové, proto se nepočítají.

**Kontrola.** $L$ je sama normální, takže přesně $\mathbb{{E}}[L^{degree}] = {moment_factor}\sigma_p^{degree}$,
kde $\sigma_p = \sqrt{{w^\top\Sigma w}}$ je volatilita portfolia. Další kroky se k tomuto číslu musí dopracovat
úplně jinou cestou – přes hafniány a fotony.
"""),
                html.Div(className="metric-grid", children=[
                    metric_tile(f"Přesná hodnota E[L{_power(degree)}]", _scientific(run.study.exact)),
                    metric_tile("Volatilita portfolia σ_p = √(wᵀΣw)", f"{volatility * PERCENT:.2f} %"),
                    metric_tile(
                        f"(E[L{_power(degree)}])^(1/{degree})", f"{run.study.exact ** (1 / degree) * PERCENT:.2f} %",
                        hint="Odmocnina momentu převede „výnos na d-tou“ zpět na procenta výnosu. "
                        "Pro d = 2 je to volatilita, vyšší momenty dají víc, protože zdůrazňují velké výkyvy.",
                    ),
                ]),
            ]),
            html.Div([
                html.H4("Kovarianční matice Σ"),
                dcc.Graph(figure=covariance_heatmap(problem.covariance, mode_labels)),
            ]),
        ]),
        _details_link(PORTFOLIO_MOMENT),
    ])


def _hafnian_step(run: GbsDemoRun) -> html.Section:
    degree = run.problem.degree
    terms = sorted(hafnian_terms(run.problem), key=lambda term: term.contribution, reverse=True)
    moment = sum(term.contribution for term in terms)
    shown_terms = terms[:HAFNIAN_TABLE_ROWS]
    return _step(2, "Wickova věta: moment = vážený součet hafniánů", [
        _markdown(rf"""
**Roznásobení.** Mocnina $(w^\top X)^{degree}$ se rozpadne na {_count_noun(len(terms), "monom", "monomy", "monomů")}
$c_n\,x^n$. Vzor
$n = (n_1, \dots, n_k)$ říká, kolikrát se v monomu $x^n = X_1^{{n_1}}\cdots X_k^{{n_k}}$ opakuje které aktivum,
a $c_n = \frac{{{degree}!}}{{n_1!\cdots n_k!}}\,w_1^{{n_1}}\cdots w_k^{{n_k}}$ je multinomický koeficient krát
váhy. Pro $k$ aktiv je vzorů $\binom{{{degree}+k-1}}{{k-1}}$.

**Wickova věta pro každý monom.** Střední hodnota monomu se spočítá rozdělením jeho {degree} činitelů do dvojic:
každou dvojici nahradí kovariance a součiny přes všechna rozdělení se sečtou. Například
$\mathbb{{E}}[X_1^2X_2^2] = \Sigma_{{11}}\Sigma_{{22}} + 2\Sigma_{{12}}^2$ – dvojice (1,1)(2,2) jednou
a (1,2)(1,2) dvakrát. Obecně je to hafnián matice $\Sigma_n$, která opakuje řádek i sloupec $i$ celkem
$n_i$-krát, a proto

$$
\mathbb{{E}}[L^{degree}] = \sum_{{|n| = {degree}}} c_n\,\mathrm{{Haf}}(\Sigma_n).
$$

Sloupec „E[xⁿ] podle Wicka“ ukazuje rozdělení do dvojic pro největší členy. Počet rozdělení roste jako
$1\cdot3\cdot5\cdots(d-1)$ a výpočet hafniánu je obecně #P-těžký.
"""),
        hafnian_table(shown_terms, moment),
        html.P(f"Zobrazeno {len(shown_terms)} největších z {len(terms)} členů.", className="hint small"),
        _details_link(WICK_THEOREM),
    ])


def _encoding_step(run: GbsDemoRun, mode_labels: Sequence[str]) -> html.Section:
    program = run.program
    squeezing_values = ", ".join(f"{squeezing:.2f}" for squeezing in program.squeezing)
    return _step(3, "Nahrání do GBS: stlačení a interferometr", [
        _markdown(rf"""
**Cíl.** Zařízení má mít matici $B = \gamma\Sigma$ – pak jeho pravděpodobnosti obsahují přesně hafniány
$\mathrm{{Haf}}(\Sigma_n)$ z kroku 2, jen vynásobené známým $\gamma^{{d/2}}$.

**Jak.** Kovarianční matice je symetrická a pozitivně semidefinitní, proto jde rozložit na vlastní čísla
a vlastní vektory: $\Sigma = V\,\mathrm{{diag}}(\lambda)\,V^\top$. Porovnání s
$B = U\,\mathrm{{diag}}(\tanh r)\,U^\top$ dá návod: **interferometr $U = V$** a **stlačení
$\tanh r_j = \gamma\lambda_j$**.

**Proč eigen-portfolia.** Vlastní vektory jsou hlavní komponenty portfolia – vzájemně nekorelované kombinace
aktiv, jejichž rozptyly jsou $\lambda_j$. Vstupní mód $j$ nese komponentu $j$: čím větší její rozptyl, tím
silnější stlačení a tím víc fotonových párů (v průměru $\sinh^2 r_j$ fotonů). Interferometr pak udělá se
světlem totéž co matice $V$ v rozkladu – poskládá z komponent zpět jednotlivá aktiva. Proto **každý výstupní
mód (detektor) odpovídá jednomu aktivu** a počet fotonů $n_i$ hraje roli mocniny $X_i$ v monomu.

**Proč $\gamma$.** Stlačení nemůže být nekonečné ($\tanh r < 1$), proto $\gamma = s/\lambda_{{\max}}$, kde
$s = \tanh r_{{\max}} = {np.tanh(program.squeezing.max()):.2f}$ je nastavená síla stlačení. Tady
$\gamma = {program.scale:.2f}$ a $r = ({squeezing_values})$.
"""),
        dcc.Graph(figure=circuit_diagram(program, mode_labels), config={"displayModeBar": False}),
        html.Div(className="two-columns", children=[
            html.Div([
                html.H4("Interferometr |U| (řádky = aktiva, sloupce = vstupní módy)"),
                dcc.Graph(figure=interferometer_heatmap(program, mode_labels)),
            ]),
            html.Div(className="metric-grid", children=[
                metric_tile("Škálování γ", f"{program.scale:.2f}"),
                metric_tile("Největší stlačení r_max", f"{program.squeezing.max():.2f}"),
                metric_tile(
                    "Střední počet fotonů n̄", f"{program.mean_photon_number:.2f}",
                    hint="Součet sinh²(r_j) přes všechny módy.",
                ),
            ]),
        ]),
        _details_link(ENCODING),
    ])


def _measurement_step(run: GbsDemoRun, mode_labels: Sequence[str]) -> html.Section:
    degree = run.problem.degree
    return _step(4, "Měření: výstřely a počty fotonů", [
        _markdown(rf"""
**Výstřel** je jedno spuštění obvodu: zdroje vyšlou pulz stlačeného světla, ten projde interferometrem a každý
detektor spočítá své fotony. Výsledkem je vzor $n$, třeba $(2, 0, 2)$.

**Proč jen sudé součty.** Stlačené vakuum vzniká nelineárním procesem, při kterém se foton čerpacího laseru
rozpadne na **dvojici** fotonů. Každý zdroj proto vyzáří 0, 2, 4, … fotonů, a to s pravděpodobností
$P(2m) = \frac{{(2m)!}}{{(2^m m!)^2}}\,\frac{{\tanh^{{2m}} r}}{{\cosh r}}$. Interferometr fotony jen
přerozděluje – žádné nevyrábí ani nepohlcuje – takže **celkový počet zůstane sudý**. Jednotlivé detektory
liché počty vidět mohou: pár se může rozdělit, třeba $(1, 0, 1)$.

**Proč jen {_photon_count(degree)} (✓).** Vzor se součtem $|n| = {degree}$ odpovídá monomu stupně {degree} –
jen takové hafniány vystupují v součtu z kroku 2. Výstřely s jiným počtem fotonů nesou informaci o jiných
hafniánech, a proto je estimátor zahodí. Jejich podíl řídí jen stlačení, interferometr celkový počet nemění:
přesně {_photon_count(degree)} má tady **{run.study.useful_shot_fraction * PERCENT:.1f} %** výstřelů. Střední
počet fotonů je
$\bar n = \sum_j \sinh^2 r_j = {run.program.mean_photon_number:.2f}$.
"""),
        html.Div(className="two-columns", children=[
            html.Div([
                html.H4(f"Prvních {len(run.shots)} výstřelů"),
                dcc.Graph(figure=shot_stream_heatmap(run.shots, degree, mode_labels, SHOT_PREVIEW_MAX_TOTAL)),
            ]),
            html.Div([
                html.H4("Rozdělení celkového počtu fotonů"),
                dcc.Graph(figure=photon_total_chart(run.total_photon_probabilities, degree)),
            ]),
        ]),
        _details_link(SHOTS),
    ])


def _frequency_step(run: GbsDemoRun) -> html.Section:
    return _step(5, "Z četností zpět k hafniánům", [
        _markdown(r"""
Ze vzorce pro pravděpodobnost vzoru jde hafnián vyjádřit. Platí
$p(n) = \frac{\mathrm{Haf}(B_n)^2}{n!\,\prod_j\cosh r_j}$ a $\mathrm{Haf}(B_n) = \gamma^{d/2}\,\mathrm{Haf}(\Sigma_n)$,
takže

$$
\mathrm{Haf}(\Sigma_n) = \gamma^{-d/2}\sqrt{p(n)\; n!\;\textstyle\prod_j \cosh r_j}.
$$

Neznámou pravděpodobnost nahradí **relativní četnost** $\hat p(n) = N_n/N$ – kolikrát ze všech $N$ výstřelů
padl vzor $n$ – a dosazením do součtu z kroku 2 vznikne odhad momentu. Graf porovnává četnosti s přesnými
pravděpodobnostmi: relativně se liší zhruba o $1/\sqrt{N_n}$ a odmocnina tuto chybu v odhadu hafniánu ještě
půlí. Vzory, které padají zřídka, jsou proto odhadnuté nejhůř.
"""),
        dcc.Graph(figure=pattern_frequency_chart(run.study)),
        _details_link(ESTIMATOR),
    ])


def _comparison_step(run: GbsDemoRun) -> html.Section:
    study = run.study
    degree = run.problem.degree
    sample_count = study.sample_sizes[-1]
    sample_size = _format_count(sample_count)
    gbs_error, mc_error = study.gbs_relative_rmse[-1], study.mc_relative_rmse[-1]
    gbs_constant, mc_constant = study.gbs_error_constant, study.mc_error_constant
    return _step(6, "Srovnání s klasickým Monte Carlem", [
        _markdown(rf"""
**Jak se srovnává.** Obě metody dostanou stejný rozpočet $N$: klasické MC $N$ náhodných scénářů, GBS $N$
výstřelů – včetně těch, které zahodí. Celý odhad se zopakuje {REPETITIONS}× s jinými náhodnými čísly.
**Relativní RMSE** je typická odchylka odhadu od přesné hodnoty v procentech: odmocnina z průměru čtverců
odchylek, vydělená přesnou hodnotou.

**Co předpovídá teorie.** Chyba obou metod klesá jako $c/\sqrt{{N}}$ – čtyřnásobek vzorků chybu jen
půlí. O vítězi rozhoduje konstanta $c$:

- **klasické MC:** $c_{{\mathrm{{MC}}}} = {mc_constant:.2f}$. U gaussovského portfolia závisí jen na stupni
  momentu: $L^{degree}$ má těžký chvost a vzácné extrémní scénáře průměr rozkolísají.
- **GBS:** $c_{{\mathrm{{GBS}}}} = {gbs_constant:.2f}$. Odmocnina v odhadu chybu půlí, ale zahozené výstřely
  a vzory, které nesou velký podíl momentu a přitom padají zřídka, ji zvětšují.

Pro relativní chybu {TARGET_RELATIVE_ERROR * PERCENT:.0f} % tak MC potřebuje asi
**{_format_count(_samples_for(mc_constant))}** scénářů a GBS asi **{_format_count(_samples_for(gbs_constant))}**
výstřelů. {_theory_verdict(gbs_constant, mc_constant)}

**Co naměřila simulace.** {_measured_verdict(gbs_error, mc_error, sample_size)} Chyba odhadnutá
z {REPETITIONS} opakování je sama náhodná (zhruba ±{_rmse_noise_percent():.0f} %); přerušované čáry v grafu
ukazují teoretické $c/\sqrt{{N}}$.
"""),
        html.H4(f"Naměřeno ({REPETITIONS} opakování, N = {sample_size})"),
        html.Div(className="metric-grid", children=[
            metric_tile("GBS odhad", _scientific(study.gbs_trajectory[-1])),
            metric_tile("MC odhad", _scientific(study.mc_trajectory[-1])),
            metric_tile("Relativní chyba GBS", f"{gbs_error * PERCENT:.2f} %"),
            metric_tile("Relativní chyba MC", f"{mc_error * PERCENT:.2f} %"),
        ]),
        html.H4(f"Teorie pro velké N (chyba ≈ c/√N, N = {sample_size})"),
        html.Div(className="metric-grid", children=[
            metric_tile("Teoretická chyba GBS", f"{gbs_constant / np.sqrt(sample_count) * PERCENT:.2f} %"),
            metric_tile("Teoretická chyba MC", f"{mc_constant / np.sqrt(sample_count) * PERCENT:.2f} %"),
            metric_tile(
                f"Výstřelů GBS pro chybu {TARGET_RELATIVE_ERROR * PERCENT:.0f} %",
                _format_count(_samples_for(gbs_constant)),
            ),
            metric_tile(
                f"Scénářů MC pro chybu {TARGET_RELATIVE_ERROR * PERCENT:.0f} %",
                _format_count(_samples_for(mc_constant)),
            ),
        ]),
        html.Div(className="two-columns", children=[
            dcc.Graph(figure=convergence_chart(study)),
            dcc.Graph(figure=trajectory_chart(study)),
        ]),
        _details_link(COMPARISON),
    ])


def _measured_verdict(gbs_error: float, mc_error: float, sample_size: str) -> str:
    if _is_comparable(gbs_error, mc_error):
        return f"Při N = {sample_size} mají **obě metody srovnatelnou chybu**."
    if gbs_error < mc_error:
        return f"Při N = {sample_size} má **GBS estimátor {mc_error / gbs_error:.1f}× menší chybu** než klasické MC."
    return f"Při N = {sample_size} má **klasické MC {gbs_error / mc_error:.1f}× menší chybu** než GBS estimátor."


def _theory_verdict(gbs_constant: float, mc_constant: float) -> str:
    """Error ∝ c/√N, so the ratio of required samples is the squared ratio of the constants."""
    if _is_comparable(gbs_constant, mc_constant):
        return "Teoreticky jsou tedy obě metody zhruba stejně dobré."
    sample_ratio = (gbs_constant / mc_constant) ** 2
    if sample_ratio < 1:
        return f"GBS tedy potřebuje zhruba **{1 / sample_ratio:.1f}× méně** vzorků."
    return f"GBS tedy potřebuje zhruba **{sample_ratio:.1f}× víc** vzorků."


def _is_comparable(first: float, second: float) -> bool:
    return max(first, second) / min(first, second) < COMPARABLE_ERROR_RATIO


def _samples_for(error_constant: float) -> int:
    """Error ≈ c/√N reaches the target at N = (c / target)², rounded because the constant is approximate."""
    samples = (error_constant / TARGET_RELATIVE_ERROR) ** 2
    rounding_digits = SAMPLE_COUNT_SIGNIFICANT_DIGITS - 1 - floor(log10(samples))
    return int(round(samples, rounding_digits))


def _rmse_noise_percent() -> float:
    """Relative standard error of an RMSE estimated from R repetitions is roughly 1/√(2R)."""
    return PERCENT / np.sqrt(2 * REPETITIONS)


def _details_link(topic: TheoryTopic) -> dcc.Link:
    return details_link(topic.title, theory_href(topic.anchor))


def _step(number: int, title: str, children: List) -> html.Section:
    return html.Section(
        className="card step",
        children=[html.H2([html.Span(str(number), className="step-number"), title])] + children,
    )


def _markdown(text: str) -> dcc.Markdown:
    return dcc.Markdown(text, mathjax=True)


def _subscript(number: int) -> str:
    return str(number).translate(SUBSCRIPT_DIGITS)


def _power(exponent: int) -> str:
    return str(exponent).translate(SUPERSCRIPT_DIGITS) if exponent > 1 else ""


def _photon_count(count: int) -> str:
    return _count_noun(count, "foton", "fotony", "fotonů")


def _count_noun(count: int, one: str, two_to_four: str, other: str) -> str:
    """Czech plural in the nominative/accusative: 1 foton, 2–4 fotony, 0 and 5+ fotonů."""
    if count == 1:
        return f"{count} {one}"
    if 2 <= count <= 4:
        return f"{count} {two_to_four}"
    return f"{count} {other}"


def _format_count(count: int) -> str:
    return f"{count:,}".replace(",", " ")


def _scientific(value: float) -> str:
    return f"{value:.4e}"
