#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
This module is the camera
* Captures images
* Places preview images in queue
* Places solver images in queue
* Takes full res images on demand

"""
from multiprocessing import Queue
import time
from PIL import Image
from PiFinder import config
from pathlib import Path
from PiFinder.camera_interface import CameraInterface
from PiFinder.state import SharedStateObj
import logging

import zwoasi as asi

class CameraASI(CameraInterface):
    """The camera class for PI cameras.  Implements the CameraInterface interface."""

    def __init__(self, exposure_time: int, gain: float, library: Path):
        asi.init(
            str(library.absolute())
        )  # Initialize the ASI library
        # find a camera
        num_cameras = asi.get_num_cameras()  # Get the number of connected cameras
        if num_cameras == 0:
            #self.handpad.display("Error:", " no camera found", "")
            self.camType = "not found"
            logging.info("camera not found")
            time.sleep(1)
        else:
            asi.list_cameras()
            self.initialize()
            #self.handpad.display("ZWO camera found", "", "")
            logging.info("ZWO camera found")
            time.sleep(1)
        self.camType = "ZWO"
        self.exposure_time = exposure_time
        self.gain = gain

    def initialize(self) -> None:
        """Initializes the camera and set the needed control parameters"""
        if self.camType == "not found":
            return
        self.camera = asi.Camera(0)  # Initialize the camera
        self.camera.set_control_value(
            asi.ASI_BANDWIDTHOVERLOAD,
            self.camera.get_controls()["BandWidth"]["MinValue"],
        )
        self.camera.disable_dark_subtract()
        self.camera.set_control_value(asi.ASI_WB_B, 99)
        self.camera.set_control_value(asi.ASI_WB_R, 75)
        self.camera.set_control_value(asi.ASI_GAMMA, 50)
        self.camera.set_control_value(asi.ASI_BRIGHTNESS, 50)
        self.camera.set_control_value(asi.ASI_FLIP, 0)
        self.camera.set_image_type(asi.ASI_IMG_RAW8)

    def capture(self) -> Image.Image:
        self.camera.set_control_value(asi.ASI_GAIN, self.gain)
        self.camera.set_control_value(
            asi.ASI_EXPOSURE, self.exposure_time
        )  # microseconds
        return Image.fromarray(self.camera.capture().astype("uint8"), "RGB")

    def capture_file(self, filename: str) -> None:
        self.camera.set_control_value(asi.ASI_GAIN, self.gain)
        self.camera.set_control_value(asi.ASI_EXPOSURE, self.exposure_time)  # microseconds
        self.camera.capture(filename=filename)

    def set_camera_config(
        self, exposure_time: float, gain: float
    ) -> Tuple[float, float]:
        self.exposure_time = exposure_time
        self.gain = gain
        return exposure_time, gain

    def get_cam_type(self) -> str:
        return self.camType


def get_images(shared_state: SharedStateObj, camera_image: Image.Image, command_queue: "Queue[str]", console_queue: "Queue[str]"):
    """
    Instantiates the camera hardware
    then calls the universal image loop
    """

    cfg = config.Config()
    exposure_time: int = cfg.get_option("camera_exp")
    analog_gain: int = cfg.get_option("camera_gain")
    library_path = Path(cfg.get_option("camera_library_path"))
    camera_hardware = CameraASI(exposure_time, analog_gain, library_path)
    camera_hardware.get_image_loop(
        shared_state, camera_image, command_queue, console_queue, cfg
    )
