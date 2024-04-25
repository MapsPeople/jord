#!/usr/bin/env python3

from typing import Iterable, Union

from shapely import LineString, LinearRing, MultiLineString, Point

from .projection import line_line_intersection, project_point_to_line

__all__ = [
    "ensure_ccw_ring",
    "ensure_cw_ring",
    "make_projected_ring",
    "make_extruded_ring",
]


def ensure_ccw_ring(ring: LinearRing) -> LinearRing:
    if not ring.is_ccw:
        return LinearRing(list(ring.coords)[::-1])
    return ring


def ensure_cw_ring(ring: LinearRing) -> LinearRing:
    if ring.is_ccw:
        return LinearRing(list(ring.coords)[::-1])
    return ring


def make_projected_ring(
    lines: Union[MultiLineString, Iterable[LineString]], ccw: bool = True
) -> LinearRing:
    points = []

    if isinstance(lines, MultiLineString):
        lines = lines.geoms

    num_lines = len(lines)

    if ccw:
        lines = lines[::-1]

    for n in range(num_lines):
        points.append(project_point_to_line(Point(lines[n - 1].coords[-1]), lines[n]))

    ring = LinearRing(points)

    assert ring.is_closed
    assert ring.is_ring

    return ring


def make_extruded_ring(
    lines: Union[MultiLineString, Iterable[LineString]], ccw: bool = True
) -> LinearRing:
    points = []

    if isinstance(lines, MultiLineString):
        lines = lines.geoms

    num_lines = len(lines)

    if ccw:
        lines = lines[::-1]

    for n in range(num_lines):
        points.append(Point(line_line_intersection(lines[n - 1], lines[n]).coords[-1]))

    ring = LinearRing(points)

    assert ring.is_closed
    assert ring.is_ring

    return ring


if __name__ == "__main__":

    def juijh():
        r"""

            0   1   2

        0   0---0   0
                    |
        1   0       0
            |
        2   0   0---0

        to become


            0   1   2

        0   0---0---0
            |       |
        1   0       0
            |       |
        2   0---0---0

        :return:
        """

        lines = [
            LineString([[0, 0], [1, 0]]),
            LineString([[2, 0], [2, 1]]),
            LineString([[2, 2], [1, 2]]),
            LineString([[0, 2], [0, 1]]),
        ]

        print(make_extruded_ring(lines))

    def juijh2():
        r"""

            0   1   2   3

        0   0---0---0---0
                    |
        1   0       0
            |
        2   0   0---0

        to become


            0   1   2

        0   0---0---0
            |       |
        1   0       0
            |       |
        2   0---0---0

        :return:
        """

        lines = [
            LineString([[0, 0], [3, 0]]),
            LineString([[2, 0], [2, 1]]),
            LineString([[2, 2], [1, 2]]),
            LineString([[0, 2], [0, 1]]),
        ]

        print(make_extruded_ring(lines))

    juijh2()
