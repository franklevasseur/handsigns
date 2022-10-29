from typing import Any, Callable, Protocol, TypeAlias

import cv2
import mediapipe as mp


class Result(Protocol):
    multi_hand_landmarks: list[Any]


Callback: TypeAlias = Callable[[cv2.Mat, Result], cv2.Mat]


class VideoHandler:

    def __init__(self, cb: Callback) -> None:
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands  # type: ignore
        self.hands = self.mp_hands.Hands()
        self.mp_draw = mp.solutions.drawing_utils  # type: ignore
        self.cb = cb

        self.killed = False

        # Check if the webcam is opened correctly
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")

    def kill(self) -> None:
        self.killed = True

    def run(self) -> None:
        while not self.killed:
            success, img = self.cap.read()
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(imgRGB)
            new_img = self.cb(img, results)

            cv2.imshow('Input', new_img)

            c = cv2.waitKey(1)
            if c == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()
