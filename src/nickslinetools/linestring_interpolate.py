from typing import List

from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.linestring_length import linestring_length
from nicks_line_tools.linestring_measure import linestring_measure
from nicks_line_tools.nicks_itertools import pairwise


def linestring_interpolate_normalised(linestring: List[Vector2], normalised_distance: float):
	linestring_measured, total_length = linestring_measure(linestring)
	real_distance_along = normalised_distance * total_length
	
	dist = 0
	for (a, ab_len), (b, _) in pairwise(linestring_measured):
		ab = b - a
		if dist + ab_len >= real_distance_along:
			return a + ab.scaled((real_distance_along - dist) / ab_len)
		dist += ab_len
	
	return a + ab.scaled((real_distance_along - dist + 1) / ab_len)


def linestring_interpolate(linestring: List[Vector2], real_distance_along: float):
	dist = 0
	for a, b in pairwise(linestring):
		ab = b - a
		ab_len = ab.magnitude
		if dist + ab_len >= real_distance_along:
			return a + ab.scaled((real_distance_along - dist) / ab_len)
		dist += ab_len
	
	return a + ab.scaled((real_distance_along - dist + 1) / ab_len)
