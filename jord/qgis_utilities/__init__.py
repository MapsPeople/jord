#!/usr/bin/env python3

__author__ = "heider"
__doc__ = r"""

            This module must remain clean and clear of additional external dependencies outside of qgis, and base requirements of jord.

           Created on 5/5/22
           """

import logging
from pathlib import Path

with open(Path(__file__).parent / "README.md") as this_init_file:
    __doc__ += this_init_file.read()

try:
    from .importing import *
    from .configuration import *

    # from .helpers import * # import issues
    # from .numpy_utilities import *
    from .data_provider import *
    from .geometry_types import *
    from .conversion import *

    # from .styles import *
    # from .categorisation import *
    # from .styling import *
    # from .plugin_version import *
except ImportError as ix:
    this_package_name = Path(__file__).parent.name
    logging.error(f"Make sure qgis module is available for {this_package_name}")
    raise ix
