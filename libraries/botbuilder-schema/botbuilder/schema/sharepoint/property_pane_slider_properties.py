# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema.sharepoint.property_pane_field_properties import (
    PropertyPaneFieldProperties,
)


class PropertyPaneSliderProperties(PropertyPaneFieldProperties):
    """
    SharePoint property pane slider properties object.

    :param label: The label of the slider.
    :type label: str
    :param value: The value of the slider.
    :type value: str
    :param aria_label: Text for screen readers to announce regardless of toggle state.
    :type aria_label: str
    :param disabled: Indicates whether the slider is disabled.
    :type disabled: bool
    :param max: The maximum value of the slider.
    :type max: int
    :param min: The minimum value of the slider.
    :type min: int
    :param show_value: Indicates whether to show the value on the right of the slider.
    :type show_value: bool
    :param step: The step amount between two adjacent values (defaults to 1).
    :type step: int
    """

    # Mapping of class attributes to their serialized keys
    _attribute_map = {
        "label": {"key": "label", "type": "str"},
        "value": {"key": "value", "type": "str"},
        "aria_label": {"key": "ariaLabel", "type": "str"},
        "disabled": {"key": "disabled", "type": "bool"},
        "max": {"key": "max", "type": "int"},
        "min": {"key": "min", "type": "int"},
        "show_value": {"key": "showValue", "type": "bool"},
        "step": {"key": "step", "type": "int"},
    }

    def __init__(
        self,
        label: str = None,
        value: str = None,
        aria_label: str = None,
        disabled: bool = False,
        max: int = None,
        min: int = None,
        show_value: bool = False,
        step: int = 1,
        **kwargs
    ) -> None:
        super(PropertyPaneSliderProperties, self).__init__(**kwargs)
        self.label = label
        self.value = value
        self.aria_label = aria_label
        self.disabled = disabled
        self.max = max
        self.min = min
        self.show_value = show_value
        self.step = step
