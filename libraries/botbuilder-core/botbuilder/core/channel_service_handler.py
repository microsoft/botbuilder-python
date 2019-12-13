# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.schema import (
    Activity,
    AttachmentData,
    ChannelAccount,
    ConversationParameters,
    ConversationsResult,
    ConversationResourceResponse,
    PagedMembersResult,
    ResourceResponse,
    Transcript,
)

from botframework.connector.auth import (
    AuthenticationConfiguration,
    ChannelProvider,
    ClaimsIdentity,
    CredentialProvider,
    JwtTokenValidation,
)


class BotActionNotImplementedError(Exception):
    """Raised when an action is not implemented"""


class ChannelServiceHandler:
    """
    Initializes a new instance of the <see cref="ChannelServiceHandler"/> class,
    using a credential provider.
    """

    def __init__(
        self,
        credential_provider: CredentialProvider,
        auth_config: AuthenticationConfiguration,
        channel_provider: ChannelProvider = None,
    ):
        if not credential_provider:
            raise TypeError("credential_provider can't be None")

        if not auth_config:
            raise TypeError("auth_config can't be None")

        self._credential_provider = credential_provider
        self._auth_config = auth_config
        self._channel_provider = channel_provider

    async def handle_send_to_conversation(
        self, auth_header, conversation_id, activity
    ) -> ResourceResponse:
        claims_identity = await self._authenticate(auth_header)
        return await self.on_send_to_conversation(
            claims_identity, conversation_id, activity
        )

    async def handle_reply_to_activity(
        self, auth_header, conversation_id, activity_id, activity
    ) -> ResourceResponse:
        claims_identity = await self._authenticate(auth_header)
        return await self.on_reply_to_activity(
            claims_identity, conversation_id, activity_id, activity
        )

    async def handle_update_activity(
        self, auth_header, conversation_id, activity_id, activity
    ) -> ResourceResponse:
        claims_identity = await self._authenticate(auth_header)
        return await self.on_update_activity(
            claims_identity, conversation_id, activity_id, activity
        )

    async def handle_delete_activity(self, auth_header, conversation_id, activity_id):
        claims_identity = await self._authenticate(auth_header)
        await self.on_delete_activity(claims_identity, conversation_id, activity_id)

    async def handle_get_activity_members(
        self, auth_header, conversation_id, activity_id
    ) -> List[ChannelAccount]:
        claims_identity = await self._authenticate(auth_header)
        return await self.on_get_activity_members(
            claims_identity, conversation_id, activity_id
        )

    async def handle_create_conversation(
        self, auth_header, parameters: ConversationParameters
    ) -> ConversationResourceResponse:
        claims_identity = await self._authenticate(auth_header)
        return await self.on_create_conversation(claims_identity, parameters)

    async def handle_get_conversations(
        self, auth_header, continuation_token: str = ""
    ) -> ConversationsResult:
        claims_identity = await self._authenticate(auth_header)
        return await self.on_get_conversations(claims_identity, continuation_token)

    async def handle_get_conversation_members(
        self, auth_header, conversation_id
    ) -> List[ChannelAccount]:
        claims_identity = await self._authenticate(auth_header)
        return await self.on_get_conversation_members(claims_identity, conversation_id)

    async def handle_get_conversation_paged_members(
        self,
        auth_header,
        conversation_id,
        page_size: int = 0,
        continuation_token: str = "",
    ) -> PagedMembersResult:
        claims_identity = await self._authenticate(auth_header)
        return await self.on_get_conversation_paged_members(
            claims_identity, conversation_id, page_size, continuation_token
        )

    async def handle_delete_conversation_member(
        self, auth_header, conversation_id, member_id
    ):
        claims_identity = await self._authenticate(auth_header)
        await self.on_delete_conversation_member(
            claims_identity, conversation_id, member_id
        )

    async def handle_send_conversation_history(
        self, auth_header, conversation_id, transcript: Transcript
    ) -> ResourceResponse:
        claims_identity = await self._authenticate(auth_header)
        return await self.on_send_conversation_history(
            claims_identity, conversation_id, transcript
        )

    async def handle_upload_attachment(
        self, auth_header, conversation_id, attachment_upload: AttachmentData
    ) -> ResourceResponse:
        claims_identity = await self._authenticate(auth_header)
        return await self.on_upload_attachment(
            claims_identity, conversation_id, attachment_upload
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
        raise BotActionNotImplementedError()

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
        :param parameters:
        :return:
        """
        raise BotActionNotImplementedError()

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
        raise BotActionNotImplementedError()

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
        raise BotActionNotImplementedError()

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
        raise BotActionNotImplementedError()

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
        raise BotActionNotImplementedError()

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
        raise BotActionNotImplementedError()

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
        raise BotActionNotImplementedError()

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

        This REST API takes a ConversationId. Optionally a page_size and/or
        continuation_token can be provided. It returns a PagedMembersResult, which
        contains an array
        of ChannelAccounts representing the members of the conversation and a
        continuation token that can be used to get more values.

        One page of ChannelAccounts records are returned with each call. The number
        of records in a page may vary between channels and calls. The page_size
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
        raise BotActionNotImplementedError()

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
        raise BotActionNotImplementedError()

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
        raise BotActionNotImplementedError()

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
        raise BotActionNotImplementedError()

    async def _authenticate(self, auth_header: str) -> ClaimsIdentity:
        if not auth_header:
            is_auth_disabled = (
                await self._credential_provider.is_authentication_disabled()
            )
            if is_auth_disabled:
                # In the scenario where Auth is disabled, we still want to have the
                # IsAuthenticated flag set in the ClaimsIdentity. To do this requires
                # adding in an empty claim.
                return ClaimsIdentity({}, True)

            raise PermissionError()

        return await JwtTokenValidation.validate_auth_header(
            auth_header,
            self._credential_provider,
            self._channel_provider,
            "unknown",
            auth_configuration=self._auth_config,
        )
