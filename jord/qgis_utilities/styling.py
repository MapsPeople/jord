#!/usr/bin/env python3

import logging
from typing import Iterable, Mapping

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

__all__ = ["style_layer_from_mapping", "set3dviewsettings"]

from jord.qgis_utilities.enums import (
    Qgis3dAltitudeClamping,
    Qgis3dAltitudeBinding,
    Qgis3dCullingMode,
    Qgis3dFacade,
)


def style_layer_from_mapping(
    layer: QgsVectorLayer,
    style_mapping_field_dict: Mapping,
    field_name: str = "layer",
    default_color: TripleNumber = (0, 0, 0),
    default_opacity: float = 1.0,
    default_width: float = 0.1,
    *,
    repaint: bool = True,
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
    if repaint:
        layer.triggerRepaint()


def set3dviewsettings(
    layers: QgsVectorLayer,
    offset: float = 0,
    extrusion: float = 4,
    color: TripleNumber = (222, 222, 222),
    facades: Qgis3dFacade = Qgis3dFacade.walls,
    culling_mode: Qgis3dCullingMode = Qgis3dCullingMode.front_face,
    *,
    repaint: bool = True,
) -> None:
    if layers is None:
        return

    import qgis._3d as q3d

    symbol = q3d.QgsPolygon3DSymbol()
    symbol.setAddBackFaces(False)
    symbol.setAltitudeBinding(Qgis3dAltitudeBinding.centroid.value)
    symbol.setAltitudeClamping(Qgis3dAltitudeClamping.absolute.value)
    symbol.setCullingMode(culling_mode.value)
    # symbol.setHeight()
    symbol.setOffset(offset)
    symbol.setExtrusionHeight(extrusion)
    symbol.setRenderedFacade(facades.value)
    symbol.setEdgesEnabled(True)
    symbol.setEdgeWidth(1.0)
    symbol.setEdgeColor(QColor(255, 255, 255))

    # symbol.setInvertNormals(False)
    # symbol.setEdgeColor(QColor(0, 0, 0))
    # symbol.setShape(q3d.QgsSymbol3DShape.Cylinder)

    material_settings = q3d.QgsPhongMaterialSettings()
    qcolor = QColor(*color)

    material_settings.setAmbient(qcolor)
    material_settings.setDiffuse(qcolor)
    material_settings.setSpecular(qcolor)
    symbol.setMaterialSettings(material_settings)

    renderer = q3d.QgsVectorLayer3DRenderer()
    renderer.setSymbol(symbol)

    for layers_inner in layers:
        if layers_inner:
            if isinstance(layers_inner, Iterable):
                for layer in layers_inner:
                    if layer:
                        # renderer.setLayer(layer)
                        layer.setRenderer3D(renderer)
                        if repaint:
                            layer.triggerRepaint()
            else:
                # renderer.setLayer(layers_inner)
                layers_inner.setRenderer3D(renderer)
                if repaint:
                    layers_inner.triggerRepaint()
