# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import CardFactory, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount, ThumbnailCard, CardImage, HeroCard, Attachment, CardAction
from botbuilder.schema.teams import AppBasedLinkQuery, MessagingExtensionAttachment, MessagingExtensionQuery, MessagingExtensionResult, MessagingExtensionResponse
from botbuilder.core.teams import TeamsActivityHandler, TeamsInfo

from typing import List
import requests

class SearchBasedMessagingExtension(TeamsActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        await turn_context.send_activities(MessageFactory.text(f"Echo: {turn_context.activity.text}"))
   
    async def on_teams_messaging_extension_query(self, turn_context: TurnContext, query: MessagingExtensionQuery):
        search_query = str(query.parameters[0].value)
        response = requests.get(f"http://registry.npmjs.com/-/v1/search",params={"text":search_query})
        data = response.json()

        attachments = []
        
        for obj in data["objects"]:
            hero_card = HeroCard(
                title=obj["package"]["name"],
                tap=CardAction(
                    type="invoke",
                    value=obj["package"]
                ),
                preview=[CardImage(url=obj["package"]["links"]["npm"])]
            )

            attachment = MessagingExtensionAttachment(
                content_type=CardFactory.content_types.hero_card,
                content=HeroCard(title=obj["package"]["name"]),
                preview=CardFactory.hero_card(hero_card)
            )
            attachments.append(attachment)
        return MessagingExtensionResponse(
            compose_extension=MessagingExtensionResult(
                type="result",
                attachment_layout="list",
                attachments=attachments
            )
        )
       
       

    async def on_teams_messaging_extension_select_item(self, turn_context: TurnContext, query) -> MessagingExtensionResponse: 
        hero_card = HeroCard(
            title=query["name"],
            subtitle=query["description"],
            buttons=[
                CardAction(
                    type="openUrl",
                    value=query["links"]["npm"]
                )
            ]
        )
        attachment = MessagingExtensionAttachment(
            content_type=CardFactory.content_types.hero_card,
            content=hero_card
        )

        return MessagingExtensionResponse(
            compose_extension=MessagingExtensionResult(
                type="result",
                attachment_layout="list",
                attachments=[attachment]
            )
        )

    def _create_messaging_extension_result(self, attachments: List[MessagingExtensionAttachment]) -> MessagingExtensionResult:
        return MessagingExtensionResult(
            type="result",
            attachment_layout="list",
            attachments=attachments
        )
    
    def _create_search_result_attachment(self, search_query: str) -> MessagingExtensionAttachment:
        card_text = f"You said {search_query}"
        bf_logo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQtB3AwMUeNoq4gUBGe6Ocj8kyh3bXa9ZbV7u1fVKQoyKFHdkqU"

        button = CardAction(
            type="openUrl",
            title="Click for more Information",
            value="https://docs.microsoft.com/en-us/microsoftteams/platform/concepts/bots/bots-overview"
        )

        images = [CardImage(url=bf_logo)]
        buttons = [button]

        hero_card = HeroCard(
            title="You searched for:",
            text=card_text,
            images=images,
            buttons=buttons
        )

        return MessagingExtensionAttachment(
            content_type=CardFactory.content_types.hero_card,
            content=hero_card,
            preview=CardFactory.hero_card(hero_card)
        )
    
    def _create_dummy_search_result_attachment(self) -> MessagingExtensionAttachment:
        card_text = "https://docs.microsoft.com/en-us/microsoftteams/platform/concepts/bots/bots-overview"
        bf_logo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQtB3AwMUeNoq4gUBGe6Ocj8kyh3bXa9ZbV7u1fVKQoyKFHdkqU"

        button = CardAction(
                type = "openUrl",
                title = "Click for more Information",
                value = "https://docs.microsoft.com/en-us/microsoftteams/platform/concepts/bots/bots-overview"
            )

        images = [CardImage(url=bf_logo)]
        
        buttons = [button]
            

        hero_card = HeroCard(
            title="Learn more about Teams:", 
            text=card_text, images=images, 
            buttons=buttons
        )

        preview = HeroCard(
            title="Learn more about Teams:", 
            text=card_text, 
            images=images
        )

        return MessagingExtensionAttachment(
            content_type = CardFactory.content_types.hero_card,
            content = hero_card,
            preview = CardFactory.hero_card(preview)
        )
    
    def _create_select_items_result_attachment(self, search_query: str) -> MessagingExtensionAttachment:
        card_text = f"You said {search_query}"
        bf_logo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQtB3AwMUeNoq4gUBGe6Ocj8kyh3bXa9ZbV7u1fVKQoyKFHdkqU"

        buttons = CardAction(
            type="openUrl",
            title="Click for more Information",
            value="https://docs.microsoft.com/en-us/microsoftteams/platform/concepts/bots/bots-overview"
        )

        images = [CardImage(url=bf_logo)]
        buttons = [buttons]

        select_item_tap = CardAction(
            type="invoke",
            value={"query": search_query}
        )

        hero_card = HeroCard(
            title="You searched for:",
            text=card_text,
            images=images,
            buttons=buttons
        )

        preview = HeroCard(
            title=card_text,
            text=card_text,
            images=images,
            tap=select_item_tap
            )

        return MessagingExtensionAttachment(
            content_type=CardFactory.content_types.hero_card,
            content=hero_card,
            preview=CardFactory.hero_card(preview)
        )