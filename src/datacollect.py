import csv
from typing import TypeAlias, cast

import cv2

from src.videohandle import Result, VideoHandler

Sample: TypeAlias = list[float]


def collect(file_destination: str):

    all_samples: list[Sample] = []

    def handle_sample(img: cv2.Mat, results: Result) -> cv2.Mat:

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # index = hand_landmarks.landmark[8]
                # thumb = hand_landmarks.landmark[4]
                # cv2.putText(img, f"x={index.x:,.2f} y={index.y:,.2f} z={index.z:,.2f}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                # cv2.putText(img, f"x={thumb.x:,.2f} y={thumb.y:,.2f} z={thumb.z:,.2f}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                next_sample: Sample = [cast(float, f) for lm in hand_landmarks.landmark for f in [lm.x, lm.y, lm.z]]
                all_samples.append(next_sample)

                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        return img

    videoHandler = VideoHandler(handle_sample)
    videoHandler.run()

    # write to csv file
    with open(file_destination, 'a', newline='') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerows(all_samples)
