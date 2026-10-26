"""Markdown split into top-level blocks (paragraphs, lists, display formulas), each editable on its own.

A block ends at a blank line, except inside a code fence or a $$ formula, and except where a list goes on after
the blank line (a loose list or an indented continuation stays one block, so its numbering and spacing do not
change). Joining the blocks with blank lines renders the same as the original text.
"""

from __future__ import annotations

import hashlib
import re
import textwrap
from typing import List, Tuple

KEY_LENGTH = 16
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
LIST_ITEM = re.compile(r"^ {0,3}([-*+]|\d{1,9}[.)])(\s|$)")


def split_blocks(markdown: str) -> List[str]:
    """Blocks of the text after the same dedent that dcc.Markdown applies; empty text has no blocks."""
    blocks: List[str] = []
    current: List[str] = []
    fence = ""
    in_formula = False
    blank_pending = False
    for line in textwrap.dedent(markdown).split("\n"):
        if fence or in_formula:
            current.append(line)
        elif not line.strip():
            blank_pending = bool(current)
            continue
        elif blank_pending and not _continues_list(current, line):
            blocks.append(_joined(current))
            current = [line]
        else:
            current.extend(["", line] if blank_pending else [line])
        blank_pending = False
        fence, in_formula = _state_after(line, fence, in_formula)
    if current:
        blocks.append(_joined(current))
    return blocks


def block_key(block: str) -> str:
    """Identifies a block by its original text, so an edit stays with its paragraph when others change."""
    return hashlib.sha256(block.encode("utf-8")).hexdigest()[:KEY_LENGTH]


def _joined(lines: List[str]) -> str:
    return "\n".join(lines).rstrip()


def _continues_list(current: List[str], line: str) -> bool:
    in_list = any(LIST_ITEM.match(previous) for previous in current)
    return in_list and (bool(LIST_ITEM.match(line)) or line[:1] in (" ", "\t"))


def _state_after(line: str, fence: str, in_formula: bool) -> Tuple[str, bool]:
    """Whether the next line is still inside a code fence or a $$ formula."""
    if fence:
        return ("" if line.strip().startswith(fence) else fence), in_formula
    opening = FENCE.match(line)
    if opening and not in_formula:
        return opening.group(1), False
    if line.count("$$") % 2:
        return "", not in_formula
    return "", in_formula
