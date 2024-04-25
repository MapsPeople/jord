#!/usr/bin/env python3
import json
import time
from typing import Any, Iterable, List, Mapping, Optional, Union

from warg import passes_kws_to

from jord.geojson_utilities import GeoJsonGeometryTypesEnum

APPEND_TIMESTAMP = True
SKIP_MEMORY_LAYER_CHECK_AT_CLOSE = True
PIXEL_SIZE = 1
DEFAULT_NUMBER = 0
CONTRAST_ENHANCE = True
DEFAULT_LAYER_NAME = "TemporaryLayer"
DEFAULT_LAYER_CRS = "EPSG:4326"
VERBOSE = False

USE_TEMP_GROUP = False

__all__ = [
    "add_qgis_single_feature_layer",
    "add_qgis_single_geometry_layers",
    "add_qgis_multi_feature_layer",
]


def add_qgis_single_feature_layer(
    qgis_instance_handle: Any,
    geom: Any,  #: QgsGeometry,
    name: Optional[str] = None,
    crs: Optional[str] = None,
    columns: Optional[Mapping[str, Any]] = None,
    index: bool = False,
    categorise_by_attribute: Optional[str] = None,
    group: Any = None,
    visible: bool = True,
) -> List:
    """
    An example url is “Point?crs=epsg:4326&field=id:integer&field=name:string(20)&index=yes”

    :param visible:
    :param categorise_by_attribute:
    :param group:
    :param columns: Field=name:type(length,precision) Defines an attribute of the layer. Multiple field parameters can be added to the data provider definition. Type is one of “integer”, “double”, “string”.
    :param index: index=yes Specifies that the layer will be constructed with a spatial index
    :param qgis_instance_handle:
    :param geom:
    :type geom: QgsGeometry
    :param name:
    :type name: Optional[str]
    :param crs: Crs=definition Defines the coordinate reference system to use for the layer. Definition is any string accepted by QgsCoordinateReferenceSystem.createFromString()
    :return: None
    :rtype: None
    """
    # noinspection PyUnresolvedReferences
    from qgis.core import (
        QgsVectorLayer,
        QgsFeature,
        QgsVectorLayer,
        QgsRasterLayer,
        QgsProject,
    )
    from .categorisation import categorise_layer

    # noinspection PyUnresolvedReferences
    import qgis

    # uri = geom.type()
    # uri = geom.wkbType()
    # uri = geom.wktTypeStr()

    return_collection = []

    geom_type = json.loads(geom.asJson())["type"]
    uri = geom_type  # TODO: URI MIGHT BE NONE?
    if uri is None:
        raise Exception(f"Could not load {geom.asJson()} as json")

    if name is None:
        name = DEFAULT_LAYER_NAME

    if crs is None:
        crs = DEFAULT_LAYER_CRS

    layer_name = f"{name}"
    if APPEND_TIMESTAMP:
        layer_name += f"_{time.time()}"

    if columns:
        fields = {k: solve_type(v) for k, v in columns}
    else:
        fields = None

    if categorise_by_attribute and fields:
        assert (
            categorise_by_attribute in fields
        ), f"{categorise_by_attribute} was not found in {fields}"

    if qgis_instance_handle is None:
        qgis_project = QgsProject.instance()
    elif not isinstance(qgis_instance_handle, QgsProject):
        qgis_project = qgis_instance_handle.qgis_project
    else:
        qgis_project = qgis_instance_handle

    if geom_type == GeoJsonGeometryTypesEnum.geometry_collection.value.__name__:
        for g in geom.asGeometryCollection():  # TODO: Look into recursion?
            uri = json.loads(g.asJson())["type"]
            if uri is None:
                raise Exception(f"Could not load {g.asJson()} as json")
            sub_type = uri  # TODO: URI MIGHT BE NONE?

            uri += "?"

            if crs:
                uri += f"crs={crs}"

            if fields:
                uri = str(uri).rstrip("&")
                for k, v in fields.items():
                    uri += f"&field={k}:{v}"

            uri = str(uri).rstrip("&")
            uri += f'&index={"yes" if index else "no"}'
            uri.replace("?&", "?")

            feat = QgsFeature()
            feat.setGeometry(g)

            if columns:
                feat.initAttributes(len(columns))

                if False:
                    for field_idx, attr in enumerate(columns.values()):
                        feat.setAttribute(field_idx, attr)
                else:
                    feat.setAttributes(
                        list(to_string_if_not_of_exact_type(columns.values()))
                    )

            sub_layer = QgsVectorLayer(uri, f"{layer_name}_{sub_type}", "memory")
            layer_data_provider = sub_layer.dataProvider()
            layer_data_provider.addFeatures([feat])
            layer_data_provider.updateExtents()

            if SKIP_MEMORY_LAYER_CHECK_AT_CLOSE:
                sub_layer.setCustomProperty("skipMemoryLayersCheck", 1)

            if categorise_by_attribute:
                categorise_layer(sub_layer, categorise_by_attribute)

            sub_layer.commitChanges()
            sub_layer.updateFields()
            sub_layer.updateExtents()

            return_collection.append(sub_layer)

            if group:

                qgis_project.addMapLayer(sub_layer, False)
                group.insertLayer(0, sub_layer)
            else:
                qgis_project.addMapLayer(sub_layer)

            layer_tree_handle = qgis_project.layerTreeRoot().findLayer(sub_layer.id())
            if layer_tree_handle:
                layer_tree_handle.setItemVisibilityChecked(visible)
    else:
        uri += "?"

        if crs:
            uri += f"crs={crs}"

        if fields:
            uri = str(uri).rstrip("&")
            for k, v in fields.items():
                uri += f"&field={k}:{v}"

        uri = str(uri).rstrip("&")
        uri += f'&index={"yes" if index else "no"}'
        uri.replace("?&", "?")

        feat = QgsFeature()
        feat.setGeometry(geom)

        if columns:
            feat.initAttributes(len(columns))

            if False:
                for field_idx, attr in enumerate(columns.values()):
                    feat.setAttribute(field_idx, attr)
            else:
                feat.setAttributes(
                    list(to_string_if_not_of_exact_type(columns.values()))
                )

        layer = QgsVectorLayer(uri, layer_name, "memory")
        layer_data_provider = (
            layer.dataProvider()
        )  # DEFAULT DATA PROVIDER, TODO: MAYBE CHANGE THIS
        layer_data_provider.addFeatures([feat])
        layer_data_provider.updateExtents()

        if SKIP_MEMORY_LAYER_CHECK_AT_CLOSE:
            layer.setCustomProperty("skipMemoryLayersCheck", 1)

        if categorise_by_attribute:
            categorise_layer(layer, categorise_by_attribute)

        layer.commitChanges()
        layer.updateFields()
        layer.updateExtents()

        return_collection.append(layer)

        if group:
            qgis_project.addMapLayer(layer, False)
            group.insertLayer(0, layer)
        else:
            qgis_project.addMapLayer(layer)

        layer_tree_handle = qgis_project.layerTreeRoot().findLayer(layer.id())
        if layer_tree_handle:
            layer_tree_handle.setItemVisibilityChecked(visible)

    actions = qgis.utils.iface.layerTreeView().defaultActions()
    actions.showFeatureCount()
    actions.showFeatureCount()  # TODO: Duplicate?

    return return_collection


@passes_kws_to(add_qgis_single_feature_layer)
def add_qgis_single_geometry_layers(
    qgis_instance_handle: Any, geoms: Mapping, **kwargs  # [str,QgsGeometry]
) -> None:
    for name, geom in geoms.items():
        add_qgis_single_feature_layer(qgis_instance_handle, geom, name, **kwargs)


def solve_type(d: Any) -> str:
    """
    Does not support size/length yet...

    :param d:
    :return:
    """
    if not isinstance(d, bool):
        if isinstance(d, int):
            return "integer"

        elif isinstance(d, float):
            return "double"

    return "string"


def add_qgis_multi_feature_layer(
    qgis_instance_handle: Any,
    geoms: Iterable,  # [QgsGeometry]
    name: Optional[Iterable[str]] = None,
    crs: Optional[str] = None,
    columns: Optional[
        Union[Mapping[str, Mapping[str, Any]], Iterable[Mapping[str, Any]]]
    ] = None,
    categorise_by_attribute: Optional[str] = None,
    index: bool = False,
    group: Any = None,
    visible: bool = True,
) -> List:
    """

        fields  == column definition name, type, length/size
        Multiple field parameters can be added to the data provider definition. type is one of “integer”, “double”, “string”.

    An example url is “Point?crs=epsg:4326&field=id:integer&field=name:string(20)&index=yes”

    :param categorise_by_attribute:
    :param visible:
    :param group:
    :param qgis_instance_handle:
    :param geoms:
    :param name:
    :param crs:
    :param columns:
    :param index:
    :return:
    """

    from .categorisation import categorise_layer

    # noinspection PyUnresolvedReferences
    from qgis.core import (
        QgsFeature,
        QgsVectorLayer,
        QgsProject,
    )

    # noinspection PyUnresolvedReferences
    import qgis

    # uri = geom.type()
    # uri = geom.wkbType()
    # uri = geom.wktTypeStr()

    return_collection = []

    if name is None:
        name = DEFAULT_LAYER_NAME

    if crs is None:
        crs = DEFAULT_LAYER_CRS

    layer_name = f"{name}"
    if APPEND_TIMESTAMP:
        layer_name += f"_{time.time()}"

    geom_type = None
    uri = None
    features = []

    sample_row = None
    num_cols = None
    attr_generator = None
    fields = None

    if columns and len(columns):
        if isinstance(columns, Mapping):
            sample_row = next(iter(columns.values()), None)
            # TODO: Might not be ordered correctly
            # if isinstance(next(iter(columns.values())), Mapping):
            #    ...
            attr_generator = iter(columns.values())
        elif isinstance(columns, Iterable):
            sample_row = next(iter(columns), None)
            # TODO: Might not be ordered correctly
            # if isinstance(next(iter(columns.values())), Mapping):
            #    ...
            attr_generator = iter(columns)

        assert isinstance(sample_row, Mapping)

    if sample_row:
        fields = {k: solve_type(v) for k, v in sample_row.items()}
        num_cols = len(sample_row)

    if categorise_by_attribute and fields:
        assert (
            categorise_by_attribute in fields
        ), f"{categorise_by_attribute} was not found in {fields}"

    if not geoms:
        return  # No geometry

    for geom in geoms:
        geom_type_ = json.loads(geom.asJson())["type"]

        assert geom_type_ is not None, f"could not read {geom_type_=} as json"

        if geom_type_ is None:
            raise Exception(f"Could not load {geom.asJson()} as json")

        if geom_type is None:
            geom_type = geom_type_

        if uri is None:
            uri = geom_type_  # TODO: URI MIGHT BE NONE?

        assert (
            geom_type == geom_type_
        ), f"{geom_type_} is the not the same geometry type as {geom_type}"

        if geom_type == GeoJsonGeometryTypesEnum.geometry_collection.value.__name__:
            for g in geom.asGeometryCollection():  # TODO: Look into recursion?
                sub_type = json.loads(g.asJson())["type"]
                if sub_type is None:
                    raise Exception(f"Could not load {g.asJson()} as json")

                return_collection.extend(
                    add_qgis_multi_feature_layer(
                        qgis_instance_handle, g, f"{name}_{sub_type}"
                    )
                )
            return return_collection
        else:
            feat = QgsFeature()

            if attr_generator:
                row = next(attr_generator, None)
                if row:
                    feat.initAttributes(num_cols)
                    feat.setAttributes(
                        list(to_string_if_not_of_exact_type(row.values()))
                    )

            feat.setGeometry(geom)
            features.append(feat)

    if uri is None:
        raise Exception("uri is None")

    uri += "?"

    if crs:
        uri += f"crs={crs}"

    if fields:
        uri = str(uri).rstrip("&")
        for k, v in fields.items():
            uri += f"&field={k}:{v}"

    uri = str(uri).rstrip("&")
    uri += f'&index={"yes" if index else "no"}'
    uri.replace("?&", "?")

    layer = QgsVectorLayer(uri, layer_name, "memory")
    layer_data_provider = layer.dataProvider()
    layer_data_provider.addFeatures(features)
    layer_data_provider.updateExtents()

    if SKIP_MEMORY_LAYER_CHECK_AT_CLOSE:
        layer.setCustomProperty("skipMemoryLayersCheck", 1)

    if categorise_by_attribute:
        categorise_layer(layer, categorise_by_attribute)

    layer.commitChanges()
    layer.updateFields()
    layer.updateExtents()

    if qgis_instance_handle is None:
        qgis_project = QgsProject.instance()
    elif not isinstance(qgis_instance_handle, QgsProject):
        qgis_project = qgis_instance_handle.qgis_project
    else:
        qgis_project = qgis_instance_handle

    if group:
        qgis_project.addMapLayer(layer, False)
        group.insertLayer(0, layer)
    else:
        qgis_project.addMapLayer(layer)

    layer_tree_handle = qgis_project.layerTreeRoot().findLayer(layer.id())
    if layer_tree_handle:
        layer_tree_handle.setItemVisibilityChecked(visible)

    actions = qgis.utils.iface.layerTreeView().defaultActions()
    actions.showFeatureCount()  # TODO: Twice?
    actions.showFeatureCount()

    return_collection.append(layer)

    return return_collection


def to_string_if_not_of_exact_type(
    gen: Iterable, type_: Iterable[type] = (int, float)
) -> Union[str, Any]:
    """

    :param type_: Type for testing against
    :param gen: The iterable to be converted
    :return:
    """
    if not isinstance(type_, Iterable):
        type_ = [type_]

    for v in gen:
        if all([type(v) != t for t in type_]) or v is None:
            yield str(v)
        else:
            yield v
