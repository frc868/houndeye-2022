import pickle
import socket
import struct
import threading

import cv2
import numpy as np

import frc_vision.constants

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(
    (
        frc_vision.constants.SERVERS.RASPI_SERVER_IP,
        frc_vision.constants.SERVERS.RASPI_SERVER_PORT,
    )
)

vcap = cv2.VideoCapture(
    f"http://{frc_vision.constants.SERVERS.LIMELIGHT_SERVER_IP}:{frc_vision.constants.SERVERS.LIMELIGHT_SERVER_PORT}"
)


aframe = None
lframe = None
running = True

def read_astra():
    global aframe
    data = b""
    payload_size = struct.calcsize("Q")
    while running:
        # Receive payload with size of data
        while len(data) < payload_size:
            packet = sock.recv(4096)
            if not packet:
                break
            data += packet

        # Unpack the payload and remove it from the actual frame data
        packed_msg_size = data[:payload_size]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        data = data[payload_size:]

        # Recieve the rest of the incoming frame data
        while len(data) < msg_size:
            data += sock.recv(4096)

        # Cut off everything after the size of the data (in case extra data was transmitted)
        frame_data = data[:msg_size]
        # If any additional data was transmitted
        # (the next frame, for instance), this will
        # save that and use it for the next loop.
        data = data[msg_size:]

        # Load data into openCV
        aframe = cv2.resize(pickle.loads(frame_data), (1280, 720))
    return


def read_limelight():
    global lframe
    while running:
        ret, frame = vcap.read()
        if ret:
            lframe = cv2.resize(frame, (1280, 720))
    return


t1 = threading.Thread(target=read_astra)
t2 = threading.Thread(target=read_limelight)

t1.start()
t2.start()

view_front = True
while running:
    key = cv2.waitKey(15)
    if key == frc_vision.constants.KEYS.CLIENT_SWITCH_KEY:
        view_front = not view_front
    if key == frc_vision.constants.KEYS.CV2_WAIT_KEY:  # esc
        running = False

    if view_front:
        cv2.imshow("receive", lframe)
    else:
        cv2.imshow("receive", aframe)

cv2.destroyAllWindows()
