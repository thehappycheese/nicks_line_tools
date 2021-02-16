from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.util import clamp_zero_to_one


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