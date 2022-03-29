from typing import List

from .util.Vector2 import Vector2
from .util.nicks_itertools import pairwise


def linestring_length(linestring: List[Vector2]):
	result = 0
	for a, b in pairwise(linestring):
		result += (b - a).magnitude
	return result