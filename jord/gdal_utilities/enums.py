__author__ = "heider"
__doc__ = r"""

           Created on 5/5/22
           """

from enum import Enum

from jord.gdal_utilities.importing import GDAL

__all__ = ["GdalAccessEnum"]


class GdalAccessEnum(Enum):
    """
    Enum for GDAL.Access
    """

    read_only = GDAL.GA_ReadOnly  # Default  = 0
    """  Read-only access."""

    update = GDAL.GA_Update
    """  Update access."""
