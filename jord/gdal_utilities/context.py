__author__ = "heider"
__doc__ = r"""

           Created on 1/16/23
           """

__all__ = ["SilenceGDALSession"]

from warg import AlsoDecorator

from .importing import GDAL


class SilenceGDALSession(AlsoDecorator):
    """
    Session for silencing gdal warning and errors.
    TODO: add support for having a lasting side effect or leaving last set state of error/exception handling
    """

    def __init__(self): ...

    def __enter__(self) -> bool:
        GDAL.PushErrorHandler(
            "CPLQuietErrorHandler"
        )  # Stop GDAL printing both warnings and errors to STDERR
        GDAL.UseExceptions()  # Make GDAL raise python exceptions for errors (warnings won't raise an exception)
        return True

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # gdal.GetUseExceptions()
        GDAL.PopErrorHandler()  # Pop error handler previously pushed
        GDAL.DontUseExceptions()  # Dont use exception anymore
        # gdal.ErrorReset()


if __name__ == "__main__":
    with SilenceGDALSession():
        ...
