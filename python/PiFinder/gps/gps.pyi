from .client import *
from .watch_options import *
from _typeshed import Incomplete

def isfinite(f: float) -> bool: ...

ONLINE_SET: Incomplete
TIME_SET: Incomplete
TIMERR_SET: Incomplete
LATLON_SET: Incomplete
ALTITUDE_SET: Incomplete
SPEED_SET: Incomplete
TRACK_SET: Incomplete
CLIMB_SET: Incomplete
STATUS_SET: Incomplete
MODE_SET: Incomplete
DOP_SET: Incomplete
HERR_SET: Incomplete
VERR_SET: Incomplete
ATTITUDE_SET: Incomplete
SATELLITE_SET: Incomplete
SPEEDERR_SET: Incomplete
TRACKERR_SET: Incomplete
CLIMBERR_SET: Incomplete
DEVICE_SET: Incomplete
DEVICELIST_SET: Incomplete
DEVICEID_SET: Incomplete
RTCM2_SET: Incomplete
RTCM3_SET: Incomplete
AIS_SET: Incomplete
PACKET_SET: Incomplete
SUBFRAME_SET: Incomplete
GST_SET: Incomplete
VERSION_SET: Incomplete
POLICY_SET: Incomplete
LOGMESSAGE_SET: Incomplete
ERROR_SET: Incomplete
TIMEDRIFT_SET: Incomplete
EOF_SET: Incomplete
SET_HIGH_BIT: int
UNION_SET: Incomplete
STATUS_NO_FIX: int
STATUS_FIX: int
STATUS_DGPS_FIX: int
STATUS_RTK_FIX: int
STATUS_RTK_FLT: int
STATUS_DR: int
STATUS_GNSSDR: int
STATUS_TIME: int
STATUS_SIM: int
STATUS_PPS_FIX: int
MODE_NO_FIX: int
MODE_2D: int
MODE_3D: int
MAXCHANNELS: int
SIGNAL_STRENGTH_UNKNOWN: float

class gpsfix:
    altitude: float
    altHAE: float
    altMSL: float
    climb: float
    datum: str
    dgpsAge: int
    dgpsSta: str
    depth: float
    device: str
    ecefx: float
    ecefy: float
    ecefz: float
    ecefvx: float
    ecefvy: float
    ecefvz: float
    ecefpAcc: float
    ecefvAcc: float
    epc: float
    epd: float
    eph: float
    eps: float
    ept: float
    epv: float
    epx: float
    epy: float
    geoidSep: float
    latitude: float
    longitude: float
    magtrack: Incomplete
    magvar: Incomplete
    mode: int
    relN: Incomplete
    relE: Incomplete
    relD: Incomplete
    sep: Incomplete
    speed: Incomplete
    status: Incomplete
    time: Incomplete
    track: Incomplete
    velN: Incomplete
    velE: Incomplete
    velD: Incomplete
    def __init__(self) -> None: ...

class gpsdata:
    class satellite:
        PRN: Incomplete
        elevation: Incomplete
        azimuth: Incomplete
        ss: Incomplete
        used: Incomplete
        def __init__(self, PRN, elevation, azimuth, ss, used: Incomplete | None = ...) -> None: ...
    online: int
    valid: int
    fix: gpsfix
    status: Incomplete
    utc: str | None
    satellites_used: int
    xdop: int
    pdop: float
    epe: float
    satellites: Incomplete
    gps_id: Incomplete
    driver_mode: int
    baudrate: int
    stopbits: int
    cycle: int
    mincycle: int
    device: Incomplete
    devices: Incomplete
    version: Incomplete
    def __init__(self) -> None: ...

class gps(gpscommon, gpsdata, gpsjson):
    activated: Incomplete
    clock_sec: Incomplete
    clock_nsec: Incomplete
    path: str
    precision: int
    real_sec: Incomplete
    real_nsec: Incomplete
    serialmode: str
    def __init__(self, host: str = ..., port=..., verbose: int = ..., mode: int = ..., reconnect: bool = ...) -> None: ...
    def read(self) -> int: ...
    def __next__(self): ...
    def next(self): ...
    def stream(self, flags: int = ..., devpath: Incomplete | None = ...) -> None: ...

def is_sbas(prn): ...
