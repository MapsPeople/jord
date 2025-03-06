import datetime
from typing import Any, List, Optional

ADD_STRING_LEN = True
NUM_MB16_CHARS = 16777216

__all__ = ["solve_type", "solve_type_configuration"]


def solve_type(d: Any) -> str:
    """
    Does not support size/length yet...

    QGUS Availible Field types:
    ________________           - Provider type ( MemoryLayer) - implemented

    Whole Number (integer) - integer - X
    Decimal Number (real) - double - X
    Text (string) - string - X
    Date - date - X
    Time - time - X
    Date & Time - datetime - X
    Whole Number ( ... llint - 16bit) - int2 - O
    Whole Number (integer - 32bit) - int4 - O
    Whole Number (integer - 64bit) - int8 - O
    Decimal Number (numeric) - numeric - O
    Decimal Number (decimal) - decimal - O
    Decimal Number (real) - real - O
    Decimal Number (double) - double precision - O
    Text, unlimited length (text) - text - X
    Boolean - boolean  - X
    Binary Object (BLOB) - binary - X
    String List - stringlist - X
    Integer List - integerlist - O
    Decimal (double) List - doublelist - O
    Integer (64 bit) List - integer64list - O
    Map - map - O
    Geometry - geometry - O

    :param d:
    :return:
    """
    if not isinstance(d, bool):
        if isinstance(d, int):
            return "integer"

        elif isinstance(d, float):
            return "double"

        elif isinstance(d, bytes):
            return "binary"

        elif isinstance(d, (list, tuple, set)):  # ASSUME IS STRINGS
            return "stringlist"

        elif isinstance(d, datetime.datetime):
            return "datetime"

        elif isinstance(d, datetime.date):
            return "date"

        elif isinstance(d, datetime.time):
            return "time"

        elif isinstance(d, str):
            if False:
                if (
                    ADD_STRING_LEN
                ):  # WARNING! Shapefiles have a limitation of maximum 254 characters per field
                    return f"string({min(max(len(d) * 16, 255), NUM_MB16_CHARS)})"  # 16x buffer for large strings
            else:
                return "text"

    if isinstance(d, bool):
        if False:
            if ADD_STRING_LEN:
                return "string(255)"  # True, False (5)
        else:
            return "boolean"

    if False:
        return "text"

    return "string"


def solve_type_configuration(
    d: Any,
    k: Optional[str],
    columns: Optional[List],
    allocation_multiplier: Optional[int] = 2,
) -> Optional[str]:
    """

    :param d:
    :param k:
    :param columns:
    :param allocation_multiplier:
    :return:
    """
    if isinstance(d, str):
        a = len(d)

        if k and columns:
            max_len = a

            if isinstance(columns, List):
                for cols in columns:
                    c = cols[k]
                    if isinstance(c, str):
                        max_len = max(max_len, len(c))

            a = max_len

        if allocation_multiplier:
            a *= allocation_multiplier

        a = max(a, 255)
        return str(a)

    return None
