# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import uuid4

from botbuilder.core import Bot, BotAdapter, ChannelServiceHandler, TurnContext
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ResourceResponse,
    CallerIdConstants,
)
from botframework.connector.auth import (
    AuthenticationConfiguration,
    AuthenticationConstants,
    ChannelProvider,
    ClaimsIdentity,
    CredentialProvider,
    GovernmentConstants,
    JwtTokenValidation,
)
from .skill_conversation_reference import SkillConversationReference
from .conversation_id_factory import ConversationIdFactoryBase


class SkillHandler(ChannelServiceHandler):

    SKILL_CONVERSATION_REFERENCE_KEY = (
        "botbuilder.core.skills.SkillConversationReference"
    )

    def __init__(
        self,
        adapter: BotAdapter,
        bot: Bot,
        conversation_id_factory: ConversationIdFactoryBase,
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
        :param claims_identity: Claims identity for the bot.
        :type claims_identity: :class:`botframework.connector.auth.ClaimsIdentity`
        :param conversation_id:The conversation ID.
        :type conversation_id: str
        :param activity: Activity to send.
        :type activity: Activity
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
        :param claims_identity: Claims identity for the bot.
        :type claims_identity: :class:`botframework.connector.auth.ClaimsIdentity`
        :param conversation_id:The conversation ID.
        :type conversation_id: str
        :param activity: Activity to send.
        :type activity: Activity
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
        # Get the SkillsConversationReference
        conversation_reference_result = await self._conversation_id_factory.get_conversation_reference(
            conversation_id
        )

        # ConversationIdFactory can return either a SkillConversationReference (the newer way),
        # or a ConversationReference (the old way, but still here for compatibility).  If a
        # ConversationReference is returned, build a new SkillConversationReference to simplify
        # the remainder of this method.
        skill_conversation_reference: SkillConversationReference = None
        if isinstance(conversation_reference_result, SkillConversationReference):
            skill_conversation_reference = conversation_reference_result
        else:
            skill_conversation_reference = SkillConversationReference(
                conversation_reference=conversation_reference_result,
                oauth_scope=(
                    GovernmentConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
                    if self._channel_provider and self._channel_provider.is_government()
                    else AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
                ),
            )

        if not skill_conversation_reference:
            raise KeyError("SkillConversationReference not found")

        if not skill_conversation_reference.conversation_reference:
            raise KeyError("conversationReference not found")

        # If an activity is sent, return the ResourceResponse
        resource_response: ResourceResponse = None

        async def callback(context: TurnContext):
            nonlocal resource_response
            context.turn_state[
                SkillHandler.SKILL_CONVERSATION_REFERENCE_KEY
            ] = skill_conversation_reference

            TurnContext.apply_conversation_reference(
                activity, skill_conversation_reference.conversation_reference
            )

            context.activity.id = reply_to_activity_id

            app_id = JwtTokenValidation.get_app_id_from_claims(claims_identity.claims)
            context.activity.caller_id = (
                f"{CallerIdConstants.bot_to_bot_prefix}{app_id}"
            )

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
                resource_response = await context.send_activity(activity)

        await self._adapter.continue_conversation(
            skill_conversation_reference.conversation_reference,
            callback,
            claims_identity=claims_identity,
            audience=skill_conversation_reference.oauth_scope,
        )

        if not resource_response:
            resource_response = ResourceResponse(id=str(uuid4()))

        return resource_response

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
        context.activity.locale = end_of_conversation_activity.locale
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
        context.activity.locale = event_activity.locale
        context.activity.local_timestamp = event_activity.local_timestamp
        context.activity.timestamp = event_activity.timestamp
        context.activity.channel_data = event_activity.channel_data
        context.activity.additional_properties = event_activity.additional_properties
