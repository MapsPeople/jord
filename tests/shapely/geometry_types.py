import shapely

from jord.shapely_utilities import is_multi


def test_line_string_is_multi():
    assert is_multi(shapely.LineString([[0, 0], [1, 0], [1, 1]])) == False


def test_point_is_multi():
    assert is_multi(shapely.Point([[0, 0]])) == False


def test_linear_ring_is_multi():
    assert is_multi(shapely.LinearRing(((0, 0), (0, 1), (1, 1), (1, 0)))) == False


def test_polygon_is_multi():
    assert (
        is_multi(
            shapely.Polygon(
                ((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0))
            )
        )
        == False
    )


def test_multi_point_is_multi():
    assert is_multi(shapely.MultiPoint([[0.0, 0.0], [1.0, 2.0]]))


def test_multi_line_string_is_multi():
    assert is_multi(shapely.MultiLineString([[[0, 0], [1, 2]], [[4, 4], [5, 6]]]))


def test_multi_polygon_is_multi():
    assert is_multi(
        shapely.MultiPolygon(
            [
                (
                    ((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)),
                    [((0.1, 0.1), (0.1, 0.2), (0.2, 0.2), (0.2, 0.1))],
                )
            ]
        )
    )


def test_geometry_collection_is_multi():
    assert is_multi(
        shapely.GeometryCollection(
            [shapely.Point(51, -1), shapely.LineString([(52, -1), (49, 2)])]
        )
    )
