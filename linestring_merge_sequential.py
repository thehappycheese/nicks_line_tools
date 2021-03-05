from typing import List

from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.type_aliases import LineString
from util.convert_metres_to_degrees import convert_metres_to_degrees

SNAP_TOLERANCE_SQ = convert_metres_to_degrees(0.8) ** 2


def vector_close(a: Vector2, b: Vector2):
	return (b - a).magnitude_squared < SNAP_TOLERANCE_SQ


# TODO: not super confident that this is working yet
def linestring_merge_sequential(linestrings: List[LineString]) -> List[LineString]:
	output = []
	c_out = linestrings[0][:]
	for item in linestrings[1:]:
		if vector_close(c_out[-1], item[0]):
			c_out.extend(item[1:])
		else:
			output.append(c_out)
			c_out = item[:]
	if c_out:
		output.append(c_out)
	return output
