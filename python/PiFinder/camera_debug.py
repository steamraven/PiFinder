#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
This module is the camera
* Captures images
* Places preview images in queue
* Places solver images in queue
* Takes full res images on demand

"""
import os
import queue
import time
from PIL import Image
from PiFinder import config
from PiFinder import utils
from PiFinder.camera_interface import CameraInterface
from PiFinder.state import SharedStateObj
import PiFinder.utils
from multiprocessing import Queue


class CameraDebug(CameraInterface):
    """The debug camera class.  Implements the CameraInterface interface.

    Loads an image from disk and returns it for each exposure

    """

    def __init__(self) -> None:
        self.camType = "Debug camera"
        self.path = utils.pifinder_dir / "test_images"
        self.exposure_time = 1000
        self.gain = 10

    def initialize(self) -> None:
        pass

    def capture(self) -> Image.Image:
        return Image.open(self.path / "pifinder_debug.png")

    def capture_file(self, filename: str) -> None:
        print("capture_file not implemented")
        pass

    def set_camera_config(
        self, exposure_time: float, gain: float
    ) -> tuple[float, float]:
        return exposure_time, gain

    def get_cam_type(self) -> str:
        return self.camType


def get_images(shared_state: SharedStateObj, camera_image: Image.Image, command_queue: "Queue[str]", console_queue: "Queue[str]"):
    """
    Instantiates the camera hardware
    then calls the universal image loop
    """

    cfg = config.Config()
    camera_hardware = CameraDebug()
    camera_hardware.get_image_loop(
        shared_state, camera_image, command_queue, console_queue, cfg
    )
