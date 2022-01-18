from networktables import NetworkTables
import cv2
import frc_vision.constants
import frc_vision.hopper.utils
import logging
import numpy as np
import time
import frc_vision.hopper.viewer

logger = logging.getLogger(__name__)


# sd = NetworkTables.getTable("SmartDashboard")


class Driver:
    in_hopper: list
    switch_flag: bool
    shoot_flag: bool
    vcap: cv2.VideoCapture

    def __init__(self):
        self.in_hopper = []
        self.switch_flag = False
        self.shoot_flag = False
        self.vcap = cv2.VideoCapture(frc_vision.constants.VIEWER_ID)
        if not self.vcap.isOpened():
            logger.critical("Cannot open camera")
            exit()
        # NetworkTables.initialize(server=frc_vision.constants.ROBORIO_SERVER)

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

    def run(self, view: bool = False):
        start_time = time.time()

        _, frame = self.vcap.read()
        frame = cv2.flip(frame, 1)
        # self.red_mask, self.blue_mask = frc_vision.hopper.utils.generate_mask(frame)

        self.circles = frc_vision.hopper.utils.find_circles(
            frame
        )  # TODO: change this to work on red and blue mask
        self.switch_checks(frame)

        if view:
            v = frc_vision.hopper.viewer.Viewer()
            v.view(frame, self.circles, start_time, self.in_hopper)
