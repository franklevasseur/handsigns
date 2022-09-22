import pickle

import cv2
import sklearn.svm as svm

from src.videohandle import Result, VideoHandler


def predict(model_path: str):

    with open(model_path, 'rb') as f:
        model: svm.SVC = pickle.load(f)

    def handle_sample(img: cv2.Mat, results: Result) -> cv2.Mat:

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for id, lm in enumerate(hand_landmarks.landmark):
                    prediction = model.predict([lm.x, lm.y, lm.z])
                    cv2.putText(img, prediction[0], (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return img

    videoHandler = VideoHandler(handle_sample)
    videoHandler.run()
