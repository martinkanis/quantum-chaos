from collections import Counter

from app import app
from ui import ids
from ui.callbacks import run_simulation
from ui.form_parsing import DEFAULT_ASSET_ROWS, asset_names, default_correlation_rows
from ui.navigation import HIDDEN, VISIBLE
from ui.portfolio_page import build_portfolio_page

NAMES = asset_names(DEFAULT_ASSET_ROWS)


def outputs_of(callback):
    return callback["output"] if isinstance(callback["output"], list) else [callback["output"]]


def component_ids_used_by(callback):
    dependencies = callback["inputs"] + callback["state"]
    return {output.component_id for output in outputs_of(callback)} | {dependency["id"] for dependency in dependencies}


def callback_writing(component_id):
    return next(
        callback for callback in app.callback_map.values()
        if any(output.component_id == component_id for output in outputs_of(callback))
    )


def download_button_style_after_run(initial_value):
    *_, download_button_style = run_simulation(
        1, DEFAULT_ASSET_ROWS, default_correlation_rows(NAMES, 0.2),
        initial_value=initial_value, monthly_contribution=0, years=1, simulation_count=100, seed=42,
    )
    return download_button_style


def test_callbacky_pouzivaji_jen_komponenty_z_vychoziho_layoutu():
    layout_ids = set(app.layout)

    for callback in app.callback_map.values():
        assert component_ids_used_by(callback) - layout_ids == set()


def test_tlacitko_stazeni_je_skryte_dokud_neni_co_stahnout():
    assert build_portfolio_page()[ids.DOWNLOAD_BUTTON].style == HIDDEN
    assert download_button_style_after_run(initial_value=1000) == VISIBLE
    assert download_button_style_after_run(initial_value=None) == HIDDEN


def test_id_komponent_jsou_v_celem_layoutu_unikatni():
    duplicate_ids = [component_id for component_id, count in Counter(app.layout).items() if count > 1]

    assert duplicate_ids == []


def test_gbs_stranka_pocita_s_vlastnim_portfoliem_ne_s_prvni_strankou():
    read_ids = {dependency["id"] for dependency in callback_writing(ids.GBS_RESULTS)["state"]}

    assert {ids.GBS_ASSET_TABLE, ids.GBS_CORRELATION_TABLE} <= read_ids
    assert not {ids.ASSET_TABLE, ids.CORRELATION_TABLE} & read_ids
