from .functions import load_bundled_npy as load_bundled_npy
from .timelib import Time as Time, julian_date_of_besselian_epoch as julian_date_of_besselian_epoch
from .positionlib import Barycentric, Geocentric, Geometric, ICRF
from typing import Callable, Union

Position = Union[Barycentric, Geocentric, Geometric, ICRF]

def load_constellation_map() -> Callable[[Position],str]: ...
def load_constellation_names(): ...
