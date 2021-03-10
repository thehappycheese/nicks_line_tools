import itertools
from typing import List

import matplotlib.pyplot as plt

from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.linestring_measure import linestring_measure
from nicks_line_tools.linestring_offset import linestring_offset, linestring_params_to_points
from nicks_line_tools.linestring_remove_circle import remove_circles_from_linestring_2
from nicks_line_tools.nicks_itertools import pairwise
from nicks_line_tools.type_aliases import LineString

TEST_OFFSET = 0.4
linestring_to_offset = [
	Vector2(4.54358180, 5.14493850),
	Vector2(4.40994720, 5.77970350),
	Vector2(4.04245150, 5.81311220),
	Vector2(2.80633010, 4.51017320),
	Vector2(2.77292140, 4.14267750),
	Vector2(4.74403410, 1.10248680),
	Vector2(5.14493850, 1.10248680),
	Vector2(9.88897240, 4.87766880),
	Vector2(10.12283300, 5.27857320),
	Vector2(9.82215500, 5.71288620),
	Vector2(5.71288620, 8.81989430),
	Vector2(4.81085150, 9.15398130),
	Vector2(4.04245150, 8.75307700),
	Vector2(1.70384320, 6.78196420),
	Vector2(1.16930420, 6.08038160),
	Vector2(1.57020850, 5.01130350),
	Vector2(3.60813850, 1.90429540),
	Vector2(4.07586020, 1.70384320),
	Vector2(4.51017320, 2.17156490),
	Vector2(5.54584250, 4.37653850),
	Vector2(5.87992950, 4.71062550),
	Vector2(6.68173820, 4.57699050),
	Vector2(9.85556370, 2.73951270),
	Vector2(7.24750790, 2.77565770),
	Vector2(7.58377290, 1.26952970)
]


# tests tip cut
# TEST_OFFSET = -0.4
# linestring_to_offset = [
# 	Vector2(2.26785710, -4.01599690),
# 	Vector2(6.49646560, -5.48065480),
# 	Vector2(7.91387630, -0.92131696),
# 	Vector2(7.44140620, -0.54334076),
# 	Vector2(3.14192700, -4.39397320)
# ]


def transpose_vector_list(inp):
	out = [[], []]
	for item in inp:
		out[0].append(item.x)
		out[1].append(item.y)
	return out


def plot_LineString(plt, ps: LineString, index_label=False, **kwargs):
	plt.plot(*transpose_vector_list(ps), **kwargs)
	if index_label:
		for index, item in enumerate(ps):
			plt.annotate(index, item)


def plot_Points(plt, ps: List[Vector2], index_label=False, **kwargs):
	plt.scatter(*transpose_vector_list(ps), **kwargs)
	if index_label:
		for index, item in enumerate(ps):
			plt.annotate(index, item)


offset_positive = linestring_offset(linestring_to_offset, TEST_OFFSET)
# axs = [*itertools.chain(axs[0], axs[1])]

plot_LineString(plt, linestring_to_offset, False, color="dimgrey")
for ls in offset_positive:
	plot_LineString(plt, ls, False, color="grey")
#plt.show()






def test_remove_circles_from_linestring():
	a = [Vector2(a, b) for a, b in [[-8.86, 0.99], [-4.98, 4.23], [2.86, 2.95], [4.66, 4.03], [3.34, 6.39], [1.98, 7.39], [-2.34, 7.79]]]
	c = [Vector2(a, b) for a, b in [[-1.98, 4.51], [-0.9, 9.55], [0.98, 9.43], [6.18, 4.19], [2.22, 1.31], [4.74, 7.39], [-6.678259236067627, 2.8118659987476518]]]
	r = 2
	res = remove_circles_from_linestring_2(linestring_measure(a), c, r)
	result = []
	for ls in res:
		for a,b in pairwise(ls):
			result.append(f"Segment(({a.x},{a.y}),({b.x},{b.y}))")
	print(result)
	#print("\r\n".join(result))
	
test_remove_circles_from_linestring()