import pickle
import socket
import struct

import cv2
import numpy as np

import frc_vision.constants

vcap = cv2.VideoCapture("http://limelight.local:5800")

while True:
    ret, frame = vcap.read()

    if ret:
        cv2.imshow("frame", frame)

    if cv2.waitKey(15) == 27:
        break
cv2.destroyAllWindows()
