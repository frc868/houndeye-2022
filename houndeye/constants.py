import json

import numpy as np

CONSTANTS_FILE = "constants.json"


def load_constants():
    with open(CONSTANTS_FILE, "r") as f:
        data = json.load(f)

        Astra.HsvBounds.BLUE_BOUND_L = np.array(
            data["ASTRA"]["HSV_BOUNDS"]["BLUE_BOUND_L"]
        )
        Astra.HsvBounds.BLUE_BOUND_U = np.array(
            data["ASTRA"]["HSV_BOUNDS"]["BLUE_BOUND_U"]
        )
        Astra.HsvBounds.RED_BOUND_L = np.array(
            data["ASTRA"]["HSV_BOUNDS"]["RED_BOUND_L"]
        )
        Astra.HsvBounds.RED_BOUND_U = np.array(
            data["ASTRA"]["HSV_BOUNDS"]["RED_BOUND_U"]
        )
        Astra.HsvBounds.RED_BOUND_L2 = np.array(
            data["ASTRA"]["HSV_BOUNDS"]["RED_H_L2"]
            + [
                int(Astra.HsvBounds.RED_BOUND_L[1]),
                int(Astra.HsvBounds.RED_BOUND_L[2]),
            ]
        )
        Astra.HsvBounds.RED_BOUND_U2 = np.array(
            data["ASTRA"]["HSV_BOUNDS"]["RED_H_U2"]
            + [
                int(Astra.HsvBounds.RED_BOUND_U[1]),
                int(Astra.HsvBounds.RED_BOUND_U[2]),
            ]
        )
        Astra.EXPOSURE = data["ASTRA"]["EXPOSURE"]
        Astra.GAIN = data["ASTRA"]["GAIN"]

        CIRCLE_COMPARISON_THRESHOLD = data["CIRCLE_COMPARISON_THRESHOLD"]


def dump_constants():
    with open(CONSTANTS_FILE, "w") as f:
        json.dump(
            {
                "ASTRA": {
                    "HSV_BOUNDS": {
                        "BLUE_BOUND_L": Astra.HsvBounds.BLUE_BOUND_L.tolist(),
                        "BLUE_BOUND_U": Astra.HsvBounds.BLUE_BOUND_U.tolist(),
                        "RED_BOUND_L": Astra.HsvBounds.RED_BOUND_L.tolist(),
                        "RED_BOUND_U": Astra.HsvBounds.RED_BOUND_U.tolist(),
                        "RED_H_L2": [int(Astra.HsvBounds.RED_BOUND_L2[0])],
                        "RED_H_U2": [int(Astra.HsvBounds.RED_BOUND_U2[0])],
                    },
                    "EXPOSURE": Astra.EXPOSURE,
                    "GAIN": Astra.GAIN,
                },
                "CIRCLE_COMPARISON_THRESHOLD": CIRCLE_COMPARISON_THRESHOLD,
            },
            f,
        )


class Keys:
    CV2_WAIT_KEY = 27  # esc key
    CLIENT_SWITCH_KEY = 120  # x key


class Servers:
    ROBORIO_SERVER_IP = "roborio-868-frc.local"

    RASPI_SERVER_IP = "10.8.68.150"
    RASPI_SERVER_PORT = 9999

    LIMELIGHT_SERVER_IP = "10.8.68.151"
    LIMELIGHT_SERVER_PORT = 5800


class CameraConstants:
    RESOLUTION_W: int
    RESOLUTION_H: int
    FOV_H: float
    FOV_V: float
    FPS: int

    class HsvBounds:
        BLUE_BOUND_L: np.array  # constants.json
        BLUE_BOUND_U: np.array  # constants.json

        RED_BOUND_L: np.array  # constants.json
        RED_BOUND_U: np.array  # constants.json
        RED_BOUND_L2: np.array  # constants.json
        RED_BOUND_U2: np.array  # constants.json


class Astra(CameraConstants):
    RESOLUTION_W: int = 640
    RESOLUTION_H: int = 480
    FOV_H: float = 60
    FOV_V: float = 49.5
    FPS: int = 30
    VIDEO_SCALE: float = 0.25

    EXPOSURE: int  # constants.json
    GAIN: int  # constants.json

    class HsvBounds:
        BLUE_BOUND_L: np.array  # constants.json
        BLUE_BOUND_U: np.array  # constants.json

        RED_BOUND_L: np.array  # constants.json
        RED_BOUND_U: np.array  # constants.json
        RED_BOUND_L2: np.array  # constants.json
        RED_BOUND_U2: np.array  # constants.json


class j5Create(CameraConstants):
    RESOLUTION_W = 640
    RESOLUTION_H = 256
    FOV_H: float = 360
    FOV_V: float = 0  # TODO: figure this out
    FPS = 30
    VIDEO_SCALE: float = 0.25

    TOP_CROP = 412
    BOTTOM_CROP = 668

    class HsvBounds:
        BLUE_BOUND_L: np.array  # constants.json
        BLUE_BOUND_U: np.array  # constants.json

        RED_BOUND_L: np.array  # constants.json
        RED_BOUND_U: np.array  # constants.json
        RED_BOUND_L2: np.array  # constants.json
        RED_BOUND_U2: np.array  # constants.json


CIRCLE_COMPARISON_THRESHOLD = 1.8
