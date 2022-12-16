import pathlib as pl
import pickle
import threading
from typing import Literal, TypedDict

from . import logger as log
from .game import GameWindow
from .handcontroller import HandController
from .keyboardcontroller import KeyboardController
from .typings import TrainArtifact
from .videohandle import VideoHandler

ControlType = Literal['video', 'keyboard']


class BaseProps(TypedDict):
    logger: log.Logger
    media_dir: pl.Path


class VideoProps(BaseProps):
    control: Literal['video']
    model_path: pl.Path


class KeyboardProps(BaseProps):
    control: Literal['keyboard']


def play(props: VideoProps | KeyboardProps) -> None:
    props['logger'].info(f"Let's play a game...")
    if props['control'] == 'video':
        play_video(props)

    if props['control'] == 'keyboard':
        play_keyboard(props)


def play_video(props: VideoProps) -> None:
    logger = props['logger']
    media_dir = props['media_dir']
    model_path = props['model_path']

    logger.debug("video detected.")

    with open(model_path, 'rb') as f:
        artifact: TrainArtifact = pickle.load(f)

    controller = HandController(artifact, logger)
    videoHandler = VideoHandler(controller.handle_sample)
    game = GameWindow(media_dir, controller)
    game.setup()

    videoHandler_thread = threading.Thread(target=videoHandler.run)
    videoHandler_thread.start()
    game.run()

    videoHandler.kill()
    videoHandler_thread.join()


def play_keyboard(props: KeyboardProps) -> None:
    logger = props['logger']
    media_dir = props['media_dir']

    logger.debug("keyboard detected.")

    controller = KeyboardController(logger)
    game = GameWindow(media_dir, controller)
    game.setup()
    game.run()
