#!/usr/bin/env python3
from shapely import LineString
from shapely.ops import shared_paths

g1 = LineString([(0, 0), (10, 0), (10, 5), (20, 5)])
g2 = LineString([(5, 0), (30, 0), (30, 5), (0, 5)])
forward, backward = shared_paths(g1, g2).geoms
