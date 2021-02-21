import math
from typing import List
from typing import List
from typing import List

from nicks_line_tools.type_aliases import LineString
from nicks_line_tools.type_aliases import LineString
from nicks_line_tools.type_aliases import LineString
from nicks_line_tools.type_aliases import LineString
from nicks_line_tools.type_aliases import LineString


def linestring_param_to_point(linestring: LineString, param: float):
	a = linestring[math.floor(param)]
	b = linestring[math.ceil(param)]
	return a + (b - a).scaled(param % 1)


def linestring_params_to_points(linestring: LineString, params: List[float]):
	return list(linestring_param_to_point(linestring, param) for param in params)


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