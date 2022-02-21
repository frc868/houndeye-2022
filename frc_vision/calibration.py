import tkinter as tk

import frc_vision.constants

"""
Certain code is intentionally all on one line
to make it easier to debug (ignoring style guide).
Black formatter has not been applied to this file.
"""

# fmt: off

def create_scale(from_, to, key, original_value):
    """Lessens code length in `initialize_calibrators`."""
    s = tk.Scale(
        root,
        from_=from_,
        to=to,
        length=500,
        orient=tk.HORIZONTAL,
        command=lambda value: calibrators(key, value),
    )
    s.pack()
    s.set(original_value)

def create_label(name):
    """Lessens code length in `initialize_calibrators`."""
    l = tk.Label(
        root,
        text=name
    )
    l.pack()

def initalize_calibrators():
    """
    Check if calibration is on, and if so, enable trackbars.
    """
    global root

    root = tk.Tk()

    create_label("HSV Lower Bound (B)")
    create_scale(0, 179, "HLB", frc_vision.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_L[0])
    create_scale(0, 255, "SLB", frc_vision.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_L[1])
    create_scale(0, 255, "VLB", frc_vision.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_L[2])
    
    create_label("HSV Upper Bound (B)")
    create_scale(0, 179, "HUB", frc_vision.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_U[0])
    create_scale(0, 255, "SUB", frc_vision.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_U[1])
    create_scale(0, 255, "VUB", frc_vision.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_U[2])
    
    create_label("HSV Lower Bound (R)")
    create_scale(0, 179, "HLR", frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L[0])
    create_scale(0, 255, "SLR", frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L[1])
    create_scale(0, 255, "VLR", frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L[2])
    
    create_label("HSV Upper Bound (R)")
    create_scale(0, 179, "HUR", frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U[0])
    create_scale(0, 255, "SUR", frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U[1])
    create_scale(0, 255, "VUR", frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U[2])

    create_label("HSV Bound (R2)")
    create_scale(0, 179, "HLR2", frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L2[0])    
    create_scale(0, 179, "HUR2", frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U2[0])

    create_label("Circle Comparison Threshold")
    create_scale(50, 300, "Circle", int(frc_vision.constants.CIRCLE_COMPARISON_THRESHOLD*100))

    b = tk.Button(root, text="Save constants to file", command=frc_vision.constants.dump_constants)
    b.pack()
        
    create_label("Exposure")
    create_scale(0, 500, "exp", frc_vision.constants.ASTRA.EXPOSURE)

    create_label("Gain")
    create_scale(0, 500, "gain", frc_vision.constants.ASTRA.GAIN)



def calibrators(key: str, value: str):
    """
    Set constants to trackbar positions.
    """
    if key == "HLB": frc_vision.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_L[0] = int(value)
    if key == "SLB": frc_vision.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_L[1] = int(value)
    if key == "VLB": frc_vision.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_L[2] = int(value)
    if key == "HUB": frc_vision.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_U[0] = int(value)
    if key == "SUB": frc_vision.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_U[1] = int(value)
    if key == "VUB": frc_vision.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_U[2] = int(value)
    if key == "HLR": frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L[0] = int(value)
    if key == "SLR": frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L[1] = frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L2[1] = int(value)
    if key == "VLR": frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L[2] = frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L2[2] = int(value)
    if key == "HUR": frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U[0] = int(value)
    if key == "SUR": frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U[1] = frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U2[1] = int(value)
    if key == "VUR": frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U[2] = frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U2[2] = int(value)
    if key == "HLR2": frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L2[0] = int(value)
    if key == "HUR2": frc_vision.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U2[0] = int(value)

    if key == "Circle": frc_vision.constants.CIRCLE_COMPARISON_THRESHOLD = int(value)/100
    if key == "exp": frc_vision.constants.ASTRA.EXPOSURE = int(value)
    if key == "gain": frc_vision.constants.ASTRA.GAIN = int(value)


def update_calibrators():
    root.update()
    root.update_idletasks()
