# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model

from botbuilder.schema.sharepoint.actions.card_action import (
    ExternalLinkActionParameters,
)
from botbuilder.schema.sharepoint.actions.focus_parameters import FocusParameters
from adaptivecards.adaptivecard import AdaptiveCard


class QuickViewResponse(Model):
    """
    SharePoint Quick View Response object.

    :param data: The data of the quick view.
    :type data: object
    :param template: The template of the quick view.
    :type template: AdaptiveCard
    :param view_id: The ID of the view.
    :type view_id: str
    :param title: The title of the quick view.
    :type title: str
    :param external_link: The external link of the quick view.
    :type external_link: ExternalLinkActionParameters
    :param focus_parameters: The focus parameters of the quick view.
    :type focus_parameters: FocusParameters
    :param requires_sso: The flag to determine if SSO is required.
    :type requires_sso: bool
    :param post_sso_view_id: The view ID after SSO.
    :type post_sso_view_id: str
    """

    _attribute_map = {
        "data": {"key": "data", "type": "object"},
        "template": {"key": "template", "type": "AdaptiveCard"},
        "view_id": {"key": "viewId", "type": "str"},
        "title": {"key": "title", "type": "str"},
        "external_link": {
            "key": "externalLink",
            "type": "ExternalLinkActionParameters",
        },
        "focus_parameters": {"key": "focusParameters", "type": "FocusParameters"},
        "requires_sso": {"key": "requiresSso", "type": "bool"},
        "post_sso_view_id": {"key": "postSsoViewId", "type": "str"},
    }

    def __init__(
        self,
        *,
        data: object = None,
        template: "AdaptiveCard" = None,
        view_id: str = None,
        title: str = None,
        external_link: "ExternalLinkActionParameters" = None,
        focus_parameters: "FocusParameters" = None,
        requires_sso: bool = False,
        post_sso_view_id: str = None,
        **kwargs
    ) -> None:
        super(QuickViewResponse, self).__init__(**kwargs)
        self.data = data
        self.template = template
        self.view_id = view_id
        self.title = title
        self.external_link = external_link
        self.focus_parameters = focus_parameters
        self.requires_sso = requires_sso
        self.post_sso_view_id = post_sso_view_id
