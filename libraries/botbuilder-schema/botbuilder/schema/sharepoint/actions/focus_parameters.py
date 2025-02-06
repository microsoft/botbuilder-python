# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum
from msrest.serialization import Model


class AriaLiveOption(str, Enum):
    """
    ARIA live region options.
    """

    Polite = "polite"
    """ Polite live region """
    Assertive = "assertive"
    """ Assertive live region """
    Off = "off"
    """ No live region """


class FocusParameters(Model):
    """
    Parameters for setting focus on an element in a client action.

    :param focus_target: The focus target of type.
    :type focus_target: str
    :param aria_live: The ARIA live region option.
    :type aria_live: AriaLiveOption
    """

    _attribute_map = {
        "focus_target": {"focusTarget": "id", "type": "str"},
        "aria_live": {"key": "ariaLive", "type": "AriaLiveOption"},
    }

    def __init__(
        self, *, focus_target: str = None, aria_live: AriaLiveOption = None, **kwargs
    ) -> None:
        super(FocusParameters, self).__init__(**kwargs)
        self.focus_target = focus_target
        self.aria_live = aria_live
