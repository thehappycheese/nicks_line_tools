from typing import Tuple, Sequence

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
