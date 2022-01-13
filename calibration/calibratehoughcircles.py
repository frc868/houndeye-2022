import tkinter as tk

root = tk.Tk()
l1 = tk.Label(root, text="HoughCircles Constants")
l1.pack()

dp = 1
minDist = 160
param1 = 100
param2 = 50
minRadius = 75
maxRadius = 0
color = "red"

color0 = tk.Scale(
    root,
    from_=0,
    to=1,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("color", value),
)
color0.pack()

dp0 = tk.Scale(
    root,
    from_=0,
    to=5,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("dp", value),
)
dp0.pack()
dp0.set(dp)
minDist0 = tk.Scale(
    root,
    from_=100,
    to=300,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("minDist", value),
)
minDist0.pack()
minDist0.set(minDist)
param10 = tk.Scale(
    root,
    from_=0,
    to=200,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("param1", value),
)
param10.pack()
param10.set(param1)
param20 = tk.Scale(
    root,
    from_=0,
    to=100,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("param2", value),
)
param20.pack()
param20.set(param2)
minRadius0 = tk.Scale(
    root,
    from_=0,
    to=500,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("minRadius", value),
)
minRadius0.pack()
minRadius0.set(minRadius)

maxRadius0 = tk.Scale(
    root,
    from_=0,
    to=500,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("maxRadius", value),
)
maxRadius0.pack()
maxRadius0.set(maxRadius)


import cv2
import gamepiece_detection.constants
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


vcap = cv2.VideoCapture(0)
if not vcap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = vcap.read()
    # print(dp, minDist, param1, param2, minRadius, maxRadius)

    # flips the frame horizontally
    frame = cv2.flip(frame, 1)
    # converts to usable openCV code
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # mask = cv2.inRange(
    #     hsv,
    #     gamepiece_detection.constants.BLUE_BOUND_L,
    #     gamepiece_detection.constants.BLUE_BOUND_U,
    # )
    # masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

    mask1 = cv2.inRange(
        hsv,
        gamepiece_detection.constants.RED_BOUND_L,
        gamepiece_detection.constants.RED_BOUND_U,
    )
    mask2 = cv2.inRange(
        hsv,
        gamepiece_detection.constants.RED_BOUND_L2,
        gamepiece_detection.constants.RED_BOUND_U2,
    )
    mask = mask1 | mask2
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

    gray = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 5)

    ############ Possibility 1 #############
    # circles = cv2.HoughCircles(
    #     blurred,
    #     cv2.HOUGH_GRADIENT,
    #     1.5,
    #     minDist,
    #     param1=param1,
    #     param2=param2,
    #     minRadius=minRadius,
    #     maxRadius=maxRadius,
    # )
    # # print(circles)
    # if circles is not None:

    #     circles = np.round(circles[0, :]).astype("int")
    #     for (x, y, r) in circles:
    #         cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
    #         cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)

    ############ Possibility 2 #############
    cnts, hier = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through contours and filter by the number of vertices
    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)
        if len(approx) > 5:
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 8)

    root.update()
    root.update_idletasks()
    cv2.imshow("mask", mask)
    cv2.imshow("gray", gray)
    cv2.imshow("frame", frame)

    if cv2.waitKey(20) & 0xFF == ord("q"):
        break


vcap.release()
cv2.destroyAllWindows()
