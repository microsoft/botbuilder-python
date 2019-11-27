# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class O365ConnectorCardSection(Model):
    """O365 connector card section.

    :param title: Title of the section
    :type title: str
    :param text: Text for the section
    :type text: str
    :param activity_title: Activity title
    :type activity_title: str
    :param activity_subtitle: Activity subtitle
    :type activity_subtitle: str
    :param activity_text: Activity text
    :type activity_text: str
    :param activity_image: Activity image
    :type activity_image: str
    :param activity_image_type: Describes how Activity image is rendered.
     Possible values include: 'avatar', 'article'
    :type activity_image_type: str or
     ~botframework.connector.teams.models.enum
    :param markdown: Use markdown for all text contents. Default value is
     true.
    :type markdown: bool
    :param facts: Set of facts for the current section
    :type facts:
     list[~botframework.connector.teams.models.O365ConnectorCardFact]
    :param images: Set of images for the current section
    :type images:
     list[~botframework.connector.teams.models.O365ConnectorCardImage]
    :param potential_action: Set of actions for the current section
    :type potential_action:
     list[~botframework.connector.teams.models.O365ConnectorCardActionBase]
    """

    _attribute_map = {
        "title": {"key": "title", "type": "str"},
        "text": {"key": "text", "type": "str"},
        "activity_title": {"key": "activityTitle", "type": "str"},
        "activity_subtitle": {"key": "activitySubtitle", "type": "str"},
        "activity_text": {"key": "activityText", "type": "str"},
        "activity_image": {"key": "activityImage", "type": "str"},
        "activity_image_type": {"key": "activityImageType", "type": "str"},
        "markdown": {"key": "markdown", "type": "bool"},
        "facts": {"key": "facts", "type": "[O365ConnectorCardFact]"},
        "images": {"key": "images", "type": "[O365ConnectorCardImage]"},
        "potential_action": {
            "key": "potentialAction",
            "type": "[O365ConnectorCardActionBase]",
        },
    }

    def __init__(self, **kwargs):
        super(O365ConnectorCardSection, self).__init__(**kwargs)
        self.title = kwargs.get("title", None)
        self.text = kwargs.get("text", None)
        self.activity_title = kwargs.get("activity_title", None)
        self.activity_subtitle = kwargs.get("activity_subtitle", None)
        self.activity_text = kwargs.get("activity_text", None)
        self.activity_image = kwargs.get("activity_image", None)
        self.activity_image_type = kwargs.get("activity_image_type", None)
        self.markdown = kwargs.get("markdown", None)
        self.facts = kwargs.get("facts", None)
        self.images = kwargs.get("images", None)
        self.potential_action = kwargs.get("potential_action", None)
