#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
This module is for IMU related functions

"""
import time
from typing import NoReturn
from multiprocessing import Queue
from PiFinder.state import SharedStateObj

QUEUE_LEN = 50
AVG_LEN = 2
MOVE_CHECK_LEN = 10

Quaternion = tuple[float,float,float,float]

class Imu:
    moving = False
    flip = False

    def __init__(self):
        pass

    def moving(self):
        """
        Compares most recent reading
        with past readings
        """
        return self.moving

    def flip(self, quat: Quaternion):
        """
        Compares most recent reading
        with past readings and find
        and filter anomolies
        """
        return self.flip

    def update(self):
        # Throw out non-calibrated data
        pass


def imu_monitor(shared_state: SharedStateObj, console_queue: "Queue[str]" ) -> NoReturn:
    imu = Imu()
    imu_calibrated = False
    imu_data = {
        "moving": False,
        "move_start": None,
        "move_end": None,
        "pos": None,
        "start_pos": None,
        "status": 0,
    }
    while True:
        imu.update()
        time.sleep(0.1)
