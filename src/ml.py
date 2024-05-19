import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import time
import cv2
from cv2 import VideoCapture



def main(func, func2):


    def print_result(a, b, d):
        print(a)



    model_path = os.path.join(os.path.dirname(__file__), "exported_model/model.tflite")
    Classifier_BaseOptions = mp.tasks.BaseOptions
    Classifier_ImageClassifier = mp.tasks.vision.ImageClassifier
    Classifier_ImageClassifierOptions = mp.tasks.vision.ImageClassifierOptions
    Classifier_VisionRunningMode = mp.tasks.vision.RunningMode

    Classifier_options = Classifier_ImageClassifierOptions(
        base_options=Classifier_BaseOptions(model_asset_path=model_path),
        running_mode=Classifier_VisionRunningMode.LIVE_STREAM,
        max_results=5,
        result_callback=print_result
    )

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose = mp_pose.Pose()
    cap = VideoCapture(0)

    with Classifier_ImageClassifier.create_from_options(Classifier_options) as classifier:
        c = 0
        while True:
            success, frame = cap.read()
            if not success:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame with MediaPipe Pose
            result = pose.process(frame_rgb)

            # Draw the pose landmarks on the frame
            if result.pose_landmarks:
                """x = [
                    print('x is', data_point.x, 'y is', data_point.y, 'z is', data_point.z,
                          'visibility is', data_point.visibility)
                    for data_point in result.pose_landmarks.landmark
                ]"""

                rwrist = result.pose_landmarks.landmark[16]
                lwrist = result.pose_landmarks.landmark[15]

                rshoulder = result.pose_landmarks.landmark[12]
                lshoulder = result.pose_landmarks.landmark[11]

                relbow = result.pose_landmarks.landmark[14]
                lelbow = result.pose_landmarks.landmark[13]

                if min(rshoulder.y, lshoulder.y) >= min(rwrist.y, lwrist.y) and min(rshoulder.y, lshoulder.y) >= min(
                        relbow.y, lelbow.y):
                    func()
                    print("IT WORKS")
                else:
                    func2()
                print(lwrist.y)
                mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

            classifier.classify_async(mp_image, timestamp_ms=c)
            c += 1
            cv2.imshow('MediaPipe Classifier', frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break








if __name__ == "__main__":
    main(lambda x: print(x), lambda y: print(y))