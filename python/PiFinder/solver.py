#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
This module is the solver
* runs loop looking for new images
* tries to solve them
* If solved, emits solution into queue

"""
import time
import logging
from typing import cast, Optional
from typing_extensions import TypedDict, NotRequired
from multiprocessing import Queue

from PiFinder.tetra3 import Tetra3
from PiFinder import utils
from PiFinder.state import IMUPos, SharedStateObj, PartialSolution
from PIL.Image import Image


class Solving(TypedDict):
    RA: Optional[float]     # set by tetra3
    Dec: Optional[float]    # set by tetra3
    imu_pos: NotRequired[Optional[IMUPos]]  # set by this function
    solve_time: NotRequired[Optional[float]]  # set by this function
    cam_solve_time: NotRequired[float]  # set by this function
    T_extract: NotRequired[float]   # set by tetra3
    T_solve: NotRequired[float]     # set by tetra3

def solver(shared_state: SharedStateObj, solver_queue: "Queue[PartialSolution]", camera_image: Image, console_queue: "Queue[str]"):
    logging.getLogger("tetra3.Tetra3").addHandler(logging.NullHandler())
    t3 = Tetra3(utils.astro_data_dir / "pifinder_fov10-5_m7_hip.npz")
    last_solve_time = 0
    solved: Solving = {
        "RA": None,
        "Dec": None,
        "imu_pos": None,
        "solve_time": None,
        "cam_solve_time": 0,
    }
    try:
        while True:
            if shared_state.power_state() == 0:
                time.sleep(0.5)
            # use the time the exposure started here to
            # reject images startede before the last solve
            # which might be from the IMU
            last_image_metadata = shared_state.last_image_metadata()
            if last_image_metadata["exposure_end"] > (last_solve_time):
                solve_image = camera_image.copy()

                new_solve = t3.solve_from_image(
                    solve_image, fov_estimate=10.2, fov_max_error=0.5, solve_timeout=100
                )

                solved |= new_solve

                total_tetra_time = solved["T_extract"] + solved["T_solve"]
                if total_tetra_time > 1000:
                    console_queue.put(f"SLV: Long: {total_tetra_time}")

                if solved["RA"] is not None:
                    if last_image_metadata["imu"]:
                        solved["imu_pos"] = last_image_metadata["imu"]["pos"]
                    else:
                        solved["imu_pos"] = None
                    solved["solve_time"] = time.time()
                    solved["cam_solve_time"] = time.time()
                    solver_queue.put(solved)

                last_solve_time = last_image_metadata["exposure_end"]
    except EOFError:
        logging.error("Main no longer running for solver")
