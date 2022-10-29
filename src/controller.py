from typing import Any, cast

import cv2
import numpy as np
import numpy.typing as npt

from . import logger as log
from .game.typings import Controller, Orientation
from .typings import TrainArtifact
from .videohandle import Result

DEFAULT_ORIENTATION = ((0.0, 0.0), (0.0, 0.0))
DEFAULT_SYMBOL = 'none'
MIN_CONF_THRESHOLD = 0.85


class HandController(Controller):

    def __init__(self, artifact: TrainArtifact, logger: log.Logger) -> None:
        self.model = artifact.model
        self.labels = artifact.labels
        self.logger = logger
        self._orientation: Orientation = DEFAULT_ORIENTATION
        self._symbol = DEFAULT_SYMBOL

    @property
    def orientation(self) -> Orientation:
        return self._orientation

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def all_symbols(self) -> list[str]:
        return self.labels

    def handle_sample(self, img: cv2.Mat, results: Result) -> cv2.Mat:
        self._reset()

        if not results.multi_hand_landmarks:
            return img

        hands = sorted(results.multi_hand_landmarks, key=lambda h: h.landmark[0].x)
        if len(hands) <= 0:
            return img

        if len(hands) == 1:
            left, = hands
            return self._handle_left(img, left)

        right, left, *_ = hands
        img = self._handle_left(img, left)
        return self._handle_right(img, right)

    def _handle_left(self, img: cv2.Mat, left: Any) -> cv2.Mat:
        h, w, *_ = img.shape
        left_index = left.landmark[8]
        left_thumb = left.landmark[4]

        self._orientation = ((left_thumb.x * w, left_thumb.y * h), (left_index.x * w, left_index.y * h))
        cv2.line(img,
                 (int(self._orientation[0][0]), int(self._orientation[0][1])),
                 (int(self._orientation[1][0]), int(self._orientation[1][1])), (255, 0, 0), 2)
        return img

    def _handle_right(self, img: cv2.Mat, right: Any) -> cv2.Mat:
        sample: list[float] = [cast(float, f) for lm in right.landmark for f in [lm.x, lm.y, lm.z]]
        model_output: npt.NDArray[np.float64] = self.model.predict_proba([sample])
        prediction_confs: npt.NDArray[np.float64] = model_output[0]
        prediction_idx = np.argmax(prediction_confs)
        prediction_conf = prediction_confs[prediction_idx]
        prediction_label = self.labels[prediction_idx]

        if (prediction_conf < MIN_CONF_THRESHOLD):
            prediction_label = DEFAULT_SYMBOL
            prediction_conf = 1 - prediction_conf

        cv2.putText(img, prediction_label, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        cv2.putText(img, f"x={prediction_conf:,.2f}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

        self._symbol = prediction_label
        return img

    def _reset(self) -> None:
        self._orientation = DEFAULT_ORIENTATION
        self._symbol = DEFAULT_SYMBOL
