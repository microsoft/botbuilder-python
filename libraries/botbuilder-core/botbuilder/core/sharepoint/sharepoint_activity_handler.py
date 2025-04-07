# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# pylint: disable=too-many-lines

from http import HTTPStatus
from botbuilder.core import ActivityHandler, InvokeResponse
from botbuilder.core.activity_handler import _InvokeResponseException
from botbuilder.core.turn_context import TurnContext
from botbuilder.schema.sharepoint import (
    AceRequest,
    BaseHandleActionResponse,
    CardViewResponse,
    GetPropertyPaneConfigurationResponse,
    QuickViewHandleActionResponse,
    QuickViewResponse,
)
from ..serializer_helper import deserializer_helper


class SharePointActivityHandler(ActivityHandler):
    """
    The SharePointActivityHandler is derived from ActivityHandler. It adds support for
    SharePoint-specific events and interactions.
    """

    async def on_invoke_activity(self, turn_context: TurnContext) -> InvokeResponse:
        """
        Invoked when an invoke activity is received from the connector.
        Invoke activities can be used to communicate many different things.

        :param turn_context: A context object for this turn.

        :returns: An InvokeResponse that represents the work queued to execute.

        .. remarks::
            Invoke activities communicate programmatic commands from a client or channel to a bot.
            The meaning of an invoke activity is defined by the "invoke_activity.name" property,
            which is meaningful within the scope of a channel.
        """
        try:
            if not turn_context.activity.name:
                raise NotImplementedError()

            if turn_context.activity.name == "cardExtension/getCardView":
                return self._create_invoke_response(
                    await self.on_sharepoint_task_get_card_view(
                        turn_context,
                        deserializer_helper(AceRequest, turn_context.activity.value),
                    )
                )

            if turn_context.activity.name == "cardExtension/getQuickView":
                return self._create_invoke_response(
                    await self.on_sharepoint_task_get_quick_view(
                        turn_context,
                        deserializer_helper(AceRequest, turn_context.activity.value),
                    )
                )

            if (
                turn_context.activity.name
                == "cardExtension/getPropertyPaneConfiguration"
            ):
                return self._create_invoke_response(
                    await self.on_sharepoint_task_get_property_pane_configuration(
                        turn_context,
                        deserializer_helper(AceRequest, turn_context.activity.value),
                    )
                )

            if (
                turn_context.activity.name
                == "cardExtension/setPropertyPaneConfiguration"
            ):
                ace_request = deserializer_helper(
                    AceRequest, turn_context.activity.value
                )
                set_prop_pane_config_response = (
                    await self.on_sharepoint_task_set_property_pane_configuration(
                        turn_context, ace_request
                    )
                )
                self.validate_set_property_pane_configuration_response(
                    set_prop_pane_config_response
                )
                return self._create_invoke_response(set_prop_pane_config_response)

            if turn_context.activity.name == "cardExtension/handleAction":
                return self._create_invoke_response(
                    await self.on_sharepoint_task_handle_action(
                        turn_context,
                        deserializer_helper(AceRequest, turn_context.activity.value),
                    )
                )

            if turn_context.activity.name == "cardExtension/token":
                await self.on_sign_in_invoke(turn_context)
                return self._create_invoke_response()

        except _InvokeResponseException as invoke_exception:
            return invoke_exception.create_invoke_response()
        return await super().on_invoke_activity(turn_context)

    async def on_sharepoint_task_get_card_view(
        self, turn_context: TurnContext, ace_request: AceRequest
    ) -> CardViewResponse:
        """
        Override this in a derived class to provide logic for when a card view is fetched.

        :param turn_context: A context object for this turn.
        :param ace_request: The ACE invoke request value payload.
        :returns: A Card View Response for the request.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_sharepoint_task_get_quick_view(
        self, turn_context: TurnContext, ace_request: AceRequest
    ) -> QuickViewResponse:
        """
        Override this in a derived class to provide logic for when a quick view is fetched.

        :param turn_context: A strongly-typed context object for this turn.
        :param ace_request: The ACE invoke request value payload.
        :returns: A Quick View Response for the request
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_sharepoint_task_get_property_pane_configuration(
        self, turn_context: TurnContext, ace_request: AceRequest
    ) -> GetPropertyPaneConfigurationResponse:
        """
        Override this in a derived class to provide logic for getting configuration pane properties.

        :param turn_context: A strongly-typed context object for this turn.
        :param ace_request: The ACE invoke request value payload.
        :returns: A Property Pane Configuration Response for the request.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_sharepoint_task_set_property_pane_configuration(
        self, turn_context: TurnContext, ace_request: AceRequest
    ) -> BaseHandleActionResponse:
        """
        Override this in a derived class to provide logic for setting configuration pane properties.

        :param turn_context: A strongly-typed context object for this turn.
        :param ace_request: The ACE invoke request value payload.
        :returns: Card view or no-op action response.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_sharepoint_task_handle_action(
        self, turn_context: TurnContext, ace_request: AceRequest
    ) -> BaseHandleActionResponse:
        """
        Override this in a derived class to provide logic for handling ACE actions.

        :param turn_context: A strongly-typed context object for this turn.
        :param ace_request: The ACE invoke request value payload.
        :returns: A handle action response..
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    def validate_set_property_pane_configuration_response(
        self, response: BaseHandleActionResponse
    ):
        """
        Validates the response for SetPropertyPaneConfiguration action.

        :param response: The response object.
        :raises ValueError: If response is of type QuickViewHandleActionResponse.
        """
        if isinstance(response, QuickViewHandleActionResponse):
            raise _InvokeResponseException(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                "Response for SetPropertyPaneConfiguration action can't be of QuickView type.",
            )
