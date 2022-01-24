import cv2
import time

capture = cv2.VideoCapture("lib/testing_video/blue1.avi")

while capture.isOpened():
    _, frame = capture.read()
    # print(_)
    # if _:
    cv2.imshow("frame", frame)
    if cv2.waitKey(15) == 27:
        cv2.destroyAllWindows()
