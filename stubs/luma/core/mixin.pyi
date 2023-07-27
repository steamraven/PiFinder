from _typeshed import Incomplete
from typing import Union, Literal
Rotate = Union[Literal[0], Literal[1], Literal[2], Literal[3]]
Mode = Union[Literal["1"], Literal["RGB"], Literal["RGBA"]]
class capabilities:
    width: Incomplete
    height: Incomplete
    size: Incomplete
    bounding_box: Incomplete
    rotate: Incomplete
    mode: Incomplete
    persist: bool
    def capabilities(self, width: int, height: int, rotate: Rotate, mode: Mode = ...) -> None: ...
    def clear(self) -> None: ...
    def preprocess(self, image: Incomplete) -> Incomplete: ...
    def display(self, image: Incomplete) -> None: ...
