import time
import typing

import cv2
import numpy as np

import frc_vision.astra.utils
import frc_vision.utils


class ViewerFrame:
    frame: frc_vision.utils.cv2Frame
    name: str
    show_data: bool

    def __init__(
        self, frame: frc_vision.utils.cv2Frame, name: str, show_data: bool = False
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
    frame: frc_vision.utils.cv2Frame, blue_circles, red_circles
) -> frc_vision.utils.cv2Frame:
    """
    Draw circles on a given frame, along with distance information

    Params:
        frame: the frame to draw circles on
        blue_circles: blue circles generated from `find_circles`
        red_circles: red circles generated from `find_circles`

    Returns:
        frame: the frame with circles drawn on it

    Raises:
        None
    """

    if blue_circles is not None:
        for (x, y, r, d) in blue_circles:
            cv2.circle(frame, (x, y), r, (255, 0, 0), 4)
            cv2.circle(frame, (x, y), 2, (0, 255, 0), 3)
            cv2.putText(
                frame, str(d), (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255)
            )

    if red_circles is not None:
        for (x, y, r, d) in red_circles:
            cv2.circle(frame, (x, y), r, (0, 0, 255), 4)
            cv2.circle(frame, (x, y), 2, (0, 255, 0), 3)
            cv2.putText(
                frame, str(d), (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0)
            )

    return frame


def draw_metrics(
    frame, start_time: float, data: tuple[ViewerData] = []
) -> frc_vision.utils.cv2Frame:
    """Draws metrics to the frame. Also draws FPS."""
    data = [ViewerData("FPS", round(1.0 / (time.time() - start_time), 2))] + data
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
            frame = draw_circles(frame, circles[0], circles[1])
            frame = draw_metrics(frame, start_time, data)
        cv2.imshow(vframe.name, frame)
