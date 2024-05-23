# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import uuid4
from logging import Logger
from typing import Callable

from botbuilder.core import Bot, BotAdapter, TurnContext
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ResourceResponse,
    CallerIdConstants,
)
from botframework.connector.auth import (
    ClaimsIdentity,
    JwtTokenValidation,
)
from .skill_conversation_reference import SkillConversationReference
from .conversation_id_factory import ConversationIdFactoryBase

from .skill_handler import SkillHandler


class _SkillHandlerImpl(SkillHandler):
    def __init__(  # pylint: disable=super-init-not-called
        self,
        skill_conversation_reference_key: str,
        adapter: BotAdapter,
        bot: Bot,
        conversation_id_factory: ConversationIdFactoryBase,
        get_oauth_scope: Callable[[], str],
        logger: Logger = None,
    ):
        if not skill_conversation_reference_key:
            raise TypeError("skill_conversation_reference_key can't be None")
        if not adapter:
            raise TypeError("adapter can't be None")
        if not bot:
            raise TypeError("bot can't be None")
        if not conversation_id_factory:
            raise TypeError("conversation_id_factory can't be None")

        self._skill_conversation_reference_key = skill_conversation_reference_key
        self._adapter = adapter
        self._bot = bot
        self._conversation_id_factory = conversation_id_factory
        self._get_oauth_scope = get_oauth_scope or (lambda: "")
        self._logger = logger

    async def on_send_to_conversation(
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        activity: Activity,
    ) -> ResourceResponse:
        """
        send_to_conversation() API for Skill

        This method allows you to send an activity to the end of a conversation.

        This is slightly different from ReplyToActivity().
        * SendToConversation(conversation_id) - will append the activity to the end
        of the conversation according to the timestamp or semantics of the channel.
        * ReplyToActivity(conversation_id,ActivityId) - adds the activity as a reply
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
            claims_identity,
            conversation_id,
            None,
            activity,
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
        * SendToConversation(conversation_id) - will append the activity to the end
        of the conversation according to the timestamp or semantics of the channel.
        * ReplyToActivity(conversation_id,ActivityId) - adds the activity as a reply
        to another activity, if the channel supports it. If the channel does not
        support nested replies, ReplyToActivity falls back to SendToConversation.

        Use ReplyToActivity when replying to a specific activity in the
        conversation.

        Use SendToConversation in all other cases.
        :param claims_identity: Claims identity for the bot.
        :type claims_identity: :class:`botframework.connector.auth.ClaimsIdentity`
        :param conversation_id:The conversation ID.
        :type conversation_id: str
        :param activity_id: Activity ID to send.
        :type activity_id: str
        :param activity: Activity to send.
        :type activity: Activity
        :return:
        """
        return await self._process_activity(
            claims_identity,
            conversation_id,
            activity_id,
            activity,
        )

    async def on_delete_activity(
        self, claims_identity: ClaimsIdentity, conversation_id: str, activity_id: str
    ):
        skill_conversation_reference = await self._get_skill_conversation_reference(
            conversation_id
        )

        async def callback(turn_context: TurnContext):
            turn_context.turn_state[self.SKILL_CONVERSATION_REFERENCE_KEY] = (
                skill_conversation_reference
            )
            await turn_context.delete_activity(activity_id)

        await self._adapter.continue_conversation(
            skill_conversation_reference.conversation_reference,
            callback,
            claims_identity=claims_identity,
            audience=skill_conversation_reference.oauth_scope,
        )

    async def on_update_activity(
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        activity_id: str,
        activity: Activity,
    ) -> ResourceResponse:
        skill_conversation_reference = await self._get_skill_conversation_reference(
            conversation_id
        )

        resource_response: ResourceResponse = None

        async def callback(turn_context: TurnContext):
            nonlocal resource_response
            turn_context.turn_state[self.SKILL_CONVERSATION_REFERENCE_KEY] = (
                skill_conversation_reference
            )
            activity.apply_conversation_reference(
                skill_conversation_reference.conversation_reference
            )
            turn_context.activity.id = activity_id
            turn_context.activity.caller_id = (
                f"{CallerIdConstants.bot_to_bot_prefix}"
                f"{JwtTokenValidation.get_app_id_from_claims(claims_identity.claims)}"
            )
            resource_response = await turn_context.update_activity(activity)

        await self._adapter.continue_conversation(
            skill_conversation_reference.conversation_reference,
            callback,
            claims_identity=claims_identity,
            audience=skill_conversation_reference.oauth_scope,
        )

        return resource_response or ResourceResponse(id=str(uuid4()).replace("-", ""))

    @staticmethod
    def _apply_skill_activity_to_turn_context_activity(
        context: TurnContext, activity: Activity
    ):
        context.activity.type = activity.type
        context.activity.text = activity.text
        context.activity.code = activity.code
        context.activity.name = activity.name
        context.activity.relates_to = activity.relates_to

        context.activity.reply_to_id = activity.reply_to_id
        context.activity.value = activity.value
        context.activity.entities = activity.entities
        context.activity.locale = activity.locale
        context.activity.local_timestamp = activity.local_timestamp
        context.activity.timestamp = activity.timestamp
        context.activity.channel_data = activity.channel_data
        context.activity.additional_properties = activity.additional_properties

    async def _process_activity(
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        reply_to_activity_id: str,
        activity: Activity,
    ) -> ResourceResponse:
        skill_conversation_reference = await self._get_skill_conversation_reference(
            conversation_id
        )

        # If an activity is sent, return the ResourceResponse
        resource_response: ResourceResponse = None

        async def callback(context: TurnContext):
            nonlocal resource_response
            context.turn_state[SkillHandler.SKILL_CONVERSATION_REFERENCE_KEY] = (
                skill_conversation_reference
            )

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
                await self._send_to_bot(activity, context)
            elif activity.type == ActivityTypes.event:
                await self._send_to_bot(activity, context)
            elif activity.type in (ActivityTypes.command, ActivityTypes.command_result):
                if activity.name.startswith("application/"):
                    # Send to channel and capture the resource response for the SendActivityCall so we can return it.
                    resource_response = await context.send_activity(activity)
                else:
                    await self._send_to_bot(activity, context)
            else:
                # Capture the resource response for the SendActivityCall so we can return it.
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

    async def _get_skill_conversation_reference(
        self, conversation_id: str
    ) -> SkillConversationReference:
        # Get the SkillsConversationReference
        try:
            skill_conversation_reference = (
                await self._conversation_id_factory.get_skill_conversation_reference(
                    conversation_id
                )
            )
        except (NotImplementedError, AttributeError):
            if self._logger:
                self._logger.log(
                    30,
                    "Got NotImplementedError when trying to call get_skill_conversation_reference() "
                    "on the SkillConversationIdFactory, attempting to use deprecated "
                    "get_conversation_reference() method instead.",
                )

            # ConversationIdFactory can return either a SkillConversationReference (the newer way),
            # or a ConversationReference (the old way, but still here for compatibility).  If a
            # ConversationReference is returned, build a new SkillConversationReference to simplify
            # the remainder of this method.
            conversation_reference_result = (
                await self._conversation_id_factory.get_conversation_reference(
                    conversation_id
                )
            )
            if isinstance(conversation_reference_result, SkillConversationReference):
                skill_conversation_reference: SkillConversationReference = (
                    conversation_reference_result
                )
            else:
                skill_conversation_reference: SkillConversationReference = (
                    SkillConversationReference(
                        conversation_reference=conversation_reference_result,
                        oauth_scope=self._get_oauth_scope(),
                    )
                )

        if not skill_conversation_reference:
            raise KeyError("SkillConversationReference not found")

        if not skill_conversation_reference.conversation_reference:
            raise KeyError("conversationReference not found")

        return skill_conversation_reference

    async def _send_to_bot(self, activity: Activity, context: TurnContext):
        _SkillHandlerImpl._apply_skill_activity_to_turn_context_activity(
            context, activity
        )
        await self._bot.on_turn(context)
