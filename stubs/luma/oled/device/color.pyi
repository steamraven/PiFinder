from _typeshed import Incomplete

import abc
from abc import ABCMeta
from luma.core.device import device as device
#from luma.oled.device.framebuffer_mixin import __framebuffer_mixin

class color_device(device, metaclass=abc.ABCMeta):
    __metaclass__ = ABCMeta
    def __init__(self, serial_interface: Incomplete, width: Incomplete, height: Incomplete, rotate: Incomplete, framebuffer: Incomplete, **kwargs: Incomplete) -> None: ...
    def display(self, image: Incomplete) -> None: ...
