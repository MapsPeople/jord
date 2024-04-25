from typing import Mapping, Any, Optional

import shapely
from shapely import Point
from shapely.geometry.base import BaseGeometry

from jord.shapely_utilities import dilate
from .morphology import closing, opening

__all__ = [
    "zero_buffer",
    "deflimmer",
    "clean_geometry",
    "unflimmer",
    "sanitise",
    "clean_shape",
]


def zero_buffer(
    geom: BaseGeometry,
) -> BaseGeometry:
    return dilate(geom, distance=0)


def clean_shape(
    shape: shapely.geometry.base.BaseGeometry,
) -> shapely.geometry.base.BaseGeometry:
    """
    removes self-intersections and duplicate points

    :param shape: The shape to cleaned
    :return: the cleaned shape
    """
    return zero_buffer(shape).simplify(0)


def deflimmer(geom: BaseGeometry, eps: float = 1e-7) -> BaseGeometry:
    """

    :param geom:
    :param eps:
    :return:
    """
    return opening(closing(geom, distance=eps), distance=eps)


clean_geometry = unflimmer = deflimmer


def sanitise(
    geom: BaseGeometry,
    *args: callable,
    kwargs: Optional[Mapping[callable, Mapping[str, Any]]] = None
) -> BaseGeometry:
    """
      #A positive distance produces a dilation, a negative distance an erosion. A very small or zero distance may sometimes be used to “tidy” a polygon.

    :param geom: The shape to sanitised
    :param args: The sanitisation callable steps
    :param kwargs: The sanitisation callable step kwargs in mappings with callable as key then sub-mapping is kwargs for callable
    :return: The sanitised shape
    """

    if kwargs is None:
        kwargs = {}

    if not len(args):
        args = (zero_buffer, deflimmer)

    for f in args:
        if f in kwargs:
            geom = f(geom, **(kwargs[f]))
        else:
            geom = f(geom)

    return geom


if __name__ == "__main__":

    def ausdhasu():
        p = Point((1, 1))
        print(clean_shape(p))

    ausdhasu()
