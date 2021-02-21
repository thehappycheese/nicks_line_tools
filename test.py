import itertools
from typing import List

import matplotlib.pyplot as plt

from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.linestring_offset import linestring_offset
from nicks_line_tools.linestring_parameters import linestring_params_to_points
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


fig, axs = plt.subplots(2, 2)

params, offset_positive, offset_negative, filtered, splits, closest_point_clipped_linestrings, closest_points_for_plot = linestring_offset(linestring_to_offset, TEST_OFFSET)
axs = [*itertools.chain(axs[0],axs[1])]
for ax in axs:
	plot_LineString(ax, linestring_to_offset, False, color="dimgrey")
	# plot_LineString(offset_positive, False, color="grey")
	# plot_LineString(ax, offset_negative, False, color="grey")
	
	points = linestring_params_to_points(offset_positive, params)
	plot_Points(ax, points)

for linestring, color in zip(splits, ["brown", "darkorange", "teal", "olivedrab", "goldenrod", "seagreen", "royalblue", "rebeccapurple", "mediumvioletred", "dodgerblue", "firebrick", "brown", "darkorange", "teal", "olivedrab", "goldenrod", "seagreen", "royalblue", ]):
	plot_LineString(axs[0], linestring, False, color=color)

for linestring, color in zip(filtered, ["brown", "darkorange", "teal", "olivedrab", "goldenrod", "seagreen", "royalblue", "rebeccapurple", "mediumvioletred", "dodgerblue", "firebrick", "brown", "darkorange", "teal", "olivedrab", "goldenrod", "seagreen", "royalblue", ]):
	plot_LineString(axs[1], linestring, False, color=color)

for linestring, color in zip(closest_point_clipped_linestrings, ["brown", "darkorange", "teal", "olivedrab", "goldenrod", "seagreen", "royalblue", "rebeccapurple", "mediumvioletred", "dodgerblue", "firebrick", "brown", "darkorange", "teal", "olivedrab", "goldenrod", "seagreen", "royalblue", ]):
	plot_LineString(axs[2], linestring, False, color=color)

for point in closest_points_for_plot:
	axs[2].add_patch(plt.Circle(point, TEST_OFFSET, fill=False, linewidth=1))

closest_point_clipped_linestrings_pos = closest_point_clipped_linestrings
params, offset_positive, offset_negative, filtered, splits, closest_point_clipped_linestrings, closest_points_for_plot = linestring_offset(linestring_to_offset, -TEST_OFFSET)
for linestring in itertools.chain(closest_point_clipped_linestrings, closest_point_clipped_linestrings_pos):
	plot_LineString(axs[3], linestring, False, color="red")

plt.show()


def test_circle_cutter():
	ls = [
		Vector2(-1, 4),
		Vector2(2, 2),
		Vector2(4, 5),
		Vector2(5, 4),
		Vector2(4, -2)
	]
	print(ls)
	
	center = Vector2(3, 2)
	radius = 2
	
	for segment in pairwise(ls):
		print(remove_circle_from_linesegment(center, radius, segment))
	print(remove_circle_from_linestring(center, radius, ls))
