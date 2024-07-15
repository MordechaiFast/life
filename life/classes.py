from collections import defaultdict
from dataclasses import dataclass
from typing import Self


type point = tuple[int, int]


@dataclass
class Pattern:
    name: str
    cells: set[point]

    @classmethod
    def from_toml(cls, name, toml_data) -> Self:
        return cls(name, {tuple(cell) for cell in toml_data["alive_cells"]})


NEIGHBOR_DELTAS: tuple[point] = (
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1)
)
ALIVE = "♥"
DEAD = "‧"


class Grid:
    def __init__(self, pattern: Pattern) -> None:
        if type(pattern) is Pattern:
            self.cells = pattern.cells.copy()
        elif type(pattern) is set:
            self.cells = pattern.copy()
        else:
            raise ValueError(pattern)

    def evolve(self) -> None:
        """Rules of Life:
        Cells can be either dead or alive.
        At each step of the grid's evolution:
        - Cells with one or zero neighbors die.
        - Cells with two neighbors stay alive but don't come alive.
        - Cells with three nighbors come alive (or stay alive).
        - Cells with more than three neighbors die.
        """
        neighbors_count = defaultdict(int)
        for x, y in self.cells:
            for dx, dy in NEIGHBOR_DELTAS:
                neighbors_count[(x + dx, y + dy)] += 1
        stay_alive = {
            cell for cell in neighbors_count if neighbors_count[cell] == 2
        } & self.cells
        come_alive = {
            cell for cell in neighbors_count if neighbors_count[cell] == 3
        }
        self.cells = stay_alive | come_alive

    def window(self, top_right: point, bottom_left: point) -> str:
        rows = (
            " ".join(
                ALIVE if (x, y) in self.cells else DEAD
                for y in range(top_right[1], bottom_left[1])
            )
            for x in range(top_right[0], bottom_left[0])
        )
        return " " + "\n ".join(rows)

    def __repr__(self) -> str:
        return (self.__class__.__name__ + "({"
                + ", ".join(str(cell) for cell in sorted(self.cells))
                + "})")
