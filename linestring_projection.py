from typing import Tuple

from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.nicks_itertools import pairwise
from nicks_line_tools.type_aliases import LineString


def scalar_projection_of_point_onto_line(a: Vector2, b: Vector2, p: Vector2) -> float:
	"""project p onto line ab returning scalar t such that a+ab.t is the desired output point."""
	ab = b - a
	ap = p - a
	t = ap.dot(ab) / ab.dot(ab)
	return t


def scalar_projection_of_point_onto_line_segment(a: Vector2, b: Vector2, p: Vector2) -> float:
	"""project p onto line ab returning scalar t such that a+ab.t is the desired output point, where t is clamped between 0 and 1."""
	ab = b - a
	ap = p - a
	t = ap.dot(ab) / ab.dot(ab)
	return max(0.0, min(1.0, t))


def project_point_onto_linestring(target: LineString, tool: Vector2) -> Tuple[float, Vector2]:
	"""project tool onto target and return an point on target that is the minimum distance from the tool. This function does not deal with multiple minimums and simply returns an arbitrary minimum"""
	min_mag_squared = float('inf')
	point = None
	
	for segment in pairwise(target):
		c = tool
		a, b = segment
		# project c onto ab,
		ab = b - a
		ac = c - a
		# p is the projection of c onto ab
		p_scalar = max(0.0, min(1.0, ac.dot(ab) / ab.magnitude_squared))
		p = a + ab.scaled(p_scalar)
		pc_magnitude_squared = (p - c).magnitude_squared
		if min_mag_squared > pc_magnitude_squared:
			point = p
			min_mag_squared = pc_magnitude_squared
	return min_mag_squared, point
