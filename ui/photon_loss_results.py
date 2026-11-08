"""Results of the photon loss lab: the estimate at the chosen transmission, both charts, the boundaries and the sweep."""

from __future__ import annotations

from typing import List, Optional, Tuple

from dash import dash_table, dcc, html

from gbs.loss_charts import bias_chart, samples_chart
from gbs.loss_study import LossPoint, LossStudy
from gbs.monomial_problem import required_samples
from ui.advantage_results import TARGET_RELATIVE_ERROR, format_count, format_number, named_monomial
from ui.components import SCROLLABLE_TABLE_STYLE, TABLE_CELL_STYLE, TABLE_HEADER_STYLE, metric_tile
from ui.photon_loss_content import advantage_label, loss_decibels, percent_label, signed_percent, times_label
from ui.random_matrix_content import czech_decimal

INFINITE = "∞"
UNRELIABLE_MARK = " (dolní odhad)"
"""Appended where the kept patterns do not reach far enough and p_η(n) is only a lower bound."""


def build_photon_loss_results(study: LossStudy, bench_transmission: Optional[float]) -> html.Div:
    return html.Div(
        className="results",
        children=[
            _summary_section(study),
            _samples_section(study, bench_transmission),
            _bias_section(study),
            _boundaries_section(study, bench_transmission),
            _sweep_section(study),
        ],
    )


def _summary_section(study: LossStudy) -> html.Section:
    point, comparison, problem = study.chosen, study.comparison, study.problem
    title = (
        f"Výsledek při propustnosti {percent_label(point.transmission)} "
        f"(ztráty {czech_decimal(loss_decibels(point.transmission), 1)} dB)"
    )
    return _section(title, [
        html.P(
            f"Monom {named_monomial(list(problem.variable_names), list(problem.exponents))} stupně {problem.degree}, "
            f"přesná hodnota E[xⁿ] = {format_number(comparison.exact)}.",
            className="hint",
        ),
        html.Div(className="metric-grid", children=[
            metric_tile(
                "Cílový vzor padá bez ztrát", f"1× za {format_count(1 / comparison.pattern_probability)} výstřelů",
                "p(n) ideálního přístroje.",
            ),
            metric_tile(
                "Cílový vzor padá se ztrátami",
                f"1× za {format_count(1 / point.lossy_probability)} výstřelů" + _reliability_mark(point),
                "p_η(n): součet přes všechny vzory, ze kterých ztráta udělá právě vzor n.",
            ),
            metric_tile(
                "Odhad bez opravy / přesná hodnota", czech_decimal(1 + point.naive_bias, 2),
                f"Vychýlení {signed_percent(point.naive_bias)}: systematická chyba, kterou žádný počet výstřelů nezmenší.",
            ),
            metric_tile(
                "Rozptyl 1 výstřelu s opravou / μ²", _variance_label(point),
                f"Bez ztrát {format_number(comparison.gbs_relative_variance)}, Monte Carlo "
                f"{format_number(comparison.mc_relative_variance)}. Méně je lépe.",
            ),
            metric_tile(*_samples_tile(study, point)),
            metric_tile(*_threshold_tile(study, point)),
        ]),
        dcc.Markdown(_verdict(study)),
        html.P(_truncation_note(study), className="hint small"),
    ])


def _samples_tile(study: LossStudy, point: LossPoint) -> Tuple[str, str, str]:
    if not point.correction_converged:
        return (
            "GBS-P s opravou potřebuje", f"{INFINITE} výstřelů",
            "Propustnost je pod kritickou hranicí: nestranná oprava má nekonečný rozptyl a žádný počet výstřelů nestačí.",
        )
    advantage = study.advantage(point)
    shots = format_count(required_samples(point.corrected_relative_variance, TARGET_RELATIVE_ERROR))
    scenarios = format_count(required_samples(study.comparison.mc_relative_variance, TARGET_RELATIVE_ERROR))
    detail = f"Pro relativní chybu 1 %: {shots} výstřelů GBS-P s opravou proti {scenarios} scénářům Monte Carla."
    if advantage >= 1:
        return "GBS-P s opravou potřebuje méně vzorků", times_label(advantage), detail
    return "Monte Carlo potřebuje méně vzorků", times_label(1 / advantage), detail


def _threshold_tile(study: LossStudy, point: LossPoint) -> Tuple[str, str, str]:
    if study.resolvable_by_threshold_detectors:
        return (
            "Prahové detektory: odhad / přesná hodnota", czech_decimal(1 + point.threshold_bias, 2),
            "Z četnosti kliků přesně v módech cílového vzoru, bez opravy ztrát.",
        )
    return (
        "Prahové detektory", "nerozliší vzor",
        f"Vzor má v některém módu dva a víc fotonů. Z četnosti kliků by vyšlo "
        f"{czech_decimal(1 + point.threshold_bias, 1)}× přesné hodnoty.",
    )


def _variance_label(point: LossPoint) -> str:
    return format_number(point.corrected_relative_variance) if point.correction_converged else INFINITE


def _verdict(study: LossStudy) -> str:
    point, comparison = study.chosen, study.comparison
    ideal_shots = format_count(required_samples(comparison.gbs_relative_variance, TARGET_RELATIVE_ERROR))
    scenarios = format_count(required_samples(comparison.mc_relative_variance, TARGET_RELATIVE_ERROR))
    opening = (
        f"Bez ztrát potřebuje GBS-P pro relativní chybu 1 % asi **{ideal_shots}** výstřelů proti **{scenarios}** "
        f"scénářům Monte Carla ({advantage_label(study, study.sweep[0])}). Při propustnosti "
        f"{percent_label(point.transmission)} dává odhad bez opravy **{czech_decimal(1 + point.naive_bias, 2)}× "
        f"přesné hodnoty**"
    )
    if not point.correction_converged:
        return (
            f"{opening} a nestranná oprava má **nekonečný rozptyl**: propustnost je pod kritickou hranicí "
            f"{percent_label(study.critical_transmission)}, takže ztráty tu odhad GBS-P ničí úplně."
        )
    shots = format_count(required_samples(point.corrected_relative_variance, TARGET_RELATIVE_ERROR))
    return (
        f"{opening}; s nestrannou opravou potřebuje GBS-P asi **{shots}** výstřelů, tedy "
        f"**{advantage_label(study, point)}** než Monte Carlo."
    )


def _truncation_note(study: LossStudy) -> str:
    point = study.chosen
    return (
        f"Součty jdou přes vzory s nejvýš {study.problem.degree + study.extra_photons} fotony "
        f"({study.extra_photons} nad stupeň úlohy). Odhad zanedbané části: u četnosti "
        f"{_share_label(point.probability_tail_share)}, u rozptylu opravy {_share_label(point.correction_tail_share)}; "
        f"hrubá horní mez z rozdělení počtu fotonů {percent_label(study.tail_probability, 1)}."
    )


def _share_label(share: float) -> str:
    if share == float("inf"):
        return "nelze odhadnout, vrstvy součtu neklesají"
    if share < 1e-4:
        return "pod 0,01 %"
    return percent_label(share, 2)


def _reliability_mark(point: LossPoint) -> str:
    return "" if point.probability_reliable else UNRELIABLE_MARK


def _samples_section(study: LossStudy, bench_transmission: Optional[float]) -> html.Section:
    return _section("Kolik vzorků je potřeba, když se ztrácejí fotony", [
        dcc.Graph(figure=samples_chart(study, TARGET_RELATIVE_ERROR, bench_transmission)),
        html.P(
            "Vodorovná čára: Monte Carlo ztráty netrápí. Fialová: GBS-P s nestrannou opravou ztrát – každých pár "
            "procent ztrát navíc zvedne počet výstřelů o řád. Šedé pásmo: pod kritickou propustností má oprava "
            "nekonečný rozptyl. Modrá tečkovaná čára vlevo: pod ní ztrátový přístroj klasicky simuluje algoritmus "
            "Qi a kol. (2020) s chybou 1 %. Oranžová čerchovaná: propustnost pracovního stolu simulátoru čipu "
            "s výchozími ztrátami a detektorem SNSPD. Kosočtverec: zvolená propustnost.",
            className="hint small",
        ),
    ])


def _bias_section(study: LossStudy) -> html.Section:
    return _section("Odhad bez opravy: o kolik se netrefí", [
        dcc.Graph(figure=bias_chart(study)),
        html.P(
            "Odhad dělený přesnou hodnotou na logaritmické ose. Detektory počítající fotony podceňují, protože ztráta "
            "odvede výstřely z cílového vzoru; prahové detektory (čárkovaně) přeceňují, protože do kliku spadnou "
            "i vzory s více fotony. Ani jedna chyba se s počtem výstřelů nezmenšuje. Křivka detektorů počítajících "
            "fotony končí tam, kam ještě sahá tabulka vzorů; pod tím je četnost jen dolní odhad (viz tabulka níže).",
            className="hint small",
        ),
    ])


def _boundaries_section(study: LossStudy, bench_transmission: Optional[float]) -> html.Section:
    point = study.chosen
    strongest = float(study.comparison.encoding.squeezing.max())
    tiles = [
        metric_tile(
            "Kritická propustnost η_c", percent_label(study.critical_transmission, 1),
            "tanh r_max / (1 + tanh r_max): pod ní má nestranná oprava nekonečný rozptyl (naše odvození).",
        ),
        metric_tile(
            "Klasická simulace podle Qi a kol.", percent_label(study.simulable_transmission, 1),
            "Pod touto propustností jde ztrátový přístroj simulovat klasicky s chybou 1 % (postačující podmínka).",
        ),
        metric_tile(
            "Nejsilnější stlačení r_max", czech_decimal(strongest, 2),
            "Parametr stlačení nejvíc stlačeného módu; rozhoduje o obou hranicích.",
        ),
    ]
    if bench_transmission is not None:
        tiles.append(metric_tile(
            "Pracovní stůl simulátoru čipu", percent_label(bench_transmission),
            "Výchozí ztráty vazby a světlovodů a účinnost SNSPD pro čip s tolika světlovody, kolik má úloha proměnných.",
        ))
    side = "nad" if point.transmission > study.critical_transmission else "pod"
    return _section("Hranice", [
        html.Div(className="metric-grid", children=tiles),
        html.P(
            f"Zvolená propustnost {percent_label(point.transmission)} leží {side} kritickou hranicí a hluboko nad "
            "hranicí klasické simulace: o použitelnosti odhadu tu rozhoduje jeho vlastní rozptyl, ne věty "
            "o simulovatelnosti.",
            className="hint",
        ),
    ])


def _sweep_section(study: LossStudy) -> html.Section:
    rows = [_sweep_row(study, point) for point in study.sweep]
    return _section("Celá řada propustností", [
        html.P(
            "Stejná čísla jako v grafech, pro každou propustnost řady. Nekonečno znamená, že nestranná oprava má "
            "nekonečný rozptyl.",
            className="hint",
        ),
        dash_table.DataTable(
            data=rows,
            columns=[
                {"id": "transmission", "name": "Propustnost η"},
                {"id": "loss", "name": "Ztráty (dB)"},
                {"id": "frequency", "name": "Vzor padá 1× za"},
                {"id": "naive", "name": "Odhad bez opravy / přesná"},
                {"id": "variance", "name": "Rozptyl s opravou / μ²"},
                {"id": "shots", "name": "Výstřelů pro chybu 1 %"},
                {"id": "advantage", "name": "Proti Monte Carlu"},
            ],
            style_cell=TABLE_CELL_STYLE,
            style_header=TABLE_HEADER_STYLE,
            style_table=SCROLLABLE_TABLE_STYLE,
        ),
    ])


def _sweep_row(study: LossStudy, point: LossPoint) -> dict:
    converged = point.correction_converged
    return {
        "transmission": percent_label(point.transmission, 1),
        "loss": czech_decimal(loss_decibels(point.transmission), 2),
        "frequency": format_count(1 / point.lossy_probability) + _reliability_mark(point),
        "naive": czech_decimal(1 + point.naive_bias, 3),
        "variance": _variance_label(point),
        "shots": format_count(required_samples(point.corrected_relative_variance, TARGET_RELATIVE_ERROR))
        if converged else INFINITE,
        "advantage": advantage_label(study, point),
    }


def _section(title: str, children: List) -> html.Section:
    return html.Section(className="card", children=[html.H2(title), *children])
