# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum
from msrest.serialization import Model

from botbuilder.schema.sharepoint import CardViewResponse, QuickViewResponse


class ViewResponseType(str, Enum):
    """
    Adaptive Card Extension View response type.
    """

    Card = "Card"
    """ Render card view """

    QuickView = "QuickView"
    """ Render quick view """

    NoOp = "NoOp"
    """ No operation """


class BaseHandleActionResponse(Model):
    """
    Response returned when handling a client-side action on an Adaptive Card Extension.

    :param response_type: The type of view response.
    :type response_type: ViewResponseType
    :param render_arguments: Arguments to render the view.
    :type render_arguments: object
    """

    _attribute_map = {
        "response_type": {"key": "responseType", "type": "ViewResponseType"},
        "render_arguments": {"key": "renderArguments", "type": "object"},
    }

    def __init__(
        self,
        *,
        response_type: ViewResponseType = None,
        render_arguments: object = None,
        **kwargs
    ) -> None:
        super(BaseHandleActionResponse, self).__init__(**kwargs)
        self.response_type = response_type
        self.render_arguments = render_arguments


class CardViewHandleActionResponse(BaseHandleActionResponse):
    """
    Adaptive Card Extension Client-side action response to render card view..

    :param render_arguments: Arguments to render the view.
    :type render_arguments: CardViewResponse
    """

    _attribute_map = {
        "render_arguments": {"key": "renderArguments", "type": "CardViewResponse"},
    }

    def __init__(self, *, render_arguments: CardViewResponse = None, **kwargs) -> None:
        super(CardViewHandleActionResponse, self).__init__(
            response_type=ViewResponseType.Card, **kwargs
        )
        self.render_arguments = render_arguments


class QuickViewHandleActionResponse(BaseHandleActionResponse):
    """
    Adaptive Card Extension Client-side action response to render quick view.

    :param response_type: The type of view response.
    :type type: ViewResponseType
    :param render_arguments: Arguments to render the view.
    :type render_arguments: QuickViewResponse
    """

    _attribute_map = {
        "render_arguments": {"key": "renderArguments", "type": "QuickViewResponse"},
    }

    def __init__(self, *, render_arguments: QuickViewResponse = None, **kwargs) -> None:
        super(QuickViewHandleActionResponse, self).__init__(
            response_type=ViewResponseType.QuickView, **kwargs
        )
        self.render_arguments = render_arguments


class NoOpHandleActionResponse(BaseHandleActionResponse):
    """
    The handle action response for no op.

    :param response_type: The type of view response.
    :type response_type: ViewResponseType
    :param render_arguments: Arguments to render the view.
    :type render_arguments: object
    """

    _attribute_map = {}

    def __init__(self, **kwargs) -> None:
        super(NoOpHandleActionResponse, self).__init__(
            response_type=ViewResponseType.NoOp, **kwargs
        )
        self.render_arguments = None
