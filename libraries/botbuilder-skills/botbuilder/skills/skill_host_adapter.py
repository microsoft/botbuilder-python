# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod

from botbuilder.core import Bot, BotAdapter, InvokeResponse, TurnContext
from botbuilder.schema import (
    Activity,
    ChannelAccount,
    ConversationAccount,
    ConversationsResult,
    RoleTypes,
)
from botframework.connector.auth import ClaimsIdentity

from .adapters import BotFrameworkSkill
from .channel_api_middleware import ChannelApiMiddleware
from .skill_conversation import SkillConversation


class SkillHostAdapter(ABC):

    """
    A skill host adapter implements API to forward activity to a skill and
    implements routing ChannelAPI calls from the Skill up through the bot/adapter.
    """

    INVOKE_ACTIVITY_NAME = "SkillEvents.ChannelApiInvoke"

    def __init__(self, adapter: BotAdapter, logger: object = None):

        self.channel_adapter = adapter
        self._logger = logger

        if not any(
            isinstance(middleware, ChannelApiMiddleware)
            for middleware in adapter.middleware_set
        ):
            adapter.middleware_set.use(ChannelApiMiddleware(self))

    @abstractmethod
    async def forward_activity(
        self,
        context: TurnContext,
        skill: BotFrameworkSkill,
        skill_host_endpoint: str,
        activity: Activity,
    ) -> InvokeResponse:
        """
        Forwards an activity to a skill.
        :param context: Turn context
        :param skill: A BotFrameworkSkill instance with the skill information.
        :param skill_host_endpoint: The callback Url for the skill host.
        :param activity: activity to forward
        :return: Async task with optional InvokeResponse.
        """
        raise NotImplementedError()

    async def get_conversations_async(
        self,
        bot: Bot,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        continuation_token: str = "",
    ) -> ConversationsResult:
        """
        List the Conversations in which this bot has participated.

        GET from this method with a skip token

        The return value is a ConversationsResult, which contains an array of
        ConversationMembers and a skip token.  If the skip token is not empty, then
        there are further values to be returned. Call this method again with the
        returned token to get more values.

        Each ConversationMembers object contains the ID of the conversation and an
        array of ChannelAccounts that describe the members of the conversation.
        :param bot:
        :param claims_identity:
        :param conversation_id:
        :param continuation_token:
        :return:
        """
        # pylint: disable=unnecessary-pass
        pass

    async def _invoke_channel_api(
        self,
        bot: Bot,
        claims_identity: ClaimsIdentity,
        method: str,
        conversation_id: str,
        *args,
    ) -> object:
        if self._logger:
            self._logger.log(f'InvokeChannelApiAsync(). Invoking method "{method}"')

        skill_conversation = SkillConversation(conversation_id)

        # TODO: Extention for create_invoke_activity
        channel_api_invoke_activity: Activity = Activity.create_invoke_activity()
        channel_api_invoke_activity.name = SkillHostAdapter.INVOKE_ACTIVITY_NAME
        channel_api_invoke_activity.channel_id = "unknown"
        channel_api_invoke_activity.service_url = skill_conversation.service_url
        channel_api_invoke_activity.conversation = ConversationAccount(
            id=skill_conversation.conversation_id
        )
        channel_api_invoke_activity.from_property = ChannelAccount(id="unknown")
        channel_api_invoke_activity.recipient = ChannelAccount(
            id="unknown", role=RoleTypes.bot
        )

        # Take first activity or default
        activity_payload = next(
            iter([arg for arg in args if isinstance(arg, Activity)]), None
        )

        if activity_payload:

            # fix up activityPayload with original conversation.Id and id
            activity_payload.conversation.id = skill_conversation.conversation_id
            activity_payload.service_url = skill_conversation.service_url

        # printing for pylint
        print(bot, claims_identity)
