import math
import typing
from dataclasses import dataclass

import cv2

import houndeye.constants
import houndeye.utils
from houndeye.processing import Processor
from houndeye.runner import Alliance
from houndeye.utils import cv2Frame

circles = typing.NewType("circles", list[tuple[int, int, int]])
circles_depth = typing.NewType("circles_depth", list[tuple[int, int, int, int]])


class Processor:
    frame_callback: typing.Callable

    @dataclass
    class ProcessingResult:
        blue_circles: circles | circles_depth
        txb: list[float]
        tyb: list[float]

        red_circles: circles | circles_depth
        txr: list[float]
        tyr: list[float]

    def run(self) -> tuple[ProcessingResult, cv2Frame]:
        raise NotImplementedError

    @classmethod
    def package_data(cls, processing_result: ProcessingResult, alliance: Alliance):
        raise NotImplementedError


class AstraProcessor(Processor):
    frame_callback: typing.Callable[
        [None], tuple[cv2Frame, cv2Frame]
    ]  # a color frame and a depth frame

    @dataclass
    class ProcessingResult:
        blue_circles: circles_depth
        txb: list[float]
        tyb: list[float]
        tdb: list[float]

        red_circles: circles_depth
        txr: list[float]
        tyr: list[float]
        tdr: list[float]

    def __init__(self, frame_callback: typing.Callable) -> None:
        self.frame_callback = frame_callback

    def run(self) -> tuple[ProcessingResult, cv2Frame]:
        """
        Runs processing on the frame (calculates angles and distance information for all blue and red circles)

        Returns:
            a ProcessingResult containing circles, tx, ty, and td
            the unprocessed frame
        """

        color_frame, depth_frame = self.frame_callback()

        blue_mask, red_mask = generate_masks(color_frame)
        blue_circles: circles_depth = find_circles(blue_mask, depth_frame)
        red_circles: circles_depth = find_circles(red_mask, depth_frame)

        txb, tyb = calculate_angles(blue_circles)
        txr, tyr = calculate_angles(red_circles)

        tdb = [d for _, _, _, d in blue_circles]
        tdr = [d for _, _, _, d in red_circles]

        return self.ProcessingResult(
            blue_circles, txb, tyb, tdb, red_circles, txr, tyr, tdr
        ), color_frame

    @classmethod
    def package_data(
        cls, processing_result: ProcessingResult, alliance: Alliance
    ) -> dict[str, list[float | int | bool]]:
        match alliance:
            case Alliance.BLUE:
                tx, ty, td = processing_result.txb, processing_result.tyb, processing_result.tdb
            case Alliance.RED:
                tx, ty, td = processing_result.txr, processing_result.tyb, processing_result.tdr
        
        s = sorted(zip(tx, ty, td), key=lambda x: x[2])  # sorts by distance
        tx, ty, td = zip(*s)
        return {'tx': tx, 'ty': ty, 'td': td}


class j5CreateProcessor(Processor):
    frame_callback: typing.Callable[[None], cv2Frame]  #  only a color frame

    @dataclass
    class ProcessingResult:
        blue_circles: circles_depth
        txb: list[float]
        tyb: list[float]

        red_circles: circles_depth
        txr: list[float]
        tyr: list[float]

    def __init__(self, frame_callback: typing.Callable) -> None:
        self.frame_callback = frame_callback

    def run(self) -> tuple[ProcessingResult, cv2Frame]:
        color_frame = self.frame_callback()

        blue_mask, red_mask = generate_masks(color_frame)
        blue_circles: circles = find_circles(blue_mask)
        red_circles: circles = find_circles(red_mask)

        txb, tyb = calculate_angles(blue_circles)
        txr, tyr = calculate_angles(red_circles)

        return self.ProcessingResult(blue_circles, txb, tyb, red_circles, txr, tyr), color_frame

    @classmethod
    def package_data(
        cls, processing_result: ProcessingResult, alliance: Alliance
    ) -> dict[str, list[float | int | bool]]:
        match alliance:
            case Alliance.BLUE:
                tx, ty = processing_result.txb, processing_result.tyb
                tr = [r for _, _, r in processing_result.blue_circles]
            case Alliance.RED:
                tx, ty = processing_result.txr, processing_result.tyr
                tr = [r for _, _, r in processing_result.red]
        
        s = sorted(zip(tx, ty, tr), key=lambda x: x[2], reverse=True)  # sorts by radius, so circles with the largest radius (biggest) are first
        tx, ty, tr = zip(*s)
        return {'tx': tx, 'ty': ty}


def generate_masks(
    frame: cv2Frame,
) -> tuple[cv2Frame, cv2Frame]:
    """
    Generates a blue and a red mask for a frame and applies GaussianBlur.

    Args:
        frame: a color frame

    Returns:
        a blue mask and a red mask
    """

    frame = cv2.GaussianBlur(frame, (7, 7), sigmaX=1.5, sigmaY=1.5)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blue_mask = cv2.inRange(
        hsv,
        houndeye.constants.Astra.HsvBounds.BLUE_BOUND_L,
        houndeye.constants.Astra.HsvBounds.BLUE_BOUND_U,
    )

    red_mask1 = cv2.inRange(
        hsv,
        houndeye.constants.Astra.HsvBounds.RED_BOUND_L,
        houndeye.constants.Astra.HsvBounds.RED_BOUND_U,
    )
    red_mask2 = cv2.inRange(
        hsv,
        houndeye.constants.Astra.HsvBounds.RED_BOUND_L2,
        houndeye.constants.Astra.HsvBounds.RED_BOUND_U2,
    )
    red_mask = red_mask1 | red_mask2

    return blue_mask, red_mask


def find_circles(
    mask: cv2Frame, depth_frame: cv2Frame | None = None
) -> circles | circles_depth:
    """
    Finds circles given a blurred mask and an optional depth frame.

    Args:
        mask: a blurred mask (typically GaussianBlur) to perform operations on
        depth_frame: a depth frame (must be the same dimensions as the mask))

    Returns:
        circles: a list of tuples of either 3 or 4 ints depending on if a depth frame is provided
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
                < houndeye.constants.CIRCLE_COMPARISON_THRESHOLD
            )
            if contour_area != 0
            else False,
        ]

        if all(circle_validators):
            if depth_frame:
                d = calculate_distance(x, y, depth_frame)
                circles += [(int(x), int(y), int(r), int(d))]
            else:
                circles += [(int(x), int(y), int(r))]

    return circles


def calculate_distance(x: int, y: int, depth_frame: cv2Frame) -> float:
    """
    Calculates the distance a certain circle is from the camera.

    Args:
        x: the x coordinate of the circle in the frame (NOT tx)
        y: the y coordinate of the circle in the frame (NOT ty)
        depth_frame: a depth frame from the Astra

    Returns:
        distance: the distance the ball is from the camera (needs calibration)
    """
    raw_distance = int(depth_frame[int(y), int(x)])
    distance = (
        ((1.80721769144085 * (10 ** -12)) * raw_distance ** 3)
        + ((6.9159950965501 * (10 ** -8)) * raw_distance ** 2)
        + ((3.78266960007055 * (10 ** -3)) * raw_distance)
        + (0.418729798948999)
    )
    return distance


def calculate_angles(
    circles: list[circles | circles_depth],
) -> tuple[list[float], list[float]]:
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

    for x, y, *_ in circles:  # ignoring r and d (if it exists)
        tx += [
            (houndeye.constants.Astra.FOV_H / 2)
            * (x - (houndeye.constants.Astra.RESOLUTION_W / 2))
            / (houndeye.constants.Astra.RESOLUTION_W / 2)
        ]
        ty += [
            (houndeye.constants.Astra.FOV_V / 2)
            * (y - (houndeye.constants.Astra.RESOLUTION_H / 2))
            / (houndeye.constants.Astra.RESOLUTION_H / 2)
        ]
    return tx, ty
