# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import uuid4
from typing import List

from botbuilder.core.integration import ChannelServiceHandler
from botbuilder.core import Bot, BotAdapter, TurnContext
from botbuilder.schema import (
    Activity,
    ActivityTypes,
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
from botframework.connector.auth import (
    AuthenticationConfiguration,
    ChannelProvider,
    ClaimsIdentity,
    CredentialProvider,
)

from .skill_conversation_id_factory import SkillConversationIdFactory


class SkillHandler(ChannelServiceHandler):
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
        self.skill_conversation_reference_key = "SkillConversationReference"

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

    async def on_get_conversations(
        self, claims_identity: ClaimsIdentity, continuation_token: str = "",
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
        :param claims_identity:
        :param conversation_id:
        :param continuation_token:
        :return:
        """
        raise NotImplementedError()

    async def on_create_conversation(
        self, claims_identity: ClaimsIdentity, parameters: ConversationParameters,
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
        :param claims_identity:
        :param conversation_id:
        :param parameters:
        :return:
        """
        raise NotImplementedError()

    async def on_send_conversation_history(
        self,
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
        :param claims_identity:
        :param conversation_id:
        :param transcript:
        :return:
        """
        raise NotImplementedError()

    async def on_update_activity(
        self,
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
        :param claims_identity:
        :param conversation_id:
        :param activity_id:
        :param activity:
        :return:
        """
        raise NotImplementedError()

    async def on_delete_activity(
        self, claims_identity: ClaimsIdentity, conversation_id: str, activity_id: str,
    ):
        """
        delete_activity() API for Skill.

        Delete an existing activity.

        Some channels allow you to delete an existing activity, and if successful
        this method will remove the specified activity.
        :param claims_identity:
        :param conversation_id:
        :param activity_id:
        :return:
        """
        raise NotImplementedError()

    async def on_get_conversation_members(
        self, claims_identity: ClaimsIdentity, conversation_id: str,
    ) -> List[ChannelAccount]:
        """
        get_conversation_members() API for Skill.

        Enumerate the members of a conversation.

        This REST API takes a ConversationId and returns a list of ChannelAccount
        objects representing the members of the conversation.
        :param claims_identity:
        :param conversation_id:
        :return:
        """
        raise NotImplementedError()

    async def on_get_conversation_paged_members(
        self,
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
        :param claims_identity:
        :param conversation_id:
        :param page_size:
        :param continuation_token:
        :return:
        """
        raise NotImplementedError()

    async def on_delete_conversation_member(
        self, claims_identity: ClaimsIdentity, conversation_id: str, member_id: str,
    ):
        """
        delete_conversation_member() API for Skill.

        Deletes a member from a conversation.

        This REST API takes a ConversationId and a memberId (of type string) and
        removes that member from the conversation. If that member was the last
        member
        of the conversation, the conversation will also be deleted.
        :param claims_identity:
        :param conversation_id:
        :param member_id:
        :return:
        """
        raise NotImplementedError()

    async def on_get_activity_members(
        self, claims_identity: ClaimsIdentity, conversation_id: str, activity_id: str,
    ) -> List[ChannelAccount]:
        """
        get_activity_members() API for Skill.

        Enumerate the members of an activity.

        This REST API takes a ConversationId and a ActivityId, returning an array
        of ChannelAccount objects representing the members of the particular
        activity in the conversation.
        :param claims_identity:
        :param conversation_id:
        :param activity_id:
        :return:
        """
        raise NotImplementedError()

    async def on_upload_attachment(
        self,
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
        :param claims_identity:
        :param conversation_id:
        :param attachment_upload:
        :return:
        """
        raise NotImplementedError()

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
            raise RuntimeError("ConversationReference not found")

        async def callback(context: TurnContext):
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
