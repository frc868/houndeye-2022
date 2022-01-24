import threading
import time
import tkinter as tk

import cv2
import networktables
import numpy as np

import frc_vision.constants

vcap = cv2.VideoCapture(frc_vision.constants.VIEWER_ID)
if not vcap.isOpened():
    print("Cannot open camera")
    exit()

root = tk.Tk()
l1 = tk.Label(root, text="HSV Lower Bound")
l1.pack()
h1 = tk.Scale(
    root,
    from_=0,
    to=255,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("h1", value),
)
h1.pack()
h1.set(frc_vision.constants.HSV_BOUNDS.WEBCAM.BLUE_BOUND_L[0])

s1 = tk.Scale(
    root,
    from_=0,
    to=255,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("s1", value),
)
s1.pack()
s1.set(frc_vision.constants.HSV_BOUNDS.WEBCAM.BLUE_BOUND_L[1])

v1 = tk.Scale(
    root,
    from_=0,
    to=255,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("v1", value),
)
v1.pack()
v1.set(frc_vision.constants.HSV_BOUNDS.WEBCAM.BLUE_BOUND_L[2])


l2 = tk.Label(root, text="HSV Upper Bound")
l2.pack()
h2 = tk.Scale(
    root,
    from_=0,
    to=255,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("h2", value),
)
h2.pack()
h2.set(frc_vision.constants.HSV_BOUNDS.WEBCAM.BLUE_BOUND_U[0])

s2 = tk.Scale(
    root,
    from_=0,
    to=255,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("s2", value),
)
s2.pack()
s2.set(frc_vision.constants.HSV_BOUNDS.WEBCAM.BLUE_BOUND_U[1])

v2 = tk.Scale(
    root,
    from_=0,
    to=255,
    length=500,
    orient=tk.HORIZONTAL,
    command=lambda value: update("v2", value),
)
v2.pack()
v2.set(frc_vision.constants.HSV_BOUNDS.WEBCAM.BLUE_BOUND_U[2])


lower_range = np.array([0, 0, 0])
upper_range = np.array([0, 0, 0])


def update(name, value):
    if name == "h1":
        lower_range[0] = value
    elif name == "s1":
        lower_range[1] = value
    elif name == "v1":
        lower_range[2] = value
    elif name == "h2":
        upper_range[0] = value
    elif name == "s2":
        upper_range[1] = value
    elif name == "v2":
        upper_range[2] = value


while True:
    ret, frame = vcap.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(
        hsv,
        lower_range,
        upper_range,
    )
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("masked_frame_old", masked_frame)

    cv2.erode(masked_frame, (5, 5), iterations=10)
    cv2.dilate(masked_frame, (5, 5), iterations=10)
    cv2.imshow("mask_frame", masked_frame)

    cv2.imshow("feed", frame)
    # cv2.imshow("mask", masked_frame)

    root.update()
    root.update_idletasks()
    if cv2.waitKey(20) & 0xFF == ord("q"):
        break

vcap.release()
cv2.destroyAllWindows()
