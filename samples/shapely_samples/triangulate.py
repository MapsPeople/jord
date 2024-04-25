#!/usr/bin/env python3
from shapely import MultiPoint
from shapely.ops import triangulate

points = MultiPoint([(0, 0), (1, 1), (0, 2), (2, 2), (3, 1), (1, 0)])
triangulate(points)

from shapely.ops import voronoi_diagram

points = MultiPoint([(0, 0), (1, 1), (0, 2), (2, 2), (3, 1), (1, 0)])
regions = voronoi_diagram(points)
list(regions.geoms)
