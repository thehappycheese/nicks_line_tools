from typing import Tuple, List, NewType

from nicks_line_tools.Vector2 import Vector2

# Define some type aliases to shorten type declarations
LineSegment = Tuple[Vector2, Vector2]
LineString = List[Vector2]
Radians = NewType("Radians", float)