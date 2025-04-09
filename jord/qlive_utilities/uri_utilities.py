import json
from typing import Any, Mapping, Optional

__all__ = ["build_uri_oh_no"]


def build_uri_oh_no(
    geom: Any,
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

    geom_json = json.loads(geom.asJson())

    if geom_json is None:
        raise ValueError("Geom is empty")

    uri = geom_json["type"]  # As GeoJSON Repr, str dict

    if crs:
        uri += f"?crs={crs}"

    if fields:
        for k, v in fields.items():
            uri += f"&field={k}:{v}"

    uri += f'&index={"yes" if index else "no"}'

    return uri
