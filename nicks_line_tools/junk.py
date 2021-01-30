import math

from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.Vector2 import Vector2


def triangle_area(a: Vector2, b: Vector2, c: Vector2):
	"""for a clockwise triangle this will return the area"""
	# (x1y2 + x2y3 + x3y1 – x1y3 – x2y1 – x3y2) / 2
	# a x b = a.x*b.y - a.y*b.x
	# b x c = b.x*c.y - b.y*c.x
	# c x a = c.x*a.y - c.y*a.x
	# (a.cross(b) + b.cross(c) + c.cross(a)) / 2
	return (
			       a.x * b.y - b.x * a.y +
			       b.x * c.y - c.x * b.y +
			       c.x * a.y - c.y * a.x
	       ) * 0.5


def clockwise(a: Vector2, b: Vector2, c: Vector2):
	return (b - a).left.dot(c - a)


def segments_are_collinear(a: Vector2, b: Vector2, c: Vector2, d: Vector2):
	return (b-a).cross(d-c) == 0


def segments_are_overlapping(a: Vector2, b: Vector2, c: Vector2):
	ab = b - a
	bc = c - b
	inv_det = ab.cross(bc)
	if math.isclose(inv_det, 0):
		# line segments are parallel
		
		return False
	# segments are parallel
	return False