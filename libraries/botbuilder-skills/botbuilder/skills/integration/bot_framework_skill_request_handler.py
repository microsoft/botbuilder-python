# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import re
from re import Pattern
from typing import Awaitable, Callable, Dict, List

from flask import Request, Response

from botbuilder.core import Bot, BotAdapter
from botframework.connector.auth import (
    AuthenticationConfiguration,
    ChannelProvider,
    ClaimsIdentity,
    CredentialProvider,
    JwtTokenValidation,
)

from .actions import (
    get_activity_members_action,
    send_conversation_history_action,
    reply_to_activity_action,
    update_activity_action,
    delete_activity_action,
    send_to_conversaiton_action,
    delete_conversation_member_action,
    upload_attachment_action,
    get_conversation_members_action,
    get_conversation_paged_members_action,
    get_conversations_action,
    create_conversation_action,
)
from ..bot_framework_skill_client import BotFrameworkClient
from ..channel_api_methods import ChannelApiMethods
from ..http_helper import HttpHelper

RouteAction = Callable[
    [BotAdapter, BotFrameworkClient, Bot, ClaimsIdentity, Request, Dict[str, str]],
    Awaitable[object],
]


class ChannelRoute:
    def __init__(
        self, method: str = None, pattern: Pattern = None, action: RouteAction = None
    ):
        self.pattern = pattern
        self.method = method
        self.action = action


class RouteResult:
    def __init__(
        self,
        method: str = None,
        parameters: Dict[str, str] = None,
        action: RouteAction = None,
    ):
        self.method = method
        self.parameters = parameters
        self.action = action


class BotFrameworkSkillRequestHandler:

    _ROUTES: List[ChannelRoute] = [
        ChannelRoute(
            method=ChannelApiMethods.GET_ACTIVITY_MEMBERS,
            pattern=re.compile(
                r"/GET:(?P<path>.*)/v3/conversations/(?P<conversation_id>[^\s/]*)"
                r"/activities/(?P<activity_id>.*)/members",
                flags=re.IGNORECASE,
            ),
            action=get_activity_members_action,
        ),
        ChannelRoute(
            method=ChannelApiMethods.SEND_CONVERSATION_HISTORY,
            pattern=re.compile(
                r"/POST:(?P<path>.*)/v3/conversations/(?P<conversation_id>[^\s/]*)/activities/history",
                flags=re.IGNORECASE,
            ),
            action=send_conversation_history_action,
        ),
        ChannelRoute(
            method=ChannelApiMethods.REPLY_TO_ACTIVITY,
            pattern=re.compile(
                r"/POST:(?P<path>.*)/v3/conversations/(?P<conversation_id>[^\s/]*)/activities/(?P<activity_id>.*)?",
                flags=re.IGNORECASE,
            ),
            action=reply_to_activity_action,
        ),
        ChannelRoute(
            method=ChannelApiMethods.UPDATE_ACTIVITY,
            pattern=re.compile(
                r"/PUT:(?P<path>.*)/v3/conversations/(?P<conversation_id>[^\s/]*)/activities/(?P<activity_id>.*)?",
                flags=re.IGNORECASE,
            ),
            action=update_activity_action,
        ),
        ChannelRoute(
            method=ChannelApiMethods.DELETE_ACTIVITY,
            pattern=re.compile(
                r"/DELETE:(?P<path>.*)/v3/conversations/(?P<conversation_id>[^\s/]*)/activities/(?P<activity_id>.*)?",
                flags=re.IGNORECASE,
            ),
            action=delete_activity_action,
        ),
        ChannelRoute(
            method=ChannelApiMethods.SEND_TO_CONVERSATION,
            pattern=re.compile(
                r"/POST:(?P<path>.*)/v3/conversations/(?P<conversation_id>[^\s/]*)/activities",
                flags=re.IGNORECASE,
            ),
            action=send_to_conversaiton_action,
        ),
        ChannelRoute(
            method=ChannelApiMethods.DELETE_CONVERSATION_MEMBER,
            pattern=re.compile(
                r"/DELETE:(?P<path>.*)/v3/conversations/(?P<conversation_id>[^\s/]*)/members/(?P<member_id>.*)",
                flags=re.IGNORECASE,
            ),
            action=delete_conversation_member_action,
        ),
        ChannelRoute(
            method=ChannelApiMethods.UPLOAD_ATTACHMENT,
            pattern=re.compile(
                r"/POST:(?P<path>.*)/v3/conversations/(?P<conversation_id>[^\s/]*)/attachments",
                flags=re.IGNORECASE,
            ),
            action=upload_attachment_action,
        ),
        ChannelRoute(
            method=ChannelApiMethods.GET_CONVERSATION_MEMBERS,
            pattern=re.compile(
                r"/GET:(?P<path>.*)/v3/conversations/(?P<conversation_id>[^\s/]*)/members",
                flags=re.IGNORECASE,
            ),
            action=get_conversation_members_action,
        ),
        ChannelRoute(
            method=ChannelApiMethods.GET_CONVERSATION_PAGED_MEMBERS,
            pattern=re.compile(
                r"/GET:(?P<path>.*)/v3/conversations/(?P<conversation_id>[^\s/]*)/pagedmember",
                flags=re.IGNORECASE,
            ),
            action=get_conversation_paged_members_action,
        ),
        ChannelRoute(
            method=ChannelApiMethods.GET_CONVERSATIONS,
            pattern=re.compile(
                r"/GET:(?P<path>.*)/v3/conversations/", flags=re.IGNORECASE
            ),
            action=get_conversations_action,
        ),
        ChannelRoute(
            method=ChannelApiMethods.CREATE_CONVERSATION,
            pattern=re.compile(
                r"/POST:(?P<path>.*)/v3/conversations/", flags=re.IGNORECASE
            ),
            action=create_conversation_action,
        ),
    ]

    def __init__(
        self,
        skill_client: BotFrameworkClient,
        credential_provider: CredentialProvider,
        auth_config: AuthenticationConfiguration,
        channel_provider: ChannelProvider = None,
    ):
        if not credential_provider:
            raise TypeError("credential_provider cannot be None")

        if not auth_config:
            raise TypeError("auth_config cannot be None")

        self._skill_client = skill_client
        self._credential_provider = credential_provider
        self._auth_config = auth_config
        self._channel_provider = channel_provider

    async def process(
        self, request: Request, response: Response, adapter: BotAdapter, bot: Bot
    ):
        if not request:
            raise TypeError("request cannot be None")

        if not response:
            raise TypeError("response cannot be None")

        if not bot:
            raise TypeError("bot cannot be None")

        result = None
        status_code = 200
        try:
            # grab the auth header from the inbound http request
            auth_header = request.headers["Authorization"]
            claims_identity = await JwtTokenValidation.validate_auth_header(
                auth_header,
                self._credential_provider,
                self._channel_provider.channel_service,
                "unknown",
                auth_configuration=self._auth_config,
            )

            route = BotFrameworkSkillRequestHandler._get_route(request)
            if not route:
                response.status_code = 404
                return

            return await route.action(
                adapter,
                self._skill_client,
                bot,
                claims_identity,
                request,
                route.parameters,
            )
        except:
            status_code = 401

        HttpHelper.write_response(response, status_code, result)

    @staticmethod
    async def _get_route(request: Request) -> RouteResult:
        path = f"/{request.method}:{request.path}"
        for route in BotFrameworkSkillRequestHandler._ROUTES:
            match = route.pattern.match(path)
            if match:
                result = RouteResult(method=route.method, parameters=match.groupdict())

                return result

        return None
