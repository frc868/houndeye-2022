import typing

import cv2
import numpy as np

import frc_vision.constants

cv2Frame = typing.NewType("cv2Frame", np.ndarray)
circles = typing.NewType("circles", list[tuple[int]])
