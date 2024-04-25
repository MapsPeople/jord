#!/usr/bin/env python3

import shapely
from shapely.geometry import LinearRing
from shapely.geometry.base import BaseGeometry

__all__ = ["closing", "opening", "erode", "erosion", "dilate", "dilation", "close"]

from warg import passes_kws_to

FALLBACK_CAPSTYLE = shapely.BufferCapStyle.round  # CAN BE OVERRIDDEN
FALLBACK_JOINSTYLE = shapely.BufferCapStyle.round  # CAN BE OVERRIDDEN


@passes_kws_to(shapely.geometry.base.BaseGeometry.buffer)
def morphology_buffer(
    geom: BaseGeometry,
    distance: float = 1e-7,
    cap_style: shapely.BufferCapStyle = shapely.BufferCapStyle.flat,
    join_style: shapely.BufferJoinStyle = shapely.BufferJoinStyle.mitre,
    **kwargs
):
    if distance == 0:
        if isinstance(geom, shapely.GeometryCollection):
            return shapely.GeometryCollection(
                [
                    morphology_buffer(
                        g,
                        distance=distance,
                        cap_style=cap_style,
                        join_style=join_style,
                        **kwargs
                    )
                    for g in geom.geoms
                ]
            )

        if not isinstance(
            geom, (shapely.Polygon, shapely.MultiPolygon)
        ):  # So if line(s) or point(s)
            return geom

    if (
        isinstance(geom, shapely.Point) and cap_style == shapely.BufferCapStyle.flat
    ):  # parameter NONSENSE, probably not what is intended
        cap_style = FALLBACK_CAPSTYLE
        join_style = FALLBACK_JOINSTYLE

    return geom.buffer(
        distance=distance, cap_style=cap_style, join_style=join_style, **kwargs
    )


@passes_kws_to(morphology_buffer)
def erosion(geom: BaseGeometry, distance: float = 1e-7, **kwargs) -> BaseGeometry:
    """

    :param distance:
    :param cap_style:
    :param join_style:
    :param geom: The geometry to be eroded
    :return: The eroded geometry
    """
    return morphology_buffer(geom=geom, distance=-distance, **kwargs)


@passes_kws_to(morphology_buffer)
def dilation(geom: BaseGeometry, distance: float = 1e-7, **kwargs) -> BaseGeometry:
    """

    :param cap_style:
    :param join_style:
    :param geom: The geometry to be dilated
    :param distance: Dilation amount
    :return: The dilated geometry
    """

    return morphology_buffer(geom=geom, distance=distance, **kwargs)


@passes_kws_to(shapely.geometry.base.BaseGeometry.buffer)
def closing(geom: BaseGeometry, **kwargs) -> BaseGeometry:
    """

    :param geom: The geometry to be closed
    :return: The closed geometry
    """
    return erode(dilate(geom, **kwargs), **kwargs)


@passes_kws_to(shapely.geometry.base.BaseGeometry.buffer)
def opening(geom: BaseGeometry, **kwargs) -> BaseGeometry:
    """

    :param geom: The geometry to be opened
    :return: The opened geometry
    """
    return dilate(erode(geom, **kwargs), **kwargs)


@passes_kws_to(shapely.geometry.base.BaseGeometry.buffer)
def pro_closing(geom: BaseGeometry, **kwargs) -> BaseGeometry:
    """
      Remove Salt and Pepper

      Common Variants
    Opening and closing are themselves often used in combination to achieve more subtle results. If we represent the closing of an image f by C(f), and its opening by O(f), then some common combinations include:

    Proper Opening
    Min(f, /em{C}(O(C(f))))

    Proper Closing
    Max(f, O(C(O(f))))

    Automedian Filter
    Max(O(C(O(f))), Min(f, C(O(C(f)))))

    These operators are commonly known as morphological filters.


    Closing
    Dilation means that the central pixel will be replaced by the brightest pixel in the vicinity (filter structural element).
    Perfect for removing pepper noise and ensuring that the key features are relatively sharp.

    Opening
    Erosion means is that if we have a structuring element that is a 3 X 3 matrix, the central pixel will be replaced by the darkest pixel in the 3 X 3 neighborhood.
    Opening is erosion followed by dilation which makes it perfect for removing salt noise (white dots) and ensuring that the key features are relatively sharp.

      :param geom:
      :param kwargs:
      :return:
    """

    return opening(closing(opening(geom, **kwargs), **kwargs), **kwargs)


@passes_kws_to(shapely.geometry.base.BaseGeometry.buffer)
def pro_opening(geom: BaseGeometry, **kwargs) -> BaseGeometry:
    """
      Remove Salt and Pepper

      Common Variants
    Opening and closing are themselves often used in combination to achieve more subtle results. If we represent the closing of an image f by C(f), and its opening by O(f), then some common combinations include:

    Proper Opening
    Min(f, /em{C}(O(C(f))))

    Proper Closing
    Max(f, O(C(O(f))))

    Automedian Filter
    Max(O(C(O(f))), Min(f, C(O(C(f)))))

    These operators are commonly known as morphological filters.


    Closing
    Dilation means that the central pixel will be replaced by the brightest pixel in the vicinity (filter structural element).
    Perfect for removing pepper noise and ensuring that the key features are relatively sharp.

    Opening
    Erosion means is that if we have a structuring element that is a 3 X 3 matrix, the central pixel will be replaced by the darkest pixel in the 3 X 3 neighborhood.
    Opening is erosion followed by dilation which makes it perfect for removing salt noise (white dots) and ensuring that the key features are relatively sharp.

      :param geom:
      :param kwargs:
      :return:
    """

    return closing(opening(closing(geom, **kwargs), **kwargs), **kwargs)


# open = opening # keyword clash
erode = erosion
dilate = dilation
close = closing

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

        # A positive distance produces a dilation, a negative distance an erosion. A very small or zero distance may sometimes be used to “tidy” a polygon.
        geoms = opening(geoms)
        geoms = dilate(geoms)
        geoms = closing(geoms)
        geoms = erode(geoms)

        p = geopandas.GeoSeries(geoms)
        p.plot()
        pyplot.show()

    def ahfuashdu():
        from random import random
        import matplotlib.pyplot
        import geopandas

        circle_diameter = 100.0
        ring_width = 6.0

        circle = dilate(shapely.Point(0, 0), distance=circle_diameter)
        ring = circle.difference(erode(circle, distance=ring_width))

        noise_elements = []

        num_noise_points = 1000
        num_noise_lines = 100
        noise_amplitude = 2.0

        for i in range(num_noise_points):
            noise_elements.append(
                dilate(
                    shapely.Point(
                        -circle_diameter + random() * circle_diameter * 2,
                        -circle_diameter + random() * circle_diameter * 2,
                    ),
                    distance=random() * noise_amplitude,
                )
            )

        for i in range(num_noise_lines):
            noise_elements.append(
                dilate(
                    shapely.LineString(
                        [
                            shapely.Point(
                                -circle_diameter + random() * circle_diameter * 2,
                                -circle_diameter + random() * circle_diameter * 2,
                            )
                            for _ in range(2)
                        ]
                    ),
                    distance=random() * noise_amplitude,
                )
            )

        noisy_ring = shapely.unary_union(noise_elements + [ring])

        geopandas.GeoSeries(noisy_ring).plot()
        matplotlib.pyplot.title("noisy_ring")
        matplotlib.pyplot.show()

        some_ring = opening(noisy_ring, distance=noise_amplitude)

        geopandas.GeoSeries(some_ring).plot()
        matplotlib.pyplot.title("opening_ring")
        matplotlib.pyplot.show()

        some_ring = closing(
            opening(noisy_ring, distance=noise_amplitude), distance=noise_amplitude
        )

        geopandas.GeoSeries(some_ring).plot()
        matplotlib.pyplot.title("some_ring")
        matplotlib.pyplot.show()

        pro_closing_ring = pro_closing(noisy_ring, distance=noise_amplitude)

        geopandas.GeoSeries(pro_closing_ring).plot()
        matplotlib.pyplot.title("pro_closing_ring")
        matplotlib.pyplot.show()

        pro_opening_ring = pro_opening(noisy_ring, distance=noise_amplitude)

        geopandas.GeoSeries(pro_opening_ring).plot()
        matplotlib.pyplot.title("pro_opening_ring")
        matplotlib.pyplot.show()

    def ahfuas3232hdu():
        lr = LinearRing([(-1, -1), (1, 1), (1, 1), (1, -1), (-1, -1)])
        print(dilate(lr))
        print(lr.buffer(0))

    def simple_dilate_example():
        print(dilate(shapely.Point(0, 0)))
        print(dilate(shapely.Point(0, 0), distance=0))

    simple_dilate_example()
    # ahfuas3232hdu()
    # ahfuashdu()
    # aishdjauisd()
