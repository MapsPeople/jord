#!/usr/bin/env python3

import logging
from typing import Any, Iterable, Mapping

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

__all__ = ["style_layer_from_mapping", "set_3d_view_settings"]

from jord.qgis_utilities.enums import (
    Qgis3dAltitudeClamping,
    Qgis3dAltitudeBinding,
    Qgis3dCullingMode,
    Qgis3dFacade,
)

logger = logging.getLogger(__name__)


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
        symbol.setColor(QColor(*cat_color, 255))
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


def make_line_symbol(
    culling_mode, edge_color, edge_width, extrusion, facades, offset
) -> Any:
    # ->q3d.QgsPolygon3DSymbol:
    import qgis._3d as q3d

    symbol = q3d.QgsLine3DSymbol()
    symbol.setWidth(edge_width)
    symbol.setOffset(offset)
    symbol.setExtrusionHeight(extrusion)
    symbol.setRenderAsSimpleLines(True)

    return symbol


def make_point_symbol(
    culling_mode, edge_color, edge_width, extrusion, facades, offset
) -> Any:
    # ->q3d.QgsPolygon3DSymbol:
    import qgis._3d as q3d

    symbol = q3d.QgsPoint3DSymbol()
    # symbol.setShape(q3d.QgsSymbol3DShape.Cylinder)
    # symbol.setHeight()
    # symbol.setRadius(extrusion)
    # symbol.setCullingMode(culling_mode.value)
    # symbol.setTransformation(0, 0, offset)
    return symbol


def set_3d_view_settings(
    layers: QgsVectorLayer,
    *,
    offset: float = 0,
    extrusion: float = 4,
    color: TripleNumber = (222, 222, 222),
    facades: Qgis3dFacade = Qgis3dFacade.walls,
    culling_mode: Qgis3dCullingMode = Qgis3dCullingMode.front_face,
    repaint: bool = True,
    edge_width: float = 1.0,
    edge_color: TripleNumber = (255, 255, 255),
) -> None:
    if layers is None:
        return

    polygon_renderer = make_renderer(
        color,
        make_polygon_symbol(
            culling_mode, edge_color, edge_width, extrusion, facades, offset
        ),
    )

    line_renderer = make_renderer(
        color,
        make_line_symbol(
            culling_mode, edge_color, edge_width, extrusion, facades, offset
        ),
    )

    point_renderer = make_renderer(
        color,
        make_point_symbol(
            culling_mode, edge_color, edge_width, extrusion, facades, offset
        ),
    )

    for layers_inner in layers:
        if layers_inner:
            if isinstance(layers_inner, Iterable):
                for layer in layers_inner:
                    if layer:
                        set_renderer(
                            layer, line_renderer, point_renderer, polygon_renderer
                        )

                        if repaint:
                            layer.triggerRepaint()
            else:
                set_renderer(
                    layers_inner, line_renderer, point_renderer, polygon_renderer
                )
                if repaint:
                    layers_inner.triggerRepaint()


def set_renderer(layer, line_renderer, point_renderer, polygon_renderer):
    from qgis.core import QgsWkbTypes

    if layer.geometryType() == QgsWkbTypes.PointGeometry:  # QgsWkbTypes.Point:
        layer.setRenderer3D(point_renderer)
    elif layer.geometryType() == QgsWkbTypes.LineGeometry:  # QgsWkbTypes.Line:
        layer.setRenderer3D(line_renderer)
    elif layer.geometryType() == QgsWkbTypes.PolygonGeometry:  # QgsWkbTypes.Polygon:
        layer.setRenderer3D(polygon_renderer)
    else:
        logger.error(f"geometry type not supported: {layer.geometryType()}, skipping")


def make_renderer(color, symbol):
    import qgis._3d as q3d

    apply_common_symbol_settings(symbol)
    apply_material(color, symbol)
    renderer = q3d.QgsVectorLayer3DRenderer()
    renderer.setSymbol(symbol)

    return renderer


def make_polygon_symbol(
    culling_mode, edge_color, edge_width, extrusion, facades, offset
) -> Any:
    # ->q3d.QgsPolygon3DSymbol:
    import qgis._3d as q3d

    symbol = q3d.QgsPolygon3DSymbol()
    symbol.setCullingMode(culling_mode.value)
    symbol.setOffset(offset)
    symbol.setExtrusionHeight(extrusion)
    symbol.setRenderedFacade(facades.value)

    if edge_width > 0:
        symbol.setEdgesEnabled(True)
    else:
        symbol.setEdgesEnabled(False)

    symbol.setEdgeWidth(edge_width)
    symbol.setEdgeColor(QColor(*edge_color))
    symbol.setAddBackFaces(False)
    # symbol.setInvertNormals(False)

    return symbol


def apply_common_symbol_settings(symbol) -> None:
    if symbol is None:
        logger.error("symbol is None, skipping")
        return

    if hasattr(symbol, "setAltitudeBinding"):
        symbol.setAltitudeBinding(Qgis3dAltitudeBinding.centroid.value)
    if hasattr(symbol, "setAltitudeClamping"):
        symbol.setAltitudeClamping(Qgis3dAltitudeClamping.absolute.value)


def apply_material(color, symbol) -> None:
    import qgis._3d as q3d

    material_settings = q3d.QgsPhongMaterialSettings()

    q_color = QColor(*color)
    material_settings.setAmbient(q_color)
    material_settings.setDiffuse(q_color)
    material_settings.setSpecular(q_color)
    symbol.setMaterialSettings(material_settings)
