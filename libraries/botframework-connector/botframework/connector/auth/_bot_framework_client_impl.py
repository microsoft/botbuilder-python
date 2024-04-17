# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from copy import deepcopy
from json import dumps, loads
from logging import Logger

from botbuilder.schema import (
    Activity,
    ConversationReference,
    ConversationAccount,
    ChannelAccount,
    InvokeResponse,
    RoleTypes,
)

from ..http_client_factory import HttpClientFactory
from ..http_request import HttpRequest
from .._not_implemented_http_client import _NotImplementedHttpClient
from ..skills.bot_framework_client import BotFrameworkClient

from .service_client_credentials_factory import ServiceClientCredentialsFactory


class _BotFrameworkClientImpl(BotFrameworkClient):
    def __init__(
        self,
        credentials_factory: ServiceClientCredentialsFactory,
        http_client_factory: HttpClientFactory,
        login_endpoint: str,
        logger: Logger = None,
    ):
        self._credentials_factory = credentials_factory
        self._http_client = (
            http_client_factory.create_client()
            if http_client_factory
            else _NotImplementedHttpClient()
        )
        self._login_endpoint = login_endpoint
        self._logger = logger

    async def post_activity(
        self,
        from_bot_id: str,
        to_bot_id: str,
        to_url: str,
        service_url: str,
        conversation_id: str,
        activity: Activity,
    ) -> InvokeResponse:
        if not to_url:
            raise TypeError("to_url")
        if not service_url:
            raise TypeError("service_url")
        if not conversation_id:
            raise TypeError("conversation_id")
        if not activity:
            raise TypeError("activity")

        if self._logger:
            self._logger.log(20, f"post to skill '{to_bot_id}' at '{to_url}'")

        credentials = await self._credentials_factory.create_credentials(
            from_bot_id, to_bot_id, self._login_endpoint, True
        )

        # Get token for the skill call
        token = credentials.get_access_token() if credentials.microsoft_app_id else None

        # Clone the activity so we can modify it before sending without impacting the original object.
        activity_copy = deepcopy(activity)

        # Apply the appropriate addressing to the newly created Activity.
        activity_copy.relates_to = ConversationReference(
            service_url=activity_copy.service_url,
            activity_id=activity_copy.id,
            channel_id=activity_copy.channel_id,
            conversation=ConversationAccount(
                id=activity_copy.conversation.id,
                name=activity_copy.conversation.name,
                conversation_type=activity_copy.conversation.conversation_type,
                aad_object_id=activity_copy.conversation.aad_object_id,
                is_group=activity_copy.conversation.is_group,
                role=activity_copy.conversation.role,
                tenant_id=activity_copy.conversation.tenant_id,
                properties=activity_copy.conversation.properties,
            ),
            bot=None,
        )
        activity_copy.conversation.id = conversation_id
        activity_copy.service_url = service_url
        if not activity_copy.recipient:
            activity_copy.recipient = ChannelAccount(role=RoleTypes.skill)
        else:
            activity_copy.recipient.role = RoleTypes.skill

        headers_dict = {
            "Content-type": "application/json; charset=utf-8",
            "x-ms-conversation-id": conversation_id,
        }
        if token:
            headers_dict.update(
                {
                    "Authorization": f"Bearer {token}",
                }
            )
        json_content = dumps(activity_copy.serialize()).encode("utf-8")

        request = HttpRequest(
            request_uri=to_url, content=json_content, headers=headers_dict
        )
        response = await self._http_client.post(request=request)

        data = await response.read_content_str()

        if not await response.is_succesful() and self._logger:
            # Otherwise we can assume we don't have to deserialize - so just log the content so it's not lost.
            self._logger.log(
                40,
                f"Bot Framework call failed to '{to_url}' returning '{int(response.status_code)}' and '{data}'",
            )

        return InvokeResponse(
            status=response.status_code, body=loads(data) if data else None
        )
