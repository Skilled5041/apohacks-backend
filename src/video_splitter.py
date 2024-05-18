import cv2
import os

filename = os.path.join(os.path.dirname(__file__), "../dataset/IMG_2534.avi")
print(filename)
assert os.path.exists(filename)
vidcap = cv2.VideoCapture(filename)
success = True
count = 0
while success:
    success, image = vidcap.read()
    cv2.imwrite(f"../dataset/zombie/filedddd{count}{count}{count}.jpg", image)
    print(f"Reading a new frame: {success}")
    count += 1
    if cv2.waitKey(1) & 0xff == ord('q'):
        break