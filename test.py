from typing import List

import matplotlib.pyplot as plt

from nicks_line_tools.Vector2 import Vector2
import nicks_line_tools.offset as lt

squig = [
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


plot_LineString(squig, True, color="r")
offsets = [lt.connect_offset_segments(item) for item in lt.offset_segments(squig, 0.5)]
for offset_c in offsets:
	plot_LineString(offset_c, False, color="g")

intersects_p = lt.self_intersection(offsets[0])
intersects_o = lt.intersection(offsets[0], squig)
intersects_n = lt.intersection(offsets[0], offsets[1])

plot_Points(lt.params_to_points(offsets[0], intersects_o), True, color="tab:grey", zorder=10)
plot_Points(lt.params_to_points(offsets[0], intersects_p), True, color="tab:blue", zorder=10)
plot_Points(lt.params_to_points(offsets[0], intersects_n), True, color="tab:purple", zorder=10)

plt.show()
