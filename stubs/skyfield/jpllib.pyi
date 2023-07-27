from .constants import AU_KM as AU_KM, DAY_S as DAY_S
from .errors import EphemerisRangeError as EphemerisRangeError
from .timelib import compute_calendar_date as compute_calendar_date
from .vectorlib import VectorFunction as VectorFunction, VectorSum as VectorSum
from _typeshed import Incomplete

class SpiceKernel:
    path: Incomplete
    filename: Incomplete
    spk: Incomplete
    segments: Incomplete
    codes: Incomplete
    def __init__(self, path) -> None: ...
    def close(self) -> None: ...
    def comments(self): ...
    def names(self): ...
    def decode(self, name): ...
    def __getitem__(self, target: str) -> VectorSum: ...
    def __contains__(self, name_or_code) -> bool: ...

class SPICESegment(VectorFunction):
    def __new__(cls, ephemeris, spk_segment): ...
    ephemeris: Incomplete
    center: Incomplete
    target: Incomplete
    spk_segment: Incomplete
    def __init__(self, ephemeris, spk_segment) -> None: ...
    @property
    def vector_name(self): ...
    def time_range(self, ts): ...

class ChebyshevPosition(SPICESegment): ...
class ChebyshevPositionVelocity(SPICESegment): ...
