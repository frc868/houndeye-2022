import cv2
import frc_vision.hopper.utils
import numpy as np
import time


class Viewer:
    def __init__(self):
        pass

    def view(self, frame, circles, start_time, in_hopper: list):
        frame = self.draw_circles(frame, circles)
        frame = self.draw_metrics(frame, start_time, in_hopper)
        cv2.imshow("frame", frame)
        mask = frc_vision.hopper.utils._generate_test_mask(frame)
        masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow("masked_frame", masked_frame)

    def draw_circles(self, frame, circles):
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for (x, y, r) in circles[0, :]:
                cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)
        return frame

    def draw_metrics(self, frame, start_time: float, in_hopper: list):
        cv2.putText(
            frame,
            f"fps: {round(1.0 / (time.time() - start_time), 2)}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
        )
        cv2.putText(
            frame,
            str(in_hopper),
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
        )
        return frame
