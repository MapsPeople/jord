#!/usr/bin/env python3
from typing import Sequence, Tuple, Optional

import numpy
from shapely.geometry import Polygon, Point, LineString
from shapely.geometry.base import BaseGeometry
from warg import pairs, Number

__all__ = [
    "project_point_to_object",
    "project_point_to_line_points",
    "project_point_to_line",
    "nearest_geometry",
]


def project_point_to_object(point: Point, geometry: BaseGeometry) -> Point:
    """Find the nearest point in geometry, measured from given point.

    :param point: a shapely Point
    :param geometry: a shapely geometry object (LineString, Polygon)

    :return: a shapely Point that lies on geometry closest to point
    """
    nearest_point = None
    min_dist = float("inf")

    if isinstance(geometry, Polygon):
        for seg_start, seg_end in pairs(list(geometry.exterior.coords)):
            line_start = Point(seg_start)
            line_end = Point(seg_end)

            intersection_point = project_point_to_line_points(
                point, line_start, line_end
            )
            cur_dist = point.distance(intersection_point)

            if cur_dist < min_dist:
                min_dist = cur_dist
                nearest_point = intersection_point

    elif isinstance(geometry, LineString):
        for seg_start, seg_end in pairs(list(geometry.coords)):
            line_start = Point(seg_start)
            line_end = Point(seg_end)

            intersection_point = project_point_to_line_points(
                point, line_start, line_end
            )
            cur_dist = point.distance(intersection_point)

            if cur_dist < min_dist:
                min_dist = cur_dist
                nearest_point = intersection_point
    else:
        raise NotImplementedError(
            "project_point_to_object not implemented for"
            + " geometry type '"
            + geometry.type
            + "'."
        )
    return nearest_point


def project_point_to_line_points(
    point: Point, line_start: Point, line_end: Point, must_be_orthogonal: bool = False
) -> Point:
    """Find the nearest point on a straight line, measured from given point.

    Source: http://gis.stackexchange.com/a/438/19627

    :param must_be_orthogonal:
    :param point: a shapely Point object
    :param line_start: the line starting point as a shapely Point
    :param line_end: the line end point as a shapely Point

    :return: a shapely Point that lies on the straight line closest to point

    """

    line_magnitude = line_start.distance(line_end)

    u = (
        (point.x - line_start.x) * (line_end.x - line_start.x)
        + (point.y - line_start.y) * (line_end.y - line_start.y)
    ) / (line_magnitude**2)

    # closest point does not fall within the line segment,
    # take the shorter distance to an endpoint

    if u < 0.00001 or u > 1:
        ix = point.distance(line_start)
        iy = point.distance(line_end)

        if ix > iy:
            if must_be_orthogonal:
                raise Exception
            return line_end

        else:
            if must_be_orthogonal:
                raise Exception()
            return line_start

    ix = line_start.x + u * (line_end.x - line_start.x)
    iy = line_start.y + u * (line_end.y - line_start.y)

    return Point([ix, iy])


def project_point_to_line(point: Point, line: LineString) -> Point:
    line_coords = line.coords

    # assert line_coords == 2

    return project_point_to_line_points(point, *[Point(*xy) for xy in line_coords])


def line_line_intersection(line: LineString, other: LineString) -> Optional[Point]:
    """

    p = p1_start
    r = (p1_end - p1_start)

    q = p2_start
    s = (p2_end - p2_start)

    t = numpy.cross(q - p, s) / (numpy.cross(r, s))

    # This is the intersection point
    i = p + t * r

    :param line:
    :param other:
    :return:
    """

    import sympy.geometry

    l1 = sympy.geometry.Line(*[sympy.geometry.Point(*xy) for xy in line.coords])

    l2 = sympy.geometry.Line(*[sympy.geometry.Point(*xy) for xy in other.coords])

    l1_l2_intersection = l1.intersection(
        l2
    )  # These are two infinite lines defined by two points on the line

    if len(l1_l2_intersection) == 1:
        if isinstance(l1_l2_intersection[0], sympy.geometry.Line2D):  # Same
            return
        return Point(*l1_l2_intersection[0])


def get_intersection_linear_functions(
    a1: Number, b1: Number, a2: Number, b2: Number
) -> Tuple[Number, Number]:
    A = numpy.array([[-a1, 1], [-a2, 1]])
    b = numpy.array([[b1], [b2]])
    # you have to solve linear System AX = b where X = [x y]'
    return numpy.squeeze(numpy.linalg.pinv(A) @ b)  # x,y


def nearest_geometry(
    geometries: Sequence[BaseGeometry], point: Point
) -> Tuple[BaseGeometry, float, int]:
    """Find the nearest geometry among a list, measured from fixed point.

    :param geometries: a list of shapely geometry objects
    :param point: a shapely Point

    :return:        Tuple (geom, min_dist, min_index) of the geometry with minimum distance        to point, its distance min_dist and the list index of geom, so that        geom = geometries[min_index].
    """
    min_dist, min_index = min(
        (point.distance(geom), k) for (k, geom) in enumerate(geometries)
    )

    return geometries[min_index], min_dist, min_index


if __name__ == "__main__":
    print(
        line_line_intersection(
            LineString([[0, 0], [1, 1]]), LineString([[1, 0], [0, 1]])
        )
    )
    print(
        line_line_intersection(
            LineString([[0, 0], [1, 1]]), LineString([[6, 0], [5, 1]])
        )
    )
    print(
        line_line_intersection(
            LineString([[0, 0], [1, 1]]), LineString([[0, 0], [1, 1]])
        )
    )
    print(
        line_line_intersection(
            LineString([[0, 0], [1, 1]]), LineString([[1, 0], [2, 1]])
        )
    )
