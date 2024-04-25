#!/usr/bin/env python3

from enum import Enum

# noinspection PyUnresolvedReferences
from qgis.core import (
    QgsMultiBandColorRenderer,
    QgsPalettedRasterRenderer,
    QgsSingleBandColorDataRenderer,
    QgsSingleBandGrayRenderer,
    QgsSingleBandPseudoColorRenderer,
)

from jord.geojson_utilities import GeoJsonGeometryTypesEnum

__all__ = ["QgisRendererEnum", "QgisLayerTypeEnum"]


class QgisRendererEnum(Enum):
    multi_band = QgsMultiBandColorRenderer
    paletted_raster = QgsPalettedRasterRenderer
    single_band_color = QgsSingleBandColorDataRenderer
    single_band_gray = QgsSingleBandGrayRenderer
    single_band_pseudo = QgsSingleBandPseudoColorRenderer


class QgisLayerTypeEnum(Enum):
    point = GeoJsonGeometryTypesEnum.point.value.__name__
    multi_point = GeoJsonGeometryTypesEnum.multi_point.value.__name__
    line_string = GeoJsonGeometryTypesEnum.line_string.value.__name__
    multi_line_string = GeoJsonGeometryTypesEnum.multi_line_string.value.__name__
    polygon = GeoJsonGeometryTypesEnum.polygon.value.__name__
    multi_polygon = GeoJsonGeometryTypesEnum.multi_polygon.value.__name__
    curve_polygon = "CurvePolygon"
    multi_surface = "MultiSurface"
    compound_curve = "CompoundCurve"
    multi_curve = "MultiCurve"
    no_geometry = "No Geometry"
