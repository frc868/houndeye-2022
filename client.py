import pickle
import socket
import struct

import cv2
import numpy as np

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 9999))

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
    cv2.imshow("receive", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
