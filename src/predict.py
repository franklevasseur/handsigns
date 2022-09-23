import pickle
from typing import cast

import cv2
import sklearn.svm as svm

from src.typings import TrainArtifact
from src.videohandle import Result, VideoHandler


def predict(model_path: str):

    with open(model_path, 'rb') as f:
        artifact: TrainArtifact = pickle.load(f)
        model = artifact.model
        labels = artifact.labels

    def handle_sample(img: cv2.Mat, results: Result) -> cv2.Mat:

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                sample: list[float] = [cast(float, f) for lm in hand_landmarks.landmark for f in [lm.x, lm.y, lm.z]]
                model_output = model.predict([sample])
                prediction_int = model_output[0]
                prediction_label = labels[prediction_int]
                cv2.putText(img, prediction_label, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return img

    videoHandler = VideoHandler(handle_sample)
    videoHandler.run()
