#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
This module is the solver
* Checks IMU
* Plate solves high-res image

"""
import os
import sys
import queue
import pprint
import time
import copy
from multiprocessing import Queue
from typing import Optional, cast, Union
from typing_extensions import TypedDict
import uuid
import json
import datetime
import logging

from PIL import ImageOps, Image
from skyfield.api import (
    wgs84,
    Loader,
    Star,
    Angle,
    position_of_radec,
    load_constellation_map,
)
from skyfield.jpllib import SpiceKernel
from skyfield.positionlib import Barycentric, Geocentric, Geometric, ICRF

from PiFinder.image_util import subtract_background
from PiFinder import config
import PiFinder.utils as utils
from PiFinder.state import SharedStateObj, PartialSolution, Solution

IMU_ALT = 2
IMU_AZ = 0

Position = Union[Barycentric, Geocentric, Geometric, ICRF]

class Skyfield_utils:
    """
    Class to persist various
    expensive items that
    skyfield requires (ephemeris, constellations, etc)
    and provide useful util functions using them.
    """

    def __init__(self):
        load = Loader(utils.astro_data_dir)
        self.eph = cast(SpiceKernel, load("de421.bsp"))
        self.earth = self.eph["earth"]
        self.observer_loc = None
        self.constellation_map = load_constellation_map()
        self.ts = load.timescale()

    def set_location(self, lat:float, lon:float, altitude:float):
        """
        set observing location
        """
        self.observer_loc = self.earth + wgs84.latlon(
            lat,
            lon,
            altitude,
        )

    def altaz_to_radec(self, alt:float, az:float, dt: datetime.datetime):
        """
        returns the ra/dec of a specfic
        apparent alt/az at the given time
        """
        t = self.ts.from_datetime(dt)

        assert self.observer_loc, "altaz_to_radic should only be called after set_location"
        observer = self.observer_loc.at(t)
        a = observer.from_altaz(alt_degrees=alt, az_degrees=az)
        ra, dec, distance = a.radec(epoch=t)
        return ra._degrees, dec._degrees

    def radec_to_altaz(self, ra:float, dec:float, dt: datetime.datetime, atmos:bool=True):
        """
        returns the apparent ALT/AZ of a specfic
        RA/DEC at the given time
        """
        t = self.ts.from_datetime(dt)

        assert self.observer_loc, "set_location must be called before radec_to_altaz"
        observer = cast(Barycentric, self.observer_loc.at(t))
        sky_pos = Star(
            ra=Angle(degrees=ra),
            dec_degrees=dec,
        )

        apparent = observer.observe(sky_pos).apparent()
        if atmos:
            alt, az, distance = apparent.altaz("standard")
        else:
            alt, az, distance = apparent.altaz()
        return alt.degrees, az.degrees

    def radec_to_constellation(self, ra:float, dec:float):
        """
        Take a ra/dec and return the constellation
        """
        sky_pos = position_of_radec(Angle(degrees=ra)._hours, dec)
        return self.constellation_map(sky_pos)


# Create a single instance of the skyfield utils
sf_utils = Skyfield_utils()

class Solving(TypedDict):
    RA: Optional[float]
    Dec: Optional[float]
    Alt: Optional[float]
    Az: Optional[float]
    solve_source: Optional[str]
    imu_pos: Optional[list[int]]
    constellation: Optional[str]
    solve_time: float
    cam_solve_time: float

def integrator(shared_state: SharedStateObj, solver_queue: "Queue[PartialSolution]", console_queue: "Queue[str]"):
    try:
        solved: Solving = {
            "RA": None,
            "Dec": None,
            "imu_pos": None,
            "Alt": None,
            "Az": None,
            "solve_source": None,
            "solve_time": None,
            "cam_solve_time": 0,
            "constellation": None,
        }
        cfg = config.Config()
        if cfg.get_option("screen_direction") == "left":
            left_handed = True
        else:
            left_handed = False

        # This holds the last image solve position info
        # so we can delta for IMU updates
        last_image_solve: Optional[Solving] = None
        last_solved = None
        last_solve_time = time.time()
        while True:
            if shared_state.power_state() == 0:
                time.sleep(0.5)
            else:
                time.sleep(1 / 30)

            # Check for new camera solve in queue
            next_image_solve: Optional[PartialSolution] = None
            try:
                next_image_solve = solver_queue.get(block=False)
            except queue.Empty:
                pass

            if next_image_solve:
                solved = cast(Solving, next_image_solve)
                assert solved["RA"] and solved["Dec"], "RA and Dec set in solver"
                solved["solve_source"] = "CAM"

                # see if we can generate alt/az
                location = shared_state.location()
                dt = shared_state.datetime()

                # see if we can calc alt-az
                solved["Alt"] = None
                solved["Az"] = None
                if location and dt:
                    # We have position and time/date!
                    sf_utils.set_location(
                        location["lat"],
                        location["lon"],
                        location["altitude"],
                    )
                    alt, az = sf_utils.radec_to_altaz(
                        solved["RA"],
                        solved["Dec"],
                        dt,
                    )
                    solved["Alt"] = alt
                    solved["Az"] = az

                last_image_solve = copy.copy(solved)

            # generate new solution by offsetting last camera solve
            # if we don't have an alt/az solve
            # we can't use the IMU
            if solved["Alt"]:
                imu = shared_state.imu()
                if imu:
                    dt = shared_state.datetime()
                    assert dt is not None, "shared_state.datetime() should not be None after being set"
                    if last_image_solve and last_image_solve["Alt"]:
                        assert last_image_solve["Az"], "Az should be set at the same time as Alt"
                        # If we have alt, then we have
                        # a position/time

                        # calc new alt/az
                        lis_imu = last_image_solve["imu_pos"]
                        imu_pos = imu["pos"]
                        if lis_imu is not None and imu_pos is not None:
                            alt_offset = imu_pos[IMU_ALT] - lis_imu[IMU_ALT]
                            if left_handed:
                                alt_offset = ((alt_offset + 180) % 360 - 180) * -1
                            else:
                                alt_offset = (alt_offset + 180) % 360 - 180
                            alt_upd = (last_image_solve["Alt"] - alt_offset) % 360

                            az_offset = imu_pos[IMU_AZ] - lis_imu[IMU_AZ]
                            az_offset = (az_offset + 180) % 360 - 180
                            az_upd = (last_image_solve["Az"] + az_offset) % 360

                            solved["Alt"] = alt_upd
                            solved["Az"] = az_upd

                            # Turn this into RA/DEC
                            solved["RA"], solved["Dec"] = sf_utils.altaz_to_radec(
                                solved["Alt"], solved["Az"], dt
                            )

                            # if abs(alt_offset) + abs(az_offset) > .01:
                            if True:
                                solved["solve_time"] = time.time()
                                # solved["solve_source"] = "IMU"

            # Is the solution new?
            if solved["RA"] and solved["solve_time"] > last_solve_time:
                assert solved["Dec"] is not None, "RA and Dec are set by solver"
                last_solve_time = time.time()
                # Update remaining solved keys
                solved["constellation"] = sf_utils.radec_to_constellation(
                    solved["RA"], solved["Dec"]
                )

                # add solution
                shared_state.set_solution(cast(Solution, solved))
                shared_state.set_solve_state(True)
                last_solved = solved
    except EOFError:
        logging.error("Main no longer running for integrator")
