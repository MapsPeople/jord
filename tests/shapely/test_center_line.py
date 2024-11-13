import shapely

from jord.geometric_analysis import construct_centerline
from jord.shapely_utilities import dilate


def test_u():
    buffer_size = 0.5

    polygon = dilate(
        shapely.LineString([[0, 0], [2, 0], [2, 2], [0, 2]]), distance=buffer_size
    )

    centerline = construct_centerline(polygon, interpolation_distance=buffer_size)
    print(polygon.wkt)
    print(centerline.wkt)


def test_o():
    buffer_size = 0.5

    polygon = dilate(
        shapely.LineString([[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]),
        distance=buffer_size,
    )

    centerline = construct_centerline(polygon, interpolation_distance=buffer_size)
    print(polygon.wkt)
    print(centerline.wkt)


def test_l():
    buffer_size = 0.5

    polygon = dilate(
        shapely.MultiLineString([[[0, 3], [0, 0], [1, 0]]]), distance=buffer_size
    )

    centerline = construct_centerline(polygon, interpolation_distance=buffer_size)
    print(polygon.wkt)
    print(centerline.wkt)


def test_t():
    buffer_size = 0.5

    polygon = dilate(
        shapely.MultiLineString([[[0, 3], [0, 0], [1, 0]], [[-1, 2], [1, 2]]]),
        distance=buffer_size,
    )

    centerline = construct_centerline(polygon, interpolation_distance=buffer_size)
    print(polygon.wkt)
    print(centerline.wkt)


def test_R():
    buffer_size = 0.5

    polygon = dilate(
        shapely.GeometryCollection(
            (
                shapely.MultiLineString(
                    [
                        [[0, 4], [0, 0]],
                        [[0, 2], [2, 0]],
                    ]
                ),
                dilate(shapely.Point(1, 3), distance=1).boundary,
            )
        ),
        distance=buffer_size,
    )

    centerline = construct_centerline(polygon, interpolation_distance=buffer_size)
    print(polygon.wkt)
    print(centerline.wkt)


def test_H():
    buffer_size = 0.5

    polygon = dilate(
        shapely.GeometryCollection(
            (
                shapely.MultiLineString(
                    [
                        [[0, 4], [0, 0]],
                        [[0, 2], [2, 2]],
                        [[2, 4], [2, 0]],
                    ]
                ),
            )
        ),
        distance=buffer_size,
    )

    centerline = construct_centerline(
        polygon, interpolation_distance=buffer_size, simplify_lines=True
    )
    print(polygon.wkt)
    print(centerline.wkt)


def test_blob():
    buffer_size = 0.5

    polygon = dilate(
        shapely.GeometryCollection(
            (
                dilate(shapely.Point(0, 3), distance=1).boundary,
                dilate(shapely.Point(1, 3), distance=1).boundary,
            )
        ),
        distance=buffer_size,
    )

    centerline = construct_centerline(polygon, interpolation_distance=buffer_size)
    print(polygon.wkt)
    print(centerline.wkt)


def test_8():
    buffer_size = 0.5

    polygon = dilate(
        shapely.GeometryCollection(
            (
                dilate(shapely.Point(0, 3), distance=1).boundary,
                dilate(shapely.Point(2, 3), distance=1).boundary,
            )
        ),
        distance=buffer_size,
    )

    centerline = construct_centerline(polygon, interpolation_distance=buffer_size)
    print(polygon.wkt)
    print(centerline.wkt)


def test_8_far():
    buffer_size = 0.5

    polygon = dilate(
        shapely.GeometryCollection(
            (
                dilate(shapely.Point(0, 3), distance=1).boundary,
                dilate(shapely.Point(2.5, 3), distance=1).boundary,
            )
        ),
        distance=buffer_size,
    )

    centerline = construct_centerline(polygon, interpolation_distance=buffer_size)
    print(polygon.wkt)
    print(centerline.wkt)


def test_8_near():
    buffer_size = 0.5

    polygon = dilate(
        shapely.GeometryCollection(
            (
                dilate(shapely.Point(0, 3), distance=1).boundary,
                dilate(shapely.Point(1.5, 3), distance=1).boundary,
            )
        ),
        distance=buffer_size,
    )

    centerline = construct_centerline(polygon, interpolation_distance=buffer_size)
    print(polygon.wkt)
    print(centerline.wkt)
