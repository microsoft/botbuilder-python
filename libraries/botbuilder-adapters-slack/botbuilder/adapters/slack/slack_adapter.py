# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC
from typing import List, Callable, Awaitable

from aiohttp.web_request import Request
from aiohttp.web_response import Response
from botframework.connector.auth import ClaimsIdentity
from botbuilder.core import conversation_reference_extension
from botbuilder.core import BotAdapter, TurnContext
from botbuilder.schema import (
    Activity,
    ResourceResponse,
    ActivityTypes,
    ConversationAccount,
    ConversationReference,
)

from .activity_resourceresponse import ActivityResourceResponse
from .slack_client import SlackClient
from .slack_helper import SlackHelper
from .slack_adatper_options import SlackAdapterOptions


class SlackAdapter(BotAdapter, ABC):
    """
    BotAdapter that can handle incoming Slack events. Incoming Slack events are deserialized to an Activity that is
     dispatched through the middleware and bot pipeline.
    """

    def __init__(
        self,
        client: SlackClient,
        on_turn_error: Callable[[TurnContext, Exception], Awaitable] = None,
        options: SlackAdapterOptions = None,
    ):
        super().__init__(on_turn_error)
        self.slack_client = client
        self.slack_logged_in = False
        self.options = options if options else SlackAdapterOptions()

    async def send_activities(
        self, context: TurnContext, activities: List[Activity]
    ) -> List[ResourceResponse]:
        """
        Send a message from the bot to the messaging API.

        :param context: A TurnContext representing the current incoming message and environment.
        :type context: :class:`botbuilder.core.TurnContext`
        :param activities: An array of outgoing activities to be sent back to the messaging API.
        :type activities: :class:`typing.List[Activity]`
        :return: An array of ResourceResponse objects containing the IDs that Slack assigned to the sent messages.
        :rtype: :class:`typing.List[ResourceResponse]`
        """

        if not context:
            raise Exception("TurnContext is required")
        if not activities:
            raise Exception("List[Activity] is required")

        responses = []

        for activity in activities:
            if activity.type == ActivityTypes.message:
                message = SlackHelper.activity_to_slack(activity)

                slack_response = await self.slack_client.post_message(message)

                if slack_response and slack_response.status_code / 100 == 2:
                    resource_response = ActivityResourceResponse(
                        id=slack_response.data["ts"],
                        activity_id=slack_response.data["ts"],
                        conversation=ConversationAccount(
                            id=slack_response.data["channel"]
                        ),
                    )

                    responses.append(resource_response)

        return responses

    async def update_activity(self, context: TurnContext, activity: Activity):
        """
        Update a previous message with new content.

        :param context: A TurnContext representing the current incoming message and environment.
        :type context: :class:`botbuilder.core.TurnContext`
        :param activity: The updated activity in the form '{id: `id of activity to update`, ...}'.
        :type activity: :class:`botbuilder.schema.Activity`
        :return: A resource response with the ID of the updated activity.
        :rtype: :class:`botbuilder.schema.ResourceResponse`
        """

        if not context:
            raise Exception("TurnContext is required")
        if not activity:
            raise Exception("Activity is required")
        if not activity.id:
            raise Exception("Activity.id is required")
        if not activity.conversation:
            raise Exception("Activity.conversation is required")

        message = SlackHelper.activity_to_slack(activity)
        results = await self.slack_client.chat_update(
            ts=message.ts,
            channel=message.channel,
            text=message.text,
        )

        if results.status_code / 100 != 2:
            raise Exception(f"Error updating activity on slack: {results}")

        return ResourceResponse(id=activity.id)

    async def delete_activity(
        self, context: TurnContext, reference: ConversationReference
    ):
        """
        Delete a previous message.

        :param context: A TurnContext representing the current incoming message and environment.
        :type context: :class:`botbuilder.core.TurnContext`
        :param reference: An object in the form "{activityId: `id of message to delete`,conversation: { id: `id of Slack
         channel`}}".
        :type reference: :class:`botbuilder.schema.ConversationReference`
        """

        if not context:
            raise Exception("TurnContext is required")
        if not reference:
            raise Exception("ConversationReference is required")
        if not reference.channel_id:
            raise Exception("ConversationReference.channel_id is required")
        if not context.activity.timestamp:
            raise Exception("Activity.timestamp is required")

        await self.slack_client.chat_delete(
            channel=reference.conversation.id, ts=reference.activity_id
        )

    async def continue_conversation(
        self,
        reference: ConversationReference,
        callback: Callable,
        bot_id: str = None,  # pylint: disable=unused-argument
        claims_identity: ClaimsIdentity = None,
        audience: str = None,  # pylint: disable=unused-argument
    ):
        """
        Send a proactive message to a conversation.

        .. remarks::

            Most channels require a user to initiate a conversation with a bot before the bot can send activities to the
             user.

        :param reference: A reference to the conversation to continue.
        :type reference: :class:`botbuilder.schema.ConversationReference`
        :param callback: The method to call for the resulting bot turn.
        :type callback: :class:`typing.Callable`
        :param bot_id: Unused for this override.
        :type bot_id: str
        :param claims_identity: A ClaimsIdentity for the conversation.
        :type claims_identity: :class:`botframework.connector.auth.ClaimsIdentity`
        :param audience: Unused for this override.
        :type audience: str
        """

        if not reference:
            raise Exception("ConversationReference is required")
        if not callback:
            raise Exception("callback is required")

        if claims_identity:
            request = conversation_reference_extension.get_continuation_activity(
                reference
            )
            context = TurnContext(self, request)
            context.turn_state[BotAdapter.BOT_IDENTITY_KEY] = claims_identity
            context.turn_state[BotAdapter.BOT_CALLBACK_HANDLER_KEY] = callback
        else:
            request = TurnContext.apply_conversation_reference(
                conversation_reference_extension.get_continuation_activity(reference),
                reference,
            )
            context = TurnContext(self, request)

        return await self.run_pipeline(context, callback)

    async def process(self, req: Request, logic: Callable) -> Response:
        """
        Accept an incoming webhook request and convert it into a TurnContext which can be processed by the bot's logic.

        :param req: The aiohttp Request object.
        :type req: :class:`aiohttp.web_request.Request`
        :param logic: The method to call for the resulting bot turn.
        :type logic: :class:`tying.Callable`
        :return: The aiohttp Response.
        :rtype: :class:`aiohttp.web_response.Response`
        """

        if not req:
            raise Exception("Request is required")

        if not self.slack_logged_in:
            await self.slack_client.login_with_slack()
            self.slack_logged_in = True

        body = await req.text()

        if (
            self.options.verify_incoming_requests
            and not self.slack_client.verify_signature(req, body)
        ):
            return SlackHelper.response(
                req, 401, "Rejected due to mismatched header signature"
            )

        slack_body = SlackHelper.deserialize_body(req.content_type, body)

        if slack_body.type == "url_verification":
            return SlackHelper.response(req, 200, slack_body.challenge)

        if (
            not self.slack_client.options.slack_verification_token
            and slack_body.token != self.slack_client.options.slack_verification_token
        ):
            text = f"Rejected due to mismatched verificationToken:{body}"
            return SlackHelper.response(req, 403, text)

        if slack_body.payload:
            # handle interactive_message callbacks and block_actions
            activity = SlackHelper.payload_to_activity(slack_body.payload)
        elif slack_body.type == "event_callback":
            activity = await SlackHelper.event_to_activity(
                slack_body.event, self.slack_client
            )
        elif slack_body.command:
            activity = await SlackHelper.command_to_activity(
                slack_body, self.slack_client
            )
        else:
            return SlackHelper.response(
                req, 200, f"Unknown Slack event type {slack_body.type}"
            )

        context = TurnContext(self, activity)
        await self.run_pipeline(context, logic)

        return SlackHelper.response(req, 200)
