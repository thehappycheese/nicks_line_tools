# Nicks Line Tools

A set of pure python tools for working with linestrings. This library is only useful if you can't use the popular `shapely` library for some reason (`shapely` uses the compiled GEOS library written in C++ and is therefore much faster)

This project has no dependencies outside the standard library, and therefore has no binaries to compile.

## Usage

**Note the implementation of the offset algorithm is not yet completed**

```python
from nicks_line_tools.Vector2 import Vector2
from nicks_line_tools.linestring_offset import linestring_offset

ls = [Vector2(1, 1), Vector2(5, 6), Vector2(12, 8)]

ls_offset = linestring_offset(ls, 5)
```

## Limitations:

- No support for arcs
- No handling of malformed input geometry
- Probably cryptic error messages when things go wrong

## References

Implementation loosely inspired by
[Xu-Zheng Liu, Jun-Hai Yong, Guo-Qin Zheng, Jia-Guang Sun. An offset algorithm for polyline curves. Computers in Industry, Elsevier, 2007, 15p. inria-00518005](https://hal.inria.fr/inria-00518005/document)
This was the first google result for 'line offset algorithm'

> Having implemented the paper as close as I can, I am a bit annoyed with it.
> The algorithm is really described well up untill algorithim 4 step 1b.
> After that it is very hard to decypher. 
> I did get it working, but I think I had to re-invent the last few bits of the algorithim, just going on the gist of what the paper describes.
> I did not implement algorithms 2 and 3, as they deal with curved (arc) segments.





#### Definitions (For the psudocode in this readme only)

Type definitions
```python
from typing import List, Tuple
from nicks_line_tools.Vector2 import Vector2

# define type aliases for convenience:
LineString = List[Vector2]
MultiLineString = List[LineString]
LineSegment = Tuple[Vector2, Vector2]
LineSegmentList = List[Tuple[Vector2, Vector2]]
Parameter = float

# declare type of variables used:
input_linestring: LineString
offset_ls: LineString
offset_segments: LineSegmentList
raw_offset_ls: LineString
```

Function Type Definitions (pseudocode)
```python
intersect = (tool: LineString, target: LineString) -> (point_of_intersection: Optional[Vector2], distance_along_target: List[Parameter])
project = (tool: Vector2, target: LineString) -> (nearest_point_on_target_to_tool: Vector2, distance_along_target: Parameter)
interpolate = (distance_along_target: Parameter, target: LineString) -> (point_on_target: Vector2)
```

#### Aim
Given a `LineString`, call it the `input_linestring`; the goal is to find the `offset_ls` which is parallel to `input_linestring` and offset by the distance `d`


#### Algorithm 0.0 - Pre-Treatment
1. Pretreatment steps are **not implemented**... these mostly deal with arcs and malformed input geometry
1. No check is performed to prevent execution when `d==0`


#### Algorithm 0.1 - Segment Offset
2. Create an empty `LineSegmentList` called `offset_segments`
1. For each `LineSegment` of `input_linestring`
   1. Take each segment `(a,b)` of `input_linestring` and compute the vector from the start to the end of the segment<br/>
      `ab = b - a`
   1. rotate this vector by -90 degrees to obtain the 'left normal'<br/>
      `ab_left = Vector2(-ab.y, ab.x)`
   1. normalise `ab_left` by dividing each component by the magnitude of `ab_left`.
   1. multiply the vector by the scalar `d` to obtain the `segment_offset_vector`
   1. add the `segment_offset_vector` to `a` and `b` to get `offset_a` and `offset_b`
   1. append `(offset_a, offset_b)` to `offset_segments`


#### Algorithm 1 - Line Extension
4. Create an empty `LineString` called `raw_offset_ls`
1. Append `offset_segments[0][0]` to `raw_offset_ls`
1. For each pair of consecutive segments `(a,b),(c,d)` in `offset_segments`
   1. If `(a,b)` is co-linear with `(c,d)` then append `b` to raw_offset_ls, and go to the next pair of segments.
   1. Otherwise, find the intersection point `p` of the infinite lines that are collinear with `(a,b)` and `(c,d)`;<br>
      Pay attention to the location of `p` relative to each of the segments:
      1. if `p` is within the segment it is a *True Intersection Point* or **TIP**
      1. If `p` is outside the segment it is called a *False Intersection Point* of **FIP**.<br/>
         **FIP**s are further classified  as follows:
         - **Positive FIP** or **PFIP** if `p` is after the end of a segment, or
         - **Negative FIP** or **NFIP** if `p` is before the start of a segment.
   1. If `p` is a **TIP** for both `(a,b)` and `(c,d)` append `p` to `raw_offset_ls`
   1. If `p` is a **FIP** for both `(a,b)` and `(c,d)`
      1. If `p` is a **PFIP** for `(a,b)` then append `p`to `raw_offset_ls`
      1. Otherwise, append `b` then `c` to `raw_offset_ls`
   1. Otherwise, append `b` then `c` to `raw_offset_ls`
1. Remove zero length segments in `raw_offset_ls`

>Note: mitre limits are not mentioned in the original paper and have not been implemented in this package (yet).
> Extending line segments that are close to parallel will generate an intersection point far from the origin 
> which would cause problems with floating-point precision.

> TODO: It should be possible to maintain a partial mapping between the segments of  `input_ls` and

#### Algorithm 4.1 - Dual Clipping:
8. Find `raw_offset_ls_twin` by repeating Algorithms 0.1 and 1 but offset the `input_linestring` in the opposite direction (`-d`)
1. Find `intersection_points` between
   1. `raw_offset_ls` and `raw_offset_ls`
   1. `raw_offset_ls` and `raw_offset_ls_twin`

1. Find `split_offset_mls` by splitting `raw_offset_ls` at each point in `intersection_points`
1. If `intersection_points` was empty, then add `raw_offset_ls` to `split_offset_mls` and skip to Algorithm 4.2.
1. Delete each `LineString` in `split_offset_mls` if it intersects the `input_linestring`<br>
   unless the intersection is with the first or last `LineSegment` of `input_linestring`
   1. If we find such an intersection point that *is* on the first or last `LineSegment` of `input_linestring`<br/>
   then add the intersection point to a list called `cut_targets`

#### Algorithm 4.1.2 - Cookie Cutter:
13. For each point `p` in `cut_targets`
   1. construct a circle of diameter `d` with its center at `p`
   1. delete all parts of any linestring in `split_offset_mls` which falls within this circle
1. Empty the `cut_targets` list

#### Algorithm 4.1.3 - Proximity Clipping
17. For each linestring `item_ls` in `split_offset_mls`
   1. For each segment `(a,b)` in `item_ls`
      1. For each segment `(u,v)` of `input_linestring`
         - Find `a_proj` and `b_proj` by projecting `a` and `b` onto segment `(u,v)`
         - Adjust the projected points such that `a_proj` and `b_proj` lie **at** or **between** `u` and `v`
         - Find `a_dist` by computing `magnitude(a_proj - a)`
         - Find `b_dist` by computing `magnitude(b_proj - b)`
         - if either `a_dist` or `b_dist` is less than the absolute value of `d` then
            - if `a_dist > b_dist`add `a_proj` to `cut_targets`
            - Otherwise, add `b_proj` to `cut_targets`  
1. Repeat Algorithm 4.1.2
1. Remove zero length segments and empty linestrings etc **(TODO: not yet implemented)** 
1. Join remaining linestrings that are touching to form new linestring(s) **(TODO: not yet implemented)**




