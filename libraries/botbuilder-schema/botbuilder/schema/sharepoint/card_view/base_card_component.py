# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum
from msrest.serialization import Model


class CardComponentName(str, Enum):
    """
    Names of the components allowed in a card view.
    """

    Text = "Text"
    """ Text component """
    CardButton = "CardButton"
    """ Card button component """
    CardBar = "CardBar"
    """ Card bar component """
    TextInput = "TextInput"
    """ Text input component """
    SearchBox = "SearchBox"
    """ Search box component """
    SearchFooter = "SearchFooter"
    """ Search footer component """


class BaseCardComponent(Model):
    """
    Base class for all card components.

    :param id: The ID of the component.
    :type id: str
    :param component_name: The name of the component.
    :type component_name: CardComponentName
    """

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "component_name": {"key": "componentName", "type": "CardComponentName"},
    }

    def __init__(
        self, *, id: str = None, component_name: CardComponentName = None, **kwargs
    ) -> None:
        super(BaseCardComponent, self).__init__(**kwargs)
        self.id = id
        self.component_name = component_name
