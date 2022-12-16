import pathlib as pl
import random
from typing import Any, cast

import arcade
import pyglet

from .map_loader import load_map
from .typings import Controller

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1000
SCREEN_TITLE: str = 'Escape the Dungeon'

WELCOME_MESSAGE = 'Hello Denis... Welcome to the Dungeon of Infinity... Try to escape... Good luck...'

CHARACTER_SCALING = 0.15
KEY_INDICATOR_SCALING = 0.20
WALL_SCALING = 0.5
FLOOR_SCALING = 1
PLAYER_MOVEMENT_SPEED = 0.05
WALL_SIZE = 64

CHAR_SIZE = 14
SIZE_PER_CHAR = 4


WALL_RESSOURCE = ":resources:images/tiles/stoneCenter.png"
FLOOR_RESSOURCE = ":resources:images/topdown_tanks/tileSand2.png"
DOOR_RESSOURCE = ":resources:images/tiles/doorClosed_mid.png"
KEY_RESSOURCE = ":resources:images/items/keyYellow.png"


def PLAYER_RESSOURCE(media_dir: pl.Path | str): return str(media_dir / pl.Path('images', 'jesus.png'))
def MAP_RESSOURCE(media_dir: pl.Path | str): return str(media_dir / pl.Path('maps', 'dungeon_of_infinity.txt'))
def MUSIC_RESSOURCE(media_dir: pl.Path | str): return str(media_dir / pl.Path('sounds', 'soundtrack.mp3'))


class Door(arcade.Sprite):

    def __init__(self, x: float, y: float, key: str):
        super().__init__(DOOR_RESSOURCE, WALL_SCALING)
        self.center_x = x
        self.center_y = y

        self._default_hit_box = self.hit_box
        self._empty_hit_box: arcade.PointList = [(0.0, 0.0)]

        self.key = key

    def open(self):
        self.set_hit_box(self._empty_hit_box)
        self.alpha = 125

    def close(self):
        self.set_hit_box(self._default_hit_box)
        self.alpha = 255


class ExitKey(arcade.Sprite):

    def __init__(self, x: float, y: float):
        super().__init__(KEY_RESSOURCE, WALL_SCALING)
        self.center_x = x
        self.center_y = y
        self._picked_up = False

    @property
    def picked_up(self):
        return self._picked_up

    def pickup(self):
        self._picked_up = True

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        if self._picked_up:
            return
        return super().draw(filter=filter, pixelated=pixelated, blend_function=blend_function)


class Player(arcade.Sprite):

    def __init__(self, media_dir):
        super().__init__(PLAYER_RESSOURCE(media_dir), CHARACTER_SCALING)
        self.key_indicator: arcade.Sprite | None = None

    def pickkey(self):
        self.key_indicator = arcade.Sprite(KEY_RESSOURCE, KEY_INDICATOR_SCALING)

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        if self.key_indicator:
            self.key_indicator.center_x = self.center_x + 30
            self.key_indicator.center_y = self.center_y + 30
            self.key_indicator.draw(filter=filter, pixelated=pixelated, blend_function=blend_function)
        return super().draw(filter=filter, pixelated=pixelated, blend_function=blend_function)


class GameWindow(arcade.Window):

    def __init__(self, media_dir: pl.Path, controller: Controller):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, screen=cast(Any, None))

        self.controller = controller
        self.controller.check_in(self)
        self.media_dir = media_dir

        self.spawn: tuple[float, float]

        self.physics_engine: arcade.PhysicsEngineSimple
        self.camera: arcade.Camera

        self.my_music: arcade.Sound
        self.media_player: pyglet.media.Player

        self.walls: arcade.SpriteList
        self.decorations: arcade.SpriteList

        self.doors: list[Door] = []
        self.player: Player
        self.exit_key: ExitKey

        self.map = load_map(MAP_RESSOURCE(media_dir))

    def setup(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
        self.camera = arcade.Camera(self.width, self.height)

        self.my_music = cast(arcade.Sound, arcade.load_sound(MUSIC_RESSOURCE(self.media_dir)))
        self.media_player = self.my_music.play()

        self.player = Player(self.media_dir)
        self.walls = arcade.SpriteList(use_spatial_hash=True)
        self.decorations = arcade.SpriteList(use_spatial_hash=True)

        current_x: float = 0.0
        current_y: float = len(self.map) * WALL_SIZE
        for row in self.map:
            current_x = 0.0
            for cell in row:
                if cell == "wall":
                    wall = arcade.Sprite(WALL_RESSOURCE, WALL_SCALING)
                    wall.center_x = current_x
                    wall.center_y = current_y
                    self.walls.append(wall)
                elif cell == "door":
                    N = len(self.controller.all_symbols)
                    # random int between 0 and N-1
                    i = random.randint(0, N - 1)
                    symbol = self.controller.all_symbols[i]

                    door = Door(current_x, current_y, symbol)
                    self.doors.append(door)
                    self.walls.append(door)
                elif cell == "spawn":
                    spawner = arcade.SpriteSolidColor(WALL_SIZE, WALL_SIZE, arcade.csscolor.DARK_RED)
                    spawner.center_x = current_x
                    spawner.center_y = current_y
                    self.spawn = (current_x, current_y)
                    self.decorations.append(spawner)
                    self.player.center_x = current_x
                    self.player.center_y = current_y
                elif cell == "void":
                    voider = arcade.SpriteSolidColor(WALL_SIZE, WALL_SIZE, (5, 5, 5))
                    voider.center_x = current_x
                    voider.center_y = current_y
                    self.decorations.append(voider)
                    pass
                elif cell == "floor" or cell == "key":
                    if cell == "key":
                        self.exit_key = ExitKey(current_x, current_y)

                    floor = arcade.Sprite(FLOOR_RESSOURCE, FLOOR_SCALING)
                    floor.center_x = current_x
                    floor.center_y = current_y
                    floor.alpha = 200
                    self.decorations.append(floor)
                current_x += WALL_SIZE
            current_y -= WALL_SIZE

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.walls)

    def on_update(self, delta_time: float):

        orientation = self.controller.orientation
        symbol = self.controller.symbol

        delta_y = orientation[1][1] - orientation[0][1]
        self.player.change_y = - delta_y * PLAYER_MOVEMENT_SPEED

        delta_x = orientation[1][0] - orientation[0][0]
        self.player.change_x = - delta_x * PLAYER_MOVEMENT_SPEED

        for d in self.doors:
            if d.key == symbol:
                d.open()
            else:
                d.close()

        collides = arcade.check_for_collision(self.player, self.exit_key)
        if collides:
            self.exit_key.pickup()
            self.player.pickkey()

        self.physics_engine.update()
        self.center_camera_to_player()

    def center_camera_to_player(self):
        screen_center_x: float = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y: float = self.player.center_y - (self.camera.viewport_height / 2)
        player_centered = pyglet.math.Vec2(screen_center_x, screen_center_y)
        self.camera.move_to(player_centered)

    def draw_welcome_message(self):
        arcade.draw_text(WELCOME_MESSAGE, self.spawn[0] - (len(WELCOME_MESSAGE) * SIZE_PER_CHAR), self.spawn[1] - WALL_SIZE, arcade.color.DARK_RED, CHAR_SIZE)

    def draw_orientation(self):
        orientation = self.controller.orientation

        delta_x = orientation[1][0] - orientation[0][0]
        delta_y = orientation[1][1] - orientation[0][1]
        x1 = self.player.center_x
        y1 = self.player.center_y
        x2 = x1 - delta_x
        y2 = y1 - delta_y
        arcade.draw_line(x1, y1, x2, y2, arcade.color.DARK_RED, 2)

    def draw_symbols(self):
        for d in self.doors:
            arcade.draw_text(d.key, d.center_x - (len(d.key) * SIZE_PER_CHAR), d.center_y - WALL_SIZE, arcade.color.DARK_RED, CHAR_SIZE)

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.decorations.draw()
        self.player.draw()
        self.exit_key.draw()
        self.walls.draw()
        self.draw_welcome_message()
        self.draw_orientation()
        self.draw_symbols()
