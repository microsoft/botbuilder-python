# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from msrest.pipeline import ClientRawResponse
from msrest.exceptions import HttpOperationError

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
        **operation_config
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
