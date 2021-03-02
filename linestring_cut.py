import math

from nicks_line_tools.linestring_interpolate import linestring_interpolate
from nicks_line_tools.linestring_measure import linestring_measure
from nicks_line_tools.type_aliases import LineString


def linestring_cut(linestring: LineString, normalised_distance_along: float):
	# Cuts a line in two at a distance from its starting point
	measured_linestring, total_length = linestring_measure(linestring)
	distance_along = total_length * normalised_distance_along
	
	if distance_along <= 0.0:
		return None, linestring
	if distance_along >= total_length:
		return linestring, None
	else:
		projected_distance_of_vertex = 0
		for index, (vertex, segment_length) in enumerate(measured_linestring):
			if math.isclose(projected_distance_of_vertex, distance_along):
				return (
					linestring[:index + 1],
					linestring[index:]
				)
			if projected_distance_of_vertex > distance_along:
				a = linestring[index],
				b = linestring[index+1]
				new_vertex_at_cut = linestring_interpolate(
					linestring,
					distance_along
				)
				return (
					LineString(linestring_coordinates[:index] + [(new_vertex_at_cut.x, new_vertex_at_cut.y)]),
					LineString([(new_vertex_at_cut.x, new_vertex_at_cut.y)] + linestring_coordinates[index:])
				)
			projected_distance_of_vertex += segment_length
