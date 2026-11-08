"""What the detectors on the bench register: shares of the laser light, click probabilities of single photons and the
clicks counted from a run of photons."""

from __future__ import annotations

from typing import Optional

import numpy as np
from dash import dcc, html

from gbs.bench import Bench, LightSource, PhotonCounts, bench_transmission, chip_length_cm, loss_db, registered_shares
from gbs.bench_charts import counts_chart
from gbs.chip_parts import czech_percent
from ui.chip_bench_content import COUNTS_HINT, DETECTOR_LABELS, LASER_READOUT_HINT, PHOTON_READOUT_HINT
from ui.chip_sampling_results import czech_count

SOURCE_OFF_TEXT = "Zdroj je vypnutý, detektory nic nezaznamenají."
MILLIMETRES_PER_CM = 10


def build_bench_readout(bench: Bench, chip_shares: Optional[np.ndarray], mode_count: int) -> html.Div:
    """chip_shares are the |U_ij|² of the input the source shines into, None while the source is off."""
    if chip_shares is None:
        return html.Div(html.P(SOURCE_OFF_TEXT, className="hint"))
    registered = registered_shares(chip_shares, bench.losses, bench.detector, mode_count)
    if bench.source == LightSource.LASER:
        return html.Div(children=[
            html.P(_bench_summary(bench, mode_count)),
            _detector_table(chip_shares, registered, "Změří fotodioda"),
            html.P(LASER_READOUT_HINT, className="hint small"),
        ])
    dark = bench.detector.dark_click_probability
    clicks = registered + (1 - registered) * dark
    silence = (1 - float(np.sum(registered))) * (1 - dark) ** len(registered)
    return html.Div(children=[
        html.P(_bench_summary(bench, mode_count)),
        _detector_table(chip_shares, clicks, "Cvaknutí na jeden foton"),
        html.P(f"Žádný detektor necvakne s pravděpodobností {czech_percent(silence)}: foton se ztratí na stole nebo "
               "ho detektor mine."),
        html.P(PHOTON_READOUT_HINT, className="hint small"),
    ])


def build_photon_counts(counts: PhotonCounts) -> html.Div:
    clicked = counts.shots - counts.silent_shots
    return html.Div(children=[
        html.P(
            f"Vystřeleno {czech_count(counts.shots)} fotonů: aspoň jeden detektor cvakl {czech_count(clicked)}krát, "
            f"{czech_count(counts.silent_shots)}krát necvakl žádný."
        ),
        dcc.Graph(figure=counts_chart(counts), config={"displayModeBar": False}),
        html.P(COUNTS_HINT, className="hint small"),
    ])


def _bench_summary(bench: Bench, mode_count: int) -> str:
    losses = bench.losses
    length_mm = chip_length_cm(mode_count) * MILLIMETRES_PER_CM
    total_db = _czech_decibels(loss_db(losses, mode_count))
    return (
        f"Stůl propustí {czech_percent(bench_transmission(losses, mode_count))} světla: ztráta {total_db} dB "
        f"(2 × {_czech_decibels(losses.coupling_db)} dB na přechodech vlákno–čip a "
        f"{_czech_decibels(losses.waveguide_db_per_cm)} dB/cm na {length_mm:.0f} mm světlovodů). "
        f"Detektor {DETECTOR_LABELS[bench.detector_kind][0]} má účinnost {czech_percent(bench.detector.efficiency)}."
    )


def _detector_table(chip_shares: np.ndarray, registered: np.ndarray, registered_title: str) -> html.Table:
    header = html.Tr([html.Th("detektor"), html.Th("na výstupu čipu"), html.Th(registered_title)])
    rows = [
        html.Tr([html.Th(str(index + 1)), html.Td(czech_percent(float(share))), html.Td(czech_percent(float(value)))])
        for index, (share, value) in enumerate(zip(chip_shares, registered))
    ]
    return html.Table(className="chip-matrix chip-bench-table", children=[html.Thead(header), html.Tbody(rows)])


def _czech_decibels(value: float) -> str:
    return f"{value:.1f}".replace(".", ",")
