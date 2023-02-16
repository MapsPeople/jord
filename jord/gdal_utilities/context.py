#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 1/16/23
           """

__all__ = ["SilenceGDALSession"]

from osgeo import gdal
from warg import AlsoDecorator


class SilenceGDALSession(AlsoDecorator):
    """
    Session for silencing gdal warning and errors.
    TODO: add support for having a lasting side effect or leaving last set state of error/exception handling
    """

    def __init__(self):
        ...

    def __enter__(self) -> bool:
        gdal.PushErrorHandler(
            "CPLQuietErrorHandler"
        )  # Stop GDAL printing both warnings and errors to STDERR
        gdal.UseExceptions()  # Make GDAL raise python exceptions for errors (warnings won't raise an exception)
        return True

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # gdal.GetUseExceptions()
        gdal.PopErrorHandler()  # Pop error handler previously pushed
        gdal.DontUseExceptions()  # Dont use exception anymore
        # gdal.ErrorReset()


if __name__ == "__main__":
    with SilenceGDALSession():
        ...
