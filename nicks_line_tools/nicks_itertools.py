# note that the below recipes are already in the popular more_itertools package. However the goal of this package is zero dependencies.

import itertools


def pairwise(iterable):
	"""s -> (s0,s1), (s1,s2), (s2, s3), ...
	This function will be replaced by builtin implementation in python 3.10"""
	a, b = itertools.tee(iterable)
	next(b, None)
	return zip(a, b)


def grouper(iterable, n, fillvalue=None):
	"""Collect data into fixed-length chunks or blocks"""
	# grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
	args = [iter(iterable)] * n
	return itertools.zip_longest(*args, fillvalue=fillvalue)
