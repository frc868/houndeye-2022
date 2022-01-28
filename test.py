import cv2

vcap = cv2.VideoCapture("http://limelight.local:5800")

while True:
    ret, frame = vcap.read()

    if ret:
        cv2.imshow("frame", frame)

    print(cv2.waitKey(15))


cv2.destroyAllWindows()
