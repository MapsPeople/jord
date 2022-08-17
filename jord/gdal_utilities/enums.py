# !/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 5/5/22
           """

from enum import Enum

from jord.gdal_utilities.importing import GDAL


class GdalAccessEnum(Enum):
    """
    Enum for GDAL.Access
    """

    read_only = GDAL.GA_ReadOnly  # Default  = 0
    """  Read-only access."""

    update = GDAL.GA_Update
    """  Update access."""
