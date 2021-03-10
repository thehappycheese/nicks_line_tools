import math
from typing import Optional, Tuple, List

from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.type_aliases import LineString
from nicks_line_tools.nicks_itertools import pairwise


def linesegment_intersection(a: Vector2, b: Vector2, c: Vector2, d: Vector2) -> Optional[Tuple[Vector2, float, float]]:
	# computes the intersection between two line segments; a to b, and c to d
	
	ab = b - a
	cd = d - c
	
	# The intersection of segments is expressed as a parametric equation
	# where t1 and t2 are unknown scalars
	# note that a real intersection can only happen when 0<=t1<=1 and 0<=t2<=1,
	# a + ab·t1 = c + cd·t2
	
	# This can be rearranged as follows:
	# ab·t1 - cd·t2 = c - a
	
	# by collecting the scalars t1 and -t2 into the column vector T,
	# and by collecting the vectors ab and cd into matrix M:
	# we get the matrix form:
	# [ab_x  cd_x][ t1] = [ac_x]
	# [ab_y  cd_y][-t2]   [ac_y]
	# or
	# M·T=ac
	
	# the determinant of the matrix M is the inverse of the cross product of ab and cd.
	# 1/(ab×cd)
	# Therefore if ab×cd=0 the determinant is undefined and the matrix cannot be inverted
	# This means the lines are
	#   a) parallel and
	#   b) possibly collinear
	
	# pre-multiplying both sides by the inverted 2x2 matrix we get:
	# [ t1] = 1/(ab×cd)·[ cd_y  -cd_x][ac_x]
	# [-t2]             [-ab_y   ab_x][ac_y]
	# or
	# T = M⁻¹·ac
	
	# multiplied out
	# [t1] = 1/(ab_x·cd_y - ab_y·cd_x)·[ cd_y·ac_x - cd_x·ac_y]
	# [t2]                             [-ab_y·ac_x + ab_x·ac_y]
	
	# since it is neat to write cross products in python code, observe that the above is equivalent to:
	# [t1] = [ ac×cd / ab×cd ]
	# [t2] = [ ab×ac / ab×cd ]
	
	ab_cross_cd = ab.cross(cd)
	
	if ab_cross_cd == 0:
		# TODO: this can also happen if either vector is the Zero vector.
		# vectors are not linearly independent; ab and cd are parallel
		# segments are collinear if ac is parallel to ab
		# ac ∥ ab
		# or more conveniently if ac is perpendicular to the left normal of ab
		# ac ⟂ (ab⟂)
		# the left normal of ab = [-ab_y]
		#                         [ ab_x]
		# dot product of perpendicular vectors is zero:
		# if ab.left.dot(ac) == 0:
		# 	# segments are collinear
		# 	# TODO: we can compute the range over which t1 and t2 produce an overlap, if any, here. Doesnt seem to be needed for now.
		# else:
		# 	# segments are parallel
		#   # there is no possible solution result.
		# 	return None
		
		return None
	else:
		ac = c - a
		time_1 = ac.cross(cd) / ab_cross_cd
		time_2 = -ab.cross(ac) / ab_cross_cd
		return a + ab.scaled(time_1), time_1, time_2


def linestring_intersection_with_self(inp: LineString) -> List[float]:
	intersection_parameters = []
	for i, (a, b) in enumerate(pairwise(inp)):
		for j, (c, d) in enumerate(pairwise(inp[i + 2:])):
			# print(f"{i},{i + 1} against {j + i + 2},{j + i + 1 + 2}")
			intersection_result = linesegment_intersection(a, b, c, d)
			if intersection_result is not None:
				# TODO: collect p to prevent recalculation?
				p, t1, t2 = intersection_result
				if 0 <= t1 <= 1 and 0 <= t2 <= 1:
					param_1 = i + t1
					param_2 = j + i + 2 + t2
					# print((param_1, param_2))
					intersection_parameters.append(param_1)
					intersection_parameters.append(param_2)
	last_item = float("inf")
	output = []
	for item in sorted(intersection_parameters):
		if not math.isclose(last_item, item):
			output.append(item)
			last_item = item
	
	return output


def linestring_intersection(target: LineString, tool: LineString) -> List[float]:
	"""will return a list of parameters for the target where the tool intersects the target. Parameters are a floating point number where
	0.0 <= parameter <= len(linestring)-1.0
	Parameters that are rounded to the nearest integer are the same as the index of target. Intermediate values represent the interpolated point between vertices on the target linestring."""
	intersection_parameters = []
	for i, (a, b) in enumerate(pairwise(target)):
		for j, (c, d) in enumerate(pairwise(tool)):
			# print(f"{i},{i + 1} against {j + i + 2},{j + i + 1 + 2}")
			intersection_result = linesegment_intersection(a, b, c, d)
			if intersection_result is not None:
				# TODO: collect p to prevent recalculation?
				p, t1, t2 = intersection_result
				if 0 <= t1 <= 1 and 0 <= t2 <= 1:
					param_1 = i + t1
					
					print(param_1)
					intersection_parameters.append(param_1)
	
	last_item = float("inf")
	output = []
	for item in sorted(intersection_parameters):
		if not math.isclose(last_item, item):
			output.append(item)
			last_item = item
	
	return output