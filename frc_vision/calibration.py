import tkinter as tk

import cv2

import frc_vision.constants


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

def initalize_calibrators():
    """
    Check if calibration is on, and if so, enable trackbars.
    """
    global root

    root = tk.Tk()

    l1 = tk.Label(root, text="HSV Lower Bound (B)")
    l1.pack()
    create_scale(0, 179, "HLB", frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_L[0])
    create_scale(0, 255, "SLB", frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_L[1])
    create_scale(0, 255, "VLB", frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_L[2])
    
    l2 = tk.Label(root, text="HSV Upper Bound (B)")
    l2.pack()
    
    create_scale(0, 179, "HUB", frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_U[0])
    create_scale(0, 255, "SUB", frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_U[1])
    create_scale(0, 255, "VUB", frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_U[2])
    
    l3 = tk.Label(root, text="HSV Lower Bound (R)")
    l3.pack()
    
    create_scale(0, 179, "HLR", frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L[0])
    create_scale(0, 255, "SLR", frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L[1])
    create_scale(0, 255, "VLR", frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L[2])
    
    l4 = tk.Label(root, text="HSV Upper Bound (R)")
    l4.pack()
    
    create_scale(0, 179, "HUR", frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U[0])
    create_scale(0, 255, "SUR", frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U[1])
    create_scale(0, 255, "VUR", frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U[2])

    tk.Label(root, text="HSV Bound (R2)").pack()
    
    create_scale(0, 179, "HLR2", frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L2[0])    
    create_scale(0, 179, "HUR2", frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U2[0])

    l5 = tk.Label(root, text="Circle Comparison Threshold")
    l5.pack()

    create_scale(50, 300, "Circle", int(frc_vision.constants.CIRCLE_COMPARISON_THRESHOLD*100))


def calibrators(key: str, value: str):
    """
    Set constants to trackbar positions.
    """
    match key:
        case "HLB": frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_L[0] = int(value)
        case "SLB": frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_L[1] = int(value)
        case "VLB": frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_L[2] = int(value)
        case "HUB": frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_U[0] = int(value)
        case "SUB": frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_U[1] = int(value)
        case "VUB": frc_vision.constants.HSV_BOUNDS.ASTRA.BLUE_BOUND_U[2] = int(value)
        case "HLR": frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L[0] = int(value)
        case "SLR": frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L[1] = frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L2[1] = int(value)
        case "VLR": frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L[2] = frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L2[2] = int(value)
        case "HUR": frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U[0] = int(value)
        case "SUR": frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U[1] = frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U2[1] = int(value)
        case "VUR": frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U[2] = frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U2[2] = int(value)
        case "HLR2": frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_L2[0] = int(value)
        case "HUR2": frc_vision.constants.HSV_BOUNDS.ASTRA.RED_BOUND_U2[0] = int(value)

        case "Circle": frc_vision.constants.CIRCLE_COMPARISON_THRESHOLD = int(value)/100

def update_calibrators():
    root.update()
    root.update_idletasks()
