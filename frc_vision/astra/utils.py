import cv2
import frc_vision.constants
import frc_vision.utils
import numpy as np


def generate_masks(
    frame: frc_vision.utils.cv2Frame,
) -> tuple[frc_vision.utils.cv2Frame, frc_vision.utils.cv2Frame]:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blue_mask = cv2.inRange(
        hsv,
        frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_L,
        frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_U,
    )

    red_mask1 = cv2.inRange(
        hsv,
        frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L,  # TODO: generate these values
        frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U,
    )
    red_mask2 = cv2.inRange(
        hsv,
        frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L2,
        frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U2,
    )
    red_mask = red_mask1 | red_mask2

    return blue_mask, red_mask


def calculate_angles(circles):
    circles = np.uint16(np.around(circles))

    for x, y, r in circles[0, :]:
        tx = (
            (frc_vision.constants.ASTRA.FOV_H / 2)
            * (x - (frc_vision.constants.ASTRA.RESOLUTION_W / 2))
            / (frc_vision.constants.ASTRA.RESOLUTION_W / 2)
        )
        ty = (
            (frc_vision.constants.ASTRA.FOV_V / 2)
            * (y - (frc_vision.constants.ASTRA.RESOLUTION_H / 2))
            / (frc_vision.constants.ASTRA.RESOLUTION_H / 2)
        )
    return tx, ty
