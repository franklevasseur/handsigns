import pathlib as pl
import pickle
from typing import cast

import cv2
import numpy as np
import numpy.typing as npt

from . import logger as log
from .typings import TrainArtifact
from .videohandle import Result, VideoHandler


def predict(model_path: pl.Path, logger: log.Logger) -> None:
    logger.info(f"Predicting with model {model_path}")

    with open(model_path, 'rb') as f:
        artifact: TrainArtifact = pickle.load(f)
        model = artifact.model
        labels = artifact.labels

    def handle_sample(img: cv2.Mat, results: Result) -> cv2.Mat:

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                sample: list[float] = [cast(float, f) for lm in hand_landmarks.landmark for f in [lm.x, lm.y, lm.z]]
                model_output: npt.NDArray[np.float64] = model.predict_proba([sample])
                prediction_confs: npt.NDArray[np.float64] = model_output[0]
                prediction_idx = np.argmax(prediction_confs)
                prediction_conf = prediction_confs[prediction_idx]
                prediction_label = labels[prediction_idx]

                if (prediction_conf < 0.75):
                    prediction_label = 'none'
                    prediction_conf = 1 - prediction_conf

                cv2.putText(img, prediction_label, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                cv2.putText(img, f"x={prediction_conf:,.2f}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

        return img

    videoHandler = VideoHandler(handle_sample)
    videoHandler.run()
