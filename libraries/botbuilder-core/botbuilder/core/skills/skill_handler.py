# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from logging import Logger

from botbuilder.core import Bot, BotAdapter, ChannelServiceHandler
from botbuilder.schema import (
    Activity,
    ResourceResponse,
)
from botframework.connector.auth import (
    AuthenticationConfiguration,
    AuthenticationConstants,
    ChannelProvider,
    ClaimsIdentity,
    CredentialProvider,
    GovernmentConstants,
)
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
        logger: Logger = None,
    ):
        # pylint: disable=import-outside-toplevel
        super().__init__(credential_provider, auth_configuration, channel_provider)

        if not adapter:
            raise TypeError("adapter can't be None")
        if not bot:
            raise TypeError("bot can't be None")
        if not conversation_id_factory:
            raise TypeError("conversation_id_factory can't be None")

        self._logger = logger

        def aux_func():
            nonlocal self
            return (
                GovernmentConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
                if self._channel_provider and self._channel_provider.is_government()
                else AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
            )

        from ._skill_handler_impl import _SkillHandlerImpl

        self._inner = _SkillHandlerImpl(
            self.SKILL_CONVERSATION_REFERENCE_KEY,
            adapter,
            bot,
            conversation_id_factory,
            aux_func,
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
