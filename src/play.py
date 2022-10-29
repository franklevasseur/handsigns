import pathlib as pl
import pickle
import threading

from . import logger as log
from .controller import HandController
from .game import GameWindow
from .typings import TrainArtifact
from .videohandle import VideoHandler


def play(model_path: pl.Path, media_dir: pl.Path, logger: log.Logger) -> None:
    logger.info(f"Let's play a game...")

    with open(model_path, 'rb') as f:
        artifact: TrainArtifact = pickle.load(f)

    controller = HandController(artifact, logger)
    videoHandler = VideoHandler(controller.handle_sample)
    game = GameWindow(media_dir, controller)
    game.setup()

    videoHandler_thread = threading.Thread(target=videoHandler.run)
    videoHandler_thread.start()
    game.run()
