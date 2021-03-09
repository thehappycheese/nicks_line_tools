from typing import List, Tuple

from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.nicks_itertools import pairwise


def linestring_measure(linestring: List[Vector2]) -> Tuple[List[Tuple[Vector2, float]], float]:
	""":returns: ([(point:vector, dist_to_next_point:float), ...], total_length:float)"""
	result = []
	total_length = 0
	for a, b in pairwise(linestring):
		ab_len = (b - a).magnitude
		result.append((a, ab_len))
		total_length += ab_len
	result.append((b, 0))
	return result, total_length

