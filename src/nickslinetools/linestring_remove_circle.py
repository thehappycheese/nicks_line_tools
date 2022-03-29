import math
from typing import Tuple, List

from . import interval_tools
from .util.Vector2 import Vector2
from .type_aliases import LineSegment, LineString, MeasuredLineString
from .util.nicks_itertools import pairwise


def remove_circle_from_linesegment(circle_center: Vector2, radius: float, line_segment: LineSegment) -> Tuple[int, List[LineSegment]]:
	c = circle_center
	a, b = line_segment
	# project c onto ab,
	ab = b - a
	ac = c - a
	ab_magnitude_squared = ab.magnitude_squared
	if ab_magnitude_squared == 0:
		# TODO: prevent this call from happening
		# print("prevent zero length input")
		return interval_tools.SUB_RESULT_NONE, []
	# p is the projection of c onto ab
	p_scalar = ac.dot(ab) / ab_magnitude_squared
	p = a + ab.scaled(p_scalar)
	pc_magnitude_squared = (p - c).magnitude_squared
	radius_squared = radius * radius
	
	if pc_magnitude_squared > radius_squared or math.isclose(pc_magnitude_squared, radius_squared):
		return interval_tools.SUB_RESULT_ALL, [line_segment]
	
	ab_magnitude = math.sqrt(ab_magnitude_squared)
	half_chord_length_over_ab_mag = math.sqrt(radius_squared - pc_magnitude_squared) / ab_magnitude
	q_scalar = p_scalar - half_chord_length_over_ab_mag
	r_scalar = p_scalar + half_chord_length_over_ab_mag
	
	relation, intervals = interval_tools.interval_subtraction((0, 1), (q_scalar, r_scalar))
	return relation, [(a + ab.scaled(interval[0]), a + ab.scaled(interval[1])) for interval in intervals]


def remove_circles_from_linesegment(line_segment: LineSegment, line_segment_length: float, circle_centers: List[Vector2], radius: float) -> Tuple[Tuple[float, float], List[LineSegment]]:
	# TODO: make work with measured linestring
	# TODO: make pass in radius squared
	a, b = line_segment
	ab = b - a
	ab_magnitude_squared = ab.magnitude_squared
	ab_magnitude = math.sqrt(ab_magnitude_squared)
	radius_squared = radius * radius
	if ab_magnitude_squared == 0:
		raise Exception("must prevent zero length input to remove_circles_from_linesegment")
	intervals_to_subtract = []
	for circle_center in circle_centers:
		# project circle_center onto ab,
		ac = circle_center - a
		p_scalar = ac.dot(ab) / ab_magnitude_squared
		p = a + ab.scaled(p_scalar)
		pc_magnitude_squared = (p - circle_center).magnitude_squared
		if pc_magnitude_squared > radius_squared or math.isclose(pc_magnitude_squared, radius_squared):
			continue
		half_chord_length_over_ab_mag = math.sqrt(radius_squared - pc_magnitude_squared) / ab_magnitude
		intervals_to_subtract.append((
			p_scalar - half_chord_length_over_ab_mag,
			p_scalar + half_chord_length_over_ab_mag
		))
	intervals_to_return = interval_tools.interval_subtract_multiinterval((0, 1), intervals_to_subtract)
	return (intervals_to_subtract[0][0], intervals_to_subtract[-1][1]), [(a + ab.scaled(interval[0]), a + ab.scaled(interval[1])) for interval in intervals_to_return]


def remove_circles_from_linestring_2(measured_linestring: MeasuredLineString, circle_centers: List[Vector2], radius: float):
	"""Second version of this operation that is substantially optimised"""
	result_linestrings = []
	current_linestring = []
	
	for (a, ab_length), (b, _) in pairwise(measured_linestring[0]):
		(first_parameter, last_parameter), line_segments = remove_circles_from_linesegment((a, b), ab_length, circle_centers, radius)
		
		if not line_segments:
			# nothing to add
			continue
		elif len(line_segments) == 1:
			if first_parameter != 0:
				if current_linestring:
					result_linestrings.append(current_linestring)
					current_linestring = []
				current_linestring.append(line_segments[0][0])
			current_linestring.append(line_segments[0][1])
			if last_parameter != 1:
				result_linestrings.append(current_linestring)
				current_linestring = []
		else:
			first_segment = line_segments[0]
			middle_segments = line_segments[1:-1]
			last_segment = line_segments[-1]
			
			if first_parameter == 0:
				if current_linestring:
					current_linestring.append(first_segment[1])
				else:
					current_linestring.extend(first_segment)
				result_linestrings.append(current_linestring)
				current_linestring = []
			else:
				if current_linestring:
					result_linestrings.append(current_linestring)
					current_linestring = []
				result_linestrings.append(list(first_segment))
			
			result_linestrings.extend(list(item) for item in middle_segments)
			
			if last_parameter==1:
				current_linestring.extend(last_segment)
			else:
				result_linestrings.append(list(last_segment))
			
		
	return result_linestrings


def linestring_remove_circle(circle_center: Vector2, radius: float, line_string: LineString) -> List[LineString]:
	results: List[LineString] = []
	sub_result: LineString = []
	
	for line_segment in pairwise(line_string):
		relation, segments = remove_circle_from_linesegment(circle_center, radius, line_segment)
		
		if relation == interval_tools.SUB_RESULT_ALL:
			if len(sub_result) == 0:
				sub_result.append(line_segment[0])
			sub_result.append(line_segment[1])
		else:
			if relation & interval_tools.SUB_RESULT_START:
				if len(sub_result) == 0:
					sub_result.append(line_segment[0])
				sub_result.append(segments[0][1])
				results.append(sub_result)
				sub_result = []
			
			if relation & interval_tools.SUB_RESULT_END:
				sub_result.append(segments[-1][0])
				sub_result.append(line_segment[1])
	
	if sub_result:
		results.append(sub_result)
	return results


def remove_circles_from_linestring(circle_centers: List[Vector2], radius: float, line_string: LineString):
	# TODO: this will have very poor performance...
	#  to implement it in a single pass though we would need to implement remove_circles_from_linesegment()
	result = [line_string]
	for circle_center in circle_centers:
		new_result = []
		for ls in result:
			new_result.extend(linestring_remove_circle(circle_center, radius, ls))
		result = new_result
	return result
