#!/usr/bin/env python3

import logging
from typing import Mapping

# noinspection PyUnresolvedReferences
from qgis.PyQt.QtGui import QColor

# noinspection PyUnresolvedReferences
from qgis.core import (
    QgsCategorizedSymbolRenderer,
    QgsLineSymbol,
    QgsRendererCategory,
    QgsSymbol,
    QgsVectorLayer,
)
from warg import TripleNumber

__all__ = ["style_layer_from_mapping"]

from jord.qgis_utilities.enums import Qgis3dCullingMode, Qgis3dFacade


def style_layer_from_mapping(
    layer: QgsVectorLayer,
    style_mapping_field_dict: Mapping,
    field_name: str = "layer",
    default_color: TripleNumber = (0, 0, 0),
    default_opacity: float = 1.0,
    default_width: float = 0.1,
) -> None:
    if layer is None:
        return

    style_mapping = style_mapping_field_dict[field_name]

    render_categories = []
    for cat in layer.uniqueValues(layer.fields().indexFromName(field_name)):
        cat_color = default_color
        cat_opacity = default_opacity
        cat_width = default_width
        label = str(cat)

        if cat in style_mapping.keys():
            style = style_mapping[label]
            if "color" in style:
                cat_color = (
                    int(n) for n in style["color"]
                )  # TODO: also support with AlphaChannel | Qt.GlobalColor | QGradient
            if "opacity" in style:
                cat_opacity = max(0.0, min(float(style["opacity"]), 1.0))
            if "width" in style:
                cat_width = max(0.0, float(style["width"]))

        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        symbol.setColor(QColor(*(cat_color), 255))
        symbol.setOpacity(cat_opacity)

        if isinstance(symbol, QgsLineSymbol):
            symbol.setWidth(cat_width)
        else:
            logging(f"width ignored, symbol is of type: {type(symbol)}")

        render_categories.append(
            QgsRendererCategory(cat, symbol=symbol, label=label, render=True)
        )

    layer.setRenderer(QgsCategorizedSymbolRenderer(field_name, render_categories))
    layer.triggerRepaint()


def set3dviewsettings(
    layer: QgsVectorLayer,
    offset: float = 0,
    extrusion: float = 4,
) -> None:
    if layer is None:
        return

    import qgis._3d as q3d

    symbol = q3d.QgsPolygon3DSymbol()
    symbol.setAddBackFaces(False)
    symbol.setAltitudeBinding(1)
    symbol.setAltitudeClamping(0)
    symbol.setCullingMode(Qgis3dCullingMode.front_face.value)
    # symbol.setHeight()
    symbol.setOffset(offset)
    symbol.setExtrusionHeight(extrusion)
    symbol.setRenderedFacade(Qgis3dFacade.walls.value)
    symbol.setEdgesEnabled(True)
    symbol.setEdgeWidth(0.1)

    # symbol.setInvertNormals(False)
    # symbol.setEdgeColor(QColor(0, 0, 0))
    # symbol.setShape(q3d.QgsSymbol3DShape.Cylinder)

    material_settings = q3d.QgsPhongMaterialSettings()
    material_settings.setAmbient(QColor(255, 0, 0))
    material_settings.setDiffuse(QColor(255, 0, 0))
    material_settings.setSpecular(QColor(255, 0, 0))
    symbol.setMaterial(material_settings)

    renderer = q3d.QgsVectorLayer3DRenderer()
    renderer.setSymbol(symbol)

    # renderer.setLayer(layer)
    layer.setRenderer3D(renderer)
    layer.triggerRepaint()
