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

__all__ = ["QgisRendererEnum", "QgisLayerTypeEnum", "Qgis3dCullingMode", "Qgis3dFacade"]


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


class Qgis3dCullingMode(Enum):
    no_culling = 0  # Qgs3DTypes.CullingMode.NoCulling
    back_face = 1
    front_face = 2
    front_and_back_face = 3


class AltitudeBinding(Enum):
    vertex = 0  # Vertex: Clamp every vertex of feature

    centroid = 1  # Centroid: Clamp just centroid of feature


class AltitudeClamping(Enum):
    absolute = 0  # Absolute: Elevation is taken directly from feature and is independent of terrain height (
    # final elevation = feature elevation)

    relative = 1  # Relative: Elevation is relative to terrain height (final elevation = terrain elevation +
    # feature elevation)

    terrain = 2  # Terrain: Elevation is clamped to terrain (final elevation = terrain elevation)


class Qgis3dFacade(Enum):
    no_facade = 0
    walls = 1
    roofs = 2
    walls_and_roofs = 3
