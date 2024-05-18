import cv2
import mediapipe as mp


# Initialize MediaPipe Pose and Drawing utilities
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Open the video file
cap = cv2.VideoCapture(0)


frame_number = 0
csv_data = []

while cap.isOpened():
    ret, frame = cap.read()

    # Convert the frame to RGB
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

        if min(rshoulder.y, lshoulder.y) >= min(rwrist.y, lwrist.y) and min(rshoulder.y, lshoulder.y) >= min(relbow.y, lelbow.y):
            print("IT WORKS")
        print(lwrist.y)
        mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)





    # Display the frame
    cv2.imshow('MediaPipe Pose', frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()