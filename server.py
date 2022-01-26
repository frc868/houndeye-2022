import pickle
import socket
import struct

import cv2

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 9999))
sock.listen(5)


vcap = cv2.VideoCapture(1)


while True:
    client, addr = sock.accept()
    if client:
        while True:
            ret, frame = vcap.read()
            if ret:
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client.sendall(message)
                cv2.imshow("transmit", frame)
            if cv2.waitKey(1) == 27:
                break
