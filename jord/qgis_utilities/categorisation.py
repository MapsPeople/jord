#!/usr/bin/env python3

import random
from itertools import cycle
from typing import Callable, Generator, Iterable, Sized

# noinspection PyUnresolvedReferences
from qgis.PyQt.QtGui import QColor

# noinspection PyUnresolvedReferences
from qgis.core import (
    QgsCategorizedSymbolRenderer,
    QgsRendererCategory,
    QgsSimpleFillSymbolLayer,
    QgsSymbol,
    QgsVectorLayer,
)

# noinspection PyUnresolvedReferences
from qgis.utils import iface
from warg import QuadNumber, TripleNumber, n_uint_mix_generator_builder

__all__ = [
    "categorise_layer",
    "random_color_alpha_generator",
    "random_color_generator",
    "random_rgba",
    "random_rgb",
]


def random_rgb(mix: TripleNumber = (255, 255, 255)) -> TripleNumber:
    red = random.randrange(0, mix[0])
    green = random.randrange(0, mix[1])
    blue = random.randrange(0, mix[2])
    return red, green, blue


def random_rgba(mix: QuadNumber = (1, 1, 1, 1)) -> QuadNumber:
    red = random.randrange(0, mix[0])
    green = random.randrange(0, mix[1])
    blue = random.randrange(0, mix[2])
    alpha = random.randrange(0, mix[3])
    return red, green, blue, alpha


def random_color_generator() -> Generator[TripleNumber, None, None]:
    while 1:
        yield random_rgb()


def random_color_alpha_generator() -> Generator[QuadNumber, None, None]:
    while 1:
        yield random_rgba()


def categorise_layer(
    layer: QgsVectorLayer,
    field_name: str = "layer",
    *,
    color_iterable: Iterable = n_uint_mix_generator_builder(
        255, 255, 255, mix_min=(0, 0, 0)
    ),
    opacity: float = 1.0,
    outline_only: bool = False,
    outline_width=1.0,
) -> None:
    """

    https://qgis.org/pyqgis/3.0/core/Vector/QgsVectorLayer.html
    https://qgis.org/pyqgis/3.0/core/other/QgsFields.html

    :param layer:
    :param field_name:
    :param color_iterable:
    :return:
    """

    if isinstance(color_iterable, Sized):
        # noinspection PyTypeChecker
        color_iterable = cycle(color_iterable)

    if isinstance(color_iterable, Callable) and not isinstance(
        color_iterable, Generator
    ):
        # noinspection PyCallingNonCallable
        color_iterable = color_iterable()  # Compat

    color_iter = iter(color_iterable)

    available_field_names = layer.fields().names()

    assert (
        field_name in available_field_names
    ), f"Did not find {field_name=} in {available_field_names=}"

    render_categories = []
    for cat in layer.uniqueValues(layer.fields().indexFromName(field_name)):
        if cat is not None:
            sym = QgsSymbol.defaultSymbol(layer.geometryType())
            set_symbol_styling(color_iter, opacity, outline_only, outline_width, sym)

            render_categories.append(
                QgsRendererCategory(cat, symbol=sym, label=str(cat), render=True)
            )

    if True:  # add default
        sym = QgsSymbol.defaultSymbol(layer.geometryType())
        # https://qgis.org/pyqgis/master/core/QgsSymbolLayer.html#qgis.core.QgsSymbolLayer.setFillColor
        # https://qgis.org/pyqgis/3.40/core/QgsSimpleLineSymbolLayer.html
        # QgsLinePatternFillSymbolLayer

        # sym.symbolLayer(0).setStrokeColor(QColor(*col))
        # StrokeWidth
        # StrokeStyle
        # FillColor
        # FillStyle

        set_symbol_styling(color_iter, opacity, outline_only, outline_width, sym)

        render_categories.append(
            QgsRendererCategory("", symbol=sym, label="default", render=True)
        )

        if False:
            # render_categories.append(QgsRendererCategory()) # crashes qgis
            render_categories.append(
                QgsRendererCategory([], symbol=sym, label="EmptyList", render=True)
            )
            render_categories.append(
                QgsRendererCategory("", symbol=sym, label="EmptyString", render=True)
            )
            render_categories.append(
                QgsRendererCategory("None", symbol=sym, label="None", render=True)
            )

    layer.setRenderer(QgsCategorizedSymbolRenderer(field_name, render_categories))
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())


def set_symbol_styling(color_iter, opacity, outline_only, outline_width, sym) -> None:
    col = next(color_iter)
    if len(col) == 3:
        col = (*col, 255)
    if outline_only:
        outline_symbol_layer = QgsSimpleFillSymbolLayer()
        outline_symbol_layer.setColor(QColor("transparent"))
        outline_symbol_layer.setStrokeWidth(outline_width)
        outline_symbol_layer.setStrokeColor(QColor(*col))
        sym.changeSymbolLayer(0, outline_symbol_layer)
    else:
        sym.setColor(QColor(*col))
    sym.setOpacity(opacity)
