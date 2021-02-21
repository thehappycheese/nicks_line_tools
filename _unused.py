from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.nicks_itertools import pairwise
from nicks_line_tools.type_aliases import LineSegment
from nicks_line_tools.type_aliases import LineString
from nicks_line_tools.util import clamp_zero_to_one
from nicks_line_tools.util import clamp_zero_to_one
from nicks_line_tools.util import clamp_zero_to_one
from nicks_line_tools.util import clamp_zero_to_one


def closest_point_on_line_to_line(a: Vector2, b: Vector2, c: Vector2, d: Vector2) -> (float, Vector2):
	"""the closest point on ab to cd, and the distance_squared"""
	ab = b - a
	cd = d - c
	
	ab_magnitude_squared = ab.magnitude_squared
	cd_magnitude_squared = cd.magnitude_squared
	
	# TODO: handle zero vectors?
	
	ac = c - a
	ad = d - a
	ca = a - c
	cb = b - c
	
	result = []
	
	# project c onto ab
	c_on_ab = a + ab.scaled(clamp_zero_to_one(ac.dot(ab) / ab_magnitude_squared))
	dist_c_sq = (c_on_ab - c).magnitude_squared
	result.append((dist_c_sq, c_on_ab))
	# project d onto ab
	d_on_ab = a + ab.scaled(clamp_zero_to_one(ad.dot(ab) / ab_magnitude_squared))
	dist_d_sq = (d_on_ab - d).magnitude_squared
	result.append((dist_d_sq, d_on_ab))
	
	# project a onto cd
	a_on_cd = c + cd.scaled(clamp_zero_to_one(ca.dot(cd) / cd_magnitude_squared))
	dist_a_sq = (a_on_cd - a).magnitude_squared
	result.append((dist_a_sq, a))
	# project b onto cd
	b_on_cd = c + cd.scaled(clamp_zero_to_one(cb.dot(cd) / cd_magnitude_squared))
	dist_b_sq = (b_on_cd - b).magnitude_squared
	result.append((dist_b_sq, b))
	
	ab_cross_cd = ab.cross(cd)
	
	if ab_cross_cd == 0:
		# vectors are not linearly independent; ab and cd are parallel and maybe collinear
		return min(result, key=lambda item: item[0])
	else:
		ac = c - a
		time_1 = ac.cross(cd) / ab_cross_cd
		time_2 = -ab.cross(ac) / ab_cross_cd
		if 0 <= time_1 <= 1 and 0 <= time_2 <= 1:
			return 0, a + ab.scaled(time_1)
		else:
			return min(result, key=lambda item: item[0])


def closest_point_on_linestring_to_line(linestring: LineString, line: LineSegment) -> (float, Vector2):
	"""the closest point linestring to line, and the distance_squared"""
	# key si required since second member of tuples (Vector2) are not comparable with <
	return min((closest_point_on_line_to_line(*item, *line) for item in pairwise(linestring)), key=lambda item: item[0])