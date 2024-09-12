import logging
from typing import Any, Mapping, Optional

from shapely import LineString, Point
from shapely.geometry.base import BaseGeometry

from .morphology import closing, opening
from .uniformity import clean_shape, zero_buffer

__all__ = [
    "deflimmer",
    "clean_geometry",
    "unflimmer",
    "sanitise",
]

logger = logging.getLogger(__name__)


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
      #A positive distance produces a dilation, a negative distance an erosion. A very small or zero distance
      may sometimes be used to “tidy” a polygon.

    :param geom: The shape to sanitised
    :param args: The sanitisation callable steps
    :param kwargs: The sanitisation callable step kwargs in mappings with callable as key then sub-mapping is
    kwargs for callable
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

    def ausdhasu2():
        p = LineString([(1, 1), (1, 1)])
        print(clean_shape(p))

    ausdhasu2()
