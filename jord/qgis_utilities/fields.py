import logging
from typing import Any, Iterable, Sequence

# noinspection PyUnresolvedReferences
from qgis.core import QgsDefaultValue, QgsEditorWidgetSetup, QgsFieldConstraints

__all__ = [
    "add_dropdown_widget",
    "make_field_unique",
    "HIDDEN_WIDGET",
    "make_field_not_null",
    "make_field_default",
    "make_field_boolean",
    "make_field_reuse_last_entered_value",
]

IGNORE_THIS_STRING = """

Line edit – a simple edit box
Classification – displays a combo box with the values used for “unique value” classification (symbology tab)
Range – allows numeric values within a given range, the widget can be either slider or spin box
Unique values
    editable – displays a line edit widget with auto-completion suggesting values already used in the
    attribute table
    not editable – displays a combo box with already used values
File name – adds a file chooser dialog
Value map – shows a combo box with predefined description/value items
Enumeration – a combo box with values that can be used within the columns type
Immutable – read-only
Hidden – makes the attribute invisible for the user
CheckBox – a checkbox with customizable representation for both checked and unchecked state
Text edit – an edit box that allow multiple input lines
Calendar – a calendar widget to input dates
"""

IGNORE_THIS_STRING2 = """
QGIS Widget Types
_________________

Binary

Checkbox

Classification

Color

DateTime

Enumeration

Attachment

Geometry

Hidden

JsonView

KeyValue

List

Range

RelationReference

TextEdit

UniqueValues

UuidGenerator

ValueMap

ValueRelation

"""

HIDDEN_WIDGET = QgsEditorWidgetSetup("Hidden", {})
CHECKBOX_WIDGET = QgsEditorWidgetSetup(
    "CheckBox",
    {
        "Checked state": "True",
        "Unchecked state": "False",
    },
)
UNIQUE_VALUES_WIDGET = QgsEditorWidgetSetup(
    "UniqueValues",
    {"Editable": True},
)

logger = logging.getLogger(__name__)


def add_dropdown_widget(layers: Any, field_name: str, form_widget: Any) -> None:
    """
    https://gis.stackexchange.com/questions/470963/setting-dropdown-on-feature-attribute-form-using-plugin
      :param layer:
      :param field_name:
      :param form_widget:
      :return:
    """

    if layers is None:
        return

    for layers_inner in layers:
        if layers_inner:
            if isinstance(layers_inner, Iterable):
                for layer in layers_inner:
                    if layer:
                        idx = layer.fields().indexFromName(field_name)
                        if idx < 0:
                            continue
                        layer.setEditorWidgetSetup(
                            idx,
                            form_widget,
                        )
            else:
                idx = layers_inner.fields().indexFromName(field_name)
                if idx < 0:
                    continue
                layers_inner.setEditorWidgetSetup(
                    idx,
                    form_widget,
                )


def make_field_unique(
    layers: Sequence[Any], field_name: str = "admin_id", auto_generate: bool = True
) -> None:
    if layers is None:
        return

    unique_widget = None
    default_value_generator = None

    if False:
        unique_widget = QgsEditorWidgetSetup(
            "UuidGenerator",
            {},
        )
        if False:
            logger.error(unique_widget.config())
    elif auto_generate:
        default_value_generator = QgsDefaultValue()
        default_value_generator.setExpression("rtrim( ltrim( uuid(), '{'), '}')")
    else:
        unique_widget = UNIQUE_VALUES_WIDGET

    for layers_inner in layers:
        if layers_inner:
            if isinstance(layers_inner, Iterable):
                for layer in layers_inner:
                    if layer:
                        idx = layer.fields().indexFromName(field_name)
                        if idx < 0:
                            continue

                        if unique_widget:
                            layer.setEditorWidgetSetup(
                                idx,
                                unique_widget,
                            )
                        elif default_value_generator:
                            layer.setDefaultValueDefinition(
                                idx, default_value_generator
                            )
                        else:
                            raise NotImplementedError

                        layer.setFieldConstraint(
                            idx, QgsFieldConstraints.ConstraintNotNull
                        )
                        layer.setFieldConstraint(
                            idx, QgsFieldConstraints.ConstraintUnique
                        )
            else:
                idx = layers_inner.fields().indexFromName(field_name)

                if idx < 0:
                    continue

                if unique_widget:
                    layers_inner.setEditorWidgetSetup(
                        idx,
                        unique_widget,
                    )
                elif default_value_generator:
                    layers_inner.setDefaultValueDefinition(idx, default_value_generator)
                else:
                    raise NotImplementedError

                layers_inner.setFieldConstraint(
                    idx, QgsFieldConstraints.ConstraintNotNull
                )
                layers_inner.setFieldConstraint(
                    idx, QgsFieldConstraints.ConstraintUnique
                )


def make_field_not_null(layers: Sequence[Any], field_name: str = "name") -> None:
    if layers is None:
        return

    for layers_inner in layers:
        if layers_inner:
            if isinstance(layers_inner, Iterable):
                for layers in layers_inner:
                    if layers:
                        idx = layers.fields().indexFromName(field_name)
                        if idx < 0:
                            continue

                        layers.setFieldConstraint(
                            idx, QgsFieldConstraints.ConstraintNotNull
                        )
            else:
                idx = layers_inner.fields().indexFromName(field_name)
                if idx < 0:
                    continue
                layers_inner.setFieldConstraint(
                    idx, QgsFieldConstraints.ConstraintNotNull
                )


def make_field_default(
    layers: Sequence[Any], field_name: str, default_expression: str = "'None'"
) -> None:
    if layers is None:
        return

    default_value = QgsDefaultValue()
    default_value.setExpression(default_expression)

    for layers_inner in layers:
        if layers_inner:
            if isinstance(layers_inner, Iterable):
                for layers in layers_inner:
                    if layers:
                        layers.setDefaultValueDefinition(
                            layers.fields().indexFromName(field_name), default_value
                        )
            else:
                layers_inner.setDefaultValueDefinition(
                    layers_inner.fields().indexFromName(field_name), default_value
                )


def make_field_boolean(layers: Sequence[Any], field_name: str) -> None:
    if layers is None:
        return

    for layers_inner in layers:
        if layers_inner:
            if isinstance(layers_inner, Iterable):
                for layers in layers_inner:
                    if layers:
                        idx = layers.fields().indexFromName(field_name)

                        if idx < 0:
                            continue

                        layers.setDefaultValueDefinition(idx, CHECKBOX_WIDGET)
            else:
                idx = layers_inner.fields().indexFromName(field_name)

                if idx < 0:
                    continue

                layers_inner.setEditorWidgetSetup(
                    idx,
                    CHECKBOX_WIDGET,
                )


def make_field_reuse_last_entered_value(layers: Sequence[Any], field_name: str) -> None:
    if layers is None:
        return

    for layers_inner in layers:
        if layers_inner:
            if isinstance(layers_inner, Iterable):
                for layer in layers_inner:
                    if layer:
                        idx = layer.fields().indexFromName(field_name)

                        if idx < 0:
                            continue

                        layer_form_config = layer.editFormConfig()
                        layer_form_config.setReuseLastValue(idx, True)
                        layer.setEditFormConfig(layer_form_config)
            else:
                idx = layers_inner.fields().indexFromName(field_name)

                if idx < 0:
                    continue

                layer_form_config = layers_inner.editFormConfig()
                layer_form_config.setReuseLastValue(idx, True)
                layers_inner.setEditFormConfig(layer_form_config)


def fit_field_to_length(layers: Sequence[Any], field_name: str, length: int) -> None:
    if layers is None:
        return

    for layers_inner in layers:
        if layers_inner:
            if isinstance(layers_inner, Iterable):
                for layer in layers_inner:
                    if layer:
                        fields = layer.fields()

                        idx = fields.indexFromName(field_name)
                        if idx < 0:
                            continue

                        fields[idx].setLength(length)
            else:
                fields = layers_inner.fields()
                idx = fields.indexFromName(field_name)
                if idx < 0:
                    continue
                fields[idx].setLength(length)
