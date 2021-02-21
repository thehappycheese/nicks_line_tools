import math


def clamp_zero_to_one(inp: float):
	return max(0.0, min(1.0, inp))


def less_than_and_not_close_to(a, b):
	return a < b and not math.isclose(a, b)