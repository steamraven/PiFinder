#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
This module is for GPS related functions

"""
import io
import pynmea2
import serial


def gps_monitor(gps_queue, console_queue):
    ser = serial.Serial("/dev/ttyACM0", 9600, timeout=5.0)
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    gps_locked = False
    while True:
        line = sio.readline()
        msg = pynmea2.parse(line)
        # Ignore any messages without lat/long info
        if not (hasattr(msg, "latitude") and hasattr(msg, "longitude")):
            continue

        if str(msg.sentence_type) == "GGA" and msg.latitude + msg.longitude != 0:
            if gps_locked == False:
                console_queue.put("GPS: Locked")
                gps_locked = True

            gps_queue.put(msg)
