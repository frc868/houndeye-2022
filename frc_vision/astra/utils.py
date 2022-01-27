import cv2
import numpy as np

import frc_vision.constants
import frc_vision.utils
from frc_vision.utils import circles, cv2Frame


def generate_masks(
    frame: cv2Frame,
) -> tuple[cv2Frame, cv2Frame]:
    frame = cv2.GaussianBlur(frame, (7, 7), sigmaX=1.5, sigmaY=1.5)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blue_mask = cv2.inRange(
        hsv,
        frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_L,
        frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_U,
    )

    red_mask1 = cv2.inRange(
        hsv,
        frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L,
        frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U,
    )
    red_mask2 = cv2.inRange(
        hsv,
        frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L2,
        frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U2,
    )
    red_mask = red_mask1 | red_mask2

    return blue_mask, red_mask


def calculate_angles(circles: circles):
    """Calculates x and y deviation from center of camera feed."""
    tx = []
    ty = []
    for x, y, r in circles:
        tx += [
            (frc_vision.constants.ASTRA.FOV_H / 2)
            * (x - (frc_vision.constants.ASTRA.RESOLUTION_W / 2))
            / (frc_vision.constants.ASTRA.RESOLUTION_W / 2)
        ]
        ty += [
            (frc_vision.constants.ASTRA.FOV_V / 2)
            * (y - (frc_vision.constants.ASTRA.RESOLUTION_H / 2))
            / (frc_vision.constants.ASTRA.RESOLUTION_H / 2)
        ]
    return tx, ty


def calculate_distance(circles: circles, depth_frame: cv2Frame) -> list[float]:
    ta = []
    for x, y, r in circles:
        roi_margin = int(
            r * 0.20
        )  # can be adjusted to reflect the portion of the ball to test
        x1 = max(0, x - roi_margin)
        x2 = min(frc_vision.constants.ASTRA.RESOLUTION_W - 1, x + roi_margin)
        y1 = max(0, y - roi_margin)
        y2 = min(frc_vision.constants.ASTRA.RESOLUTION_H - 1, y + roi_margin)
        roi = depth_frame[y1:y2, x1:x2]

        ta += int(np.average(roi))
    return ta


def zip_networktables_data(txb, tyb, txr, tyr, tab, tar):
    """Add color information and zip data for NetworkTables transmission."""
    color = ["B" for x in txb] + ["R" for x in txr]
    tx = txb + txr
    ty = tyb + tyr
    ta = tab + tar
    return zip(color, tx, ty, ta)
