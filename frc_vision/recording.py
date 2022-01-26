import logging
import time

import cv2
import networktables
from networktables import NetworkTables

import frc_vision.astra.utils
import frc_vision.calibration
import frc_vision.config
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
        self.vcap = cv2.VideoCapture(frc_vision.config.RECORDING_FILENAME)
        if not self.vcap.isOpened():
            logger.critical("Cannot open recording")
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
        blue_mask, red_mask = frc_vision.astra.utils.generate_masks(frame)
        blue_circles = frc_vision.utils.find_circles(blue_mask)
        red_circles = frc_vision.utils.find_circles(red_mask)
        self.switch_checks(blue_circles, red_circles)
        return blue_circles, red_circles

    def destroy(self):
        self.vcap.release()
        cv2.destroyAllWindows()

    def run(self, view: bool = False):
        if frc_vision.config.ENABLE_CALIBRATION:
            frc_vision.calibration.initalize_calibrators()

        running = True
        playing = True
        while running:
            start_time = time.time()

            if playing:
                _, oframe = self.vcap.read()
            else:
                pass
            frame = cv2.flip(oframe, 1)
            blue_circles, red_circles = self.process_frame(frame)

            if view:
                blue_mask, red_mask = frc_vision.astra.utils.generate_masks(frame)
                frc_vision.viewer.view(
                    (
                        frc_vision.viewer.ViewerFrame(frame, "frame", show_data=True),
                        frc_vision.viewer.ViewerFrame(
                            blue_mask, "blue_mask", show_data=True
                        ),
                        frc_vision.viewer.ViewerFrame(
                            red_mask, "red_mask", show_data=True
                        ),
                    ),
                    (blue_circles, red_circles),
                    (),
                    start_time,
                )
            if frc_vision.config.ENABLE_CALIBRATION:
                frc_vision.calibration.update_calibrators()

            k = cv2.waitKey(40)
            if (
                k == frc_vision.constants.CV2_WAIT_KEY
            ):  # Changed for recording to slow down playback
                running = False
            elif k == 32:
                playing = not playing

        self.destroy()
