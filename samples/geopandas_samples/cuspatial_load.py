#!/usr/bin/env python3

import cuspatial  # conda install -c rapidsai -c conda-forge -c nvidia cuspatial=23.10 python=3.10 cudatoolkit=11.8
import geopandas
from shapely.geometry import Polygon

p1 = Polygon([(0, 0), (1, 0), (1, 1)])
p2 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
geoseries = geopandas.GeoSeries([p1, p2])

cuspatial_geoseries = cuspatial.from_geopandas(geoseries)
print(cuspatial_geoseries)
