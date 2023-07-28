#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
This module handles non-volatile config options
"""
import json, os
from pathlib import Path
from typing import Any


class Config:
    def __init__(self):
        """
        load all settings from config file
        """
        cwd = Path.cwd()
        self.config_file_path = Path(cwd, "../config.json")
        self.default_file_path = Path(cwd, "../default_config.json")
        if not os.path.exists(self.config_file_path):
            self._config_dict: dict[str, Any] = {}
        else:
            with open(self.config_file_path, "r") as config_file:
                self._config_dict = json.load(config_file)

        # open default default_config
        with open(self.default_file_path, "r") as config_file:
            self._default_config_dict = json.load(config_file)

    def set_option(self, option: str, value: Any):
        self._config_dict[option] = value
        with open(self.config_file_path, "w") as config_file:
            json.dump(self._config_dict, config_file, indent=4)

    def get_option(self, option: str) -> Any:
        return self._config_dict.get(option, self._default_config_dict[option])
