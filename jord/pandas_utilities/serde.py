from typing import Any, Collection, List, Mapping, Optional

from pandas import DataFrame

__all__ = ["df_to_columns", "columns_to_df"]


def df_to_columns(
    shape_df: DataFrame, ignored_columns: Optional[Collection] = None
) -> List[Mapping[str, Any]]:
    columns = []

    for key, c in shape_df.iterrows():
        o = {"key": key, **dict(c)}

        if ignored_columns:
            for p in ignored_columns:
                o.pop(p)

        columns.append(o)

    return columns


def columns_to_df(columns: List[Mapping[str, Any]]) -> DataFrame: ...
