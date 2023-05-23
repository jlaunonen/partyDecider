from __future__ import annotations

from dataclasses import dataclass

from .utils import parse_bool


@dataclass
class AppItem:
    id: int
    steam_id: int | None
    name: str
    enabled: bool = False

    def to_csv(self) -> tuple:
        return self.id, self.steam_id, int(self.enabled), self.name

    @classmethod
    def from_csv(cls, row: list[str]) -> AppItem:
        if len(row) != 4:
            raise ValueError(row)

        return AppItem(
            id=int(row[0]),
            steam_id=int(row[1]) if row[1] else None,
            name=row[3],
            enabled=parse_bool(row[2], False),
        )
