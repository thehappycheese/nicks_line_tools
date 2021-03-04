import math
from typing import Optional, Tuple
from nicks_line_tools.linestring_measure import linestring_measure
from nicks_line_tools.nicks_itertools import pairwise
from nicks_line_tools.type_aliases import LineString


def linestring_cut(linestring: LineString, normalised_distance_along: float) -> Tuple[Optional[LineString], Optional[LineString]]:
	"""cut linestring at normalised distance along and returns a pair of linestrings"""
	measured_linestring, total_length = linestring_measure(linestring)
	distance_along = total_length * normalised_distance_along
	
	if distance_along < 0.0 or math.isclose(distance_along, 0):
		return None, linestring
	if distance_along > total_length or math.isclose(distance_along, total_length):
		return linestring, None
	else:
		distance_remaining = distance_along
		for index, ((a, segment_length), (b, _)) in enumerate(pairwise(measured_linestring)):
			if math.isclose(0, distance_remaining):
				return (
					linestring[:index + 1],
					linestring[index:]
				)
			elif distance_remaining < segment_length:
				ab = b - a
				intermediate_point = ab / segment_length * distance_remaining
				
				return (
					linestring[:index+1] + [intermediate_point],
					[intermediate_point] + linestring[index+1:]
				)
			distance_remaining -= segment_length