#!/usr/bin/env python3

import statistics
from typing import Generator, Iterable, List, Sequence, Tuple, Union

import shapely
from shapely.geometry import (
    LineString,
    MultiLineString,
    MultiPolygon,
    Polygon,
)
from shapely.geometry.base import BaseGeometry
from warg import Number, pairs

from jord.shapely_utilities.base import sanitise
from .lines import segments
from .rings import ensure_ccw_ring, ensure_cw_ring

__all__ = [
    "explode_polygons",
    "polygon_has_interior_rings",
    "iter_polygons",
    "discard_holes",
    "get_coords_from_polygonal_shape",
    "get_polygonal_shape_from_coords",
]


def polygon_has_interior_rings(polygon: Polygon) -> bool:
    """

    :param polygon:
    :return:
    """
    return len(polygon.interiors) > 0


def mean_std_dev_line_length(geom: BaseGeometry) -> Tuple[float, float]:
    """

    :param geom:
    :return:
    """
    line_lengths = []
    if isinstance(geom, LineString):
        for segment in segments(geom):
            line_lengths.append(segment.length)
    elif isinstance(geom, MultiLineString):
        for li in geom.geoms:
            for segment in segments(li):
                line_lengths.append(segment.length)
    elif isinstance(geom, (Polygon, MultiPolygon)):
        exterior_rings, interior_rings = extract_poly_rings(geom)
        for ex_ring in exterior_rings:
            for segment in segments(ex_ring):
                line_lengths.append(segment.length)
        for in_ring in interior_rings:
            for segment in segments(in_ring):
                line_lengths.append(segment.length)
    else:
        raise ValueError(f"Unhandled geometry type: {repr(geom.type)}")

    return (
        statistics.mean(line_lengths),
        statistics.stdev(line_lengths) if len(line_lengths) > 1 else 0,
    )


def mean_std_dev_area(geom: BaseGeometry) -> Tuple[float, float]:
    """

    :param geom:
    :return:
    """
    poly_areas = []
    if isinstance(geom, Polygon):
        poly_areas.append(geom.area)
    elif isinstance(geom, MultiPolygon):
        for po in geom.geoms:
            poly_areas.append(po.area)
    else:
        raise ValueError(f"Unhandled geometry type: {repr(geom.type)}")

    return (
        statistics.mean(poly_areas),
        statistics.stdev(poly_areas) if len(poly_areas) > 1 else 0,
    )


def prune_area(geom: BaseGeometry, eps: float = 1e-7) -> BaseGeometry:
    """

    :param geom:
    :param eps:
    :return:
    """
    raise NotImplementedError
    poly_areas = []
    if isinstance(geom, Polygon):
        poly_areas.append(geom.area)

    elif isinstance(geom, MultiPolygon):
        for po in geom.geoms:
            poly_areas.append(po.area)

    return poly_areas


def prune_rings(geom: BaseGeometry, eps: float = 1e-7) -> BaseGeometry:
    """

    :param geom:
    :param eps:
    :return:
    """
    raise NotImplementedError
    poly_areas = []
    if isinstance(geom, Polygon):
        poly_areas.append(geom.area)
    elif isinstance(geom, MultiPolygon):
        for po in geom.geoms:
            poly_areas.append(po.area)

    return poly_areas


def prune_holes(
    geom: Union[MultiPolygon, Polygon], epsilon: Number = 1000
) -> Union[MultiPolygon, Polygon]:
    """

    :param epsilon:
    :param geom:
    :return:"""

    if isinstance(geom, MultiPolygon):
        parts = []

        for polygon in geom.geoms:
            interiors = []

            for interior in polygon.interiors:
                p = Polygon(interior)

                if p.area > epsilon:
                    interiors.append(interior)

            temp_pol = Polygon(polygon.exterior.coords, holes=interiors)
            parts.append(temp_pol)

        return MultiPolygon(parts)

    interiors = []

    for interior in geom.interiors:
        p = Polygon(interior)
        if p.area > epsilon:
            interiors.append(interior)

    return Polygon(geom.exterior.coords, holes=interiors)


def get_coords_from_polygonal_shape(
    shape: Union[shapely.Polygon, shapely.MultiPolygon]
) -> List[List[List[tuple[float, float]]]]:
    coords = []

    if isinstance(shape, shapely.Polygon):
        coords.append(shape.exterior.coords[:])
        for linearring in shape.interiors:
            coords.append(linearring.coords[:])
    elif isinstance(shape, shapely.MultiPolygon):
        for polygon in shape.geoms:
            coords.append(get_coords_from_polygonal_shape(polygon))

    return coords


def get_polygonal_shape_from_coords(
    coords: Union[
        Iterable[Iterable[Iterable[tuple[float, float]]]],
        Iterable[Iterable[tuple[float, float]]],
    ]
) -> Union[Polygon, MultiPolygon, None]:
    outer = next(iter(coords), None)

    assert isinstance(outer, Iterable)
    a = next(iter(outer), None)
    if isinstance(a, Iterable):  # Polygon
        b = next(iter(a), None)
        if isinstance(b, Iterable):  # Holes
            polygons = []
            for poly in coords:  # MultiPolygon and # MultiPolygon Holes
                polygons.append(get_polygonal_shape_from_coords(poly))
            return MultiPolygon(polygons)
        else:
            exterior, *interior = coords
            if interior:
                return Polygon(exterior, holes=interior)
            return Polygon(exterior)

    if len(coords[0]) == 0:
        return None

    return Polygon(coords)


def extract_poly_coords(geom: Union[Polygon, MultiPolygon]) -> Tuple[List, List]:
    """
    TODO: Duplicate of get_coords_from_polygonal_shape

    :param geom:
    :return:
    """
    if geom.type == "Polygon":
        exterior_coords = geom.exterior.coords[:]
        interior_coords = []
        for interior in geom.interiors:
            interior_coords += interior.coords[:]
    elif geom.type == "MultiPolygon":
        exterior_coords = []
        interior_coords = []
        for part in geom.geoms:
            epc = extract_poly_coords(part)  # Recursive call
            exterior_coords += epc[0]
            interior_coords += epc[1]
    else:
        raise ValueError(f"Unhandled geometry type: {repr(geom.type)}")
    return exterior_coords, interior_coords


def extract_poly_rings(geom: BaseGeometry) -> Tuple[List, List]:
    """

    :param geom:
    :return:
    """
    interior_rings = []
    exterior_rings = []
    if isinstance(geom, Polygon):
        exterior_rings.append(geom.exterior)
        interior_rings.extend(geom.interiors)
    elif isinstance(geom, MultiPolygon):
        for part in geom.geoms:
            exterior_rings.append(part.exterior)
            interior_rings.extend(part.interiors)
    else:
        raise ValueError(f"Unhandled geometry type: {repr(geom.type)}")

    return exterior_rings, interior_rings


def discard_holes(
    shape: Union[shapely.Polygon, shapely.MultiPolygon]
) -> Union[Polygon, MultiPolygon]:
    if isinstance(shape, shapely.Polygon):
        return shapely.Polygon(shape.exterior.coords)
    elif isinstance(shape, shapely.MultiPolygon):
        shape_parts = []
        for shape_part in shape.geoms:
            shape_parts.append(shapely.Polygon(shape_part.exterior.coords))
        return MultiPolygon(shape_parts)
    raise NotImplementedError


def ensure_ccw_poly(polygon: Polygon) -> Polygon:
    """
    This function checks if the polygon is counter-clockwise if not it is reversed


    :param polygon: The polygon to check
    :return: Returns the polygon turned clockwise
    """

    return Polygon(
        shell=ensure_ccw_ring(polygon.exterior),
        holes=[ensure_ccw_ring(hole) for hole in polygon.interiors],
    )


def ensure_cw_poly(polygon: Polygon) -> Polygon:
    """
    This function checks if the polygon is clockwise if not it is reversed


    :param polygon: The polygon to check
    :return: Returns the polygon turned clockwise
    """

    return Polygon(
        shell=ensure_cw_ring(polygon.exterior),
        holes=[ensure_cw_ring(hole) for hole in polygon.interiors],
    )


def iter_polygons(
    _input_geometry: BaseGeometry,
) -> Union[Generator[Polygon, None, None], Tuple[BaseGeometry]]:
    """

    :param _input_geometry:
    :return:
    """
    if isinstance(_input_geometry, MultiPolygon):
        return (polygon for polygon in _input_geometry.geoms)

    # assert isinstance(_input_geometry, Polygon)

    return (_input_geometry,)


def explode_polygons(
    polygons: Union[Polygon, MultiPolygon, Sequence[Polygon]],
    return_index: bool = False,
) -> Union[Sequence[LineString], Tuple[Sequence[LineString], Sequence[int]]]:
    """

    :param polygons:
    :param return_index:
    :return: main line features that make up the polygons
    """
    lines_out = []
    index = []

    if isinstance(polygons, Polygon):
        polygons = [polygons]

    if isinstance(polygons, MultiPolygon):
        polygons = polygons.geoms

    for i, l in enumerate(polygons):
        for s in [LineString(s) for s in pairs(l.exterior.coords)]:
            lines_out.append(s)
            index.append(i)

        for p in l.interiors:
            lines_out.append(LineString(p.coords))
            index.append(i)

    if return_index:
        return lines_out, index

    return lines_out


if __name__ == "__main__":

    def aishdjauisd():
        # Import constructors for creating geometry collections
        from shapely.geometry import MultiPoint, MultiLineString

        # Import necessary geometric objects from shapely module
        from shapely.geometry import Point, LineString, Polygon

        # Create Point geometric object(s) with coordinates
        point1 = Point(2.2, 4.2)
        point2 = Point(7.2, -25.1)
        point3 = Point(9.26, -2.456)
        # point3D = Point(9.26, -2.456, 0.57)

        # Create a MultiPoint object of our points 1,2 and 3
        multi_point = MultiPoint([point1, point2, point3])

        # It is also possible to pass coordinate tuples inside
        multi_point2 = MultiPoint([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])

        # We can also create a MultiLineString with two lines
        line1 = LineString([point1, point2])
        line2 = LineString([point2, point3])
        multi_line = MultiLineString([line1, line2])
        polygon = Polygon([point2, point1, point3])

        from shapely.geometry import GeometryCollection
        from matplotlib import pyplot
        import geopandas

        geoms = GeometryCollection([multi_point, multi_point2, multi_line, polygon])
        print(mean_std_dev_line_length(geoms))
        geoms = sanitise(geoms)
        print(mean_std_dev_line_length(geoms))

        p = geopandas.GeoSeries(geoms)
        p.plot()
        pyplot.show()

    def ahsudh():
        # Import constructors for creating geometry collections
        from shapely.geometry import MultiPoint, MultiLineString

        # Import necessary geometric objects from shapely module
        from shapely.geometry import Point, LineString, Polygon

        # Create Point geometric object(s) with coordinates
        point1 = Point(2.2, 4.2)
        point2 = Point(7.2, -25.1)
        point3 = Point(9.26, -2.456)
        # point3D = Point(9.26, -2.456, 0.57)

        # Create a MultiPoint object of our points 1,2 and 3
        multi_point = MultiPoint([point1, point2, point3])

        # It is also possible to pass coordinate tuples inside
        multi_point2 = MultiPoint([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])

        # We can also create a MultiLineString with two lines
        line1 = LineString([point1, point2])
        line2 = LineString([point2, point3])
        multi_line = MultiLineString([line1, line2])
        polygon = Polygon([point2, point1, point3])
        polygon2 = Polygon([point3, point2, point1])
        multi_polygon = MultiPolygon([polygon, polygon2])

        print(mean_std_dev_line_length(line1))
        print(mean_std_dev_line_length(line2))
        print(mean_std_dev_line_length(multi_line))
        print(mean_std_dev_line_length(polygon))
        print(mean_std_dev_line_length(polygon2))
        print(mean_std_dev_line_length(multi_polygon))

        print(mean_std_dev_area(polygon))
        print(mean_std_dev_area(polygon2))
        print(mean_std_dev_area(multi_polygon))

        from shapely.geometry import GeometryCollection
        from matplotlib import pyplot
        import geopandas

        geoms = GeometryCollection(
            [multi_point, multi_point2, multi_line, polygon, polygon2, multi_polygon]
        )

        p = geopandas.GeoSeries(geoms)
        p.plot()
        pyplot.show()

    ahsudh()
    # aishdjauisd()
