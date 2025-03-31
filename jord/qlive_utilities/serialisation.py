import base64
import json
import pickle
from enum import Enum
from typing import Any, Callable, Mapping, Sequence, Tuple, Union

from jord.qlive_utilities.procedures import QliveRPCMethodEnum, QliveRPCMethodMap

__all__ = ["build_package", "read_package"]


class SerialisationMethodEnum(Enum):
    json, pickle = "json", "pickle"


SERIALISATION_METHOD = SerialisationMethodEnum.pickle
VERBOSE = False


def build_package(
    method: QliveRPCMethodEnum, *args: Any, **kwargs
) -> Union[bytes, str, None]:
    """

    :param method:
    :param args:
    :return:
    """
    if VERBOSE:
        print(type(method), method, args)

    if not isinstance(method, QliveRPCMethodEnum):
        assert method
        assert isinstance(method, str), method
        method = QliveRPCMethodEnum(method)

    if VERBOSE:
        print(type(method.value), method.value, args)

    if SERIALISATION_METHOD == SerialisationMethodEnum.pickle:
        return pickle.dumps({"method": method.value, "args": args, "kwargs": kwargs})
    elif SERIALISATION_METHOD == SerialisationMethodEnum.json:
        return json.dumps(
            {"method": method.value, "args": args, "kwargs": kwargs}
        )  # TODO: ?
    elif False:
        ...
        # return base64.b64encode(str({"method": method.value, "args": args}).encode("ascii"))
    else:
        raise NotImplemented


def read_package(package: bytes) -> Tuple[Callable, Sequence[Any], Mapping[str, Any]]:
    """

    :param package:
    :return:
    """
    if SERIALISATION_METHOD == SerialisationMethodEnum.json:
        str_dict = (
            base64.b64decode(package)
            .decode("ascii")
            .replace(
                # Json library convert string dictionary to real dictionary type. Double quotes is standard
                # format for json
                "'",
                '"',
            )
        )
        res_dict = json.loads(str_dict)  # convert string dictionary to dict format
    elif SERIALISATION_METHOD == SerialisationMethodEnum.pickle:
        res_dict = pickle.loads(package)
    else:
        raise NotImplemented
    return (
        QliveRPCMethodMap[QliveRPCMethodEnum(res_dict["method"])],
        res_dict["args"],
        res_dict["kwargs"],
    )


if __name__ == "__main__":
    print(read_package(build_package(method=QliveRPCMethodEnum.add_wkt)))
    print(read_package(build_package(method=QliveRPCMethodEnum.add_wkb)))
    print(read_package(build_package(method=QliveRPCMethodEnum.add_dataframe_layer)))
