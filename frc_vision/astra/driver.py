import logging
import time
import typing

import cv2
import networktables
import numpy as np
from networktables import NetworkTables
from openni import _openni2 as c_api
from openni import openni2

import frc_vision.astra.utils
import frc_vision.config
import frc_vision.constants
import frc_vision.utils
import frc_vision.viewer
from frc_vision.utils import cv2Frame

logger = logging.getLogger(__name__)  # TODO: Write logs to file.


class AstraException(Exception):
    pass


class Driver:
    color_stream: typing.Optional[openni2.VideoStream]
    depth_stream: typing.Optional[openni2.VideoStream]
    table: networktables.NetworkTable

    def __init__(self):
        self.create_streams()

    def create_streams(self) -> None:
        """
        Initializes and synchronized the color and depth streams from an
        Orbbec Astra camera through OpenNI.

        Params:
            None

        Returns:
            None

        Raises:
            None

        """
        logger.info("Initializing OpenNI")
        openni2.initialize(dll_directories=["./openni-redist"])

        logger.info("Opening device")
        device = openni2.Device.open_any()

        logger.info("Creating color stream")
        self.color_stream = device.create_color_stream()
        self.color_stream.set_video_mode(
            c_api.OniVideoMode(
                pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,
                resolutionX=frc_vision.constants.ASTRA.RESOLUTION_W,
                resolutionY=frc_vision.constants.ASTRA.RESOLUTION_H,
                fps=frc_vision.constants.ASTRA.FPS,
            )
        )
        self.color_stream.start()

        # pixelFormat can also be "ONI_PIXEL_FORMAT_DEPTH_1_MM"
        logger.info("Creating depth stream")
        self.depth_stream = device.create_depth_stream()
        self.depth_stream.set_video_mode(
            c_api.OniVideoMode(
                pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM,
                resolutionX=frc_vision.constants.ASTRA.RESOLUTION_W,
                resolutionY=frc_vision.constants.ASTRA.RESOLUTION_H,
                fps=frc_vision.constants.ASTRA.FPS,
            )
        )
        self.depth_stream.start()

        logger.info("Synchronizing color and depth sensors")
        device.set_image_registration_mode(openni2.IMAGE_REGISTRATION_DEPTH_TO_COLOR)
        device.set_depth_color_sync_enabled(True)

        NetworkTables.initialize(server=frc_vision.constants.ROBORIO_SERVER)
        self.table = NetworkTables.getTable("FRCVision")

    def get_frames(self) -> tuple[cv2Frame, cv2Frame]:
        """
        Reads the color and depth frames from an Orbbec Astra camera
        through OpenNI and converts it to an openCV-usable format.

        Params:
            None

        Returns:
            openCV color frame
            openCV depth frame

        Raises:
            None
        """

        raw_color_frame = self.color_stream.read_frame()
        color_frame = np.frombuffer(
            raw_color_frame.get_buffer_as_uint8(), dtype=np.uint8
        )
        color_frame.shape = (
            frc_vision.constants.ASTRA.RESOLUTION_H,
            frc_vision.constants.ASTRA.RESOLUTION_W,
            3,
        )
        color_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2RGB)
        color_frame = cv2.flip(color_frame, 1)

        raw_depth_frame = self.depth_stream.read_frame()
        depth_frame = np.frombuffer(
            raw_depth_frame.get_buffer_as_uint16(), dtype=np.uint16
        )
        depth_frame.shape = (
            frc_vision.constants.ASTRA.RESOLUTION_H,
            frc_vision.constants.ASTRA.RESOLUTION_W,
        )
        depth_frame = cv2.medianBlur(depth_frame, 3)
        depth_frame = cv2.flip(depth_frame, 1)

        return color_frame, depth_frame

    def destroy(self):
        """Cleans up streams and unloads camera."""
        self.depth_stream.stop()
        self.color_stream.stop()

        openni2.unload()
        cv2.destroyAllWindows()

    def write_to_networktables(self, circles):
        """Writes circle location data to NetworkTables."""
        tx, ty = frc_vision.astra.utils.calculate_angles(circles)
        self.table.putNumber("tx", tx)
        self.table.putNumber("ty", ty)

    def process_frame(self, color_frame, depth_frame):
        """
        Run all processing on the frames and return
        the end result. (Not decided yet)

        TODO: add depth frame analysis.
        """
        blue_mask, red_mask = frc_vision.astra.utils.generate_masks(color_frame)
        blue_circles = frc_vision.utils.find_circles(color_frame, blue_mask)
        red_circles = frc_vision.utils.find_circles(color_frame, red_mask)
        return blue_circles, red_circles

    def run(self, view: bool = False) -> None:
        """Main driver to run the detection program."""
        if frc_vision.config.ENABLE_CALIBRATION:
            self.initalize_calibrators()

        running = True
        while running:
            start_time = time.time()
            color_frame, depth_frame = self.get_frames()
            blue_circles, red_circles = self.process_frame(color_frame, depth_frame)
            self.write_to_networktables(
                blue_circles
            )  # TODO: find a NetworkTables implementation that allows for data for multiple gamepieces to be sent

            if view:
                frc_vision.viewer.view(
                    (
                        frc_vision.viewer.ViewerFrame(
                            color_frame, "color", show_data=True
                        ),
                        frc_vision.viewer.ViewerFrame(depth_frame, "depth"),
                    ),
                    (blue_circles, red_circles),
                    [],
                    start_time,
                )

            if cv2.waitKey(15) == frc_vision.constants.CV2_WAIT_KEY:
                running = False

        self.destroy()
