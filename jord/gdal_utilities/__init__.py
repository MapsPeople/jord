#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 5/5/22
           """

from pathlib import Path

with open(Path(__file__).parent / "README.md", "r") as this_init_file:
    __doc__ += this_init_file.read()

try:
    from .conversion import *
    from .enums import *
    from .importing import *
    from .context import *
    from .cloning import *
except ImportError as ix:
    this_package_name = Path(__file__).parent.name
    print(f"Make sure gdal module is available for {this_package_name}")
    raise ix
