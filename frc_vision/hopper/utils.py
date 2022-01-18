import numpy as np
import cv2
import time
import frc_vision.constants


class cv2Frame(np.ndarray):
    pass


def generate_masks(frame):
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

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

    blue_mask = cv2.inRange(
        hsv,
        frc_vision.constants.HSV_BOUNDS.WEBCAM.BLUE_BOUND_L,
        frc_vision.constants.HSV_BOUNDS.WEBCAM.BLUE_BOUND_U,
    )
    return red_mask, blue_mask


def _generate_test_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(
        hsv,
        frc_vision.constants.HSV_BOUNDS.WEBCAM.BLUE_BOUND_L,
        frc_vision.constants.HSV_BOUNDS.WEBCAM.BLUE_BOUND_U,
    )
    return mask


def find_circles(frame):
    mask = frc_vision.hopper.utils._generate_test_mask(frame)
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

    gray = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), sigmaX=1.5, sigmaY=1.5)

    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        frc_vision.constants.HOUGH_CONSTANTS.DP,
        frc_vision.constants.HOUGH_CONSTANTS.MIN_DIST,
        param1=frc_vision.constants.HOUGH_CONSTANTS.PARAM1,
        param2=frc_vision.constants.HOUGH_CONSTANTS.PARAM2,
        minRadius=frc_vision.constants.HOUGH_CONSTANTS.MIN_RADIUS,
        maxRadius=frc_vision.constants.HOUGH_CONSTANTS.MAX_RADIUS,
    )
    return circles


def draw_circles(frame):
    circles = find_circles(frame)
    if circles is not None:
        circles = np.uint16(np.around(circles))

        for (x, y, r) in circles[0, :]:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)
    return frame
