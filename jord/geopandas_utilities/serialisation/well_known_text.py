#!/usr/bin/env python3

from enum import Enum
from pathlib import Path
from typing import Sequence

import pandas
from pandas import DataFrame
from shapely import wkt

__all__ = ["load_wkts_from_csv", "csv_wkt_generator"]


# from sorcery import assigned_names


class WktTypeEnum(Enum):
    (
        point,
        multipoint,
        linestring,
        multilinestring,
        polygon,
        multipolygon,
        geometrycollection,
    ) = (
        "point",
        "multipoint",
        "linestring",
        "multilinestring",
        "polygon",
        "multipolygon",
        "geometrycollection",
    )  # assigned_names()


def load_wkts_from_csv(
    csv_file_path: Path, geometry_column: str = "Shape", additional_cols: Sequence = ()
) -> DataFrame:
    """
    Well-Known Text
    """
    df = pandas.read_csv(
        str(csv_file_path), usecols=[*additional_cols, geometry_column]
    )
    df[geometry_column] = df[geometry_column].apply(wkt.loads)
    return df


def csv_wkt_generator(csv_file_path: Path, geometry_column: str = "Shape") -> wkt:
    """

    :param csv_file_path:
    :param geometry_column:
    :return:
    """
    for idx, g in pandas.read_csv(
        str(csv_file_path), usecols=[geometry_column]
    ).iterrows():
        yield wkt.loads(g)


if __name__ == "__main__":

    def uashdu():
        for t in WktTypeEnum:
            print(t)

    uashdu()
