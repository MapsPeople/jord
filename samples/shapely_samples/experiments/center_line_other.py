import shapely

from jord.shapely_utilities import dilate


def test_center_line_of_square():
    from shapely.geometry import Polygon
    from centerline.geometry import Centerline

    polygon = Polygon([[0, 0], [0, 4], [4, 4], [4, 0]])
    attributes = {"id": 1, "name": "polygon", "valid": True}

    centerline = Centerline(polygon, **attributes)

    print(polygon.wkt)
    print(centerline.geometry.wkt)


def test_center_line_of_rect():
    from shapely.geometry import Polygon
    from centerline.geometry import Centerline

    polygon = Polygon([[0, 0], [2, 0], [2, 1], [0, 1]])
    attributes = {"id": 1, "name": "polygon", "valid": True}

    centerline = Centerline(polygon, **attributes)

    print(polygon.wkt)
    print(centerline.geometry.wkt)


def test_center_line_of_rect2():
    from shapely.geometry import Polygon

    polygon = Polygon([[0, 0], [2, 0], [2, 1], [0, 1]])

    import pygeoops

    centerline = pygeoops.centerline(polygon)

    print(polygon.wkt)
    print(centerline.wkt)


def test_center_line_of_u():
    polygon = dilate(shapely.LineString([[0, 0], [2, 0], [2, 2], [0, 2]]), distance=0.5)

    import pygeoops

    centerline = pygeoops.centerline(polygon)

    print(polygon.wkt)
    print(centerline.wkt)
