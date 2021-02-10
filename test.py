from typing import List

import matplotlib.pyplot as plt

from .Vector2 import Vector2
from . import offset as lt

original: lt.LineString = [
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


def transpose_vector_list(inp: lt.LineString):
	out = [[], []]
	for item in inp:
		out[0].append(item.x)
		out[1].append(item.y)
	return out


def plot_LineString(ps: lt.LineString, index_label=False, **kwargs):
	plt.plot(*transpose_vector_list(ps), **kwargs)
	if index_label:
		for index, item in enumerate(ps):
			plt.annotate(index, item)


def plot_Points(ps: List[Vector2], index_label=False, **kwargs):
	plt.scatter(*transpose_vector_list(ps), **kwargs)
	if index_label:
		for index, item in enumerate(ps):
			plt.annotate(index, item)


plot_LineString(original, True, color="b")
offset_positive, offset_negative = [
	lt.connect_offset_segments(item) for item in lt.offset_segments(original, 0.5)

]
plot_LineString(offset_positive, False, color="g")
plot_LineString(offset_negative, False, color="r")

intersection_parameters = sorted([
	*((item, 'pos') for item in lt.self_intersection(offset_positive)),
	*((item, 'org') for item in lt.intersection(offset_positive, original)),
	*((item, 'neg') for item in lt.intersection(offset_positive, offset_negative))
])

plot_Points(lt.linestring_params_to_points(offset_positive, [item[0] for item in intersection_parameters if item[1] == "pos"]), False, color="g", zorder=10)
plot_Points(lt.linestring_params_to_points(offset_positive, [item[0] for item in intersection_parameters if item[1] == "org"]), False, color="b", zorder=10)
plot_Points(lt.linestring_params_to_points(offset_positive, [item[0] for item in intersection_parameters if item[1] == "neg"]), False, color="r", zorder=10)

split_segments = lt.split_at_parameters(offset_positive, [item[0] for item in intersection_parameters])

filtered_segments = [
	item for index, item in enumerate(split_segments)
	if index == 0 or index >= len(intersection_parameters) or (intersection_parameters[index][1] != "org" and intersection_parameters[index - 1][1] != "org")
]
for ls in filtered_segments:
	plot_LineString(ls, False, color="magenta")

plt.show()
