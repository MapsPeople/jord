#!/usr/bin/env python3

__all__ = ["build_uri"]

import json
from typing import Optional, Mapping


def build_uri(
    geom,
    crs: Optional[str] = None,
    fields: Optional[Mapping[str, str]] = None,
    index: bool = False,
) -> str:
    """

    :param geom:
    :param crs:
    :param fields:
    :param index:
    :return:
    :rtype: str
    """
    uri = json.loads(geom.asJson())["type"]  # As GeoJSON Repr, str dict

    if crs:
        uri += f"?crs={crs}"

    if fields:
        for k, v in fields.items():
            uri += f"&field={k}:{v}"

    uri += f'&index={"yes" if index else "no"}'

    return uri
