from networktables import NetworkTables
import cv2
import frc_vision.constants
import frc_vision.hopper.utils
import logging
import numpy as np
import time
import frc_vision.hopper.viewer
from openni import openni2
from openni import _openni2 as c_api

logger = logging.getLogger(__name__)


class Driver:
    in_hopper: list
    switch_flag: bool
    shoot_flag: bool

    def __init__(self):
        self.in_hopper = []
        self.switch_flag = False
        self.shoot_flag = False
        self.vcap = cv2.VideoCapture(frc_vision.constants.VIEWER_ID)
        openni2.initialize()
        dev = openni2.Device.open_any()
        self.color_stream = dev.create_color_stream()
        self.color_stream.set_video_mode(
            c_api.OniVideoMode(
                pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,
                resolutionX=640,
                resolutionY=480,
                fps=30,
            )
        )
        self.color_stream.start()

        self.depth_stream = dev.create_depth_stream()
        self.depth_stream.set_video_mode(
            c_api.OniVideoMode(
                pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM,
                resolutionX=640,
                resolutionY=480,
                fps=30,
            )
        )
        self.depth_stream.start()
        dev.set_image_registration_mode(openni2.IMAGE_REGISTRATION_DEPTH_TO_COLOR)
        dev.set_depth_color_sync_enabled(True)

        NetworkTables.initialize(server=frc_vision.constants.ROBORIO_SERVER)
        # self.sd = NetworkTables.getTable("SmartDashboard")

    def shooter(self):
        self.shoot_flag = True

    def switch(self):
        self.switch_flag = True

    def _switch_checks(self):  # old
        if self.switch_flag:
            if np.sum(self.red_mask) > np.sum(self.blue_mask):
                self.in_hopper.append("R")
            else:
                self.in_hopper.append("B")
            self.switch_flag = False

        if self.shoot_flag:
            if self.in_hopper != []:
                self.in_hopper.pop(0)
            self.shoot_flag = False

    def switch_checks(self, frame):  # testing with ping pong ball
        if self.switch_flag:
            if frc_vision.hopper.utils.find_circles(frame) is not None:
                self.in_hopper.append("Found")
            else:
                self.in_hopper.append("No")
            self.switch_flag = False

        if self.shoot_flag:
            if self.in_hopper != []:
                self.in_hopper.pop(0)
            self.shoot_flag = False

    def get_color_frame(self) -> np.ndarray:
        raw_frame = self.color_stream.read_frame()
        frame = np.frombuffer(raw_frame.get_buffer_as_uint8(), dtype=np.uint8)
        frame.shape = (480, 640, 3)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)

        return frame
    
    def get_depth_frame(self):
        frame = self.depth_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        img = np.frombuffer(frame_data, dtype=np.uint16)
        img.shape = (self.height, self.width)
        img = cv2.medianBlur(img, 3)
        img = cv2.flip(img, 1)

        # self.depth_frame = img.copy()

        return img

    def run(self, view: bool = False):
        start_time = time.time()
        frame = self.get_color_frame()
        dframe = self.get_depth_frame()
        # cv2.imshow("test", frame)
        # self.red_mask, self.blue_mask = frc_vision.hopper.utils.generate_mask(frame)

        self.circles = frc_vision.hopper.utils.find_circles(
            frame
        )  # TODO: change this to work on red and blue mask
        self.switch_checks(frame)
        # self.sd.putBoolean("start_motor", "Found" in self.in_hopper)
        # self.sd.putNumber("tx", 0)
        if self.circles is not None:
            test_circles = np.uint16(np.around(self.circles))

            x,y,r = test_circles[0, :][0]
            tx = frc_vision.constants.ASTRA_CAMERA.FOV_H/2 * (x-(frc_vision.constants.ASTRA_CAMERA.RESOLUTION_W/2))/(frc_vision.constants.ASTRA_CAMERA.RESOLUTION_W/2)
            ty = frc_vision.constants.ASTRA_CAMERA.FOV_V/2 * (y-(frc_vision.constants.ASTRA_CAMERA.RESOLUTION_H/2))/(frc_vision.constants.ASTRA_CAMERA.RESOLUTION_H/2)
            print(f"tx: {tx}, ty: {ty}")
        # print(self.circles[0])

        if view:
            v = frc_vision.hopper.viewer.Viewer()
            v.view(frame, self.circles, start_time, self.in_hopper)
