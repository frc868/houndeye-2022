from ast import List
import json

import numpy as np

CONSTANTS_FILE = "constants.json"


def load_constants():
    with open(CONSTANTS_FILE, "r") as f:
        data = json.load(f)
        print(data["HSV_BOUNDS"]["BLUE_BOUND_L"])

        HSV_BOUNDS.ASTRA.BLUE_BOUND_L = np.array(data["HSV_BOUNDS"]["BLUE_BOUND_L"])
        HSV_BOUNDS.ASTRA.BLUE_BOUND_U = np.array(data["HSV_BOUNDS"]["BLUE_BOUND_U"])
        HSV_BOUNDS.ASTRA.RED_BOUND_L = np.array(data["HSV_BOUNDS"]["RED_BOUND_L"])
        HSV_BOUNDS.ASTRA.RED_BOUND_U = np.array(data["HSV_BOUNDS"]["RED_BOUND_U"])
        HSV_BOUNDS.ASTRA.RED_BOUND_L2 = np.array(
            data["HSV_BOUNDS"]["RED_H_L2"] + [int(HSV_BOUNDS.ASTRA.RED_BOUND_L[1]), int(HSV_BOUNDS.ASTRA.RED_BOUND_L[2])]
        )
        HSV_BOUNDS.ASTRA.RED_BOUND_U2 = np.array(
            data["HSV_BOUNDS"]["RED_H_U2"] + [int(HSV_BOUNDS.ASTRA.RED_BOUND_U[1]), int(HSV_BOUNDS.ASTRA.RED_BOUND_U[2])]
        )
        CIRCLE_COMPARISON_THRESHOLD = data["CIRCLE_COMPARISON_THRESHOLD"]


def dump_constants():
    with open(CONSTANTS_FILE, "w") as f:
        json.dump(
            {
                "HSV_BOUNDS": {
                    "BLUE_BOUND_L": [HSV_BOUNDS.ASTRA.BLUE_BOUND_L.tolist()],
                    "BLUE_BOUND_U": [HSV_BOUNDS.ASTRA.BLUE_BOUND_U.tolist()],
                    "RED_BOUND_L": [HSV_BOUNDS.ASTRA.RED_BOUND_L.tolist()],
                    "RED_BOUND_U": [HSV_BOUNDS.ASTRA.RED_BOUND_U.tolist()],
                    "RED_H_L2": [HSV_BOUNDS.ASTRA.RED_BOUND_L2[0]],
                    "RED_H_U2": [HSV_BOUNDS.ASTRA.RED_BOUND_U2[0]],
                },
                "CIRCLE_COMPARISON_THRESHOLD": CIRCLE_COMPARISON_THRESHOLD,
            },
            f,
        )


class KEYS:
    CV2_WAIT_KEY = 27  # esc key
    CLIENT_SWITCH_KEY = 120  # x key


class SERVERS:
    ROBORIO_SERVER_IP = "roborio-868-frc.local"

    RASPI_SERVER_IP = "10.8.68.150"
    RASPI_SERVER_PORT = 9999

    LIMELIGHT_SERVER_IP = "10.8.68.151"
    LIMELIGHT_SERVER_PORT = 5800


class HSV_BOUNDS:
    class ASTRA:
        BLUE_BOUND_L = np.array(
            [98, 116, 59]
        )  # lower bound for blue ball, in format [H, S, V]
        BLUE_BOUND_U = np.array(
            [121, 223, 255]
        )  # upper bound for blue ball, in format [H, S, V]

        RED_BOUND_L = np.array(
            [169, 83, 0]
        )  # lower bound for the first red ball mask, in format [H, S, V]
        RED_BOUND_U = np.array(
            [179, 250, 255]
        )  # upper bound for first red ball mask, in format [H, S, V]
        RED_BOUND_L2 = np.array(
            [0, RED_BOUND_L[1], RED_BOUND_L[2]]
        )  # lower bound for second red ball mask, in format [H, S, V]
        RED_BOUND_U2 = np.array(
            [20, RED_BOUND_U[1], RED_BOUND_U[2]]
        )  # upper bound for second red ball mask, in format [H, S, V]


class ASTRA:
    RESOLUTION_W = 640
    RESOLUTION_H = 480
    FOV_H = 60
    FOV_V = 49.5
    FPS = 30


class HOUGH_CONSTANTS:
    DP = 1.8  # Inverse ratio of the accumulator resolution to the image resolution. TODO: Do more research on what this value does.
    MIN_DIST = 100  # Minimum distance between each circle center
    PARAM1 = 200  # Higher of two variables passed to Canny edge detector, second is half of this
    PARAM2 = 55  # Passed to HoughCircles. The smaller it is, the more false circles there are, and vice versa.
    MIN_RADIUS = 0  # Minimum radius of detected circle. TODO: Calibrate to gamepiece.
    MAX_RADIUS = 0  # Maximum radius of detected circle. TODO: Calibrate to gamepiece.


CIRCLE_COMPARISON_THRESHOLD = 1.8
