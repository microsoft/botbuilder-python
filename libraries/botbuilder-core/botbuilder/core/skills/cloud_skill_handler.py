# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from logging import Logger
from botbuilder.core import BotAdapter, Bot, CloudChannelServiceHandler
from botbuilder.schema import Activity, ResourceResponse
from botframework.connector.auth import BotFrameworkAuthentication, ClaimsIdentity

from .conversation_id_factory import ConversationIdFactoryBase
from .skill_handler import SkillHandler
from ._skill_handler_impl import _SkillHandlerImpl


class CloudSkillHandler(CloudChannelServiceHandler):
    SKILL_CONVERSATION_REFERENCE_KEY = SkillHandler.SKILL_CONVERSATION_REFERENCE_KEY

    def __init__(
        self,
        adapter: BotAdapter,
        bot: Bot,
        conversation_id_factory: ConversationIdFactoryBase,
        auth: BotFrameworkAuthentication,
        logger: Logger = None,
    ):
        super().__init__(auth)

        if not adapter:
            raise TypeError("adapter can't be None")
        if not bot:
            raise TypeError("bot can't be None")
        if not conversation_id_factory:
            raise TypeError("conversation_id_factory can't be None")

        self._inner = _SkillHandlerImpl(
            self.SKILL_CONVERSATION_REFERENCE_KEY,
            adapter,
            bot,
            conversation_id_factory,
            auth.get_originating_audience,
            logger,
        )

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
        return await self._inner.on_send_to_conversation(
            claims_identity,
            conversation_id,
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
        return await self._inner.on_reply_to_activity(
            claims_identity,
            conversation_id,
            activity_id,
            activity,
        )

    async def on_delete_activity(
        self, claims_identity: ClaimsIdentity, conversation_id: str, activity_id: str
    ):
        await self._inner.on_delete_activity(
            claims_identity, conversation_id, activity_id
        )

    async def on_update_activity(
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        activity_id: str,
        activity: Activity,
    ) -> ResourceResponse:
        return await self._inner.on_update_activity(
            claims_identity, conversation_id, activity_id, activity
        )
