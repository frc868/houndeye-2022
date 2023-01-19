import logging
import typing

import cscore
import cv2
import numpy as np
from openni import _openni2 as c_api
from openni import openni2

import houndeye.calibration
import houndeye.constants
import houndeye.processing.cargo_detection
import houndeye.utils
import houndeye.viewer
from houndeye.drivers import Driver
from houndeye.processing import cargo_detection
from houndeye.utils import cv2Frame

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Driver:
    depth_enabled: bool
    camera_constants: houndeye.constants.CameraConstants
    video_scale: float  # controls how much network bandwidth is used
    name: str
    cs_output: cscore.CvSource
    processor: houndeye.processing.cargo_detection.Processor

    def get_frames(self) -> tuple[cv2Frame]:
        raise NotImplementedError

    def stop(self) -> None:
        raise NotImplementedError


class Astra(Driver):
    """Driver for the Astra camera. This should only ever be created once."""

    depth_enabled: bool = True
    camera_constants: houndeye.constants.Astra = houndeye.constants.Astra
    video_scale: float = 0.25
    name: str = "Astra"
    processor: houndeye.processing.cargo_detection.Processor

    color_stream: openni2.VideoStream
    depth_stream: openni2.VideoStream
    camera_settings: openni2.CameraSettings

    def __init__(self) -> None:
        self.create_streams()
        self.processor = cargo_detection.AstraProcessor(self.get_frames)

    def create_streams(self) -> None:
        """
        Initializes and synchronized the color and depth streams from an
        Orbbec Astra camera through OpenNI.
        """
        logger.info("Initializing OpenNI")
        openni2.initialize(dll_directories=["./openni-redist"])

        logger.info("Opening device")
        device = openni2.Device.open_any()

        logger.info("Creating color stream")
        self.color_stream = device.create_color_stream()

        self.camera_settings = openni2.CameraSettings(self.color_stream)
        self.camera_settings.set_auto_exposure(False)
        self.camera_settings.set_auto_white_balance(False)
        self.camera_settings.set_exposure(self.camera_constants.EXPOSURE)
        self.camera_settings.set_gain(self.camera_constants.GAIN)

        self.color_stream.set_video_mode(
            c_api.OniVideoMode(
                pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,
                resolutionX=self.camera_constants.RESOLUTION_W,
                resolutionY=self.camera_constants.RESOLUTION_H,
                fps=self.camera_constants.FPS,
            )
        )
        self.color_stream.start()

        # pixelFormat can also be "ONI_PIXEL_FORMAT_DEPTH_1_MM"
        logger.info("Creating depth stream")
        self.depth_stream = device.create_depth_stream()
        self.depth_stream.set_video_mode(
            c_api.OniVideoMode(
                pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM,
                resolutionX=self.camera_constants.RESOLUTION_W,
                resolutionY=self.camera_constants.RESOLUTION_H,
                fps=self.camera_constants.FPS,
            )
        )
        self.depth_stream.start()

        logger.info("Synchronizing color and depth sensors")
        device.set_image_registration_mode(openni2.IMAGE_REGISTRATION_DEPTH_TO_COLOR)
        device.set_depth_color_sync_enabled(True)

    def get_frames(self) -> tuple[cv2Frame, cv2Frame]:
        """
        Reads the color and depth frames from an Orbbec Astra camera
        through OpenNI and converts it to an openCV-usable format.

        Args:
            None

        Returns:
            openCV color frame
            openCV depth frame
        """

        raw_color_frame = self.color_stream.read_frame()
        color_frame = np.frombuffer(
            raw_color_frame.get_buffer_as_uint8(), dtype=np.uint8
        )
        color_frame.shape = (
            houndeye.constants.Astra.RESOLUTION_H,
            houndeye.constants.Astra.RESOLUTION_W,
            3,
        )
        color_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2RGB)
        color_frame = cv2.flip(color_frame, 1)

        raw_depth_frame = self.depth_stream.read_frame()
        depth_frame = np.frombuffer(
            raw_depth_frame.get_buffer_as_uint16(), dtype=np.uint16
        )
        depth_frame.shape = (
            houndeye.constants.Astra.RESOLUTION_H,
            houndeye.constants.Astra.RESOLUTION_W,
        )
        depth_frame = cv2.medianBlur(depth_frame, 3)
        depth_frame = cv2.flip(depth_frame, 1)

        return color_frame, depth_frame

    def stop():
        openni2.unload()
        cv2.destroyAllWindows()


class j5Create(Driver):
    depth_enabled: bool = False
    camera_constants: houndeye.constants.j5Create = houndeye.constants.j5Create
    name: str = "j5Create 360"
    processor: houndeye.processing.cargo_detection.Processor

    vcap: cv2.VideoCapture

    def __init__(self):
        self.vcap = cv2.VideoCapture(1)
        self.processor = cargo_detection.j5CreateProcessor(self.get_frames)

    def get_frames(self) -> cv2Frame:
        frame = self.vcap.read()
        frame = frame[
            self.camera_constants.TOP_CROP : self.camera_constants.BOTTOM_CROP, :
        ]
        cv2.flip(frame, 0)
        return frame

    def stop(self) -> None:
        pass  # TODO: stop the vcap
