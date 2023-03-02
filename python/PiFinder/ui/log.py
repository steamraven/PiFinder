#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
This module contains all the UI Module classes

"""
import datetime
import time
from PIL import ImageFont

from PiFinder import solver
from PiFinder.obj_types import OBJ_TYPES
from PiFinder.ui.base import UIModule
from PiFinder import obslog
from skyfield.api import Angle
from skyfield.positionlib import ICRF

RED = (0, 0, 255)


class UILog(UIModule):
    """
    Log an observation of the
    current target

    """

    __title__ = "LOG"
    _config_options = {
        "Transp.": {
            "type": "enum",
            "value": "NA",
            "options": ["NA", "Excl", "VGood", "Good", "Fair", "Poor"],
        },
        "Seeing": {
            "type": "enum",
            "value": "NA",
            "options": ["NA", "Excl", "VGood", "Good", "Fair", "Poor"],
        },
        "Eyepiece": {
            "type": "enum",
            "value": "NA",
            "options": [
                "NA",
                "6mm",
                "13mm",
                "25mm",
            ],
        },
        "Obsability": {
            "type": "enum",
            "value": "NA",
            "options": ["NA", "Easy", "Med", "Hard", "X Hard"],
        },
        "Appeal": {
            "type": "enum",
            "value": "NA",
            "options": ["NA", "Low", "Med", "High", "WOW"],
        },
    }

    def __init__(self, *args):
        super().__init__(*args)
        self.target = None
        self.__catalog_names = self.config_object.get_option("catalogs")
        self._observing_session = None
        self.modal_timer = 0
        self.modal_duration = 0
        self.modal_text = None
        self.font_small = ImageFont.truetype(
            "/home/pifinder/PiFinder/fonts/RobotoMono-Bold.ttf", 8
        )

    def resolve_catalog_name(self, catalog_id):
        """
        Takes catalog_id (single letter) and returns name
        """
        for catalog_name in self.__catalog_names:
            if catalog_name.startswith(catalog_id):
                return catalog_name
        return "UNKN"

    def reset_config(self):
        """
        Resets object specific note items
        """
        # Reset config, but leave seeing/tranparency
        self._config_options["Obsability"]["value"] = "NA"
        self._config_options["Appeal"]["value"] = "NA"

    def record_object(self, _object):
        """
        Creates a session if needed
        then records the current target

        _object should be a target like dict

        These will be jsonified when logging
        """
        # build notes
        notes = {}
        for k, v in self._config_options.items():
            notes[k] = v["value"]

        if self._observing_session == None:
            self._observing_session = obslog.Observation_session(
                self.shared_state, self.__uuid__
            )

        self.reset_config()

        return self._observing_session.log_object(
            catalog=_object["catalog"],
            designation=_object["designation"],
            solution=self.shared_state.solution(),
            notes=notes,
        )

    def key_b(self):
        """
        when B is pressed,
        Just log it with preview image
        """
        session_uuid, obs_id = self.record_object(self.target)
        filename = f"log_{session_uuid}_{obs_id}_low"
        self.command_queues["camera"].put("save:" + filename)

        # Start the timer for the confirm.
        self.modal_timer = time.time()
        self.modal_duration = 2
        self.modal_text = "Logged!"
        self.update()

    def key_c(self):
        """
        when c is pressed,
        photo and log it!
        """
        session_uuid, obs_id = self.record_object(self.target)

        # Start the timer for the confirm.
        self.modal_timer = time.time()
        self.modal_duration = 2
        self.modal_text = "Taking Photo"
        filename = f"log_{session_uuid}_{obs_id}_high"
        self.command_queues["camera"].put("save_hi:" + filename)
        self.update()
        wait = True
        while wait:
            # we need to wait until we have another solve image
            # check every 2 seconds...
            time.sleep(0.2)
            if self.shared_state.last_image_time()[1] > self.modal_timer + 1:
                wait = False
                self.modal_timer = time.time()
                self.modal_duration = 1
                self.modal_text = "Logged!"

    def key_d(self):
        """
        when D (don't) is pressed
        Exit back to chart
        """
        self.reset_config()
        self.switch_to = "UIChart"

    def key_up(self):
        pass

    def key_down(self):
        pass

    def active(self):
        # Make sure we set the logged time to 0 to indicate we
        # have not logged yet
        state_target = self.ui_state["target"]
        if state_target != self.target:
            self.target = state_target
            self.reset_config()
        self.update()

    def update(self, force=False):
        # Clear Screen
        self.draw.rectangle([0, 0, 128, 128], fill=(0, 0, 0))

        if self.modal_text:
            if time.time() - self.modal_timer > self.modal_duration:
                self.switch_to = "UIChart"
                self.modal_text = None
                return self.screen_update()

            padded_text = (" " * int((14 - len(self.modal_text)) / 2)) + self.modal_text

            self.draw.text((0, 50), padded_text, font=self.font_large, fill=RED)
            return self.screen_update()

        if not self.shared_state.solve_state():
            self.draw.text((0, 20), "No Solve Yet", font=self.font_large, fill=RED)
            return self.screen_update()

        if not self.target:
            self.draw.text((0, 20), "No Target Set", font=self.font_large, fill=RED)
            return self.screen_update()

        # Target Name
        line = ""
        line += self.resolve_catalog_name(self.target["catalog"])
        line += str(self.target["designation"])
        self.draw.text((0, 20), line, font=self.font_large, fill=RED)

        # ID Line in BOld
        # Type / Constellation
        object_type = OBJ_TYPES.get(self.target["obj_type"], self.target["obj_type"])
        object_text = f"{object_type: <14} {self.target['const']}"
        self.draw.text((0, 40), object_text, font=self.font_bold, fill=(0, 0, 128))

        # Notes Prompt
        self.draw.text(
            (15, 100), "Hold A for notes", font=self.font_base, fill=(0, 0, 128)
        )

        # Distance to target
        solution = self.shared_state.solution()
        pointing_pos = ICRF.from_radec(
            ra_hours=Angle(degrees=solution["RA"])._hours,
            dec_degrees=solution["Dec"],
        )

        target_pos = ICRF.from_radec(
            ra_hours=Angle(degrees=self.target["ra"])._hours,
            dec_degrees=self.target["dec"],
        )

        distance = pointing_pos.separation_from(target_pos)
        self.draw.text(
            (5, 60),
            f"Pointing {distance.degrees:0.1f} deg",
            font=self.font_bold,
            fill=(0, 0, 128),
        )
        self.draw.text((5, 75), f"from target", font=self.font_bold, fill=(0, 0, 128))

        # Notes Prompt
        self.draw.text(
            (15, 100), "Hold A for notes", font=self.font_base, fill=(0, 0, 128)
        )

        # Bottom button help
        self.draw.rectangle([0, 118, 40, 128], fill=(0, 0, 32))
        self.draw.text((2, 117), "B", font=self.font_small, fill=RED)
        self.draw.text((10, 117), "Log", font=self.font_small, fill=(0, 0, 128))
        self.draw.rectangle([44, 118, 84, 128], fill=(0, 0, 32))
        self.draw.text((46, 117), "C", font=self.font_small, fill=RED)
        self.draw.text((54, 117), "Photo", font=self.font_small, fill=(0, 0, 128))
        self.draw.rectangle([88, 118, 128, 128], fill=(0, 0, 32))
        self.draw.text((90, 117), "D", font=self.font_small, fill=RED)
        self.draw.text((98, 117), "Abort", font=self.font_small, fill=(0, 0, 128))

        return self.screen_update()
