# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from msrest.serialization import Model

from botbuilder.schema.sharepoint.property_pane_page import PropertyPanePage


class GetPropertyPaneConfigurationResponse(Model):
    """
    SharePoint ACE get property pane configuration response.

    :param pages: The pages of the property pane configuration.
    :type pages: list[PropertyPanePage]
    """

    _attribute_map = {
        "pages": {"key": "pages", "type": "[PropertyPanePage]"},
        "current_page": {"key": "currentPage", "type": "int"},
        "loading_indicator_delay_time": {
            "key": "loadingIndicatorDelayTime",
            "type": "int",
        },
        "show_loading_indicator": {"key": "showLoadingIndicator", "type": "bool"},
    }

    def __init__(
        self,
        *,
        pages: List[PropertyPanePage] = None,
        current_page: int = None,
        loading_indicator_delay_time: int = None,
        show_loading_indicator: bool = None,
        **kwargs
    ) -> None:
        super(GetPropertyPaneConfigurationResponse, self).__init__(**kwargs)
        self.pages = pages if pages is not None else []
        self.current_page = current_page
        self.loading_indicator_delay_time = loading_indicator_delay_time
        self.show_loading_indicator = show_loading_indicator
