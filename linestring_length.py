from typing import List

from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.nicks_itertools import pairwise


def linestring_length(linestring: List[Vector2]):
	result = 0
	for a, b in pairwise(linestring):
		result += (b - a).magnitude
	return result