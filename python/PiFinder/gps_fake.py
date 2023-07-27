#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
This module is for GPS related functions

"""
import time
from typing import NoReturn, Union
from multiprocessing import Queue
from PiFinder.state import Location


def gps_monitor(gps_queue:"Queue[tuple[str, Union[Location,str]]]", console_queue: "Queue[str]") -> NoReturn:
    gps_locked = False
    while True:
        """
        Just sleep for now
        """
        time.sleep(0.5)
