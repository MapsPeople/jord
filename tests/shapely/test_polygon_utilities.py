from typing import Union

import pytest
import shapely

from jord.shapely_utilities import discard_holes, has_holes


@pytest.fixture(scope="module")
def a_point() -> shapely.Point:
    return shapely.Point(2.2, 4.2)


@pytest.fixture(scope="module")
def another_point() -> shapely.Point:
    return shapely.Point(7.2, -25.1)


@pytest.fixture(scope="module")
def third_point() -> shapely.Point:
    return shapely.Point(9.26, -2.456)


@pytest.fixture(scope="module")
def a_line(a_point: shapely.Point, another_point: shapely.Point) -> shapely.Point:
    return shapely.LineString([a_point, another_point])


@pytest.fixture(scope="module")
def another_line(
    another_point: shapely.Point, third_point: shapely.Point
) -> shapely.LineString:
    return shapely.LineString([another_point, third_point])


@pytest.fixture(scope="module")
def a_multi_point(
    a_point: shapely.Point, another_point: shapely.Point, third_point: shapely.Point
) -> shapely.MultiPoint:
    return shapely.MultiPoint([a_point, another_point, third_point])


@pytest.fixture(scope="module")
def another_multi_point() -> shapely.MultiPoint:
    return shapely.MultiPoint([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])


@pytest.fixture(scope="module")
def a_multi_line(
    a_line: shapely.LineString, another_line: shapely.LineString
) -> shapely.MultiLineString:
    return shapely.MultiLineString([a_line, another_line])


@pytest.fixture(scope="module")
def a_polygon(
    a_point: shapely.Point, another_point: shapely.Point, third_point: shapely.Point
) -> shapely.Polygon:
    return shapely.Polygon([another_point, a_point, third_point])


@pytest.fixture(scope="module")
def another_polygon(
    a_point: shapely.Point, another_point: shapely.Point, third_point: shapely.Point
) -> shapely.Polygon:
    return shapely.Polygon([third_point, another_point, a_point])


@pytest.fixture(scope="module")
def a_multi_polygon(
    a_polygon: shapely.Polygon, another_polygon: shapely.Polygon
) -> shapely.MultiPolygon:
    return shapely.MultiPolygon([a_polygon, another_polygon])


@pytest.fixture(scope="module")
def a_geometry_collection(
    a_multi_point: shapely.MultiPoint,
    a_multi_line: shapely.MultiLineString,
    a_polygon: shapely.Polygon,
    another_polygon: shapely.Polygon,
    a_multi_polygon: shapely.MultiPolygon,
) -> shapely.GeometryCollection:
    return shapely.GeometryCollection(
        [a_multi_point, a_multi_line, a_polygon, another_polygon, a_multi_polygon]
    )


@pytest.mark.parametrize("poly", ("a_polygon", "another_polygon"))
def test_discard_holes_polygonal(request, poly: Union[shapely.Polygon]):
    assert not has_holes(discard_holes(request.getfixturevalue(poly)))


@pytest.mark.parametrize("multi", ("a_geometry_collection", "a_multi_polygon"))
def test_discard_holes_multi_geoms(
    request, multi: Union[shapely.GeometryCollection, shapely.MultiPolygon]
):
    assert not has_holes(discard_holes(request.getfixturevalue(multi)))


@pytest.mark.parametrize("non_poly", ("a_point", "a_line", "another_line"))
def test_discard_holes_non_polygonal_raises(
    request, non_poly: shapely.geometry.base.BaseGeometry
):
    with pytest.raises(NotImplementedError):
        discard_holes(request.getfixturevalue(non_poly))
