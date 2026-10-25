import numpy as np
import pytest

from gbs.advantage_share import advantage_share
from ui import ids
from ui.navigation import (
    ACTIVE_LINK_CLASS,
    NAV_LINK_IDS,
    PAGE_BY_PATH,
    PAGE_IDS,
    QPURPOSE_PATH,
    qpurpose_href,
    show_page,
)
from ui.qpurpose_content import (
    KEY_FINDINGS,
    REPLICATION_COEFFICIENT_VECTORS,
    REPLICATION_MATRICES,
    REPLICATION_SEED,
    REPLICATION_SHARES,
    SOURCES_ANCHOR,
    TOPICS,
)
from ui.qpurpose_page import build_qpurpose_page, degree_sweep_markdown
from ui.topic_catalog import breadcrumb_trail


def test_stranka_qpurpose_je_podstrankou_vyhody_gbs():
    link_classes = show_page(QPURPOSE_PATH)[len(PAGE_IDS):len(PAGE_IDS) + len(NAV_LINK_IDS)]
    active = [link_id for link_id, link_class in zip(NAV_LINK_IDS, link_classes) if link_class == ACTIVE_LINK_CLASS]

    assert PAGE_BY_PATH[QPURPOSE_PATH] == ids.QPURPOSE_PAGE
    assert active == [ids.NAV_CORE_MENU]
    assert [label for label, _ in breadcrumb_trail(ids.QPURPOSE_PAGE)][-2:] == [
        "Výhoda GBS", "Qpurpose: co skutečně prodávají",
    ]


def test_kapitoly_maji_unikatni_kotvy_a_tldr_na_ne_odkazuje():
    anchors = [topic.anchor for topic in TOPICS]
    page = build_qpurpose_page()
    section_ids = [child.id for child in page.children if getattr(child, "id", None)]

    assert section_ids == anchors + [SOURCES_ANCHOR]
    assert {finding.anchor for finding in KEY_FINDINGS} <= set(anchors)
    assert qpurpose_href(anchors[0]) == f"{QPURPOSE_PATH}#{anchors[0]}"


def test_tabulka_stupnu_ukazuje_vzory_pro_presny_vypocet():
    rows = degree_sweep_markdown().splitlines()

    assert len(rows) == 2 + 8
    assert rows[2].startswith("| 1 | 6 |") and rows[-1].startswith("| 8 | 153 |")


def test_ulozeny_prepocet_obrazku_2_odpovida_vypoctu():
    rng = np.random.default_rng(REPLICATION_SEED)
    for stored in REPLICATION_SHARES:
        computed = advantage_share(
            stored.mode_count, stored.degree, REPLICATION_MATRICES, REPLICATION_COEFFICIENT_VECTORS, rng
        )
        assert computed.derived_percent == pytest.approx(stored.derived_percent, abs=0.01)
        assert computed.printed_percent == pytest.approx(stored.printed_percent, abs=0.01)
        assert computed.median_scale == pytest.approx(stored.median_scale, rel=1e-3)
        assert computed.median_variance_ratio == pytest.approx(stored.median_variance_ratio, rel=1e-3)
