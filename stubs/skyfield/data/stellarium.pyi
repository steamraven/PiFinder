from _typeshed import Incomplete
from typing import NamedTuple, IO

class StarName(NamedTuple):
    hip: Incomplete
    name: Incomplete

def parse_constellations(lines: IO[bytes]) -> list[tuple[ str, list[tuple[int, int]]]]: ...
def parse_star_names(lines): ...
