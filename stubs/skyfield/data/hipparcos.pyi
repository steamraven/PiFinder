URL: str
url = URL
PANDAS_MESSAGE: str

from typing import IO
import pandas

def load_dataframe(fobj: IO[bytes]) -> pandas.DataFrame: ...
