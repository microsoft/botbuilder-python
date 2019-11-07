# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import os
import urllib.parse
import urllib.request
import base64

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, CardFactory
from botbuilder.schema import ChannelAccount, HeroCard, CardAction, ActivityTypes, Attachment, AttachmentData, Activity, \
    ActionTypes
import json


class AttachmentsBot(ActivityHandler):
    async def on_members_added_activity(self, members_added: [ChannelAccount], turn_context: TurnContext):
        await self._send_welcome_message(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        if turn_context.activity.attachments and len(turn_context.activity.attachments) > 0:
            await self._handle_incoming_attachment(turn_context)
        else:
            await self._handle_outgoing_attachment(turn_context)

        await self._display_options(turn_context)

    async def _send_welcome_message(self, turn_context: TurnContext):
        for member in turn_context.activity.members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(f"Welcome to AttachmentsBot {member.name}. This bot will introduce "
                                                 f"you to Attachments. Please select an option")
                await self._display_options(turn_context)

    async def _handle_incoming_attachment(self, turn_context: TurnContext):
        for attachment in turn_context.activity.attachments:
            attachment_info = await self._download_attachment_and_write(attachment)
            await turn_context.send_activity(
                f"Attachment {attachment_info['filename']} has been received to {attachment_info['local_path']}")

    async def _download_attachment_and_write(self, attachment: Attachment) -> dict:
        url = attachment.content_url

        local_filename = os.path.join(os.getcwd(), attachment.name)

        try:
            response = urllib.request.urlopen("http://www.python.org")
            headers = response.info()
            if headers["content-type"] == "application/json":
                data = json.load(response.data)
                with open(local_filename, "w") as out_file:
                    out_file.write(data)

                return {
                    "filename": attachment.name,
                    "local_path": local_filename
                }
            else:
                return None
        except:
            return None

    async def _handle_outgoing_attachment(self, turn_context: TurnContext):
        reply = Activity(
            type=ActivityTypes.message
        )

        first_char = turn_context.activity.text[0]
        if first_char == "1":
            reply.text = "This is an inline attachment."
            reply.attachments = [self._get_inline_attachment()]
        elif first_char == "2":
            reply.text = "This is an internet attachment."
            reply.attachments = [self._get_internet_attachment()]
        elif first_char == "3":
            reply.text = "This is an uploaded attachment."
            reply.attachments = [await self._get_upload_attachment(turn_context)]
        else:
            reply.text = "Your input was not recognized, please try again."

        await turn_context.send_activity(reply)

    async def _display_options(self, turn_context: TurnContext):
        card = HeroCard(
            text="You can upload an image or select one of the following choices",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back,
                    title="1. Inline Attachment",
                    value="1"
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title="2. Internet Attachment",
                    value="2"
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title="3. Uploaded Attachment",
                    value="3"
                )
            ]
        )

        reply = MessageFactory.attachment(CardFactory.hero_card(card))
        await turn_context.send_activity(reply)

    def _get_inline_attachment(self) -> Attachment:
        file_path = os.path.join(os.getcwd(), "resources/architecture-resize.png")
        with open(file_path, "rb") as in_file:
            base64_image = base64.b64encode(in_file.read())

        return Attachment(
            name="architecture-resize.png",
            content_type="image/png",
            content_url=f"data:image/png;base64,{base64_image}"
        )

    async def _get_upload_attachment(self, turn_context: TurnContext) -> Attachment:
        with open(os.path.join(os.getcwd(), "resources/architecture-resize.png"), "rb") as in_file:
            image_data = in_file.read()

        connector = turn_context.adapter.create_connector_client(turn_context.activity.service_url)
        conversation_id = turn_context.activity.conversation.id
        response = await connector.conversations.upload_attachment(
            conversation_id,
            AttachmentData(
                name="architecture-resize.png",
                original_base64=image_data,
                thumbnail_base64=image_data,
                type="image/png"
            )
        )

        base_uri: str = connector.config.base_url
        attachment_uri = \
            base_uri \
            + ("" if base_uri.endswith("/") else "/") \
            + f"v3/attachments/${urllib.parse.urlencode(response.id)}/views/original"

        return Attachment(
            name="architecture-resize.png",
            content_type="image/png",
            content_url=attachment_uri
        )

    def _get_internet_attachment(self) -> Attachment:
        return Attachment(
            name="Resources\architecture-resize.png",
            content_type="image/png",
            content_url="https://docs.microsoft.com/en-us/bot-framework/media/how-it-works/architecture-resize.png"
        )
