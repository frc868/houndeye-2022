import typing

import cv2
import numpy as np

import frc_vision.constants

cv2Frame = typing.NewType("cv2Frame", np.ndarray)
circles = typing.NewType("circles", list[tuple[int]])


def find_circles(mask):
    """
    Finds circles given a blurred mask.

    Params:
        mask: a BLURRED mask (typically GaussianBlur) to perform operations on

    Returns:
        circles: circles found in the frame

    Raises:
        None
    """

    cnts, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    circles = []
    for c in cnts:
        ((x, y), r) = cv2.minEnclosingCircle(c)

        circle_area = 3.14 * r ** 2
        contour_area = cv2.contourArea(c)

        circle_validators = [
            r > 10,
            (
                (circle_area / contour_area)
                < frc_vision.constants.CIRCLE_COMPARISON_THRESHOLD
            )
            if contour_area != 0
            else False,
        ]

        if all(circle_validators):
            circles += [(int(x), int(y), int(r))]

    return circles
