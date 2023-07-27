from _typeshed import Incomplete

def monotonic(): ...
STR_CLASS = basestring
STR_CLASS = str
BINARY_ENCODING: str
polystr = str
polybytes = bytes

def make_std_wrapper(stream): ...
def get_bytes_stream(stream): ...

FEET_TO_METERS: float
METERS_TO_FEET: Incomplete
MILES_TO_METERS: float
METERS_TO_MILES: Incomplete
FATHOMS_TO_METERS: float
METERS_TO_FATHOMS: Incomplete
KNOTS_TO_MPH: Incomplete
KNOTS_TO_KPH: float
MPS_TO_KPH: float
KNOTS_TO_MPS: Incomplete
MPS_TO_MPH: Incomplete
MPS_TO_KNOTS: Incomplete

def Deg2Rad(x): ...
def Rad2Deg(x): ...
def CalcRad(lat): ...
def EarthDistance(c1, c2): ...
def EarthDistanceSmall(c1, c2): ...
def MeterOffset(c1, c2): ...
def isotime(s): ...