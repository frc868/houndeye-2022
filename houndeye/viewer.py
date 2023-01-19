import time
import typing

import cv2
import numpy as np

import houndeye.utils
from houndeye.processing.cargo_detection import circles, circles_depth


class ViewerFrame:
    frame: houndeye.utils.cv2Frame
    name: str
    show_data: bool

    def __init__(
        self, frame: houndeye.utils.cv2Frame, name: str, show_data: bool = False
    ):
        self.frame = frame
        self.name = name
        self.show_data = show_data


class ViewerData:
    name: str
    value: typing.Any

    def __init__(self, name: str, value: typing.Any):
        self.name = name
        self.value = value


def draw_circles(
    frame: houndeye.utils.cv2Frame,
    blue_circles: circles | circles_depth,
    red_circles: circles | circles_depth,
) -> houndeye.utils.cv2Frame:
    """
    Draw circles on a given frame, along with distance information

    Args:
        frame: the frame to draw circles on
        blue_circles: blue circles generated from `find_circles`
        red_circles: red circles generated from `find_circles`

    Returns:
        frame: the frame with circles drawn on it
    """

    for (x, y, r, d) in blue_circles:
        cv2.circle(frame, (x, y), r, (255, 0, 0), 4)
        cv2.circle(frame, (x, y), 2, (0, 255, 0), 3)
        cv2.putText(frame, str(d), (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))

    for (x, y, r, d) in red_circles:
        cv2.circle(frame, (x, y), r, (0, 0, 255), 4)
        cv2.circle(frame, (x, y), 2, (0, 255, 0), 3)
        cv2.putText(frame, str(d), (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0))

    return frame


def calculate_fps(start_time: float) -> float:
    """Calculates FPS given a start time."""
    return round(1.0 / (time.time() - start_time), 2)


def draw_metrics(
    frame, start_time: float, data: tuple[ViewerData] = ()
) -> houndeye.utils.cv2Frame:
    """Draws metrics to the frame. Also draws FPS."""
    data = (ViewerData("FPS", calculate_fps(start_time)),) + data
    for idx, d in enumerate(data):
        cv2.putText(
            frame,
            f"{d.name}: {d.value}",
            (20, 40 + (30 * (idx))),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 0),
        )
    return frame


def view(
    frames: tuple[ViewerFrame],
    circles: tuple[np.ndarray],
    data: tuple[ViewerData],
    start_time: float,
):
    """
    Displays all given frames, and overlays data on those frames if requested.
    """
    for vframe in frames:
        frame = vframe.frame
        if vframe.show_data:
            blue_circles, red_circles = circles
            frame = draw_circles(frame, blue_circles, red_circles)
            frame = draw_metrics(frame, start_time, data)
        cv2.imshow(vframe.name, frame)
