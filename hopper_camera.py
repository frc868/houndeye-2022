from networktables import NetworkTables
import cv2
import gamepiece_detection.constants
import numpy as np
import tkinter as tk

# NetworkTables.initialize(server=gamepiece_detection.constants.ROBORIO_SERVER)
# sd = NetworkTables.getTable("SmartDashboard")


in_hopper = []
switch_flag = False
shoot_flag = False

vcap = cv2.VideoCapture(0)
if not vcap.isOpened():
    print("Cannot open camera")
    exit()


def switchCallBack():
    global switch_flag
    switch_flag = True


def shootCallBack():
    global shoot_flag
    shoot_flag = True


root = tk.Tk()
b = tk.Button(root, text="Enable Switch", command=switchCallBack)
b.pack()

b2 = tk.Button(root, text="Shoot Ball", command=shootCallBack)
b2.pack()


while True:
    ret, frame = vcap.read()

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    red_mask1 = cv2.inRange(
        hsv,
        gamepiece_detection.constants.RED_BOUND_L,
        gamepiece_detection.constants.RED_BOUND_U,
    )
    red_mask2 = cv2.inRange(
        hsv,
        gamepiece_detection.constants.RED_BOUND_L2,
        gamepiece_detection.constants.RED_BOUND_U2,
    )
    red_mask = red_mask1 | red_mask2

    blue_mask = cv2.inRange(
        hsv,
        gamepiece_detection.constants.BLUE_BOUND_L,
        gamepiece_detection.constants.BLUE_BOUND_U,
    )
    if switch_flag:
        if np.sum(red_mask) > np.sum(blue_mask):
            in_hopper.append("red")
        else:
            in_hopper.append("blue")
        switch_flag = False
    if shoot_flag:
        if in_hopper != []:
            in_hopper.pop(0)
        shoot_flag = False

    print(in_hopper)
    cv2.imshow("red", red_mask)
    cv2.imshow("blue", blue_mask)
    cv2.imshow("frame", frame)
    root.update()
    root.update_idletasks()


vcap.release()
cv2.destroyAllWindows()
