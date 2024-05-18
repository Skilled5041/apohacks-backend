import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import time

path = os.path.join(os.path.dirname(__file__), "exported_model/model.tflite")
print(path)

model_path = path

BaseOptions = mp.tasks.BaseOptions
ImageClassifier = mp.tasks.vision.ImageClassifier
ImageClassifierOptions = mp.tasks.vision.ImageClassifierOptions
VisionRunningMode = mp.tasks.vision.RunningMode


def print_result(result, a, b):
    print('ImageClassifierResult result: {}'.format(result))


options = ImageClassifierOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    max_results=5,
    result_callback=print_result
)

import cv2
cap = cv2.VideoCapture(0)

c = 0
with ImageClassifier.create_from_options(options) as classifier:
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        classifier.classify_async(mp_image, timestamp_ms=c)
        c += 1
        cv2.imshow('MediaPipe Classifier', frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

print("Done!")