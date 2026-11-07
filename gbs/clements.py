"""Clements decomposition: phases of a rectangular MZI mesh that realise a given unitary matrix.

Clements a kol., Optica 3, 1460 (2016): MZIs applied alternately from the right and from the left null the elements
below the antidiagonal one by one (Givens rotations), until a diagonal matrix of phases is left. The MZIs applied
from the left are then moved through that diagonal to the right. The result is exact on the ideal chip, up to
one phase per output waveguide that no photon counter sees.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

import numpy as np

from gbs.photonic_chip import ChipError, MeshPhases, mesh_slots, mzi_count, mzi_matrix

UNITARITY_TOLERANCE = 1e-9
FULL_TURN = 2 * np.pi


@dataclass(frozen=True)
class ClementsDecomposition:
    phases: MeshPhases
    output_phases: np.ndarray
    """Diagonal D of U = D·mesh(θ, φ): a unit complex number on each output waveguide."""


@dataclass(frozen=True)
class _Mzi:
    upper_mode: int
    internal: float
    external: float

    @property
    def matrix(self) -> np.ndarray:
        return mzi_matrix(self.internal, self.external)


def clements_decomposition(unitary: np.ndarray) -> ClementsDecomposition:
    matrix = _checked_unitary(unitary)
    from_right, from_left, diagonal = _null_below_antidiagonal(matrix)
    moved, output_phases = _move_through_diagonal(from_left, diagonal)
    return ClementsDecomposition(_arrange_in_mesh(from_right + moved, matrix.shape[0]), output_phases)


def _checked_unitary(unitary: np.ndarray) -> np.ndarray:
    matrix = np.array(unitary, dtype=complex)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or matrix.shape[0] < 2:
        raise ChipError(f"Cílová matice musí být čtvercová aspoň 2 × 2, zadaný tvar je {matrix.shape}.")
    if not np.allclose(matrix.conj().T @ matrix, np.eye(matrix.shape[0]), atol=UNITARITY_TOLERANCE):
        raise ChipError("Cílová matice musí být unitární, jinak ji síť interferometrů bez ztrát nesestaví.")
    return matrix


def _null_below_antidiagonal(unitary: np.ndarray) -> Tuple[List[_Mzi], List[_Mzi], np.ndarray]:
    """MZIs from the right (in the order applied), MZIs from the left and the diagonal that is left over."""
    matrix = unitary.copy()
    size = matrix.shape[0]
    from_right: List[_Mzi] = []
    from_left: List[_Mzi] = []
    for diagonal in range(size - 1):
        if diagonal % 2 == 0:
            for step in range(diagonal + 1):
                row, column = size - 1 - step, diagonal - step
                mzi = _nulling_from_right(matrix[row, column], matrix[row, column + 1], column)
                columns = slice(column, column + 2)
                matrix[:, columns] = matrix[:, columns] @ mzi.matrix.conj().T
                from_right.append(mzi)
        else:
            for step in range(1, diagonal + 2):
                row, column = size + step - diagonal - 2, step - 1
                mzi = _nulling_from_left(matrix[row - 1, column], matrix[row, column], row - 1)
                rows = slice(row - 1, row + 1)
                matrix[rows, :] = mzi.matrix @ matrix[rows, :]
                from_left.append(mzi)
    return from_right, from_left, np.diag(matrix).copy()


def _nulling_from_right(left: complex, right: complex, upper_mode: int) -> _Mzi:
    """U·T⁻¹ on columns (m, m + 1) zeroes the element in column m: e^{−iφ}·left·sin(θ/2) = −right·cos(θ/2)."""
    internal = 2 * np.arctan2(abs(right), abs(left))
    external = np.angle(left) - np.angle(right) - np.pi
    return _Mzi(upper_mode, float(internal), _wrapped(external))


def _nulling_from_left(upper: complex, lower: complex, upper_mode: int) -> _Mzi:
    """T·U on rows (m, m + 1) zeroes the element in row m + 1: e^{iφ}·upper·cos(θ/2) = lower·sin(θ/2)."""
    internal = 2 * np.arctan2(abs(upper), abs(lower))
    external = np.angle(lower) - np.angle(upper)
    return _Mzi(upper_mode, float(internal), _wrapped(external))


def _move_through_diagonal(from_left: Sequence[_Mzi], diagonal: np.ndarray) -> Tuple[List[_Mzi], np.ndarray]:
    """T(θ, φ)⁻¹·D = D'·T(θ, φ') with φ' = arg d₁ − arg d₂, starting with the MZI nearest to D."""
    phases = diagonal.copy()
    moved: List[_Mzi] = []
    for mzi in reversed(from_left):
        upper, lower = phases[mzi.upper_mode], phases[mzi.upper_mode + 1]
        factor = -np.exp(-1j * mzi.internal)
        phases[mzi.upper_mode] = factor * np.exp(-1j * mzi.external) * lower
        phases[mzi.upper_mode + 1] = factor * lower
        moved.append(_Mzi(mzi.upper_mode, mzi.internal, _wrapped(np.angle(upper) - np.angle(lower))))
    return moved, phases


def _arrange_in_mesh(mzis_in_order: Sequence[_Mzi], mode_count: int) -> MeshPhases:
    """Each MZI goes to the first column after the ones its waveguides already passed; Clements' order fills
    the rectangle exactly, so the mesh multiplies the MZIs in the same order."""
    slot_index: Dict[Tuple[int, int], int] = {
        (slot.column, slot.upper_mode): index for index, slot in enumerate(mesh_slots(mode_count))
    }
    internal = [0.0] * mzi_count(mode_count)
    external = [0.0] * mzi_count(mode_count)
    next_free_column = [0] * mode_count
    filled = set()
    for mzi in mzis_in_order:
        column = max(next_free_column[mzi.upper_mode], next_free_column[mzi.upper_mode + 1])
        if column % 2 != mzi.upper_mode % 2:
            column += 1
        index = slot_index.get((column, mzi.upper_mode))
        if index is None or index in filled:
            raise RuntimeError(
                f"Clements decomposition left the rectangular mesh: column {column}, modes {mzi.upper_mode}, "
                f"{mzi.upper_mode + 1}."
            )
        filled.add(index)
        internal[index], external[index] = mzi.internal, mzi.external
        next_free_column[mzi.upper_mode] = next_free_column[mzi.upper_mode + 1] = column + 1
    return MeshPhases(tuple(internal), tuple(external))


def _wrapped(phase: float) -> float:
    return float(np.mod(phase, FULL_TURN))
