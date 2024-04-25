#!/usr/bin/env python3

import inspect
from enum import Enum
from typing import Callable


class ArgumentSatisfactionEnum(Enum):
    none = "none"
    args = "args"
    kws = "kws"
    argskws = "argskws"


def partial_satisfied(partial_fn: Callable) -> bool:
    signature = inspect.signature(partial_fn.func)
    try:
        signature.bind(*partial_fn.args, **partial_fn.keywords)
        return True
    except TypeError:
        return False
