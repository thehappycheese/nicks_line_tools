from typing import List

from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.nicks_itertools import pairwise


def interpolate_linestring(linestring: List[Vector2], normalised_dist: float):
	# TODO: extract function
	linestring_len = 0
	for a, b in pairwise(linestring):
		linestring_len += (b - a).magnitude
	actual_dist = normalised_dist * linestring_len
	
	dist = 0
	for a, b in pairwise(linestring):
		ab = b - a
		ab_len = ab.magnitude
		if dist + ab_len >= actual_dist:
			return ab.scaled((actual_dist - dist) / ab_len)
		dist += ab_len
