import pyglet

from . import logger as log
from .game.typings import Controller, KeyDetector, Orientation

DEFAULT_ORIENTATION = ((0.0, 0.0), (0.0, 0.0))
DEFAULT_SYMBOL = 'none'
ALL_SYMBOLS = ['w', 'a', 's', 'd']
SPEED = 200.0


class KeyboardController(Controller):

    def __init__(self, logger: log.Logger) -> None:
        self.logger = logger
        self._key_pressed: list[int] = []

    def check_in(self, w: KeyDetector) -> None:
        w.on_key_press = self._on_key_press
        w.on_key_release = self._on_key_release

    @property
    def orientation(self) -> Orientation:
        dy = 0.0
        dx = 0.0
        if pyglet.window.key.UP in self._key_pressed:
            dy += SPEED
        if pyglet.window.key.DOWN in self._key_pressed:
            dy -= SPEED
        if pyglet.window.key.LEFT in self._key_pressed:
            dx -= SPEED
        if pyglet.window.key.RIGHT in self._key_pressed:
            dx += SPEED

        orientation = ((dx, dy), (0, 0))
        return orientation

    @property
    def symbol(self) -> str:
        if pyglet.window.key.W in self._key_pressed:
            return 'w'
        if pyglet.window.key.A in self._key_pressed:
            return 'a'
        if pyglet.window.key.S in self._key_pressed:
            return 's'
        if pyglet.window.key.D in self._key_pressed:
            return 'd'
        return DEFAULT_SYMBOL

    @property
    def all_symbols(self) -> list[str]:
        return ALL_SYMBOLS

    def _on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol not in self._key_pressed:
            self._key_pressed.append(symbol)

    def _on_key_release(self, symbol: int, modifiers: int) -> None:
        if symbol in self._key_pressed:
            self._key_pressed.remove(symbol)
