from _typeshed import Incomplete

from luma.oled.device.color import color_device


class ssd1351(color_device):
    def __init__(self, serial_interface: Incomplete | None = ..., width: int = ..., height: int = ..., rotate: int = ..., framebuffer: Incomplete | None = ..., h_offset: int = ..., v_offset: int = ..., bgr: bool = ...) -> None: ...
    def contrast(self, level: Incomplete) -> None: ...
    def command(self, cmd: Incomplete, *args: Incomplete) -> None: ...


