# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import urllib.parse

from aiohttp.web_request import Request
from aiohttp.web_response import Response

from slack.web.classes.attachments import Attachment

from botbuilder.schema import (
    Activity,
    ConversationAccount,
    ChannelAccount,
    ActivityTypes,
)

from .slack_message import SlackMessage
from .slack_client import SlackClient
from .slack_event import SlackEvent
from .slack_payload import SlackPayload
from .slack_request_body import SlackRequestBody


class SlackHelper:
    @staticmethod
    def activity_to_slack(activity: Activity) -> SlackMessage:
        """
        Formats a BotBuilder Activity into an outgoing Slack message.

        :param activity: A BotBuilder Activity object.
        :type activity: :class:`botbuilder.schema.Activity`
        :return: A Slack message object with {text, attachments, channel, thread ts} and any fields found in
         activity.channelData.
        :rtype: :class:`SlackMessage`
        """

        if not activity:
            raise Exception("Activity required")

        # use ChannelData if available
        if activity.channel_data:
            message = activity.channel_data
        else:
            message = SlackMessage(
                ts=activity.timestamp,
                text=activity.text,
                channel=activity.conversation.id,
            )

            if activity.attachments:
                attachments = []
                for att in activity.attachments:
                    if att.name == "blocks":
                        message.blocks = att.content
                    else:
                        new_attachment = Attachment(
                            author_name=att.name,
                            thumb_url=att.thumbnail_url,
                            text="",
                        )
                        attachments.append(new_attachment)

                if attachments:
                    message.attachments = attachments

            if (
                activity.conversation.properties
                and "thread_ts" in activity.conversation.properties
            ):
                message.thread_ts = activity.conversation.properties["thread_ts"]

        if message.ephemeral:
            message.user = activity.recipient.id

        if (
            message.icon_url
            or not (message.icons and message.icons.status_emoji)
            or not message.username
        ):
            message.as_user = False

        return message

    @staticmethod
    def response(  # pylint: disable=unused-argument
        req: Request, code: int, text: str = None, encoding: str = None
    ) -> Response:
        """
        Formats an aiohttp Response.

        :param req: The original aiohttp Request.
        :type req: :class:`aiohttp.web_request.Request`
        :param code: The HTTP result code to return.
        :type code: int
        :param text: The text to return.
        :type text: str
        :param encoding: The text encoding. Defaults to UTF-8.
        :type encoding: str
        :return: The aoihttp Response
        :rtype: :class:`aiohttp.web_response.Response`
        """

        response = Response(status=code)

        if text:
            response.content_type = "text/plain"
            response.body = text.encode(encoding=encoding if encoding else "utf-8")

        return response

    @staticmethod
    def payload_to_activity(payload: SlackPayload) -> Activity:
        """
        Creates an activity based on the Slack event payload.

        :param payload: The payload of the Slack event.
        :type payload: :class:`SlackPayload`
        :return: An activity containing the event data.
        :rtype: :class:`botbuilder.schema.Activity`
        """

        if not payload:
            raise Exception("payload is required")

        activity = Activity(
            channel_id="slack",
            conversation=ConversationAccount(id=payload.channel["id"], properties={}),
            from_property=ChannelAccount(
                id=(
                    payload.message.bot_id
                    if payload.message.bot_id
                    else payload.user["id"]
                )
            ),
            recipient=ChannelAccount(),
            channel_data=payload,
            text=None,
            type=ActivityTypes.event,
            value=payload,
        )

        if payload.thread_ts:
            activity.conversation.properties["thread_ts"] = payload.thread_ts

        if payload.actions:
            action = payload.actions[0]

            if action["type"] == "button":
                activity.text = action["value"]
            elif action["type"] == "select":
                selected_option = action["selected_options"]
                activity.text = selected_option["value"] if selected_option else None
            elif action["type"] == "static_select":
                activity.text = action["selected_options"]["value"]

            if activity.text:
                activity.type = ActivityTypes.message

        return activity

    @staticmethod
    async def event_to_activity(event: SlackEvent, client: SlackClient) -> Activity:
        """
        Creates an activity based on the Slack event data.

        :param event: The data of the Slack event.
        :type event: :class:`SlackEvent`
        :param client: The Slack client.
        :type client: :class:`SlackClient`
        :return: An activity containing the event data.
        :rtype: :class:`botbuilder.schema.Activity`
        """

        if not event:
            raise Exception("slack event is required")

        activity = Activity(
            id=event.event_ts,
            channel_id="slack",
            conversation=ConversationAccount(
                id=event.channel if event.channel else event.channel_id, properties={}
            ),
            from_property=ChannelAccount(
                id=event.bot_id if event.bot_id else event.user_id
            ),
            recipient=ChannelAccount(id=None),
            channel_data=event,
            text=event.text,
            type=ActivityTypes.event,
        )

        if not activity.conversation.id:
            if event.item and event.item_channel:
                activity.conversation.id = event.item_channel
            else:
                activity.conversation.id = event.team

        activity.recipient.id = await client.get_bot_user_identity(activity=activity)

        if event.thread_ts:
            activity.conversation.properties["thread_ts"] = event.thread_ts

        if event.type == "message" and not event.subtype and not event.bot_id:
            if not event.subtype:
                activity.type = ActivityTypes.message
                activity.text = event.text

            activity.conversation.properties["channel_type"] = event.channel_type
            activity.value = event
        else:
            activity.name = event.type
            activity.value = event

        return activity

    @staticmethod
    async def command_to_activity(
        body: SlackRequestBody, client: SlackClient
    ) -> Activity:
        """
        Creates an activity based on a Slack event related to a slash command.

        :param body: The data of the Slack event.
        :type body: :class:`SlackRequestBody`
        :param client: The Slack client.
        :type client: :class:`SlackClient`
        :return: An activity containing the event data.
        :rtype: :class:`botbuilder.schema.Activity`
        """

        if not body:
            raise Exception("body is required")

        activity = Activity(
            id=body.trigger_id,
            channel_id="slack",
            conversation=ConversationAccount(id=body.channel_id, properties={}),
            from_property=ChannelAccount(id=body.user_id),
            recipient=ChannelAccount(id=None),
            channel_data=body,
            text=body.text,
            type=ActivityTypes.event,
            name="Command",
            value=body.command,
        )

        activity.recipient.id = await client.get_bot_user_identity(activity)
        activity.conversation.properties["team"] = body.team_id

        return activity

    @staticmethod
    def query_string_to_dictionary(query: str) -> {}:
        """
        Converts a query string to a dictionary with key-value pairs.

        :param query: The query string to convert.
        :type query: str
        :return: A dictionary with the query values.
        :rtype: :class:`typing.Dict`
        """

        values = {}

        if not query:
            return values

        pairs = query.replace("+", "%20").split("&")

        for pair in pairs:
            key_value = pair.split("=")
            key = key_value[0]
            value = urllib.parse.unquote(key_value[1])

            values[key] = value

        return values

    @staticmethod
    def deserialize_body(content_type: str, request_body: str) -> SlackRequestBody:
        """
        Deserializes the request's body as a SlackRequestBody object.

        :param content_type: The content type of the body.
        :type content_type: str
        :param request_body: The body of the request.
        :type request_body: str
        :return: A SlackRequestBody object.
        :rtype: :class:`SlackRequestBody`
        """

        if not request_body:
            return None

        if content_type == "application/x-www-form-urlencoded":
            request_dict = SlackHelper.query_string_to_dictionary(request_body)
        elif content_type == "application/json":
            request_dict = json.loads(request_body)
        else:
            raise Exception("Unknown request content type")

        if "command=%2F" in request_body:
            return SlackRequestBody(**request_dict)

        if "payload=" in request_body:
            payload = SlackPayload(**request_dict)
            return SlackRequestBody(payload=payload, token=payload.token)

        return SlackRequestBody(**request_dict)
