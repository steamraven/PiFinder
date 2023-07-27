from _typeshed import Incomplete

class i2c:
    def __init__(self, bus: Incomplete | None = ..., port: int = ..., address: int = ...) -> None: ...
    def command(self, *cmd) -> None: ...
    def data(self, data) -> None: ...
    def cleanup(self) -> None: ...

class bitbang:
    def __init__(self, gpio: Incomplete | None = ..., transfer_size: int = ..., reset_hold_time: int = ..., reset_release_time: int = ..., **kwargs) -> None: ...
    def command(self, *cmd) -> None: ...
    def data(self, data) -> None: ...
    def cleanup(self) -> None: ...

class spi(bitbang):
    def __init__(self, spi: Incomplete | None = ..., gpio: Incomplete | None = ..., port: int = ..., device: int = ..., bus_speed_hz: int = ..., transfer_size: int = ..., gpio_DC: int = ..., gpio_RST: int = ..., spi_mode: Incomplete | None = ..., reset_hold_time: int = ..., reset_release_time: int = ...) -> None: ...
    def cleanup(self) -> None: ...

class gpio_cs_spi(spi):
    def __init__(self, *args, **kwargs) -> None: ...
    def cleanup(self) -> None: ...

class noop:
    def __getattr__(self, attr): ...
    def __setattr__(self, attr, val) -> None: ...

class __FTDI_WRAPPER_SPI:
    def __init__(self, controller, spi_port) -> None: ...
    def open(self, port, device) -> None: ...
    def writebytes(self, data) -> None: ...
    def close(self) -> None: ...

class __FTDI_WRAPPER_GPIO:
    LOW: int
    HIGH: int
    OUT: int
    def __init__(self, gpio) -> None: ...
    def setup(self, pin, direction) -> None: ...
    def output(self, pin, value) -> None: ...
    def cleanup(self, pin) -> None: ...

class __FTDI_WRAPPER_I2C:
    def __init__(self, controller, i2c_port) -> None: ...
    def write_i2c_block_data(self, address, register, data) -> None: ...
    def i2c_rdwr(self, message) -> None: ...
    def close(self) -> None: ...

def ftdi_spi(device: str = ..., bus_speed_hz: int = ..., gpio_CS: int = ..., gpio_DC: int = ..., gpio_RST: int = ..., reset_hold_time: int = ..., reset_release_time: int = ...): ...
def ftdi_i2c(device: str = ..., address: int = ...): ...

class pcf8574(i2c):
    def __init__(self, pulse_time=..., backlight_enabled: bool = ..., *args, **kwargs) -> None: ...
    def command(self, *cmd) -> None: ...
    def data(self, data) -> None: ...
