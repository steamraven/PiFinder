from typing import Union
from collections.abc import Sequence

VERSION: str

HIGH: int
LOW: int

OUT: int
IN: int

HARD_PWM: int
SERIAL: int
I2C: int
SPI: int
UNKNOWN: int
BOARD: int
BCM: int

PUD_OFF: int
PUD_UP: int
PUD_DOWN: int
RISING: int
FALLING: int
BOTH: int

def setup(channel: Union[int, Sequence[int]], direction:int, pull_up_down:int = ..., initial:int = ...) -> None: ...
def setmode(new_mode: int) -> None: ...
def input(channel: int) -> int: ...
