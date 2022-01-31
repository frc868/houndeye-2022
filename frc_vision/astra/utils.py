import cv2
import numpy as np

import frc_vision.constants
import frc_vision.utils
from frc_vision.utils import circles, cv2Frame


def generate_masks(
    frame: cv2Frame,
) -> tuple[cv2Frame, cv2Frame]:
    """
    Generates a blue and a red mask for a frame.
    (applies GaussianBlur at the start)

    Params:
        frame: a raw frame from Astra

    Returns:
        blue_mask
        red_mask

    Raises:
        None
    """
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


def find_circles(mask: cv2Frame, depth_frame: cv2Frame) -> circles:
    """
    Finds circles given a blurred mask.

    Params:
        mask: a BLURRED mask (typically GaussianBlur) to perform operations on
        depth_frame: a depth frame from the Astra

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
            d = calculate_distance(x, y, r, depth_frame)
            circles += [(int(x), int(y), int(r), int(d))]

    return circles


def calculate_distance(x: int, y: int, r: int, depth_frame: cv2Frame) -> float:
    """
    Calculates the distance a certain circle is from the camera.

    Params:
        x: the x coordinate of the circle in the frame (NOT tx)
        y: the y coordinate of the circle in the frame (NOT ty)
        r: the radius of the circle
        depth_frame: a depth frame from the Astra

    Returns:
        distance: the distance the ball is from the camera (needs calibration)

    Raises:
        None

    """
    # roi_margin = int(
    #     r * 0.20
    # )  # can be adjusted to reflect the portion of the ball to test
    # x1 = int(max(0, x - roi_margin))
    # x2 = int(min(frc_vision.constants.ASTRA.RESOLUTION_W - 1, x + roi_margin))
    # y1 = int(max(0, y - roi_margin))
    # y2 = int(min(frc_vision.constants.ASTRA.RESOLUTION_H - 1, y + roi_margin))
    # roi = depth_frame[y1:y2, x1:x2]
    # distance = np.average(roi)
    raw_distance = depth_frame[int(y), int(x)]
    # print(raw_distance)
    # distance = ((raw_distance - 1007.239)/192.461)
    # distance = ((raw_distance - 1973.467)/164.713)
    distance = (
        ((1.80721769144 * (10**-12)) * raw_distance**3) +
        ((6.91599509655 * (10**-8)) * raw_distance**2) +
        ((3.7826696 * (10**-3)) * raw_distance) +
        (0.418729798948999)
    )
    return distance


def calculate_angles(circles: circles):
    """
    Calculates x and y deviation from center of camera feed.

    Params:
        circles: circles returned from `find_circles`

    Returns:
        tx: the x degree offset from the center of the frame
        ty: the y degree offset from the center of the frame

    Raises:
        None
    """
    tx = []
    ty = []
    for x, y, r, d in circles:
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


def zip_networktables_data(txb, tyb, txr, tyr, tdb, tdr):
    """Add color information and zip data for NetworkTables transmission."""
    color = ["B" for x in txb] + ["R" for x in txr]
    tx = txb + txr
    ty = tyb + tyr
    td = tdb + tdr
    return color, tx, ty, td
