import pytest
import shapely

from jord.shapely_utilities import closing, dilate, erode, opening
from jord.shapely_utilities.morphology import clean_shape


@pytest.mark.parametrize(
    "shape",
    (
        shapely.Point(0, 0),
        shapely.LinearRing([(-1, -1), (1, 1), (1, 1), (1, -1), (-1, -1)]),
        shapely.LineString([(-1, -1), (1, 1), (1, 1), (1, -1), (-1, -1)]),
        shapely.Polygon(
            shapely.LinearRing([(-1, -1), (1, 1), (1, 1), (1, -1), (-1, -1)])
        ),
        shapely.MultiPolygon(
            [
                shapely.Polygon(
                    shapely.LinearRing([(-1, -1), (1, 1), (1, 1), (1, -1), (-1, -1)])
                )
            ]
        ),
        shapely.MultiPoint([shapely.Point(0, 0)]),
        shapely.MultiLineString(
            [shapely.LineString([(-1, -1), (1, 1), (1, 1), (1, -1), (-1, -1)])]
        ),
        shapely.GeometryCollection(
            [
                shapely.Point(0, 0),
                shapely.LineString([(-1, -1), (1, 1), (1, 1), (1, -1), (-1, -1)]),
            ]
        ),
    ),
)
@pytest.mark.parametrize(
    "operation",
    ((dilate, erode, closing, opening)),
)
def test_operation_zero(operation, shape):
    shape.equals(operation(shape, distance=0))


@pytest.mark.parametrize(
    "p,expected",
    [
        (shapely.Polygon(((1, 1), (1, 1), (1, 1), (1, 1))), shapely.Point((1, 1))),
        (
            shapely.LineString(
                (
                    (0.8493828299972399, 0.6810102249463201),
                    (0.8493828299972399, 0.68101022494632),
                )
            ),
            None,
        ),
        (
            shapely.LineString(
                (
                    (0.8544427077864901, 0.2981250003092),
                    (0.85444270778649, 0.2981250003092),
                )
                # 'LINESTRING (0.8544427077864901 0.2981250003092, 0.85444270778649 0.2981250003092)'
            ),
            None,
            # 'POLYGON ((
            # 0.85444270778649 0.2981240003092,
            # 0.85444270778649 0.2981260003092,
            # 0.8544427077864901 0.2981240003092,
            # 0.85444270778649 0.2981240003092
            # ))'
        ),
    ],
)
def test_dilate_no_area_shape(
    p: shapely.geometry.base.BaseGeometry, expected: shapely.geometry.base.BaseGeometry
):
    a = dilate(p)
    assert not a.is_empty, a
    assert isinstance(a, shapely.Polygon)
    assert a.area > 0
    assert a.minimum_clearance > 0, a.minimum_clearance
    assert a != p


@pytest.mark.parametrize(
    "p,expected",
    [
        (shapely.Polygon(((1, 1), (1, 1), (1, 1), (1, 1))), None),
        (
            shapely.LineString(
                (
                    (0.8493828299972399, 0.6810102249463201),
                    (0.8493828299972399, 0.68101022494632),
                )
            ),
            None,
        ),
    ],
)
def test_dilate_n_clean_no_area_shape(
    p: shapely.geometry.base.BaseGeometry, expected: shapely.geometry.base.BaseGeometry
):
    a = clean_shape(dilate(p))
    assert not a.is_empty, a
    assert a.area > 0
    assert a.minimum_clearance > 0, a.minimum_clearance
    assert a != p
