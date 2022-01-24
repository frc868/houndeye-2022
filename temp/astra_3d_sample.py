import frc_vision.astra.utils as au
import cv2, time

"""
initialization has the following options:
    - devices: "color", "depth", and "ir"
      *** "color" and "ir" are unable to be used together ***
    - resolution: options are:
        (640, 480) or (320, 240)
        
        
Adjust the HSV filters to extract the color of the ball.
"""

resolutionWidth = 640
resolutionHeight = 480

vw = au.Viewer3D(
    [
        "color",
        "depth",
    ],
    (resolutionWidth, resolutionHeight),
)

gui = au.GUI()
gui._create_windows(
    {
        "color": {
            "position": (325, 0),
            "flag": cv2.WINDOW_AUTOSIZE,
        },
        "depth": {
            "position": (325, 525),
            "flag": cv2.WINDOW_AUTOSIZE,
        },
        "result": {
            "position": (975, 0),
            "flag": cv2.WINDOW_AUTOSIZE,
        },
        "HSV Filters": {
            "position": (0, 0),
            "flag": cv2.WINDOW_NORMAL,
        },
    }
)

trackbars = {
    "HSV Filters": {
        "H min": (0, 179),
        "S min": (0, 255),
        "V min": (0, 255),
        "H max": (179, 179),
        "S max": (255, 255),
        "V max": (255, 255),
    }
}

vw._create_hsv_trackbars(trackbars)

running = True

while running:
    start_time = time.time()

    vw._get_color_frame()
    vw._get_depth_frame()
    vw._extract_hsv_inrange()
    vw._find_circle()

    fps = 1.0 / (time.time() - start_time)
    text = "fps: {:.2f}".format(fps)
    color_frame = vw.color_frame.copy()

    cv2.putText(
        color_frame, text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2
    )

    cv2.imshow("color", color_frame)
    cv2.imshow("depth", vw.depth_frame)
    cv2.imshow("result", vw.result_frame)

    if cv2.waitKey(15) == 27:  # esc to quit
        running = False

vw._destroy()
