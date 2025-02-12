# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema.sharepoint.property_pane_field_properties import (
    PropertyPaneFieldProperties,
)


class PropertyPaneTextFieldProperties(PropertyPaneFieldProperties):
    """
    SharePoint property pane text field properties.

        :param label: The label of the text field.
        :type label: str
        :param value: The value of the text field.
        :type value: str
        :param aria_label: Text for screen readers to announce regardless of toggle state.
        :type aria_label: str
        :param description: The description of the text field.
        :type description: str
        :param disabled: Indicates whether the text field is disabled.
        :type disabled: bool
        :param error_message: The error message for the text field.
        :type error_message: str
        :param log_name: The name used for logging value changes.
        :type log_name: str
        :param max_length: The maximum number of characters allowed in the text field.
        :type max_length: int
        :param multiline: Indicates whether the text field is multiline.
        :type multiline: bool
        :param placeholder: The placeholder text displayed in the text field.
        :type placeholder: str
        :param resizable: Indicates whether the multiline text field is resizable.
        :type resizable: bool
        :param rows: The number of rows for a multiline text field.
        :type rows: int
        :param underlined: Indicates whether the text field is underlined.
        :type underlined: bool
    """

    _attribute_map = {
        "label": {"key": "label", "type": "str"},
        "value": {"key": "value", "type": "str"},
        "aria_label": {"key": "ariaLabel", "type": "str"},
        "description": {"key": "description", "type": "str"},
        "disabled": {"key": "disabled", "type": "bool"},
        "error_message": {"key": "errorMessage", "type": "str"},
        "log_name": {"key": "logName", "type": "str"},
        "max_length": {"key": "maxLength", "type": "int"},
        "multiline": {"key": "multiline", "type": "bool"},
        "placeholder": {"key": "placeholder", "type": "str"},
        "resizable": {"key": "resizable", "type": "bool"},
        "rows": {"key": "rows", "type": "int"},
        "underlined": {"key": "underlined", "type": "bool"},
    }

    def __init__(
        self,
        *,
        label: str = None,
        value: str = None,
        aria_label: str = None,
        description: str = None,
        disabled: bool = False,
        error_message: str = None,
        log_name: str = None,
        max_length: int = None,
        multiline: bool = False,
        placeholder: str = None,
        resizable: bool = False,
        rows: int = None,
        underlined: bool = False,
        **kwargs
    ) -> None:
        super(PropertyPaneTextFieldProperties, self).__init__(**kwargs)
        self.label = label
        self.value = value
        self.aria_label = aria_label
        self.description = description
        self.disabled = disabled
        self.error_message = error_message
        self.log_name = log_name
        self.max_length = max_length
        self.multiline = multiline
        self.placeholder = placeholder
        self.resizable = resizable
        self.rows = rows
        self.underlined = underlined
