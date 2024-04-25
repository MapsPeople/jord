from typing import Any

__all__ = ["deepcopy_layer"]


def deepcopy_layer(layer) -> Any:
  # noinspection PyUnresolvedReferences
  from qgis.core import QgsFeatureRequest

  new_layer = layer.materialize(
    QgsFeatureRequest().setFilterFids(layer.allFeatureIds())
  )

  if False:
    for r in layer.featureRendererGenerators():
      new_layer.addFeatureRendererGenerator(r)

  return new_layer
