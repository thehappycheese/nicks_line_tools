# Nicks Linestring Tools
Implementation loosely inspired by
[Xu-Zheng Liu, Jun-Hai Yong, Guo-Qin Zheng, Jia-Guang Sun. An offset algorithm for polyline curves. Computers in Industry, Elsevier, 2007, 15p. inria-00518005](https://hal.inria.fr/inria-00518005/document)

## Algorithm:
 1. Given a line string, call it the **original line**
 1. Offset individual line segments by distance **d**
    1. Connect these line segments by extension, truncation, or by adding additional line segments based on some rules.
    1. The result of this step is called the **offset line**
 1. Repeat the step above but offset in the opposite direction (**-d**);
    1. The result of this step is called the **twin offset line**
 1. Cut the **offset line** by
    1. intersections with the **offset line**
    1. intersections with original line
    1. intersections with the **twin offset line**
 1. Delete segments of the **offset line** that touch the **original line**
 1. For remaining substrings(TODO... segments??) of the **offset line** find the global closest points **{P}** to the original line
    1. any of the two possible
 1. Construct circles **{C}** centered at each point of **{P}**
    1. Delete any part of the offset line inside these circles
 1. Join remaining segments to form new linestring(s)

## How to use:

```python
## TODO: write sample
```

## Limitations:
 - No support for arcs
 - No handling of malformed geometry
 - Probably cryptic error messages when things go wrong
