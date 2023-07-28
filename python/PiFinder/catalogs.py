import logging
import sqlite3
import time
import numpy as np
import pandas as pd
from typing import Any, Optional, Union, cast
from PiFinder import calc_utils
import PiFinder.utils as utils
from PiFinder import obslog
from sklearn.neighbors import BallTree

from PiFinder.state import CatObject, SharedStateObj
from PiFinder.ui.base import ConfigOptions

# collection of all catalog-related classes


class Catalog:
    """Keeps catalog data + keeps track of current catalog/object"""

    last_filtered: float = 0

    def __init__(self, catalog_name: str):
        self.name = catalog_name
        self.objects: dict[int, CatObject] = {}
        self.objects_keys_sorted: list[int] = []
        self.filtered_objects: dict[int, CatObject] = {}
        self.filtered_objects_keys_sorted: list[int] = []
        self.max_sequence = 0
        self.desc = "No description"
        self._load_catalog()

    def get_count(self):
        return len(self.objects)

    def get_filtered_count(self):
        return len(self.filtered_objects)

    def _load_catalog(self):
        """
        Loads all catalogs into memory

        """
        self.conn = sqlite3.connect(utils.pifinder_db)
        self.conn.row_factory = sqlite3.Row
        cat_objects = self.conn.execute(
            f"""
            SELECT * from objects
            where catalog='{self.name}'
            order by sequence
        """
        ).fetchall()
        cat_data = self.conn.execute(
            f"""
                SELECT * from catalogs
                where catalog='{self.name}'
            """
        ).fetchone()
        print(cat_data)
        if cat_data:
            self.max_sequence = cat_data["max_sequence"]
            self.desc = cat_data["desc"]
        else:
            logging.debug(f"no catalog data for {self.name}")
        self.objects = {int(dict(row)["sequence"]): dict(row) for row in cat_objects}
        self.objects_keys_sorted = self._get_sorted_keys(self.objects)
        self.filtered_objects = self.objects
        self.filtered_objects_keys_sorted = self.objects_keys_sorted
        assert (
            self.objects_keys_sorted[-1] == self.max_sequence
        ), f"{self.name} max sequence mismatch"
        logging.info(f"loaded {len(self.objects)} objects for {self.name}")
        self.conn.close()

    def _get_sorted_keys(self, dictionary: dict[int, CatObject]):
        return sorted(dictionary.keys())

    def filter(
        self,
        shared_state: SharedStateObj,
        magnitude_filter: Union[str, float],
        type_filter:list[str],
        altitude_filter: Union[str, float],
        observed_filter: str,
    ):
        """
        Does filtering based on params
        populates self._filtered_catalog
        from in-memory catalogs
        does not try to maintain current index because it has no notion of that
        should be done in catalog.py
        """
        self.last_filtered = time.time()

        self.filtered_objects: dict[int, CatObject] = {}

        fast_aa = None
        if altitude_filter != "None":
            # setup
            solution = shared_state.solution()
            location = shared_state.location()
            dt = shared_state.datetime()
            if location and dt and solution:
                fast_aa = calc_utils.FastAltAz(
                    location["lat"],
                    location["lon"],
                    dt,
                )

        if observed_filter != "Any":
            # setup
            observed_list = obslog.get_observed_objects()

        for key, obj in self.objects.items():
            # print(f"filtering {obj}")
            include_obj = True

            # try to get object mag to float
            try:
                obj_mag = float(obj["mag"])
            except (ValueError, TypeError):
                obj_mag = 99

            if magnitude_filter != "None" and obj_mag >= magnitude_filter:
                include_obj = False

            if type_filter != ["None"] and obj["obj_type"] not in type_filter:
                include_obj = False

            if fast_aa:
                obj_altitude = fast_aa.radec_to_altaz(
                    obj["ra"],
                    obj["dec"],
                    alt_only=True,
                )
                if obj_altitude < altitude_filter:
                    include_obj = False

            if observed_filter != "Any":
                if (obj["catalog"], obj["sequence"]) in observed_list:
                    if observed_filter == "No":
                        include_obj = False
                else:
                    if observed_filter == "Yes":
                        include_obj = False

            if include_obj:
                self.filtered_objects[key] = obj
        self.filtered_objects_keys_sorted = self._get_sorted_keys(self.filtered_objects)

    def __repr__(self):
        return "catalog repr"
        # return f"Catalog({self.name=}, {self.max_sequence=})"

    def __str__(self):
        return self.__repr__()


class CatalogDesignator:
    """Holds the string that represents the catalog input/search field.
    Usually looks like 'NGC----' or 'M-13'"""

    def __init__(self, catalog_name: str, max_sequence: int):
        self.catalog_name = catalog_name
        self.object_number: int = 0
        self.width = len(str(max_sequence))
        self.field = self.get_designator()

    def set_target(self, catalog_index: int, number:int=0):
        assert len(str(number)) <= self.get_catalog_width()
        self.catalog_index = catalog_index
        self.object_number = number
        self.field = self.get_designator()

    def append_number(self, number: int):
        number_str = str(self.object_number) + str(number)
        if len(number_str) > self.get_catalog_width():
            number_str = number_str[1:]
        self.object_number = int(number_str)
        self.field = self.get_designator()

    def set_number(self, number: int):
        self.object_number = number
        self.field = self.get_designator()

    def has_number(self):
        return self.object_number > 0

    def reset_number(self):
        self.object_number = 0
        self.field = self.get_designator()

    def increment_number(self):
        self.object_number += 1
        self.field = self.get_designator()

    def decrement_number(self):
        self.object_number -= 1
        self.field = self.get_designator()

    def get_catalog_name(self):
        return self.catalog_name

    def get_catalog_width(self):
        return self.width

    def get_designator(self):
        number_str = str(self.object_number) if self.has_number() else ""
        return (
            f"{self.get_catalog_name(): >3} {number_str:->{self.get_catalog_width()}}"
        )

    def __str__(self):
        return self.field

    def __repr__(self):
        return self.field


class CatalogTracker:
    object_tracker: dict[str, Optional[int]]
    designator_tracker: dict[str, CatalogDesignator]
    current: Catalog
    current_catalog_name: str

    def __init__(self, catalog_names: list[str], shared_state:SharedStateObj, config_options: ConfigOptions):
        self.catalog_names = catalog_names
        self.shared_state = shared_state
        self.config_options = config_options
        self.catalogs: dict[str, Catalog] = self._load_catalogs(catalog_names)
        self.designator_tracker = {
            c: CatalogDesignator(c, self.catalogs[c].max_sequence)
            for c in self.catalog_names
        }
        self.set_current_catalog(catalog_names[0])
        self.object_tracker = {c: None for c in self.catalog_names}

    def set_current_catalog(self, catalog_name: str):
        assert catalog_name in self.catalogs, f"{catalog_name} not in {self.catalogs}"
        self.current_catalog = self.catalogs[catalog_name]
        self.current_catalog_name = catalog_name

    def next_catalog(self, direction:int=1):
        current_index = self.catalog_names.index(self.current_catalog_name)
        next_index = (current_index + direction) % len(self.catalog_names)
        self.set_current_catalog(self.catalog_names[next_index])

    def previous_catalog(self):
        self.next_catalog(-1)

    def next_object(self, direction:int=1, filtered:bool=True):
        """
        direction: 1 for next, -1 for previous

        """
        keys_sorted = (
            self.current_catalog.filtered_objects_keys_sorted
            if filtered
            else self.current_catalog.objects_keys_sorted
        )
        current_key = self.object_tracker[self.current_catalog_name]
        designator = self.get_designator()
        # there is no current object, so set the first object the first or last
        if current_key is None or current_key not in keys_sorted:
            next_index = 0 if direction == 1 else len(keys_sorted) - 1
            next_key = keys_sorted[next_index]
            designator.set_number(next_key)

        else:
            current_index = keys_sorted.index(current_key)
            next_index = current_index + direction
            if next_index == -1 or next_index >= len(keys_sorted):
                next_key = None  # hack to get around the fact that 0 is a valid key
                designator.set_number(0)  # todo use -1 in designator as well
            else:
                next_key = keys_sorted[next_index % len(keys_sorted)]
                designator.set_number(next_key)
        self.set_current_object(next_key)
        return self.get_current_object()

    def previous_object(self):
        return self.next_object(-1)

    def get_objects(self, catalogs:Optional[list[str]] = None, filtered:bool=False) -> list[CatObject]:
        catalog_list = self._select_catalogs(catalogs)
        object_values: list[CatObject] = []
        for catalog in catalog_list:
            if filtered:
                object_values.extend(catalog.filtered_objects.values())
            else:
                object_values.extend(catalog.objects.values())
        flattened_objects = [obj for entry in catalog_list for obj in object_values]
        return flattened_objects

    def does_filtered_have_current_object(self):
        return (
            self.object_tracker[self.current_catalog_name]
            in self.current_catalog.filtered_objects
        )

    def get_current_object(self):
        object_key = self.object_tracker[self.current_catalog_name]
        if object_key is None:
            return None
        return self.current_catalog.objects[object_key]

    def set_current_object(self, object_number:Optional[int], catalog_name:Optional[str]=None):
        if catalog_name is not None:
            self.set_current_catalog(catalog_name)
        else:
            catalog_name = self.current_catalog_name
        self.object_tracker[catalog_name] = object_number
        self.designator_tracker[catalog_name].set_number(
            object_number if object_number else 0
        )

    def get_designator(self, catalog_name:Optional[str]=None) -> CatalogDesignator:
        catalog_name = self._get_catalog_name(catalog_name)
        return self.designator_tracker[catalog_name]

    def _load_catalogs(self, catalogs: list[str]) -> dict[str, Catalog]:
        result:dict[str, Catalog] = {}
        for catalog in catalogs:
            result[catalog] = Catalog(catalog)
        return result

    def _get_catalog_name(self, catalog: Optional[str]) -> str:
        catalog: str = catalog or self.current_catalog_name
        return catalog

    def _select_catalog(self, catalog: Optional[str]) -> Optional[Catalog]:
        catalog = self._get_catalog_name(catalog)
        return self.catalogs.get(catalog)

    def _select_catalogs(self, catalogs: Optional[list[str]]) -> list[Catalog]:
        catalog_list: list[Catalog] = []
        if catalogs is None:
            catalog_list = [self.current_catalog]
        else:
            catalog_list = [self.catalogs.get(key) for key in catalogs]
        return catalog_list

    def filter(self, catalogs:Optional[list[str]]=None):
        catalog_list: list[Catalog] = self._select_catalogs(catalogs=catalogs)
        magnitude_filter = self.config_options["Magnitude"]["value"]
        type_filter = self.config_options["Obj Types"]["value"]
        altitude_filter = self.config_options["Alt Limit"]["value"]
        observed_filter = self.config_options["Observed"]["value"]

        for catalog in catalog_list:
            catalog.filter(
                self.shared_state,
                magnitude_filter,
                type_filter,
                altitude_filter,
                observed_filter,
            )
        #  do we need this? might just be hiding a bug somewhere
        if self.current_catalog not in catalog_list:
            self.current_catalog.filter(
                self.shared_state,
                magnitude_filter,
                type_filter,
                altitude_filter,
                observed_filter,
            )

    def get_closest_objects(self, ra: float, dec: float, n: int, catalogs:Optional[list[str]] = None) -> list[CatObject]:
        """
        Takes the current catalog or a list of catalogs, gets the filtered
        objects and returns the n closest objects to ra/dec
        """
        catalog_list = self._select_catalogs(catalogs=catalogs)
        catalog_list_flat = [
            obj for catalog in catalog_list for obj in catalog.filtered_objects.values()
        ]
        object_radecs = [
            [np.deg2rad(x["ra"]), np.deg2rad(x["dec"])] for x in catalog_list_flat
        ]
        objects_bt = BallTree(object_radecs, leaf_size=4, metric="haversine")
        query = [[np.deg2rad(ra), np.deg2rad(dec)]]
        _dist, obj_ind = objects_bt.query(query, k=n)
        return [catalog_list_flat[x] for x in obj_ind[0]]

    def __repr__(self):
        return f"CatalogTracker(Current:{self.current_catalog_name} {self.object_tracker[self.current_catalog_name]}, Designator:{self.designator_tracker})"
