from .constants import ASEC2RAD as ASEC2RAD, AU_KM as AU_KM, C as C, C_AUDAY as C_AUDAY, DAY_S as DAY_S, T0 as T0
from .functions import length_of as length_of
from .relativity import light_time_difference as light_time_difference
from .timelib import Time as Time
from .units import Angle as Angle
from _typeshed import Incomplete
import pandas

class Star:
    au_km = AU_KM
    target: Incomplete
    ra: Incomplete
    dec: Incomplete
    ra_mas_per_year: Incomplete
    dec_mas_per_year: Incomplete
    parallax_mas: Incomplete
    radial_km_per_s: Incomplete
    epoch: Incomplete
    names: Incomplete
    def __init__(self, ra: Incomplete | None = ..., dec: Incomplete | None = ..., ra_hours: Incomplete | None = ..., dec_degrees: Incomplete | None = ..., ra_mas_per_year: float = ..., dec_mas_per_year: float = ..., parallax_mas: float = ..., radial_km_per_s: float = ..., names=..., epoch=...) -> None: ...
    @classmethod
    def from_dataframe(cls, df: pandas.DataFrame) -> Star: ...
