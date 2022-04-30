import math

import cv2

import frc_vision.constants
import frc_vision.utils
from frc_vision.utils import circles, cv2Frame


def generate_masks(
    frame: cv2Frame,
) -> tuple[cv2Frame, cv2Frame]:
    """
    Generates a blue and a red mask for a frame.
    (applies GaussianBlur at the start)

    Args:
        frame: a raw frame from Astra

    Returns:
        a blue mask and a red mask
    """

    frame = cv2.GaussianBlur(frame, (7, 7), sigmaX=1.5, sigmaY=1.5)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blue_mask = cv2.inRange(
        hsv,
        frc_vision.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_L,
        frc_vision.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_U,
    )

    red_mask1 = cv2.inRange(
        hsv,
        frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L,
        frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U,
    )
    red_mask2 = cv2.inRange(
        hsv,
        frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L2,
        frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U2,
    )
    red_mask = red_mask1 | red_mask2

    return blue_mask, red_mask


def find_circles(mask: cv2Frame, depth_frame: cv2Frame) -> circles:
    """
    Finds circles given a blurred mask.

    Args:
        mask: a BLURRED mask (typically GaussianBlur) to perform operations on
        depth_frame: a depth frame from the Astra

    Returns:
        circles: circles found in the frame
    """

    cnts, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    circles = []
    for c in cnts:
        ((x, y), r) = cv2.minEnclosingCircle(c)

        circle_area = math.pi * r ** 2
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

    Args:
        x: the x coordinate of the circle in the frame (NOT tx)
        y: the y coordinate of the circle in the frame (NOT ty)
        r: the radius of the circle
        depth_frame: a depth frame from the Astra

    Returns:
        distance: the distance the ball is from the camera (needs calibration)
    """
    raw_distance = depth_frame[int(y), int(x)]
    raw_distance = int(raw_distance)
    distance = (
        ((1.80721769144085 * (10 ** -12)) * raw_distance ** 3)
        + ((6.9159950965501 * (10 ** -8)) * raw_distance ** 2)
        + ((3.78266960007055 * (10 ** -3)) * raw_distance)
        + (0.418729798948999)
    )
    return distance


def calculate_angles(circles: circles):
    """
    Calculates x and y deviation from center of camera feed.

    Args:
        circles: circles returned from `find_circles`

    Returns:
        tx: the x degree offset from the center of the frame
        ty: the y degree offset from the center of the frame
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


def zip_networktables_data(tx, ty, td):
    """Add color information and zip data for NetworkTables transmission."""
    if not tx:
        return tx, ty, td
    else:  # code below doesn't work unless there's at least one value
        s = sorted(zip(tx, ty, td), key=lambda x: x[2])  # sorts by distance
        tx, ty, td = zip(*s)
        return tx, ty, td
