import json

import numpy as np

CONSTANTS_FILE = "constants.json"


def load_constants():
    with open(CONSTANTS_FILE, "r") as f:
        data = json.load(f)

        ASTRA.HSV_BOUNDS.BLUE_BOUND_L = np.array(data["ASTRA"]["HSV_BOUNDS"]["BLUE_BOUND_L"])
        ASTRA.HSV_BOUNDS.BLUE_BOUND_U = np.array(data["ASTRA"]["HSV_BOUNDS"]["BLUE_BOUND_U"])
        ASTRA.HSV_BOUNDS.RED_BOUND_L = np.array(data["ASTRA"]["HSV_BOUNDS"]["RED_BOUND_L"])
        ASTRA.HSV_BOUNDS.RED_BOUND_U = np.array(data["ASTRA"]["HSV_BOUNDS"]["RED_BOUND_U"])
        ASTRA.HSV_BOUNDS.RED_BOUND_L2 = np.array(
            data["ASTRA"]["HSV_BOUNDS"]["RED_H_L2"]
            + [
                int(ASTRA.HSV_BOUNDS.RED_BOUND_L[1]),
                int(ASTRA.HSV_BOUNDS.RED_BOUND_L[2]),
            ]
        )
        ASTRA.HSV_BOUNDS.RED_BOUND_U2 = np.array(
            data["ASTRA"]["HSV_BOUNDS"]["RED_H_U2"]
            + [
                int(ASTRA.HSV_BOUNDS.RED_BOUND_U[1]),
                int(ASTRA.HSV_BOUNDS.RED_BOUND_U[2]),
            ]
        )
        ASTRA.EXPOSURE = data["ASTRA"]["EXPOSURE"]
        ASTRA.GAIN = data["ASTRA"]["GAIN"]

        CIRCLE_COMPARISON_THRESHOLD = data["CIRCLE_COMPARISON_THRESHOLD"]


def dump_constants():
    with open(CONSTANTS_FILE, "w") as f:
        json.dump(
            {
                "ASTRA": {
                    "HSV_BOUNDS": {
                        "BLUE_BOUND_L": ASTRA.HSV_BOUNDS.BLUE_BOUND_L.tolist(),
                        "BLUE_BOUND_U": ASTRA.HSV_BOUNDS.BLUE_BOUND_U.tolist(),
                        "RED_BOUND_L": ASTRA.HSV_BOUNDS.RED_BOUND_L.tolist(),
                        "RED_BOUND_U": ASTRA.HSV_BOUNDS.RED_BOUND_U.tolist(),
                        "RED_H_L2": [int(ASTRA.HSV_BOUNDS.RED_BOUND_L2[0])],
                        "RED_H_U2": [int(ASTRA.HSV_BOUNDS.RED_BOUND_U2[0])]
                    },
                    "EXPOSURE": ASTRA.EXPOSURE,
                    "GAIN": ASTRA.GAIN
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


class ASTRA:
    RESOLUTION_W = 640
    RESOLUTION_H = 480
    FOV_H = 60
    FOV_V = 49.5
    FPS = 30

    class HSV_BOUNDS:
        BLUE_BOUND_L: np.array # constants.json
        BLUE_BOUND_U: np.array # constants.json

        RED_BOUND_L: np.array # constants.json
        RED_BOUND_U : np.array # constants.json
        RED_BOUND_L2: np.array # constants.json
        RED_BOUND_U2: np.array # constants.json

    EXPOSURE: int # constants.json
    GAIN: int # constants.json


CIRCLE_COMPARISON_THRESHOLD = 1.8
