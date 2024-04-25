import shapely
from shapely import LineString, Point
from shapely.geometry import Polygon

point = Point([(0.0, 0.0)])
line = LineString([(0.5, 0.5), (0.5, 1.5), (1.5, 1.5), (1.5, 0.5)])
poly = Polygon([(0.25, 0.25), (0.25, 0.75), (0.75, 0.75), (0.75, 0.25)])

print(point.buffer(1, cap_style="flat"))  # WHA
print(line.buffer(1, cap_style="flat"))
print(poly.buffer(1, cap_style="flat"))

print(point.buffer(-1, cap_style="flat"))
print(line.buffer(-1, cap_style="flat"))
print(poly.buffer(-1, cap_style="flat"))

print(point.buffer(1, cap_style=shapely.BufferCapStyle.square))
