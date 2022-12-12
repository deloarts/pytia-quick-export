"""
    Document data models.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True, kw_only=True)
class DatumModel:
    index: int
    name: str  # Represents the header item name
    value: str | None


@dataclass(slots=True)
class DataModel:
    data: List[DatumModel] = field(default_factory=lambda: [])
