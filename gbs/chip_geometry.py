"""Where the parts of the drawn chip lie: columns of MZIs from left to right, waveguide 1 on top."""

from __future__ import annotations

from typing import List

from gbs.photonic_chip import Chip

COLUMN_WIDTH = 1.6
LEAD_LENGTH = 0.5
COUPLER_GAP = 0.07
"""Half the distance of the two waveguides inside a directional coupler (the mode spacing is 1)."""
EXTERNAL_SHIFTER_AT = 0.07
FIRST_BEND = (0.14, 0.24)
FIRST_COUPLER_CENTER = 0.30
SECOND_BEND_FROM_FIRST = (0.36, 0.46)
INTERNAL_SHIFTER_AT = 0.50
SECOND_BEND = (0.54, 0.64)
SECOND_COUPLER_CENTER = 0.70
LAST_BEND = (0.76, 0.86)
"""Positions along one column as fractions of its width: φ, coupler, arms with θ, coupler, way out."""
PORT_LABEL_ROOM = 1.0
PORT_LABEL_ROOM_PER_COLUMN = 0.16
"""Room left and right of the chip for the input labels and the detected shares; wide chips are drawn smaller, so
their labels need more of the axis."""
MAX_SHIFTER_MODES = 8
"""Larger chips are drawn without phase shifters, which would no longer fit."""
COORDINATE_DECIMALS = 3


def label_room(mode_count: int) -> float:
    return max(PORT_LABEL_ROOM, PORT_LABEL_ROOM_PER_COLUMN * mode_count)


def wire_y(mode: int, mode_count: int) -> float:
    """Waveguide 1 on top."""
    return float(mode_count - 1 - mode)


def column_x(column: int, fraction: float) -> float:
    """Rounded, because the coordinates end up as text in SVG paths sent to the browser."""
    return round((column + fraction) * COLUMN_WIDTH, COORDINATE_DECIMALS)


def chip_end(mode_count: int) -> float:
    return mode_count * COLUMN_WIDTH


def modes_outside_mzis(chip: Chip, column: int) -> List[int]:
    """Waveguides that pass the column straight, at the edge of the mesh."""
    in_mzis = {mode for slot in chip.slots if slot.column == column for mode in (slot.upper_mode, slot.lower_mode)}
    return sorted(set(range(chip.mode_count)) - in_mzis)
