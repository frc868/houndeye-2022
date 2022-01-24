import numpy as np

ROBORIO_SERVER = "roborio-868-frc.local"
CV2_WAIT_KEY = 27  # esc key


class HSV_BOUNDS:
    class ASTRA:
        pass

    class WEBCAM:
        BLUE_BOUND_L = np.array(
            [98, 112, 0]
        )  # lower bound for blue ball, in format [H, S, V]
        BLUE_BOUND_U = np.array(
            [112, 241, 255]
        )  # upper bound for blue ball, in format [H, S, V]

        RED_BOUND_L = np.array(
            [0, 149, 63]
        )  # lower bound for the first red ball mask, in format [H, S, V]
        RED_BOUND_U = np.array(
            [10, 255, 255]
        )  # upper bound for first red ball mask, in format [H, S, V]
        RED_BOUND_L2 = np.array(
            [171, 149, 63]
        )  # lower bound for second red ball mask, in format [H, S, V]
        RED_BOUND_U2 = np.array(
            [179, 255, 255]
        )  # upper bound for second red ball mask, in format [H, S, V]

    TEST_BOUND_L = np.array([9, 141, 0])  # temp
    TEST_BOUND_U = np.array([21, 248, 255])  # temp


class ASTRA:
    RESOLUTION_W = 640
    RESOLUTION_H = 480
    FOV_H = 60
    FOV_V = 49.5
    FPS = 30


TEST_BOUND_L = np.array([9, 141, 0])
TEST_BOUND_U = np.array([21, 248, 255])


class HOUGH_CONSTANTS:
    DP = 1.8  # Inverse ratio of the accumulator resolution to the image resolution. TODO: Do more research on what this value does.
    MIN_DIST = 100  # Minimum distance between each circle center
    PARAM1 = 200  # Higher of two variables passed to Canny edge detector, second is half of this
    PARAM2 = 55  # Passed to HoughCircles. The smaller it is, the more false circles there are, and vice versa.
    MIN_RADIUS = 0  # Minimum radius of detected circle. TODO: Calibrate to gamepiece.
    MAX_RADIUS = 0  # Maximum radius of detected circle. TODO: Calibrate to gamepiece.


VIEWER_ID = (
    0  # TODO: Test on driver station computer. This can also be set to a video file!
)
