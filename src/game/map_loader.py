from pathlib import Path
from typing import Literal

CellType = Literal["wall", "floor", "door", "spawn", "key", "exit", "void"]
Mapp = list[list[CellType]]


def cell_to_char(cell: CellType) -> str:
    """Convert a cell type to a character."""
    if cell == "wall":
        return "#"
    if cell == "floor":
        return "."
    if cell == "spawn":
        return "s"
    if cell == "door":
        return "+"
    if cell == "key":
        return "k"
    if cell == "exit":
        return "e"

    return " "


def char_to_cell(char: str) -> CellType:
    """Convert a character to a cell type."""
    if char == "#":
        return "wall"
    if char == ".":
        return "floor"
    if char == "s":
        return "spawn"
    if char == "+":
        return "door"
    if char == "k":
        return "key"
    if char == "e":
        return "exit"

    return "void"


def load_map(file: Path | str) -> Mapp:
    """Load a map from a file."""

    mapp: Mapp
    with open(file, "r") as f:
        mapp = [[char_to_cell(char) for char in line] for line in f.read().splitlines()]

    return mapp
