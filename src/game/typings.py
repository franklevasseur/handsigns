from typing import Protocol

import pyglet

Orientation = tuple[tuple[float, float], tuple[float, float]]


class Controller(Protocol):

    def check_in(self, w: pyglet.window.Window) -> None:
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
