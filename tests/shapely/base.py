import shapely

from jord.shapely_utilities.base import clean_shape, sanitise, zero_buffer


def test_point_clean_shape():
    p = shapely.Point((1, 1))
    assert clean_shape(p) == p


def test_linestring_clean_shape():
    p = shapely.LineString([(1, 1), (2, 2)])
    assert clean_shape(p) == p


def test_geometry_collection_clean_shape():
    p = shapely.GeometryCollection(
        [shapely.LineString([(1, 1), (2, 2)]), shapely.Point((1, 1))]
    )
    assert clean_shape(p) == p


def test_sanitise_kwargs():
    p = shapely.GeometryCollection(
        [shapely.LineString([(1, 1), (2, 2)]), shapely.Point((1, 1))]
    )

    def i(g, *, a=None):
        assert a == 1
        return g

    assert sanitise(p, i, kwargs={i: {"a": 1}}) == p


def test_sanitise_geom_zero():
    p = shapely.GeometryCollection(
        [shapely.LineString([(1, 1), (2, 2)]), shapely.Point((1, 1))]
    )

    assert sanitise(p, zero_buffer) == p


def test_sanitise_poly():
    p = shapely.Polygon([(-1, 1), (1, 1), (1, -1), (-1, -1), (-1, 1)])

    assert sanitise(p).equals(p)
