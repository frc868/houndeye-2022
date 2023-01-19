import typing

import numpy as np

cv2Frame = typing.NewType("cv2Frame", np.ndarray)


def zip_networktables_data(tx, ty, td):
    """Add color information and zip data for NetworkTables transmission."""
    if not tx:
        return tx, ty, td
    else:  # code below doesn't work unless there's at least one value
        s = sorted(zip(tx, ty, td), key=lambda x: x[2])  # sorts by distance
        tx, ty, td = zip(*s)
        return tx, ty, td
