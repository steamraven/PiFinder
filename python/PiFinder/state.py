#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This module contains the shared state
    object.
"""
import time
import datetime
from typing import Optional
from typing_extensions import TypedDict
from PIL.Image import Image
import pytz

IMUPos = tuple[float,float,float]

class Location(TypedDict):
    lat: float
    lon: float
    altitude: float
    timezone: Optional[str]
    gps_lock: bool

class IMUData(TypedDict):
    moving: bool
    move_start: float
    move_end: float
    pos: Optional[IMUPos]
    start_pos: list[int]
    status: int

class Solution(TypedDict):
    RA: float
    Dec: float
    Alt: float
    Az: float 
    solve_source: str 
    imu_pos: Optional[IMUPos]
    constellation: str
    solve_time: float
    cam_solve_time: float
    Roll: float
    Matches: Optional[str]
    
class PartialSolution(TypedDict):
    RA: float
    Dec: float
    imu_pos: Optional[IMUPos]
    solve_time: float
    cam_solve_time: float
    Roll: float

class ImageMetadata(TypedDict):
    exposure_start: float
    exposure_end: float
    imu: Optional[IMUData]

class CatObject(TypedDict):
    ra: float
    dec: float
    catalog: str
    sequence: int
    obj_type: str
    const: str
    mag: str
    size: int
    desc: str

class UIState(TypedDict):
        history_list: list[CatObject]
        observing_list: list[CatObject]
        target: Optional[CatObject]
        message_timeout: float
        active_list: list[CatObject]

class SharedStateObj:
    def __init__(self):
        self.__power_state: int = 1
        self.__solve_state = False
        self.__last_image_metadata: ImageMetadata = {
            "exposure_start": 0,
            "exposure_end": 0,
            "imu": None,
        }
        self.__solution: Optional[Solution] = None
        self.__imu = None
        self.__location: Optional[Location] = None
        self.__datetime: Optional[datetime.datetime] = None
        self.__datetime_time: Optional[float] = None
        self.__target = None
        self.__screen: Optional[Image] = None

    def power_state(self):
        return self.__power_state

    def set_power_state(self, v: int):
        self.__power_state = v

    def solve_state(self):
        return self.__solve_state

    def set_solve_state(self, v: bool):
        self.__solve_state = v

    def imu(self):
        return self.__imu

    def set_imu(self, v: IMUData):
        self.__imu = v

    def solution(self):
        return self.__solution

    def set_solution(self, v: Solution):
        self.__solution = v

    def location(self):
        return self.__location

    def set_location(self, v: Location):
        self.__location = v

    def last_image_metadata(self):
        return self.__last_image_metadata

    def set_last_image_metadata(self, v: ImageMetadata):
        self.__last_image_metadata = v

    def datetime(self):
        if self.__datetime is None:
            return self.__datetime
        assert self.__datetime_time,  "__datatome_time should be set when __datetime is set"
        return self.__datetime + datetime.timedelta(
            seconds=time.time() - self.__datetime_time
        )

    def local_datetime(self):
        if self.__datetime is None:
            return self.__datetime

        if not self.__location:
            return self.datetime()

        dt = self.datetime()
        assert dt, "datetime() is not none if __datetime is not None"
        assert "timezone" in self.__location and self.__location["timezone"] is not None, "timezone set from last_location in config"
        return dt.astimezone(pytz.timezone(self.__location["timezone"]))

    def set_datetime(self, dt: "datetime.datetime"):
        if dt.tzname() is None:
            utc_tz = pytz.timezone("UTC")
            dt = utc_tz.localize(dt)

        if self.__datetime is None:
            self.__datetime_time = time.time()
            self.__datetime = dt
        else:
            # only reset if there is some significant diff
            # as some gps recievers send multiple updates that can
            # rewind and fastforward the clock
            assert self.__datetime_time, "__datatome_time should be set when __datetime is set"
            curtime = self.__datetime + datetime.timedelta(
                seconds=time.time() - self.__datetime_time
            )
            if curtime > dt:
                diff = (curtime - dt).seconds
            else:
                diff = (dt - curtime).seconds
            if diff > 60:
                self.__datetime_time = time.time()
                self.__datetime = dt

    def screen(self):
        return self.__screen

    def set_screen(self, v: Image):
        self.__screen = v
