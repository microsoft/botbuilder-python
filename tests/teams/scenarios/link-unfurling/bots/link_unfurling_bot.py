# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import CardFactory, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount, ThumbnailCard, CardImage, HeroCard, Attachment
from botbuilder.schema.teams import AppBasedLinkQuery, MessagingExtensionAttachment, MessagingExtensionQuery, MessagingExtensionResult, MessagingExtensionResponse
from botbuilder.core.teams import TeamsActivityHandler, TeamsInfo

class LinkUnfurlingBot(TeamsActivityHandler):
    async def on_teams_app_based_link_query(self, turn_context: TurnContext, query: AppBasedLinkQuery):
        hero_card = ThumbnailCard(
            title="Thumnnail card",
            text=query.url,
            images=[
                    CardImage(
                        url="https://raw.githubusercontent.com/microsoft/botframework-sdk/master/icon.png"
                    )
                ]
        )
        attachments = MessagingExtensionAttachment(
                                        content_type=CardFactory.content_types.hero_card,
                                        content=hero_card)
        result = MessagingExtensionResult(
            attachment_layout="list",
            type="result",
            attachments=[attachments]
        )
        return MessagingExtensionResponse(compose_extension=result)
    
    async def on_teams_messaging_extension_query(self, turn_context: TurnContext, query: MessagingExtensionQuery):
        if query.command_id == "searchQuery":
            card = HeroCard(
                title="This is a Link Unfurling Sample",
                subtitle="It will unfurl links from *.botframework.com",
                text="This sample demonstrates how to handle link unfurling in Teams. Please review the readme for more information."
            )
            attachment = Attachment(
                                content_type=CardFactory.content_types.hero_card,
                                content=card
                            )
            msg_ext_atc = MessagingExtensionAttachment(
                            content=card,
                            content_type=CardFactory.content_types.hero_card,
                            preview=attachment
                        )
            msg_ext_res = MessagingExtensionResult(
                    attachment_layout="list",
                    type="result",
                    attachments=[msg_ext_atc]
                )
            response = MessagingExtensionResponse(
                compose_extension=msg_ext_res
            )

            return response
        
        raise NotImplementedError(f"Invalid command: {query.command_id}")