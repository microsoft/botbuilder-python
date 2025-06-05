# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from aiohttp.web import HTTPException
from typing import List
from msrest.pipeline import ClientRawResponse
from msrest.exceptions import HttpOperationError

from botbuilder.schema import Activity
from botframework.connector.retry_action import RetryAction

from ... import models


class TeamsOperations(object):
    """TeamsOperations operations.

    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    """

    models = models

    def __init__(self, client, config, serializer, deserializer):
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer

        self.config = config

    def get_teams_channels(
        self, team_id, custom_headers=None, raw=False, **operation_config
    ):
        """Fetches channel list for a given team.

        Fetch the channel list.

        :param team_id: Team Id
        :type team_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ConversationList or ClientRawResponse if raw=true
        :rtype: ~botframework.connector.teams.models.ConversationList or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.get_teams_channels.metadata["url"]
        path_format_arguments = {
            "teamId": self._serialize.url("team_id", team_id, "str")
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
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize("ConversationList", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    get_teams_channels.metadata = {"url": "/v3/teams/{teamId}/conversations"}

    def get_team_details(
        self, team_id, custom_headers=None, raw=False, **operation_config
    ):
        """Fetches details related to a team.

        Fetch details for a team.

        :param team_id: Team Id
        :type team_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: TeamDetails or ClientRawResponse if raw=true
        :rtype: ~botframework.connector.teams.models.TeamDetails or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.get_team_details.metadata["url"]
        path_format_arguments = {
            "teamId": self._serialize.url("team_id", team_id, "str")
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
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize("TeamDetails", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    get_team_details.metadata = {"url": "/v3/teams/{teamId}"}

    def fetch_participant(
        self,
        meeting_id: str,
        participant_id: str,
        tenant_id: str,
        custom_headers=None,
        raw=False,
        **operation_config,
    ):
        """Fetches Teams meeting participant details.

        :param meeting_id: Teams meeting id
        :type meeting_id: str
        :param participant_id: Teams meeting participant id
        :type participant_id: str
        :param tenant_id: Teams meeting tenant id
        :type tenant_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: TeamsMeetingParticipant or ClientRawResponse if raw=true
        :rtype: ~botframework.connector.teams.models.TeamsParticipantChannelAccount or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """

        # Construct URL
        url = self.fetch_participant.metadata["url"]
        path_format_arguments = {
            "meetingId": self._serialize.url("meeting_id", meeting_id, "str"),
            "participantId": self._serialize.url(
                "participant_id", participant_id, "str"
            ),
            "tenantId": self._serialize.url("tenant_id", tenant_id, "str"),
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
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize("TeamsMeetingParticipant", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    fetch_participant.metadata = {
        "url": "/v1/meetings/{meetingId}/participants/{participantId}?tenantId={tenantId}"
    }

    def fetch_meeting(
        self, meeting_id: str, custom_headers=None, raw=False, **operation_config
    ):
        """Fetch meeting information.

        :param meeting_id: Meeting Id, encoded as a BASE64 string.
        :type meeting_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: MeetingInfo or ClientRawResponse if raw=true
        :rtype: ~botframework.connector.teams.models.MeetingInfo or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """

        # Construct URL
        url = self.fetch_participant.metadata["url"]
        path_format_arguments = {
            "meetingId": self._serialize.url("meeting_id", meeting_id, "str")
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
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise HttpOperationError(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize("MeetingInfo", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    fetch_participant.metadata = {"url": "/v1/meetings/{meetingId}"}

    def send_meeting_notification(
        self,
        meeting_id: str,
        notification: models.MeetingNotificationBase,
        custom_headers=None,
        raw=False,
        **operation_config,
    ):
        """Send a teams meeting notification.

        :param meeting_id: Meeting Id, encoded as a BASE64 string.
        :type meeting_id: str
        :param notification: The notification to send to Teams
        :type notification: ~botframework.connector.teams.models.MeetingNotificationBase
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: MeetingNotificationResponse or ClientRawResponse if raw=true
        :rtype: ~botframework.connector.teams.models.MeetingNotificationResponse or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """

        # Construct URL
        url = self.send_meeting_notification.metadata["url"]
        path_format_arguments = {
            "meetingId": self._serialize.url("meeting_id", meeting_id, "str"),
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
        body_content = self._serialize.body(notification, "notification")

        # Construct and send request
        request = self._client.post(
            url, query_parameters, header_parameters, body_content
        )
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200, 201, 202]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("MeetingNotificationResponse", response)
        if response.status_code == 201:
            deserialized = self._deserialize("MeetingNotificationResponse", response)
        if response.status_code == 202:
            deserialized = self._deserialize("MeetingNotificationResponse", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    send_meeting_notification.metadata = {
        "url": "/v1/meetings/{meetingId}/notification"
    }

    async def send_message_to_list_of_users(
        self,
        activity: Activity,
        teams_members: List[models.TeamMember],
        tenant_id: str,
        custom_headers=None,
        raw=False,
        **operation_config,
    ):
        """
        Send a message to a list of Teams members.

        :param activity: The activity to send.
        :type activity: ~botframework.connector.models.Activity
        :param teams_members: The tenant ID.
        :type teams_members: list[~botframework.connector.teams.models.TeamMember].
        :param tenant_id: The tenant ID.
        :type tenant_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: A response object containing the operation id.
        :rtype: str or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """

        if activity is None:
            raise ValueError(f"{activity} is required")
        if not teams_members:
            raise ValueError(f"{teams_members} is required")
        if not tenant_id:
            raise ValueError(f"{tenant_id} is required")

        content = {
            "members": teams_members,
            "activity": activity,
            "tenant_id": tenant_id,
        }

        async def task(_):
            api_url = "v3/batch/conversation/users/"

            # Construct parameters
            query_parameters = {}

            # Construct headers
            header_parameters = {}
            header_parameters["Accept"] = "application/json"
            header_parameters["Content-Type"] = "application/json; charset=utf-8"
            if custom_headers:
                header_parameters.update(custom_headers)

            # Construct body
            body_content = self._serialize.body(content, "content")

            # Construct and send request
            request = self._client.post(
                api_url, query_parameters, header_parameters, body_content
            )
            response = self._client.send(request, stream=False, **operation_config)

            if response.status_code not in [200, 201, 202]:
                raise models.ErrorResponseException(self._deserialize, response)

            deserialized = None
            if response.status_code in {200, 201, 202}:
                deserialized = self._deserialize(response)

            if raw:
                client_raw_response = ClientRawResponse(deserialized, response)
                return client_raw_response

            return deserialized

        def retry_exception_handler(exception, _):
            if isinstance(exception, HTTPException) and exception.status_code == 429:
                return 429
            return None

        return await RetryAction.run_async(
            task, retry_exception_handler=retry_exception_handler
        )

    async def send_message_to_all_users_in_tenant(
        self,
        activity: Activity,
        tenant_id: str,
        custom_headers=None,
        raw=False,
        **operation_config,
    ):
        if activity is None:
            raise ValueError(f"{activity} is required")
        if not tenant_id:
            raise ValueError(f"{tenant_id} is required")

        content = {"activity": activity, "tenant_id": tenant_id}

        async def task(_):
            api_url = "v3/batch/conversation/tenant/"

            # Construct parameters
            query_parameters = {}

            # Construct headers
            header_parameters = {}
            header_parameters["Accept"] = "application/json"
            header_parameters["Content-Type"] = "application/json; charset=utf-8"
            if custom_headers:
                header_parameters.update(custom_headers)

            # Construct body
            body_content = self._serialize.body(content, "content")

            # Construct and send request
            request = self._client.post(
                api_url, query_parameters, header_parameters, body_content
            )
            response = self._client.send(request, stream=False, **operation_config)

            if response.status_code not in [200, 201, 202]:
                raise models.ErrorResponseException(self._deserialize, response)

            deserialized = None
            if response.status_code in [200, 201, 202]:
                deserialized = self._deserialize(response)

            if raw:
                client_raw_response = ClientRawResponse(deserialized, response)
                return client_raw_response

            return deserialized

        def retry_exception_handler(exception, _):
            if isinstance(exception, HTTPException) and exception.status_code == 429:
                return 429
            return None

        return await RetryAction.run_async(
            task, retry_exception_handler=retry_exception_handler
        )

    async def send_message_to_all_users_in_team(
        self,
        activity: Activity,
        team_id: str,
        tenant_id: str,
        custom_headers=None,
        raw=False,
        **operation_config,
    ):
        if activity is None:
            raise ValueError(f"{activity} is required")
        if not team_id:
            raise ValueError(f"{team_id} is required")
        if not tenant_id:
            raise ValueError(f"{tenant_id} is required")

        content = {"activity": activity, "team_id": team_id, "tenant_id": tenant_id}

        async def task(_):
            api_url = "v3/batch/conversation/team/"

            # Construct parameters
            query_parameters = {}

            # Construct headers
            header_parameters = {}
            header_parameters["Accept"] = "application/json"
            header_parameters["Content-Type"] = "application/json; charset=utf-8"
            if custom_headers:
                header_parameters.update(custom_headers)

            # Construct body
            body_content = self._serialize.body(content, "content")

            # Construct and send request
            request = self._client.post(
                api_url, query_parameters, header_parameters, body_content
            )
            response = self._client.send(request, stream=False, **operation_config)

            if response.status_code not in [200, 201, 202]:
                raise models.ErrorResponseException(self._deserialize, response)

            deserialized = None
            if response.status_code in [200, 201, 202]:
                deserialized = self._deserialize(response)

            if raw:
                client_raw_response = ClientRawResponse(deserialized, response)
                return client_raw_response

            return deserialized

        def retry_exception_handler(exception, _):
            if isinstance(exception, HTTPException) and exception.status_code == 429:
                return 429
            return None

        return await RetryAction.run_async(
            task, retry_exception_handler=retry_exception_handler
        )

    async def send_message_to_list_of_channels(
        self,
        activity: Activity,
        channels_members: List[models.TeamMember],
        tenant_id: str,
        custom_headers=None,
        raw=False,
        **operation_config,
    ):
        if activity is None:
            raise ValueError(f"{activity} is required")
        if not channels_members:
            raise ValueError(f"{channels_members} is required")
        if not tenant_id:
            raise ValueError(f"{tenant_id} is required")

        content = {
            "activity": activity,
            "members": channels_members,
            "tenant_id": tenant_id,
        }

        async def task(_):
            api_url = "v3/batch/conversation/channels/"

            # Construct parameters
            query_parameters = {}

            # Construct headers
            header_parameters = {}
            header_parameters["Accept"] = "application/json"
            header_parameters["Content-Type"] = "application/json; charset=utf-8"
            if custom_headers:
                header_parameters.update(custom_headers)

            # Construct body
            body_content = self._serialize.body(content, "content")

            # Construct and send request
            request = self._client.post(
                api_url, query_parameters, header_parameters, body_content
            )
            response = self._client.send(request, stream=False, **operation_config)

            if response.status_code not in [200, 201, 202]:
                raise models.ErrorResponseException(self._deserialize, response)

            deserialized = None
            if response.status_code in [200, 201, 202]:
                deserialized = self._deserialize(response)

            if raw:
                client_raw_response = ClientRawResponse(deserialized, response)
                return client_raw_response

            return deserialized

        def retry_exception_handler(exception, _):
            if isinstance(exception, HTTPException) and exception.status_code == 429:
                return 429
            return None

        return await RetryAction.run_async(
            task, retry_exception_handler=retry_exception_handler
        )

    async def get_operation_state(
        self, operation_id: str, custom_headers=None, raw=False, **operation_config
    ):
        if not operation_id:
            raise ValueError(f"{operation_id} is required")

        async def task(_):
            api_url = "v3/batch/conversation/{operationId}"

            path_format_arguments = {
                "operationId": self._serialize.url("operation_id", operation_id, "str"),
            }
            api_url = self._client.format_url(api_url, **path_format_arguments)

            # Construct parameters
            query_parameters = {}

            # Construct headers
            header_parameters = {}
            header_parameters["Accept"] = "application/json"
            if custom_headers:
                header_parameters.update(custom_headers)

            # Construct and send request
            request = self._client.get(api_url, query_parameters, header_parameters)
            response = self._client.send(request, stream=False, **operation_config)

            if response.status_code not in [200]:
                raise HttpOperationError(self._deserialize, response)

            deserialized = None

            if response.status_code == 200:
                deserialized = self._deserialize(response)

            if raw:
                client_raw_response = ClientRawResponse(deserialized, response)
                return client_raw_response

            return deserialized

        def retry_exception_handler(exception, _):
            if isinstance(exception, HTTPException) and exception.status_code == 429:
                return 429
            return None

        return await RetryAction.run_async(
            task, retry_exception_handler=retry_exception_handler
        )

    async def get_paged_failed_entries(
        self, operation_id: str, custom_headers=None, raw=False, **operation_config
    ):
        if not operation_id:
            raise ValueError(f"{operation_id} is required")

        async def task(_):
            api_url = "v3/batch/conversation/failedentries/{operationId}"

            path_format_arguments = {
                "operationId": self._serialize.url("operation_id", operation_id, "str"),
            }
            api_url = self._client.format_url(api_url, **path_format_arguments)

            # Construct parameters
            query_parameters = {}

            # Construct headers
            header_parameters = {}
            header_parameters["Accept"] = "application/json"
            if custom_headers:
                header_parameters.update(custom_headers)

            # Construct and send request
            request = self._client.get(api_url, query_parameters, header_parameters)
            response = self._client.send(request, stream=False, **operation_config)

            if response.status_code not in [200]:
                raise HttpOperationError(self._deserialize, response)

            deserialized = None

            if response.status_code == 200:
                deserialized = self._deserialize(response)

            if raw:
                client_raw_response = ClientRawResponse(deserialized, response)
                return client_raw_response

            return deserialized

        def retry_exception_handler(exception, _):
            if isinstance(exception, HTTPException) and exception.status_code == 429:
                return 429
            return None

        return await RetryAction.run_async(
            task, retry_exception_handler=retry_exception_handler
        )

    async def cancel_operation(
        self, operation_id: str, custom_headers=None, raw=False, **operation_config
    ):
        if not operation_id:
            raise ValueError(f"{operation_id} is required")

        async def task(_):
            api_url = "v3/batch/conversation/{operationId}"

            path_format_arguments = {
                "operationId": self._serialize.url("operation_id", operation_id, "str"),
            }
            api_url = self._client.format_url(api_url, **path_format_arguments)

            # Construct parameters
            query_parameters = {}

            # Construct headers
            header_parameters = {}
            header_parameters["Accept"] = "application/json"
            if custom_headers:
                header_parameters.update(custom_headers)

            # Construct and send request
            request = self._client.delete(api_url, query_parameters, header_parameters)
            response = self._client.send(request, stream=False, **operation_config)

            if response.status_code not in [200]:
                raise HttpOperationError(self._deserialize, response)

            deserialized = None

            if response.status_code == 200:
                deserialized = self._deserialize(response)

            if raw:
                client_raw_response = ClientRawResponse(deserialized, response)
                return client_raw_response

            return deserialized

        def retry_exception_handler(exception, _):
            if isinstance(exception, HTTPException) and exception.status_code == 429:
                return 429
            return None

        return await RetryAction.run_async(
            task, retry_exception_handler=retry_exception_handler
        )
