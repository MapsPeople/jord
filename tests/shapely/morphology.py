import pytest
import shapely

from jord.shapely_utilities import dilate, erode, opening, closing


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
