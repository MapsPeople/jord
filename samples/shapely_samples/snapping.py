#!/usr/bin/env python3
from shapely import LineString, Polygon
from shapely.ops import snap

square = Polygon([(1, 1), (2, 1), (2, 2), (1, 2), (1, 1)])
line = LineString([(0, 0), (0.8, 0.8), (1.8, 0.95), (2.6, 0.5)])
result = snap(line, square, 0.5)
