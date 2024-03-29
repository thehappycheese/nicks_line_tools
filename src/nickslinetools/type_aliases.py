from typing import Tuple, List, NewType

from .util.Vector2 import Vector2

# Define some type aliases to shorten type declarations
LineSegment = Tuple[Vector2, Vector2]
LineString = List[Vector2]
MeasuredLineString = Tuple[List[Tuple[Vector2, float]], float]
Radians = NewType("Radians", float)
