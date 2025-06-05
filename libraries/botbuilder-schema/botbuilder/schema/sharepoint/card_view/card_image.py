# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model


class CardImage(Model):
    """
    Properties for the image rendered in a card view.

    :param image_url: The URL to display as image or icon.
    :type image_url: str
    :param alt_text: The alternate text for the image.
    :type alt_text: str
    """

    _attribute_map = {
        "image_url": {"key": "imageUrl", "type": "str"},
        "alt_text": {"key": "altText", "type": "str"},
    }

    def __init__(
        self, *, alt_text: str = None, image_url: str = None, **kwargs
    ) -> None:
        super(CardImage, self).__init__(**kwargs)
        self.image_url = image_url
        self.alt_text = alt_text
