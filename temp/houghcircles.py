import tkinter as tk

root = tk.Tk()
l1 = tk.Label(root, text="HoughCircles Constants")
l1.pack()

dp = 10
minDist = 160
param1 = 100
param2 = 50
minRadius = 75
maxRadius = 0
# color = "red"

# color0 = tk.Scale(
#     root,
#     from_=10,
#     to=50,
#     length=500,
#     orient=tk.HORIZONTAL,
#     command=lambda value: update("color", value),
# )
# color0.pack()

dpS = tk.Scale(
    root,
    from_=10,
    to=50,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("dp", value),
)
dpS.pack()
dpS.set(dp)
minDistS = tk.Scale(
    root,
    from_=1,
    to=300,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("minDist", value),
)
minDistS.pack()
minDistS.set(minDist)
param1S = tk.Scale(
    root,
    from_=1,
    to=200,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("param1", value),
)
param1S.pack()
param1S.set(param1)
param2S = tk.Scale(
    root,
    from_=1,
    to=100,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("param2", value),
)
param2S.pack()
param2S.set(param2)
minRadiusS = tk.Scale(
    root,
    from_=0,
    to=500,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("minRadius", value),
)
minRadiusS.pack()
minRadiusS.set(minRadius)

maxRadiusS = tk.Scale(
    root,
    from_=0,
    to=500,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("maxRadius", value),
)
maxRadiusS.pack()
maxRadiusS.set(maxRadius)


import cv2
import frc_vision.constants
import numpy as np


def update(name, value):
    global dp, minDist, param1, param2, minRadius, maxRadius, color
    print(name, value)
    if name == "color":
        color = "red" if int(value) == 0 else "blue"
    elif name == "dp":
        dp = int(value)
    elif name == "minDist":
        minDist = int(value)
    elif name == "param1":
        param1 = int(value)
    elif name == "param2":
        param2 = int(value)
    elif name == "minRadius":
        minRadius = int(value)
    elif name == "maxRadius":
        maxRadius = int(value)


vcap = cv2.VideoCapture(1)
if not vcap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = vcap.read()

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(
        hsv,
        frc_vision.constants.TEST_BOUND_L,
        frc_vision.constants.TEST_BOUND_U,
    )
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

    gray = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), sigmaX=1.5, sigmaY=1.5)

    ############ Possibility 1 #############
    edge = cv2.Canny(blurred, param1 // 2, param1)
    cv2.imshow("edge", edge)

    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp / 10,
        minDist,
        param1=param1,
        param2=param2,
        # minRadius=minRadius,
        # maxRadius=maxRadius,
    )
    # print(circles)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for (x, y, r) in circles[0, :]:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)

    ############ Possibility 2 #############
    # cnts, hier = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print(cnts)

    # Iterate through contours and filter by the number of vertices
    # if len(cnts) > 0:
    #     c = max(cnts, key=cv2.contourArea)
    #     ((x, y), r) = cv2.minEnclosingCircle(c)
    #     print(x, y, r)
    #     cv2.circle(frame, (int(x), int(y)), int(r), (0, 255, 0), 4)
    # cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)

    root.update()
    root.update_idletasks()
    cv2.imshow("mask", mask)
    cv2.imshow("masked_frame", masked_frame)
    cv2.imshow("frame", frame)

    if cv2.waitKey(20) & 0xFF == ord("q"):
        break


vcap.release()
cv2.destroyAllWindows()
