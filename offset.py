import math
from typing import List
from typing import Optional
from typing import Tuple

from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.nicks_itertools import pairwise

# Define some type aliases to shorten type declarations
from nicks_line_tools.util import clamp_zero_to_one

LineSegment = Tuple[Vector2, Vector2]
LineString = List[Vector2]


def offset_segments(inp: LineString, offset: float) -> Tuple[List[LineSegment], List[LineSegment]]:
	segments_positive: List[LineSegment] = []
	segments_negative: List[LineSegment] = []
	for a, b in zip(inp, inp[1:]):
		offset_vector = (b - a).left.unit.scaled(offset)
		segments_positive.append((a + offset_vector, b + offset_vector))
		segments_negative.append((a - offset_vector, b - offset_vector))
	return segments_positive, segments_negative


def solve_intersection(a: Vector2, b: Vector2, c: Vector2, d: Vector2) -> Optional[Tuple[Vector2, float, float]]:
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
		# 	return None
		
		return None
	else:
		ac = c - a
		time_1 = ac.cross(cd) / ab_cross_cd
		time_2 = -ab.cross(ac) / ab_cross_cd
		return a + ab.scaled(time_1), time_1, time_2


def connect_offset_segments(inp: List[LineSegment]) -> LineString:
	# Algorithm 1 - connect disjoint line segments by extension
	if len(inp) == 1:
		return [*inp[0]]
	result = [inp[0][0]]
	for (a, b), (c, d) in pairwise(inp):
		ab = b - a
		cd = d - c
		
		if math.isclose(ab.cross(cd), 0):
			# consecutive segments are parallel and therefore also collinear
			# Case 1
			result.append(b)
		else:
			# Case 2
			
			# the following function finds the intersection of two line segments and the coefficients such that:
			# p = a + t_ab*ab
			# p = c + t_cd*cd
			# note that t_ab and t_cd are between 0 and 1 when p lies within their respective line segments.
			p, t_ab, t_cd = solve_intersection(a, b, c, d)
			
			# TIP means 'true intersection point' : ie. the intersection point lies within the segment.
			# FIP means 'false intersection point' : ie the intersection point lies outside the segment.
			# PFIP means 'positive false intersection point' : ie the intersection point lies beyond the segment in the direction of the segment
			# NFIP is the 'negative false intersection point' : ie the intersection point lies behind the segment in the direction of the segment
			
			TIP_ab = 0 <= t_ab <= 1
			FIP_ab = not TIP_ab
			PFIP_ab = FIP_ab and t_ab > 0
			# NFIP_ab = FIP_ab and t_ab < 0
			
			TIP_cd = 0 <= t_cd <= 1
			FIP_cd = not TIP_cd
			# PFIP_cd = FIP_cd and t_cd > 0
			# NFIP_cd = FIP_cd and t_cd < 0
			
			if TIP_ab and TIP_cd:
				# Case 2a
				result.append(p)
			elif FIP_ab and FIP_cd:
				# Case 2b.
				if PFIP_ab:
					result.append(p)
				else:
					result.append(b)
					result.append(c)
			else:
				# Case 2c. (either ab or cd
				result.append(b)
				result.append(c)
	
	result.append(d)
	return result


def self_intersection(inp: LineString) -> List[float]:
	intersection_parameters = []
	for i, (a, b) in enumerate(pairwise(inp)):
		for j, (c, d) in enumerate(pairwise(inp[i + 2:])):
			print(f"{i},{i + 1} against {j + i + 2},{j + i + 1 + 2}")
			intersection_result = solve_intersection(a, b, c, d)
			if intersection_result is not None:
				# TODO: collect p to prevent recalculation?
				p, t1, t2 = intersection_result
				if 0 <= t1 <= 1 and 0 <= t2 <= 1:
					param_1 = i + t1
					param_2 = j + i + 2 + t2
					print((param_1, param_2))
					intersection_parameters.append(param_1)
					intersection_parameters.append(param_2)
	last_item = float("inf")
	output = []
	for item in sorted(intersection_parameters):
		if not math.isclose(last_item, item):
			output.append(item)
			last_item = item
	
	return output


def intersection(target: LineString, tool: LineString) -> List[float]:
	"""will return a list of parameters for the target where the tool intersects the target."""
	intersection_parameters = []
	for i, (a, b) in enumerate(pairwise(target)):
		for j, (c, d) in enumerate(pairwise(tool)):
			print(f"{i},{i + 1} against {j + i + 2},{j + i + 1 + 2}")
			intersection_result = solve_intersection(a, b, c, d)
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


def split_at_parameters(inp: LineString, params: List[float]):
	output: List[LineString] = []
	accumulator: LineString = [inp[0]]
	index = 0
	for param in params:
		
		while param > index + 1:
			accumulator.append(inp[index + 1])
			index += 1
		
		a = inp[index]
		b = inp[index + 1]
		
		cut_point = a + (b - a).scaled(param - index)
		accumulator.append(cut_point)
		output.append(accumulator)
		if math.isclose(param - index, 1):
			accumulator = []
		else:
			accumulator = [cut_point]
	
	index += 1
	
	while index < len(inp):
		accumulator.append(inp[index])
		index += 1
	
	output.append(accumulator)
	
	return output


def linestring_params_to_points(inp: LineString, params: List[float]):
	output = []
	for param in params:
		a = inp[math.floor(param)]
		b = inp[math.ceil(param)]
		output.append(a + (b - a).scaled(param % 1))
	return output


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
		return min(result, key=lambda item:item[0])
	else:
		ac = c - a
		time_1 = ac.cross(cd) / ab_cross_cd
		time_2 = -ab.cross(ac) / ab_cross_cd
		if 0 <= time_1 <= 1 and 0 <= time_2 <= 1:
			return 0, a + ab.scaled(time_1)
		else:
			return min(result, key=lambda item:item[0])


def global_closest_point_on_linestring_to_line(linestring: LineString, line: LineSegment) -> (float, Vector2):
	return min((closest_point_on_line_to_line(*item, *line) for item in pairwise(linestring)), key=lambda item: item[0])


def offset_linestring(inp: LineString, offset: float) -> LineString:
	positive_seg, negative_seg = offset_segments(inp, offset)
	positive = connect_offset_segments(positive_seg)
	negative = connect_offset_segments(negative_seg)
	closest_point_on_line_to_line()
