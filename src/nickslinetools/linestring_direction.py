import math
from typing import Optional

from .util.Vector2 import Vector2
from .linestring_measure import linestring_measure
from .util.nicks_itertools import pairwise
from .type_aliases import LineString, Radians


def linestring_direction(line_string: LineString, normalised_distance_along: float) -> Vector2:
	"""returns the direction (as a unit vector) of a linestring segment which contains the point"""
	measured_linestring, line_string_length = linestring_measure(line_string)
	de_normalised_distance_along = line_string_length * normalised_distance_along
	len_so_far = 0
	for (a, ab_len), (b, _) in pairwise(measured_linestring):
		ab = b - a
		len_so_far += ab_len
		if len_so_far >= de_normalised_distance_along:
			return ab / ab_len
	return ab / ab_len
