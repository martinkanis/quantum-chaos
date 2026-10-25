import re
from pathlib import Path

from app import app
from ui.layout import HIGHLIGHT_ROOTS_ATTRIBUTE
from ui.navigation import PAGE_IDS

ASSETS = Path(__file__).resolve().parent.parent / "assets"
SCRIPT = (ASSETS / "highlighter.js").read_text(encoding="utf-8")
COLOR_PATTERN = re.compile(r'\{name: "([^"]+)", fill: "(#[0-9a-f]{6})", line: "(#[0-9a-f]{6})"\}')
TEXT_COLOR = "#1c2330"
"""--text in assets/style.css."""


def relative_luminance(hex_color: str) -> float:
    channels = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(first: str, second: str) -> float:
    lighter, darker = sorted((relative_luminance(first), relative_luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def test_zvyraznovat_jde_text_na_kazde_strance_aplikace():
    roots = app.layout.to_plotly_json()["props"][HIGHLIGHT_ROOTS_ATTRIBUTE].split()

    assert roots == list(PAGE_IDS)
    assert set(roots) <= set(app.layout)
    assert f'"{HIGHLIGHT_ROOTS_ATTRIBUTE}"' in SCRIPT


def test_paleta_ma_devet_ruznych_pastelovych_barev_se_ctivym_textem():
    colors = COLOR_PATTERN.findall(SCRIPT)
    names = [name for name, _fill, _line in colors]
    fills = [fill for _name, fill, _line in colors]

    assert len(colors) == 9
    assert len(set(names)) == len(set(fills)) == 9
    # Pastel: light enough that the page's dark text keeps the highest (AAA) contrast on the highlight.
    assert all(contrast(fill, TEXT_COLOR) >= 7 for fill in fills)
