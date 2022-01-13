import numpy as np

BLUE_BOUND_L = np.array([98, 112, 0])  # lower bound for blue ball, in format [H, S, V]
BLUE_BOUND_U = np.array(
    [112, 241, 255]
)  # upper bound for blue ball, in format [H, S, V]

RED_BOUND_L = np.array(
    [0, 149, 63]
)  # lower bound for the first red ball mask, in format [H, S, V]
RED_BOUND_U = np.array(
    [10, 255, 255]
)  # upper bound for first red ball mask, in format [H, S, V]

RED_BOUND_L2 = np.array(
    [171, 149, 63]
)  # lower bound for second red ball mask, in format [H, S, V]
RED_BOUND_U2 = np.array(
    [179, 255, 255]
)  # upper bound for second red ball mask, in format [H, S, V]

ROBORIO_SERVER = "roborio-868-frc.local"
