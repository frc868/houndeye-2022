from openni import openni2
from openni import _openni2 as c_api
import sys, cv2
import numpy as np
import logging
import frc_vision.constants

logger = logging.getLogger(__name__)  # TODO: Write logs to file.


class Driver:
    def __init__(self, sensors, resolution):
        self.width, self.height = resolution
        self.fps = 30

        if ("color" in sensors) and ("ir" in sensors):
            logger.critical("Cannot initiate color and ir sensors at the same time...")
            sys.exit()

        print("[INFO] initializing openni...")
        openni2.initialize()

        print("[INFO] opening device...")
        dev = openni2.Device.open_any()

        # pixelFormat can also be "ONI_PIXEL_FORMAT_DEPTH_1_MM"
        if "depth" in sensors:
            print("[INFO] creating depth stream...")
            self.depth_stream = dev.create_depth_stream()
            self.depth_stream.set_video_mode(
                c_api.OniVideoMode(
                    pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM,
                    resolutionX=self.width,
                    resolutionY=self.height,
                    fps=self.fps,
                )
            )
            self.depth_stream.start()

        if "ir" in sensors:
            print("[INFO] creating ir stream...")
            self.ir_stream = dev.create_ir_stream()
            self.ir_stream.set_video_mode(
                c_api.OniVideoMode(
                    pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_GRAY16,
                    resolutionX=self.width,
                    resolutionY=self.height,
                    fps=self.fps,
                )
            )
            self.ir_stream.start()

        if "color" in sensors:
            print("[INFO] creating color stream...")
            self.color_stream = dev.create_color_stream()
            self.color_stream.set_video_mode(
                c_api.OniVideoMode(
                    pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,
                    resolutionX=self.width,
                    resolutionY=self.height,
                    fps=self.fps,
                )
            )
            self.color_stream.start()

        if ("color" in sensors) and ("depth" in sensors):
            print("[INFO] synchronizong color and depth sensors...")
            dev.set_image_registration_mode(openni2.IMAGE_REGISTRATION_DEPTH_TO_COLOR)
            dev.set_depth_color_sync_enabled(True)

        self.sensors = sensors

    def _get_depth_frame(self):
        frame = self.depth_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        img = np.frombuffer(frame_data, dtype=np.uint16)
        img.shape = (self.height, self.width)
        img = cv2.medianBlur(img, 3)
        img = cv2.flip(img, 1)

        self.depth_frame = img.copy()

        return img

    def _get_ir_frame(self):
        frame = self.ir_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        img = np.frombuffer(frame_data, dtype=np.uint16)
        img.shape = (self.height, self.width)
        img = np.multiply(img, int(65535 / 1023))
        img = cv2.GaussianBlur(img, (5, 5), 0)
        img = cv2.flip(img, 1)

        self.ir_frame = img.copy()

        return img

    def _get_color_frame(self):
        frame = self.color_stream.read_frame()
        frame_data = frame.get_buffer_as_uint8()
        img = np.frombuffer(frame_data, dtype=np.uint8)
        img.shape = (self.height, self.width, 3)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.flip(img, 1)

        self.color_frame = img.copy()

        return img

    def _destroy(self):
        if "depth" in self.sensors:
            self.depth_stream.stop()
        if "ir" in self.sensors:
            self.ir_stream.stop()
        if "color" in self.sensors:
            self.color_stream.stop()

        openni2.unload()
        cv2.destroyAllWindows()

    def _nothing(self, x):
        pass

    def _create_hsv_trackbars(self, trackbars):
        for window in trackbars:
            for trackbar in trackbars[window]:
                count = trackbars[window][trackbar]

                cv2.createTrackbar(trackbar, window, count[0], count[1], self._nothing)

    def _extract_hsv_inrange(self):
        h_min = cv2.getTrackbarPos("H min", "HSV Filters")
        s_min = cv2.getTrackbarPos("S min", "HSV Filters")
        v_min = cv2.getTrackbarPos("V min", "HSV Filters")
        h_max = cv2.getTrackbarPos("H max", "HSV Filters")
        s_max = cv2.getTrackbarPos("S max", "HSV Filters")
        v_max = cv2.getTrackbarPos("V max", "HSV Filters")

        self.lower_range = np.array([h_min, s_min, v_min])
        self.upper_range = np.array([h_max, s_max, v_max])

        frame = self.color_frame.copy()
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, self.lower_range, self.upper_range)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        self.hsv_min = "MIN H:{} S:{} V:{}".format(h_min, s_min, v_min)
        self.hsv_max = "MAX H:{} S:{} V:{}".format(h_max, s_max, v_max)

        cv2.putText(
            result, self.hsv_min, (5, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2
        )

        cv2.putText(
            result, self.hsv_max, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2
        )

        self.hsv_mask = mask.copy()
        self.result_frame = result.copy()

    def _find_circle(self):
        mask = self.hsv_mask.copy()

        cnts, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        self.ball_center = None

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            if radius > 10:
                ball_center = (int(x), int(y))

                cv2.circle(self.color_frame, ball_center, int(radius), (0, 255, 0), 2)

                roi_margin = int(
                    radius * 0.20
                )  # can be adjusted to reflect the portion of the ball to test
                x1 = max(0, ball_center[0] - roi_margin)
                x2 = min(self.width - 1, ball_center[0] + roi_margin)
                y1 = max(0, ball_center[1] - roi_margin)
                y2 = min(self.height - 1, ball_center[1] + roi_margin)
                roi = self.depth_frame[y1:y2, x1:x2]

                distance = int(np.average(roi))

                cv2.putText(
                    self.color_frame,
                    str(distance),
                    ball_center,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )

                self.ball_center = ball_center


class GUI:
    def _create_windows(self, windows):
        for window in windows:
            position = windows[window]["position"]
            flag = windows[window]["flag"]

            self._create_window(window, position, flag)

    def _create_window(self, title, position, flag):
        cv2.namedWindow(title, flag)
        cv2.moveWindow(title, position[0], position[1])
