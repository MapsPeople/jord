#!/usr/bin/env python3

__all__ = ["read_geometries"]

from pathlib import Path
from typing import Union, Tuple, Any


def read_geometries(
    fn: Union[str, Path], bbox: Tuple[float, float, float, float] = None
) -> Any:
    """
    reads to shapely geometries to features using fiona collection
    feature = dict('geometry': <shapely geometry>, 'properties': <dict with properties>

    :param fn:
    :param bbox:
    :return:
    """
    from fiona import collection
    from shapely.geometry import shape

    with collection(str(fn), "r") as c:
        ft_list = []
        c = c.items(bbox=bbox)
        for ft in c:
            if ft[1]["geometry"] is not None:
                ft_list.append(shape(ft[1]["geometry"]))

    return ft_list
