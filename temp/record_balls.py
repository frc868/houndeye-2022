import cv2
import numpy as np
from openni import _openni2 as c_api
from openni import openni2

openni2.initialize()
dev = openni2.Device.open_any()
color_stream = dev.create_color_stream()
color_stream.set_video_mode(
    c_api.OniVideoMode(
        pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,
        resolutionX=640,
        resolutionY=480,
        fps=30,
    )
)
color_stream.start()


depth_stream = dev.create_depth_stream()
depth_stream.set_video_mode(
    c_api.OniVideoMode(
        pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM,
        resolutionX=640,
        resolutionY=480,
        fps=30,
    )
)
depth_stream.start()


def get_color_frame(color_stream) -> np.ndarray:
    raw_frame = color_stream.read_frame()
    frame = np.frombuffer(raw_frame.get_buffer_as_uint8(), dtype=np.uint8)
    frame.shape = (480, 640, 3)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.flip(frame, 1)

    return frame

def get_depth_frame(depth_stream):
    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()
    img = np.frombuffer(frame_data, dtype=np.uint16)
    img.shape = (480, 640)
    img = cv2.medianBlur(img, 3)
    img = cv2.flip(img, 1)

    return img

capture = cv2.VideoWriter('red1.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, (640,480))
                        
depth = cv2.VideoWriter('blue1_depth.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, (640,480))

while True:
    f=get_color_frame(color_stream)
    # d=get_depth_frame(depth_stream)
    cv2.imshow("color", f)
    # cv2.imshow("depth", d)
    # print(f.dtype, d.dtype)
    capture.write(f)
    # depth.write(get_depth_frame(depth_stream))

    if cv2.waitKey(15) == 27:
        depth_stream.stop()
        color_stream.stop()
        openni2.unload()
        cv2.destroyAllWindows()
        break