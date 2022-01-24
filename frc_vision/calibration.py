import cv2

import frc_vision.constants


def initalize_calibrators():
    """
    Check if calibration is on, and if so, enable trackbars.
    """

    cv2.createTrackbar(
        "H min (B)",
        "HSV Calibration",
        frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_L[0],
        179,
        calibrators,
    )
    cv2.createTrackbar(
        "S min (B)",
        "HSV Calibration",
        frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_L[1],
        255,
        calibrators,
    )
    cv2.createTrackbar(
        "V min (B)",
        "HSV Calibration",
        frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_L[2],
        255,
        calibrators,
    )
    cv2.createTrackbar(
        "H max (B)",
        "HSV Calibration",
        frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_U[0],
        179,
        calibrators,
    )
    cv2.createTrackbar(
        "S max (B)",
        "HSV Calibration",
        frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_U[1],
        255,
        calibrators,
    )
    cv2.createTrackbar(
        "V max (B)",
        "HSV Calibration",
        frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_U[2],
        255,
        calibrators,
    )
    cv2.createTrackbar(
        "H min (R)",
        "HSV Calibration",
        frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L[0],
        179,
        calibrators,
    )
    cv2.createTrackbar(
        "S min (R)",
        "HSV Calibration",
        frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L[1],
        255,
        calibrators,
    )
    cv2.createTrackbar(
        "V min (R)",
        "HSV Calibration",
        frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L[2],
        255,
        calibrators,
    )
    cv2.createTrackbar(
        "H max (R)",
        "HSV Calibration",
        frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U[0],
        179,
        calibrators,
    )
    cv2.createTrackbar(
        "S max (R)",
        "HSV Calibration",
        frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U[1],
        255,
        calibrators,
    )
    cv2.createTrackbar(
        "V max (R)",
        "HSV Calibration",
        frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U[2],
        255,
        calibrators,
    )

    cv2.createTrackbar(
        "DP",
        "HoughCircles Calibration",
        frc_vision.constants.HOUGH_CONSTANTS.DP,
        50,
        calibrators,
    )
    cv2.createTrackbar(
        "minDist",
        "HoughCircles Calibration",
        frc_vision.constants.HOUGH_CONSTANTS.MIN_DIST,
        400,
        calibrators,
    )
    cv2.createTrackbar(
        "param1",
        "HoughCircles Calibration",
        frc_vision.constants.HOUGH_CONSTANTS.PARAM1,
        400,
        calibrators,
    )
    cv2.createTrackbar(
        "param2",
        "HoughCircles Calibration",
        frc_vision.constants.HOUGH_CONSTANTS.PARAM2,
        200,
        calibrators,
    )
    cv2.createTrackbar(
        "minRadius",
        "HoughCircles Calibration",
        frc_vision.constants.HOUGH_CONSTANTS.MIN_RADIUS,
        500,
        calibrators,
    )
    cv2.createTrackbar(
        "maxRadius",
        "HoughCircles Calibration",
        frc_vision.constants.HOUGH_CONSTANTS.MAX_RADIUS,
        500,
        calibrators,
    )


def calibrators():
    """
    Set constants to trackbar positions.
    """

    frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_L[0] = cv2.getTrackbarPos(
        "H min (B)", "HSV Calibration"
    )
    frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_L[1] = cv2.getTrackbarPos(
        "S min (B)", "HSV Calibration"
    )
    frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_L[2] = cv2.getTrackbarPos(
        "V min (B)", "HSV Calibration"
    )
    frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_U[0] = cv2.getTrackbarPos(
        "H max (B)", "HSV Calibration"
    )
    frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_U[1] = cv2.getTrackbarPos(
        "S max (B)", "HSV Calibration"
    )
    frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_U[2] = cv2.getTrackbarPos(
        "V max (B)", "HSV Calibration"
    )

    frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L[0] = cv2.getTrackbarPos(
        "H min (R)", "HSV Calibration"
    )
    frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L[1] = cv2.getTrackbarPos(
        "S min (R)", "HSV Calibration"
    )
    frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L[2] = cv2.getTrackbarPos(
        "V min (R)", "HSV Calibration"
    )
    frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U[0] = cv2.getTrackbarPos(
        "H max (R)", "HSV Calibration"
    )
    frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U[1] = cv2.getTrackbarPos(
        "S max (R)", "HSV Calibration"
    )
    frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U[2] = cv2.getTrackbarPos(
        "V max (R)", "HSV Calibration"
    )

    frc_vision.constants.HOUGH_CONSTANTS.DP = (
        cv2.getTrackbarPos("DP", "HoughCircles Calibration") / 10
    )
    frc_vision.constants.HOUGH_CONSTANTS.MIN_DIST = cv2.getTrackbarPos(
        "minDist", "HoughCircles Calibration"
    )
    frc_vision.constants.HOUGH_CONSTANTS.PARAM1 = cv2.getTrackbarPos(
        "param1", "HoughCircles Calibration"
    )
    frc_vision.constants.HOUGH_CONSTANTS.PARAM2 = cv2.getTrackbarPos(
        "param2", "HoughCircles Calibration"
    )
    frc_vision.constants.HOUGH_CONSTANTS.MIN_RADIUS = cv2.getTrackbarPos(
        "minRadius", "HoughCircles Calibration"
    )
    frc_vision.constants.HOUGH_CONSTANTS.MAX_RADIUS = cv2.getTrackbarPos(
        "maxRadius", "HoughCircles Calibration"
    )
