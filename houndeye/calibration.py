import tkinter as tk

import houndeye.astra.driver
import houndeye.constants

"""
Certain code is intentionally all on one line
to make it easier to debug (ignoring style guide).
Black formatter has not been applied to this file.
"""

# fmt: off

SCALES = {}

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
    SCALES[key] = s
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
    global color

    root = tk.Tk()

    create_label("HSV Lower Bound (B)")
    create_scale(0, 179, "HLB", houndeye.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_L[0])
    create_scale(0, 255, "SLB", houndeye.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_L[1])
    create_scale(0, 255, "VLB", houndeye.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_L[2])
    
    create_label("HSV Upper Bound (B)")
    create_scale(0, 179, "HUB", houndeye.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_U[0])
    create_scale(0, 255, "SUB", houndeye.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_U[1])
    create_scale(0, 255, "VUB", houndeye.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_U[2])
    
    create_label("HSV Lower Bound (R)")
    create_scale(0, 179, "HLR", houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L[0])
    create_scale(0, 255, "SLR", houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L[1])
    create_scale(0, 255, "VLR", houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L[2])
    
    create_label("HSV Upper Bound (R)")
    create_scale(0, 179, "HUR", houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U[0])
    create_scale(0, 255, "SUR", houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U[1])
    create_scale(0, 255, "VUR", houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U[2])

    create_label("HSV Bound (R2)")
    create_scale(0, 179, "HLR2", houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L2[0])    
    create_scale(0, 179, "HUR2", houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U2[0])

    create_label("Circle Comparison Threshold")
    create_scale(50, 300, "circle", int(houndeye.constants.CIRCLE_COMPARISON_THRESHOLD*100))
        
    create_label("Exposure")
    create_scale(0, 500, "exp", houndeye.constants.ASTRA.EXPOSURE)

    create_label("Gain")
    create_scale(0, 500, "gain", houndeye.constants.ASTRA.GAIN)

    save_b = tk.Button(root, text="Save constants to file", command=houndeye.constants.dump_constants)
    save_b.pack()

    create_label("Utilities")
    
    color = "blue"

    def color_b_callback():
        global color
        color = "blue" if color == "red" else "red"
        if color == "blue":
            color_b.configure(text="  BLUE  ", bg="blue")
        elif color == "red":
            color_b.configure(text="  RED  ", bg="red")


    color_b = tk.Button(root, text="  BLUE  ", bg="blue", command=color_b_callback)
    color_b.pack()

    def center_b_callback():
        houndeye.astra.driver

    center_b = tk.Button(root, text="Center values", command=center_b_callback)
    center_b.pack()

    def include_b_callback():
        pass

    include_b = tk.Button(root, text="Include pixel", command=include_b_callback)
    include_b.pack()

    def exclude_b_callback():
        pass

    exclude_b = tk.Button(root, text="Exclude pixel", command=exclude_b_callback)
    exclude_b.pack()


def calibrators(key: str, value: str):
    """
    Set constants to trackbar positions.
    """
    if key == "HLB": houndeye.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_L[0] = int(value)
    if key == "SLB": houndeye.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_L[1] = int(value)
    if key == "VLB": houndeye.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_L[2] = int(value)
    if key == "HUB": houndeye.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_U[0] = int(value)
    if key == "SUB": houndeye.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_U[1] = int(value)
    if key == "VUB": houndeye.constants.ASTRA.HSV_BOUNDS.BLUE_BOUND_U[2] = int(value)
    if key == "HLR": houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L[0] = int(value)
    if key == "SLR": houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L[1] = houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L2[1] = int(value)
    if key == "VLR": houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L[2] = houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L2[2] = int(value)
    if key == "HUR": houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U[0] = int(value)
    if key == "SUR": houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U[1] = houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U2[1] = int(value)
    if key == "VUR": houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U[2] = houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U2[2] = int(value)
    if key == "HLR2": houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_L2[0] = int(value)
    if key == "HUR2": houndeye.constants.ASTRA.HSV_BOUNDS.RED_BOUND_U2[0] = int(value)

    if key == "circle": houndeye.constants.CIRCLE_COMPARISON_THRESHOLD = int(value)/100
    if key == "exp": houndeye.constants.ASTRA.EXPOSURE = int(value)
    if key == "gain": houndeye.constants.ASTRA.GAIN = int(value)



def update_calibrators():
    root.update()
    root.update_idletasks()


if __name__ == "__main__":
    initalize_calibrators()
    while True:
        update_calibrators()
