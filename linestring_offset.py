from __future__ import annotations

import math
from typing import List

from typing import Tuple

from .Vector2 import Vector2
from .linestring_intersection import linesegment_intersection, self_intersection, intersection
from .linestring_parameters import linestring_param_to_point
from .linestring_parameters import split_at_parameters
from .linestring_remove_circle import linestring_remove_circle, remove_circles_from_linestring
from .nicks_itertools import pairwise
from .type_aliases import LineSegment, LineString

from .util import clamp_zero_to_one
from .util import less_than_and_not_close_to


def linestring_offset_segments(inp: LineString, offset: float) -> Tuple[List[LineSegment], List[LineSegment]]:
	segments_positive: List[LineSegment] = []
	segments_negative: List[LineSegment] = []
	for a, b in zip(inp, inp[1:]):
		offset_vector = (b - a).left.unit.scaled(offset)
		segments_positive.append((a + offset_vector, b + offset_vector))
		segments_negative.append((a - offset_vector, b - offset_vector))
	return segments_positive, segments_negative


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
			# TODO: test for mitre limit
			# the following function finds the intersection of two line segments and the coefficients such that:
			# p = a + t_ab*ab
			# p = c + t_cd*cd
			# note that t_ab and t_cd are between 0 and 1 when p lies within their respective line segments.
			p, t_ab, t_cd = linesegment_intersection(a, b, c, d)
			
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
				# TODO: test for mitre limit
				result.append(p)
			elif FIP_ab and FIP_cd:
				# Case 2b.
				if PFIP_ab:
					# TODO: test for mitre limit
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


def closest_point_pairs(target: LineString, tool: LineString, filter_distance: float):
	"""Return all points on 'target' that are closest point pairs with the segments of 'tool' which are less than filter distance"""
	result = []
	filter_distance_sq = filter_distance * filter_distance  # note that this also takes the absolute value of filter_distance
	
	for a, b in pairwise(target):
		ab = b - a
		ab_magnitude_squared = ab.magnitude_squared
		for c, d in pairwise(tool):
			ad = d - a
			ac = c - a
			
			# project c onto ab
			c_on_ab = a + ab.scaled(clamp_zero_to_one(ac.dot(ab) / ab_magnitude_squared))
			dist_c_sq = (c_on_ab - c).magnitude_squared
			# if dist_c_sq <= filter_distance_sq or math.isclose(dist_c_sq, filter_distance_sq):
			# result.append(c_on_ab)
			
			# project d onto ab
			d_on_ab = a + ab.scaled(clamp_zero_to_one(ad.dot(ab) / ab_magnitude_squared))
			dist_d_sq = (d_on_ab - d).magnitude_squared
			# if dist_d_sq <= filter_distance_sq or math.isclose(dist_d_sq, filter_distance_sq):
			# result.append(d_on_ab)
			
			if less_than_and_not_close_to(dist_c_sq, filter_distance_sq) or less_than_and_not_close_to(dist_d_sq, filter_distance_sq):
				if dist_d_sq < dist_c_sq:
					result.append(c_on_ab)
				else:
					result.append(d_on_ab)
	
	return result


def linestring_offset(input_linestring: LineString, d: float) -> LineString:
	offset_segments, offset_segments_twin = linestring_offset_segments(input_linestring, d)
	
	# Step 1a
	positive_linestring = connect_offset_segments(offset_segments)
	negative_linestring = connect_offset_segments(offset_segments_twin)
	
	# Step 1b
	intersection_parameters = sorted([
		*(item for item in self_intersection(positive_linestring)),
		*(item for item in intersection(positive_linestring, negative_linestring))
	])
	offset_positive_split = []
	if len(intersection_parameters) == 0:
		# Case 1
		filtered_linestrings = [positive_linestring]
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
					# example:
					# a linestring of len == 4 has vertices 0 to 3 inclusive, and can have parameters that are between 0 and 3 inclusive
					# 0------1------2-----------3
					if all(parameter < 1 or parameter > len(input_linestring) - 1 for parameter in intersects_with_original):
						# all the intersection points are on input_linestring[0] or input_linestring[-1]
						# TODO: the following line assumes there will be exactly one intersection with the original linestring
						#  seems like it would be straightforward to pass all the points along and cut them all away at once...
						#  would need to implement remove_circles_from_linestring() to make that work
						filtered_linestrings_to_be_clipped.append((
							linestring_param_to_point(positive_linestring, intersects_with_original[0]),
							line_string
						))
					else:
						pass  # reject linestring
				else:
					filtered_linestrings.append(line_string)
		for intersection_point, line_string in filtered_linestrings_to_be_clipped:
			# TODO: devise test. not sure what this does exactly.
			filtered_linestrings.extend(linestring_remove_circle(intersection_point, d, line_string))
	
	# Delete parts of filtered_linestrings which
	closest_points_for_plot = []
	closest_point_clipped_linestrings = []
	for linestring in filtered_linestrings:
		closest_points = closest_point_pairs(input_linestring, linestring, d)
		closest_points_for_plot.extend(closest_points)
		closest_point_clipped_linestrings.extend(
			remove_circles_from_linestring(closest_points, d, linestring)
		)
	
	return intersection_parameters, positive_linestring, negative_linestring, filtered_linestrings, offset_positive_split, closest_point_clipped_linestrings, closest_points_for_plot
