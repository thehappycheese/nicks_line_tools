import math
from typing import Tuple, List

from nicks_line_tools import interval_tools
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.type_aliases import LineSegment, LineString
from nicks_line_tools.nicks_itertools import pairwise


def remove_circle_from_linesegment(circle_center: Vector2, radius: float, line_segment: LineSegment) -> Tuple[int, List[LineSegment]]:
	c = circle_center
	a, b = line_segment
	# project c onto ab,
	ab = b - a
	ac = c - a
	ab_magnitude_squared = ab.magnitude_squared
	if ab_magnitude_squared == 0:
		# TODO: prevent this call from happening
		print("prevent zero length input")
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


def remove_circles_from_linesegment(circle_centers: List[Vector2], radius: float, line_segment: LineSegment) -> Tuple[int, List[LineSegment]]:
	# TODO: to efficiently implement this, we would need to implement interval_tools. subtract_intervals_from_interval()
	#  which is as good as pythons sorted() function for large inputs... but for small inputs the line sweep algorithm would still dominate.
	#  Probably would be better than the while-loop-recursive function currently used
	raise Exception("not implemented")


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
