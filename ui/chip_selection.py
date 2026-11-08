"""The phase shifter the reader works with in laboratory 1: picked by a click on the chip, set by one slider."""

from __future__ import annotations

from typing import Any, Dict, Optional

from gbs.chip_parts import ChipPart, ClickedPart, SelectedShifter
from gbs.photonic_chip import mesh_slots

SHIFTER_PARTS = (ChipPart.INTERNAL_SHIFTER, ChipPart.EXTERNAL_SHIFTER)
DEFAULT_SELECTED_SHIFTER = SelectedShifter(ChipPart.INTERNAL_SHIFTER, 0)
SHIFTER_SYMBOLS = {ChipPart.INTERNAL_SHIFTER: "θ", ChipPart.EXTERNAL_SHIFTER: "φ"}
SHIFTER_ROLES = {ChipPart.INTERNAL_SHIFTER: "dělení světla", ChipPart.EXTERNAL_SHIFTER: "fáze horního vstupu"}


def selected_shifter_data(shifter: SelectedShifter) -> Dict[str, Any]:
    """What dcc.Store keeps of the selection."""
    return {"part": shifter.part.value, "mzi": shifter.mzi}


def parse_selected_shifter(data: Any, mzi_total: int) -> SelectedShifter:
    """The stored selection, or θ of MZI 1 when there is none or the chip no longer has that MZI."""
    if not isinstance(data, dict):
        return DEFAULT_SELECTED_SHIFTER
    part, mzi = data.get("part"), data.get("mzi")
    is_shifter = part in {shifter_part.value for shifter_part in SHIFTER_PARTS}
    if not is_shifter or not isinstance(mzi, int) or not 0 <= mzi < mzi_total:
        return DEFAULT_SELECTED_SHIFTER
    return SelectedShifter(ChipPart(part), mzi)


def selection_for_click(clicked: ClickedPart) -> Optional[SelectedShifter]:
    """A click on a shifter selects it, a click on an MZI its θ; other parts select nothing."""
    if clicked.part in SHIFTER_PARTS:
        return SelectedShifter(clicked.part, clicked.index)
    if clicked.part == ChipPart.MZI:
        return SelectedShifter(ChipPart.INTERNAL_SHIFTER, clicked.index)
    return None


def selected_shifter_title(shifter: SelectedShifter, mode_count: int) -> str:
    slot = mesh_slots(mode_count)[shifter.mzi]
    number = shifter.mzi + 1
    return (
        f"{SHIFTER_SYMBOLS[shifter.part]}{number} · MZI {number} (světlovody {slot.upper_mode + 1} a "
        f"{slot.lower_mode + 1}) – {SHIFTER_ROLES[shifter.part]}"
    )
