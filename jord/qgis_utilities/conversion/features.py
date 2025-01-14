import logging
from typing import Any, Optional, Tuple

import shapely

logger = logging.getLogger(__name__)

__all__ = [
    "MissingFeatureError",
    "GeometryIsInvalidError",
    "GeometryIsEmptyError",
    "layer_data_generator",
    "feature_to_shapely",
    "parse_q_value",
]


class MissingFeatureError(Exception): ...


class GeometryIsEmptyError(Exception): ...


class GeometryIsInvalidError(Exception): ...


def parse_q_value(v: Any) -> Any:
    """

    :param v:
    :return:
    """
    # noinspection PyUnresolvedReferences
    from qgis.PyQt.QtCore import QVariant

    if isinstance(v, QVariant):
        if v.isNull():
            v = None
        else:
            v = v.value()

    return v


def layer_data_generator(layer_tree_layer: Any) -> Tuple:
    """

    :param layer_tree_layer:
    :return:
    """
    geometry_layer = layer_tree_layer.layer()
    if (
        geometry_layer
        and geometry_layer.hasFeatures()
        and geometry_layer.featureCount() > 0
    ):
        for layer_feature in geometry_layer.getFeatures():
            layer_feature_attributes = {
                k.name(): parse_q_value(v)
                for k, v in zip(
                    layer_feature.fields(),
                    layer_feature.attributes(),
                )
            }
            if len(layer_feature_attributes) == 0:
                logger.error(
                    f"Did not find attributes, skipping {layer_tree_layer.name()} {list(geometry_layer.getFeatures())}"
                )
            else:
                logger.info(
                    f"found {layer_feature_attributes=} for {layer_tree_layer.name()=}"
                )
            yield layer_feature_attributes, layer_feature
    else:
        raise MissingFeatureError(
            f"no feature was not found for {layer_tree_layer.name()}"
        )


def feature_to_shapely(
    layer_feature: Any,
) -> Optional[shapely.geometry.base.BaseGeometry]:
    """

    :param layer_feature:
    :return:
    """
    feature_geom = layer_feature.geometry()
    if feature_geom is not None:
        if True:
            if not feature_geom.isGeosValid():
                msg = (
                    f"{layer_feature.id()=} is not a valid geometry, {feature_geom.lastError()}\n"
                    f"{feature_geom.validateGeometry()}"
                )
                logger.error(msg)
                if True:
                    raise GeometryIsInvalidError(msg)
                elif False:
                    feature_geom = feature_geom.makeValid()

        if True:
            if feature_geom.isNull() or feature_geom.isEmpty():
                raise GeometryIsEmptyError(f"{layer_feature.id()=} is empty")

        geom_wkb = feature_geom.asWkb()
        if geom_wkb is not None:
            if not isinstance(geom_wkb, bytes):
                geom_wkb = bytes(geom_wkb)
            return shapely.from_wkb(geom_wkb)
