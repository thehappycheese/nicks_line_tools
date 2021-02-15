from __future__ import annotations
import math
from typing import List

from typing import Optional
from typing import Tuple

from .Vector2 import Vector2
from .nicks_itertools import pairwise

from .util import clamp_zero_to_one

# Define some type aliases to shorten type declarations
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
	if len(inp) == 0:
		return []
	if len(inp) == 1:
		return [*inp[0]]
	result = [inp[0][0]]
	for (a, b), (c, d) in pairwise(inp):
		ab = b - a
		cd = d - c
		
		if math.isclose(ab.cross(cd), 0):
			# If the cross product of the direction vectors is zero,
			# consecutive segments are parallel
			# we know that in the parallel case b==c
			# therefore we can infer that ab and cd are also collinear,
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
	
	result.append(d)  # noqa
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
	"""will return a list of parameters for the target where the tool intersects the target. Parameters are a floating point number where
	0.0 <= parameter <= len(linestring)-1.0
	Parameters that are rounded to the nearest integer are the same as the index of target. Intermediate values represent the interpolated point between vertices on the target linestring."""
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


def linestring_param_to_point(linestring: LineString, param: float):
	a = linestring[math.floor(param)]
	b = linestring[math.ceil(param)]
	return a + (b - a).scaled(param % 1)


def linestring_params_to_points(linestring: LineString, params: List[float]):
	return list(linestring_param_to_point(linestring, param) for param in params)


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


def global_closest_point_on_linestring_to_line(linestring: LineString, line: LineSegment) -> (float, Vector2):
	return min((closest_point_on_line_to_line(*item, *line) for item in pairwise(linestring)), key=lambda item: item[0])


def remove_circle_from_line(intersection_point: Vector2, offset: float, line_segment: LineSegment) -> List[LineSegment]:
	c = intersection_point
	a, b = line_segment
	# project c onto ab (line segment)
	ab = b - a
	ac = c - a
	ab_magnitude_squared = ab.magnitude_squared
	c_on_ab = a + ab.scaled(ac.dot(ab) / ab_magnitude_squared)
	dist_c = (c_on_ab - c).magnitude
	if dist_c>d:
		return line_segment
	else:
		# find sidepoints with trig?
	result.append((dist_c_sq, c_on_ab))
	pass


def remove_circle_from_linestring(intersection_point: Vector2, offset: float, line_string: LineString) -> List[LineSegment]:
	pass


def linestring_offset(input_linestring: LineString, offset: float) -> LineString:
	positive_segments, negative_segments = offset_segments(input_linestring, offset)
	
	# Step 1a
	positive_linestring = connect_offset_segments(positive_segments)
	negative_linestring = connect_offset_segments(negative_segments)
	
	# Step 1b
	intersection_parameters = sorted([
		*(item, 1 for item in self_intersection(positive_linestring)),
		*(item, -1 for item in intersection(positive_linestring, negative_linestring))
	])
	if len(intersection_parameters) == 0:
		# Case 1
		pass  # TODO: skip
	else:
		# Case 2
		
		offset_positive_split: List[LineString] = split_at_parameters(positive_linestring, intersection_parameters)
		
		filtered_linestrings: List[LineString] = []
		filtered_linestrings_to_be_clipped: List[Tuple[Vector2, LineString]] = []
		for line_string in offset_positive_split:
			intersects_with_original = intersection(input_linestring, line_string)
			if len(intersects_with_original) == 0:
				# Case 1
				filtered_linestrings.append(line_string)
			else:
				# Case 2
				if intersects_with_original:
					# a linestring of len == 4 has vertices 0 to 3 inclusive, and can have parameters that are between 0 and 3 inclusive
					# 0------1------2-----------3
					if all(item < 1 or item > len(line_string) - 1 for item in intersects_with_original):
						# all the intersection points are on input_linestring[0] or input_linestring[-1]
						# TODO: the following line assumes there will be exactly one intersection with the original linestring
						filtered_linestrings_to_be_clipped.append((linestring_param_to_point(input_linestring, intersects_with_original[0]), line_string))
					else:
						pass  # reject linestring
				else:
					filtered_linestrings.append(line_string)
		for intersection_point, line_string in filtered_linestrings_to_be_clipped:
			filtered_linestrings.extend(remove_circle_from_linestring(intersection_point, offset, line_string))
	
	# Delete parts of filtered_linestrings which
	
	return positive_linestring
