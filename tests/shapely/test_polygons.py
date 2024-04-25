from shapely import box, difference, unary_union

from jord.shapely_utilities import (
    get_coords_from_polygonal_shape,
    get_polygonal_shape_from_coords,
)


def test_shapely_polygon():
    polygon = box(0, 0, 1, 1)
    polygon_coords = get_coords_from_polygonal_shape(polygon)
    res_polygonal = get_polygonal_shape_from_coords(polygon_coords)

    assert res_polygonal == polygon, f"{res_polygonal=} != {polygon=}"


def test_shapely_polygon_hole():
    polygon = difference(box(0, 0, 3, 3), box(1, 1, 2, 2))
    polygon_coords = get_coords_from_polygonal_shape(polygon)
    res_polygonal = get_polygonal_shape_from_coords(polygon_coords)

    assert res_polygonal == polygon, f"{res_polygonal=} != {polygon=}"


def test_shapely_polygon_multi_hole():
    polygon = difference(
        box(0, 0, 5, 5), unary_union((box(1, 1, 2, 2), box(3, 3, 4, 4)))
    )
    polygon_coords = get_coords_from_polygonal_shape(polygon)
    res_polygonal = get_polygonal_shape_from_coords(polygon_coords)

    assert res_polygonal == polygon, f"{res_polygonal=} != {polygon=}"


def test_shapely_multi_polygon():
    polygon = unary_union((box(0, 0, 1, 1), box(2, 2, 3, 3)))
    polygon_coords = get_coords_from_polygonal_shape(polygon)
    res_polygonal = get_polygonal_shape_from_coords(polygon_coords)

    assert res_polygonal == polygon, f"{res_polygonal=} != {polygon=}"


def test_shapely_multi_polygon_hole_single():
    polygon = unary_union(
        (difference(box(0, 0, 3, 3), box(1, 1, 2, 2)), box(4, 4, 5, 5))
    )
    polygon_coords = get_coords_from_polygonal_shape(polygon)
    res_polygonal = get_polygonal_shape_from_coords(polygon_coords)

    assert res_polygonal == polygon, f"{res_polygonal=} != {polygon=}"


def test_shapely_multi_polygon_hole_both():
    polygon = unary_union(
        (
            difference(box(0, 0, 3, 3), box(1, 1, 2, 2)),
            difference(box(4, 4, 7, 7), box(5, 5, 6, 6)),
        )
    )
    polygon_coords = get_coords_from_polygonal_shape(polygon)
    res_polygonal = get_polygonal_shape_from_coords(polygon_coords)

    assert res_polygonal == polygon, f"{res_polygonal=} != {polygon=}"


def test_shapely_multi_polygon_hole_both_transform_identity():
    from warg import leaf_type_apply

    polygon = unary_union(
        (
            difference(box(0, 0, 3, 3), box(1, 1, 2, 2)),
            difference(box(4, 4, 7, 7), box(5, 5, 6, 6)),
        )
    )
    polygon_coords = get_coords_from_polygonal_shape(polygon)
    polygon_coords = leaf_type_apply(polygon_coords, lambda a: a, tuple)
    res_polygonal = get_polygonal_shape_from_coords(polygon_coords)

    assert res_polygonal == polygon, f"{res_polygonal=} != {polygon=}"


def test_shapely_multi_polygon_hole_both_transform_translate_single_dim():
    from warg import leaf_type_apply

    polygon = unary_union(
        (
            difference(box(0, 0, 3, 3), box(1, 1, 2, 2)),
            difference(box(4, 4, 7, 7), box(5, 5, 6, 6)),
        )
    )
    polygon_coords = get_coords_from_polygonal_shape(polygon)
    polygon_coords = leaf_type_apply(polygon_coords, lambda a: (a[0], a[1] + 1), tuple)
    res_polygonal = get_polygonal_shape_from_coords(polygon_coords)

    assert res_polygonal != polygon, f"{res_polygonal=}, {polygon=}"


if __name__ == "__main__":
    test_shapely_polygon()
    test_shapely_polygon_hole()
    test_shapely_polygon_multi_hole()
    test_shapely_multi_polygon()
    test_shapely_multi_polygon_hole_single()
    test_shapely_multi_polygon_hole_both()
    test_shapely_multi_polygon_hole_both_transform_identity()
    test_shapely_multi_polygon_hole_both_transform_translate_single_dim()
