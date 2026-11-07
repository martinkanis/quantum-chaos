import re
from typing import Dict, List

import plotly.graph_objects as go

from gbs import chip_hover_texts
from gbs.chip_charts import LightSource, chip_figure
from gbs.chip_programming import ChipTarget, build_setup, design_phases
from gbs.photonic_chip import light_flow, split_ratios

KIND_BY_TEMPLATE = {
    chip_hover_texts.INPUT_HOVER: "vstupy",
    chip_hover_texts.WAVEGUIDE_HOVER: "světlovody",
    chip_hover_texts.EXTERNAL_SHIFTER_HOVER: "posouvače φ",
    chip_hover_texts.INTERNAL_SHIFTER_HOVER: "posouvače θ",
    chip_hover_texts.COUPLER_HOVER: "děliče",
    chip_hover_texts.MZI_HOVER: "interferometry",
    chip_hover_texts.LASER_DETECTOR_HOVER: "detektory",
    chip_hover_texts.PHOTON_DETECTOR_HOVER: "detektory",
}
HIDDEN_TRACE_NAME = "<extra></extra>"


def hover_texts(figure: go.Figure) -> Dict[str, List[str]]:
    """What the browser shows on hover over each point, grouped by the kind of chip part."""
    texts: Dict[str, List[str]] = {}
    for trace in figure.data:
        template = trace.hovertemplate.replace(HIDDEN_TRACE_NAME, "")
        texts[KIND_BY_TEMPLATE[template]] = [
            re.sub(r"%\{customdata\[(\d)\]\}", lambda match: values[int(match[1])], template)
            for values in trace.customdata
        ]
    return texts


def chip_hovers(target: ChipTarget, spread: float, mode_count: int, inputs, source: LightSource):
    setup = build_setup(target, spread, 1, mode_count)
    phases = design_phases(setup)
    return setup, hover_texts(chip_figure(setup.chip, phases, light_flow(setup.chip, phases, inputs), source))


def test_kazda_soucastka_maleho_cipu_se_pri_najeti_mysi_popise():
    _, texts = chip_hovers(ChipTarget.SPREAD_EVENLY, 0.0, 4, (1,), LightSource.LASER)

    assert {kind: len(items) for kind, items in texts.items()} == {
        "vstupy": 4, "světlovody": 12, "posouvače φ": 6, "posouvače θ": 6, "děliče": 12, "interferometry": 6,
        "detektory": 4,
    }
    assert [text.endswith("Svítí sem laser.") for text in texts["vstupy"]] == [False, True, False, False]
    assert all(text.endswith("kolik světla dopadlo: 25,0 %.") for text in texts["detektory"])
    assert texts["děliče"][0].startswith("<b>1. dělič MZI 1</b>")
    assert all("pošle 50,0 % světla" in text for text in texts["děliče"])


def test_delic_vyrobeneho_cipu_ukaze_svuj_skutecny_pomer():
    setup, texts = chip_hovers(ChipTarget.RANDOM, 0.08, 4, (0,), LightSource.LASER)
    ratios = [f"{100 * ratio:.1f} %".replace(".", ",") for ratio in split_ratios(setup.chip).ravel()]

    assert [re.search(r"pošle (.*?) světla", text)[1] for text in texts["děliče"]] == ratios
    assert len(set(ratios)) > 1


def test_cip_s_osmi_svetlovody_popise_posouvace_i_bez_cisel_u_nich():
    setup, texts = chip_hovers(ChipTarget.RANDOM, 0.0, 8, (0,), LightSource.LASER)
    figure = chip_figure(setup.chip, design_phases(setup), light_flow(setup.chip, design_phases(setup), (0,)))
    annotations = [annotation.text for annotation in figure.layout.annotations]

    assert len(texts["posouvače φ"]) == len(texts["posouvače θ"]) == 28
    assert not any(text.startswith(("θ", "φ")) for text in annotations)


def test_velky_cip_s_fotony_popise_detektory_a_nema_nenakreslene_posouvace():
    _, texts = chip_hovers(ChipTarget.RANDOM, 0.0, 16, range(6), LightSource.PHOTONS)

    assert "posouvače φ" not in texts and "posouvače θ" not in texts
    assert len(texts["děliče"]) == 2 * len(texts["interferometry"]) == 240
    assert sum(text.endswith("Sem vstupuje jeden foton.") for text in texts["vstupy"]) == 6
    assert all("Průměrně sem dorazí" in text for text in texts["detektory"])
