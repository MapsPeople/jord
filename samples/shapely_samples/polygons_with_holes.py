#!/usr/bin/env python3
import geopandas
from matplotlib import pyplot
from shapely.geometry import Polygon

# Example polygon with two holes
inputPolygon = Polygon(
    ((0, 0), (10, 0), (10, 10), (0, 10)),
    (((1, 3), (5, 3), (5, 1), (1, 1)), ((9, 9), (9, 8), (8, 8), (8, 9))),
)

polygonExterior = inputPolygon.exterior
polygonInteriors = []
for i in range(len(inputPolygon.interiors)):
    # do the stuff with your polygons
    polygonInteriors.append(inputPolygon.interiors[i])

newPolygon = Polygon(
    polygonExterior, [[pt for pt in inner.coords] for inner in polygonInteriors]
)

p = geopandas.GeoSeries(newPolygon)
p.plot()
pyplot.show()
