"""Estimated reading time of explanatory texts, shown in tables of contents to help plan studying."""

from __future__ import annotations

import math
import re
from typing import Iterable

WORDS_PER_MINUTE = 150
"""Slower than the usual 200–250 words per minute: the texts are technical and full of formulas."""

WORD_PATTERN = re.compile(r"[^\W\d_]+")


def reading_minutes(texts: Iterable[str]) -> int:
    word_count = sum(len(WORD_PATTERN.findall(text)) for text in texts)
    return max(1, math.ceil(word_count / WORDS_PER_MINUTE))


def reading_time_label(minutes: int) -> str:
    return f"{minutes} min čtení"
