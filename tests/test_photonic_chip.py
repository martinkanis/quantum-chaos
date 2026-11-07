import numpy as np
import pytest

from gbs.boson_sampling import random_unitary
from gbs.chip_programming import (
    ChipTarget,
    build_setup,
    calibrated_phases,
    design_phases,
    read_out,
    target_unitary,
)
from gbs.clements import clements_decomposition
from gbs.photonic_chip import (
    ChipError,
    MeshPhases,
    MziSlot,
    coupler_matrix,
    ideal_chip,
    light_flow,
    mesh_slots,
    mzi_count,
    mzi_matrix,
    pattern_match,
    split_ratios,
    transfer_matrix,
    transmission,
    zero_phases,
)


def cross_share(internal):
    """Share of the light from the upper input that ends in the lower output."""
    return abs(mzi_matrix(internal, 0.0)[1, 0]) ** 2


def test_theta_rozhoduje_jak_mzi_deli_svetlo_od_krize_po_rovny_stav():
    assert cross_share(0.0) == pytest.approx(1.0)
    assert cross_share(np.pi / 2) == pytest.approx(0.5)
    assert cross_share(np.pi) == pytest.approx(0.0, abs=1e-15)


def test_matice_mzi_odpovida_vzorci_z_vykladu_i_delici_ze_skript():
    theta, phi = 1.1, 0.7
    half = theta / 2
    expected = 1j * np.exp(1j * half) * np.array([
        [np.exp(1j * phi) * np.sin(half), np.cos(half)],
        [np.exp(1j * phi) * np.cos(half), -np.sin(half)],
    ])

    assert np.allclose(mzi_matrix(theta, phi), expected)
    assert abs(expected[0, 0]) ** 2 == pytest.approx(np.cos((np.pi - theta) / 2) ** 2)


def test_clementsova_sit_pro_ctyri_svetlovody_ma_sest_mzi_ve_ctyrech_sloupcich():
    assert mesh_slots(4) == (
        MziSlot(0, 0), MziSlot(0, 2), MziSlot(1, 1), MziSlot(2, 0), MziSlot(2, 2), MziSlot(3, 1),
    )
    assert all(len(mesh_slots(modes)) == mzi_count(modes) == modes * (modes - 1) // 2 for modes in range(2, 9))


@pytest.mark.parametrize("modes", range(2, 8))
def test_clementsuv_rozklad_slozi_libovolnou_unitarni_matici(modes):
    rng = np.random.default_rng(modes)
    for _ in range(10):
        unitary = random_unitary(modes, rng)
        decomposition = clements_decomposition(unitary)
        rebuilt = np.diag(decomposition.output_phases) @ transfer_matrix(ideal_chip(modes), decomposition.phases)

        assert np.allclose(rebuilt, unitary, atol=1e-9)
        assert np.allclose(np.abs(decomposition.output_phases), 1)


@pytest.mark.parametrize("target", list(ChipTarget))
def test_kazdy_cil_je_unitarni_a_na_idealnim_cipu_ho_navrh_trefi_presne(target):
    setup = build_setup(target, split_spread=0.0, seed=1)

    assert np.allclose(setup.target.conj().T @ setup.target, np.eye(4))
    assert read_out(setup, design_phases(setup), input_mode=0).match == pytest.approx(1.0)


def test_rozklad_odmitne_matici_ktera_neni_unitarni():
    with pytest.raises(ChipError, match="unitární"):
        clements_decomposition(np.ones((3, 3)))
    with pytest.raises(ChipError, match="čtvercová"):
        clements_decomposition(np.ones((2, 3)))


def test_svetlo_se_v_siti_neztraci_a_detektory_vidi_sloupec_mapy_prenosu():
    chip = build_setup(ChipTarget.RANDOM, split_spread=0.08, seed=2).chip
    phases = MeshPhases(tuple(np.linspace(0.3, 2.9, 6)), tuple(np.linspace(1.0, 5.0, 6)))
    flow = light_flow(chip, phases, input_modes=(2,))

    assert all(sum(column) == pytest.approx(1.0) for column in flow.columns)
    assert all(sum(mzi.entering) == pytest.approx(sum(mzi.leaving)) for mzi in flow.mzis)
    assert all(sum(mzi.inside) == pytest.approx(sum(mzi.entering)) for mzi in flow.mzis)
    assert np.allclose(flow.detected, transmission(transfer_matrix(chip, phases))[:, 2])


def test_nulove_faze_obraceji_poradi_svetlovodu():
    chip_transmission = transmission(transfer_matrix(ideal_chip(4), zero_phases(4)))

    assert np.allclose(chip_transmission, np.eye(4)[::-1])
    assert pattern_match(chip_transmission, np.full((4, 4), 0.25)) == pytest.approx(0.25)


def test_shoda_je_podil_svetla_ktery_dopadne_kam_ma():
    swapped_first_two = np.eye(4)[[1, 0, 2, 3]]

    assert pattern_match(np.eye(4), np.eye(4)) == 1.0
    assert pattern_match(swapped_first_two, np.eye(4)) == pytest.approx(0.5)


def test_vyrobeny_cip_je_podle_seedu_stejny_a_bez_rozptylu_idealni():
    first = build_setup(ChipTarget.RANDOM, split_spread=0.03, seed=4)
    again = build_setup(ChipTarget.RANDOM, split_spread=0.03, seed=4)
    other = build_setup(ChipTarget.RANDOM, split_spread=0.03, seed=5)

    assert first.chip == again.chip and np.array_equal(first.target, again.target)
    assert first.chip != other.chip
    assert np.allclose(split_ratios(build_setup(ChipTarget.RANDOM, 0.0, 4).chip), 0.5)
    assert np.all(np.abs(split_ratios(first.chip) - 0.5) < 0.15)


def test_dva_delice_jsou_bloky_50_50():
    splitters = target_unitary(ChipTarget.TWO_SPLITTERS, 4, np.random.default_rng(0))

    assert np.allclose(transmission(splitters), np.kron(np.eye(2), np.full((2, 2), 0.5)))
    assert np.allclose(splitters[:2, :2], coupler_matrix(np.pi / 4))


@pytest.mark.parametrize("target", [ChipTarget.RANDOM, ChipTarget.SPREAD_EVENLY, ChipTarget.TWO_SPLITTERS])
def test_doladeni_vrati_shodu_kterou_vyrobni_chyby_vzaly(target):
    for seed in (1, 2, 3):
        setup = build_setup(target, split_spread=0.03, seed=seed)
        designed = read_out(setup, design_phases(setup), 0).match
        calibrated = read_out(setup, calibrated_phases(setup), 0).match

        assert designed < 0.995
        assert calibrated > 0.999


def test_obraceni_doladit_nejde_ale_pruchod_ano():
    for seed in (1, 2, 3):
        reverse = build_setup(ChipTarget.REVERSE, split_spread=0.03, seed=seed)
        through = build_setup(ChipTarget.PASS_THROUGH, split_spread=0.03, seed=seed)

        reverse_gain = read_out(reverse, calibrated_phases(reverse), 0).match - read_out(
            reverse, design_phases(reverse), 0).match
        through_gain = read_out(through, calibrated_phases(through), 0).match - read_out(
            through, design_phases(through), 0).match

        assert 0 <= reverse_gain < 0.001
        assert through_gain > 0.001


def test_kriz_s_nepresnymi_delici_propousti_cos2_souctu_uhlu():
    angle = np.arcsin(np.sqrt(0.53))
    stays = [abs(mzi_matrix(theta, 0.0, (angle, angle))[0, 0]) ** 2 for theta in np.linspace(0, 2 * np.pi, 2001)]

    assert min(stays) == pytest.approx(np.cos(2 * angle) ** 2)
    assert min(stays) == pytest.approx((1 - 2 * 0.53) ** 2)
    assert round(100 * min(stays), 2) == 0.36


def test_neplatny_cip_faze_nebo_vstup_maji_ceskou_hlasku():
    chip = ideal_chip(4)

    with pytest.raises(ChipError, match="vstupů 1 až 4"):
        light_flow(chip, zero_phases(4), input_modes=(4,))
    with pytest.raises(ChipError, match="jen jednou"):
        light_flow(chip, zero_phases(4), input_modes=(1, 1))
    with pytest.raises(ChipError, match="6 interferometrů"):
        transfer_matrix(chip, zero_phases(3))
    with pytest.raises(ChipError, match="obě fáze"):
        MeshPhases((0.0, 1.0), (0.0,))
    with pytest.raises(ChipError, match="konečná"):
        MeshPhases((float("nan"),), (0.0,))
    with pytest.raises(ChipError, match="Rozptyl"):
        build_setup(ChipTarget.RANDOM, split_spread=0.5, seed=1)
    with pytest.raises(ChipError, match="nezáporné"):
        build_setup(ChipTarget.RANDOM, split_spread=0.0, seed=-1)
