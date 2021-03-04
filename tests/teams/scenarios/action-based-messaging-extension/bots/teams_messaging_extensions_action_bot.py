# Copyright (c) Microsoft Corp. All rights reserved.
# Licensed under the MIT License.

from typing import List
import random
from botbuilder.core import (
    CardFactory,
    MessageFactory,
    TurnContext,
    UserState,
    ConversationState,
    PrivateConversationState,
)
from botbuilder.schema import ChannelAccount, HeroCard, CardAction, CardImage
from botbuilder.schema.teams import (
    MessagingExtensionAction,
    MessagingExtensionActionResponse,
    MessagingExtensionAttachment,
    MessagingExtensionResult,
)
from botbuilder.core.teams import TeamsActivityHandler, TeamsInfo
from botbuilder.azure import CosmosDbPartitionedStorage


class TeamsMessagingExtensionsActionBot(TeamsActivityHandler):
    async def on_teams_messaging_extension_submit_action_dispatch(
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ) -> MessagingExtensionActionResponse:
        if action.command_id == "createCard":
            return await self.create_card_command(turn_context, action)
        elif action.command_id == "shareMessage":
            return await self.share_message_command(turn_context, action)

    async def create_card_command(
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ) -> MessagingExtensionActionResponse:
        title = action.data["title"]
        subTitle = action.data["subTitle"]
        text = action.data["text"]

        card = HeroCard(title=title, subtitle=subTitle, text=text)
        cardAttachment = CardFactory.hero_card(card)
        attachment = MessagingExtensionAttachment(
            content=card,
            content_type=CardFactory.content_types.hero_card,
            preview=cardAttachment,
        )
        attachments = [attachment]

        extension_result = MessagingExtensionResult(
            attachment_layout="list", type="result", attachments=attachments
        )
        return MessagingExtensionActionResponse(compose_extension=extension_result)

    async def share_message_command(
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ) -> MessagingExtensionActionResponse:
        # The user has chosen to share a message by choosing the 'Share Message' context menu command.

        # TODO: .user is None
        title = "Shared Message"  # f'{action.message_payload.from_property.user.display_name} orignally sent this message:'
        text = action.message_payload.body.content
        card = HeroCard(title=title, text=text)

        if not action.message_payload.attachments is None:
            # This sample does not add the MessagePayload Attachments.  This is left as an
            #  exercise for the user.
            card.subtitle = (
                f"({len(action.message_payload.attachments)} Attachments not included)"
            )

        # This Messaging Extension example allows the user to check a box to include an image with the
        # shared message.  This demonstrates sending custom parameters along with the message payload.
        include_image = action.data["includeImage"]
        if include_image == "true":
            image = CardImage(
                url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQtB3AwMUeNoq4gUBGe6Ocj8kyh3bXa9ZbV7u1fVKQoyKFHdkqU"
            )
            card.images = [image]

        cardAttachment = CardFactory.hero_card(card)
        attachment = MessagingExtensionAttachment(
            content=card,
            content_type=CardFactory.content_types.hero_card,
            preview=cardAttachment,
        )
        attachments = [attachment]

        extension_result = MessagingExtensionResult(
            attachment_layout="list", type="result", attachments=attachments
        )
        return MessagingExtensionActionResponse(compose_extension=extension_result)
