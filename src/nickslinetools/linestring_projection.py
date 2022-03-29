from typing import Tuple

from .util.Vector2 import Vector2
from .util.nicks_itertools import pairwise
from .type_aliases import LineString
from .util.clamp_zero_to_one import clamp_zero_to_one


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
	t = clamp_zero_to_one(t)
	return t


def project_point_onto_linestring(target: LineString, tool: Vector2) -> Tuple[float, Vector2]:
	"""returns the distance to the linestring, and the point on the line"""
	min_mag_squared = float('inf')
	point = None
	
	for segment in pairwise(target):
		c = tool
		a, b = segment
		# project c onto ab,
		ab = b - a
		ac = c - a
		# p is the projection of c onto ab
		p_scalar = clamp_zero_to_one(ac.dot(ab) / ab.magnitude_squared)
		p = a + ab.scaled(p_scalar)
		pc_magnitude_squared = (p - c).magnitude_squared
		if min_mag_squared > pc_magnitude_squared:
			point = p
			min_mag_squared = pc_magnitude_squared
	return min_mag_squared, point


def project_point_onto_linestring_distance_along(target: LineString, tool: Vector2) -> Tuple[float, Vector2, float]:
	"""returns the distance to the linestring (squared), and the point on the line, and the distance along the line"""
	min_mag_squared = float('inf')
	dist_along_at_min_mag_squared = None
	point = None
	dist_along_so_far = 0
	for segment in pairwise(target):
		c = tool
		a, b = segment
		# project c onto ab,
		ab = b - a
		ac = c - a
		ab_magnitude = ab.magnitude
		# p is the projection of c onto ab, clamped between a and b
		p_scalar = clamp_zero_to_one(ac.dot(ab) / ab.magnitude_squared)
		p = a + ab.scaled(p_scalar)
		pc_magnitude_squared = (p - c).magnitude_squared
		if min_mag_squared > pc_magnitude_squared:
			point = p
			min_mag_squared = pc_magnitude_squared
			dist_along_at_min_mag_squared = dist_along_so_far+p_scalar*ab_magnitude
		dist_along_so_far += ab_magnitude
		
	return min_mag_squared, point, dist_along_at_min_mag_squared