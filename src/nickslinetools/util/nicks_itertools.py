# note that the below recipes are already in the popular more_itertools package. However the goal of this package is zero dependencies.
import collections.abc
import itertools
from typing import Iterable
from typing import Iterator
from typing import NewType, Tuple, Any

T = NewType("T", Any)


def pairwise(iterable: T) -> Tuple[T, T]:
	"""s -> (s0,s1), (s1,s2), (s2, s3), ...
	This function will be replaced by builtin implementation in python 3.10"""
	a, b = itertools.tee(iterable)
	next(b, None)
	return zip(a, b)


def consecutive_disjoint_pairs(iterable: Iterable[T]) -> Iterator[Tuple[T, T]]:
	"""[1,2,3,4,5] -> ( (1,2), (3,4) )"""
	m = iterable if isinstance(iterable, collections.abc.Iterator) else iter(iterable)
	for a, b in zip(m, m):
		yield a, b


def grouper(iterable, n, fillvalue=None):
	"""Collect data into fixed-length chunks or blocks"""
	# grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
	args = [iter(iterable)] * n
	return itertools.zip_longest(*args, fillvalue=fillvalue)
