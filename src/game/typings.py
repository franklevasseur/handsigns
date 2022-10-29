from typing import Protocol

Orientation = tuple[tuple[float, float], tuple[float, float]]


class Controller(Protocol):
    @property
    def all_symbols(self) -> list[str]:
        ...

    @property
    def orientation(self) -> Orientation:
        ...

    @property
    def symbol(self) -> str:
        ...
