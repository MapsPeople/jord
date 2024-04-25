#!/usr/bin/env python3

__author__ = "heider"
__doc__ = r"""

           Created on 5/5/22
           """

from pathlib import Path

with open(Path(__file__).parent / "README.md") as this_init_file:
    __doc__ += this_init_file.read()


from .procedures import *
from .serialisation import *
from .uri_utilities import *
from .client import *
from .clients import *
