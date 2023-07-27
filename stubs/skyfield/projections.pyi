from .functions import length_of as length_of
from .positionlib import Barycentric, Astrometric
from typing import Union, Callable
import pandas

Projection = Callable[
    [Astrometric], 
    Union[
        tuple[float, float], 
        tuple["pandas.Series[float]","pandas.Series[float]"]
    ]
]

def build_stereographic_projection(center: Astrometric) -> Projection: ...
