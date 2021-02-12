# Nicks Line Tools

A set of pure python tools for working with linestrings. This library is only useful if you can't use the popular `shapely` library for some reason (`shapely` uses the compiled GEOS library written in C++ and is therefore much faster)

This project has no dependencies outside the standard library, and therefore has no binaries to compile.

## Usage

**Note the implementation of the offset algorithm is not yet completed**
```python
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.offset import linestring_offset

ls = [Vector2(1, 1), Vector2(5, 6), Vector2(12, 8)]

ls_offset = linestring_offset(ls, 5)
```

## Limitations:

- No support for arcs
- No handling of malformed geometry
- Probably cryptic error messages when things go wrong

## Description of Algorithms
### linestring_interpolate()

### linestring_offset()

Implementation loosely inspired by
[Xu-Zheng Liu, Jun-Hai Yong, Guo-Qin Zheng, Jia-Guang Sun. An offset algorithm for polyline curves. Computers in Industry, Elsevier, 2007, 15p. inria-00518005](https://hal.inria.fr/inria-00518005/document)






#### Definitions
```python
from typing import List, Tuple
from nicks_line_tools.Vector2 import Vector2

# define type aliases for convenience:
LineString = List[Vector2]
MultiLineString = List[LineString]
LineSegment = Tuple[Vector2, Vector2]
LineSegmentList = List[Tuple[Vector2, Vector2]]

# declare type of variables used:
original_ls: LineString
offset_ls: LineString
offset_segments: LineSegmentList
raw_offset_ls: LineString

# define basic operations
# intersect(tool:LineString, target:LineString) -> (point_of_intersection:Optional[Vector2], distance_along_target:List[float])
# project(tool:Vector2, target:LineString) -> (nearest_point_on_target_to_tool: Vector2, distance_along_target: float)
# interpolate(distance_along_target:float, target:LineString) -> (point_on_target: Vector2)

```

#### Aim
Given a `LineString`, call it the `original_ls`; the goal is to find the `offset_ls` which is parallel to `original_ls` and offset by the distance `d`

#### Algorithm 0 - Pre-Treatment
1. Pretreatment steps are **not implemented**... these mostly deal with arcs and malformed input geometry

#### Algorithm 1 - Line Extension

2. Offset each `LineSegment` of the `original_ls` by `d`
    1. The resulting `LineSegmentList` is called `offset_segments`
1. For each `segment[i]` in `offset_segments`
    1. Merge `segment[i]` with `segment[i+1]` if co-linear,
    1. extend the `segment[i]` to meet `segment[i+1]`,
    1. truncate of the `segment[i]` to the intersection with `segment[i+1]`, or
    1. insert a new segment after `segment[i]`.
1. TODO: describe the rules used in `connect_offset_segments()`
1. The resulting `LineString` is called the `raw_offset_ls`

#### Algorithm 4 - Dual Clipping:

6. Repeat Algorithm 1 above but offset in the opposite direction (`-d`);
    1. The result of this step is called the `twin_offset_ls`
1. Find the `intersection_points` and `intersection_parameters` between the `raw_offset_ls` and 
    1. `raw_offset_ls`
    1. `original_ls`
    1. `twin_offset_ls`
    
1. The resulting  `MultiLineString` is called `split_offset_mls`
1. If `intersection_points` is empty, then the result is `raw_offset_ls`. Skip to ##??
1. Delete each `LineString` in `split_offset_mls` that intersects the `original_ls` unless the intersection is with the first or last `LineSegment` of `original_ls`
   
1. For each remaining `item:LineString` in `split_offset_mls` find the global closest point(s?) `P` between the `item` and the `original_ls`
    1. For each `point` in `P`
    1. Delete any part of the `raw_offset_line` which is within a circle centered at each `point` in `P`
1. Join for in Join remaining segments to form new linestring(s)




