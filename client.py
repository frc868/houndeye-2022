import pickle
import socket
import struct
import threading

import cv2
import numpy as np

import frc_vision.constants

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((frc_vision.constants.SERVER_IP, frc_vision.constants.SERVER_PORT))

vcap = cv2.VideoCapture("http://limelight.local:5800")

aframe = None
lframe = None


def read_astra():
    global aframe
    data = b""
    payload_size = struct.calcsize("Q")
    while True:

        # Receive size of data
        while len(data) < payload_size:
            packet = sock.recv(4096)
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        # data = data[payload_size:]

        # Recieve all incoming frame data
        # data = data[payload_size:]
        while len(data) < msg_size:
            data += sock.recv(4096)

        # Cut off everything after the size of the data (in case extra data was transmitted)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Load data into openCV
        frame = pickle.loads(frame_data)
        aframe = cv2.resize(frame, (800, 500))


def read_limelight():
    global lframe
    while True:
        ret, lframe = vcap.read()
        lframe = cv2.resize(lframe, (800, 500))


t1 = threading.Thread(target=read_astra)
t2 = threading.Thread(target=read_limelight)

t1.start()
t2.start()

view_limelight = False
while True:
    key = cv2.waitKey(15)
    if key == 120:
        view_limelight = not view_limelight
    if key == 27:  # esc
        break
    elif view_limelight:  # x
        cv2.imshow("receive", lframe)
    else:
        cv2.imshow("receive", aframe)
