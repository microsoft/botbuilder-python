# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import uuid4

from botbuilder.core import Bot, BotAdapter, ChannelServiceHandler, TurnContext
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ConversationReference,
    ResourceResponse,
)
from botframework.connector.auth import (
    AuthenticationConfiguration,
    ChannelProvider,
    ClaimsIdentity,
    CredentialProvider,
)

from .skill_conversation_id_factory import SkillConversationIdFactory


class SkillHandler(ChannelServiceHandler):

    SKILL_CONVERSATION_REFERENCE_KEY = (
        "botbuilder.core.skills.SkillConversationReference"
    )

    def __init__(
        self,
        adapter: BotAdapter,
        bot: Bot,
        conversation_id_factory: SkillConversationIdFactory,
        credential_provider: CredentialProvider,
        auth_configuration: AuthenticationConfiguration,
        channel_provider: ChannelProvider = None,
        logger: object = None,
    ):
        super().__init__(credential_provider, auth_configuration, channel_provider)

        if not adapter:
            raise TypeError("adapter can't be None")
        if not bot:
            raise TypeError("bot can't be None")
        if not conversation_id_factory:
            raise TypeError("conversation_id_factory can't be None")

        self._adapter = adapter
        self._bot = bot
        self._conversation_id_factory = conversation_id_factory
        self._logger = logger

    async def on_send_to_conversation(
        self, claims_identity: ClaimsIdentity, conversation_id: str, activity: Activity,
    ) -> ResourceResponse:
        """
        send_to_conversation() API for Skill

        This method allows you to send an activity to the end of a conversation.

        This is slightly different from ReplyToActivity().
        * SendToConversation(conversationId) - will append the activity to the end
        of the conversation according to the timestamp or semantics of the channel.
        * ReplyToActivity(conversationId,ActivityId) - adds the activity as a reply
        to another activity, if the channel supports it. If the channel does not
        support nested replies, ReplyToActivity falls back to SendToConversation.

        Use ReplyToActivity when replying to a specific activity in the
        conversation.

        Use SendToConversation in all other cases.
        :param claims_identity:
        :param conversation_id:
        :param activity:
        :return:
        """
        return await self._process_activity(
            claims_identity, conversation_id, None, activity,
        )

    async def on_reply_to_activity(
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        activity_id: str,
        activity: Activity,
    ) -> ResourceResponse:
        """
        reply_to_activity() API for Skill.

        This method allows you to reply to an activity.

        This is slightly different from SendToConversation().
        * SendToConversation(conversationId) - will append the activity to the end
        of the conversation according to the timestamp or semantics of the channel.
        * ReplyToActivity(conversationId,ActivityId) - adds the activity as a reply
        to another activity, if the channel supports it. If the channel does not
        support nested replies, ReplyToActivity falls back to SendToConversation.

        Use ReplyToActivity when replying to a specific activity in the
        conversation.

        Use SendToConversation in all other cases.
        :param claims_identity:
        :param conversation_id:
        :param activity_id:
        :param activity:
        :return:
        """
        return await self._process_activity(
            claims_identity, conversation_id, activity_id, activity,
        )

    async def _process_activity(
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        reply_to_activity_id: str,
        activity: Activity,
    ) -> ResourceResponse:
        conversation_reference = await self._conversation_id_factory.get_conversation_reference(
            conversation_id
        )

        if not conversation_reference:
            raise KeyError("ConversationReference not found")

        skill_conversation_reference = ConversationReference(
            activity_id=activity.id,
            user=activity.from_property,
            bot=activity.recipient,
            conversation=activity.conversation,
            channel_id=activity.channel_id,
            service_url=activity.service_url,
        )

        async def callback(context: TurnContext):
            context.turn_state[
                SkillHandler.SKILL_CONVERSATION_REFERENCE_KEY
            ] = skill_conversation_reference
            TurnContext.apply_conversation_reference(activity, conversation_reference)
            context.activity.id = reply_to_activity_id

            if activity.type == ActivityTypes.end_of_conversation:
                await self._conversation_id_factory.delete_conversation_reference(
                    conversation_id
                )
                self._apply_eoc_to_turn_context_activity(context, activity)
                await self._bot.on_turn(context)
            elif activity.type == ActivityTypes.event:
                self._apply_event_to_turn_context_activity(context, activity)
                await self._bot.on_turn(context)
            else:
                await context.send_activity(activity)

        await self._adapter.continue_conversation(
            conversation_reference, callback, claims_identity=claims_identity
        )
        return ResourceResponse(id=str(uuid4()))

    @staticmethod
    def _apply_eoc_to_turn_context_activity(
        context: TurnContext, end_of_conversation_activity: Activity
    ):
        context.activity.type = end_of_conversation_activity.type
        context.activity.text = end_of_conversation_activity.text
        context.activity.code = end_of_conversation_activity.code

        context.activity.reply_to_id = end_of_conversation_activity.reply_to_id
        context.activity.value = end_of_conversation_activity.value
        context.activity.entities = end_of_conversation_activity.entities
        context.activity.local_timestamp = end_of_conversation_activity.local_timestamp
        context.activity.timestamp = end_of_conversation_activity.timestamp
        context.activity.channel_data = end_of_conversation_activity.channel_data
        context.activity.additional_properties = (
            end_of_conversation_activity.additional_properties
        )

    @staticmethod
    def _apply_event_to_turn_context_activity(
        context: TurnContext, event_activity: Activity
    ):
        context.activity.type = event_activity.type
        context.activity.name = event_activity.name
        context.activity.value = event_activity.value
        context.activity.relates_to = event_activity.relates_to

        context.activity.reply_to_id = event_activity.reply_to_id
        context.activity.value = event_activity.value
        context.activity.entities = event_activity.entities
        context.activity.local_timestamp = event_activity.local_timestamp
        context.activity.timestamp = event_activity.timestamp
        context.activity.channel_data = event_activity.channel_data
        context.activity.additional_properties = event_activity.additional_properties
