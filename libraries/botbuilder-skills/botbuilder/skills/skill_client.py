# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC
from typing import List

from botbuilder.core import Bot, BotAdapter
from botbuilder.schema import (
    Activity,
    AttachmentData,
    ChannelAccount,
    ConversationAccount,
    ConversationParameters,
    ConversationResourceResponse,
    ConversationsResult,
    PagedMembersResult,
    ResourceResponse,
    RoleTypes,
    Transcript,
)
from botframework.connector.auth import ClaimsIdentity

from .channel_api_args import ChannelApiArgs
from .channel_api_methods import ChannelApiMethods
from .channel_api_middleware import ChannelApiMiddleware
from .skill_conversation import SkillConversation


class SkillClient(ABC):

    """
    A skill host adapter implements API to forward activity to a skill and
    implements routing ChannelAPI calls from the Skill up through the bot/adapter.
    """

    INVOKE_ACTIVITY_NAME = "SkillEvents.ChannelApiInvoke"

    def __init__(self, adapter: BotAdapter, logger: object = None):

        self._bot_adapter = adapter
        self._logger = logger

        if not any(
            isinstance(middleware, ChannelApiMiddleware)
            for middleware in adapter.middleware_set
        ):
            adapter.middleware_set.use(ChannelApiMiddleware(self))

    async def get_conversations(
        self,
        bot: Bot,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        continuation_token: str = "",
    ) -> ConversationsResult:
        """
        get_conversations() API for Skill

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
        return await self._invoke_channel_api(
            bot,
            claims_identity,
            ChannelApiMethods.GET_CONVERSATIONS,
            conversation_id,
            continuation_token,
        )

    async def create_conversation(
        self,
        bot: Bot,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        parameters: ConversationParameters,
    ) -> ConversationResourceResponse:
        """
        create_conversation() API for Skill

        Create a new Conversation.

        POST to this method with a
        * Bot being the bot creating the conversation
        * IsGroup set to true if this is not a direct message (default is false)
        * Array containing the members to include in the conversation

        The return value is a ResourceResponse which contains a conversation id
        which is suitable for use
        in the message payload and REST API uris.

        Most channels only support the semantics of bots initiating a direct
        message conversation.  An example of how to do that would be:

        var resource = await connector.conversations.CreateConversation(new
        ConversationParameters(){ Bot = bot, members = new ChannelAccount[] { new
        ChannelAccount("user1") } );
        await connect.Conversations.SendToConversationAsync(resource.Id, new
        Activity() ... ) ;

        end.
        :param bot:
        :param claims_identity:
        :param conversation_id:
        :param parameters:
        :return:
        """
        return await self._invoke_channel_api(
            bot,
            claims_identity,
            ChannelApiMethods.CREATE_CONVERSATION,
            conversation_id,
            parameters,
        )

    async def send_to_conversation(
        self,
        bot: Bot,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        activity: Activity,
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
        :param bot:
        :param claims_identity:
        :param conversation_id:
        :param activity:
        :return:
        """
        return await self._invoke_channel_api(
            bot,
            claims_identity,
            ChannelApiMethods.SEND_TO_CONVERSATION,
            conversation_id,
            activity,
        )

    async def send_conversation_history(
        self,
        bot: Bot,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        transcript: Transcript,
    ) -> ResourceResponse:
        """
        send_conversation_history() API for Skill.

        This method allows you to upload the historic activities to the
        conversation.

        Sender must ensure that the historic activities have unique ids and
        appropriate timestamps. The ids are used by the client to deal with
        duplicate activities and the timestamps are used by the client to render
        the activities in the right order.
        :param bot:
        :param claims_identity:
        :param conversation_id:
        :param transcript:
        :return:
        """
        return await self._invoke_channel_api(
            bot,
            claims_identity,
            ChannelApiMethods.SEND_CONVERSATION_HISTORY,
            conversation_id,
            transcript,
        )

    async def update_activity(
        self,
        bot: Bot,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        activity_id: str,
        activity: Activity,
    ) -> ResourceResponse:
        """
        update_activity() API for Skill.

        Edit an existing activity.

        Some channels allow you to edit an existing activity to reflect the new
        state of a bot conversation.

        For example, you can remove buttons after someone has clicked "Approve"
        button.
        :param bot:
        :param claims_identity:
        :param conversation_id:
        :param activity_id:
        :param activity:
        :return:
        """
        return await self._invoke_channel_api(
            bot,
            claims_identity,
            ChannelApiMethods.UPDATE_ACTIVITY,
            conversation_id,
            activity_id,
            activity,
        )

    async def reply_to_activity(
        self,
        bot: Bot,
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
        :param bot:
        :param claims_identity:
        :param conversation_id:
        :param activity_id:
        :param activity:
        :return:
        """
        return await self._invoke_channel_api(
            bot,
            claims_identity,
            ChannelApiMethods.REPLY_TO_ACTIVITY,
            conversation_id,
            activity_id,
            activity,
        )

    async def delete_activity(
        self,
        bot: Bot,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        activity_id: str,
    ):
        """
        delete_activity() API for Skill.

        Delete an existing activity.

        Some channels allow you to delete an existing activity, and if successful
        this method will remove the specified activity.
        :param bot:
        :param claims_identity:
        :param conversation_id:
        :param activity_id:
        :return:
        """
        return await self._invoke_channel_api(
            bot,
            claims_identity,
            ChannelApiMethods.DELETE_ACTIVITY,
            conversation_id,
            activity_id,
        )

    async def get_conversation_members(
        self, bot: Bot, claims_identity: ClaimsIdentity, conversation_id: str,
    ) -> List[ChannelAccount]:
        """
        get_conversation_members() API for Skill.

        Enumerate the members of a conversation.

        This REST API takes a ConversationId and returns a list of ChannelAccount
        objects representing the members of the conversation.
        :param bot:
        :param claims_identity:
        :param conversation_id:
        :return:
        """
        return await self._invoke_channel_api(
            bot,
            claims_identity,
            ChannelApiMethods.GET_CONVERSATION_MEMBERS,
            conversation_id,
        )

    async def get_conversation_paged_members(
        self,
        bot: Bot,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        page_size: int = None,
        continuation_token: str = "",
    ) -> PagedMembersResult:
        """
        get_conversation_paged_members() API for Skill.

        Enumerate the members of a conversation one page at a time.

        This REST API takes a ConversationId. Optionally a pageSize and/or
        continuationToken can be provided. It returns a PagedMembersResult, which
        contains an array
        of ChannelAccounts representing the members of the conversation and a
        continuation token that can be used to get more values.

        One page of ChannelAccounts records are returned with each call. The number
        of records in a page may vary between channels and calls. The pageSize
        parameter can be used as
        a suggestion. If there are no additional results the response will not
        contain a continuation token. If there are no members in the conversation
        the Members will be empty or not present in the response.

        A response to a request that has a continuation token from a prior request
        may rarely return members from a previous request.
        :param bot:
        :param claims_identity:
        :param conversation_id:
        :param page_size:
        :param continuation_token:
        :return:
        """
        return await self._invoke_channel_api(
            bot,
            claims_identity,
            ChannelApiMethods.GET_CONVERSATION_PAGED_MEMBERS,
            conversation_id,
            page_size,
            continuation_token,
        )

    async def delete_conversation_member(
        self,
        bot: Bot,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        member_id: str,
    ):
        """
        delete_conversation_member() API for Skill.

        Deletes a member from a conversation.

        This REST API takes a ConversationId and a memberId (of type string) and
        removes that member from the conversation. If that member was the last
        member
        of the conversation, the conversation will also be deleted.
        :param bot:
        :param claims_identity:
        :param conversation_id:
        :param member_id:
        :return:
        """
        return await self._invoke_channel_api(
            bot,
            claims_identity,
            ChannelApiMethods.DELETE_CONVERSATION_MEMBER,
            conversation_id,
            member_id,
        )

    async def get_activity_members(
        self,
        bot: Bot,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        activity_id: str,
    ) -> List[ChannelAccount]:
        """
        get_activity_members() API for Skill.

        Enumerate the members of an activity.

        This REST API takes a ConversationId and a ActivityId, returning an array
        of ChannelAccount objects representing the members of the particular
        activity in the conversation.
        :param bot:
        :param claims_identity:
        :param conversation_id:
        :param activity_id:
        :return:
        """
        return await self._invoke_channel_api(
            bot,
            claims_identity,
            ChannelApiMethods.GET_ACTIVITY_MEMBERS,
            conversation_id,
            activity_id,
        )

    async def upload_attachment(
        self,
        bot: Bot,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        attachment_upload: AttachmentData,
    ) -> ResourceResponse:
        """
        upload_attachment() API for Skill.

        Upload an attachment directly into a channel's blob storage.

        This is useful because it allows you to store data in a compliant store
        when dealing with enterprises.

        The response is a ResourceResponse which contains an AttachmentId which is
        suitable for using with the attachments API.
        :param bot:
        :param claims_identity:
        :param conversation_id:
        :param attachment_upload:
        :return:
        """
        return await self._invoke_channel_api(
            bot,
            claims_identity,
            ChannelApiMethods.UPLOAD_ATTACHMENT,
            conversation_id,
            attachment_upload,
        )

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

        # TODO: Extension for create_invoke_activity
        channel_api_invoke_activity: Activity = Activity.create_invoke_activity()
        channel_api_invoke_activity.name = SkillClient.INVOKE_ACTIVITY_NAME
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

            # Use the activityPayload for channel accounts, it will be in From=Bot/Skill Recipient=User,
            # We want to send it to the bot as From=User, Recipient=Bot so we have correct state context.
            channel_api_invoke_activity.channel_id = activity_payload.channel_id
            channel_api_invoke_activity.from_property = activity_payload.recipient
            channel_api_invoke_activity.recipient = activity_payload.from_property

            # We want ActivityPayload to also be in User->Bot context, if it is outbound it will go through context.
            # SendActivity which will flip outgoing to Bot->Use regardless this gives us same memory context of
            # User->Bot which is useful for things like EndOfConversation processing being in the correct
            # memory context.
            activity_payload.from_property = channel_api_invoke_activity.from_property
            activity_payload.recipient = channel_api_invoke_activity.recipient

        channel_api_args = ChannelApiArgs(method=method, args=args)

        channel_api_invoke_activity.value = channel_api_args

        # send up to the bot to process it...
        await self._bot_adapter.process_activity_with_claims(
            claims_identity, channel_api_invoke_activity, bot.on_turn
        )

        if channel_api_args.exception:
            raise channel_api_args.exception

        # Return the result that was captured in the middleware handler.
        return channel_api_args.result
