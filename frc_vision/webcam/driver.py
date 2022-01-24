import logging
import time

import cv2
import networktables
from networktables import NetworkTables

import frc_vision.constants
import frc_vision.utils
import frc_vision.viewer
import frc_vision.webcam.utils

logger = logging.getLogger(__name__)


class Driver:
    in_hopper: list
    switch_flag: bool
    shoot_flag: bool
    table: networktables.NetworkTable
    vcap: cv2.VideoCapture

    def __init__(self):
        self.in_hopper = []
        self.switch_flag = False
        self.shoot_flag = False
        self.vcap = cv2.VideoCapture(frc_vision.constants.VIEWER_ID)
        if not self.vcap.isOpened():
            logger.critical("Cannot open camera")
            exit()
        NetworkTables.initialize(server=frc_vision.constants.ROBORIO_SERVER)
        self.table = NetworkTables.getTable("FRCVision")

    def shooter(self):
        self.shoot_flag = True

    def switch(self):
        self.switch_flag = True

    def switch_checks(self, blue_circles, red_circles):
        """Run switch checks for the hopper camera (very temporary, this will change)"""
        if self.switch_flag:
            if len(blue_circles) > 0 and len(red_circles) > 0:
                self.in_hopper.append(
                    "B" if len(blue_circles) > len(red_circles) else "R"
                )
            elif len(blue_circles) > 0:
                self.in_hopper.append("B")
            elif len(red_circles) > 0:
                self.in_hopper.append("R")

            self.switch_flag = False

        if self.shoot_flag:
            if self.in_hopper != []:
                self.in_hopper.pop(0)
            self.shoot_flag = False

    def process_frame(self, frame):
        """
        Run all processing on the frame and return
        the end result. (Not decided yet)
        """
        blue_mask, red_mask = frc_vision.webcam.utils.generate_masks(frame)
        blue_circles = frc_vision.utils.find_circles(frame, blue_mask)
        red_circles = frc_vision.utils.find_circles(frame, red_mask)
        self.switch_checks(frame, blue_circles, red_circles)
        return blue_circles, red_circles

    def destroy(self):
        self.vcap.release()
        cv2.destroyAllWindows()

    def run(self, view: bool = False):
        running = True
        while running:
            start_time = time.time()

            _, frame = self.vcap.read()
            frame = cv2.flip(frame, 1)
            blue_circles, red_circles = self.process_frame(frame)

            if view:
                frc_vision.viewer.view(
                    (frc_vision.viewer.ViewerFrame(frame, "frame", show_data=True)),
                    (blue_circles, red_circles),
                    start_time,
                )

            if cv2.waitKey(15) == frc_vision.constants.CV2_WAIT_KEY:
                running = False

        self.destroy()
