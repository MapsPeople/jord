import logging
from typing import Any, Mapping, Optional, Tuple

# noinspection PyUnresolvedReferences
from qgis.PyQt.QtCore import QVariant

import shapely

logger = logging.getLogger(__name__)

__all__ = [
    "MissingFeatureError",
    "GeometryIsInvalidError",
    "GeometryIsEmptyError",
    "layer_data_generator",
    "feature_to_shapely",
    "parse_q_value",
    "extract_layer_attributes",
    "extract_feature_attributes",
    "is_str_value_null_like",
    "REAL_NONE_JSON_VALUE",
    "NULL_VALUE",
    "NAN_VALUE",
    "STR_NA_VALUE",
    "STR_NONE_VALUE",
    "parse_field",
    "extract_field_value",
    "extract_layer_data_single",
]


REAL_NONE_JSON_VALUE = "REAL_NONE"
NAN_VALUE = "nan"
NULL_VALUE = "NULL"
STR_NA_VALUE = "<NA>"
STR_NONE_VALUE = "None"


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


def extract_feature_attributes(layer_feature: Any) -> dict[str, Any]:
    """

    :param layer_feature:
    :return:
    """

    return {
        k.name(): parse_q_value(v)
        for k, v in zip(
            layer_feature.fields(),
            layer_feature.attributes(),
        )
    }


def extract_layer_attributes(layer_tree_layer: Any) -> list[dict[str, Any]]:
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
        layer_feature_attributes = []
        for layer_feature in geometry_layer.getFeatures():
            layer_feature_attributes.append(extract_feature_attributes(layer_feature))

        return layer_feature_attributes

    raise MissingFeatureError(f"no feature was not found for {layer_tree_layer.name()}")


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
            layer_feature_attributes = extract_feature_attributes(layer_feature)

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
    validate: bool = True,
) -> Optional[shapely.geometry.base.BaseGeometry]:
    """

    :param validate:
    :param layer_feature:
    :return:
    """
    feature_geom = layer_feature.geometry()
    if feature_geom is not None:
        if validate:
            if not feature_geom.isGeosValid():
                msg = (
                    f"{layer_feature.id()=} is not a valid geometry, {feature_geom.lastError()}\n"
                    f"{feature_geom.validateGeometry()}"
                )
                logger.error(msg)

                if True:
                    raise GeometryIsInvalidError(msg)
                else:
                    feature_geom = feature_geom.makeValid()

        if validate:
            if feature_geom.isNull() or feature_geom.isEmpty():
                raise GeometryIsEmptyError(f"{layer_feature.id()=} is empty")
        else:
            if feature_geom.isNull() or feature_geom.isEmpty():
                return None

        geom_wkb = feature_geom.asWkb()
        if geom_wkb is not None:
            if not isinstance(geom_wkb, bytes):
                geom_wkb = bytes(geom_wkb)

            return shapely.from_wkb(geom_wkb)


def extract_layer_data_single(layer_tree_layer: Any) -> Tuple:
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
        if geometry_layer.featureCount() > 1:
            raise ValueError(f"{layer_tree_layer.name()} has more than one feature")

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

            return layer_feature_attributes, layer_feature

    raise MissingFeatureError(f"no feature was not found for {layer_tree_layer.name()}")


def parse_field(feature_attributes: Mapping[str, Any], field_name: str) -> Any:
    """

    :param feature_attributes:
    :param field_name:
    :return:
    """
    field_value = feature_attributes[field_name]

    if isinstance(field_value, str):
        ...

    elif isinstance(field_value, QVariant):
        # logger.warning(f"{typeToDisplayString(type(v))}")
        if field_value.isNull():
            field_value = None
        else:
            field_value = field_value.value()

    return field_value


def is_str_value_null_like(v_str_) -> bool:
    """

    :param v_str_:
    :return:
    """
    return (
        (v_str_ == NAN_VALUE.lower())
        or (v_str_ == NULL_VALUE.lower())
        or (v_str_ == STR_NA_VALUE.lower())
        or (v_str_ == STR_NONE_VALUE.lower())
        or len(v_str_.strip()) == 0
    )


def extract_field_value(feature_attributes: Mapping[str, Any], field_name: str) -> Any:
    """

    :param feature_attributes:
    :param field_name:
    :return:
    """
    field_value = feature_attributes.get(field_name)

    if field_value is None:
        ...

    elif isinstance(field_value, str):
        v = field_value
        v_str = v.lower().strip()

        if is_str_value_null_like(v_str):
            field_value = None

        else:
            field_value = v

    elif isinstance(field_value, QVariant):
        if field_value.isNull():
            field_value = None

        else:
            v = str(field_value.value())

            v_str = v.lower().strip()

            if is_str_value_null_like(v_str):
                field_value = None

            else:
                field_value = v

    return field_value
