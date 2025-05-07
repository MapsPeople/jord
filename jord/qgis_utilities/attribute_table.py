from typing import Any, Collection

__all__ = ["set_column_visibility", "set_visible_columns"]


def set_column_visibility(layers: Any, column_name: str, visible: bool = False) -> None:
    if not isinstance(layers, Collection):
        layers = [layers]

    for layer in layers:
        config = layer.attributeTableConfig()
        columns = config.columns()
        for column in columns:
            if column.name == column_name:
                column.hidden = not visible
                break
        config.setColumns(columns)
        layer.setAttributeTableConfig(config)


def set_visible_columns(layers: Any, column_names: Collection[str]) -> None:
    if not isinstance(layers, Collection):
        layers = [layers]

    for layer in layers:
        config = layer.attributeTableConfig()
        columns = config.columns()
        for column in columns:
            if column.name in column_names:
                column.hidden = True
            else:
                column.hidden = False
        config.setColumns(columns)
        layer.setAttributeTableConfig(config)
