import enum
import subprocess
import time

import cscore
import cv2
import networktables
from cscore import CameraServer
from networktables import NetworkTables

import houndeye.calibration
import houndeye.constants
import houndeye.drivers
import houndeye.processing
import houndeye.utils
import houndeye.viewer
from houndeye.processing import cargo_detection


class Alliance(enum.IntEnum):
    BLUE = enum.auto()
    RED = enum.auto()


class TableGroup:
    HoundEye: networktables.NetworkTable
    SmartDashboard: networktables.NetworkTable
    FMSInfo: networktables.NetworkTable


class Runner:
    tables: TableGroup = TableGroup()
    enable_calibration: bool
    enable_networking: bool
    alliance: Alliance = Alliance.BLUE
    drivers: list[houndeye.drivers.Driver]

    def __init__(
        self,
        drivers: list[houndeye.drivers.Driver],
        enable_calibration: bool = False,
        enable_networking: bool = True,
    ) -> None:
        self.drivers = drivers
        self.enable_calibration = enable_calibration
        self.enable_networking = enable_networking

        if self.enable_networking:
            self.initialize_networktables()
            self.initialize_cameraserver()

    def initialize_networktables(self) -> None:
        """Connects to NetworkTables on the roboRIO."""
        NetworkTables.initialize(server=houndeye.constants.Servers.ROBORIO_SERVER_IP)
        self.tables.HoundEye = NetworkTables.getTable("HoundEye")
        self.tables.SmartDashboard = NetworkTables.getTable("SmartDashboard")
        self.tables.FMSInfo = NetworkTables.getTable("FMSInfo")
        self.set_alliance()

    def initialize_cameraserver(self) -> None:
        CameraServer.enableLogging()
        cs = CameraServer()
        for idx, driver in enumerate(self.drivers):
            driver.cs_output = cs.putVideo(
                f"HoundEye Cam {idx}",
                *driver.video_dimensions,  # unpack the length and width
            )

    def set_alliance(self) -> None:
        """
        Checks FMSInfo to see what alliance is currently set.
        This can be changed in practice through the Driver Station.
        """
        self.alliance = (
            Alliance.RED
            if self.tables.FMSInfo.getBoolean("IsRedAlliance", True)
            else Alliance.BLUE
        )

    def destroy(self) -> None:
        """Cleans up streams and unloads cameras."""
        for driver in self.drivers:
            driver.stop()
        # TODO: add CameraServer stop

    def write_rpi_temps(self) -> None:
        """Runs `vcgencmd measure_temp` to get the current temperature of the Pi and sends it to SmartDashboard."""
        raw_output = subprocess.run(
            ["vcgencmd", "measure_temp"], capture_output=True, text=True
        ).stdout
        trimmed_output = raw_output.removeprefix("temp=").removesuffix("'C\n")
        self.tables.SmartDashboard.putNumber("rpi_temp", float(trimmed_output))

    def send_nt_data(self, data: dict[str, list[str | bool | int | float]]) -> None:
        """
        Sends circle data over NetworkTables.

        CURRENT DATA STRUCTURE:
        Four arrays are output to NetworkTables, with
        indices being consistent across all arrays
        (that is, ball 0 will be ball 0 in color, tx, ty, and td)
        color: either "B" or "R", denotes ball color
        tx: x degree offset from center (from -30 to 30)
        ty: y degree offset from center (from -24.75 to 24.75)
        td: distance from camera to ball
        """
        self.tables.HoundEye.putString(
            "alliance", "B" if self.alliance == Alliance.BLUE else "R"
        )
        for key, value in data.items():
            match value:
                case list(int()) | list(float()):
                    self.tables.HoundEye.getSubTable().putNumberArray(key, value)
                case list(bool()):
                    self.tables.HoundEye.getSubTable().putNumberArray(key, value)
                case list(str()):
                    self.tables.HoundEye.getSubTable().putStringArray(key, value)
                case _:
                    self.tables.HoundEye.getSubTable().putValue(
                        key, value
                    )  # can't use this for list types

    def send_camera_data(
        self,
        frame: houndeye.utils.cv2Frame,
        processing_result: houndeye.processing.Processor.ProcessingResult,
        camera_constants: houndeye.constants.CameraConstants,
        cs_output: cscore.CvSource,
        start_time: float,
    ) -> None:
        frame = houndeye.viewer.draw_circles(
            frame, processing_result.blue_circles, processing_result.red_circles
        )
        frame = houndeye.viewer.draw_metrics(frame, start_time)
        frame = cv2.resize(
            frame,
            (
                camera_constants.RESOLUTION_W * camera_constants.video_scale,
                camera_constants.RESOLUTION_H * camera_constants.video_scale,
            ),
        )
        cs_output.putFrame(frame)

    def run(self) -> None:
        """Main driver to run the detection program."""
        houndeye.constants.load_constants()

        if self.enable_calibration:
            houndeye.calibration.initalize_calibrators()

        running = True
        while running:
            try:
                start_time = time.time()
                for driver in self.drivers:
                    processing_result, frame = driver.processor.run()
                    if self.enable_networking:
                        self.send_nt_data(
                            driver.processor.package_data(
                                processing_result, self.alliance
                            )
                        )
                        self.send_camera_data(
                            frame, processing_result, driver, start_time
                        )

                if self.enable_networking:
                    self.set_alliance()
                    self.write_rpi_temps()

                if self.enable_calibration:
                    blue_mask, red_mask = cargo_detection.generate_masks(color_frame)
                    houndeye.viewer.view(
                        frames=(
                            houndeye.viewer.ViewerFrame(
                                color_frame, "color", show_data=True
                            ),
                            houndeye.viewer.ViewerFrame(depth_frame, "depth"),
                            houndeye.viewer.ViewerFrame(blue_mask, "blue"),
                            houndeye.viewer.ViewerFrame(red_mask, "red"),
                        ),
                        circles=(blue_circles, red_circles),
                        data=(
                            houndeye.viewer.ViewerData("tx", tx),
                            houndeye.viewer.ViewerData("ty", ty),
                            houndeye.viewer.ViewerData("ta", ta),
                        ),
                        start_time=start_time,
                    )

                    houndeye.calibration.update_calibrators()

                if cv2.waitKey(15) == houndeye.constants.Keys.CV2_WAIT_KEY:
                    running = False
            except KeyboardInterrupt:
                running = False

        self.destroy()
