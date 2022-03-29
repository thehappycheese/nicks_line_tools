from __future__ import annotations

import itertools
from typing import Any
from typing import Collection
from typing import Iterable
from typing import Sequence
from typing import Tuple

from .util import nicks_itertools

Interval = Tuple[float, float]

SUB_RESULT_ALL = 4
SUB_RESULT_BOTH_ENDS = 3
SUB_RESULT_START = 1
SUB_RESULT_END = 2
SUB_RESULT_NONE = 0


def interval_subtraction(ab: Interval, cd: Interval) -> Tuple[int, Sequence[Interval]]:
	"""returns (relation, ab - cd)
	where relation is an integer describing the part of ab that is returned
	0: none
	1: start_of_ab_returned
	2: end_of_ab_returned
	3: start_and_end_of_ab returned
	4: all"""
	a, b = ab
	c, d = cd
	cd_contains_ab_lower_bound = c <= a <= d
	cd_contains_ab_upper_bound = c <= b <= d
	
	#     ab:        ╠════╣
	#     cd:  ╠════════════╣
	# result:
	if cd_contains_ab_lower_bound and cd_contains_ab_upper_bound:
		return 0, tuple()
	
	ab_contains_cd_lower_bound = a <= c <= b
	ab_contains_cd_upper_bound = a <= d <= b
	
	#     ab:  ╠════════════╣
	#     cd:        ╠════╣
	# result:  ╠═════╡    ╞═╣
	if ab_contains_cd_lower_bound and ab_contains_cd_upper_bound:
		interim_result = []
		if a != c:
			interim_result.append((a, c))
		if d != b:
			interim_result.append((d, b))
		return (3, interim_result)
	
	#     ab:        ╠══════════╣
	#     cd:  ╠════════════╣
	# result:               ╞═══╣
	if cd_contains_ab_lower_bound:
		if d != b:
			return (2, ((d, b),))
	
	#     ab:    ╠══════════╣
	#     cd:        ╠════════════╣
	# result:    ╠═══╡
	if cd_contains_ab_upper_bound:
		if a != c:
			return (1, ((a, c),))
	
	# if execution makes it past all above continues, the only remaining possibility is that the intervals are disjoint
	# in this case the entire first interval is output
	
	return (4, (ab,))


def interval_subtract_multiinterval(minuend: Interval, subtrahend: Iterable[Interval]) -> Collection[Interval]:
	""" minuend - subtrahend = difference
	note: only minor adaption of this function would be required to subtract a multi interval from a multi interval"""
	
	bound_list = []
	
	# sorted_link_bounds: Tuple[
	#   bound_value: float; bound value,
	#   bound_side: int; [0=lower bound | 1=upper_bound],
	#   bound_index: int; -1 means minuend and other values mean subtrahend)
	sorted_link_bounds: Iterable[Tuple[float, int, int]] = sorted(
		itertools.chain(
			[(minuend[0], 0, -1), (minuend[1], 1, -1)],
			# [*itertools.chain(*[((item[0], 0, index), (item[1], 1, index)) for index, item in enumerate(subtrahend)])]
			[*itertools.chain(*[((item[0], 0, 0), (item[1], 1, 0)) for item in subtrahend])]
		)
	)
	
	minuend_stack_count = 0
	subtrahend_stack_count = 0
	for current_bound in sorted_link_bounds:
		current_bound_value, current_bound_side, current_bound_index, = current_bound
		# TODO: why is this next value un-used?
		add_bound_to_list = False
		if current_bound_index == -1:
			# minuend
			if current_bound_side == 0:
				# lower_bound
				if minuend_stack_count == 0 and subtrahend_stack_count == 0:
					# minuend rise from zero while outside subtrahend
					bound_list.append(current_bound_value)
				minuend_stack_count += 1
			else:
				# upper_bound
				minuend_stack_count -= 1
				if minuend_stack_count == 0 and subtrahend_stack_count == 0:
					# minuend fall to zero while outside subtrahend
					bound_list.append(current_bound_value)
		else:
			# subtrahend
			if current_bound_side == 0:
				# lower_bound
				if subtrahend_stack_count == 0 and minuend_stack_count > 0:
					# subtrahend rise from zero while inside minuend
					bound_list.append(current_bound_value)
				subtrahend_stack_count += 1
			else:
				# upper_bound
				subtrahend_stack_count -= 1
				if subtrahend_stack_count == 0 and minuend_stack_count > 0:
					# subtrahend fall to zero while inside minuend
					bound_list.append(current_bound_value)
	
	return [(lower_bound, upper_bound) for lower_bound, upper_bound in nicks_itertools.consecutive_disjoint_pairs(bound_list) if lower_bound != upper_bound]
