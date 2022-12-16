from typing import Protocol

Orientation = tuple[tuple[float, float], tuple[float, float]]


class KeyDetector(Protocol):

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        ...

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        ...


class Controller(Protocol):

    def check_in(self, w: KeyDetector) -> None:
        ...

    @property
    def all_symbols(self) -> list[str]:
        ...

    @property
    def orientation(self) -> Orientation:
        ...

    @property
    def symbol(self) -> str:
        ...
