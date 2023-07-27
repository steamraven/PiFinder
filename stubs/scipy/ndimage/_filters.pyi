from _typeshed import Incomplete
from typing import TypeVar
import numpy as np
import numpy.typing as npt

A = TypeVar("A", bound=np.generic)

def correlate1d(input, weights, axis: int = ..., output: Incomplete | None = ..., mode: str = ..., cval: float = ..., origin: int = ...): ...
def convolve1d(input, weights, axis: int = ..., output: Incomplete | None = ..., mode: str = ..., cval: float = ..., origin: int = ...): ...
def gaussian_filter1d(input, sigma, axis: int = ..., order: int = ..., output: Incomplete | None = ..., mode: str = ..., cval: float = ..., truncate: float = ..., *, radius: Incomplete | None = ...): ...
def gaussian_filter(input, sigma, order: int = ..., output: Incomplete | None = ..., mode: str = ..., cval: float = ..., truncate: float = ..., *, radius: Incomplete | None = ..., axes: Incomplete | None = ...): ...
def prewitt(input, axis: int = ..., output: Incomplete | None = ..., mode: str = ..., cval: float = ...): ...
def sobel(input, axis: int = ..., output: Incomplete | None = ..., mode: str = ..., cval: float = ...): ...
def generic_laplace(input, derivative2, output: Incomplete | None = ..., mode: str = ..., cval: float = ..., extra_arguments=..., extra_keywords: Incomplete | None = ...): ...
def laplace(input, output: Incomplete | None = ..., mode: str = ..., cval: float = ...): ...
def gaussian_laplace(input, sigma, output: Incomplete | None = ..., mode: str = ..., cval: float = ..., **kwargs): ...
def generic_gradient_magnitude(input, derivative, output: Incomplete | None = ..., mode: str = ..., cval: float = ..., extra_arguments=..., extra_keywords: Incomplete | None = ...): ...
def gaussian_gradient_magnitude(input, sigma, output: Incomplete | None = ..., mode: str = ..., cval: float = ..., **kwargs): ...
def correlate(input, weights, output: Incomplete | None = ..., mode: str = ..., cval: float = ..., origin: int = ...): ...
def convolve(input, weights, output: Incomplete | None = ..., mode: str = ..., cval: float = ..., origin: int = ...): ...
def uniform_filter1d(input, size, axis: int = ..., output: Incomplete | None = ..., mode: str = ..., cval: float = ..., origin: int = ...): ...
def uniform_filter(input: npt.NDArray[A], size: int = ..., output: Incomplete | None = ..., mode: str = ..., cval: float = ..., origin: int = ..., *, axes: Incomplete | None = ...) -> npt.NDArray[A]: ...
def minimum_filter1d(input, size, axis: int = ..., output: Incomplete | None = ..., mode: str = ..., cval: float = ..., origin: int = ...): ...
def maximum_filter1d(input, size, axis: int = ..., output: Incomplete | None = ..., mode: str = ..., cval: float = ..., origin: int = ...): ...
def minimum_filter(input, size: Incomplete | None = ..., footprint: Incomplete | None = ..., output: Incomplete | None = ..., mode: str = ..., cval: float = ..., origin: int = ..., *, axes: Incomplete | None = ...): ...
def maximum_filter(input, size: Incomplete | None = ..., footprint: Incomplete | None = ..., output: Incomplete | None = ..., mode: str = ..., cval: float = ..., origin: int = ..., *, axes: Incomplete | None = ...): ...
def rank_filter(input, rank, size: Incomplete | None = ..., footprint: Incomplete | None = ..., output: Incomplete | None = ..., mode: str = ..., cval: float = ..., origin: int = ..., *, axes: Incomplete | None = ...): ...
def median_filter(input, size: Incomplete | None = ..., footprint: Incomplete | None = ..., output: Incomplete | None = ..., mode: str = ..., cval: float = ..., origin: int = ..., *, axes: Incomplete | None = ...): ...
def percentile_filter(input, percentile, size: Incomplete | None = ..., footprint: Incomplete | None = ..., output: Incomplete | None = ..., mode: str = ..., cval: float = ..., origin: int = ..., *, axes: Incomplete | None = ...): ...
def generic_filter1d(input, function, filter_size, axis: int = ..., output: Incomplete | None = ..., mode: str = ..., cval: float = ..., origin: int = ..., extra_arguments=..., extra_keywords: Incomplete | None = ...): ...
def generic_filter(input, function, size: Incomplete | None = ..., footprint: Incomplete | None = ..., output: Incomplete | None = ..., mode: str = ..., cval: float = ..., origin: int = ..., extra_arguments=..., extra_keywords: Incomplete | None = ...): ...