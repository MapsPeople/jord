import inspect
from enum import Enum
from typing import Callable

__all__ = ["ArgumentSatisfactionEnum", "partial_satisfied"]


class ArgumentSatisfactionEnum(Enum):
    none = "none"
    args = "args"
    kws = "kws"
    argskws = "argskws"


def partial_satisfied(partial_fn: Callable) -> bool:
    """

    :param partial_fn:
    :return:
    """
    signature = inspect.signature(partial_fn.func)

    try:
        signature.bind(*partial_fn.args, **partial_fn.keywords)
        return True
    except TypeError:
        return False
