from typing import List

from .util.Vector2 import Vector2
from .type_aliases import LineString

SNAP_TOLERANCE_SQ = 0.000007198193253493374  # 0.8 metres in degrees... probably


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
