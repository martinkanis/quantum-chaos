import pytest
from dash import dcc, no_update

from gbs.advantage_lab import run_lab
from gbs.benchmark_problems import find_benchmark
from gbs.monomial_problem import MonomialProblemError
from gbs.photon_tuning import TuningMode
from gbs.qiskit_export import SCRIPT_FILE_NAME
from ui import ids
from ui.advantage_callbacks import apply_benchmark, download_qiskit_script, should_run_lab
from ui.advantage_form import (
    EXPONENT_COLUMN,
    build_monomial_problem,
    covariance_column_id,
    matrix_rows,
    resized_rows,
    symmetrized_rows,
)
from ui.advantage_page import build_advantage_page
from ui.advantage_results import build_advantage_results, format_count, format_number
from ui.guide_page import GUIDE_SOURCES_ANCHOR, GUIDE_TOPICS, build_guide_page
from ui.navigation import ADVANTAGE_PATH, GUIDE_PATH, PAGE_IDS, PORTFOLIO_PATH, VISIBLE, guide_href, show_page
from ui.theory_content import SOURCES_ANCHOR, TOPICS, all_sources


def visible_pages(pathname):
    styles = show_page(pathname)[: len(PAGE_IDS)]
    return [page_id for page_id, style in zip(PAGE_IDS, styles) if style == VISIBLE]


def links_in(component):
    if isinstance(component, dcc.Link):
        yield component.href
    children = getattr(component, "children", None)
    for child in children if isinstance(children, list) else [children]:
        if child is not None and not isinstance(child, str):
            yield from links_in(child)


def test_navigace_ukaze_stranku_vyhody_i_pruvodce():
    assert visible_pages(ADVANTAGE_PATH) == [ids.ADVANTAGE_PAGE]
    assert visible_pages(GUIDE_PATH) == [ids.GUIDE_PAGE]


def test_kazda_kapitola_pruvodce_ma_vlastni_kotvu_a_sekci():
    anchors = [topic.anchor for topic in GUIDE_TOPICS]
    page = build_guide_page()
    section_ids = [child.id for child in page.children if getattr(child, "id", None)]

    assert len(set(anchors)) == len(anchors)
    assert section_ids == anchors + [GUIDE_SOURCES_ANCHOR]
    assert not set(anchors + [GUIDE_SOURCES_ANCHOR]) & ({topic.anchor for topic in TOPICS} | {SOURCES_ANCHOR})


def test_kazda_kapitola_pruvodce_ma_shrnuti_vyklad_i_zdroje():
    for topic in GUIDE_TOPICS:
        assert topic.in_short.strip() and topic.explanation.strip() and topic.further_reading


def test_souhrnny_seznam_pruvodce_obsahuje_kazdy_zdroj_prave_jednou():
    sources = all_sources(GUIDE_TOPICS)

    assert len(sources) == len(set(sources))
    assert any(source.czech for source in sources)


def test_odkazy_ze_stranky_vyhody_vedou_na_existujici_kapitoly_pruvodce():
    anchors = {topic.anchor for topic in GUIDE_TOPICS}
    guide_links = [href for href in links_in(build_advantage_page()) if href.startswith(f"{GUIDE_PATH}#")]

    assert guide_links
    assert {href.split("#")[1] for href in guide_links} <= anchors
    assert guide_href("x") == f"{GUIDE_PATH}#x"


def test_tabulka_matice_prevede_ulohu_tam_i_zpet():
    benchmark = find_benchmark("historie-usa")

    rebuilt = build_monomial_problem(matrix_rows(benchmark.problem))

    assert rebuilt.exponents == benchmark.problem.exponents
    assert rebuilt.variable_names == benchmark.problem.variable_names
    assert (rebuilt.covariance == benchmark.problem.covariance).all()


def test_nova_promenna_zacina_nekorelovana_s_jednotkovym_rozptylem():
    rows = resized_rows(matrix_rows(find_benchmark("spolecny-extrem").problem), 3)

    assert [row[covariance_column_id(2)] for row in rows] == [0.0, 0.0, 1.0]
    assert rows[2][EXPONENT_COLUMN] == 2
    assert build_monomial_problem(resized_rows(rows, 1)).exponents == (8,)


def test_uprava_pod_diagonalou_se_zrcadli_nad_diagonalu():
    rows = matrix_rows(find_benchmark("spolecny-extrem").problem)
    edited = [dict(row) for row in rows]
    edited[1][covariance_column_id(0)] = 0.3

    symmetric = symmetrized_rows(edited, previous_rows=rows)

    assert symmetric[0][covariance_column_id(1)] == symmetric[1][covariance_column_id(0)] == 0.3
    assert symmetrized_rows(rows, previous_rows=rows) is None


def test_bez_predchozi_verze_rozhoduje_horni_trojuhelnik():
    rows = matrix_rows(find_benchmark("spolecny-extrem").problem)
    rows[1][covariance_column_id(0)] = 0.9

    assert symmetrized_rows(rows, previous_rows=None)[1][covariance_column_id(0)] == 0.5


@pytest.mark.parametrize(
    ("column", "value", "message"),
    [(covariance_column_id(1), None, "Vyplň všechny prvky"), (EXPONENT_COLUMN, 2.5, "celé číslo")],
)
def test_neuplna_tabulka_skonci_srozumitelnou_chybou(column, value, message):
    rows = matrix_rows(find_benchmark("spolecny-extrem").problem)
    rows[0][column] = value

    with pytest.raises(MonomialProblemError, match=message):
        build_monomial_problem(rows)


def test_vyber_pripravene_ulohy_naplni_tabulku_pocet_promennych_i_popis():
    rows, variable_count, description = apply_benchmark("historie-usa")

    assert variable_count == len(rows) == 3
    assert "1928–2023" in description
    assert apply_benchmark("neexistuje") == (no_update, no_update, no_update)


def test_laborator_bezi_po_kliknuti_nebo_pri_prvnim_zobrazeni_stranky():
    assert should_run_lab(ids.ADVANTAGE_RUN_BUTTON, PORTFOLIO_PATH, current_results=["hotovo"])
    assert should_run_lab(None, ADVANTAGE_PATH, current_results=None)
    assert not should_run_lab(ids.URL, ADVANTAGE_PATH, current_results=["hotovo"])
    assert not should_run_lab(None, PORTFOLIO_PATH, current_results=None)


@pytest.mark.parametrize("mode", list(TuningMode))
def test_vysledky_laboratore_se_vykresli(mode):
    run = run_lab(find_benchmark("historie-usa").problem, mode, max_sample_size=10_000, seed=42)

    results = build_advantage_results(run, emulation=None, emulation_error="Příliš velká úloha.")

    assert len(results.children) == 5


def test_stazeni_vrati_skript_pro_qiskit():
    rows = matrix_rows(find_benchmark("spolecny-extrem").problem)

    download, message = download_qiskit_script(1, rows, TuningMode.PER_MODE.value, 42)

    assert download["filename"] == SCRIPT_FILE_NAME
    assert "StatevectorSampler" in download["content"]
    assert SCRIPT_FILE_NAME in message


def test_stazeni_z_neplatne_tabulky_ukaze_chybu_misto_souboru():
    rows = matrix_rows(find_benchmark("spolecny-extrem").problem)
    rows[0][EXPONENT_COLUMN] = 7

    download, message = download_qiskit_script(1, rows, TuningMode.PER_MODE.value, 42)

    assert download is no_update
    assert "sudý" in message


def test_cisla_se_zobrazi_cesky_a_zaokrouhlene():
    assert format_number(174_352) == "174 352"
    assert format_number(10.34) == "10,34"
    assert format_number(4.28308e-12) == "4,283 · 10⁻¹²"
    assert format_count(248.6) == "250"
    assert format_count(72_148) == "72 000"
    assert format_count(7.46e9) == "7,5 · 10⁹"
