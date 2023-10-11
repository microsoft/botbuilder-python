# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from msrest.pipeline import ClientRawResponse
from msrest.exceptions import HttpOperationError

from ... import models


class ConversationsOperations:
    """ConversationsOperations async operations.

    You should not instantiate directly this class, but create a Client instance that will create it for you and attach
     it as attribute.

    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    :ivar api_version: The API version to use for the request. Constant value: "v3".
    """

    models = models

    def __init__(self, client, config, serializer, deserializer) -> None:
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer

        self.config = config
        self.api_version = "v3"

    async def get_conversations(
        self,
        continuation_token=None,
        *,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """GetConversations.

        List the Conversations in which this bot has participated.
        GET from this method with a skip token
        The return value is a ConversationsResult, which contains an array of
        ConversationMembers and a skip token.  If the skip token is not empty,
        then
        there are further values to be returned. Call this method again with
        the returned token to get more values.
        Each ConversationMembers object contains the ID of the conversation and
        an array of ChannelAccounts that describe the members of the
        conversation.

        :param continuation_token: skip or continuation token
        :type continuation_token: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ConversationsResult or ClientRawResponse if raw=true
        :rtype: ~botframework.connector.models.ConversationsResult or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.connector.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.get_conversations.metadata["url"]

        # Construct parameters
        query_parameters = {}
        if continuation_token is not None:
            query_parameters["continuationToken"] = self._serialize.query(
                "continuation_token", continuation_token, "str"
            )

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = await self._client.async_send(
            request, stream=False, **operation_config
        )

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("ConversationsResult", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    get_conversations.metadata = {"url": "/v3/conversations"}

    async def create_conversation(
        self, parameters, *, custom_headers=None, raw=False, **operation_config
    ):
        """CreateConversation.

        Create a new Conversation.
        POST to this method with a
        * Bot being the bot creating the conversation
        * IsGroup set to true if this is not a direct message (default is
        false)
        * Array containing the members to include in the conversation
        The return value is a ResourceResponse which contains a conversation id
        which is suitable for use
        in the message payload and REST API uris.
        Most channels only support the semantics of bots initiating a direct
        message conversation.  An example of how to do that would be:
        ```
        var resource = await connector.conversations.CreateConversation(new
        ConversationParameters(){ Bot = bot, members = new ChannelAccount[] {
        new ChannelAccount("user1") } );
        await connect.Conversations.SendToConversationAsync(resource.Id, new
        Activity() ... ) ;
        ```.

        :param parameters: Parameters to create the conversation from
        :type parameters:
         ~botframework.connector.models.ConversationParameters
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ConversationResourceResponse or ClientRawResponse if raw=true
        :rtype: ~botframework.connector.models.ConversationResourceResponse or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.connector.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.create_conversation.metadata["url"]

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        header_parameters["Content-Type"] = "application/json; charset=utf-8"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        body_content = self._serialize.body(parameters, "ConversationParameters")

        # Construct and send request
        request = self._client.post(
            url, query_parameters, header_parameters, body_content
        )
        response = await self._client.async_send(
            request, stream=False, **operation_config
        )

        if response.status_code not in [200, 201, 202]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("ConversationResourceResponse", response)
        if response.status_code == 201:
            deserialized = self._deserialize("ConversationResourceResponse", response)
        if response.status_code == 202:
            deserialized = self._deserialize("ConversationResourceResponse", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    create_conversation.metadata = {"url": "/v3/conversations"}

    async def send_to_conversation(
        self,
        conversation_id,
        activity,
        *,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """SendToConversation.

        This method allows you to send an activity to the end of a
        conversation.
        This is slightly different from ReplyToActivity().
        * SendToConversation(conversationId) - will append the activity to the
        end of the conversation according to the timestamp or semantics of the
        channel.
        * ReplyToActivity(conversationId,ActivityId) - adds the activity as a
        reply to another activity, if the channel supports it. If the channel
        does not support nested replies, ReplyToActivity falls back to
        SendToConversation.
        Use ReplyToActivity when replying to a specific activity in the
        conversation.
        Use SendToConversation in all other cases.

        :param conversation_id: Conversation ID
        :type conversation_id: str
        :param activity: Activity to send
        :type activity: ~botframework.connector.models.Activity
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ResourceResponse or ClientRawResponse if raw=true
        :rtype: ~botframework.connector.models.ResourceResponse or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.connector.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.send_to_conversation.metadata["url"]
        path_format_arguments = {
            "conversationId": self._serialize.url(
                "conversation_id", conversation_id, "str"
            )
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        header_parameters["Content-Type"] = "application/json; charset=utf-8"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        body_content = self._serialize.body(activity, "Activity")

        # Construct and send request
        request = self._client.post(
            url, query_parameters, header_parameters, body_content
        )
        response = await self._client.async_send(
            request, stream=False, **operation_config
        )

        if response.status_code not in [200, 201, 202]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("ResourceResponse", response)
        if response.status_code == 201:
            deserialized = self._deserialize("ResourceResponse", response)
        if response.status_code == 202:
            deserialized = self._deserialize("ResourceResponse", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    send_to_conversation.metadata = {
        "url": "/v3/conversations/{conversationId}/activities"
    }

    async def send_conversation_history(
        self,
        conversation_id,
        activities=None,
        *,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """SendConversationHistory.

        This method allows you to upload the historic activities to the
        conversation.
        Sender must ensure that the historic activities have unique ids and
        appropriate timestamps. The ids are used by the client to deal with
        duplicate activities and the timestamps are used by the client to
        render the activities in the right order.

        :param conversation_id: Conversation ID
        :type conversation_id: str
        :param activities: A collection of Activities that conforms to the
         Transcript schema.
        :type activities: list[~botframework.connector.models.Activity]
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ResourceResponse or ClientRawResponse if raw=true
        :rtype: ~botframework.connector.models.ResourceResponse or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.connector.models.ErrorResponseException>`
        """
        history = models.Transcript(activities=activities)

        # Construct URL
        url = self.send_conversation_history.metadata["url"]
        path_format_arguments = {
            "conversationId": self._serialize.url(
                "conversation_id", conversation_id, "str"
            )
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        header_parameters["Content-Type"] = "application/json; charset=utf-8"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        body_content = self._serialize.body(history, "Transcript")

        # Construct and send request
        request = self._client.post(
            url, query_parameters, header_parameters, body_content
        )
        response = await self._client.async_send(
            request, stream=False, **operation_config
        )

        if response.status_code not in [200, 201, 202]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("ResourceResponse", response)
        if response.status_code == 201:
            deserialized = self._deserialize("ResourceResponse", response)
        if response.status_code == 202:
            deserialized = self._deserialize("ResourceResponse", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    send_conversation_history.metadata = {
        "url": "/v3/conversations/{conversationId}/activities/history"
    }

    async def update_activity(
        self,
        conversation_id,
        activity_id,
        activity,
        *,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """UpdateActivity.

        Edit an existing activity.
        Some channels allow you to edit an existing activity to reflect the new
        state of a bot conversation.
        For example, you can remove buttons after someone has clicked "Approve"
        button.

        :param conversation_id: Conversation ID
        :type conversation_id: str
        :param activity_id: activityId to update
        :type activity_id: str
        :param activity: replacement Activity
        :type activity: ~botframework.connector.models.Activity
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ResourceResponse or ClientRawResponse if raw=true
        :rtype: ~botframework.connector.models.ResourceResponse or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.connector.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.update_activity.metadata["url"]
        path_format_arguments = {
            "conversationId": self._serialize.url(
                "conversation_id", conversation_id, "str"
            ),
            "activityId": self._serialize.url("activity_id", activity_id, "str"),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        header_parameters["Content-Type"] = "application/json; charset=utf-8"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        body_content = self._serialize.body(activity, "Activity")

        # Construct and send request
        request = self._client.put(
            url, query_parameters, header_parameters, body_content
        )
        response = await self._client.async_send(
            request, stream=False, **operation_config
        )

        if response.status_code not in [200, 201, 202]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("ResourceResponse", response)
        if response.status_code == 201:
            deserialized = self._deserialize("ResourceResponse", response)
        if response.status_code == 202:
            deserialized = self._deserialize("ResourceResponse", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    update_activity.metadata = {
        "url": "/v3/conversations/{conversationId}/activities/{activityId}"
    }

    async def reply_to_activity(
        self,
        conversation_id,
        activity_id,
        activity,
        *,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """ReplyToActivity.

        This method allows you to reply to an activity.
        This is slightly different from SendToConversation().
        * SendToConversation(conversationId) - will append the activity to the
        end of the conversation according to the timestamp or semantics of the
        channel.
        * ReplyToActivity(conversationId,ActivityId) - adds the activity as a
        reply to another activity, if the channel supports it. If the channel
        does not support nested replies, ReplyToActivity falls back to
        SendToConversation.
        Use ReplyToActivity when replying to a specific activity in the
        conversation.
        Use SendToConversation in all other cases.

        :param conversation_id: Conversation ID
        :type conversation_id: str
        :param activity_id: activityId the reply is to (OPTIONAL)
        :type activity_id: str
        :param activity: Activity to send
        :type activity: ~botframework.connector.models.Activity
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ResourceResponse or ClientRawResponse if raw=true
        :rtype: ~botframework.connector.models.ResourceResponse or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.connector.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.reply_to_activity.metadata["url"]
        path_format_arguments = {
            "conversationId": self._serialize.url(
                "conversation_id", conversation_id, "str"
            ),
            "activityId": self._serialize.url("activity_id", activity_id, "str"),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        header_parameters["Content-Type"] = "application/json; charset=utf-8"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        body_content = self._serialize.body(activity, "Activity")

        # Construct and send request
        request = self._client.post(
            url, query_parameters, header_parameters, body_content
        )
        response = await self._client.async_send(
            request, stream=False, **operation_config
        )

        if response.status_code not in [200, 201, 202]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("ResourceResponse", response)
        if response.status_code == 201:
            deserialized = self._deserialize("ResourceResponse", response)
        if response.status_code == 202:
            deserialized = self._deserialize("ResourceResponse", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    reply_to_activity.metadata = {
        "url": "/v3/conversations/{conversationId}/activities/{activityId}"
    }

    async def delete_activity(
        self,
        conversation_id,
        activity_id,
        *,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """DeleteActivity.

        Delete an existing activity.
        Some channels allow you to delete an existing activity, and if
        successful this method will remove the specified activity.

        :param conversation_id: Conversation ID
        :type conversation_id: str
        :param activity_id: activityId to delete
        :type activity_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: None or ClientRawResponse if raw=true
        :rtype: None or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.connector.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.delete_activity.metadata["url"]
        path_format_arguments = {
            "conversationId": self._serialize.url(
                "conversation_id", conversation_id, "str"
            ),
            "activityId": self._serialize.url("activity_id", activity_id, "str"),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.delete(url, query_parameters, header_parameters)
        response = await self._client.async_send(
            request, stream=False, **operation_config
        )

        if response.status_code not in [200, 202]:
            raise models.ErrorResponseException(self._deserialize, response)

        if raw:
            client_raw_response = ClientRawResponse(None, response)
            return client_raw_response

    delete_activity.metadata = {
        "url": "/v3/conversations/{conversationId}/activities/{activityId}"
    }

    async def get_conversation_members(
        self, conversation_id, *, custom_headers=None, raw=False, **operation_config
    ):
        """GetConversationMembers.

        Enumerate the members of a conversation.
        This REST API takes a ConversationId and returns an array of
        ChannelAccount objects representing the members of the conversation.

        :param conversation_id: Conversation ID
        :type conversation_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: list or ClientRawResponse if raw=true
        :rtype: list[~botframework.connector.models.ChannelAccount] or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.connector.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.get_conversation_members.metadata["url"]
        path_format_arguments = {
            "conversationId": self._serialize.url(
                "conversation_id", conversation_id, "str"
            )
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = await self._client.async_send(
            request, stream=False, **operation_config
        )

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("[ChannelAccount]", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    get_conversation_members.metadata = {
        "url": "/v3/conversations/{conversationId}/members"
    }

    async def get_conversation_member(
        self,
        conversation_id,
        member_id,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """GetConversationMember.

        Get a member of a conversation.
        This REST API takes a ConversationId and memberId and returns a
        ChannelAccount object representing the member of the conversation.

        :param conversation_id: Conversation Id
        :type conversation_id: str
        :param member_id: Member Id
        :type member_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: list or ClientRawResponse if raw=true
        :rtype: list[~botframework.connector.models.ChannelAccount] or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.connector.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.get_conversation_member.metadata["url"]
        path_format_arguments = {
            "conversationId": self._serialize.url(
                "conversation_id", conversation_id, "str"
            ),
            "memberId": self._serialize.url("member_id", member_id, "str"),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = await self._client.async_send(
            request, stream=False, **operation_config
        )

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("ChannelAccount", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    get_conversation_member.metadata = {
        "url": "/v3/conversations/{conversationId}/members/{memberId}"
    }

    async def get_conversation_paged_members(
        self,
        conversation_id,
        page_size=None,
        continuation_token=None,
        *,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """GetConversationPagedMembers.

        Enumerate the members of a conversation one page at a time.
        This REST API takes a ConversationId. Optionally a pageSize and/or
        continuationToken can be provided. It returns a PagedMembersResult,
        which contains an array
        of ChannelAccounts representing the members of the conversation and a
        continuation token that can be used to get more values.
        One page of ChannelAccounts records are returned with each call. The
        number of records in a page may vary between channels and calls. The
        pageSize parameter can be used as
        a suggestion. If there are no additional results the response will not
        contain a continuation token. If there are no members in the
        conversation the Members will be empty or not present in the response.
        A response to a request that has a continuation token from a prior
        request may rarely return members from a previous request.

        :param conversation_id: Conversation ID
        :type conversation_id: str
        :param page_size: Suggested page size
        :type page_size: int
        :param continuation_token: Continuation Token
        :type continuation_token: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: PagedMembersResult or ClientRawResponse if raw=true
        :rtype: ~botframework.connector.models.PagedMembersResult or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.get_conversation_paged_members.metadata["url"]
        path_format_arguments = {
            "conversationId": self._serialize.url(
                "conversation_id", conversation_id, "str"
            )
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        if page_size is not None:
            query_parameters["pageSize"] = self._serialize.query(
                "page_size", page_size, "int"
            )
        if continuation_token is not None:
            query_parameters["continuationToken"] = self._serialize.query(
                "continuation_token", continuation_token, "str"
            )

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = await self._client.async_send(
            request, stream=False, **operation_config
        )

        if response.status_code not in [200]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("PagedMembersResult", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    get_conversation_paged_members.metadata = {
        "url": "/v3/conversations/{conversationId}/pagedmembers"
    }

    async def get_teams_conversation_paged_members(
        self,
        conversation_id,
        page_size=None,
        continuation_token=None,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """GetTeamsConversationPagedMembers.

        Enumerate the members of a Teams conversation one page at a time.
        This REST API takes a ConversationId. Optionally a pageSize and/or
        continuationToken can be provided. It returns a PagedMembersResult,
        which contains an array
        of ChannelAccounts representing the members of the conversation and a
        continuation token that can be used to get more values.
        One page of ChannelAccounts records are returned with each call. The
        number of records in a page may vary between channels and calls. The
        pageSize parameter can be used as
        a suggestion. If there are no additional results the response will not
        contain a continuation token. If there are no members in the
        conversation the Members will be empty or not present in the response.
        A response to a request that has a continuation token from a prior
        request may rarely return members from a previous request.

        :param conversation_id: Conversation ID
        :type conversation_id: str
        :param page_size: Suggested page size
        :type page_size: int
        :param continuation_token: Continuation Token
        :type continuation_token: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: PagedMembersResult or ClientRawResponse if raw=true
        :rtype: ~botframework.connector.models.PagedMembersResult or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.get_conversation_paged_members.metadata["url"]
        path_format_arguments = {
            "conversationId": self._serialize.url(
                "conversation_id", conversation_id, "str"
            )
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        if page_size is not None:
            query_parameters["pageSize"] = self._serialize.query(
                "page_size", page_size, "int"
            )
        if continuation_token is not None:
            query_parameters["continuationToken"] = self._serialize.query(
                "continuation_token", continuation_token, "str"
            )

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = await self._client.async_send(
            request, stream=False, **operation_config
        )

        if response.status_code not in [200]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("TeamsPagedMembersResult", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    get_conversation_paged_members.metadata = {
        "url": "/v3/conversations/{conversationId}/pagedmembers"
    }

    async def delete_conversation_member(
        self,
        conversation_id,
        member_id,
        *,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """DeleteConversationMember.

        Deletes a member from a conversation.
        This REST API takes a ConversationId and a memberId (of type string)
        and removes that member from the conversation. If that member was the
        last member
        of the conversation, the conversation will also be deleted.

        :param conversation_id: Conversation ID
        :type conversation_id: str
        :param member_id: ID of the member to delete from this conversation
        :type member_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: None or ClientRawResponse if raw=true
        :rtype: None or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.connector.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.delete_conversation_member.metadata["url"]
        path_format_arguments = {
            "conversationId": self._serialize.url(
                "conversation_id", conversation_id, "str"
            ),
            "memberId": self._serialize.url("member_id", member_id, "str"),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.delete(url, query_parameters, header_parameters)
        response = await self._client.async_send(
            request, stream=False, **operation_config
        )

        if response.status_code not in [200, 204]:
            raise models.ErrorResponseException(self._deserialize, response)

        if raw:
            client_raw_response = ClientRawResponse(None, response)
            return client_raw_response

    delete_conversation_member.metadata = {
        "url": "/v3/conversations/{conversationId}/members/{memberId}"
    }

    async def get_activity_members(
        self,
        conversation_id,
        activity_id,
        *,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """GetActivityMembers.

        Enumerate the members of an activity.
        This REST API takes a ConversationId and a ActivityId, returning an
        array of ChannelAccount objects representing the members of the
        particular activity in the conversation.

        :param conversation_id: Conversation ID
        :type conversation_id: str
        :param activity_id: Activity ID
        :type activity_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: list or ClientRawResponse if raw=true
        :rtype: list[~botframework.connector.models.ChannelAccount] or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.connector.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.get_activity_members.metadata["url"]
        path_format_arguments = {
            "conversationId": self._serialize.url(
                "conversation_id", conversation_id, "str"
            ),
            "activityId": self._serialize.url("activity_id", activity_id, "str"),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = await self._client.async_send(
            request, stream=False, **operation_config
        )

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("[ChannelAccount]", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    get_activity_members.metadata = {
        "url": "/v3/conversations/{conversationId}/activities/{activityId}/members"
    }

    async def upload_attachment(
        self,
        conversation_id,
        attachment_upload,
        *,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """UploadAttachment.

        Upload an attachment directly into a channel's blob storage.
        This is useful because it allows you to store data in a compliant store
        when dealing with enterprises.
        The response is a ResourceResponse which contains an AttachmentId which
        is suitable for using with the attachments API.

        :param conversation_id: Conversation ID
        :type conversation_id: str
        :param attachment_upload: Attachment data
        :type attachment_upload: ~botframework.connector.models.AttachmentData
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ResourceResponse or ClientRawResponse if raw=true
        :rtype: ~botframework.connector.models.ResourceResponse or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.connector.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.upload_attachment.metadata["url"]
        path_format_arguments = {
            "conversationId": self._serialize.url(
                "conversation_id", conversation_id, "str"
            )
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        header_parameters["Content-Type"] = "application/json; charset=utf-8"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        body_content = self._serialize.body(attachment_upload, "AttachmentData")

        # Construct and send request
        request = self._client.post(
            url, query_parameters, header_parameters, body_content
        )
        response = await self._client.async_send(
            request, stream=False, **operation_config
        )

        if response.status_code not in [200, 201, 202]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("ResourceResponse", response)
        if response.status_code == 201:
            deserialized = self._deserialize("ResourceResponse", response)
        if response.status_code == 202:
            deserialized = self._deserialize("ResourceResponse", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    upload_attachment.metadata = {
        "url": "/v3/conversations/{conversationId}/attachments"
    }
