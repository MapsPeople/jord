from typing import Union

from .importing import GDAL, OGR

__all__ = ["clone_data_to_memory", "clone_raster_to_memory", "clone_vector_to_memory"]


def clone_data_to_memory(
    ds: Union[GDAL.Dataset, OGR.DataSource], name: str = ""
) -> Union[GDAL.Dataset, OGR.DataSource]:
    """

    :param ds:
    :param name:
    :return:
    """
    if isinstance(ds, GDAL.Dataset):
        return clone_raster_to_memory(ds, name)
    elif isinstance(ds, OGR.DataSource):
        return clone_vector_to_memory(ds, name)
    else:
        raise TypeError("Data source must be of GDAL dataset or OGR datasource")


def clone_vector_to_memory(vector_ds: OGR.DataSource, name: str = "") -> OGR.DataSource:
    """

    :param vector_ds:
    :param name:
    :return:
    """
    return OGR.GetDriverByName("Memory").CopyDataSource(vector_ds, name)


def clone_raster_to_memory(raster_ds: GDAL.Dataset, name: str = "") -> GDAL.Dataset:
    """

    :param raster_ds:
    :param name:
    :return:
    """
    return GDAL.GetDriverByName("MEM").CopyDataSource(raster_ds, name)
