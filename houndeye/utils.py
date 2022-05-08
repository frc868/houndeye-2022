import typing

import numpy as np

cv2Frame = typing.NewType("cv2Frame", np.ndarray)
circles = typing.NewType("circles", list[tuple[int]])
