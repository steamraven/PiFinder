from . import Image as Image
from _typeshed import Incomplete
from typing_extensions import TypeAlias

def getrgb(color): ...
def getcolor(color, mode): ...

colormap: Incomplete

_RGB: TypeAlias = tuple[int, int, int] | tuple[int, int, int, int]
_Ink: TypeAlias = str | int | _RGB
_GreyScale: TypeAlias = tuple[int, int]