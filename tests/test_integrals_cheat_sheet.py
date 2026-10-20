from math import exp, pi, sqrt

import numpy as np
import pytest

from ui import ids
from ui.integrals_cheat_sheet_content import (
    GAUSSIAN_TOPIC,
    MONTE_CARLO_STANDARD_ERROR,
    MONTE_CARLO_TOPIC,
    SOURCES_ANCHOR,
    TOPICS,
)
from ui.integrals_cheat_sheet_page import RELATED_PAGES, build_integrals_cheat_sheet_page
from ui.navigation import (
    ACTIVE_LINK_CLASS,
    INTEGRALS_CHEAT_SHEET_PATH,
    NAV_LINK_IDS,
    PAGE_BY_PATH,
    PAGE_IDS,
    show_page,
)
from ui.theory_content import all_sources
from ui.topic_catalog import CHEAT_SHEETS_TOPIC, RESEARCH_TOPICS, breadcrumb_trail

DERIVATIVE_STEP = 1e-6
SAMPLE_POINTS = np.array([0.3, 0.7, 1.3, 2.1])


def derivative(function, points):
    return (function(points + DERIVATIVE_STEP) - function(points - DERIVATIVE_STEP)) / (2 * DERIVATIVE_STEP)


def integrate(function, lower, upper, points=2_000_001):
    grid = np.linspace(lower, upper, points)
    return np.trapezoid(function(grid), grid)


def test_tahak_je_vlastnim_tematem_s_odkazem_v_horni_liste():
    link_classes = show_page(INTEGRALS_CHEAT_SHEET_PATH)[len(PAGE_IDS):len(PAGE_IDS) + len(NAV_LINK_IDS)]
    active = [link_id for link_id, link_class in zip(NAV_LINK_IDS, link_classes) if link_class == ACTIVE_LINK_CLASS]

    assert PAGE_BY_PATH[INTEGRALS_CHEAT_SHEET_PATH] == ids.INTEGRALS_CHEAT_SHEET_PAGE
    assert active == [ids.NAV_CHEAT_SHEETS_LINK]
    assert CHEAT_SHEETS_TOPIC in RESEARCH_TOPICS
    assert [label for label, _ in breadcrumb_trail(ids.INTEGRALS_CHEAT_SHEET_PAGE)] == [
        "Témata", "Matematické taháky", "Tahák: integrály",
    ]


def test_kapitoly_maji_unikatni_kotvy_a_kazdy_zdroj_odkaz():
    anchors = [topic.anchor for topic in TOPICS]
    page = build_integrals_cheat_sheet_page()
    section_ids = [child.id for child in page.children if getattr(child, "id", None)]
    sources = all_sources(TOPICS)

    assert section_ids == anchors + [SOURCES_ANCHOR]
    assert all(anchor.startswith("tahak-") for anchor in section_ids)
    assert set(RELATED_PAGES) <= set(anchors)
    assert all("](http" in source.citation for source in sources)
    assert len(sources) == len(set(sources))


@pytest.mark.parametrize(
    "integrand, antiderivative",
    [
        (lambda x: x**3, lambda x: x**4 / 4),
        (lambda x: 1 / x, lambda x: np.log(np.abs(x))),
        (lambda x: 2**x, lambda x: 2**x / np.log(2)),
        (lambda x: np.exp(3 * x), lambda x: np.exp(3 * x) / 3),
        (lambda x: 1 / np.cos(x) ** 2, np.tan),
        (lambda x: 1 / np.sin(x) ** 2, lambda x: -1 / np.tan(x)),
        (lambda x: 1 / (1 + x**2), np.arctan),
        (np.sqrt, lambda x: 2 / 3 * x**1.5),
        (lambda x: 3 * x**2 - 4 / x + 2 * np.exp(x), lambda x: x**3 - 4 * np.log(np.abs(x)) + 2 * np.exp(x)),
        (lambda x: x * np.exp(x), lambda x: (x - 1) * np.exp(x)),
        (np.log, lambda x: x * np.log(x) - x),
        (lambda x: x**2 * np.cos(x), lambda x: x**2 * np.sin(x) + 2 * x * np.cos(x) - 2 * np.sin(x)),
        (lambda x: 2 * x * np.cos(x**2), lambda x: np.sin(x**2)),
        (lambda x: x * np.exp(-(x**2) / 2), lambda x: -np.exp(-(x**2) / 2)),
        (np.tan, lambda x: -np.log(np.abs(np.cos(x)))),
        (lambda x: np.cos(3 * x), lambda x: np.sin(3 * x) / 3),
    ],
)
def test_derivace_primitivni_funkce_z_tahaku_vrati_integrand(integrand, antiderivative):
    np.testing.assert_allclose(derivative(antiderivative, SAMPLE_POINTS), integrand(SAMPLE_POINTS), rtol=1e-6)


def test_urcite_integraly_z_tahaku():
    assert integrate(lambda x: x**2, 0, 1) == pytest.approx(1 / 3, rel=1e-9)
    assert integrate(lambda x: x * np.exp(x), 0, 1) == pytest.approx(1, rel=1e-9)
    assert integrate(lambda x: 2 * np.sqrt(np.clip(1 - x**2, 0, None)), -1, 1) == pytest.approx(pi, rel=1e-6)
    far_tail = np.geomspace(1, 1e6, 2_000_001)
    assert np.trapezoid(far_tail**-2.0, far_tail) == pytest.approx(1 - 1e-6, rel=1e-6)


def test_gaussovske_integraly_z_tahaku():
    density = lambda x: np.exp(-(x**2) / 2) / sqrt(2 * pi)  # noqa: E731

    assert integrate(lambda x: np.exp(-(x**2) / 2), -40, 40) == pytest.approx(sqrt(2 * pi), rel=1e-9)
    assert f"{sqrt(2 * pi):.3f}".replace(".", "{,}") in GAUSSIAN_TOPIC.explanation
    assert integrate(lambda x: np.exp(-2 * x**2), -40, 40) == pytest.approx(sqrt(pi / 2), rel=1e-9)
    assert [integrate(lambda x, power=power: x**power * density(x), -40, 40) for power in (2, 4, 6)] == (
        pytest.approx([1, 3, 15], rel=1e-8)
    )
    assert integrate(lambda x: np.cosh(x) * density(x), -40, 40) == pytest.approx(exp(0.5), rel=1e-9)


def test_chyba_monte_carla_v_prikladu_odpovida_rozptylu():
    standard_deviation = sqrt(1 / 5 - 1 / 9)

    assert f"{standard_deviation:.3f}".replace(".", "{,}") == MONTE_CARLO_STANDARD_ERROR
    assert MONTE_CARLO_STANDARD_ERROR in MONTE_CARLO_TOPIC.explanation
    assert f"{standard_deviation / sqrt(10_000):.3f}".replace(".", ",") in MONTE_CARLO_TOPIC.explanation
