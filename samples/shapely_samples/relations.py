from shapely.geometry import Polygon

poly1 = Polygon([(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)])
poly2 = Polygon([(0.5, 0.5), (0.5, 1.5), (1.5, 1.5), (1.5, 0.5)])
poly3 = Polygon([(0.25, 0.25), (0.25, 0.75), (0.75, 0.75), (0.75, 0.25)])

print(poly1.intersection(poly2))
print(poly1.intersects(poly2))

print(poly1.union(poly2))
print(poly1.overlaps(poly2))

print(poly1.touches(poly2))

print(poly1.contains(poly2))

print("wah")
print(poly1.intersection(poly3))
print(poly1.intersects(poly3))

print(poly1.union(poly3))
print(poly1.overlaps(poly3))

print(poly1.touches(poly3))

print(poly1.contains(poly3))
