#!/usr/bin/env python3
from shapely import Polygon

coords = [(0, 0), (0, 2), (1, 1), (2, 2), (2, 0), (1, 1), (0, 0)]
p = Polygon(coords)
from shapely.validation import explain_validity

explain_validity(p)

from shapely.validation import make_valid

coords = [(0, 0), (0, 2), (1, 1), (2, 2), (2, 0), (1, 1), (0, 0)]
p = Polygon(coords)
make_valid(p)

from shapely.validation import make_valid

coords = [(0, 0), (0, 2), (1, 1), (2, 2), (2, 0), (1, 1), (0, 0)]
p = Polygon(coords)
make_valid(p)
