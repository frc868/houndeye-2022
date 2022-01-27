import pickle
import socket
import struct

import cv2

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("10.8.68.190", 9999))
sock.listen(5)


vcap = cv2.VideoCapture(0)


while True:
    client, addr = sock.accept()
    if client:
        while True:
            ret, frame = vcap.read()
            if ret:
                frame = cv2.resize(frame, (320, 240))
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client.sendall(message)
                cv2.imshow("transmit", frame)
            if cv2.waitKey(15) == 27:
                break
