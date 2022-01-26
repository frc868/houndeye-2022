import cv2
import numpy as np

import frc_vision.constants
import frc_vision.utils


def generate_masks(
    frame: frc_vision.utils.cv2Frame,
) -> tuple[frc_vision.utils.cv2Frame, frc_vision.utils.cv2Frame]:

    frame = cv2.GaussianBlur(frame, (7, 7), sigmaX=1.5, sigmaY=1.5)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blue_mask = cv2.inRange(
        hsv,
        frc_vision.constants.HSV_BOUNDS.WEBCAM.BLUE_BOUND_L,
        frc_vision.constants.HSV_BOUNDS.WEBCAM.BLUE_BOUND_U,
    )

    red_mask1 = cv2.inRange(
        hsv,
        frc_vision.constants.HSV_BOUNDS.WEBCAM.RED_BOUND_L,
        frc_vision.constants.HSV_BOUNDS.WEBCAM.RED_BOUND_U,
    )
    red_mask2 = cv2.inRange(
        hsv,
        frc_vision.constants.HSV_BOUNDS.WEBCAM.RED_BOUND_L2,
        frc_vision.constants.HSV_BOUNDS.WEBCAM.RED_BOUND_U2,
    )
    red_mask = red_mask1 | red_mask2

    return blue_mask, red_mask
